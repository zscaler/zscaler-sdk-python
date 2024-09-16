.. _release-notes:

Release Notes
=============

Zscaler Python SDK Changelog
----------------------------

0.9.3 (September, 16 2024)
---------------------------

Notes
^^^^^

- Python Versions: **v3.8, v3.9, v3.10, v3.11**

### Bug Fixes

* Added function `list_version_profiles` to ZPA `connectors` package  (`156 <https://github.com/zscaler/zscaler-sdk-python/pull/156>`_)

0.9.2 (August, 31 2024)
------------------------

Notes
^^^^^

- Python Versions: **v3.8, v3.9, v3.10, v3.11**

Bug Fixes
------------


- Added Zscaler Mobile Admin Portal package (`#154 <https://github.com/zscaler/zscaler-sdk-python/pull/154>`_)

0.9.1 (August, 31 2024)
------------------------

Notes
^^^^^

- Python Versions: **v3.8, v3.9, v3.10, v3.11**

Enhancements
------------

Zscaler Mobile Portal
^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Added Zscaler Mobile Admin Portal package(`#142 <https://github.com/zscaler/zscaler-sdk-python/pull/142>`_)

0.9.0 (August, 23 2024)
------------------------

Notes
^^^^^

- Python Versions: **v3.8, v3.9, v3.10, v3.11**

Enhancements
------------

ZPA Segment Group
^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Added new ZPA PUT v2 Endpoint for Segment Group Updates (`#136 <https://github.com/zscaler/zscaler-sdk-python/pull/136>`_)

0.8.0 (August, 17 2024)
------------------------

Notes
^^^^^

- Python Versions: **v3.8, v3.9, v3.10, v3.11**

Enhancements
------------

ZIA Cloud App Control Rules
^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Added new ZIA Cloud App Control Rule and URL Domain Review Endpoints (`#132 <https://github.com/zscaler/zscaler-sdk-python/pull/132>`_)

0.7.0 (July, 26 2024)
----------------------

Notes
^^^^^

- Python Versions: **v3.8, v3.9, v3.10, v3.11**

Enhancements
------------

ZIA Cloud App Control Rules
^^^^^^^^^^^^^^^^^^^^^^^^^^^

- `GET /webApplicationRules/{rule_type}` to Get the list of Web Application Rule by type (`#135 <https://github.com/zscaler/zscaler-sdk-python/pull/135>`_)
- `GET /webApplicationRules/{rule_type}/{ruleId}` to Get a Web Application Rule by type and id (`#135 <https://github.com/zscaler/zscaler-sdk-python/pull/135>`_)
- `POST /webApplicationRules/{rule_type}` to Adds a new Web Application rule (`#135 <https://github.com/zscaler/zscaler-sdk-python/pull/135>`_)
- `PUT /webApplicationRules/{rule_type}/{ruleId}` to Update a new Web Application rule (`#135 <https://github.com/zscaler/zscaler-sdk-python/pull/135>`_)
- `DELETE /webApplicationRules/{rule_type}/{ruleId}` to Delete a new Web Application rule (`#135 <https://github.com/zscaler/zscaler-sdk-python/pull/135>`_)

ZIA URL Categories
^^^^^^^^^^^^^^^^^^

- Added `review_domains_post` function `POST /urlCategories/review/domains` to find matching entries present in existing custom URL categories. (`#132 <https://github.com/zscaler/zscaler-sdk-python/pull/132>`_)
- Added `review_domains_put` function `PUT /urlCategories/review/domains` to Add the list of matching URLs fetched by POST /urlCategories/review/domains to the specified custom URL categories. (`#132 <https://github.com/zscaler/zscaler-sdk-python/pull/132>`_)
- Added new attribute `urlCategories2` to `urlfilteringrules` package. See (`Zscaler Release Notes <https://help.zscaler.com/zia/release-upgrade-summary-2024#:~:text=Filtering%20Policy.-,Update%20to%20Cloud%20Service%20API,-The%20UrlFilteringRule%20model>`_)(`#132 <https://github.com/zscaler/zscaler-sdk-python/pull/132>`_)

Data Loss Prevention
^^^^^^^^^^^^^^^^^^^^

