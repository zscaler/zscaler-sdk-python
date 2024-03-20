Service Edge Group Management Example
======================================

This script contains several examples that can be executed from the CLI to create/read/update/delete Service Edge Group resources in the Zscaler Private Access (ZPA) service. See the [README](../README.md) for authentication requirements. The examples in this folder assume that environment variables are being used as the authentication method.

### Listing All Service Edge Group

```shell
$ python3 service_edge_group_management.py -l
```

### Get Details of a Specific Service Edge Group By ID

```shell
$ python3 service_edge_group_management.py -g GROUP_ID
```

### Adding a New Service Edge Group

```shell
$ python3 service_edge_group_management.py --add --name "New Service Edge Group" --latitude 37.3382082 --longitude -121.8863286 --location "San Jose, CA, USA", --city_country "California, US" --country_code "US"
```

### Update an Existing Service Edge Group

```shell
$ python3 service_edge_group_management.py --update GROUP_ID --name "Updated Service Edge Group" --description "New description"
```

### Delete an Service Edge Group

```shell
$ python3 service_edge_group_management.py -d GROUP_ID

```
