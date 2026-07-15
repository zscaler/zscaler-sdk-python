Provisioning Key Management Example
===================================

This script contains several examples that can be executed from the CLI to create/read/update/delete Provisioning Key resources in the Zscaler Private Access (ZPA) service. See the [README](../README.md) for authentication requirements. The examples in this folder assume that environment variables are being used as the authentication method.

### Listing All App Connector or Service Edge Group Provisioning Keys

* Choose 1: for Connector
* Choose 2: for Service Edge

```shell
$ python3 provisioning_key_management.py --list
```

### Get Details of a Specific Segment Group

```shell
$ python3 segment_group_management.py -g SEGMENT_GROUP_ID
```

### Add a App Connector or Service Edge Group Provisioning Key

* Choose 1: for Connector
* Choose 2: for Service Edge

```shell
$ python3 provisioning_key_management.py --add
```

### Update Specific App Connector or Service Edge Group Provisioning Key

* Choose 1: for Connector
* Choose 2: for Service Edge

```shell
$ python3 provisioning_key_management.py --update KEY_ID
```

### Delete Specific App Connector or Service Edge Group Provisioning Key

* Choose 1: for Connector
* Choose 2: for Service Edge

```shell
$ python3 provisioning_key_management.py --delete KEY_ID
```
