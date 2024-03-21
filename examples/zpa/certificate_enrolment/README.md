Machine Group Example
=====================

This script contains several examples that can be executed from the CLI to create/read/update/delete Machine Group resources in the Zscaler Private Access (ZPA) service. See the [README](../README.md) for authentication requirements. The examples in this folder assume that environment variables are being used as the authentication method.

### List All Enrollment Certificates

```shell
$ python3 certificate_enrolment_management.py -l
```

### Get Details of an Enrollment Certificate By Name

```shell
$ python3 certificate_enrolment_management.py -s "Certificate Name"
```
