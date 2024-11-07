# Zscaler Private Access (ZPA) Provider

The Zscaler-SDK-Python can be used to interact with the Zscaler Private Access (ZPA) API, to automate the provisioning of application segments, segment grouos, app connector groups, service edge groups, provisioning keys etc.

### Authentication

This example requires authentication to the Zscaler service using environment variables or hard-coded credentails.

### Support Zscaler Private Access Clouds
The Zscaler SDK Python supports the following environments: `BETA`, `GOV`, `GOVUS`, `PRODUCTION` `PREVIEW`, `ZPATWO` values or via environment variable `ZPA_CLOUD=BETA`, `ZPA_CLOUD=GOV`, `ZPA_CLOUD=GOVUS`, `ZPA_CLOUD=PREVIEW` `ZPA_CLOUD=PRODUCTION`, `ZPA_CLOUD=ZPATWO`.

#### Environment variables
You can provide credentials via the ``ZPA_CLIENT_ID``, ``ZPA_CLIENT_SECRET``, ``ZPA_CUSTOMER_ID``, ``ZPA_CLOUD`` environment variables, representing your ZPA client_id, client_secret, customer_id and cloud respectively.

~> **NOTE** `ZPA_CLOUD` environment variable is an optional parameter when running this provider in production; however, this parameter is required to provision resources in the ZPA Beta Cloud, Gov Cloud, Gov US Cloud, or Preview Cloud.

**Usage:**

```sh
export ZPA_CLIENT_ID="xxxxxxxxxxxxxxxx"
export ZPA_CLIENT_SECRET="xxxxxxxxxxxxxxxx"
export ZPA_CUSTOMER_ID="xxxxxxxxxxxxxxxx"
export ZPA_CLOUD="<zpa_cloud_name>"
```

If you are on Windows, use PowerShell to set the environmenr variables using the following commands:

```powershell
$env:client_id='xxxxxxxxxxxxxxxx'
$env:client_secret='xxxxxxxxxxxxxxxx'
$env:customer_id='xxxxxxxxxxxxxxxx'
$env:cloud='<zpa_cloud_name>'
```

### Static credentials

!> **WARNING:** Hard-coding credentials into any Terraform configuration is not recommended, and risks secret leakage should this file be committed to public version control

Static credentials can be provided by specifying the `client_id`, `client_secret` and `customer_id`, and cloud 
