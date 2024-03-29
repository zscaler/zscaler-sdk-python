Application Server Management Example
=====================================

This script contains several examples that can be executed from the CLI to create/read/update/delete Application Server resources in the Zscaler Private Access (ZPA) service. See the [README](../README.md) for authentication requirements. The examples in this folder assume that environment variables are being used as the authentication method.

### Listing All Application Servers

```shell
$ python3 application_server_management.py -l
```

### Get Details of a Specific Application Servers

```shell
$ python3 application_server_management.py -g SERVER_ID
```

### Add a New Application Server

```shell
$ python3 application_server_management.py --add --name "New App Server" --description "New App Server Description" --enabled true --address "192.168.100.11"
```

### Update an Existing Application Server

```shell
$ python3 application_server_management.py --update SERVER_ID --name "Updated App Server Name" --description "Updated App Server description"
```

### Delete an Application Server

```shell
$ python3 application_server_management.py -d SERVER_ID

```
