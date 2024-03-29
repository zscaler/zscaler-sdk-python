VPN Credential Management Example
=================================

This script contains several examples that can be executed from the CLI to create/read/update/delete VPN Credential resources in the Zscaler Internet Access (ZIA) service. See the [README](../README.md) for authentication requirements. The examples in this folder assume that environment variables are being used as the authentication method.

### Add a VPN credential using `IP` authentication type:

```shell
$ python3 vpn_credentials_management.py -a IP --pre_shared_key "<YourPreSharedSecret>" --ip_address "1.1.1.1" --comments "SJC Branch Office"
```

### Add a VPN credential using `UFQDN` authentication type:

```shell
$ python3 vpn_credentials_management.py -a UFQDN --pre_shared_key "<YourPreSharedSecret>"--email user@example.com --comments "SJC Branch Office"
```

### List all VPN credentials:

```shell
$ python3 vpn_credentials_management.py -l
```

###  Update a VPN Credential (Requires the vpn credential ID):

```shell
$ python3 vpn_credentials_management.py -u 99825183 --comments "Updated Comment"
```

###  Delete a VPN Credential (Requires the vpn credential ID):

```shell
$ python3 vpn_credentials_management.py -d 99825183
```

###  Bulk delete VPN credentials (Requires the IDs of all vpn credentials to be deleted):

```shell
$ python3 vpn_credential_bulk_delete.py --bulk-delete 99826517 99825183
```
