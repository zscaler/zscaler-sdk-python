Static IP Management Example
============================

This script contains several examples that can be executed from the CLI to create/read/update/delete Static IP resources in the Zscaler Internet Access (ZIA) service. See the [README](../README.md) for authentication requirements. The examples in this folder assume that environment variables are being used as the authentication method.

### Adding a New Static IP Address

```shell
$ python3 static_ip_management.py -a --ip_address "203.0.113.11" --comment "Los Angeles Branch Office"
```

### Updating an Existing Static IP

```shell
$ python3 static_ip_management.py -u 12345 --comment "Updated Los Angeles Branch Office"
```

### Deleting a Static IP

```shell
$ python3 static_ip_management.py -d 12345
```

### Listing All Static IPs

```shell
$ python3 static_ip_management.py -l
```

### Checking if a Static IP is Valid

```shell
$ python3 static_ip_management.py -c --ip_address "203.0.113.11"
```

