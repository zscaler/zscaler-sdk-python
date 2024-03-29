# Zscaler Internet Access (ZIA) Provider

The Zscaler-SDK-Python can be used to interact with the Zscaler Internet Access (ZIA) API, to automate the provisioning of new locations, IPSec and GRE tunnels, URL filtering policies, Cloud Firewall Policies, DLP Dictionaries, Local Accounts etc.

### Authentication

This example requires authentication to the Zscaler service using environment variables or hard-coded credentails.

### Support Zscaler Internet Access Clouds
The Zscaler SDK Python supports the following environments:

* zscaler
* zscloud
* zspreview
* zscalerbeta
* zscalerone
* zscalertwo
* zscalerthree
* zscalergov
* zscalerten

#### Environment variables
You can provide credentials via the ``ZIA_USERNAME``, ``ZIA_PASSWORD``, ``ZIA_API_KEY``, ``ZIA_CLOUD`` environment variables, representing your ZIA username, password, API Key credentials and tenant base URL, respectively.

**Usage:**

```sh
export ZIA_USERNAME="xxxxxxxxxxxxxxxx"
export ZIA_PASSWORD="xxxxxxxxxxxxxxxx"
export ZIA_API_KEY="xxxxxxxxxxxxxxxx"
export ZIA_CLOUD="<zscaler_cloud_name>"
```

If you are on Windows, use PowerShell to set the environmenr variables using the following commands:

```powershell
$env:username='xxxxxxxxxxxxxxxx'
$env:password='xxxxxxxxxxxxxxxx'
$env:api_key='xxxxxxxxxxxxxxxx'
$env:zia_cloud='<zscaler_cloud_name>'
```

### Static credentials
⚠️ **WARNING:** Hard-coding credentials into any example configuration is **NOT** recommended, and risks secret leakage should the script configuration file be committed to public version control system.

### Zscaler Sandbox Authentication

The Zscaler-SDK-Python requires both the `ZIA_CLOUD` and `ZIA_SANDBOX_TOKEN` in order to authenticate to the Zscaler Cloud Sandbox environment. For details on how obtain the API Token visit the Zscaler help portal [About Sandbox API Token](https://help.zscaler.com/zia/about-sandbox-api-token)