# Official Python SDK for the Zscaler Products (Beta)

[![PyPI - Downloads](https://img.shields.io/pypi/dw/zscaler-sdk-python)](https://pypistats.org/packages/zscaler-sdk-python)
[![License](https://img.shields.io/github/license/zscaler/zscaler-sdk-python.svg)](https://github.com/zscaler/zscaler-sdk-python)
[![Documentation Status](https://readthedocs.org/projects/zscaler-sdk-python/badge/?version=latest)](https://zscaler-sdk-python.readthedocs.io/en/latest/?badge=latest)
[![Latest version released on PyPi](https://img.shields.io/pypi/v/zscaler-sdk-python.svg)](https://pypi.org/project/zscaler-sdk-python)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/zscaler-sdk-python.svg)](https://pypi.python.org/pypi/zscaler-sdk-python/)
[![Zscaler Community](https://img.shields.io/badge/zscaler-community-blue)](https://community.zscaler.com/)

## Support Disclaimer

-> **Disclaimer:** Please refer to our [General Support Statement](docsrc/zs/guides/support.rst) before proceeding with the use of this provider. You can also refer to our [troubleshooting guide](docsrc/zs/guides/troubleshooting.rst) for guidance on typical problems.

## Zscaler Python SDK Overview

The Zscaler SDK for Python includes functionality to accelerate development with [Python](https://www.python.org/) several Zscaler services such as:

* [Zscaler Internet Access (ZIA)](https://help.zscaler.com/zia/getting-started-zia-api)
* [Zscaler Private Access (ZPA)](https://help.zscaler.com/zpa/getting-started-zpa-api)
* [Documentation](http://zscaler-sdk-python.readthedocs.io)

Each package is supportedd by an individual and robust HTTP client designed to handle failures on different levels by performing intelligent retries.

**Beta:** This SDK is supported for production use cases, but we do expect future releases to have some interface changes; see [Interface stability](#interface-stability). 
We are keen to hear feedback from you on these SDKs. Please [file issues](https://github.com/zscaler/zscaler-sdk-python/issues), and we will address them. 

## Contents

- [Getting Started](#getting-started)
- [Usage](#usage)
- [Authentication](#authentication)
- [Pagination](#pagination)
- [Logging](#logging)
- [Rate Limiting](#rate-limiting)
- [Environment variables](#environment-variables)
- [Building the SDK](#building-the-sdk)
- [Interface stability](#interface-stability)
- [Need help?](#need-help)
- [Contributing](#contributing)

> Requires Python version 3.8.0 or higher.

## Getting started<a id="getting-started"></a>

To install the Zscaler Python SDK in your project:
1. Please install Zscaler SDK for Python via `pip install zscaler-sdk-python` and instantiate the respective client based on your project usage:
- `ZIAClientHelper`
- `ZPAClientHelper`

Zscaler SDK for Python is compatible with Python 3.7 _(until [June 2023](https://devguide.python.org/versions/))_, 3.8, 3.9, 3.10, and 3.11.

The upgrade to the latest version of this SDK can be done by executing the following command:
```python
%pip install --upgrade zscaler-sdk-python
```
followed by
```python
dbutils.library.restartPython()
```

## Authentication<a id="authentication"></a>

Each Zscaler product has separate developer documentation and authentication methods. In this section you will find

1. Credentials that are hard-coded into configuration arguments.

   :warning: **Caution**: Zscaler does not recommend hard-coding credentials into arguments, as they can be exposed in plain text in version control systems. Use environment variables instead.

### ZIA native authentication

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

### ZPA native authentication

- For authentication via Zscaler Private Access, you must provide `client_id`, `client_secret`, `customer_id` and `cloud`

The ZPA Cloud is identified by several cloud name prefixes, which determines which API endpoint the requests should be sent to. The following cloud environments are supported:

* `PRODUCTION`
* `ZPATWO`
* `BETA`
* `GOV`
* `GOVUS`

### Environment variables

You can provide credentials via the `ZPA_CLIENT_ID`, `ZPA_CLIENT_SECRET`, `ZPA_CUSTOMER_ID`, `ZPA_CLOUD` environment variables, representing your ZPA `client_id`, `client_secret`, `customer_id` and `cloud` of your ZPA account, respectively.

~> **NOTE** `ZPA_CLOUD` environment variable is required, and is used to identify the correct API gateway where the API requests should be forwarded to.

| Argument     | Description | Environment variable |
|--------------|-------------|-------------------|
| `client_id`       | _(String)_ The ZPA API client ID generated from the ZPA console.| `ZPA_CLIENT_ID` |    
| `client_secret`       | _(String)_ The ZPA API client secret generated from the ZPA console.| `ZPA_CLIENT_SECRET` |
| `customer_id`       | _(String)_ The ZPA tenant ID found in the Administration > Company menu in the ZPA console.| `ZPA_CUSTOMER_ID` |   
| `cloud`       | _(String)_ The Zscaler cloud for your tenancy.| `ZPA_CLOUD` |

## Usage<a id="usage"></a>

Before you can interact with any of the Zscaler APIs, you need to generate API keys or retrieve tenancy information for each product that you are interfacing with. Once you have the requirements and you have installed Zscaler SDK Python, you're ready to go.

### Quick ZIA Example

```python
from zscaler import ZIAClientHelper
from pprint import pprint

zia = ZIAClientHelper(username='ZIA_USERNAME', password='ZIA_PASSWORD', api_key='ZIA_API_KEY', cloud='ZIA_CLOUD')
for user in zia.users.list_users():
    pprint(user)
```

### Quick ZPA Example

```python
from zscaler import ZPAClientHelper
from pprint import pprint

zpa = ZPAClientHelper(client_id='ZPA_CLIENT_ID', client_secret='ZPA_CLIENT_SECRET', customer_id='ZPA_CUSTOMER_ID', cloud='ZPA_CLOUD')
for app_segment in zpa.app_segments.list_segments():
    pprint(app_segment)
```

~> **NOTE** The `ZPA_CLOUD` environment variable is optional and only required if your project needs to interact with any other ZPA cloud other than production cloud. In this case, use the `ZPA_CLOUD` environment variable followed by the name of the corresponding environment: `ZPA_CLOUD=BETA`, `ZPA_CLOUD=ZPATWO`, `ZPA_CLOUD=GOV`, `ZPA_CLOUD=GOVUS`, `ZPA_CLOUD=PREVIEW`, `ZPA_CLOUD=DEV`.

## Pagination<a id="pagination"></a>

This SDK provides methods that retrieve a list of resources from the API, which return paginated results due to the volume of data. Each method capable of returning paginated data is prefixed as `list_` and handles the pagination internally by providing an easy interface to iterate through pages. The user does not need to manually fetch each page; instead, they can process items as they iterate through them.

### Example of Iterating Over Paginated Results

The following example shows how you can list ZPA items using this SDK, processing each item one at a time. This pattern is useful for operations that need to handle large datasets efficiently.

```python
from zscaler import ZPAClientHelper
from pprint import pprint

# Initialize the client
zpa = ZPAClientHelper(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, customer_id=CUSTOMER_ID, cloud=CLOUD)

for apps in zpa.app_segments.list_segments():
    pprint(apps)
```

### Customizing Pagination Parameters

While pagination is handled automatically, you can also customize pagination behavior by specifying parameters such as data_per_page and max_items. These parameters give you control over the volume of data fetched per request and the total amount of data to process. This is useful for limiting the scope of data fetched

* `max_pages`: controls the number of items fetched per API call (per page).
* `max_items`: controls the total number of items to retrieve across all pages. 

```python
from zscaler import ZPAClientHelper
from pprint import pprint

# Initialize the client
zpa = ZPAClientHelper(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, customer_id=CUSTOMER_ID, cloud=CLOUD)

pagination_params = {
    'max_pages': 1,
    'max_items': 5
}

# Fetch data using custom pagination settings
segments = zpa.app_segments.list_segments(**pagination_params)
for segment in segments:
    pprint(segment)
```

### Efficient Pagination Handling

For more details on each pagination parameter see:
[ZPA Pagination Parameters](zscaler/zpa/README.md)
[ZIA Pagination Parameters](zscaler/zia/README.md)

## Logging<a id="logging"></a>

The Zscaler SDK Python, provides robust logging for debug purposes.
Logs are disabled by default and should be enabled explicitly via custom environment variable:

* `ZSCALER_SDK_LOG` - Turn on logging
* `ZSCALER_SDK_VERBOSE` - Turn on logging in verbose mode

```sh
export ZSCALER_SDK_LOG=true
export ZSCALER_SDK_VERBOSE=true
```

**NOTE**: DO NOT SET DEBUG LEVEL IN PRODUCTION!

You should now see logs in your console. Notice that API tokens are **NOT** logged to the console; however, we still advise to use caution and never use `DEBUG` level logging in production.

What it being logged? `requests`, `responses`,  `http errors`, `caching responses`.

## Environment variables<a id="environment-variables"></a>

Each one of the configuration values above can be turned into an environment variable name with the `_` (underscore) character and UPPERCASE characters. The following are accepted:

- `ZSCALER_CLIENT_CACHE_ENABLED` - Enable or disable the caching mechanism within the clien
- `ZSCALER_CLIENT_CACHE_DEFAULT_TTL` - Duration (in seconds) that cached data remains valid. By default data is cached in memory for `3600` seconds.
- `ZSCALER_CLIENT_CACHE_DEFAULT_TTI` - This environment variable sets the maximum amount of time (in seconds) that cached data can remain in the cache without being accessed. If the cached data is not accessed within this timeframe, it is removed from the cache, regardless of its TTL. The default TTI is `1800` seconds (`30 minutes`) 
- `ZSCALER_SDK_LOG` - Turn on logging
- `ZSCALER_SDK_VERBOSE` - Turn on logging in verbose mode

## Rate Limiting<a id="rate-limiting"></a>

Zscaler provides unique rate limiting numbers for each individual product. Regardless of the product, a 429 response will be returned if too many requests are made within a given time. 
Please see:
* [ZPA Rate Limiting][rate-limiting-zpa] for rate limiting requirements.
* [ZIA Rate Limiting][rate-limiting-zia] for a complete list of which endpoints are rate limited.

When a 429 error is received, the `Retry-After` header will tell you the time at which you can retry. This section discusses the method for handling rate limiting with this SDK.

### Built-In Retry

This SDK uses the built-in retry strategy to automatically retry on 429 errors. The default Maximum Retry Attempts for both ZIA and ZPA explicitly limits the number of retry attempts to a maximum of `5`.

Retry Conditions: The client for both ZPA and ZIA retries a request under the following conditions:

* HTTP status code 429 (Too Many Requests): This indicates that the rate limit has been exceeded. The client waits for a duration specified by the `Retry-After` header, if present, or a default of `2 ` seconds, before retrying.

* Exceptions during request execution: Any requests.RequestException encountered during the request triggers a retry, except on the last attempt, where the exception is raised.

## Building the SDK<a id="building-the-sdk"></a>

In most cases, you won't need to build the SDK from source. If you want to build it yourself, you'll need these prerequisites:

- Clone the repo
- Run `make build:dist` from the root of the project (assuming Python is installed)
- Ensure tests run succesfully by executing `make test-simple`
- Install `tox` if not installed already using: `pip install tox`. 
- Run tests using `tox` in the root directory of the project.

## Interface stability<a id="interface-stability"></a>

Zscaler is actively working on stabilizing the Zscaler SDK for Python's interfaces.  
You are highly encouraged to pin the exact dependency version and read the [changelog](https://github.com/zscaler/zscaler-sdk-python/blob/master/CHANGELOG.md) 
where Zscaler documents the changes. Zscaler may have minor [documented](https://github.com/zscaler/zscaler-sdk-python/blob/master/CHANGELOG.md)
backward-incompatible changes, such as renaming some type names to bring more consistency.

## Contributing<a id="contributing"></a>

At this moment we are not accepting contributions, but we welcome suggestions on how to improve this SDK or feature requests, which can then be added in  future releases.

[zenith]: https://community.zscaler.com/
[zscaler-support]: https://help.zscaler.com/contact-support
[github-issues]: https://github.com/zscaler/zscaler-sdk-python/issues
[rate-limiting-zpa]: https://help.zscaler.com/zpa/understanding-rate-limiting
[rate-limiting-zia]: https://help.zscaler.com/zia/understanding-rate-limiting

## Need help?<a id="need-help"></a>

If you run into problems using the SDK, you can:

- Ask questions on the [Zenith Community][zenith]
- Post [issues on GitHub][github-issues] (for code errors)
- Support [customer support portal][zscaler-support]

Contributors
------------

- William Guilherme - [willguibr](https://github.com/willguibr)
- Eddie Parra - [eparra](https://github.com/eparra)
- Paul Abbot - [abbottp](https://github.com/abbottp)

## License
MIT License

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
