App Connector Group Management Example
======================================

This script contains several examples that can be executed from the CLI to create/read/update/delete App Connector Group resources in the Zscaler Private Access (ZPA) service. See the [README](../README.md) for authentication requirements. The examples in this folder assume that environment variables are being used as the authentication method.

### Listing All App Connector Groups

```shell
$ python3 connector_group_management.py -l
```

### Get Details of a Specific Connector Group By ID

```shell
$ python3 connector_group_management.py -g CONNECTOR_GROUP_ID
```

### Adding a New Connector Group

```shell
$ python3 connector_group_management.py --add --name "New Connector Group" --latitude 37.3382082 --longitude -121.8863286 --location "San Jose, CA, USA", --city_country "California, US" --country_code "US"
```

### Update an Existing Connector Groups

```shell
$ python3 connector_group_management.py --update CONNECTOR_GROUP_ID --name "Updated App Connector Group" --description "New description"
```

### Delete an Connector Groups

```shell
$ python3 connector_group_management.py -d CONNECTOR_GROUP_ID

```
