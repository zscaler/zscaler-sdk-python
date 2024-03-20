Server Group Management Example
===============================

This script contains several examples that can be executed from the CLI to create/read/update/delete Server group resources in the Zscaler Private Access (ZPA) service. See the [README](../README.md) for authentication requirements. The examples in this folder assume that environment variables are being used as the authentication method.

### Listing All Server Groups

```shell
$ python3 server_group_management.py -l
```

### Get Details of a Specific Server Group by ID

```shell
$ python3 server_group_management.py -g GROUP_ID
```

### Get Details of a Specific Server Group by Name

```shell
$ python3 server_group_management.py -g GROUP_NAME
```

### Add a New Server Group -  Dynamic Discovery On

```shell
$ python3 server_group_management.py --add --name "New Server Group" --description "New Server Group Description" --dynamic_discovery True --enabled True --app_connector_group_ids APP_CONNECTOR_GROUP_IDS
```

### Add a New Server Group -  Dynamic Discovery Off

```shell
$ python3 server_group_management.py --add --name "New Server Group" --description "New Server Group Description" --dynamic_discovery False --enabled True --app_connector_group_ids APP_CONNECTOR_GROUP_IDS --server_ids SERVER_IDS
```

### Update an Existing Server Group

```shell
$ python3 server_group_management.py --update GROUP_ID --name "Updated Server Group" --description "Updated Server Group"
```

### Delete an Server Group

```shell
$ python3 server_group_management.py -d GROUP_ID

```
