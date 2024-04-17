Identity Provider Example
=========================

This script contains several examples that can be executed from the CLI to `READ` Identity Provider resources in the Zscaler Private Access (ZPA) service. See the [README](../README.md) for authentication requirements. The examples in this folder assume that environment variables are being used as the authentication method.

### Listing All Identity Provider

```shell
$ python3 identity_provider_management.py -l
```

### Get Details of an Identity Provider By Name

```shell
$ python3 identity_provider_management.py -n IDP_NAME
```

### Get Details of an Identity Provider By ID

```shell
$ python3 identity_provider_management.py -g IDP_ID
```
