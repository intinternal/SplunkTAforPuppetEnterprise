# encoding = utf-8

import os
import sys
import json


def validate_input(helper, definition):
    """Implement your own validation logic to validate the input stanza configurations"""
    # This example accesses the modular input variable
    # server = definition.parameters.get('server', None)
    # port = definition.parameters.get('port', None)
    pass


def validate_input(helper, definition):
    """Implement your own validation logic to validate the input stanza configurations"""
    # This example accesses the modular input variable
    # server = definition.parameters.get('server', None)
    # port = definition.parameters.get('port', None)
    pass


def get_data(helper, offset):
    server = helper.get_arg('server')
    port = helper.get_arg('port')
    service_id = helper.get_arg('service_id')
    api_token = helper.get_global_setting("api_token")

    method = 'GET'
    api_request = 'application/json' 

    url = server + ":" + port + "/activity-api/v1/events?service_id=" + service_id
    url += "&limit=10"  # TODO for debugging
    if offset is not None:
        url += "&offset={}".format(offset)
    
    headers = {
           'X-Authentication': api_token, 
           'Content-type': api_request
           }
           
    response = helper.send_http_request(url, 
                                        method, 
                                        parameters=None, 
                                        payload=None,
                                        headers=headers, 
                                        cookies=None, 
                                        verify=False, 
                                        cert=None,
                                        timeout=None, 
                                        use_proxy=True)
     
    r_status = response.status_code
    response.raise_for_status()
    helper.log_error(response.text) 
    
    return response.json()


def write_events(helper, ew, events_data):
    service_id = helper.get_arg('service_id')
    input_type = helper.get_input_type()

    for stanza_name in helper.get_input_stanza_names():
        for one_dict in events_data:
            one_dict['_service_id'] = service_id
            data = json.dumps(one_dict, sort_keys=False)
        
            event = helper.new_event(source=input_type, index=helper.get_output_index(stanza_name), sourcetype=helper.get_sourcetype(stanza_name), data=data)
            ew.write_event(event)
        return


def collect_events(helper, ew):
    #get checkpoint value
    service_id = helper.get_arg('service_id')
    offset_ckpt_str = service_id + "_offset"
    stop_offset_ckpt_str = service_id + "_stop_offset"
    total_ckpt_str = service_id + "_total"

    offset_ckpt = helper.get_check_point(offset_ckpt_str)  # Will be 0 if we were caught up on previous run
    stop_offset_ckpt = helper.get_check_point(stop_offset_ckpt_str)  # Only valid if offset_ckpt != 0 or None. Get UP TO this value.
    previous_total = helper.get_check_point(total_ckpt_str)
    previous_total = previous_total if previous_total is not None else 0

    # Query first to figure out how many new records there are
    data = get_data(helper, offset_ckpt)
    total_rows = data['total-rows']
    limit = data['limit']
    new_rows = total_rows - previous_total
    helper.log_info('Got {} new rows. Previous total {}, current total {}'.format(new_rows, previous_total, total_rows))
    helper.save_check_point(total_ckpt_str, total_rows)

    if offset_ckpt is None or offset_ckpt == 0:  # We are getting new data
        if new_rows <= limit:  # We can get all
            events_data = data['commits'][:new_rows]
            helper.save_check_point(offset_ckpt_str, 0)
        else:  # We need to catch up on the next run
            events_data = data['commits']
            helper.save_check_point(offset_ckpt_str, limit)
            helper.save_check_point(stop_offset_ckpt_str, new_rows)
    else:  # We are still catching up, want to get up to stop_offset_ckpt
        rows_to_get = stop_offset_ckpt - offset_ckpt
        if new_rows > limit:  # We didn't get any new data because it's coming in too fast
            helper.log_error("Data is coming in too fast. Got {} new rows, but limit is {}!".format(new_rows, limit))
            events_data = []
            helper.save_check_point(offset_ckpt_str, offset + new_rows)
            helper.save_check_point(stop_offset_ckpt_str, new_rows)
        elif rows_to_get > limit:  # We need to keep catching up on next run
            events_data = data['commits'][new_rows:]
            helper.save_check_point(offset_ckpt_str, offset_ckpt + limit)
            helper.save_check_point(stop_offset_ckpt_str, stop_offset_ckpt + new_rows)
        else:  # We can finish catching up on this run
            events_data = data['commits'][new_rows: rows_to_get + new_rows]
            helper.save_check_point(offset_ckpt_str, 0)

    write_events(helper, ew, events_data)


# If offset is not None or 0, we need to get results up to stop_offset_ckpt
#  ex. offset is 10, stop_offset_ckpt is 15. This means we want records 10 - 15 inclusive
# We will need to update stop_offset_ckpt based on the total_records in the request and in the checkpoint
# stop_offset_ckpt += new_total - total_ckpt
# if offset + limit < stop_offset_ckpt
#   offset += limit
# else:
#   offset = 0, we are back at begining
# Need to check if we are falling behind too:
# if new_total - total_ckpt >= limit: falling behind
# at end: total_ckpt