- Added `list_dict_predefined_identifiers` function `GET /dlpDictionaries/{dictId}/predefinedIdentifiers` to retrieves the list of identifiers that are available for selection in the specified hierarchical DLP dictionary.(`#132 <https://github.com/zscaler/zscaler-sdk-python/pull/132>`_)
- Added `validate_dlp_expression` function `GET /dlpEngines/validateDlpExpr` to Validates a DLP engine expression.(`#132 <https://github.com/zscaler/zscaler-sdk-python/pull/132>`_)
- Added `list_edm_schemas` function `GET /dlpExactDataMatchSchemas` to retrieves a list of ZIA DLP Exact Data Match Schemas.(`#132 <https://github.com/zscaler/zscaler-sdk-python/pull/132>`_)
- Added `list_edm_schema_lite` function `GET /dlpExactDataMatchSchemas` to retrieves a list of active EDM templates (or EDM schemas) and their criteria (or token details), only.(`#132 <https://github.com/zscaler/zscaler-sdk-python/pull/132>`_)

0.6.2 (July, 19 2024)
----------------------

Notes
^^^^^

- Python Versions: **v3.8, v3.9, v3.10, v3.11**

Bug Fixes
^^^^^^^^^

- Fixed ZPA Resources and ZIA is_expired method  (`#125 <https://github.com/zscaler/zscaler-sdk-python/pull/125>`_)

0.6.1 (July, 4 2024)
----------------------

Notes
^^^^^

- Python Versions: **v3.8, v3.9, v3.10, v3.11**

Bug Fixes
^^^^^^^^^

- Fixed ZPA Pagination pagesize parameter to the maximum supported of `500`  (`#118 <https://github.com/zscaler/zscaler-sdk-python/pull/118>`_)
- Fixed ZIA Isolation Profile method misconfiguration (`#118 <https://github.com/zscaler/zscaler-sdk-python/pull/118>`_)

Enhancements
^^^^^^^^^^^^

- Added the following new ZIA location management endpoints (`#118 <https://github.com/zscaler/zscaler-sdk-python/pull/118>`_)
    - `locations/bulkDelete`
    - `locations/groups/count`

0.6.0 (June, 28 2024)
----------------------

Notes
^^^^^

- Python Versions: **v3.8, v3.9, v3.10, v3.11**

Enhancements
^^^^^^^^^^^^

- Added ZDX Endpoints, Tests and Examples (`#116 <https://github.com/zscaler/zscaler-sdk-python/pull/116>`_)

0.5.2 (June, 24 2024)
----------------------

Notes
^^^^^

- Python Versions: **v3.8, v3.9, v3.10, v3.11**

Bug Fixes
^^^^^^^^^

- Added and Fixed ZIA integration tests. (`#113 <https://github.com/zscaler/zscaler-sdk-python/pull/113>`_)

0.5.1 (June, 20 2024)
----------------------

Notes
^^^^^

- Python Versions: **v3.8, v3.9, v3.10, v3.11**

Bug Fixes
^^^^^^^^^

- Added and Fixed ZIA integration tests. (`#112 <https://github.com/zscaler/zscaler-sdk-python/pull/112>`_)

0.5.0 (June, 19 2024)
----------------------

Notes
^^^^^

- Python Versions: **v3.8, v3.9, v3.10, v3.11**

Bug Fixes
^^^^^^^^^

- Fixed ZIA `forwarding_control` nested attribute formatting. (`#111 <https://github.com/zscaler/zscaler-sdk-python/pull/111>`_)
- Fixed ZIA `zpa_gateway` nested attribute formatting. (`#111 <https://github.com/zscaler/zscaler-sdk-python/pull/111>`_)

0.4.0 (June, 07 2024)
----------------------

Notes
^^^^^

- Python Versions: **v3.8, v3.9, v3.10, v3.11**

Enhancements
^^^^^^^^^^^^

- Added support to ZPA Microtenant endpoints. (`#105 <https://github.com/zscaler/zscaler-sdk-python/pull/105>`_)

0.3.1 (May, 29 2024)
----------------------

Notes
^^^^^

- Python Versions: **v3.8, v3.9, v3.10, v3.11**

Enhancements
^^^^^^^^^^^^

- Enhanced zpa rate-limit with retry-after header tracking (`#100 <https://github.com/zscaler/zscaler-sdk-python/pull/100>`_)

