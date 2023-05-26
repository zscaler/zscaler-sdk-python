# Zscaler SDK Python for the Zscaler API

[![Build Status](https://github.com/zscaler/zscaler-sdk-python/actions/workflows/build.yml/badge.svg)](https://github.com/zscaler/zscaler-sdk-python/actions/workflows/build.yml)
[![Documentation Status](https://readthedocs.org/projects/zscaler/badge/?version=latest)](https://zscaler.readthedocs.io/?badge=latest)
[![License](https://img.shields.io/github/license/zscaler/zscaler-sdk-python.svg)](https://github.com/zscaler/zscaler-sdk-python)
[![Code Quality](https://app.codacy.com/project/badge/Grade/d339fa5d957140f496fdb5c40abc4666)](https://www.codacy.com/gh/zscaler/zscaler-sdk-python/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=zscaler/zscaler-sdk-python&amp;utm_campaign=Badge_Grade)
[![PyPI Version](https://img.shields.io/pypi/v/zscaler.svg)](https://pypi.org/project/zscaler-sdk-python)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/zscaler.svg)](https://pypi.python.org/pypi/zscaler-sdk-python/)
[![GitHub Release](https://img.shields.io/github/release/zscaler/zscaler-sdk-python.svg)](https://github.com/zscaler/zscaler-sdk-python/releases/)

Zscaler SDK Python is an SDK that provides a uniform and easy-to-use interface for each of the Zscaler product APIs.

## Quick links
* [Zscaler SDK Python API Documentation](https://zscaler-sdk-python.readthedocs.io)

## Overview
Each Zscaler product has separate developer documentation and authentication methods. This SDK simplifies
software development using the Zscaler API.

This SDK leverages the [RESTfly framework](https://restfly.readthedocs.io/en/latest/index.html) developed
by Steve McGrath.

## Features
- Simplified authentication with Zscaler APIs.
- Uniform interaction with all Zscaler APIs.
- Uses [python-box](https://github.com/cdgriffith/Box/wiki) to add dot notation access to json data structures.
- Zscaler API output automatically converted from CamelCase to Snake Case.
- Various quality of life enhancements for object CRUD methods.

## Products
- Zscaler Private Access (ZPA)
- Zscaler Internet Access (ZIA)

## Installation

The most recent version can be installed from pypi as per below.

    $ pip install zscaler-sdk-python

## Usage

Before you can interact with any of the Zscaler APIs, you may need to generate API keys or retrieve tenancy information
for each product that you are interfacing with. Once you have the requirements and you have installed Zscaler SDK Python, you're ready to go.

### Quick ZIA Example

```python
from zscaler import ZIA
from pprint import pprint

zia = ZIA(api_key='API_KEY', cloud='CLOUD', username='USERNAME', password='PASSWORD')
for user in zia.users.list_users():
    pprint(user)
```

### Quick ZPA Example

```python
from zscaler import ZPA
from pprint import pprint

zpa = ZPA(client_id='CLIENT_ID', client_secret='CLIENT_SECRET', customer_id='CUSTOMER_ID')
for app_segment in zpa.app_segments.list_segments():
    pprint(app_segment)
```

## Documentation
### API Documentation
Zscaler SDK Python's API is fully 100% documented and is hosted at [ReadTheDocs](https://zscaler-sdk-python.readthedocs.io).

This documentation should be used when working with Zscaler SDK Python rather than referring to Zscaler's API reference.
Zscaler SDK Python makes some quality of life improvements to simplify and clarify arguments passed to Zscaler's API.

## Is It Tested?
Yes! Zscaler SDK Python has a complete test suite that fully covers all methods within the ZIA and ZPA modules.

## Contributing

Contributions to Zscaler SDK Python are absolutely welcome.

Please see the [Contribution Guidelines](https://github.com/zscaler/zscaler-sdk-python/blob/main/CONTRIBUTING.md) for more information.

[Poetry](https://python-poetry.org/docs/) is currently being used for builds and management. You'll want to have
poetry installed and available in your environment.

## Issues
Please feel free to open an issue using [Github Issues](https://github.com/zscaler/zscaler-sdk-python/issues) if you run into any problems using Zscaler SDK Python.

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
