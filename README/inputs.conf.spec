[puppet_enterprise_status://<name>]
server = Input your Puppet Enterprise Server
port = Input your Puppet Enterprise DB Port (HTTPS 8081, HTTP: 8080)

[puppet_enterprise_extended_details://<name>]
server = Input your Puppet Enterprise Server
port = Input your Puppet Enterprise DB Port (HTTPS 8081, HTTP: 8080)

[puppet_enterprise_aggregate_details_by_certname://<name>]
server = Input your Puppet Enterprise Server
port = Input your Puppet Enterprise DB Port (HTTPS 8081, HTTP: 8080)
summarize_by = Summarize by Type of Value (Certname, Classes or Resources)

[puppet_enterprise_aggregate_by_resource://<name>]
server = Input your Puppet Enterprise Server
port = Input your Puppet Enterprise DB Port (HTTPS 8081, HTTP: 8080)
summarize_by = Puppet Enterprise Aggregate Details by Resource

[puppet_enterprise_aggregate_details_by_classes://<name>]
server = Input your Puppet Enterprise Server
port = Input your Puppet Enterprise DB Port (HTTPS 8081, HTTP: 8080)
summarize_by = Summarize by Type of Value (Certname, Classes or Resources)

[puppet_enterprise_node_status://<name>]
server = Input your Puppet Enterprise Server
port = Input your Puppet Enterprise DB Port (HTTPS 8081, HTTP: 8080)

[puppet_enterprise_factors://<name>]
server = Input your Puppet Enterprise Server
port = Input your Puppet Enterprise DB Port (HTTPS 8081, HTTP: 8080)
environment = Puppet Enterprise Environment you want to monitor.

[puppet_enterprise_activity_service://<name>]
server = Input your Puppet Enterprise Server
port = Input your Puppet Enterprise Port (HTTPS 4433)
service_id = Service ID to query, ex. classifier or rbac