0.3.0 (May, 25 2024)
----------------------

Notes
^^^^^

- Python Versions: **v3.8, v3.9, v3.10, v3.11**

Enhancements
^^^^^^^^^^^^

- Added support the zpa policy set v2 endpoints (`#96 <https://github.com/zscaler/zscaler-sdk-python/pull/96>`_)

0.2.0 (May, 14 2024)
----------------------

Notes
^^^^^

- Python Versions: **v3.8, v3.9, v3.10, v3.11**

Enhancements
^^^^^^^^^^^^

- Added Cloud Browser Isolation Endpoints and Tests (`#86 <https://github.com/zscaler/zscaler-sdk-python/pull/86>`_)

0.1.8 (May, 06 2024)
----------------------

Notes
^^^^^

- Python Versions: **v3.8, v3.9, v3.10, v3.11**

Enhancements
^^^^^^^^^^^^

- Fixed privileged remote access add_portal method return response (`#86 <https://github.com/zscaler/zscaler-sdk-python/pull/86>`_)

0.1.7 (May, 06 2024)
----------------------

Notes
^^^^^

- Python Versions: **v3.8, v3.9, v3.10, v3.11**

Internal Changes
^^^^^^^^^^^^^^^^

- Upgraded python-box to v7.1.1

0.1.6 (April, 30 2024)
----------------------

Notes
^^^^^

- Python Versions: **v3.8, v3.9, v3.10, v3.11**

Internal Changes
^^^^^^^^^^^^^^^^

- Added CodeCov workflow step. (`#83 <https://github.com/zscaler/zscaler-sdk-python/pull/83>`_)

0.1.5 (April, 26 2024)
----------------------

Notes
^^^^^

- Python Versions: **v3.8, v3.9, v3.10, v3.11**

Bug Fixes
^^^^^^^^^

- Update ZPA LSS clientTypes and log formats to new lss v2 endpoint. (`#77 <https://github.com/zscaler/zscaler-sdk-python/pull/77>`_)

0.1.4 (April, 26 2024)
----------------------

Notes
^^^^^

- Python Versions: **v3.8, v3.9, v3.10, v3.11**

Bug Fixes
^^^^^^^^^

- Fixed ZPA Connector Schedule functions due to endpoint handler change. (`#76 <https://github.com/zscaler/zscaler-sdk-python/pull/76>`_)

0.1.3 (April, 24 2024)
----------------------

Notes
^^^^^

- Python Versions: **v3.8, v3.9, v3.10, v3.11**

Internal Changes
^^^^^^^^^^^^^^^^

- Removed .devcontainer directory and updated makefile. (`#75 <https://github.com/zscaler/zscaler-sdk-python/pull/75>`_)
- Transition from setup.py to Poetry (`#75 <https://github.com/zscaler/zscaler-sdk-python/pull/75>`_)

0.1.2 (April, 20 2024)
----------------------

Notes
^^^^^

- Python Versions: **v3.8, v3.9, v3.10, v3.11**

Bug Fixes
^^^^^^^^^

- Fixed ZIA `list_dlp_incident_receiver` method to return proper `Box` response (`#67 <https://github.com/zscaler/zscaler-sdk-python/pull/67>`_)
- Fixed ZIA sandbox `get_file_hash_count` to properly parse the API response (`#67 <https://github.com/zscaler/zscaler-sdk-python/pull/67>`_)
- Removed pre-shared-key randomization from `add_vpn_credential` (`#67 <https://github.com/zscaler/zscaler-sdk-python/pull/67>`_)

0.1.1 (April, 19 2024)
----------------------

Notes
^^^^^

- Python Versions: **v3.8, v3.9, v3.10, v3.11**

Internal Changes
^^^^^^^^^^^^^^^^

- Refactored `setup.py` for better packaging and improved long description through README.md (`#57 <https://github.com/zscaler/zscaler-sdk-python/pull/57>`_)
- Refactored Integration Tests by removing `async` decorators (`#63 <https://github.com/zscaler/zscaler-sdk-python/pull/63>`_)

0.1.0 (April, 18 2024)
----------------------

Notes
^^^^^

- Python Versions: **v3.8, v3.9, v3.10, v3.11**

Internal Changes
^^^^^^^^^^^^^^^^

- 🎉 **Initial Release** 🎉
