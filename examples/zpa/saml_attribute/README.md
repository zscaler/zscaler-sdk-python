SAML Attribute Example
======================

This script contains several examples that can be executed from the CLI to `READ` SAML Attribute resources in the Zscaler Private Access (ZPA) service. See the [README](../README.md) for authentication requirements. The examples in this folder assume that environment variables are being used as the authentication method.

### Listing All SAML Attribute

```shell
$ python3 saml_attribute_management.py -l
```

### Get Details of a SAML Attribute By Name

```shell
$ python3 saml_attribute_management.py --search_name ATTRIBUTE_NAME
```

### Get Details of a SAML Attribute By ID

```shell
$ python3 saml_attribute_management.py -g ATTRIBUTE_ID
```

### Get Details of a SAML Attribute By IDP Name

```shell
$ python3 saml_attribute_management.py --list_by_idp_name IDP_NAME
```
