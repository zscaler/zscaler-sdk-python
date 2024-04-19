.. meta::
   :description lang=en:
        Official Zscaler Python  SDK that provides a simple and uniform interface for each of the Zscaler product APIs.
.. toctree::
   :maxdepth: 2
   :hidden:
   :caption: Contents

   zs/zia/index
   zs/zpa/index
   zs/guides/index

Zscaler SDK Python (Beta) - Library Reference
=====================================================================
Zscaler SDK Python is an SDK that provides a uniform and easy-to-use interface for each of the Zscaler product APIs.

Support Disclaimer
========================

-> **Disclaimer:** Please refer to our `General Support Statement <docs/guides/support.rst>`_ before proceeding with the use of this provider. 
You can also refer to our `troubleshooting guide <docs/guides/troubleshooting.rst>`_ for guidance on typical problems.

.. attention:: This SDK is supported and maintained by the Zscaler Technology Alliances team.

Quick Links
--------------
- `Zscaler SDK Python User Documentation and Examples <htthttps://zscaler-sdk-python.readthedocs.io/en/latest/>`_
- `Zscaler SDK Python SDK on GitHub <https://zscaler-sdk-python.readthedocs.io/en/latest/>`_


Overview
==========
This site is the library reference for the Zscaler SDK Python and describes every class and method in detail. If you are
looking for user documentation with explanations and examples then you might be looking for the
`Zscaler SDK Python User Documentation <https://zscaler-sdk-python.readthedocs.io/en/latest/>`_

Features
----------
- Simplified authentication with Zscaler APIs.
- Uniform interaction with all Zscaler APIs.
- Uses `python-box <https://github.com/cdgriffith/Box/wiki>`_ to add dot notation access to json data structures.
- Zscaler API output automatically converted from CamelCase to Snake Case.
- Various quality of life enhancements for object update methods.

Products
---------
This repository contains the Zscaler SDK for Python. This SDK can be used to interact with several Zscaler services such as:

- :doc:`Zscaler Private Access (ZPA) <zs/zpa/index>`
- :doc:`Zscaler Internet Access (ZIA) <zs/zia/index>`

* `Documentation <https://zscaler-sdk-python.readthedocs.io>`_

Installation
==============

The most recent version can be installed from pypi as per below.

.. code-block:: console

    $ pip install zscaler-sdk-python

Usage
========
Before you can interact with any of the Zscaler APIs, you may need to generate API keys or retrieve tenancy information
for each product that you are interfacing with. Once you have the requirements and you have installed Zscaler SDK Python,
you're ready to go.

Getting started
--------------------------

Quick ZIA Example
^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    from zscaler import ZIAClientHelper
    from pprint import pprint

    zia = ZIAClientHelper(api_key='ZIA_API_KEY', cloud='ZIA_CLOUD', username='ZIA_USERNAME', password='ZIA_PASSWORD')
    for user in zia.users.list_users():
        pprint(user)

Quick ZPA Example
^^^^^^^^^^^^^^^^^^

.. code-block:: python

    from zscaler import ZPAClientHelper
    from pprint import pprint

    zpa = ZPAClientHelper(client_id='ZPA_CLIENT_ID', client_secret='ZPA_CLIENT_SECRET', customer_id='ZPA_CUSTOMER_ID')
    for app_segment in zpa.app_segments.list_segments():
        pprint(app_segment)

.. automodule:: zscaler
   :members:

Contributing
==============
At this moment we are not accepting contributions, but we welcome suggestions on how to improve this SDK or feature requests, which can then be added in future releases.
Issues

Please feel free to open an issue using `Github Issues <https://github.com/zscaler/zscaler-sdk-python/issues>`_ 
if you run into any problems using Zscaler SDK Python or please refer to our `General Support Statement <docs/guides/support.rst>`_

Contributors
------------

* William Guilherme - `willguibr <https://github.com/willguibr>`_
* Eddie Parra - `eparra <https://github.com/eparra>`_
* Paul Abbot - `abbottp <https://github.com/abbottp>`_

License
=========
MIT License

Copyright (c) 2023 Zscaler Inc.

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