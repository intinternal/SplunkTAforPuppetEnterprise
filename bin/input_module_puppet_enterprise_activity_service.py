
# encoding = utf-8

import os
import sys
import time
import datetime
import json
import jsonpath_rw
from datetime import datetime

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

def collect_events(helper, ew):
   
    import datetime
    import json
    import jsonpath_rw
    
    method = 'GET'
    api_request = 'application/json' 
    
    api_token = helper.get_global_setting("api_token")
    server = helper.get_arg('server')
    port = helper.get_arg('port')
    service_id = helper.get_arg('service_id')
    
    #get current time
    now = datetime.datetime.now()
    
    #get checkpoint value
    ckpt = service_id + "_start_time"
    ckpt_value = helper.get_check_point(ckpt)

    #if there is no checkpoint value - that means its an initial load - set start time to now - 5 Minute
    if ckpt_value == None:
        old = now - datetime.timedelta(minutes=5)
        #format the time
        # This is a timestamp in UTC-based ISO-8601 format (YYYY-MM-DDThh:mm:ssZ) 
        start_time = old.strftime("%Y-%m-%dT%H:%M:%SZ") 
    #if it does exist then checkpoint value is start time
    else:
        start_time=ckpt_value

    end_time=now.strftime("%Y-%m-%dT%H:%M:%SZ") 

    
    url = server + ":" + port + "/activity-api/v1/events?service_id=" + service_id
    
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
    helper.log_error (response.text) 
    
    r= response.json()
     
    input_type = helper.get_input_type()
    for stanza_name in helper.get_input_stanza_names():
        
        for one_dict in r['commits']:
            data = json.dumps(one_dict,sort_keys=False)
            data['_service_id'] = service_id
        
            event = helper.new_event(source=input_type, index=helper.get_output_index(stanza_name), sourcetype=helper .get_sourcetype(stanza_name), data=data)
            helper.log_error (response.text) 
            try:
                ew.write_event(event)
                helper.log_error (response.text) 
            except Exception as e:
                raise e
        return;
    
    #save checkpoint value to end_time which is data collection time
    ckpt_value = helper.save_check_point(ckpt, end_time)
