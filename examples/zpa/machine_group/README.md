Machine Group Example
=====================

This script contains several examples that can be executed from the CLI to `READ` Machine Group resources in the Zscaler Private Access (ZPA) service. See the [README](../README.md) for authentication requirements. The examples in this folder assume that environment variables are being used as the authentication method.

### Listing All Machine Groups

```shell
$ python3 machine_group_management.py -l
```

### Get Details of an Machine Group By Name

```shell
$ python3 machine_group_management.py -n GROUP_NAME
```

### Get Details of an Machine Group By ID

```shell
$ python3 machine_group_management.py -g GROUP_ID
```
