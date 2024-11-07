Application Segment Management Example
======================================

This script contains several examples that can be executed from the CLI to create/read/update/delete Application Segment resources in the Zscaler Private Access (ZPA) service. See the [README](../README.md) for authentication requirements. The examples in this folder assume that environment variables are being used as the authentication method.

### Listing All Application Segments

```shell
$ python3 application_segment_management.py -l
```

### Get Details of a Specific Application Segment

```shell
$ python3 application_segment_management.py -g APP_SEGMENT_ID
```

### Add a New Application Segment

```shell
$ python3 application_segment_management.py --add --name "New App Segment" --domain_names example.com --segment_group_id "216196257331370167" --server_group_ids "216196257331370169" --tcp_port_ranges '80,80' --udp_port_ranges '1000,1000'
```

### Update an Existing Application Segment

```shell
$ python3 application_segment_management.py --update APP_SEGMENT_ID --name "Updated App Segment" --description "New description"
```

### Delete an Application Segment

```shell
$ python3 application_segment_management.py -d APP_SEGMENT_ID

```
