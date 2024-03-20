Segment Group Management Example
================================

This script contains several examples that can be executed from the CLI to create/read/update/delete Segment group resources in the Zscaler Private Access (ZPA) service. See the [README](../README.md) for authentication requirements. The examples in this folder assume that environment variables are being used as the authentication method.

### Listing All Segment Groups

```shell
$ python3 segment_group_management.py -l
```

### Get Details of a Specific Segment Group

```shell
$ python3 segment_group_management.py -g SEGMENT_GROUP_ID
```

### Add a New Segment Group

```shell
$ python3 segment_group_management.py --add --name "New Group" --enabled True --description "New group
```

### Update an Existing Segment Group

```shell
$ python3 segment_group_management.py --update SEGMENT_GROUP_ID --name "Updated Segment Group" --description "New description"
```

### Delete an Segment Group

```shell
$ python3 segment_group_management.py -d SEGMENT_GROUP_ID

```
