SAML Attribute Example
======================

This script contains several examples that can be executed from the CLI to `READ` SCIM Groups resources in the Zscaler Private Access (ZPA) service. See the [README](../README.md) for authentication requirements. The examples in this folder assume that environment variables are being used as the authentication method.

### Listing All SCIM Group by IDP Name

```shell
$ python3 scim_group_management.py -l IDP_NAME
```

### Get Details of a SCIM Group By Name

```shell
$ python3 scim_group_management.py --search_name GROUP_NAME
```

### Get Details of a SCIM Group By ID

```shell
$ python3 scim_group_management.py -g GROUP_ID
```
