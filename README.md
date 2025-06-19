# Official Python SDK for the Zscaler Products

[![PyPI - Downloads](https://img.shields.io/pypi/dw/zscaler-sdk-python)](https://pypistats.org/packages/zscaler-sdk-python)
[![License](https://img.shields.io/github/license/zscaler/zscaler-sdk-python.svg)](https://github.com/zscaler/zscaler-sdk-python)
[![Documentation Status](https://readthedocs.org/projects/zscaler-sdk-python/badge/?version=latest)](https://zscaler-sdk-python.readthedocs.io/en/latest/?badge=latest)
[![Latest version released on PyPi](https://img.shields.io/pypi/v/zscaler-sdk-python.svg)](https://pypi.org/project/zscaler-sdk-python)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/zscaler-sdk-python.svg)](https://pypi.python.org/pypi/zscaler-sdk-python/)
[![codecov](https://codecov.io/gh/zscaler/zscaler-sdk-python/graph/badge.svg?token=56B53PITU8)](https://codecov.io/gh/zscaler/zscaler-sdk-python)
[![Zscaler Community](https://img.shields.io/badge/zscaler-community-blue)](https://community.zscaler.com/)

## Support Disclaimer

-> **Disclaimer:** Please refer to our [General Support Statement](docsrc/zs/guides/support.rst) before proceeding with the use of this provider. You can also refer to our [troubleshooting guide](docsrc/zs/guides/troubleshooting.rst) for guidance on typical problems.

# Official Zscaler Python SDK Overview

* [Release status](#release-status)
* [Breaking Changes & Migration Guide to Multi-Client SDK](#breaking-changes--migration-guide-to-multi-client-sdk)
* [Need help?](#need-help)
* [Getting Started](#getting-started)
- [Building the SDK](#building-the-sdk)
* [Usage guide](#usage-guide)
* [Authentication](#authentication)
* [Zscaler OneAPI New Framework](#zscaler-oneapi-new-framework)
* [Zscaler Legacy API Framework](#zscaler-legacy-api-framework)
* [Configuration reference](#configuration-reference)
* [Pagination](#pagination)
* [Contributing](#contributing)

The Zscaler SDK for Python includes functionality to accelerate development via [Python](https://www.python.org/). This SDK can be
used in your server-side code to interact with the Zscaler API platform across multiple products such as:

* [ZPA API](https://help.zscaler.com/zpa/zpa-api/api-developer-reference-guide)
* [ZIA API](https://help.zscaler.com/zia/getting-started-zia-api)
* [ZDX API](https://help.zscaler.com/zdx/understanding-zdx-api)
* [ZCC API](https://help.zscaler.com/client-connector/getting-started-client-connector-api)
* [ZTW API](https://help.zscaler.com/cloud-branch-connector/getting-started-cloud-branch-connector-api)
* [ZWA API](https://help.zscaler.com/workflow-automation/getting-started-workflow-automation-api)

This SDK is designed to support the new Zscaler API framework [OneAPI](https://help.zscaler.com/oneapi/understanding-oneapi)
via a single OAuth2 HTTP client. The SDK is also backwards compatible with the previous
Zscaler API framework, and each package is supported by an individual and robust HTTP client
designed to handle failures on different levels by performing intelligent retries.

## Release Status

This library uses semantic versioning and updates are posted in ([release notes](/docs/guides/release-notes.md)) |

| Version | Status                           |
| ------- | -------------------------------- |
| 0.x     | :warning: Beta Release (Retired) |
| 1.x     | :heavy_check_mark: Release       |

The latest release can always be found on the ([releases page](github-releases))

> Requires Python version 3.8.0 or higher.
Zscaler SDK for Python is compatible with Python 3.8 _(until [June 2023](https://devguide.python.org/versions/))_, 3.8, 3.9, 3.10, and 3.11.

## Need help?

If you run into problems, please refer to our [General Support Statement](docs/guides/support.md) before proceeding with the use of this SDK. You can also refer to our [troubleshooting guide](docs/guides/troubleshooting.md) for guidance on typical problems. You can also raise an issue via ([github issues page](https://github.com/zscaler/zscaler-sdk-go/issues))

- Ask questions on the [Zenith Community][zenith]
- Post [issues on GitHub][github-issues] (for code errors)
- Support [customer support portal][zscaler-support]

## Breaking Changes & Migration Guide to Multi-Client SDK

This SDK is a complete redesign from the older `zscaler-sdk-python` or `pyzscaler packages`. If you've used either of those, please review the following before upgrading:

### What's Changed

| Feature                         | Legacy SDK (Restfly + Box)                      | New SDK (OneAPI + Pythonic Dict)                |
|---------------------------------|--------------------------------------------------|--------------------------------------------------|
| **Data Structure**              | Used `Python-Box` objects (dot notation)        | Uses native Python `dict` with `snake_case`     |
| **HTTP Engine**                 | [Restfly](https://github.com/tdunham/restfly)   | Custom HTTP executor with retries, caching, etc.|
| **Auth Model**                  | One set of credentials per service              | Unified OAuth2 (Zidentity) with scoped access    |
| **Multi-Service Support**       | Separate SDKs or config per service             | Unified client with `.zia`, `.zpa`, `.zcc`      |
| **Pagination**                  | Inconsistent or manual                          | Built-in with `resp.has_next()` and `resp.next()` |
| **Error Handling**              | Raw HTTP exceptions                             | Returns `(result, response, error)` tuples      |
| **Models**                      | Custom models + `.attribute` access             | Plain Python dict access: `object["field"]`     |
| **Return Types**                | Box-style nested objects                        | Pure JSON-serializable `dict` responses          |

### Legacy SDK Examples

```py
# Old SDK (Pyzscaler / Restfly)
client = ZIAClientHelper(api_key="...", cloud="...")

users = client.users.list()
print(users[0].name)  # Box-style access
```

### New SDK Example
```py
from zscaler import ZscalerClient

config = {
    "clientId": "...",
    "clientSecret": "...",
    "vanityDomain": "...",
    "cloud": "beta", # (Optional)
}

with ZscalerClient(config) as client:
    users, _, err = client.zia.user_management.list_users()
    if err:
        print("Error:", err)
    else:
        print(users[0]["name"])  # Pythonic dict access
```

### Migration Summary

If you're upgrading from a previous version:

* Refactor any `.attribute` access to dictionary access: `user["name"]` instead of `user.name`
* Update authentication to use OAuth2 via OneAPI:
Choose either:
```py
client = ZscalerClient({
    "client_id": "...",
    "client_secret": "...",
    "vanity_domain": "..."
})
```

or (for JWT private key auth):
```py
client = ZscalerClient({
    "client_id": "...",
    "private_key": "...",
    "vanity_domain": "..."
})
```

* If your tenant is still `NOT` migrated to Zidentity:
You can still use this SDK by instantiating the respective legacy API client directly. See section: [Zscaler Legacy API Framework](#zscaler-legacy-api-framework)
```py
from zscaler.oneapi_client import LegacyZIAClient

def main():
    with LegacyZIAClient(config) as client:
        users, _, _ = client.user_management.list_users()
        ...
```

* All data returned from the SDK is pure `dict` — no Box, no attribute-style access — just native, Pythonic, serializable output.

## Getting started

To install the Zscaler Python SDK in your project:

```sh
pip install zscaler-sdk-python
```

## Building the SDK

In most cases, you won't need to build the SDK from source. If you want to build it yourself, you'll need these prerequisites:

- Clone the repo
- Install `poetry`
- Run `poetry build` from the root of the project
- Run `pip install dist/zscalerdist/zscaler_sdk_python-x.x.x.tar.gz`

### You'll also need

* An administrator account in the Zscaler products you want to interact with.
* [OneAPI](https://help.zscaler.com/oneapi/understanding-oneapi): If you are using the OneAPI entrypoint you must have a API Client created in the [Zidentity platform](https://help.zscaler.com/zidentity/about-api-clients)
* Legacy Framework: If using the legacy API framework you must have API Keys credentials in the the respective Zscaler cloud products.
* For more information on getting started with Zscaler APIs visit one of the following links:

* [OneAPI](https://help.zscaler.com/oneapi/understanding-oneapi)
* [ZPA API](https://help.zscaler.com/zpa/zpa-api/api-developer-reference-guide)
* [ZIA API](https://help.zscaler.com/zia/getting-started-zia-api)
* [ZDX API](https://help.zscaler.com/zdx/understanding-zdx-api)
* [ZCC API](https://help.zscaler.com/client-connector/getting-started-client-connector-api)
* [ZTW API](https://help.zscaler.com/cloud-branch-connector/getting-started-cloud-branch-connector-api)
* [ZWA API](https://help.zscaler.com/workflow-automation/getting-started-workflow-automation-api)

## Usage guide

These examples will help you understand how to use this library.

Once you initialize a specific service client, you can call methods to make requests to the Zscaler API. Each Zscaler Service has its own package and is grouped by the API endpoint they belong to. For example, ZPA methods that call the [Application Segment API][application-segment-api-docs] are organized under [the zscaler/zpa resource (zscaler.zpa.application_segment.py)][application_segment]. The same logic applies to all other services.

**NOTE:** Zscaler APIs DO NOT support Asynchronous I/O calls, which made its debut in Python 3.5 and is powered by the `asyncio` library which provides avenues to produce concurrent code.

## Authentication

The latest versions => 0.20.0 of this SDK provides dual API client capability and can be used to interact both with new Zscaler [OneAPI](https://help.zscaler.com/oneapi/understanding-oneapi) framework and the legacy API platform.

If your Zscaler tenant has not been migrated to the new Zscaler [Zidentity platform](https://help.zscaler.com/zidentity/what-zidentity), you must use the respective Legacy API client described in the following section: [Zscaler Legacy API Framework](#zscaler-legacy-api-framework)

   :warning: **Caution**: Zscaler does not recommend hard-coding credentials into arguments, as they can be exposed in plain text in version control systems. Use environment variables instead.

## Zscaler OneAPI New Framework

As of the publication of SDK version => 0.20.x, OneAPI is available for programmatic interaction with the following products:

* [ZIA API](https://help.zscaler.com/oneapi/understanding-oneapi#:~:text=managed%20using%20OneAPI.-,ZIA%20API,-Zscaler%20Internet%20Access)
* [ZPA API](https://help.zscaler.com/oneapi/understanding-oneapi#:~:text=Workload%20Groups-,ZPA%20API,-Zscaler%20Private%20Access)
* [Zscaler Client Connector API](https://help.zscaler.com/oneapi/understanding-oneapi#:~:text=Version%20Profiles-,Zscaler%20Client%20Connector%20API,-Zscaler%20Client%20Connector)

**NOTE** All other products such as Zscaler Cloud Connector (ZTW) and Zscaler Digital Experience (ZDX) are supported only via the legacy authentication method described in this README.

### OneAPI (API Client Scope)

OneAPI Resources are automatically created within the ZIdentity Admin UI based on the RBAC Roles
applicable to APIs within the various products. For example, in ZIA, navigate to `Administration -> Role Management` and select `Add API Role`.

Once this role has been saved, return to the ZIdentity Admin UI and from the Integration menu
select API Resources. Click the `View` icon to the right of Zscaler APIs and under the ZIA
dropdown you will see the newly created Role. In the event a newly created role is not seen in the
ZIdentity Admin UI a `Sync Now` button is provided in the API Resources menu which will initiate an
on-demand sync of newly created roles.

**WARNING**: Attention Government customers. OneAPI and Zidentity is not currently supported for the following ZIA clouds: `zscalergov` and `zscalerten` or ZPA `GOV`, and `GOVUS`.

### Default Environment Variables

You can provide credentials via the `ZSCALER_CLIENT_ID`, `ZSCALER_CLIENT_SECRET`, `ZSCALER_VANITY_DOMAIN`, `ZSCALER_CLOUD` environment variables, representing your Zidentity OneAPI credentials `clientId`, `clientSecret`, `vanityDomain` and `cloud` respectively.

| Argument     | Description | Environment variable |
|--------------|-------------|-------------------|
| `clientId`       | _(String)_ Zscaler API Client ID, used with `clientSecret` or `PrivateKey` OAuth auth mode.| `ZSCALER_CLIENT_ID` |
| `clientSecret`       | _(String)_ A string that contains the password for the API admin.| `ZSCALER_CLIENT_SECRET` |
| `privateKey`       | _(String)_ A string Private key value.| `ZSCALER_PRIVATE_KEY` |
| `vanityDomain`       | _(String)_ Refers to the domain name used by your organization `https://<vanity_domain>.zslogin.net/oauth2/v1/token` | `ZSCALER_VANITY_DOMAIN` |
| `cloud`       | _(String)_ The host and basePath for the cloud services API is `$api.<cloud_name>.zsapi.net`.| `ZSCALER_CLOUD` |
| `sandboxToken`       | _(String)_ The Zscaler Internet Access Sandbox Token | `ZSCALER_SANDBOX_TOKEN` |
| `sandboxCloud`       | _(String)_ The Zscaler Internet Access Sandbox cloud name | `ZSCALER_SANDBOX_CLOUD` |

### Alternative OneAPI Cloud Environments

OneAPI supports authentication and can interact with alternative Zscaler enviornments i.e `beta`, `alpha` etc. To authenticate to these environments you must provide the following values:

| Argument     | Description | Environment variable |
|--------------|-------------|-------------------|
| `vanityDomain`       | _(String)_ Refers to the domain name used by your organization `https://<vanity_domain>.zslogin.net/oauth2/v1/token` | `ZSCALER_VANITY_DOMAIN` |
| `cloud`       | _(String)_ The host and basePath for the cloud services API is `$api.<cloud_name>.zsapi.net`.| `ZSCALER_CLOUD` |

For example: Authenticating to Zscaler Beta environment:

```sh
export ZSCALER_VANITY_DOMAIN="acme"
export ZSCALER_CLOUD="beta"
```

**Note 1**: The attribute `cloud` or environment variable `ZSCALER_CLOUD` is optional and only required when authenticating to an alternative Zidentity cloud environment.

**Note 2**: By default this SDK will send the authentication request and subsequent API calls to the default base URL.

**Note 3**: Authentication to Zscaler Sandbox requires the attribute/parameter `sandboxCloud`.The following cloud environments are supported:

* `zscaler`
* `zscalerone`
* `zscalertwo`
* `zscalerthree`
* `zscloud`
* `zscalerbeta`
* `zscalergov`
* `zscalerten`
* `zspreview`

### Authenticating to Zscaler Private Access (ZPA)

The authentication to Zscaler Private Access (ZPA) via the OneAPI framework, requires the extra attribute called `customerId` and optionally the attribute `microtenantId`.

| Argument     | Description | Environment variable |
|--------------|-------------|-------------------|
| `clientId`       | _(String)_ Zscaler API Client ID, used with `clientSecret` or `PrivateKey` OAuth auth mode.| `ZSCALER_CLIENT_ID` |
| `clientSecret`       | _(String)_ A string that contains the password for the API admin.| `ZSCALER_CLIENT_SECRET` |
| `privateKey`       | _(String)_ A string Private key value.| `ZSCALER_PRIVATE_KEY` |
| `customerId`       | _(String)_ The ZPA tenant ID found under Configuration & Control > Public API > API Keys menu in the ZPA console.| `ZPA_CUSTOMER_ID` |
| `microtenantId`       | _(String)_ The ZPA microtenant ID found in the respective microtenant instance under Configuration & Control > Public API > API Keys menu in the ZPA console.| `ZPA_MICROTENANT_ID` |
| `vanityDomain`       | _(String)_ Refers to the domain name used by your organization `https://<vanity_domain>.zslogin.net/oauth2/v1/token` | `ZSCALER_VANITY_DOMAIN` |
| `cloud`

### Initialize OneAPI OAuth 2.0 Client

#### OneAPI Client ID and Client Secret Authentication

Construct a client instance by passing your Zidentity `clientId`, `clientSecret` and `vanityDomain`:

```py
from zscaler import ZscalerClient

config = {
    "clientId": '{yourClientId}',
    "clientSecret": '{yourClientSecret}',
    "vanityDomain": '{yourvanityDomain}',
    "cloud": "beta", # Optional when authenticating to an alternative cloud environment
    "customerId": "", # Optional parameter. Required only when using ZPA
    "microtenantId": "", # Optional parameter. Required only when using ZPA with Microtenant
    "logging": {"enabled": False, "verbose": False},
}

def main():
    with ZscalerClient(config) as client:
        idp_id = "72058304855015574"
        query_params = {'page': '1', 'page_size': '100'}
        groups, resp, err = client.zpa.scim_groups.list_scim_groups(idp_id=idp_id, query_params=query_params)
        if err:
            print(f"Error listing SCIM groups: {err}")
            return
        if groups:
            print(f"Processing {len(groups)} groups:")
            for group in groups:
                print(group)

        try:
            resp.next()
        except StopIteration:
            print("No more groups to retrieve.")

if __name__ == "__main__":
    main()
```

#### OneAPI Client ID and Private Key Authentication

```py
from zscaler import ZscalerClient

config = {
    "clientId": '{yourClientId}',
    "privateKey": '{yourPrivateKey}',
    "vanityDomain": '{yourvanityDomain}',
    "cloud": "beta", # Optional when authenticating to an alternative cloud environment
    "customerId": "", # Optional parameter. Required only when using ZPA
    "microtenantId": "", # Optional parameter. Required only when using ZPA with Microtenant
    "logging": {"enabled": False, "verbose": False},
}

def main():
    with ZscalerClient(config) as client:
        idp_id = "72058304855015574"
        query_params = {'page': '1', 'page_size': '100'}
        groups, resp, err = client.zpa.scim_groups.list_scim_groups(idp_id=idp_id, query_params=query_params)
        if err:
            print(f"Error listing SCIM groups: {err}")
            return
        if groups:
            print(f"Processing {len(groups)} groups:")
            for group in groups:
                print(group)

        try:
            resp.next()
        except StopIteration:
            print("No more groups to retrieve.")

if __name__ == "__main__":
    main()
```

Note, that `privateKey` can be passed in JWK format or in PEM format, i.e. (examples generated with https://mkjwk.org):

> Using a Python dictionary to hard-code the Zscaler API credentials is encouraged for development ONLY; In production, you should use a more secure way of storing these values. This library supports a few different configuration sources, covered in the [configuration reference](#configuration-reference) section.

> **NOTE**: THIS IS NOT A PRODUCTION KEY AND IS DISPLAYED FOR EXAMPLE PURPOSES ONLY

![JWK Example](https://raw.githubusercontent.com/zscaler/zscaler-sdk-python/refs/heads/master/docsrc/jwk.svg)

or

> **NOTE**: THIS IS NOT A PRODUCTION KEY AND IS DISPLAYED FOR EXAMPLE PURPOSES ONLY

```
-----BEGIN PRIVATE KEY-----
MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCv3krdYg3z7h0H
60QoePJMghllQxsfPxp3mgFfYEaIbF88Z8dvPZEfhAtP19/Mv62ASjwgqzQzKHRV
-----END PRIVATE KEY-----
```

### Get and set custom headers

It is possible to set custom headers, which will be sent with each request. This feature is only supported when instantiating the OneAPI Client `ZscalerClient`.

```py
from zscaler import ZscalerClient

def main():
    with ZscalerClient(config) as client:
        client.set_custom_headers({'Custom-Header': 'custom value'})
        groups, resp, err = client.zpa.segment_groups.list_groups()
        for group in groups:
            print(group.name, group.description)

    # clear all custom headers
    client.clear_custom_headers()

    # output should be: {}
    print(client.get_custom_headers())
```

Note, that custom headers will be overwritten with default headers with the same name.
This doesn't allow breaking the client. Get default headers:

## Zscaler OneAPI Rate Limiting

Zscaler OneAPI provides unique rate limiting numbers for each individual product. Regardless of the product, a 429 response will be returned if too many requests are made within a given time.

### Built-In Retry

This SDK uses a built-in retry strategy to automatically retry on 429 errors based on the response headers returned by each respective API service.

The header `x-ratelimit-reset` is returned in the API response for each API call, which indicates the time in seconds until the rate limit resets. The SDK uses the returned value in this header to calculate the retry time for the following services:

* [ZCC Rate Limiting][rate-limiting-zcc] for rate limiting requirements.
* [ZIA Rate Limiting][rate-limiting-zia] for rate limiting requirements.
* [ZPA Rate Limiting][rate-limiting-zpa] for rate limiting requirements.

## Pagination

The pagination system in this SDK is unified across `ZCC`, `ZTW`, `ZDX`, `ZIA`, `ZPA`, `ZWA`
and is applied transparently whether you're using the Legacy API Client or the new OneAPI OAuth2 Client.

✅ This means no code changes are needed when transitioning from the legacy API framework to OneAPI framework.

When calling a method that supports pagination (e.g., `list_users`, `list_groups`, `list_app_segments`), only the first page of results is returned initially. The SDK returns a response tuple:

```py
items, response, error = client.zia.user_management.list_groups()
```

You can then use the `response.has_next()` and `response.next()` methods to retrieve subsequent pages.

### Basic Pagination Example

```py
query_parameters = {'page_size': 100}
groups, resp, err = client.zia.user_management.list_groups(query_parameters)

while resp.has_next():
    more_groups, err = resp.next()
    if err:
        break
    groups.extend(more_groups)
```

### Searching and Filtering

You can filter or search using available query parameters. The available parameters vary by service, so refer to each method's documentation for details.

```py
# Query parameters are optional on methods that can use them!
# Check the method definition for details on which query parameters are accepted.
# Using the search parameter to support search by features and fields.
query_parameters = {'search': 'Group1'}
groups, resp, err = client.zpa.segment_groups.list_groups(query_parameters)
```

```py
# Query parameters are optional on methods that can use them!
# Check the method definition for details on which query parameters are accepted.
query_parameters = {'page': '1', 'page_size': '100'}
groups, resp, err = client.zpa.segment_groups.list_groups(query_parameters)
```

### Full Example with Error Handling
```py
def main():
    with ZscalerClient(config) as client:
        query_parameters = {}
        groups, resp, err = client.zia.user_management.list_groups(query_parameters)

        if err:
            print(f"Error: {err}")
            return

        print(f"Processing {len(groups)} groups:")
        for group in groups:
            print(group)

        while resp.has_next():
            next_page, err = resp.next()
            if err:
                print(f"Error fetching next page: {err}")
                break
            for group in next_page:
                print(group)

        try:
            resp.next()  # Will raise StopIteration if no more data
        except StopIteration:
            print("✅ No more groups to retrieve.")

if __name__ == "__main__":
    main()
```

### Pagination Limits and Controls

Each Zscaler service has its own pagination requiremens and max page size:

| Service | Default Page Size | Max Page Size |             Notes                               |
|---------|-------------------|---------------|-------------------------------------------------|
| ZCC     | Varies            | Varies        | Uses `pageSize` (camelCase)                     |
| ZDX     | 10                | Varies        | Uses `limit` + `offset`, similar to cursor API  |
| ZIA     | 100               | Varies        | Uses `pageSize` (camelCase)                     |
| ZPA     | 100               | 500           | Uses `pagesize` (lowercase)                     |
| ZTW     | 100               | Varies        | Uses `pageSize` (camelCase)                     |
| ZWA     | Varies            | Varies        | Uses `pageSize` (camelCase)                     |

⚠️ **Note:** Always use `snake_case` for all parameter names, even when the API expects camelCase.The SDK handles conversion internally.


You can control how many total items or pages the SDK will fetch even if more data is available.

###  Internal Pagination Handling

The `ZscalerAPIResponse` object returned as resp handles:

* Tracking the current page
* Automatically applying proper pagination parameters per service
* Mapping pagination fields like page, pagesize, limit, offset, next_offset, etc.
* Fallback handling when the API doesn't indicate the total count

You don’t need to worry about API quirks—just use `resp.has_next()` and `resp.next()` safely.

⚠️ Note on StopIteration
The SDK raises a StopIteration if `next()` is called and no more pages are available:

```py
try:
    resp.next()
except StopIteration:
    print("All data fetched.")
```

## Logging

The Zscaler SDK Python, provides robust logging for debug purposes.
Logs are disabled by default and should be enabled explicitly via client configuration or via a [configuration file](#configuration-reference):

```py
from zscaler import ZscalerClient

config = {"logging": {"enabled": True}}
client = ZscalerClient(config)
```
You can also enable debug logging via the following environment variables:
* `ZSCALER_SDK_LOG` - Turn on logging
* `ZSCALER_SDK_VERBOSE` - Turn on logging in verbose mode

```sh
export ZSCALER_SDK_LOG=true
export ZSCALER_SDK_VERBOSE=true
```

This SDK utilizes the standard Python library `logging`. By default, log level INFO is set. You can set another log level by setting the argument `verbose` to `True`.

**NOTE**: DO NOT SET DEBUG LEVEL IN PRODUCTION!

```py
from zscaler import ZscalerClient

config = {
    "clientId": '{yourClientId}',
    "clientSecret": '{yourClientSecret}',
    "vanityDomain": '{yourvanityDomain}',
    "cloud": "beta", # Optional when authenticating to an alternative cloud environment
    "customerId": "", # Optional parameter. Required only when using ZPA
    "microtenantId": "", # Optional parameter. Required only when using ZPA with Microtenant
    "logging": {"enabled": True, "verbose": True},
}

def main():
    with ZscalerClient(config) as client:
        groups, resp, err = client.zpa.segment_groups.list_groups()
        for group in groups:
            print(group.name, group.description)
if __name__ == "__main__":
    main()
```

You should now see logs in your console. Notice that API Credentials i.e `clientId` and `clientSecret` are **NOT** logged to the console; however, Bearer tokens are still visible. We still advise to use caution and never use `verbose` level logging in production.

What it being logged? `requests`, `responses`, `http errors`, `caching responses`.

### Using Your Own Logger (Optional)
If your script defines its own logging configuration (e.g., for file or custom formatting), the SDK will not interfere with it. You can continue using your own logger like this:

```py
import logging

my_logger = logging.getLogger("my_app_logger")
my_logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
my_logger.addHandler(handler)

my_logger.info("This is your app-level log, independent from the SDK.")
```

To control SDK logging separately, use:

```py
logging.getLogger("zscaler-sdk-python").setLevel(logging.WARNING)  # or .ERROR to silence SDK logs
```

The SDK will never globally disable logging or interfere with your existing logging configuration.

## Configuration reference

This library looks for configuration in the following sources:

0. An `zscaler.yaml` file in a `.zscaler` folder in the current user's home directory (`~/.zscaler/zscaler.yaml` or `%userprofile%\.zscaler\zscaler.yaml`). See a sample [YAML Configuration](#yaml-configuration)
1. A `zscaler.yaml` file in the application or project's root directory. See a sample [YAML Configuration](#yaml-configuration)
2. [Environment variables](#environment-variables)
3. Configuration explicitly passed to the constructor (see the example in [Getting started](#getting-started))

> Only ONE source needs to be provided!

Higher numbers win. In other words, configuration passed via the constructor will OVERRIDE configuration found in environment variables, which will override configuration in the designated `zscaler.yaml` files.

**NOTE:** This option is only supported for OneAPI Zidentity credentials at the moment.

### YAML configuration

When you use an API Token instead of OAuth 2.0 the full YAML configuration looks like:

```yaml
zscaler:
  client:
    clientId: { yourClientId }
    clientSecret: { yourClientSecret }
    vanityDomain: { yourVanityDomain }
    customerId: { yourCustomerId}
    proxy:
      port: { proxy_port }
      host: { proxy_host }
      username: { proxy_username }
      password: { proxy_password }
    logging:
      enabled: true
      verbose: true
```

> **NOTE**: THIS IS NOT A PRODUCTION KEY AND IS DISPLAYED FOR EXAMPLE PURPOSES ONLY

When you use OAuth 2.0 the full YAML configuration looks like:

```yaml
zscaler:
  client:
    clientId: "YOUR_CLIENT_ID"
    privateKey: |
      -----BEGIN RSA PRIVATE KEY-----
      MIIEogIBAAKCAQEAl4F5CrP6Wu2kKwH1Z+CNBdo0iteHhVRIXeHdeoqIB1iXvuv4
      THQdM5PIlot6XmeV1KUKuzw2ewDeb5zcasA4QHPcSVh2+KzbttPQ+RUXCUAr5t+r
      0r6gBc5Dy1IPjCFsqsPJXFwqe3RzUb...
      -----END RSA PRIVATE KEY-----
    vanityDomain: { yourVanityDomain }
    customerId: { yourCustomerId}
    proxy:
      port: { proxy_port }
      host: { proxy_host }
      username: { proxy_username }
      password: { proxy_password }
    logging:
      enabled: true
      verbose: true
```

### Environment variables

Each one of the configuration values above can be turned into an environment variable name with the `_` (underscore) character and UPPERCASE characters. The following are accepted:

| Argument     | Description | Environment variable |
|--------------|-------------|-------------------|
| `clientId`       | _(String)_ Zscaler API Client ID, used with `clientSecret` or `PrivateKey` OAuth auth mode.| `ZSCALER_CLIENT_ID` |
| `clientSecret`       | _(String)_ A string that contains the password for the API admin.| `ZSCALER_CLIENT_SECRET` |
| `privateKey`       | _(String)_ A string Private key value.| `ZSCALER_CLIENT_PRIVATEKEY` |
| `vanityDomain`       | _(String)_ Refers to the domain name used by your organization `https://<vanity_domain>.zslogin.net/oauth2/v1/token` | `ZSCALER_VANITY_DOMAIN` |
| `cloud`       | _(String)_ The host and basePath for the cloud services API is `$api.<cloud_name>.zsapi.net`.| `ZSCALER_CLOUD` |
| `userAgent`       | _(String)_ Append additional information to the HTTP User-Agent | `ZSCALER_CLIENT_USERAGENT` |
| `cache.enabled`       | _(String)_ Use request memory cache | `ZSCALER_CLIENT_CACHE_ENABLED` |
| `cache.defaultTti`       | _(String)_ Cache clean up interval in seconds | `ZSCALER_CLIENT_CACHE_DEFAULTTTI` |
| `cache.defaultTtl`       | _(String)_ Cache time to live in seconds | `ZSCALER_CLIENT_CACHE_DEFAULTTTL` |
| `proxyPort`       | _(String)_ HTTP proxy port | `ZSCALER_CLIENT_PROXY_PORT` |
| `proxyHost`       | _(String)_ HTTP proxy host  | `ZSCALER_CLIENT_PROXY_HOST` |
| `proxyUsername`       | _(String)_ HTTP proxy username  | `ZSCALER_CLIENT_PROXY_USERNAME` |
| `proxyPassword`       | _(String)_ HTTP proxy password  | `ZSCALER_CLIENT_PROXY_PASSWORD` |
| `disableHttpsCheck`       | _(String)_ Disable SSL checks  | `ZSCALER_TESTING_TESTINGDISABLEHTTPSCHECK` |
| `sandboxToken`       | _(String)_ The Zscaler Internet Access Sandbox Token | `ZSCALER_SANDBOX_TOKEN` |
| `sandboxCloud`       | _(String)_ The Zscaler Internet Access Sandbox cloud name | `ZSCALER_SANDBOX_CLOUD` |

## Zscaler Legacy API Framework

The legacy Zscaler API is still utilized by several customers, and will remain in place for the foreable future with no specific annouced deprecation date.

### ZIA Legacy Authentication

Organizations whose tenant is still not migrated to Zidentity must continue using their previous ZIA API credentials.
This SDK provides a dedicated API client `LegacyZIAClient` compatible with the legacy framework, which must be used in this scenario.

- For authentication via Zscaler Internet Access, you must provide `username`, `password`, `api_key` and `cloud`

The ZIA Cloud is identified by several cloud name prefixes, which determines which API endpoint the requests should be sent to. The following cloud environments are supported:

* `zscaler`
* `zscalerone`
* `zscalertwo`
* `zscalerthree`
* `zscloud`
* `zscalerbeta`
* `zscalergov`
* `zscalerten`
* `zspreview`

### Environment variables

You can provide credentials via the `ZIA_USERNAME`, `ZIA_PASSWORD`, `ZIA_API_KEY`, `ZIA_CLOUD` environment variables, representing your ZIA `username`, `password`, `api_key` and `cloud` respectively.

| Argument     | Description | Environment variable |
|--------------|-------------|-------------------|
| `username`       | _(String)_ A string that contains the email ID of the API admin.| `ZIA_USERNAME` |
| `password`       | _(String)_ A string that contains the password for the API admin.| `ZIA_PASSWORD` |
| `api_key`       | _(String)_ A string that contains the obfuscated API key (i.e., the return value of the obfuscateApiKey() method).| `ZIA_API_KEY` |
| `cloud`       | _(String)_ The host and basePath for the cloud services API is `$zsapi.<Zscaler Cloud Name>/api/v1`.| `ZIA_CLOUD` |
| `sandboxToken`       | _(String)_ The Zscaler Internet Access Sandbox Token | `ZSCALER_SANDBOX_TOKEN` |
| `sandboxCloud`       | _(String)_ The Zscaler Internet Access Sandbox cloud name | `ZSCALER_SANDBOX_CLOUD` |

### ZIA Legacy Client Initialization

```py
import random
from zscaler.oneapi_client import LegacyZIAClient

config = {
    "username": '{yourUsername}',
    "password": '{yourPassword}',
    "api_key": '{yourApiKey}',
    "cloud": '{yourCloud}',
    "logging": {"enabled": False, "verbose": False},
}

def main():
    with LegacyZIAClient(config) as client:
        added_label, response, error = client.zia.rule_labels.add_label(
            name=f"NewLabel_{random.randint(1000, 10000)}",
            description=f"NewLabel_{random.randint(1000, 10000)}",
        )
        if err:
            print(f"Error adding label: {err}")
            return
        print(f"Label added successfully: {added_label.as_dict()}")

if __name__ == "__main__":
    main()
```

### ZTW Legacy Authentication

Organizations whose tenant is still not migrated to Zidentity must continue using their previous ZTW API credentials.
This SDK provides a dedicated API client `LegacyZTWClient` compatible with the legacy framework, which must be used in this scenario.

- For authentication via Zscaler Internet Access, you must provide `username`, `password`, `api_key` and `cloud`

The ZTW Cloud is identified by several cloud name prefixes, which determines which API endpoint the requests should be sent to. The following cloud environments are supported:

* `zscaler`
* `zscalerone`
* `zscalertwo`
* `zscalerthree`
* `zscloud`
* `zscalerbeta`
* `zscalergov`
* `zscalerten`
* `zspreview`

### Environment variables

You can provide credentials via the `ZTW_USERNAME`, `ZTW_PASSWORD`, `ZTW_API_KEY`, `ZTW_CLOUD` environment variables, representing your ZTW `username`, `password`, `api_key` and `cloud` respectively.

| Argument     | Description | Environment variable |
|--------------|-------------|-------------------|
| `username`       | _(String)_ A string that contains the email ID of the API admin.| `ZTW_USERNAME` |
| `password`       | _(String)_ A string that contains the password for the API admin.| `ZTW_PASSWORD` |
| `api_key`       | _(String)_ A string that contains the obfuscated API key (i.e., the return value of the obfuscateApiKey() method).| `ZTW_API_KEY` |
| `cloud`       | _(String)_ The host and basePath for the cloud services API is `$zsapi.<Zscaler Cloud Name>/api/v1`.| `ZTW_CLOUD` |

### ZTW Legacy Client Initialization

```py
import random
from zscaler.oneapi_client import LegacyZTWClient

config = {
    "username": '{yourUsername}',
    "password": '{yourPassword}',
    "api_key": '{yourApiKey}',
    "cloud": '{yourCloud}',
    "logging": {"enabled": False, "verbose": False},
}

def main():
    with LegacyZTWClient(config) as client:
        fetched_prov_url, response, error = client.ZTW.provisioning_url.list_provisioning_url()
        if error:
            print(f"Error fetching prov url by ID: {error}")
            return
        print(f"Fetched prov url by ID: {fetched_prov_url.as_dict()}")

if __name__ == "__main__":
    main()
```

### ZPA Legacy Authentication

Organizations whose tenant is still not migrated to Zidentity must continue using their previous ZPA API credentials.
This SDK provides a dedicated API client `LegacyZPAClient` compatible with the legacy framework, which must be used in this scenario.

- For authentication via Zscaler Private Access, you must provide `client_id`, `client_secret`, `customer_id` and `cloud`

The ZPA Cloud is identified by several cloud name prefixes, which determines which API endpoint the requests should be sent to. The following cloud environments are supported:

* `PRODUCTION`
* `ZPATWO`
* `BETA`
* `GOV`
* `GOVUS`

### Environment variables

You can provide credentials via the `ZPA_CLIENT_ID`, `ZPA_CLIENT_SECRET`, `ZPA_CUSTOMER_ID`, `ZPA_CLOUD` environment variables, representing your ZPA `clientId`, `clientSecret`, `customerId` and `cloud` of your ZPA account, respectively.

~> **NOTE** `ZPA_CLOUD` environment variable is required, and is used to identify the correct API gateway where the API requests should be forwarded to.

| Argument     | Description | Environment variable |
|--------------|-------------|-------------------|
| `clientId`       | _(String)_ The ZPA API client ID generated from the ZPA console.| `ZPA_CLIENT_ID` |
| `clientSecret`       | _(String)_ The ZPA API client secret generated from the ZPA console.| `ZPA_CLIENT_SECRET` |
| `customerId`       | _(String)_ The ZPA tenant ID found in the Administration > Company menu in the ZPA console.| `ZPA_CUSTOMER_ID` |
| `microtenantId`       | _(String)_ The ZPA microtenant ID found in the respective microtenant instance under Configuration & Control > Public API > API Keys menu in the ZPA console.| `ZPA_MICROTENANT_ID` |
| `cloud`       | _(String)_ The Zscaler cloud for your tenancy.| `ZPA_CLOUD` |

### ZPA Legacy Client Initialization

```py
import random
from zscaler.oneapi_client import LegacyZPAClient

config = {
    "clientId": '{yourClientId}',
    "clientSecret": '{yourClientSecret}',
    "customerId": '{yourCustomerId}',
    "microtenantId": '{yourMicrotenantId}',
    "cloud": '{yourCloud}',
    "logging": {"enabled": False, "verbose": False},
}

def main():
    with LegacyZPAClient(config) as client:
        added_label, response, error = client.zpa.segment_groups.add_group(
            name=f"NewGroup_{random.randint(1000, 10000)}",
            description=f"NewGroup_{random.randint(1000, 10000)}",
            enabled=True
        )
        if err:
            print(f"Error adding segment group: {err}")
            return
        print(f"Segment Group added successfully: {added_label.as_dict()}")

if __name__ == "__main__":
    main()
```

### ZCC Legacy Authentication

Organizations whose tenant is still not migrated to Zidentity must continue using their previous ZCC API credentials.
This SDK provides a dedicated API client `LegacyZCCClient` compatible with the legacy framework, which must be used in this scenario.

- For authentication via Zscaler Client Connector (ZCC), you must provide `api_key`, `secret_key`, and `cloud`

The ZCC Cloud is identified by several cloud name prefixes, which determines which API endpoint the requests should be sent to. The following cloud environments are supported:

* `zscaler`
* `zscalerone`
* `zscalertwo`
* `zscalerthree`
* `zscloud`
* `zscalerbeta`
* `zscalergov`
* `zscalerten`
* `zspreview`

### Environment variables

You can provide credentials via the `ZCC_CLIENT_ID`, `ZCC_CLIENT_ID`, `ZCC_CLOUD` environment variables, representing your ZIA `api_key`, `secret_key`, and `cloud` respectively.

~> **NOTE** `ZCC_CLOUD` environment variable is required, and is used to identify the correct API gateway where the API requests should be forwarded to.

| Argument     | Description | Environment variable |
|--------------|-------------|-------------------|
| `api_key`       | _(String)_ A string that contains the apiKey for the Mobile Portal.| `ZCC_CLIENT_ID` |
| `secret_key`       | _(String)_ A string that contains the secret key for the Mobile Portal.| `ZCC_CLIENT_SECRET` |
| `cloud`       | _(String)_ The host and basePath for the ZCC cloud services API is `$mobileadmin.<Zscaler Cloud Name>/papi`.| `ZCC_CLOUD` |

### ZCC Legacy Client Initialization

```py
import random
from zscaler.oneapi_client import LegacyZCCClient

config = {
    "api_key": '{yourApiKey}',
    "secret_key": '{yourSecreKey}',
    "cloud": '{yourCloud}',
    "logging": {"enabled": False, "verbose": False},
}

    with LegacyZCCClient(config) as client:

        for group in client.zcc.devices.list_devices():
            print(group)
if __name__ == "__main__":
    main()
```

### ZDX Legacy Authentication

This SDK provides a dedicated API client `LegacyZDXClient` compatible with the legacy framework, which must be used in this scenario.

- For authentication via Zscaler Digital Experience (ZDX), you must provide `key_id`, `key_secret`

The ZDX `cloud` attribute identifies the cloud name prefix, which determines which API endpoint the requests should be sent to. By default the ZDX API client will always send the request to the following cloud: ``zdxcloud``

* ``zdxcloud``
* ``zdxbeta``

### ZDX Environment variables

You can provide credentials via the `ZDX_CLIENT_ID`, `ZDX_CLIENT_SECRET` environment variables, representing your ZDX `key_id`, `key_secret` of your ZDX account, respectively.

| Argument     | Description | Environment variable |
|--------------|-------------|-------------------|
| `key_id`       | _(String)_ A string that contains the key_id for the ZDX Portal.| `ZDX_CLIENT_ID` |
| `key_secret`       | _(String)_ A string that contains the key_secret key for the ZDX Portal.| `ZDX_CLIENT_SECRET` |
| `cloud`            | _(String)_ The cloud name prefix that identifies the correct API endpoint.| `ZDX_CLOUD` |

### ZDX Legacy Client Initialization

```py
import random
from zscaler.oneapi_client import LegacyZDXClient

config = {
    "key_id": '{yourKeyId}',
    "key_secret": '{yourKeySecret}',
    "cloud": '{yourCloud}',
    "logging": {"enabled": False, "verbose": False},
}

def main():
    with LegacyZDXClient(config) as client:
        app_list, _, err = client.zdx.apps.list_apps(query_params{"since": 2})
        if err:
            print(f"Error listing applications: {err}")
            return
        for app in app_list:
            print(app.as_dict())

if __name__ == "__main__":
    main()
```

### ZWA Legacy Authentication

This SDK provides a dedicated API client `LegacyZWAClient` compatible with the legacy framework, which must be used in this scenario.

- For authentication via Zscaler Workflow Automation (ZWA), you must provide `key_id`, `key_secret`

The ZWA `cloud` attribute identifies the cloud name prefix, which determines which API endpoint the requests should be sent to. By default the ZDX API client will always send the request to the following cloud: ``us1``

* ``us1``

For authentication via Zscaler Workflow Automation (ZWA), you must provide `key_id`, `key_secret`

### ZWA Environment variables

You can provide credentials via the `ZWA_CLIENT_ID`, `ZWA_CLIENT_SECRET` environment variables, representing your ZDX `key_id`, `key_secret` of your ZWA account, respectively.

| Argument     | Description | Environment variable |
|--------------|-------------|-------------------|
| `key_id`       | _(String)_ The ZWA string that contains the API key ID.| `ZWA_CLIENT_ID` |
| `key_secret`       | _(String)_ The ZWA string that contains the key secret.| `ZWA_CLIENT_SECRET` |
| `cloud`       | _(String)_ The ZWA string containing cloud provisioned for your organization.| `ZWA_CLOUD` |

### ZWA Legacy Client Initialization

```py
import random
from zscaler.oneapi_client import LegacyZWAClient

config = {
    "key_id": '{yourKeyId}',
    "key_secret": '{yourKeySecret}',
    "cloud": '{yourCloud}',
    "logging": {"enabled": False, "verbose": False},
}

def main():
    with LegacyZWAClient(config) as client:
        transactions, _, err = client.zwa.dlp_incidents.get_incident_transactions('SVDP-17410643229970491392')
        if err:
            print(f"Error listing transactions: {err}")
            return
        for incident in transactions:
            print(incident.as_dict())

if __name__ == "__main__":
    main()
```

## Zscaler Legacy API Rate Limiting

Zscaler provides unique rate limiting numbers for each individual product. Regardless of the product, a 429 response will be returned if too many requests are made within a given time.
Please see:

The header `X-Rate-Limit-Remaining` is returned in the API response for each API call. This header indicates the time in seconds until the rate limit resets. The SDK uses the returned value to calculate the retry time for the following services:
* [ZCC Rate Limiting][rate-limiting-zcc] for rate limiting requirements.

The header `RateLimit-Reset` is returned in the API response for each API call. This header indicates the time in seconds until the rate limit resets. The SDK uses the returned value to calculate the retry time for the following services:
* [ZDX Rate Limiting][rate-limiting-zdx] for rate limiting requirements.
* [ZWA Rate Limiting][rate-limiting-zwa] for rate limiting requirements.

When a 429 error is received, the `Retry-After` header is returned in the API response. The SDK uses the returned value to calculate the retry time. The following services are rate limited based on its respective endpoint.
* [ZTW Rate Limiting][rate-limiting-ZTW] for a complete list of which endpoints are rate limited.
* [ZIA Rate Limiting][rate-limiting-zia] for a complete list of which endpoints are rate limited.

When a 429 error is received, the `retry-after` header will tell you the time at which you can retry. The SDK uses the returned value to calculate the retry time.
* [ZPA Rate Limiting][rate-limiting-zpa] for rate limiting requirements.

### Built-In Retry

This SDK uses the built-in retry strategy to automatically retry on 429 errors based on the response headers returned by each respective API service.

| Configuration Option        | Description                                                                                                                                          |
| --------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| client.rateLimit.maxRetries | The number of times to retry (on retryable errors)
| client.rateLimit.maxRetrySeconds | Max wait duration allowed for a retry backoff

## Contributing

At this moment we are not accepting contributions, but we welcome suggestions on how to improve this SDK or feature requests, which can then be added in  future releases.

[zenith]: https://community.zscaler.com/
[zscaler-support]: https://help.zscaler.com/contact-support
[github-issues]: https://github.com/zscaler/zscaler-sdk-python/issues
[rate-limiting-zcc]: https://help.zscaler.com/zscaler-client-connector/understanding-rate-limiting
[rate-limiting-ZTW]: https://help.zscaler.com/cloud-branch-connector/understanding-rate-limits
[rate-limiting-zdx]: https://help.zscaler.com/zdx/understanding-rate-limiting
[rate-limiting-zia]: https://help.zscaler.com/zia/understanding-rate-limiting
[rate-limiting-zpa]: https://help.zscaler.com/zpa/understanding-rate-limiting
[rate-limiting-zwa]: https://help.zscaler.com/workflow-automation/understanding-api-rate-limiting-workflow-automation-api
[application-segment-api-docs]: https://help.zscaler.com/zpa/application-controller#/mgmtconfig/v1/admin/customers/{customerId}/application-post
[application-segment]: zscaler/zpa/application_segment.py

Contributors
------------

- William Guilherme - [willguibr](https://github.com/willguibr)
- Eddie Parra - [eparra](https://github.com/eparra)
- Paul Abbot - [abbottp](https://github.com/abbottp)

Thank you to [Mitch Kelly](https://github.com/mitchos/pyZscaler), creator of the [PyZscaler](https://github.com/mitchos/pyZscaler) SDK,
which this SDK was inspired on.

## MIT License

=======

Copyright (c) 2023 [Zscaler](https://github.com/zscaler)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
