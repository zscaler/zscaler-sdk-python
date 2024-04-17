.. _examples:

Examples
========

Example scripts
---------------

There are several example scripts written as CLI programs in the 
`examples directory <https://github.com/zscaler/zscaler-sdk-python/tree/master/examples>`_
for both ZPA and ZIA interactions:

* `ZPA Examples <https://github.com/zscaler/zscaler-sdk-python/tree/master/examples/zpa>`_
* `ZIA Examples <https://github.com/zscaler/zscaler-sdk-python/tree/master/examples/zia>`_

ZPA Cookbook examples
---------------------

Get SAML Attribute Information
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

  from zscaler.zpa import ZPAClientHelper

  ZPA_CLIENT_ID = os.getenv("ZPA_CLIENT_ID")
  ZPA_CLIENT_SECRET = os.getenv("ZPA_CLIENT_SECRET")
  ZPA_CUSTOMER_ID = os.getenv("ZPA_CUSTOMER_ID")
  ZPA_CLOUD = os.getenv("ZPA_CLOUD")

  zpa = ZPAClientHelper(client_id=ZPA_CLIENT_ID, client_secret=ZPA_CLIENT_SECRET, customer_id=ZPA_CUSTOMER_ID, cloud=ZPA_CLOUD)

  # Fetch and print SAML attributes using the ZPA client.
  for saml_attribute in zpa.saml_attributes.list_attributes():
      pprint(saml_attribute)

Example output::

  Box({'id': '216199618143191061', 'creation_time': '1651557323', 'modified_by': '216199618143191056', 'name': 'DepartmentName_BD_Okta_Users', 'user_attribute': False, 'idp_id': '216199618143191058', 'saml_name': 'DepartmentName', 'idp_name': 'BD_Okta_Users'})
  Box({'id': '216199618143191062', 'creation_time': '1651557323', 'modified_by': '216199618143191056', 'name': 'Email_BD_Okta_Users', 'user_attribute': False, 'idp_id': '216199618143191058', 'saml_name': 'Email', 'idp_name': 'BD_Okta_Users'})

Print Specific SCIM Group Information
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

  from zscaler.zpa import ZPAClientHelper

  ZPA_CLIENT_ID = os.getenv("ZPA_CLIENT_ID")
  ZPA_CLIENT_SECRET = os.getenv("ZPA_CLIENT_SECRET")
  ZPA_CUSTOMER_ID = os.getenv("ZPA_CUSTOMER_ID")
  ZPA_CLOUD = os.getenv("ZPA_CLOUD")

  zpa = ZPAClientHelper(client_id=ZPA_CLIENT_ID, client_secret=ZPA_CLIENT_SECRET, customer_id=ZPA_CUSTOMER_ID, cloud=ZPA_CLOUD)

  # Fetch and print a Specific SCIM Group using the ZPA client.
  for scim_group in zpa.scim_groups.list_groups(idp_id='123456789', search='A000'):
      pprint(scim_group)

Example output::

  Box({'id': 2079446, 'modified_time': 1699852094, 'creation_time': 1699852094, 'name': 'A000', 'idp_id': 216199618143191058, 'internal_id': 'c32d4677-3ead-4964-bf0a-d4876d5ce5a1'})

ZIA Cookbook examples
---------------------

List of firewall rules by name
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

  import os
  from pprint import pprint
  from zscaler.zia import ZIAClientHelper

  # Environment variables for API access
  ZIA_USERNAME = os.environ.get('ZIA_USERNAME')
  ZIA_PASSWORD = os.environ.get('ZIA_PASSWORD')
  ZIA_API_KEY = os.environ.get('ZIA_API_KEY')
  ZIA_CLOUD = os.environ.get('ZIA_CLOUD')

  # Initialize the ZPAClientHelper with environment variables.
  zia = ZIAClientHelper(username=ZIA_USERNAME, password=ZIA_PASSWORD, api_key=ZIA_API_KEY, cloud=ZIA_CLOUD)

  for rule in zia.firewall.list_rules():
      pprint(rule.name)

Example output::

  'Default Firewall Filtering Rule'
  'Block malicious IPs and domains'
  'UCaaS One Click Rule'
  'Office 365 One Click Rule'
  'Recommended Firewall Rule'
