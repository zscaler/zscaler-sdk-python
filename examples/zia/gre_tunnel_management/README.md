GRE Tunnel with Location Management Example
===========================================

This script contains an example that can be executed from the CLI to create a location management GRE tunnel based resource in the Zscaler Internet Access (ZIA) service. See the [README](../README.md) for authentication requirements. The examples in this folder assume that environment variables are being used as the authentication method.

### Adding a New GRE Tunnel and Location Management Resource

Examples:

```shell
$ python3 add_static_and_gre_tunnel.py --ip_address <STATIC_IP> --location_name <LOCATION_NAME> [--comments <COMMENTS>]
```

### Options:
    --ip_address     The static public IP address to be added and used as the source IP for the GRE tunnel.
    --location_name  The name of the new location associated with the GRE tunnel.
    --comments       Optional. Comments or additional information about the GRE tunnel.

~> **NOTE** : The script will prompt you to decide if you want to configure gateway options for the location. If you choose yes, you'll be guided through a series of options to customize your gateway settings.

#### Configuring Gateway Options
If opted, you will be prompted to configure various gateway options, including authentication, SSL inspection, firewall settings, and more. Each option can be enabled or disabled based on your preferences.