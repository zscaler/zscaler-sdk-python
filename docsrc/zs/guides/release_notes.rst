.. _release-notes:

Release Notes
=============

Zscaler Python SDK Changelog
----------------------------

1.5.2 (June 23, 2025)
-------------------------

Notes
-----

- Python Versions: **v3.8, v3.9, v3.10, v3.11**

Bug Fixes
-----------

* (`#312 <https://github.com/zscaler/zscaler-sdk-python/pull/312>`_) - Refactored ZIA Cloud Firewall Rules client to assign `state` from `enabled` directly on request body for improved clarity and maintainability.

1.5.1 (June 23, 2025)
-------------------------

Notes
-----

- Python Versions: **v3.8, v3.9, v3.10, v3.11**

Bug Fixes
-----------

* (`#312 <https://github.com/zscaler/zscaler-sdk-python/pull/312>`_) - Refactored ZIA Cloud Firewall Rules client to assign `state` from `enabled` directly on request body for improved clarity and maintainability.
* (`#312 <https://github.com/zscaler/zscaler-sdk-python/pull/312>`_) - Removed `url` positional argument from `add_url_category`

1.5.0 (June 18, 2025)
-------------------------

Notes
-----

- Python Versions: **v3.8, v3.9, v3.10, v3.11**

New ZIA Endpoint - Browser Control Policy
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* (`#309 <https://github.com/zscaler/zscaler-sdk-python/pull/309>`_) Added the following new ZIA API Endpoints:
    - Added `GET /browserControlSettings` Retrieves the Browser Control status and the list of configured browsers in the Browser Control policy
    - Added `PUT /browserControlSettings` Updates the Browser Control settings.

New ZIA Endpoint - SaaS Security API (Casb DLP Rules)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* (`#309 <https://github.com/zscaler/zscaler-sdk-python/pull/309>`_) Added the following new ZIA API Endpoints:
    - Added `GET /casbDlpRules` Retrieves the SaaS Security Data at Rest Scanning Data Loss Prevention (DLP) rules based on the specified rule type.
    - Added `GET /casbDlpRules/{ruleId}` Retrieves the SaaS Security Data at Rest Scanning DLP rule based on the specified ID
    - Added `GET /casbDlpRules/all` Retrieves all the SaaS Security Data at Rest Scanning DLP rules
    - Added `POST /casbDlpRules` Adds a new SaaS Security Data at Rest Scanning DLP rule
    - Added `PUT /casbDlpRules/{ruleId}` Updates the SaaS Security Data at Rest Scanning DLP rule based on the specified ID
    - Added `DELETE /casbDlpRules/{ruleId}` Deletes the SaaS Security Data at Rest Scanning DLP rule based on the specified ID

New ZIA Endpoint - SaaS Security API (Casb Malware Rules)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* (`#309 <https://github.com/zscaler/zscaler-sdk-python/pull/309>`_) Added the following new ZIA API Endpoints:
    - Added `GET /casbMalwareRules` Retrieves the SaaS Security Data at Rest Scanning Malware Detection rules based on the specified rule type.
    - Added `GET /casbMalwareRules/{ruleId}` Retrieves the SaaS Security Data at Rest Scanning Malware Detection rule based on the specified ID
    - Added `GET /casbMalwareRules/all` Retrieves all the SaaS Security Data at Rest Scanning Malware Detection rules
    - Added `POST /casbMalwareRules` Adds a new SaaS Security Data at Rest Scanning Malware Detection rule.
    - Added `PUT /casbMalwareRules/{ruleId}` Updates the SaaS Security Data at Rest Scanning Malware Detection rule based on the specified ID
    - Added `DELETE /casbMalwareRules/{ruleId}` Deletes the SaaS Security Data at Rest Scanning Malware Detection rule based on the specified ID

New ZIA Endpoint - SaaS Security API
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* (`#309 <https://github.com/zscaler/zscaler-sdk-python/pull/309>`_) Added the following new ZIA API Endpoints:
    - Added `GET /domainProfiles/lite` Retrieves the domain profile summary.
    - Added `GET /quarantineTombstoneTemplate/lite` Retrieves the templates for the tombstone file created when a file is quarantined
    - Added `GET /casbEmailLabel/lite` Retrieves the email labels generated for the SaaS Security API policies in a user's email account
    - Added `GET /casbTenant/{tenantId}/tags/policy` Retrieves the tags used in the policy rules associated with a tenant, based on the tenant ID.
    - Added `GET /casbTenant/lite` Retrieves information about the SaaS application tenant

Enhancements
--------------

* (`#309 <https://github.com/zscaler/zscaler-sdk-python/pull/309>`_) - Added support for rateLimit.`maxRetrySeconds` in OneAPI client config to cap retry wait duration when encountering rate-limiting (HTTP 429). Raises zscaler.RetryTooLong if exceeded (`Issue #303 <https://github.com/zscaler/zscaler-sdk-python/issues/303>`_). This enhancement addresses API limitations with the ZCC endpoints below due to daily hard limits:
  - `/downloadDevices`
  - `/downloadServiceStatus`

Bug Fixes
-----------

* (`#309 <https://github.com/zscaler/zscaler-sdk-python/pull/309>`_) - Fixed JSON serialization for the method `lookup` in the ZIA package to ensure consistency on payload processing between Legacy client path and OneAPI.
* (`#309 <https://github.com/zscaler/zscaler-sdk-python/pull/309>`_) - Fixed ZDX `devices` model to address dictionary processing.

1.4.4 (June, 5 2025)
-------------------------

Notes
-----

- Python Versions: **v3.8, v3.9, v3.10, v3.11**

New ZIA Endpoint - Virtual ZEN Clusters
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* (`#299 <https://github.com/zscaler/zscaler-sdk-python/pull/299>`_) - Added the following new ZIA API Endpoints:
    - Added `GET /virtualZenClusters` Retrieves a list of ZIA Virtual Service Edge clusters.
    - Added `GET /virtualZenClusters/{cluster_id}` Retrieves the Virtual Service Edge cluster based on the specified ID
    - Added `POST /virtualZenClusters` Adds a new Virtual Service Edge cluster. 
    - Added `PUT /virtualZenClusters/{cluster_id}` Updates the Virtual Service Edge cluster based on the specified ID
    - Added `DELETE /virtualZenClusters/{cluster_id}` Deletes the Virtual Service Edge cluster based on the specified ID

New ZIA Endpoint - Alert Subscription
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* (`#299 <https://github.com/zscaler/zscaler-sdk-python/pull/299>`_) - Added the following new ZIA API Endpoints:
    - Added `DELETE /alertSubscriptions/{subscription_id}` Deletes the Alert Subscription based on the specified ID

Documentation
^^^^^^^^^^^^^^

* (`#299 <https://github.com/zscaler/zscaler-sdk-python/pull/299>`_) - Fixed and added several documentations and included examples.

1.4.3 (June, 3 2025)
-------------------------

Notes
-----

- Python Versions: **v3.8, v3.9, v3.10, v3.11**

Enhancements
-------------

* (`#296 <https://github.com/zscaler/zscaler-sdk-python/pull/296>`_) - Added the following new functions in the ZPA `policies` package: `add_browser_protection_rule_v2` and `update_browser_protection_rule_v2` to support `CLIENTLESS_SESSION_PROTECTION_POLICY` policy type for Browser Protection Rule configuration.
* (`#296 <https://github.com/zscaler/zscaler-sdk-python/pull/296>`_) - Added the following new `object_type` `USER_PORTAL` in the ZPA conditions template `_create_conditions_v2` to support `CLIENTLESS_SESSION_PROTECTION_POLICY` policy type for Browser Protection Rule configuration.
* (`#296 <https://github.com/zscaler/zscaler-sdk-python/pull/296>`_) - Fixed `update_segment()` behavior in all ZPA Application Segment client to ensure that port fields (`tcpPortRange`, `udpPortRange`, `tcpPortRanges`, `udpPortRanges`) are properly cleared when omitted. Previously, omitting these fields during update would leave existing port configurations intact instead of removing them.

1.4.2 (May, 29 2025)
-------------------------

Notes
-----

- Python Versions: **v3.8, v3.9, v3.10, v3.11**

Bug Fixes
-----------

* (`#294 <https://github.com/zscaler/zscaler-sdk-python/pull/294>`_) - Fixed ZIA `cloud_firewall_rules` model `nw_services` attribute
* (`#294 <https://github.com/zscaler/zscaler-sdk-python/pull/294>`_) - Fixed ZPA `cbi_certficate` pem model attribute
* (`#294 <https://github.com/zscaler/zscaler-sdk-python/pull/294>`_) - Fixed an issue where SDK logging configuration interfered with user-defined loggers. The SDK no longer overrides global logging behavior or disables logs for external modules.

1.4.1 (May, 27 2025)
-------------------------

Notes
-----

- Python Versions: **v3.8, v3.9, v3.10, v3.11**

Bug Fixes
-----------

* (`#292 <https://github.com/zscaler/zscaler-sdk-python/pull/292>`_) - Fixed ZPA `application_segment` model missing attribute `passive_health_enabled`
* (`#292 <https://github.com/zscaler/zscaler-sdk-python/pull/292>`_) - Added missing ZIA attribute `nw_services` to `reformat_params` list

1.4.0 (May, 22 2025)
-------------------------

Notes
-----

- Python Versions: **v3.8, v3.9, v3.10, v3.11**

Zscaler OneAPI Support for Cloud & Branch Connector API
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* (`#287 <https://github.com/zscaler/zscaler-sdk-python/pull/287>`_): Cloud & Branch Connector API are now supported via (`OneAPI <https://help.zscaler.com/zidentity/what-zidentity>`_) Oauth2 authentication support through (`Zidentity <https://help.zscaler.com/zidentity/what-zidentity>`_)

ZPA Application Segment Provision
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* (`#287 <https://github.com/zscaler/zscaler-sdk-python/pull/287>`_) - Added the following new ZPA API Endpoints:
    - Added `POST /provision` Provision a new application for a given customer by creating all related objects if necessary

ZPA Application Segment Weighted Load Balancer
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* (`#287 <https://github.com/zscaler/zscaler-sdk-python/pull/287>`_) - Added the following new ZPA API Endpoints:
    - Added `GET /weightedLbConfig` Get Weighted Load Balancer Config for AppSegment
    - Added `PUT /weightedLbConfig` Update Weighted Load Balancer Config for AppSegment

ZPA Policy-Set-Controller Condition - New Object Type
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* (`#287 <https://github.com/zscaler/zscaler-sdk-python/pull/287>`_) - Added the following new `object_types` to function `_create_conditions_v2` in the `policies` package: `CHROME_ENTERPRISE` and `CHROME_POSTURE_PROFILE`

Zscaler Client Connector (Legacy) New Rate Limiting Headers
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* (`#287 <https://github.com/zscaler/zscaler-sdk-python/pull/287>`_) - Enhanced `LegacyZCCClientHelper` rate limiting logic with new headers for more accurate retry-calculations.
  - `X-Rate-Limit-Retry-After-Seconds` - This header is only returned when rate limit for `/downloadDevices` and `downloadServiceStatus` is reached. 
  - The endpoint handler `/downloadDevices` and `downloadServiceStatus` has a rate limit of 3 calls per day.
  - `X-Rate-Limit-Remaining` - This header is returned for all other endpoints. ZCC endpoints called from a specific IP address are subjected to a rate limit of 100 calls per hour. See (`Zscaler Client Connector API <https://help.zscaler.com/oneapi/understanding-rate-limiting>`_)

Bug Fixes:
---------------

* (`#287 <https://github.com/zscaler/zscaler-sdk-python/pull/287>`_) - Fixed ZCC functions `remove_devices` and `force_remove_devices` to use custom decorator `zcc_param_mapper` for `os_type` attribute
* (`#287 <https://github.com/zscaler/zscaler-sdk-python/pull/287>`_) - Removed incorrect validation from ZIA `url_categories` function `add_url_category` - [Issue #284](https://github.com/zscaler/zscaler-sdk-python/issues/284)
* (`#287 <https://github.com/zscaler/zscaler-sdk-python/pull/287>`_) - Fixed ZPA `application_segment_pra` model attribute  `common_apps_dto`.
* (`#287 <https://github.com/zscaler/zscaler-sdk-python/pull/287>`_) - Fixed ZPA resources `add_privileged_credential_rule_v2`, and `update_privileged_credential_rule_v2` 
* (`#287 <https://github.com/zscaler/zscaler-sdk-python/pull/287>`_) - Fixed ZPA Application segment v2 Port formatting issue: [Issue #288](https://github.com/zscaler/zscaler-sdk-python/issues/288)
* (`#287 <https://github.com/zscaler/zscaler-sdk-python/pull/287>`_) - Added new ZPA attribute models to support `extranet` features across `server_groups` and `application_segments`
* (`#287 <https://github.com/zscaler/zscaler-sdk-python/pull/287>`_) - Added pre-check on all ZPA  `application_segment` resources to prevent port overlap configuration.
* (`#287 <https://github.com/zscaler/zscaler-sdk-python/pull/287>`_) - Added additional `CLIENT_TYPE` validation within the ZPA policy functions `add_redirection_rule_v2` and `update_redirection_rule_v2`
* (`#287 <https://github.com/zscaler/zscaler-sdk-python/pull/287>`_) - Enhanced `_create_conditions_v2` function used on ZPA Policy v2 condition block.

Internal Enhancements
-----------------------

* (`#287 <https://github.com/zscaler/zscaler-sdk-python/pull/287>`_) - Enhanced `check_response_for_error` function to parse and display API error messages more clearly.
* (`#287 <https://github.com/zscaler/zscaler-sdk-python/pull/287>`_) - Consolidated all application segment resource models into a single model shared across all Application Segment package resources.

1.3.0 (May, 12 2025)
-------------------------

Notes
-----

- Python Versions: **v3.8, v3.9, v3.10, v3.11**

ZPA Administrator Controller
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* (`#280 <https://github.com/zscaler/zscaler-sdk-python/pull/280>`_) - Added the following new ZPA API Endpoints:
    - Added `GET /administrators` Retrieves a list of administrators in a tenant. A maximum of 200 administrators are returned per request.
    - Added `GET /administrators/{admin_id}` Retrieves administrator details for a specific `{admin_id}`
    - Added `POST /administrators` Create an local administrator account
    - Added `PUT /administrators/{admin_id}` Update a local administrator account for a specific `{admin_id}`
    - Added `DELETE /administrators/{admin_id}` Delete a local administrator account for a specific `{admin_id}`

ZPA Role Controller
^^^^^^^^^^^^^^^^^^^^^^^^

* (`#280 <https://github.com/zscaler/zscaler-sdk-python/pull/280>`_) - Added the following new ZPA API Endpoints:
    - Added `GET /permissionGroups` Retrieves all the default permission groups.
    - Added `GET /roles` Retrieves a list of all configured roles in a tenant.
    - Added `GET /roles/{admin_id}` Retrieves a role details for a specific `{role_id}`
    - Added `POST /roles` Adds a new role for a tenant.
    - Added `PUT /roles/{admin_id}` Update a role for a specific `{role_id}`
    - Added `DELETE /roles/{role_id}` Delete a role for a specific `{role_id}`

ZPA Enrollment Certificate 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* (`#280 <https://github.com/zscaler/zscaler-sdk-python/pull/280>`_) - Added the following new ZPA API Endpoints:
    - Added `POST /enrollmentCert/csr/generate` Creates a CSR for a new enrollment Certificate
    - Added `POST /enrollmentCert/selfsigned/generate` Creates a self signed Enrollment Certificate
    - Added `POST /enrollmentCert` Creates a enrollment Certificate
    - Added `PUT /enrollmentCert/{cert_id}` Update an existing enrollment Certificate
    - Added `DELETE /enrollmentCert/{cert_id}` Delete an existing enrollment Certificate

ZPA SAML Attribute Controller
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* (`#280 <https://github.com/zscaler/zscaler-sdk-python/pull/280>`_) - Added the following new ZPA API Endpoints:
    - Added `POST /samlAttribute` Adds a new `SamlAttribute` for a given tenant
    - Added `PUT /samlAttribute/{attr_id}` Update an existing `SamlAttribute` for a given tenant
    - Added `DELETE /samlAttribute/{attr_id}` Delete an existing `SamlAttribute` for a given tenant

ZPA Client-Settings Controller
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* (`#280 <https://github.com/zscaler/zscaler-sdk-python/pull/280>`_) - Added the following new ZPA API Endpoints:
    - Added `GET /clientSetting` Retrieves `clientSetting` details. `ClientCertType` defaults to `CLIENT_CONNECTOR`
    - Added `POST /clientSetting` Create or update `clientSetting` for a customer. `ClientCertType` defaults to `CLIENT_CONNECTOR`
    - Added `DELETE /clientSetting` Delete an existing `clientSetting`. `ClientCertType` defaults to `CLIENT_CONNECTOR`
    - Added `GET /clientSetting/all` Retrieves all `clientSetting` details.

Bug Fixes
----------

* (`#280 <https://github.com/zscaler/zscaler-sdk-python/pull/280>`_) - Fixed `username` parameter in the ZCC `devices` model for the correct non-standard `snake_case` vs `cameCase` format.
* (`#280 <https://github.com/zscaler/zscaler-sdk-python/pull/280>`_) - Added missing `user_risk_score_levels` and `source_ip_groups` attributes to `dlp_web_rules`

1.2.4 (May, 9 2025)
-----------------------------

Notes
-----

- Python Versions: **v3.8, v3.9, v3.10, v3.11**

Bug Fixes
----------

* (`#277 <https://github.com/zscaler/zscaler-sdk-python/pull/277>`_) - Fixed documentation formatting.

1.2.3 (May, 9 2025)
-----------------------------

Notes
-----

- Python Versions: **v3.8, v3.9, v3.10, v3.11**

Bug Fixes
----------

* (`#276 <https://github.com/zscaler/zscaler-sdk-python/pull/276>`_) - Fixed ZCC `download_devices` method to support `octet-stream` header
* (`#276 <https://github.com/zscaler/zscaler-sdk-python/pull/276>`_) - Fixed ZCC `devices` model attributes and attribute edge cases.
* (`#276 <https://github.com/zscaler/zscaler-sdk-python/pull/276>`_) - Fixed missing link for resource `cloud_apps` in both `legacy` and `OneAPI` client
* (`#276 <https://github.com/zscaler/zscaler-sdk-python/pull/276>`_) - `cloud_apps` resource has been renamed to `shadow_it_report` for consistency.

1.2.2 (May, 7 2025)
-----------------------------

Notes
-----

- Python Versions: **v3.8, v3.9, v3.10, v3.11**

Bug Fix
--------

* (`#274 <https://github.com/zscaler/zscaler-sdk-python/pull/274>`_) - Fixed ZPA pagination across several resources.
* (`#274 <https://github.com/zscaler/zscaler-sdk-python/pull/274>`_) - Fixed ZCC pagination function resources
* (`#274 <https://github.com/zscaler/zscaler-sdk-python/pull/274>`_) - Fixed ZCC Device resource models
* (`#274 <https://github.com/zscaler/zscaler-sdk-python/pull/274>`_) - Fixed debug logging activation

1.2.1 (May, 6 2025)
-----------------------------

Notes
-----

- Python Versions: **v3.8, v3.9, v3.10, v3.11**

Bug Fix
--------

* (`#273 <https://github.com/zscaler/zscaler-sdk-python/pull/273>`_) - Fixed ZIA `bandwidth_classes` function names
* (`#273 <https://github.com/zscaler/zscaler-sdk-python/pull/273>`_) - Fixed ZIA `LegacyZIAClient` API client incorrect variable assignment.


1.2.0 (May, 5 2025)
-----------------------------

Notes
-----

- Python Versions: **v3.8, v3.9, v3.10, v3.11**

ZIA NAT Control Policy
^^^^^^^^^^^^^^^^^^^^^^^^

(`#270 <https://github.com/zscaler/zscaler-sdk-python/pull/270>`_) - Added the following new ZIA API Endpoints:
    - Added `GET /dnatRules` Retrieves a list of all configured and predefined DNAT Control policies.
    - Added `GET /dnatRules/{rule_id}` Retrieves the DNAT Control policy rule information based on the specified ID
    - Added `POST /dnatRules` Adds a new DNAT Control policy rule. 
    - Added `PUT /dnatRules/{rule_id}` Updates the DNAT Control policy rule information based on the specified ID
    - Added `DELETE /dnatRules/{rule_id}` Deletes the DNAT Control policy rule information based on the specified ID

ZIA NSS Servers
^^^^^^^^^^^^^^^^^^

(`#270 <https://github.com/zscaler/zscaler-sdk-python/pull/270>`_) - Added the following new ZIA API Endpoints:
    - Added `GET /nssServers` Retrieves a list of registered NSS servers.
    - Added `GET /nssServers/{nss_id}` Retrieves the registered NSS server based on the specified ID
    - Added `POST /nssServers` Adds a new NSS server.
    - Added `PUT /nssServers/{nss_id}` Updates an NSS server based on the specified ID
    - Added `DELETE /nssServers/{nss_id}` Deletes an NSS server based on the specified ID

Enhancements
^^^^^^^^^^^^^^
(`#270 <https://github.com/zscaler/zscaler-sdk-python/pull/270>`_) - Enhanced exceptions handling for clarity during configuration or API errors.
(`#270 <https://github.com/zscaler/zscaler-sdk-python/pull/270>`_) - Enhanced retry mechanism to include `408`, `409` status codes.
(`#270 <https://github.com/zscaler/zscaler-sdk-python/pull/270>`_) - Improved SDK logging behavior to prevent interference with user-defined loggers. Added example for custom logging setup.

1.1.0 (April, 28 2025)
-----------------------------

Notes
-----

- Python Versions: **v3.8, v3.9, v3.10, v3.11**

ZIA Password Expiry Settings
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#267 <https://github.com/zscaler/zscaler-sdk-python/pull/267>`_) - Added the following new ZIA API Endpoints:
    - Added `GET /passwordExpiry/settings` Retrieves the password expiration information for all the admins
    - Added `PUT /passwordExpiry/settings` Updates the password expiration information for all the admins.

ZIA Alerts
^^^^^^^^^^^^

(`#267 <https://github.com/zscaler/zscaler-sdk-python/pull/267>`_) - Added the following new ZIA API Endpoints:
    - Added `GET /alertSubscriptions` Retrieves a list of all alert subscriptions
    - Added `GET /alertSubscriptions/{subscription_id}` Retrieves the alert subscription information based on the specified ID
    - Added `POST /alertSubscriptions` Adds a new alert subscription.
    - Added `PUT /alertSubscriptions/{subscription_id}` Updates an existing alert subscription based on the specified ID

ZIA Bandwidth Classes
^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#267 <https://github.com/zscaler/zscaler-sdk-python/pull/267>`_) - Added the following new ZIA API Endpoints:
    - Added `GET /bandwidthClasses` Retrieves a list of bandwidth classes for an organization.
    - Added `GET /bandwidthClasses/lite` Retrieves a list of bandwidth classes for an organization
    - Added `GET /bandwidthClasses/{class_id}` Retrieves the alert subscription information based on the specified ID
    - Added `POST /bandwidthClasses` Adds a new bandwidth class.
    - Added `PUT /bandwidthClasses/{class_id}` Updates a bandwidth class based on the specified ID
    - Added `DELETE /bandwidthClasses/{class_id}` Deletes a bandwidth class based on the specified ID

ZIA Bandwidth Control Rules
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#267 <https://github.com/zscaler/zscaler-sdk-python/pull/267>`_) - Added the following new ZIA API Endpoints:
    - Added `GET /bandwidthControlRules` Retrieves all the rules in the Bandwidth Control policy.
    - Added `GET /bandwidthControlRules/lite` Retrieves all the rules in the Bandwidth Control policy
    - Added `GET /bandwidthControlRules/{rule_id}` Retrieves the Bandwidth Control policy rule based on the specified ID
    - Added `POST /bandwidthControlRules` Adds a new Bandwidth Control policy rule.
    - Added `PUT /bandwidthControlRules/{rule_id}` Updates the Bandwidth Control policy rule based on the specified ID
    - Added `DELETE /bandwidthControlRules/{rule_id}` Deletes a Bandwidth Control policy rule based on the specified ID

ZIA Risk Profiles
^^^^^^^^^^^^^^^^^^^^^^^

(`#267 <https://github.com/zscaler/zscaler-sdk-python/pull/267>`_) - Added the following new ZIA API Endpoints:
    - Added `GET /riskProfiles` Retrieves the cloud application risk profile.
    - Added `GET /riskProfiles/lite` Retrieves the cloud application risk profile
    - Added `GET /riskProfiles/{profile_id}` Retrieves the cloud application risk profile based on the specified ID
    - Added `POST /riskProfiles` Adds a new cloud application risk profile. 
    - Added `PUT /riskProfiles/{profile_id}` Updates the cloud application risk profile based on the specified ID
    - Added `DELETE /riskProfiles/{profile_id}` Deletes the cloud application risk profile based on the specified ID

ZIA Cloud Application Instances
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#267 <https://github.com/zscaler/zscaler-sdk-python/pull/267>`_) - Added the following new ZIA API Endpoints:
    - Added `GET /cloudApplicationInstances` Retrieves the list of cloud application instances configured in the ZIA Admin Portal.
    - Added `GET /cloudApplicationInstances/{instance_id}` Retrieves information about a cloud application instance based on the specified ID
    - Added `POST /cloudApplicationInstances` Add a new cloud application instance. 
    - Added `PUT /cloudApplicationInstances/{instance_id}` Updates information about a cloud application instance based on the specified ID
    - Added `DELETE /cloudApplicationInstances/{instance_id}` Deletes a cloud application instance based on the specified ID

ZIA Cloud Application Instances
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#267 <https://github.com/zscaler/zscaler-sdk-python/pull/267>`_) - Added the following new ZIA API Endpoints:
    - Added `GET /cloudApplicationInstances` Retrieves the list of cloud application instances configured in the ZIA Admin Portal
    - Added `GET /cloudApplicationInstances/{instance_id}` Retrieves information about a cloud application instance based on the specified ID
    - Added `POST /cloudApplicationInstances` Add a new cloud application instance
    - Added `PUT /cloudApplicationInstances/{instance_id}` Updates information about a cloud application instance based on the specified ID
    - Added `DELETE /cloudApplicationInstances/{instance_id}` Deletes a cloud application instance based on the specified ID

ZIA Tenancy Restriction Profile
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#267 <https://github.com/zscaler/zscaler-sdk-python/pull/267>`_) - Added the following new ZIA API Endpoints:
    - Added `GET /tenancyRestrictionProfile` Retrieves all the restricted tenant profiles
    - Added `GET /tenancyRestrictionProfile/{profile_id}` Retrieves the restricted tenant profile based on the specified ID
    - Added `POST /tenancyRestrictionProfile` Creates restricted tenant profiles
    - Added `PUT /tenancyRestrictionProfile/{profile_id}` Updates the restricted tenant profile based on the specified ID
    - Added `DELETE /tenancyRestrictionProfile/{profile_id}` Deletes the restricted tenant profile based on the specified ID
    - Added `GET /tenancyRestrictionProfile/app-item-count/{app_type}/{item_type}` Retrieves the item count of the specified item type for a given application, excluding any specified profile

ZIA DNS Gateway
^^^^^^^^^^^^^^^^^^^^^

(`#267 <https://github.com/zscaler/zscaler-sdk-python/pull/267>`_) - Added the following new ZIA API Endpoints:
    - Added `GET /dnsGateways` Retrieves a list of DNS Gateways
    - Added `GET /dnsGateways/lite` Retrieves a list of DNS Gateways
    - Added `GET /dnsGateways/{gateway_id}` Retrieves the DNS Gateway based on the specified ID
    - Added `POST /dnsGateways` Adds a new DNS Gateway
    - Added `PUT /dnsGateways/{gateway_id}` Updates the DNS Gateway based on the specified ID
    - Added `DELETE /dnsGateways/{gateway_id}` Deletes a DNS Gateway based on the specified ID

ZIA Proxies
^^^^^^^^^^^^^^^^^

(`#267 <https://github.com/zscaler/zscaler-sdk-python/pull/267>`_) - Added the following new ZIA API Endpoints:
    - Added `GET /proxies` Retrieves a list of all proxies configured for third-party proxy services.
    - Added `GET /proxies/lite` Retrieves a list of all proxies configured for third-party proxy services
    - Added `GET /proxies/{proxy_id}` Retrieves the proxy information based on the specified ID
    - Added `POST /proxies` Adds a new proxy for a third-party proxy service
    - Added `PUT /proxies/{proxy_id}` Updates an existing proxy based on the specified ID
    - Added `DELETE /proxies/{proxy_id}` Deletes an existing proxy based on the specified ID
    - Added `DELETE /dedicatedIPGateways/lite` Retrieves a list of dedicated IP gateways

ZIA FTP Settings
^^^^^^^^^^^^^^^^^^^^^^

(`#267 <https://github.com/zscaler/zscaler-sdk-python/pull/267>`_) - Added the following new ZIA API Endpoints:
    - Added `GET /ftpSettings` Retrieves the FTP Control status and the list of URL categories for which FTP is allowed.
    - Added `PUT /ftpSettings` Updates the FTP Control settings

ZIA Mobile Malware Protection Policy
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#267 <https://github.com/zscaler/zscaler-sdk-python/pull/267>`_) - Added the following new ZIA API Endpoints:
    - Added `GET /mobileAdvanceThreatSettings` Retrieves all the rules in the Mobile Malware Protection policy
    - Added `PUT /mobileAdvanceThreatSettings` Updates the Mobile Malware Protection rule information

ZIA Mobile Malware Protection Policy
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#267 <https://github.com/zscaler/zscaler-sdk-python/pull/267>`_) - Added the following new ZIA API Endpoints:
    - Added `GET /configAudit` Retrieves the System Audit Report.
    - Added `GET /configAudit/ipVisibility` Retrieves the IP visibility audit report
    - Added `GET /configAudit/pacFile` Retrieves the PAC file audit report

**Note**: This endpoint is accessible via Zscaler OneAPI only

ZIA Time Intervals
^^^^^^^^^^^^^^^^^^^^

(`#267 <https://github.com/zscaler/zscaler-sdk-python/pull/267>`_) - Added the following new ZIA API Endpoints:
    - Added `GET /timeIntervals` Retrieves the System Audit Report
    - Added `GET /timeIntervals/{interval_id}` Retrieves the configured time interval based on the specified ID
    - Added `POST /timeIntervals/{interval_id}` Adds a new time interval
    - Added `PUT /timeIntervals/{interval_id}` Updates the time interval based on the specified ID
    - Added `DELETE /timeIntervals/{interval_id}` Deletes a time interval based on the specified ID

ZIA Data Center Exclusions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#267 <https://github.com/zscaler/zscaler-sdk-python/pull/267>`_) - Added the following new ZIA API Endpoints:
    - Added `GET /dcExclusions` Retrieves the list of Zscaler data centers (DCs) that are currently excluded from service to your organization based on configured exclusions in the ZIA Admin Portal
    - Added `POST /dcExclusions/{dc_id}` Adds a data center (DC) exclusion to disable the tunnels terminating at a virtual IP address of a Zscaler DC
    - Added `PUT /dcExclusions/{dc_id}` Updates a Zscaler data center (DC) exclusion configuration based on the specified ID.
    - Added `DELETE /dcExclusions/{dc_id}` Deletes a Zscaler data center (DC) exclusion configuration based on the specified ID. 
    - Added `GET /datacenters` Retrieves the list of Zscaler data centers (DCs) that can be excluded from service to your organization

1.0.3 (April, 22 2025) - BREAKING CHANGES
-----------------------------------------

Notes
-----

- Python Versions: **v3.8, v3.9, v3.10, v3.11**


Zscaler OneAPI Support
-----------------------

(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_): Added support for (`OneAPI <https://help.zscaler.com/zidentity/what-zidentity>`_) Oauth2 authentication support through (`Zidentity <https://help.zscaler.com/zidentity/what-zidentity>`_)

**NOTES**
  - Starting at v1.0.0 version this SDK provides dual API client functionality and is backwards compatible with the legacy Zscaler API framework.
  - The new OneAPI framework is compatible only with the following products `ZCC/ZIA/ZPA`.
  - The following products `ZTW` - Cloud Connector and `ZDX` and Zscaler Digital Experience, authentication methods remain unnaffected.
  - The package `ZCON` (Zscaler Cloud and Branch Connector) has been renamed to `ZTW`
  - The following products `ZWA` - Zscaler Workflow Automation authentication methods remain unnaffected.

Refer to the (`README <hhttps://github.com/zscaler/zscaler-sdk-python/blob/master/README.md>`_) page for details on client instantiation, and authentication requirements on each individual product.

**WARNING**: Attention Government customers. OneAPI and Zidentity is not currently supported for the following ZIA clouds: `zscalergov` and `zscalerten` or ZPA `GOV`, and `GOVUS`. 
See the Zscaler Legacy API Framework section in the (`README Docs <https://zscaler-sdk-python.readthedocs.io/en/latest/index.html>`_) for more information on how authenticate to these environments using the built-in Legacy API method.

(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_): All API clients now support Config Setter object `ZCC/ZTW/ZDX/ZIA/ZPA/ZWA`

ZCC New Endpoints
^^^^^^^^^^^^^^^^^

(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Added the following new ZCC API Endpoints:
  - Added `GET /downloadServiceStatus` to download service status for all devices.
  - Added `GET /getDeviceCleanupInfo` to retrieve device cleanup information.
  - Added `PUT /setDeviceCleanupInfo` to cleanup device information.
  - Added `GET /getDeviceDetails` to retrieve device detailed information.
  - Added `GET /getAdminUsers` to retrieve mobile portal admin user.
  - Added `PUT /editAdminUser` to update mobile portal admin user.
  - Added `GET /getAdminUsersSyncInfo` to retrieve mobile portal admin user sync information.
  - Added `POST /syncZiaZdxAdminUsers` to retrieve mobile portal admin users ZIA and ZDX sync information.
  - Added `POST /syncZpaAdminUsers` to retrieve mobile portal admin users ZPA sync information.
  - Added `GET /getAdminRoles` to retrieve mobile portal admin roles.
  - Added `GET /getCompanyInfo` to retrieve company information.
  - Added `GET /getZdxGroupEntitlements` to retrieve ZDX Group entitlement enablement.
  - Added `PUT /updateZdxGroupEntitlement` to retrieve ZDX Group entitlement enablement.
  - Added `GET /updateZpaGroupEntitlement` to retrieve ZPA Group entitlement enablement.
  - Added `GET /web/policy/listByCompany` to retrieve Web Policy By Company ID.
  - Added `PUT /web/policy/activate` to activate mobile portal web policy
  - Added `PUT /web/policy/edit` to update mobile portal web policy
  - Added `DELETE /web/policy/{policyId}/delete` to delete mobile portal web policy.
  - Added `GET /webAppService/listByCompany` to retrieve Web App Service information By Company ID.
  - Added `GET /webFailOpenPolicy/listByCompany` to retrieve web Fail Open Policy information By Company ID.
  - Added `PUT /webFailOpenPolicy/edit` to update mobile portal web Fail Open Policy.
  - Added `GET /webForwardingProfile/listByCompany` to retrieve Web Forwarding Profile information By Company ID.
  - Added `POST /webForwardingProfile/edit` to create a Web Forwarding Profile.
  - Added `DELETE /webForwardingProfile/{profileId}/delete` to delete Web Forwarding Profile.
  - Added `GET /webTrustedNetwork/listByCompany` to retrieve multiple Web Trusted Network information By Company ID.
  - Added `POST /webTrustedNetwork/edit` to create Web Trusted Network resource.
  - Added `PUT /webTrustedNetwork/edit` to update Web Trusted Network resource.
  - Added `DELETE /webTrustedNetwork/{networkId}/delete` to delete Web Trusted Network resource.
  - Added `GET /getWebPrivacyInfo` to retrieve Web Privacy Info.
  - Added `GET /setWebPrivacyInfo` to update Web Privacy Info.

ZIA Sandbox Submission - BREAKING CHANGES
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Authentication to Zscaler Sandbox now use the following attributes during client instantiation.
 - `sandboxToken` - Can also be sourced from the `ZSCALER_SANDBOX_TOKEN` environment variable.
 - `sandboxCloud` - Can also be sourced from the `ZSCALER_SANDBOX_CLOUD` environment variable.

**NOTE** The previous `ZIA_SANDBOX_TOKEN` has been deprecated.

ZIA Sandbox Rules
^^^^^^^^^^^^^^^^^^

(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /sandboxRules` to retrieve the list of all Sandbox policy rules.
  - Added `GET /sandboxRules/{ruleId}` to retrieve the Sandbox policy rule information based on the specified ID.
  - Added `POST /sandboxRules` to add a Sandbox policy rule.
  - Added `PUT /sandboxRules/{ruleId}` to update the Sandbox policy rule configuration for the specified ID.
  - Added `DELETE /sandboxRules/{ruleId}` to delete the Sandbox policy rule based on the specified ID.

ZIA DNS Control Rules
^^^^^^^^^^^^^^^^^^^^^^

(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /firewallDnsRules` to retrieve the list of all DNS Control policy rules.
  - Added `GET /firewallDnsRules/{ruleId}` to retrieve the DNS Control policy rule information based on the specified ID.
  - Added `POST /firewallDnsRules` to add a DNS Control policy rules.
  - Added `PUT /firewallDnsRules/{ruleId}` to update the DNS Control policy rule configuration for the specified ID.
  - Added `DELETE /firewallDnsRules/{ruleId}` to delete the DNS Control policy rule based on the specified ID.

ZIA IPS Control Rules
^^^^^^^^^^^^^^^^^^^^^

(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /firewallIpsRules` to retrieve the list of all IPS Control policy rules.
  - Added `GET /firewallIpsRules/{ruleId}` to retrieve the IPS Control policy rule information based on the specified ID.
  - Added `POST /firewallIpsRules` to add a IPS Control policy rule.
  - Added `PUT /firewallIpsRules/{ruleId}` to update the IPS Control policy rule configuration for the specified ID.
  - Added `DELETE /firewallIpsRules/{ruleId}` to delete the IPS Control policy rule based on the specified ID.

ZIA File Type Control Policy
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /fileTypeRules` to retrieve the list of all File Type Control policy rules.
  - Added `GET /fileTypeRules/lite` to retrieve the list of all File Type Control policy rules.
  - Added `GET /fileTypeRules/{ruleId}` to retrieve the File Type Control policy rule information based on the specified ID.
  - Added `POST /fileTypeRules` to add a File Type Control policy rule.
  - Added `PUT /fileTypeRules/{ruleId}` to update the File Type Control policy rule configuration for the specified ID.
  - Added `DELETE /fileTypeRules/{ruleId}` to delete the File Type Control policy rule based on the specified ID.

ZIA Forwarding Control Policy - Proxy Gateways
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /proxyGateways` to retrieve the proxy gateway information.
  - Added `GET /proxyGateways/lite` to retrieve the name and ID of the proxy.

ZIA Cloud Nanolog Streaming Service (NSS)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /nssFeeds` to retrieve the cloud NSS feeds.
  - Added `GET /nssFeeds/{feedId}` to retrieve information about cloud NSS feed based on the specified ID.
  - Added `POST /nssFeeds` to add a new cloud NSS feed.
  - Added `PUT /nssFeeds/{feedId}` to update cloud NSS feed configuration based on the specified ID.
  - Added `DELETE /nssFeeds/{feedId}` to delete cloud NSS feed configuration based on the specified ID.
  - Added `GET /nssFeeds/feedOutputDefaults` to retrieve the default cloud NSS feed output format for different log types.
  - Added `GET /nssFeeds/testConnectivity/{feedId}` to test the connectivity of cloud NSS feed based on the specified ID
  - Added `POST /nssFeeds/validateFeedFormat` to validates the cloud NSS feed format and returns the validation result

ZIA Advanced Threat Protection Policy
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /cyberThreatProtection/advancedThreatSettings` to retrieve the advanced threat configuration settings.
  - Added `PUT /cyberThreatProtection/advancedThreatSettings` to update the advanced threat configuration settings.
  - Added `GET /cyberThreatProtection/maliciousUrls` to retrieve the malicious URLs added to the denylist in the Advanced Threat Protection (ATP) policy
  - Added `PUT /cyberThreatProtection/maliciousUrls` to updates the malicious URLs added to the denylist in ATP policy
  - Added `GET /cyberThreatProtection/securityExceptions` to retrieves information about the security exceptions configured for the ATP policy
  - Added `PUT /cyberThreatProtection/securityExceptions` to update security exceptions for the ATP policy

ZIA Advanced Threat Protection Policy
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /cyberThreatProtection/atpMalwareInspection` to retrieve the traffic inspection configurations of Malware Protection policy
  - Added `PUT /cyberThreatProtection/atpMalwareInspection` to update the traffic inspection configurations of Malware Protection policy.
  - Added `GET /cyberThreatProtection/atpMalwareProtocols` to retrieve the protocol inspection configurations of Malware Protection policy
  - Added `PUT /cyberThreatProtection/atpMalwareProtocols` to update the protocol inspection configurations of Malware Protection policy.
  - Added `GET /cyberThreatProtection/malwareSettings` to retrieve the malware protection policy configuration details
  - Added `PUT /cyberThreatProtection/malwareSettings` to update the malware protection policy configuration details.
  - Added `GET /cyberThreatProtection/malwarePolicy` to retrieve information about the security exceptions configured for the Malware Protection policy
  - Added `PUT /cyberThreatProtection/malwarePolicy` to update security exceptions for the Malware Protection policy.

ZIA URL & Cloud App Control Policy Settings
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /advancedUrlFilterAndCloudAppSettings` to retrieve information about URL and Cloud App Control advanced policy settings
  - Added `PUT /advancedUrlFilterAndCloudAppSettings` to update the URL and Cloud App Control advanced policy settings

ZIA Authentication Settings
^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /authSettings` to retrieve the organization's default authentication settings information, including authentication profile and Kerberos authentication information.
  - Added `GET /authSettings/lite` to retrieve organization's default authentication settings information.
  - Added `PUT /authSettings` to update the organization's default authentication settings information.

ZIA Advanced Settings
^^^^^^^^^^^^^^^^^^^^^

(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /advancedSettings` to retrieve information about the advanced settings.
  - Added `PUT /advancedSettings` to update the advanced settings configuration.

ZIA Cloud Applications
^^^^^^^^^^^^^^^^^^^^^^^

(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /cloudApplications/policy` Retrieves a list of Predefined and User Defined Cloud Applications associated with the DLP rules, Cloud App Control rules, Advanced Settings, Bandwidth Classes, and File Type Control rules.
  - Added `GET /cloudApplications/sslPolicy` Retrieves a list of Predefined and User Defined Cloud Applications associated with the SSL Inspection rules.

ZIA Shadow IT Report
^^^^^^^^^^^^^^^^^^^^

(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Added the following new ZIA API Endpoints:
- Added `PUT /cloudApplications/bulkUpdate` To Update application status and tag information for predefined or custom cloud applications based on the IDs specified
- Added `GET /cloudApplications/lite` Gets the list of predefined and custom cloud applications
- Added `GET /customTags` Gets the list of custom tags available to assign to cloud applications
- Added `POST /shadowIT/applications/export` Export the Shadow IT Report (in CSV format) for the cloud applications recognized by Zscaler based on their usage in your organization.
- Added `POST /shadowIT/applications/{entity}/exportCsv` Export the Shadow IT Report (in CSV format) for the list of users or known locations identified with using the cloud applications specified in the request.

ZIA Remote Assistance Support
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /remoteAssistance` to retrieve information about the Remote Assistance option.
  - Added `PUT /remoteAssistance` to update information about the Remote Assistance option. Using this option, you can allow Zscaler Support to access your organization’s ZIA Admin Portal for a specified time period to troubleshoot issues.

ZIA Organization Details
^^^^^^^^^^^^^^^^^^^^^^^^^

(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /orgInformation` to retrieve detailed organization information, including headquarter location, geolocation, address, and contact details.
  - Added `GET /orgInformation/lite` to retrieve minimal organization information.
  - Added `GET /subscriptions` to retrieve information about the list of subscriptions enabled for your tenant. Subscriptions define the various features and levels of functionality that are available to your organization.

ZIA End User Notification
^^^^^^^^^^^^^^^^^^^^^^^^^^
(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /eun` to retrieve information browser-based end user notification (EUN) configuration details.
  - Added `PUT /eun` to update the browser-based end user notification (EUN) configuration details.

ZIA Admin Audit Logs
^^^^^^^^^^^^^^^^^^^^^^^

(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /auditlogEntryReport` to retrieve the status of a request for an audit log report.
  - Added `POST /auditlogEntryReport` to create an audit log report for the specified time period and saves it as a CSV file.
  - Added `DELETE /auditlogEntryReport` to cancel the request to create an audit log report.
  - Added `GET /auditlogEntryReport/download` to download the most recently created audit log report.

ZIA Extranets
^^^^^^^^^^^^^^^^^^

(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /extranet` to retrieve the list of extranets configured for the organization
  - Added `GET /extranet/lite` Retrieves the name-ID pairs of all extranets configured for an organization
  - Added `GET /extranet/{Id}` Retrieves information about an extranet based on the specified ID.
  - Added `POST /extranet` Adds a new extranet for the organization.
  - Added `PUT /extranet/{Id}` Updates an extranet based on the specified ID
  - Added `DELETE /extranet/{Id}` Deletes an extranet based on the specified ID

ZIA IOT Endpoint
^^^^^^^^^^^^^^^^^^

(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Added the following new ZIA IOT API Endpoints:
  - Added `GET /iotDiscovery/deviceTypes` Retrieve the mapping between device type universally unique identifier (UUID) values and the device type names for all the device types supported by the Zscaler AI/ML.
  - Added `GET /iotDiscovery/categories` Retrieve the mapping between the device category universally unique identifier (UUID) values and the category names for all the device categories supported by the Zscaler AI/ML. The parent of device category is device type.
  - Added `GET /iotDiscovery/classifications` Retrieve the mapping between the device classification universally unique identifier (UUID) values and the classification names for all the device classifications supported by Zscaler AI/ML. The parent of device classification is device category.
  - Added `GET /iotDiscovery/deviceList` Retrieve a list of discovered devices with the following key contexts, IP address, location, ML auto-label, classification, category, and type.

ZIA 3rd-Party App Governance
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /apps/app` to search the 3rd-Party App Governance App Catalog by either app ID or URL.
  - Added `POST /apps/app` to submis an app for analysis in the 3rd-Party App Governance Sandbox.
  - Added `GET /apps/search` to search for an app by name. Any app whose name contains the search term (appName) is returned.
  - Added `GET /app_views/list` to retrieve the list of custom views that you have configured in the 3rd-Party App Governance.
  - Added `GET /app_views/{appViewId}/apps` to retrieves all assets (i.e., apps) that are related to a specified argument (i.e., custom view).

ZIA Admin Role Endpoints
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Added the following new ZIA API Endpoints:
    - Added `GET /adminRoles/{roleId}` Retrieves the admin role based on the specified ID
    - Added `GET /adminRoles/lite` Retrieves a name and ID dictionary of all admin roles. The list only includes the name and ID for all admin roles.
    - Added `POST /adminRoles` Adds an admin role.
    - Added `PUT /adminRoles/{roleId}` Updates the admin role based on the specified ID.
    - Added `DELETE /adminRoles/{roleId}` Deletes the admin role based on the specified ID.

ZPA Credential Pool (New)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Added new ZPA endpoint:
  - Added `GET /credential-pool` Gets the privileged credential pool details for the specified customer.
  - Added `GET /credential-pool/{id}` Gets the privileged credential pool details for the specified customer.
  - Added `GET /credential-pool/{id}/credential` Given Privileged credential pool id gets mapped privileged credential info
  - Added `POST /credential-pool` Adds a new privileged credential pool for the specified customer.
  - Added `PUT /credential-pool/{id}` Updates the existing credential pool for the specified customer.
  - Added `DELETE /credential-pool/{id}` Updates the existing credential pool for the specified customer.

ZWA - Zscaler Workflow Automation (NEW)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Added new ZWA endpoint:
  - Added `GET /dlp/v1/incidents/transactions/{transactionId}` Gets the list of all DLP incidents associated with the transaction ID
  - Added `GET /dlp/v1/incidents/{dlpIncidentId}` Gets the DLP incident details based on the incident ID.
  - Added `DELETE /dlp/v1/incidents/{dlpIncidentId}` Deletes the DLP incident for the specified incident ID.
  - Added `GET /dlp/v1/incidents{dlpIncidentId}/change-history` Gets the details of updates made to an incident based on the given ID and timeline.
  - Added `GET /dlp/v1/incidents/{dlpIncidentId}/tickets` Gets the information of the ticket generated for the incident. For example, ticket type, ticket ID, ticket status, etc.
  - Added `POST /dlp/v1/incidents/{dlpIncidentId}/incident-groups/search` Filters a list of DLP incident groups to which the specified incident ID belongs.
  - Added `POST /dlp/v1/incidents/{dlpIncidentId}/close` Updates the status of the incident to resolved and closes the incident with a resolution label and a resolution code.
  - Added `POST /dlp/v1/incidents/{dlpIncidentId}/notes` Adds notes to the incident during updates or status changes.
  - Added `POST /dlp/v1/incidents/{dlpIncidentId}/labels` Assign lables (a label name and it's associated value) to DLP incidents.
  - Added `POST /dlp/v1/incidents/search` Filters DLP incidents based on the given time range and the field values.
  - Added `GET /dlp/v1/incidents/{dlpIncidentId}/triggers` Downloads the actual data that triggered the incident.
  - Added `GET /dlp/v1/incidents/{dlpIncidentId}/evidence` Gets the evidence URL of the incident.

Cloud & Branch Connector - OneAPI Support
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Cloud & Branch Connector package is now compatible with OneAPI and Legacy API framework. Please refer to README for details.
(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Cloud & Branch Connector package has been renamed from `zcon` to `ztw`

ZTW Policy Management
^^^^^^^^^^^^^^^^^^^^^^^

(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Added the following new ZTW API Endpoints:
    - Added `GET /ecRules/ecRdr` Retrieves the list of traffic forwarding rules.
    - Added `PUT /ecRules/ecRdr/{ruleId}` Updates a traffic forwarding rule configuration based on the specified ID.
    - Added `POST /ecRules/ecRdr` Creates a new traffic forwarding rule.
    - Added `GET /ecRules/ecRdr/count` Retrieves the count of traffic forwarding rules available in the Cloud & Branch Connector Admin Portal.

ZTW Policy Resources
^^^^^^^^^^^^^^^^^^^^^

(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Added the following new ZTW API Endpoints:
    - Added `GET /ipSourceGroups` Retrieves the list of source IP groups.
    - Added `GET /ipSourceGroups/lite` Retrieves the list of source IP groups. This request retrieves basic information about the source IP groups, such as name and ID. For extensive details, use the GET /ipSourceGroups request.
    - Added `POST /ipSourceGroups` Adds a new custom source IP group.
    - Added `DELETE /ipSourceGroups/{ipGroupId}` Deletes a source IP group based on the specified ID.
    - Added `GET /ipDestinationGroups` Retrieves the list of destination IP groups.
    - Added `GET /ipDestinationGroups/lite` Retrieves the list of destination IP groups. This request retrieves basic information about the destination IP groups, ID, name, and type. For extensive details, use the GET /ipDestinationGroups request.
    - Added `POST /ipDestinationGroups` Adds a new custom destination IP group.
    - Added `DELETE /ipDestinationGroups/{ipGroupId}` Deletes the destination IP group based on the specified ID. Default destination groups that are automatically created cannot be deleted.
    - Added `GET /ipGroups` Retrieves the list of IP pools.
    - Added `GET /ipGroups/lite` Retrieves the list of IP pools. This request retrieves basic information about the IP pools, such as name and ID. For extensive details, use the GET /ipGroups request.
    - Added `POST /ipGroups` Adds a new custom IP pool.
    - Added `DELETE /ipGroups/{ipGroupId}` Deletes an IP pool based on the specified ID.
    - Added `GET /networkServices` Retrieves the list of all network services. The search parameters find matching values within the name or description attributes.
    - Added `POST /networkServices` Creates a new network service.
    - Added `PUT /networkServices/{serviceId}` Updates the network service information for the specified service ID.
    - Added `DELETE /networkServices/{serviceId}` Deletes the network service for the specified ID.
    - Added `GET /networkServicesGroups` Retrieves the list of network service groups.
    - Added `GET /zpaResources/applicationSegments` Retrieves the list of ZPA application segments that can be configured in traffic forwarding rule criteria.

1.0.1 (April, 22 2025) - BREAKING CHANGES
-----------------------------------------

Notes
-----

- Python Versions: **v3.8, v3.9, v3.10, v3.11**


Zscaler OneAPI Support
-----------------------

(`#261 <https://github.com/zscaler/zscaler-sdk-python/pull/261>`_): Added support for (`OneAPI <https://help.zscaler.com/zidentity/what-zidentity>`_) Oauth2 authentication support through (`Zidentity <https://help.zscaler.com/zidentity/what-zidentity>`_)

**NOTES**
  - Starting at v1.0.0 version this SDK provides dual API client functionality and is backwards compatible with the legacy Zscaler API framework.
  - The new OneAPI framework is compatible only with the following products `ZCC/ZIA/ZPA`.
  - The following products `ZTW` - Cloud Connector and `ZDX` and Zscaler Digital Experience, authentication methods remain unnaffected.
  - The package `ZCON` (Zscaler Cloud and Branch Connector) has been renamed to `ZTW`
  - The following products `ZWA` - Zscaler Workflow Automation authentication methods remain unnaffected.

Refer to the (`README <hhttps://github.com/zscaler/zscaler-sdk-python/blob/master/README.md>`_) page for details on client instantiation, and authentication requirements on each individual product.

**WARNING**: Attention Government customers. OneAPI and Zidentity is not currently supported for the following ZIA clouds: `zscalergov` and `zscalerten` or ZPA `GOV`, and `GOVUS`. 
See the Zscaler Legacy API Framework section in the (`README Docs <https://zscaler-sdk-python.readthedocs.io/en/latest/index.html>`_) for more information on how authenticate to these environments using the built-in Legacy API method.

(`#261 <https://github.com/zscaler/zscaler-sdk-python/pull/261>`_): All API clients now support Config Setter object `ZCC/ZTW/ZDX/ZIA/ZPA/ZWA`

ZCC New Endpoints
^^^^^^^^^^^^^^^^^

(`#261 <https://github.com/zscaler/zscaler-sdk-python/pull/261>`_) - Added the following new ZCC API Endpoints:
  - Added `GET /downloadServiceStatus` to download service status for all devices.
  - Added `GET /getDeviceCleanupInfo` to retrieve device cleanup information.
  - Added `PUT /setDeviceCleanupInfo` to cleanup device information.
  - Added `GET /getDeviceDetails` to retrieve device detailed information.
  - Added `GET /getAdminUsers` to retrieve mobile portal admin user.
  - Added `PUT /editAdminUser` to update mobile portal admin user.
  - Added `GET /getAdminUsersSyncInfo` to retrieve mobile portal admin user sync information.
  - Added `POST /syncZiaZdxAdminUsers` to retrieve mobile portal admin users ZIA and ZDX sync information.
  - Added `POST /syncZpaAdminUsers` to retrieve mobile portal admin users ZPA sync information.
  - Added `GET /getAdminRoles` to retrieve mobile portal admin roles.
  - Added `GET /getCompanyInfo` to retrieve company information.
  - Added `GET /getZdxGroupEntitlements` to retrieve ZDX Group entitlement enablement.
  - Added `PUT /updateZdxGroupEntitlement` to retrieve ZDX Group entitlement enablement.
  - Added `GET /updateZpaGroupEntitlement` to retrieve ZPA Group entitlement enablement.
  - Added `GET /web/policy/listByCompany` to retrieve Web Policy By Company ID.
  - Added `PUT /web/policy/activate` to activate mobile portal web policy
  - Added `PUT /web/policy/edit` to update mobile portal web policy
  - Added `DELETE /web/policy/{policyId}/delete` to delete mobile portal web policy.
  - Added `GET /webAppService/listByCompany` to retrieve Web App Service information By Company ID.
  - Added `GET /webFailOpenPolicy/listByCompany` to retrieve web Fail Open Policy information By Company ID.
  - Added `PUT /webFailOpenPolicy/edit` to update mobile portal web Fail Open Policy.
  - Added `GET /webForwardingProfile/listByCompany` to retrieve Web Forwarding Profile information By Company ID.
  - Added `POST /webForwardingProfile/edit` to create a Web Forwarding Profile.
  - Added `DELETE /webForwardingProfile/{profileId}/delete` to delete Web Forwarding Profile.
  - Added `GET /webTrustedNetwork/listByCompany` to retrieve multiple Web Trusted Network information By Company ID.
  - Added `POST /webTrustedNetwork/edit` to create Web Trusted Network resource.
  - Added `PUT /webTrustedNetwork/edit` to update Web Trusted Network resource.
  - Added `DELETE /webTrustedNetwork/{networkId}/delete` to delete Web Trusted Network resource.
  - Added `GET /getWebPrivacyInfo` to retrieve Web Privacy Info.
  - Added `GET /setWebPrivacyInfo` to update Web Privacy Info.

ZIA Sandbox Submission - BREAKING CHANGES
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#261 <https://github.com/zscaler/zscaler-sdk-python/pull/261>`_) - Authentication to Zscaler Sandbox now use the following attributes during client instantiation.
 - `sandboxToken` - Can also be sourced from the `ZSCALER_SANDBOX_TOKEN` environment variable.
 - `sandboxCloud` - Can also be sourced from the `ZSCALER_SANDBOX_CLOUD` environment variable.

**NOTE** The previous `ZIA_SANDBOX_TOKEN` has been deprecated.

ZIA Sandbox Rules
^^^^^^^^^^^^^^^^^^

(`#261 <https://github.com/zscaler/zscaler-sdk-python/pull/261>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /sandboxRules` to retrieve the list of all Sandbox policy rules.
  - Added `GET /sandboxRules/{ruleId}` to retrieve the Sandbox policy rule information based on the specified ID.
  - Added `POST /sandboxRules` to add a Sandbox policy rule.
  - Added `PUT /sandboxRules/{ruleId}` to update the Sandbox policy rule configuration for the specified ID.
  - Added `DELETE /sandboxRules/{ruleId}` to delete the Sandbox policy rule based on the specified ID.

ZIA DNS Control Rules
^^^^^^^^^^^^^^^^^^^^^^

(`#261 <https://github.com/zscaler/zscaler-sdk-python/pull/261>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /firewallDnsRules` to retrieve the list of all DNS Control policy rules.
  - Added `GET /firewallDnsRules/{ruleId}` to retrieve the DNS Control policy rule information based on the specified ID.
  - Added `POST /firewallDnsRules` to add a DNS Control policy rules.
  - Added `PUT /firewallDnsRules/{ruleId}` to update the DNS Control policy rule configuration for the specified ID.
  - Added `DELETE /firewallDnsRules/{ruleId}` to delete the DNS Control policy rule based on the specified ID.

ZIA IPS Control Rules
^^^^^^^^^^^^^^^^^^^^^

(`#261 <https://github.com/zscaler/zscaler-sdk-python/pull/261>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /firewallIpsRules` to retrieve the list of all IPS Control policy rules.
  - Added `GET /firewallIpsRules/{ruleId}` to retrieve the IPS Control policy rule information based on the specified ID.
  - Added `POST /firewallIpsRules` to add a IPS Control policy rule.
  - Added `PUT /firewallIpsRules/{ruleId}` to update the IPS Control policy rule configuration for the specified ID.
  - Added `DELETE /firewallIpsRules/{ruleId}` to delete the IPS Control policy rule based on the specified ID.

ZIA File Type Control Policy
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#261 <https://github.com/zscaler/zscaler-sdk-python/pull/261>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /fileTypeRules` to retrieve the list of all File Type Control policy rules.
  - Added `GET /fileTypeRules/lite` to retrieve the list of all File Type Control policy rules.
  - Added `GET /fileTypeRules/{ruleId}` to retrieve the File Type Control policy rule information based on the specified ID.
  - Added `POST /fileTypeRules` to add a File Type Control policy rule.
  - Added `PUT /fileTypeRules/{ruleId}` to update the File Type Control policy rule configuration for the specified ID.
  - Added `DELETE /fileTypeRules/{ruleId}` to delete the File Type Control policy rule based on the specified ID.

ZIA Forwarding Control Policy - Proxy Gateways
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#261 <https://github.com/zscaler/zscaler-sdk-python/pull/261>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /proxyGateways` to retrieve the proxy gateway information.
  - Added `GET /proxyGateways/lite` to retrieve the name and ID of the proxy.

ZIA Cloud Nanolog Streaming Service (NSS)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#261 <https://github.com/zscaler/zscaler-sdk-python/pull/261>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /nssFeeds` to retrieve the cloud NSS feeds.
  - Added `GET /nssFeeds/{feedId}` to retrieve information about cloud NSS feed based on the specified ID.
  - Added `POST /nssFeeds` to add a new cloud NSS feed.
  - Added `PUT /nssFeeds/{feedId}` to update cloud NSS feed configuration based on the specified ID.
  - Added `DELETE /nssFeeds/{feedId}` to delete cloud NSS feed configuration based on the specified ID.
  - Added `GET /nssFeeds/feedOutputDefaults` to retrieve the default cloud NSS feed output format for different log types.
  - Added `GET /nssFeeds/testConnectivity/{feedId}` to test the connectivity of cloud NSS feed based on the specified ID
  - Added `POST /nssFeeds/validateFeedFormat` to validates the cloud NSS feed format and returns the validation result

ZIA Advanced Threat Protection Policy
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#261 <https://github.com/zscaler/zscaler-sdk-python/pull/261>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /cyberThreatProtection/advancedThreatSettings` to retrieve the advanced threat configuration settings.
  - Added `PUT /cyberThreatProtection/advancedThreatSettings` to update the advanced threat configuration settings.
  - Added `GET /cyberThreatProtection/maliciousUrls` to retrieve the malicious URLs added to the denylist in the Advanced Threat Protection (ATP) policy
  - Added `PUT /cyberThreatProtection/maliciousUrls` to updates the malicious URLs added to the denylist in ATP policy
  - Added `GET /cyberThreatProtection/securityExceptions` to retrieves information about the security exceptions configured for the ATP policy
  - Added `PUT /cyberThreatProtection/securityExceptions` to update security exceptions for the ATP policy

ZIA Advanced Threat Protection Policy
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#261 <https://github.com/zscaler/zscaler-sdk-python/pull/261>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /cyberThreatProtection/atpMalwareInspection` to retrieve the traffic inspection configurations of Malware Protection policy
  - Added `PUT /cyberThreatProtection/atpMalwareInspection` to update the traffic inspection configurations of Malware Protection policy.
  - Added `GET /cyberThreatProtection/atpMalwareProtocols` to retrieve the protocol inspection configurations of Malware Protection policy
  - Added `PUT /cyberThreatProtection/atpMalwareProtocols` to update the protocol inspection configurations of Malware Protection policy.
  - Added `GET /cyberThreatProtection/malwareSettings` to retrieve the malware protection policy configuration details
  - Added `PUT /cyberThreatProtection/malwareSettings` to update the malware protection policy configuration details.
  - Added `GET /cyberThreatProtection/malwarePolicy` to retrieve information about the security exceptions configured for the Malware Protection policy
  - Added `PUT /cyberThreatProtection/malwarePolicy` to update security exceptions for the Malware Protection policy.

ZIA URL & Cloud App Control Policy Settings
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#261 <https://github.com/zscaler/zscaler-sdk-python/pull/261>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /advancedUrlFilterAndCloudAppSettings` to retrieve information about URL and Cloud App Control advanced policy settings
  - Added `PUT /advancedUrlFilterAndCloudAppSettings` to update the URL and Cloud App Control advanced policy settings

ZIA Authentication Settings
^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#261 <https://github.com/zscaler/zscaler-sdk-python/pull/261>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /authSettings` to retrieve the organization's default authentication settings information, including authentication profile and Kerberos authentication information.
  - Added `GET /authSettings/lite` to retrieve organization's default authentication settings information.
  - Added `PUT /authSettings` to update the organization's default authentication settings information.

ZIA Advanced Settings
^^^^^^^^^^^^^^^^^^^^^

(`#261 <https://github.com/zscaler/zscaler-sdk-python/pull/261>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /advancedSettings` to retrieve information about the advanced settings.
  - Added `PUT /advancedSettings` to update the advanced settings configuration.

ZIA Cloud Applications
^^^^^^^^^^^^^^^^^^^^^^^

(`#261 <https://github.com/zscaler/zscaler-sdk-python/pull/261>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /cloudApplications/policy` Retrieves a list of Predefined and User Defined Cloud Applications associated with the DLP rules, Cloud App Control rules, Advanced Settings, Bandwidth Classes, and File Type Control rules.
  - Added `GET /cloudApplications/sslPolicy` Retrieves a list of Predefined and User Defined Cloud Applications associated with the SSL Inspection rules.

ZIA Shadow IT Report
^^^^^^^^^^^^^^^^^^^^

(`#261 <https://github.com/zscaler/zscaler-sdk-python/pull/261>`_) - Added the following new ZIA API Endpoints:
- Added `PUT /cloudApplications/bulkUpdate` To Update application status and tag information for predefined or custom cloud applications based on the IDs specified
- Added `GET /cloudApplications/lite` Gets the list of predefined and custom cloud applications
- Added `GET /customTags` Gets the list of custom tags available to assign to cloud applications
- Added `POST /shadowIT/applications/export` Export the Shadow IT Report (in CSV format) for the cloud applications recognized by Zscaler based on their usage in your organization.
- Added `POST /shadowIT/applications/{entity}/exportCsv` Export the Shadow IT Report (in CSV format) for the list of users or known locations identified with using the cloud applications specified in the request.

ZIA Remote Assistance Support
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#261 <https://github.com/zscaler/zscaler-sdk-python/pull/261>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /remoteAssistance` to retrieve information about the Remote Assistance option.
  - Added `PUT /remoteAssistance` to update information about the Remote Assistance option. Using this option, you can allow Zscaler Support to access your organization’s ZIA Admin Portal for a specified time period to troubleshoot issues.

ZIA Organization Details
^^^^^^^^^^^^^^^^^^^^^^^^^

(`#261 <https://github.com/zscaler/zscaler-sdk-python/pull/261>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /orgInformation` to retrieve detailed organization information, including headquarter location, geolocation, address, and contact details.
  - Added `GET /orgInformation/lite` to retrieve minimal organization information.
  - Added `GET /subscriptions` to retrieve information about the list of subscriptions enabled for your tenant. Subscriptions define the various features and levels of functionality that are available to your organization.

ZIA End User Notification
^^^^^^^^^^^^^^^^^^^^^^^^^^
(`#261 <https://github.com/zscaler/zscaler-sdk-python/pull/261>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /eun` to retrieve information browser-based end user notification (EUN) configuration details.
  - Added `PUT /eun` to update the browser-based end user notification (EUN) configuration details.

ZIA Admin Audit Logs
^^^^^^^^^^^^^^^^^^^^^^^

(`#261 <https://github.com/zscaler/zscaler-sdk-python/pull/261>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /auditlogEntryReport` to retrieve the status of a request for an audit log report.
  - Added `POST /auditlogEntryReport` to create an audit log report for the specified time period and saves it as a CSV file.
  - Added `DELETE /auditlogEntryReport` to cancel the request to create an audit log report.
  - Added `GET /auditlogEntryReport/download` to download the most recently created audit log report.

ZIA Extranets
^^^^^^^^^^^^^^^^^^

(`#261 <https://github.com/zscaler/zscaler-sdk-python/pull/261>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /extranet` to retrieve the list of extranets configured for the organization
  - Added `GET /extranet/lite` Retrieves the name-ID pairs of all extranets configured for an organization
  - Added `GET /extranet/{Id}` Retrieves information about an extranet based on the specified ID.
  - Added `POST /extranet` Adds a new extranet for the organization.
  - Added `PUT /extranet/{Id}` Updates an extranet based on the specified ID
  - Added `DELETE /extranet/{Id}` Deletes an extranet based on the specified ID

ZIA IOT Endpoint
^^^^^^^^^^^^^^^^^^

(`#261 <https://github.com/zscaler/zscaler-sdk-python/pull/261>`_) - Added the following new ZIA IOT API Endpoints:
  - Added `GET /iotDiscovery/deviceTypes` Retrieve the mapping between device type universally unique identifier (UUID) values and the device type names for all the device types supported by the Zscaler AI/ML.
  - Added `GET /iotDiscovery/categories` Retrieve the mapping between the device category universally unique identifier (UUID) values and the category names for all the device categories supported by the Zscaler AI/ML. The parent of device category is device type.
  - Added `GET /iotDiscovery/classifications` Retrieve the mapping between the device classification universally unique identifier (UUID) values and the classification names for all the device classifications supported by Zscaler AI/ML. The parent of device classification is device category.
  - Added `GET /iotDiscovery/deviceList` Retrieve a list of discovered devices with the following key contexts, IP address, location, ML auto-label, classification, category, and type.

ZIA 3rd-Party App Governance
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#261 <https://github.com/zscaler/zscaler-sdk-python/pull/261>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /apps/app` to search the 3rd-Party App Governance App Catalog by either app ID or URL.
  - Added `POST /apps/app` to submis an app for analysis in the 3rd-Party App Governance Sandbox.
  - Added `GET /apps/search` to search for an app by name. Any app whose name contains the search term (appName) is returned.
  - Added `GET /app_views/list` to retrieve the list of custom views that you have configured in the 3rd-Party App Governance.
  - Added `GET /app_views/{appViewId}/apps` to retrieves all assets (i.e., apps) that are related to a specified argument (i.e., custom view).

ZIA Admin Role Endpoints
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#261 <https://github.com/zscaler/zscaler-sdk-python/pull/261>`_) - Added the following new ZIA API Endpoints:
    - Added `GET /adminRoles/{roleId}` Retrieves the admin role based on the specified ID
    - Added `GET /adminRoles/lite` Retrieves a name and ID dictionary of all admin roles. The list only includes the name and ID for all admin roles.
    - Added `POST /adminRoles` Adds an admin role.
    - Added `PUT /adminRoles/{roleId}` Updates the admin role based on the specified ID.
    - Added `DELETE /adminRoles/{roleId}` Deletes the admin role based on the specified ID.

ZPA Credential Pool (New)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#261 <https://github.com/zscaler/zscaler-sdk-python/pull/261>`_) - Added new ZPA endpoint:
  - Added `GET /credential-pool` Gets the privileged credential pool details for the specified customer.
  - Added `GET /credential-pool/{id}` Gets the privileged credential pool details for the specified customer.
  - Added `GET /credential-pool/{id}/credential` Given Privileged credential pool id gets mapped privileged credential info
  - Added `POST /credential-pool` Adds a new privileged credential pool for the specified customer.
  - Added `PUT /credential-pool/{id}` Updates the existing credential pool for the specified customer.
  - Added `DELETE /credential-pool/{id}` Updates the existing credential pool for the specified customer.

ZWA - Zscaler Workflow Automation (NEW)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#261 <https://github.com/zscaler/zscaler-sdk-python/pull/261>`_) - Added new ZWA endpoint:
  - Added `GET /dlp/v1/incidents/transactions/{transactionId}` Gets the list of all DLP incidents associated with the transaction ID
  - Added `GET /dlp/v1/incidents/{dlpIncidentId}` Gets the DLP incident details based on the incident ID.
  - Added `DELETE /dlp/v1/incidents/{dlpIncidentId}` Deletes the DLP incident for the specified incident ID.
  - Added `GET /dlp/v1/incidents{dlpIncidentId}/change-history` Gets the details of updates made to an incident based on the given ID and timeline.
  - Added `GET /dlp/v1/incidents/{dlpIncidentId}/tickets` Gets the information of the ticket generated for the incident. For example, ticket type, ticket ID, ticket status, etc.
  - Added `POST /dlp/v1/incidents/{dlpIncidentId}/incident-groups/search` Filters a list of DLP incident groups to which the specified incident ID belongs.
  - Added `POST /dlp/v1/incidents/{dlpIncidentId}/close` Updates the status of the incident to resolved and closes the incident with a resolution label and a resolution code.
  - Added `POST /dlp/v1/incidents/{dlpIncidentId}/notes` Adds notes to the incident during updates or status changes.
  - Added `POST /dlp/v1/incidents/{dlpIncidentId}/labels` Assign lables (a label name and it's associated value) to DLP incidents.
  - Added `POST /dlp/v1/incidents/search` Filters DLP incidents based on the given time range and the field values.
  - Added `GET /dlp/v1/incidents/{dlpIncidentId}/triggers` Downloads the actual data that triggered the incident.
  - Added `GET /dlp/v1/incidents/{dlpIncidentId}/evidence` Gets the evidence URL of the incident.

Cloud & Branch Connector - OneAPI Support
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(`#261 <https://github.com/zscaler/zscaler-sdk-python/pull/261>`_) - Cloud & Branch Connector package is now compatible with OneAPI and Legacy API framework. Please refer to README for details.
(`#261 <https://github.com/zscaler/zscaler-sdk-python/pull/261>`_) - Cloud & Branch Connector package has been renamed from `zcon` to `ztw`

ZTW Policy Management
^^^^^^^^^^^^^^^^^^^^^^^

(`#261 <https://github.com/zscaler/zscaler-sdk-python/pull/261>`_) - Added the following new ZTW API Endpoints:
    - Added `GET /ecRules/ecRdr` Retrieves the list of traffic forwarding rules.
    - Added `PUT /ecRules/ecRdr/{ruleId}` Updates a traffic forwarding rule configuration based on the specified ID.
    - Added `POST /ecRules/ecRdr` Creates a new traffic forwarding rule.
    - Added `GET /ecRules/ecRdr/count` Retrieves the count of traffic forwarding rules available in the Cloud & Branch Connector Admin Portal.

ZTW Policy Resources
^^^^^^^^^^^^^^^^^^^^^

(`#261 <https://github.com/zscaler/zscaler-sdk-python/pull/261>`_) - Added the following new ZTW API Endpoints:
    - Added `GET /ipSourceGroups` Retrieves the list of source IP groups.
    - Added `GET /ipSourceGroups/lite` Retrieves the list of source IP groups. This request retrieves basic information about the source IP groups, such as name and ID. For extensive details, use the GET /ipSourceGroups request.
    - Added `POST /ipSourceGroups` Adds a new custom source IP group.
    - Added `DELETE /ipSourceGroups/{ipGroupId}` Deletes a source IP group based on the specified ID.
    - Added `GET /ipDestinationGroups` Retrieves the list of destination IP groups.
    - Added `GET /ipDestinationGroups/lite` Retrieves the list of destination IP groups. This request retrieves basic information about the destination IP groups, ID, name, and type. For extensive details, use the GET /ipDestinationGroups request.
    - Added `POST /ipDestinationGroups` Adds a new custom destination IP group.
    - Added `DELETE /ipDestinationGroups/{ipGroupId}` Deletes the destination IP group based on the specified ID. Default destination groups that are automatically created cannot be deleted.
    - Added `GET /ipGroups` Retrieves the list of IP pools.
    - Added `GET /ipGroups/lite` Retrieves the list of IP pools. This request retrieves basic information about the IP pools, such as name and ID. For extensive details, use the GET /ipGroups request.
    - Added `POST /ipGroups` Adds a new custom IP pool.
    - Added `DELETE /ipGroups/{ipGroupId}` Deletes an IP pool based on the specified ID.
    - Added `GET /networkServices` Retrieves the list of all network services. The search parameters find matching values within the name or description attributes.
    - Added `POST /networkServices` Creates a new network service.
    - Added `PUT /networkServices/{serviceId}` Updates the network service information for the specified service ID.
    - Added `DELETE /networkServices/{serviceId}` Deletes the network service for the specified ID.
    - Added `GET /networkServicesGroups` Retrieves the list of network service groups.
    - Added `GET /zpaResources/applicationSegments` Retrieves the list of ZPA application segments that can be configured in traffic forwarding rule criteria.

1.0.2 (April, 22 2025) - BREAKING CHANGES
-----------------------------------------

Notes
-----

- Python Versions: **v3.8, v3.9, v3.10, v3.11**


Zscaler OneAPI Support
-----------------------

(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_): Added support for (`OneAPI <https://help.zscaler.com/zidentity/what-zidentity>`_) Oauth2 authentication support through (`Zidentity <https://help.zscaler.com/zidentity/what-zidentity>`_)

**NOTES**
  - Starting at v1.0.0 version this SDK provides dual API client functionality and is backwards compatible with the legacy Zscaler API framework.
  - The new OneAPI framework is compatible only with the following products `ZCC/ZIA/ZPA`.
  - The following products `ZTW` - Cloud Connector and `ZDX` and Zscaler Digital Experience, authentication methods remain unnaffected.
  - The package `ZCON` (Zscaler Cloud and Branch Connector) has been renamed to `ZTW`
  - The following products `ZWA` - Zscaler Workflow Automation authentication methods remain unnaffected.

Refer to the (`README <hhttps://github.com/zscaler/zscaler-sdk-python/blob/master/README.md>`_) page for details on client instantiation, and authentication requirements on each individual product.

**WARNING**: Attention Government customers. OneAPI and Zidentity is not currently supported for the following ZIA clouds: `zscalergov` and `zscalerten` or ZPA `GOV`, and `GOVUS`. 
See the Zscaler Legacy API Framework section in the (`README Docs <https://zscaler-sdk-python.readthedocs.io/en/latest/index.html>`_) for more information on how authenticate to these environments using the built-in Legacy API method.

(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_): All API clients now support Config Setter object `ZCC/ZTW/ZDX/ZIA/ZPA/ZWA`

ZCC New Endpoints
^^^^^^^^^^^^^^^^^

(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Added the following new ZCC API Endpoints:
  - Added `GET /downloadServiceStatus` to download service status for all devices.
  - Added `GET /getDeviceCleanupInfo` to retrieve device cleanup information.
  - Added `PUT /setDeviceCleanupInfo` to cleanup device information.
  - Added `GET /getDeviceDetails` to retrieve device detailed information.
  - Added `GET /getAdminUsers` to retrieve mobile portal admin user.
  - Added `PUT /editAdminUser` to update mobile portal admin user.
  - Added `GET /getAdminUsersSyncInfo` to retrieve mobile portal admin user sync information.
  - Added `POST /syncZiaZdxAdminUsers` to retrieve mobile portal admin users ZIA and ZDX sync information.
  - Added `POST /syncZpaAdminUsers` to retrieve mobile portal admin users ZPA sync information.
  - Added `GET /getAdminRoles` to retrieve mobile portal admin roles.
  - Added `GET /getCompanyInfo` to retrieve company information.
  - Added `GET /getZdxGroupEntitlements` to retrieve ZDX Group entitlement enablement.
  - Added `PUT /updateZdxGroupEntitlement` to retrieve ZDX Group entitlement enablement.
  - Added `GET /updateZpaGroupEntitlement` to retrieve ZPA Group entitlement enablement.
  - Added `GET /web/policy/listByCompany` to retrieve Web Policy By Company ID.
  - Added `PUT /web/policy/activate` to activate mobile portal web policy
  - Added `PUT /web/policy/edit` to update mobile portal web policy
  - Added `DELETE /web/policy/{policyId}/delete` to delete mobile portal web policy.
  - Added `GET /webAppService/listByCompany` to retrieve Web App Service information By Company ID.
  - Added `GET /webFailOpenPolicy/listByCompany` to retrieve web Fail Open Policy information By Company ID.
  - Added `PUT /webFailOpenPolicy/edit` to update mobile portal web Fail Open Policy.
  - Added `GET /webForwardingProfile/listByCompany` to retrieve Web Forwarding Profile information By Company ID.
  - Added `POST /webForwardingProfile/edit` to create a Web Forwarding Profile.
  - Added `DELETE /webForwardingProfile/{profileId}/delete` to delete Web Forwarding Profile.
  - Added `GET /webTrustedNetwork/listByCompany` to retrieve multiple Web Trusted Network information By Company ID.
  - Added `POST /webTrustedNetwork/edit` to create Web Trusted Network resource.
  - Added `PUT /webTrustedNetwork/edit` to update Web Trusted Network resource.
  - Added `DELETE /webTrustedNetwork/{networkId}/delete` to delete Web Trusted Network resource.
  - Added `GET /getWebPrivacyInfo` to retrieve Web Privacy Info.
  - Added `GET /setWebPrivacyInfo` to update Web Privacy Info.

ZIA Sandbox Submission - BREAKING CHANGES
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Authentication to Zscaler Sandbox now use the following attributes during client instantiation.
 - `sandboxToken` - Can also be sourced from the `ZSCALER_SANDBOX_TOKEN` environment variable.
 - `sandboxCloud` - Can also be sourced from the `ZSCALER_SANDBOX_CLOUD` environment variable.

**NOTE** The previous `ZIA_SANDBOX_TOKEN` has been deprecated.

ZIA Sandbox Rules
^^^^^^^^^^^^^^^^^^

(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /sandboxRules` to retrieve the list of all Sandbox policy rules.
  - Added `GET /sandboxRules/{ruleId}` to retrieve the Sandbox policy rule information based on the specified ID.
  - Added `POST /sandboxRules` to add a Sandbox policy rule.
  - Added `PUT /sandboxRules/{ruleId}` to update the Sandbox policy rule configuration for the specified ID.
  - Added `DELETE /sandboxRules/{ruleId}` to delete the Sandbox policy rule based on the specified ID.

ZIA DNS Control Rules
^^^^^^^^^^^^^^^^^^^^^^

(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /firewallDnsRules` to retrieve the list of all DNS Control policy rules.
  - Added `GET /firewallDnsRules/{ruleId}` to retrieve the DNS Control policy rule information based on the specified ID.
  - Added `POST /firewallDnsRules` to add a DNS Control policy rules.
  - Added `PUT /firewallDnsRules/{ruleId}` to update the DNS Control policy rule configuration for the specified ID.
  - Added `DELETE /firewallDnsRules/{ruleId}` to delete the DNS Control policy rule based on the specified ID.

ZIA IPS Control Rules
^^^^^^^^^^^^^^^^^^^^^

(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /firewallIpsRules` to retrieve the list of all IPS Control policy rules.
  - Added `GET /firewallIpsRules/{ruleId}` to retrieve the IPS Control policy rule information based on the specified ID.
  - Added `POST /firewallIpsRules` to add a IPS Control policy rule.
  - Added `PUT /firewallIpsRules/{ruleId}` to update the IPS Control policy rule configuration for the specified ID.
  - Added `DELETE /firewallIpsRules/{ruleId}` to delete the IPS Control policy rule based on the specified ID.

ZIA File Type Control Policy
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /fileTypeRules` to retrieve the list of all File Type Control policy rules.
  - Added `GET /fileTypeRules/lite` to retrieve the list of all File Type Control policy rules.
  - Added `GET /fileTypeRules/{ruleId}` to retrieve the File Type Control policy rule information based on the specified ID.
  - Added `POST /fileTypeRules` to add a File Type Control policy rule.
  - Added `PUT /fileTypeRules/{ruleId}` to update the File Type Control policy rule configuration for the specified ID.
  - Added `DELETE /fileTypeRules/{ruleId}` to delete the File Type Control policy rule based on the specified ID.

ZIA Forwarding Control Policy - Proxy Gateways
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /proxyGateways` to retrieve the proxy gateway information.
  - Added `GET /proxyGateways/lite` to retrieve the name and ID of the proxy.

ZIA Cloud Nanolog Streaming Service (NSS)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /nssFeeds` to retrieve the cloud NSS feeds.
  - Added `GET /nssFeeds/{feedId}` to retrieve information about cloud NSS feed based on the specified ID.
  - Added `POST /nssFeeds` to add a new cloud NSS feed.
  - Added `PUT /nssFeeds/{feedId}` to update cloud NSS feed configuration based on the specified ID.
  - Added `DELETE /nssFeeds/{feedId}` to delete cloud NSS feed configuration based on the specified ID.
  - Added `GET /nssFeeds/feedOutputDefaults` to retrieve the default cloud NSS feed output format for different log types.
  - Added `GET /nssFeeds/testConnectivity/{feedId}` to test the connectivity of cloud NSS feed based on the specified ID
  - Added `POST /nssFeeds/validateFeedFormat` to validates the cloud NSS feed format and returns the validation result

ZIA Advanced Threat Protection Policy
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /cyberThreatProtection/advancedThreatSettings` to retrieve the advanced threat configuration settings.
  - Added `PUT /cyberThreatProtection/advancedThreatSettings` to update the advanced threat configuration settings.
  - Added `GET /cyberThreatProtection/maliciousUrls` to retrieve the malicious URLs added to the denylist in the Advanced Threat Protection (ATP) policy
  - Added `PUT /cyberThreatProtection/maliciousUrls` to updates the malicious URLs added to the denylist in ATP policy
  - Added `GET /cyberThreatProtection/securityExceptions` to retrieves information about the security exceptions configured for the ATP policy
  - Added `PUT /cyberThreatProtection/securityExceptions` to update security exceptions for the ATP policy

ZIA Advanced Threat Protection Policy
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /cyberThreatProtection/atpMalwareInspection` to retrieve the traffic inspection configurations of Malware Protection policy
  - Added `PUT /cyberThreatProtection/atpMalwareInspection` to update the traffic inspection configurations of Malware Protection policy.
  - Added `GET /cyberThreatProtection/atpMalwareProtocols` to retrieve the protocol inspection configurations of Malware Protection policy
  - Added `PUT /cyberThreatProtection/atpMalwareProtocols` to update the protocol inspection configurations of Malware Protection policy.
  - Added `GET /cyberThreatProtection/malwareSettings` to retrieve the malware protection policy configuration details
  - Added `PUT /cyberThreatProtection/malwareSettings` to update the malware protection policy configuration details.
  - Added `GET /cyberThreatProtection/malwarePolicy` to retrieve information about the security exceptions configured for the Malware Protection policy
  - Added `PUT /cyberThreatProtection/malwarePolicy` to update security exceptions for the Malware Protection policy.

ZIA URL & Cloud App Control Policy Settings
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /advancedUrlFilterAndCloudAppSettings` to retrieve information about URL and Cloud App Control advanced policy settings
  - Added `PUT /advancedUrlFilterAndCloudAppSettings` to update the URL and Cloud App Control advanced policy settings

ZIA Authentication Settings
^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /authSettings` to retrieve the organization's default authentication settings information, including authentication profile and Kerberos authentication information.
  - Added `GET /authSettings/lite` to retrieve organization's default authentication settings information.
  - Added `PUT /authSettings` to update the organization's default authentication settings information.

ZIA Advanced Settings
^^^^^^^^^^^^^^^^^^^^^

(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /advancedSettings` to retrieve information about the advanced settings.
  - Added `PUT /advancedSettings` to update the advanced settings configuration.

ZIA Cloud Applications
^^^^^^^^^^^^^^^^^^^^^^^

(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /cloudApplications/policy` Retrieves a list of Predefined and User Defined Cloud Applications associated with the DLP rules, Cloud App Control rules, Advanced Settings, Bandwidth Classes, and File Type Control rules.
  - Added `GET /cloudApplications/sslPolicy` Retrieves a list of Predefined and User Defined Cloud Applications associated with the SSL Inspection rules.

ZIA Shadow IT Report
^^^^^^^^^^^^^^^^^^^^

(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Added the following new ZIA API Endpoints:
- Added `PUT /cloudApplications/bulkUpdate` To Update application status and tag information for predefined or custom cloud applications based on the IDs specified
- Added `GET /cloudApplications/lite` Gets the list of predefined and custom cloud applications
- Added `GET /customTags` Gets the list of custom tags available to assign to cloud applications
- Added `POST /shadowIT/applications/export` Export the Shadow IT Report (in CSV format) for the cloud applications recognized by Zscaler based on their usage in your organization.
- Added `POST /shadowIT/applications/{entity}/exportCsv` Export the Shadow IT Report (in CSV format) for the list of users or known locations identified with using the cloud applications specified in the request.

ZIA Remote Assistance Support
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /remoteAssistance` to retrieve information about the Remote Assistance option.
  - Added `PUT /remoteAssistance` to update information about the Remote Assistance option. Using this option, you can allow Zscaler Support to access your organization’s ZIA Admin Portal for a specified time period to troubleshoot issues.

ZIA Organization Details
^^^^^^^^^^^^^^^^^^^^^^^^^

(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /orgInformation` to retrieve detailed organization information, including headquarter location, geolocation, address, and contact details.
  - Added `GET /orgInformation/lite` to retrieve minimal organization information.
  - Added `GET /subscriptions` to retrieve information about the list of subscriptions enabled for your tenant. Subscriptions define the various features and levels of functionality that are available to your organization.

ZIA End User Notification
^^^^^^^^^^^^^^^^^^^^^^^^^^
(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /eun` to retrieve information browser-based end user notification (EUN) configuration details.
  - Added `PUT /eun` to update the browser-based end user notification (EUN) configuration details.

ZIA Admin Audit Logs
^^^^^^^^^^^^^^^^^^^^^^^

(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /auditlogEntryReport` to retrieve the status of a request for an audit log report.
  - Added `POST /auditlogEntryReport` to create an audit log report for the specified time period and saves it as a CSV file.
  - Added `DELETE /auditlogEntryReport` to cancel the request to create an audit log report.
  - Added `GET /auditlogEntryReport/download` to download the most recently created audit log report.

ZIA Extranets
^^^^^^^^^^^^^^^^^^

(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /extranet` to retrieve the list of extranets configured for the organization
  - Added `GET /extranet/lite` Retrieves the name-ID pairs of all extranets configured for an organization
  - Added `GET /extranet/{Id}` Retrieves information about an extranet based on the specified ID.
  - Added `POST /extranet` Adds a new extranet for the organization.
  - Added `PUT /extranet/{Id}` Updates an extranet based on the specified ID
  - Added `DELETE /extranet/{Id}` Deletes an extranet based on the specified ID

ZIA IOT Endpoint
^^^^^^^^^^^^^^^^^^

(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Added the following new ZIA IOT API Endpoints:
  - Added `GET /iotDiscovery/deviceTypes` Retrieve the mapping between device type universally unique identifier (UUID) values and the device type names for all the device types supported by the Zscaler AI/ML.
  - Added `GET /iotDiscovery/categories` Retrieve the mapping between the device category universally unique identifier (UUID) values and the category names for all the device categories supported by the Zscaler AI/ML. The parent of device category is device type.
  - Added `GET /iotDiscovery/classifications` Retrieve the mapping between the device classification universally unique identifier (UUID) values and the classification names for all the device classifications supported by Zscaler AI/ML. The parent of device classification is device category.
  - Added `GET /iotDiscovery/deviceList` Retrieve a list of discovered devices with the following key contexts, IP address, location, ML auto-label, classification, category, and type.

ZIA 3rd-Party App Governance
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /apps/app` to search the 3rd-Party App Governance App Catalog by either app ID or URL.
  - Added `POST /apps/app` to submis an app for analysis in the 3rd-Party App Governance Sandbox.
  - Added `GET /apps/search` to search for an app by name. Any app whose name contains the search term (appName) is returned.
  - Added `GET /app_views/list` to retrieve the list of custom views that you have configured in the 3rd-Party App Governance.
  - Added `GET /app_views/{appViewId}/apps` to retrieves all assets (i.e., apps) that are related to a specified argument (i.e., custom view).

ZIA Admin Role Endpoints
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Added the following new ZIA API Endpoints:
    - Added `GET /adminRoles/{roleId}` Retrieves the admin role based on the specified ID
    - Added `GET /adminRoles/lite` Retrieves a name and ID dictionary of all admin roles. The list only includes the name and ID for all admin roles.
    - Added `POST /adminRoles` Adds an admin role.
    - Added `PUT /adminRoles/{roleId}` Updates the admin role based on the specified ID.
    - Added `DELETE /adminRoles/{roleId}` Deletes the admin role based on the specified ID.

ZPA Credential Pool (New)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Added new ZPA endpoint:
  - Added `GET /credential-pool` Gets the privileged credential pool details for the specified customer.
  - Added `GET /credential-pool/{id}` Gets the privileged credential pool details for the specified customer.
  - Added `GET /credential-pool/{id}/credential` Given Privileged credential pool id gets mapped privileged credential info
  - Added `POST /credential-pool` Adds a new privileged credential pool for the specified customer.
  - Added `PUT /credential-pool/{id}` Updates the existing credential pool for the specified customer.
  - Added `DELETE /credential-pool/{id}` Updates the existing credential pool for the specified customer.

ZWA - Zscaler Workflow Automation (NEW)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Added new ZWA endpoint:
  - Added `GET /dlp/v1/incidents/transactions/{transactionId}` Gets the list of all DLP incidents associated with the transaction ID
  - Added `GET /dlp/v1/incidents/{dlpIncidentId}` Gets the DLP incident details based on the incident ID.
  - Added `DELETE /dlp/v1/incidents/{dlpIncidentId}` Deletes the DLP incident for the specified incident ID.
  - Added `GET /dlp/v1/incidents{dlpIncidentId}/change-history` Gets the details of updates made to an incident based on the given ID and timeline.
  - Added `GET /dlp/v1/incidents/{dlpIncidentId}/tickets` Gets the information of the ticket generated for the incident. For example, ticket type, ticket ID, ticket status, etc.
  - Added `POST /dlp/v1/incidents/{dlpIncidentId}/incident-groups/search` Filters a list of DLP incident groups to which the specified incident ID belongs.
  - Added `POST /dlp/v1/incidents/{dlpIncidentId}/close` Updates the status of the incident to resolved and closes the incident with a resolution label and a resolution code.
  - Added `POST /dlp/v1/incidents/{dlpIncidentId}/notes` Adds notes to the incident during updates or status changes.
  - Added `POST /dlp/v1/incidents/{dlpIncidentId}/labels` Assign lables (a label name and it's associated value) to DLP incidents.
  - Added `POST /dlp/v1/incidents/search` Filters DLP incidents based on the given time range and the field values.
  - Added `GET /dlp/v1/incidents/{dlpIncidentId}/triggers` Downloads the actual data that triggered the incident.
  - Added `GET /dlp/v1/incidents/{dlpIncidentId}/evidence` Gets the evidence URL of the incident.

Cloud & Branch Connector - OneAPI Support
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Cloud & Branch Connector package is now compatible with OneAPI and Legacy API framework. Please refer to README for details.
(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Cloud & Branch Connector package has been renamed from `zcon` to `ztw`

ZTW Policy Management
^^^^^^^^^^^^^^^^^^^^^^^

(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Added the following new ZTW API Endpoints:
    - Added `GET /ecRules/ecRdr` Retrieves the list of traffic forwarding rules.
    - Added `PUT /ecRules/ecRdr/{ruleId}` Updates a traffic forwarding rule configuration based on the specified ID.
    - Added `POST /ecRules/ecRdr` Creates a new traffic forwarding rule.
    - Added `GET /ecRules/ecRdr/count` Retrieves the count of traffic forwarding rules available in the Cloud & Branch Connector Admin Portal.

ZTW Policy Resources
^^^^^^^^^^^^^^^^^^^^^

(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Added the following new ZTW API Endpoints:
    - Added `GET /ipSourceGroups` Retrieves the list of source IP groups.
    - Added `GET /ipSourceGroups/lite` Retrieves the list of source IP groups. This request retrieves basic information about the source IP groups, such as name and ID. For extensive details, use the GET /ipSourceGroups request.
    - Added `POST /ipSourceGroups` Adds a new custom source IP group.
    - Added `DELETE /ipSourceGroups/{ipGroupId}` Deletes a source IP group based on the specified ID.
    - Added `GET /ipDestinationGroups` Retrieves the list of destination IP groups.
    - Added `GET /ipDestinationGroups/lite` Retrieves the list of destination IP groups. This request retrieves basic information about the destination IP groups, ID, name, and type. For extensive details, use the GET /ipDestinationGroups request.
    - Added `POST /ipDestinationGroups` Adds a new custom destination IP group.
    - Added `DELETE /ipDestinationGroups/{ipGroupId}` Deletes the destination IP group based on the specified ID. Default destination groups that are automatically created cannot be deleted.
    - Added `GET /ipGroups` Retrieves the list of IP pools.
    - Added `GET /ipGroups/lite` Retrieves the list of IP pools. This request retrieves basic information about the IP pools, such as name and ID. For extensive details, use the GET /ipGroups request.
    - Added `POST /ipGroups` Adds a new custom IP pool.
    - Added `DELETE /ipGroups/{ipGroupId}` Deletes an IP pool based on the specified ID.
    - Added `GET /networkServices` Retrieves the list of all network services. The search parameters find matching values within the name or description attributes.
    - Added `POST /networkServices` Creates a new network service.
    - Added `PUT /networkServices/{serviceId}` Updates the network service information for the specified service ID.
    - Added `DELETE /networkServices/{serviceId}` Deletes the network service for the specified ID.
    - Added `GET /networkServicesGroups` Retrieves the list of network service groups.
    - Added `GET /zpaResources/applicationSegments` Retrieves the list of ZPA application segments that can be configured in traffic forwarding rule criteria.

1.0.1 (April, 22 2025) - BREAKING CHANGES
-----------------------------------------

Notes
-----

- Python Versions: **v3.8, v3.9, v3.10, v3.11**


Zscaler OneAPI Support
-----------------------

(`#260 <https://github.com/zscaler/zscaler-sdk-python/pull/260>`_): Added support for (`OneAPI <https://help.zscaler.com/zidentity/what-zidentity>`_) Oauth2 authentication support through (`Zidentity <https://help.zscaler.com/zidentity/what-zidentity>`_)

**NOTES**
  - Starting at v1.0.0 version this SDK provides dual API client functionality and is backwards compatible with the legacy Zscaler API framework.
  - The new OneAPI framework is compatible only with the following products `ZCC/ZIA/ZPA`.
  - The following products `ZTW` - Cloud Connector and `ZDX` and Zscaler Digital Experience, authentication methods remain unnaffected.
  - The package `ZCON` (Zscaler Cloud and Branch Connector) has been renamed to `ZTW`
  - The following products `ZWA` - Zscaler Workflow Automation authentication methods remain unnaffected.

Refer to the (`README <hhttps://github.com/zscaler/zscaler-sdk-python/blob/master/README.md>`_) page for details on client instantiation, and authentication requirements on each individual product.

**WARNING**: Attention Government customers. OneAPI and Zidentity is not currently supported for the following ZIA clouds: `zscalergov` and `zscalerten` or ZPA `GOV`, and `GOVUS`. 
See the Zscaler Legacy API Framework section in the (`README Docs <https://zscaler-sdk-python.readthedocs.io/en/latest/index.html>`_) for more information on how authenticate to these environments using the built-in Legacy API method.

(`#260 <https://github.com/zscaler/zscaler-sdk-python/pull/260>`_): All API clients now support Config Setter object `ZCC/ZTW/ZDX/ZIA/ZPA/ZWA`

ZCC New Endpoints
^^^^^^^^^^^^^^^^^

(`#260 <https://github.com/zscaler/zscaler-sdk-python/pull/260>`_) - Added the following new ZCC API Endpoints:
  - Added `GET /downloadServiceStatus` to download service status for all devices.
  - Added `GET /getDeviceCleanupInfo` to retrieve device cleanup information.
  - Added `PUT /setDeviceCleanupInfo` to cleanup device information.
  - Added `GET /getDeviceDetails` to retrieve device detailed information.
  - Added `GET /getAdminUsers` to retrieve mobile portal admin user.
  - Added `PUT /editAdminUser` to update mobile portal admin user.
  - Added `GET /getAdminUsersSyncInfo` to retrieve mobile portal admin user sync information.
  - Added `POST /syncZiaZdxAdminUsers` to retrieve mobile portal admin users ZIA and ZDX sync information.
  - Added `POST /syncZpaAdminUsers` to retrieve mobile portal admin users ZPA sync information.
  - Added `GET /getAdminRoles` to retrieve mobile portal admin roles.
  - Added `GET /getCompanyInfo` to retrieve company information.
  - Added `GET /getZdxGroupEntitlements` to retrieve ZDX Group entitlement enablement.
  - Added `PUT /updateZdxGroupEntitlement` to retrieve ZDX Group entitlement enablement.
  - Added `GET /updateZpaGroupEntitlement` to retrieve ZPA Group entitlement enablement.
  - Added `GET /web/policy/listByCompany` to retrieve Web Policy By Company ID.
  - Added `PUT /web/policy/activate` to activate mobile portal web policy
  - Added `PUT /web/policy/edit` to update mobile portal web policy
  - Added `DELETE /web/policy/{policyId}/delete` to delete mobile portal web policy.
  - Added `GET /webAppService/listByCompany` to retrieve Web App Service information By Company ID.
  - Added `GET /webFailOpenPolicy/listByCompany` to retrieve web Fail Open Policy information By Company ID.
  - Added `PUT /webFailOpenPolicy/edit` to update mobile portal web Fail Open Policy.
  - Added `GET /webForwardingProfile/listByCompany` to retrieve Web Forwarding Profile information By Company ID.
  - Added `POST /webForwardingProfile/edit` to create a Web Forwarding Profile.
  - Added `DELETE /webForwardingProfile/{profileId}/delete` to delete Web Forwarding Profile.
  - Added `GET /webTrustedNetwork/listByCompany` to retrieve multiple Web Trusted Network information By Company ID.
  - Added `POST /webTrustedNetwork/edit` to create Web Trusted Network resource.
  - Added `PUT /webTrustedNetwork/edit` to update Web Trusted Network resource.
  - Added `DELETE /webTrustedNetwork/{networkId}/delete` to delete Web Trusted Network resource.
  - Added `GET /getWebPrivacyInfo` to retrieve Web Privacy Info.
  - Added `GET /setWebPrivacyInfo` to update Web Privacy Info.

ZIA Sandbox Submission - BREAKING CHANGES
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#260 <https://github.com/zscaler/zscaler-sdk-python/pull/260>`_) - Authentication to Zscaler Sandbox now use the following attributes during client instantiation.
 - `sandboxToken` - Can also be sourced from the `ZSCALER_SANDBOX_TOKEN` environment variable.
 - `sandboxCloud` - Can also be sourced from the `ZSCALER_SANDBOX_CLOUD` environment variable.

**NOTE** The previous `ZIA_SANDBOX_TOKEN` has been deprecated.

ZIA Sandbox Rules
^^^^^^^^^^^^^^^^^^

(`#260 <https://github.com/zscaler/zscaler-sdk-python/pull/260>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /sandboxRules` to retrieve the list of all Sandbox policy rules.
  - Added `GET /sandboxRules/{ruleId}` to retrieve the Sandbox policy rule information based on the specified ID.
  - Added `POST /sandboxRules` to add a Sandbox policy rule.
  - Added `PUT /sandboxRules/{ruleId}` to update the Sandbox policy rule configuration for the specified ID.
  - Added `DELETE /sandboxRules/{ruleId}` to delete the Sandbox policy rule based on the specified ID.

ZIA DNS Control Rules
^^^^^^^^^^^^^^^^^^^^^^

(`#260 <https://github.com/zscaler/zscaler-sdk-python/pull/260>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /firewallDnsRules` to retrieve the list of all DNS Control policy rules.
  - Added `GET /firewallDnsRules/{ruleId}` to retrieve the DNS Control policy rule information based on the specified ID.
  - Added `POST /firewallDnsRules` to add a DNS Control policy rules.
  - Added `PUT /firewallDnsRules/{ruleId}` to update the DNS Control policy rule configuration for the specified ID.
  - Added `DELETE /firewallDnsRules/{ruleId}` to delete the DNS Control policy rule based on the specified ID.

ZIA IPS Control Rules
^^^^^^^^^^^^^^^^^^^^^

(`#260 <https://github.com/zscaler/zscaler-sdk-python/pull/260>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /firewallIpsRules` to retrieve the list of all IPS Control policy rules.
  - Added `GET /firewallIpsRules/{ruleId}` to retrieve the IPS Control policy rule information based on the specified ID.
  - Added `POST /firewallIpsRules` to add a IPS Control policy rule.
  - Added `PUT /firewallIpsRules/{ruleId}` to update the IPS Control policy rule configuration for the specified ID.
  - Added `DELETE /firewallIpsRules/{ruleId}` to delete the IPS Control policy rule based on the specified ID.

ZIA File Type Control Policy
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#260 <https://github.com/zscaler/zscaler-sdk-python/pull/260>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /fileTypeRules` to retrieve the list of all File Type Control policy rules.
  - Added `GET /fileTypeRules/lite` to retrieve the list of all File Type Control policy rules.
  - Added `GET /fileTypeRules/{ruleId}` to retrieve the File Type Control policy rule information based on the specified ID.
  - Added `POST /fileTypeRules` to add a File Type Control policy rule.
  - Added `PUT /fileTypeRules/{ruleId}` to update the File Type Control policy rule configuration for the specified ID.
  - Added `DELETE /fileTypeRules/{ruleId}` to delete the File Type Control policy rule based on the specified ID.

ZIA Forwarding Control Policy - Proxy Gateways
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#260 <https://github.com/zscaler/zscaler-sdk-python/pull/260>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /proxyGateways` to retrieve the proxy gateway information.
  - Added `GET /proxyGateways/lite` to retrieve the name and ID of the proxy.

ZIA Cloud Nanolog Streaming Service (NSS)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#260 <https://github.com/zscaler/zscaler-sdk-python/pull/260>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /nssFeeds` to retrieve the cloud NSS feeds.
  - Added `GET /nssFeeds/{feedId}` to retrieve information about cloud NSS feed based on the specified ID.
  - Added `POST /nssFeeds` to add a new cloud NSS feed.
  - Added `PUT /nssFeeds/{feedId}` to update cloud NSS feed configuration based on the specified ID.
  - Added `DELETE /nssFeeds/{feedId}` to delete cloud NSS feed configuration based on the specified ID.
  - Added `GET /nssFeeds/feedOutputDefaults` to retrieve the default cloud NSS feed output format for different log types.
  - Added `GET /nssFeeds/testConnectivity/{feedId}` to test the connectivity of cloud NSS feed based on the specified ID
  - Added `POST /nssFeeds/validateFeedFormat` to validates the cloud NSS feed format and returns the validation result

ZIA Advanced Threat Protection Policy
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#260 <https://github.com/zscaler/zscaler-sdk-python/pull/260>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /cyberThreatProtection/advancedThreatSettings` to retrieve the advanced threat configuration settings.
  - Added `PUT /cyberThreatProtection/advancedThreatSettings` to update the advanced threat configuration settings.
  - Added `GET /cyberThreatProtection/maliciousUrls` to retrieve the malicious URLs added to the denylist in the Advanced Threat Protection (ATP) policy
  - Added `PUT /cyberThreatProtection/maliciousUrls` to updates the malicious URLs added to the denylist in ATP policy
  - Added `GET /cyberThreatProtection/securityExceptions` to retrieves information about the security exceptions configured for the ATP policy
  - Added `PUT /cyberThreatProtection/securityExceptions` to update security exceptions for the ATP policy

ZIA Advanced Threat Protection Policy
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#260 <https://github.com/zscaler/zscaler-sdk-python/pull/260>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /cyberThreatProtection/atpMalwareInspection` to retrieve the traffic inspection configurations of Malware Protection policy
  - Added `PUT /cyberThreatProtection/atpMalwareInspection` to update the traffic inspection configurations of Malware Protection policy.
  - Added `GET /cyberThreatProtection/atpMalwareProtocols` to retrieve the protocol inspection configurations of Malware Protection policy
  - Added `PUT /cyberThreatProtection/atpMalwareProtocols` to update the protocol inspection configurations of Malware Protection policy.
  - Added `GET /cyberThreatProtection/malwareSettings` to retrieve the malware protection policy configuration details
  - Added `PUT /cyberThreatProtection/malwareSettings` to update the malware protection policy configuration details.
  - Added `GET /cyberThreatProtection/malwarePolicy` to retrieve information about the security exceptions configured for the Malware Protection policy
  - Added `PUT /cyberThreatProtection/malwarePolicy` to update security exceptions for the Malware Protection policy.

ZIA URL & Cloud App Control Policy Settings
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#260 <https://github.com/zscaler/zscaler-sdk-python/pull/260>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /advancedUrlFilterAndCloudAppSettings` to retrieve information about URL and Cloud App Control advanced policy settings
  - Added `PUT /advancedUrlFilterAndCloudAppSettings` to update the URL and Cloud App Control advanced policy settings

ZIA Authentication Settings
^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#260 <https://github.com/zscaler/zscaler-sdk-python/pull/260>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /authSettings` to retrieve the organization's default authentication settings information, including authentication profile and Kerberos authentication information.
  - Added `GET /authSettings/lite` to retrieve organization's default authentication settings information.
  - Added `PUT /authSettings` to update the organization's default authentication settings information.

ZIA Advanced Settings
^^^^^^^^^^^^^^^^^^^^^

(`#260 <https://github.com/zscaler/zscaler-sdk-python/pull/260>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /advancedSettings` to retrieve information about the advanced settings.
  - Added `PUT /advancedSettings` to update the advanced settings configuration.

ZIA Cloud Applications
^^^^^^^^^^^^^^^^^^^^^^^

(`#260 <https://github.com/zscaler/zscaler-sdk-python/pull/260>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /cloudApplications/policy` Retrieves a list of Predefined and User Defined Cloud Applications associated with the DLP rules, Cloud App Control rules, Advanced Settings, Bandwidth Classes, and File Type Control rules.
  - Added `GET /cloudApplications/sslPolicy` Retrieves a list of Predefined and User Defined Cloud Applications associated with the SSL Inspection rules.

ZIA Shadow IT Report
^^^^^^^^^^^^^^^^^^^^

(`#260 <https://github.com/zscaler/zscaler-sdk-python/pull/260>`_) - Added the following new ZIA API Endpoints:
- Added `PUT /cloudApplications/bulkUpdate` To Update application status and tag information for predefined or custom cloud applications based on the IDs specified
- Added `GET /cloudApplications/lite` Gets the list of predefined and custom cloud applications
- Added `GET /customTags` Gets the list of custom tags available to assign to cloud applications
- Added `POST /shadowIT/applications/export` Export the Shadow IT Report (in CSV format) for the cloud applications recognized by Zscaler based on their usage in your organization.
- Added `POST /shadowIT/applications/{entity}/exportCsv` Export the Shadow IT Report (in CSV format) for the list of users or known locations identified with using the cloud applications specified in the request.

ZIA Remote Assistance Support
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#260 <https://github.com/zscaler/zscaler-sdk-python/pull/260>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /remoteAssistance` to retrieve information about the Remote Assistance option.
  - Added `PUT /remoteAssistance` to update information about the Remote Assistance option. Using this option, you can allow Zscaler Support to access your organization’s ZIA Admin Portal for a specified time period to troubleshoot issues.

ZIA Organization Details
^^^^^^^^^^^^^^^^^^^^^^^^^

(`#260 <https://github.com/zscaler/zscaler-sdk-python/pull/260>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /orgInformation` to retrieve detailed organization information, including headquarter location, geolocation, address, and contact details.
  - Added `GET /orgInformation/lite` to retrieve minimal organization information.
  - Added `GET /subscriptions` to retrieve information about the list of subscriptions enabled for your tenant. Subscriptions define the various features and levels of functionality that are available to your organization.

ZIA End User Notification
^^^^^^^^^^^^^^^^^^^^^^^^^^
(`#260 <https://github.com/zscaler/zscaler-sdk-python/pull/260>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /eun` to retrieve information browser-based end user notification (EUN) configuration details.
  - Added `PUT /eun` to update the browser-based end user notification (EUN) configuration details.

ZIA Admin Audit Logs
^^^^^^^^^^^^^^^^^^^^^^^

(`#260 <https://github.com/zscaler/zscaler-sdk-python/pull/260>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /auditlogEntryReport` to retrieve the status of a request for an audit log report.
  - Added `POST /auditlogEntryReport` to create an audit log report for the specified time period and saves it as a CSV file.
  - Added `DELETE /auditlogEntryReport` to cancel the request to create an audit log report.
  - Added `GET /auditlogEntryReport/download` to download the most recently created audit log report.

ZIA Extranets
^^^^^^^^^^^^^^^^^^

(`#260 <https://github.com/zscaler/zscaler-sdk-python/pull/260>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /extranet` to retrieve the list of extranets configured for the organization
  - Added `GET /extranet/lite` Retrieves the name-ID pairs of all extranets configured for an organization
  - Added `GET /extranet/{Id}` Retrieves information about an extranet based on the specified ID.
  - Added `POST /extranet` Adds a new extranet for the organization.
  - Added `PUT /extranet/{Id}` Updates an extranet based on the specified ID
  - Added `DELETE /extranet/{Id}` Deletes an extranet based on the specified ID

ZIA IOT Endpoint
^^^^^^^^^^^^^^^^^^

(`#260 <https://github.com/zscaler/zscaler-sdk-python/pull/260>`_) - Added the following new ZIA IOT API Endpoints:
  - Added `GET /iotDiscovery/deviceTypes` Retrieve the mapping between device type universally unique identifier (UUID) values and the device type names for all the device types supported by the Zscaler AI/ML.
  - Added `GET /iotDiscovery/categories` Retrieve the mapping between the device category universally unique identifier (UUID) values and the category names for all the device categories supported by the Zscaler AI/ML. The parent of device category is device type.
  - Added `GET /iotDiscovery/classifications` Retrieve the mapping between the device classification universally unique identifier (UUID) values and the classification names for all the device classifications supported by Zscaler AI/ML. The parent of device classification is device category.
  - Added `GET /iotDiscovery/deviceList` Retrieve a list of discovered devices with the following key contexts, IP address, location, ML auto-label, classification, category, and type.

ZIA 3rd-Party App Governance
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#260 <https://github.com/zscaler/zscaler-sdk-python/pull/260>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /apps/app` to search the 3rd-Party App Governance App Catalog by either app ID or URL.
  - Added `POST /apps/app` to submis an app for analysis in the 3rd-Party App Governance Sandbox.
  - Added `GET /apps/search` to search for an app by name. Any app whose name contains the search term (appName) is returned.
  - Added `GET /app_views/list` to retrieve the list of custom views that you have configured in the 3rd-Party App Governance.
  - Added `GET /app_views/{appViewId}/apps` to retrieves all assets (i.e., apps) that are related to a specified argument (i.e., custom view).

ZIA Admin Role Endpoints
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#260 <https://github.com/zscaler/zscaler-sdk-python/pull/260>`_) - Added the following new ZIA API Endpoints:
    - Added `GET /adminRoles/{roleId}` Retrieves the admin role based on the specified ID
    - Added `GET /adminRoles/lite` Retrieves a name and ID dictionary of all admin roles. The list only includes the name and ID for all admin roles.
    - Added `POST /adminRoles` Adds an admin role.
    - Added `PUT /adminRoles/{roleId}` Updates the admin role based on the specified ID.
    - Added `DELETE /adminRoles/{roleId}` Deletes the admin role based on the specified ID.

ZPA Credential Pool (New)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#260 <https://github.com/zscaler/zscaler-sdk-python/pull/260>`_) - Added new ZPA endpoint:
  - Added `GET /credential-pool` Gets the privileged credential pool details for the specified customer.
  - Added `GET /credential-pool/{id}` Gets the privileged credential pool details for the specified customer.
  - Added `GET /credential-pool/{id}/credential` Given Privileged credential pool id gets mapped privileged credential info
  - Added `POST /credential-pool` Adds a new privileged credential pool for the specified customer.
  - Added `PUT /credential-pool/{id}` Updates the existing credential pool for the specified customer.
  - Added `DELETE /credential-pool/{id}` Updates the existing credential pool for the specified customer.

ZWA - Zscaler Workflow Automation (NEW)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#260 <https://github.com/zscaler/zscaler-sdk-python/pull/260>`_) - Added new ZWA endpoint:
  - Added `GET /dlp/v1/incidents/transactions/{transactionId}` Gets the list of all DLP incidents associated with the transaction ID
  - Added `GET /dlp/v1/incidents/{dlpIncidentId}` Gets the DLP incident details based on the incident ID.
  - Added `DELETE /dlp/v1/incidents/{dlpIncidentId}` Deletes the DLP incident for the specified incident ID.
  - Added `GET /dlp/v1/incidents{dlpIncidentId}/change-history` Gets the details of updates made to an incident based on the given ID and timeline.
  - Added `GET /dlp/v1/incidents/{dlpIncidentId}/tickets` Gets the information of the ticket generated for the incident. For example, ticket type, ticket ID, ticket status, etc.
  - Added `POST /dlp/v1/incidents/{dlpIncidentId}/incident-groups/search` Filters a list of DLP incident groups to which the specified incident ID belongs.
  - Added `POST /dlp/v1/incidents/{dlpIncidentId}/close` Updates the status of the incident to resolved and closes the incident with a resolution label and a resolution code.
  - Added `POST /dlp/v1/incidents/{dlpIncidentId}/notes` Adds notes to the incident during updates or status changes.
  - Added `POST /dlp/v1/incidents/{dlpIncidentId}/labels` Assign lables (a label name and it's associated value) to DLP incidents.
  - Added `POST /dlp/v1/incidents/search` Filters DLP incidents based on the given time range and the field values.
  - Added `GET /dlp/v1/incidents/{dlpIncidentId}/triggers` Downloads the actual data that triggered the incident.
  - Added `GET /dlp/v1/incidents/{dlpIncidentId}/evidence` Gets the evidence URL of the incident.

Cloud & Branch Connector - OneAPI Support
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(`#260 <https://github.com/zscaler/zscaler-sdk-python/pull/260>`_) - Cloud & Branch Connector package is now compatible with OneAPI and Legacy API framework. Please refer to README for details.
(`#260 <https://github.com/zscaler/zscaler-sdk-python/pull/260>`_) - Cloud & Branch Connector package has been renamed from `zcon` to `ztw`

ZTW Policy Management
^^^^^^^^^^^^^^^^^^^^^^^

(`#260 <https://github.com/zscaler/zscaler-sdk-python/pull/260>`_) - Added the following new ZTW API Endpoints:
    - Added `GET /ecRules/ecRdr` Retrieves the list of traffic forwarding rules.
    - Added `PUT /ecRules/ecRdr/{ruleId}` Updates a traffic forwarding rule configuration based on the specified ID.
    - Added `POST /ecRules/ecRdr` Creates a new traffic forwarding rule.
    - Added `GET /ecRules/ecRdr/count` Retrieves the count of traffic forwarding rules available in the Cloud & Branch Connector Admin Portal.

ZTW Policy Resources
^^^^^^^^^^^^^^^^^^^^^

(`#260 <https://github.com/zscaler/zscaler-sdk-python/pull/260>`_) - Added the following new ZTW API Endpoints:
    - Added `GET /ipSourceGroups` Retrieves the list of source IP groups.
    - Added `GET /ipSourceGroups/lite` Retrieves the list of source IP groups. This request retrieves basic information about the source IP groups, such as name and ID. For extensive details, use the GET /ipSourceGroups request.
    - Added `POST /ipSourceGroups` Adds a new custom source IP group.
    - Added `DELETE /ipSourceGroups/{ipGroupId}` Deletes a source IP group based on the specified ID.
    - Added `GET /ipDestinationGroups` Retrieves the list of destination IP groups.
    - Added `GET /ipDestinationGroups/lite` Retrieves the list of destination IP groups. This request retrieves basic information about the destination IP groups, ID, name, and type. For extensive details, use the GET /ipDestinationGroups request.
    - Added `POST /ipDestinationGroups` Adds a new custom destination IP group.
    - Added `DELETE /ipDestinationGroups/{ipGroupId}` Deletes the destination IP group based on the specified ID. Default destination groups that are automatically created cannot be deleted.
    - Added `GET /ipGroups` Retrieves the list of IP pools.
    - Added `GET /ipGroups/lite` Retrieves the list of IP pools. This request retrieves basic information about the IP pools, such as name and ID. For extensive details, use the GET /ipGroups request.
    - Added `POST /ipGroups` Adds a new custom IP pool.
    - Added `DELETE /ipGroups/{ipGroupId}` Deletes an IP pool based on the specified ID.
    - Added `GET /networkServices` Retrieves the list of all network services. The search parameters find matching values within the name or description attributes.
    - Added `POST /networkServices` Creates a new network service.
    - Added `PUT /networkServices/{serviceId}` Updates the network service information for the specified service ID.
    - Added `DELETE /networkServices/{serviceId}` Deletes the network service for the specified ID.
    - Added `GET /networkServicesGroups` Retrieves the list of network service groups.
    - Added `GET /zpaResources/applicationSegments` Retrieves the list of ZPA application segments that can be configured in traffic forwarding rule criteria.

1.0.1 (April, 22 2025) - BREAKING CHANGES
-----------------------------------------

Notes
-----

- Python Versions: **v3.8, v3.9, v3.10, v3.11**


Zscaler OneAPI Support
-----------------------

(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_): Added support for (`OneAPI <https://help.zscaler.com/zidentity/what-zidentity>`_) Oauth2 authentication support through (`Zidentity <https://help.zscaler.com/zidentity/what-zidentity>`_)

**NOTES**
  - Starting at v1.0.0 version this SDK provides dual API client functionality and is backwards compatible with the legacy Zscaler API framework.
  - The new OneAPI framework is compatible only with the following products `ZCC/ZIA/ZPA`.
  - The following products `ZTW` - Cloud Connector and `ZDX` and Zscaler Digital Experience, authentication methods remain unnaffected.
  - The package `ZCON` (Zscaler Cloud and Branch Connector) has been renamed to `ZTW`
  - The following products `ZWA` - Zscaler Workflow Automation authentication methods remain unnaffected.

Refer to the (`README <hhttps://github.com/zscaler/zscaler-sdk-python/blob/master/README.md>`_) page for details on client instantiation, and authentication requirements on each individual product.

**WARNING**: Attention Government customers. OneAPI and Zidentity is not currently supported for the following ZIA clouds: `zscalergov` and `zscalerten` or ZPA `GOV`, and `GOVUS`. 
See the Zscaler Legacy API Framework section in the (`README Docs <https://zscaler-sdk-python.readthedocs.io/en/latest/index.html>`_) for more information on how authenticate to these environments using the built-in Legacy API method.

(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_): All API clients now support Config Setter object `ZCC/ZTW/ZDX/ZIA/ZPA/ZWA`

ZCC New Endpoints
^^^^^^^^^^^^^^^^^

(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Added the following new ZCC API Endpoints:
  - Added `GET /downloadServiceStatus` to download service status for all devices.
  - Added `GET /getDeviceCleanupInfo` to retrieve device cleanup information.
  - Added `PUT /setDeviceCleanupInfo` to cleanup device information.
  - Added `GET /getDeviceDetails` to retrieve device detailed information.
  - Added `GET /getAdminUsers` to retrieve mobile portal admin user.
  - Added `PUT /editAdminUser` to update mobile portal admin user.
  - Added `GET /getAdminUsersSyncInfo` to retrieve mobile portal admin user sync information.
  - Added `POST /syncZiaZdxAdminUsers` to retrieve mobile portal admin users ZIA and ZDX sync information.
  - Added `POST /syncZpaAdminUsers` to retrieve mobile portal admin users ZPA sync information.
  - Added `GET /getAdminRoles` to retrieve mobile portal admin roles.
  - Added `GET /getCompanyInfo` to retrieve company information.
  - Added `GET /getZdxGroupEntitlements` to retrieve ZDX Group entitlement enablement.
  - Added `PUT /updateZdxGroupEntitlement` to retrieve ZDX Group entitlement enablement.
  - Added `GET /updateZpaGroupEntitlement` to retrieve ZPA Group entitlement enablement.
  - Added `GET /web/policy/listByCompany` to retrieve Web Policy By Company ID.
  - Added `PUT /web/policy/activate` to activate mobile portal web policy
  - Added `PUT /web/policy/edit` to update mobile portal web policy
  - Added `DELETE /web/policy/{policyId}/delete` to delete mobile portal web policy.
  - Added `GET /webAppService/listByCompany` to retrieve Web App Service information By Company ID.
  - Added `GET /webFailOpenPolicy/listByCompany` to retrieve web Fail Open Policy information By Company ID.
  - Added `PUT /webFailOpenPolicy/edit` to update mobile portal web Fail Open Policy.
  - Added `GET /webForwardingProfile/listByCompany` to retrieve Web Forwarding Profile information By Company ID.
  - Added `POST /webForwardingProfile/edit` to create a Web Forwarding Profile.
  - Added `DELETE /webForwardingProfile/{profileId}/delete` to delete Web Forwarding Profile.
  - Added `GET /webTrustedNetwork/listByCompany` to retrieve multiple Web Trusted Network information By Company ID.
  - Added `POST /webTrustedNetwork/edit` to create Web Trusted Network resource.
  - Added `PUT /webTrustedNetwork/edit` to update Web Trusted Network resource.
  - Added `DELETE /webTrustedNetwork/{networkId}/delete` to delete Web Trusted Network resource.
  - Added `GET /getWebPrivacyInfo` to retrieve Web Privacy Info.
  - Added `GET /setWebPrivacyInfo` to update Web Privacy Info.

ZIA Sandbox Submission - BREAKING CHANGES
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Authentication to Zscaler Sandbox now use the following attributes during client instantiation.
 - `sandboxToken` - Can also be sourced from the `ZSCALER_SANDBOX_TOKEN` environment variable.
 - `sandboxCloud` - Can also be sourced from the `ZSCALER_SANDBOX_CLOUD` environment variable.

**NOTE** The previous `ZIA_SANDBOX_TOKEN` has been deprecated.

ZIA Sandbox Rules
^^^^^^^^^^^^^^^^^^

(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /sandboxRules` to retrieve the list of all Sandbox policy rules.
  - Added `GET /sandboxRules/{ruleId}` to retrieve the Sandbox policy rule information based on the specified ID.
  - Added `POST /sandboxRules` to add a Sandbox policy rule.
  - Added `PUT /sandboxRules/{ruleId}` to update the Sandbox policy rule configuration for the specified ID.
  - Added `DELETE /sandboxRules/{ruleId}` to delete the Sandbox policy rule based on the specified ID.

ZIA DNS Control Rules
^^^^^^^^^^^^^^^^^^^^^^

(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /firewallDnsRules` to retrieve the list of all DNS Control policy rules.
  - Added `GET /firewallDnsRules/{ruleId}` to retrieve the DNS Control policy rule information based on the specified ID.
  - Added `POST /firewallDnsRules` to add a DNS Control policy rules.
  - Added `PUT /firewallDnsRules/{ruleId}` to update the DNS Control policy rule configuration for the specified ID.
  - Added `DELETE /firewallDnsRules/{ruleId}` to delete the DNS Control policy rule based on the specified ID.

ZIA IPS Control Rules
^^^^^^^^^^^^^^^^^^^^^

(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /firewallIpsRules` to retrieve the list of all IPS Control policy rules.
  - Added `GET /firewallIpsRules/{ruleId}` to retrieve the IPS Control policy rule information based on the specified ID.
  - Added `POST /firewallIpsRules` to add a IPS Control policy rule.
  - Added `PUT /firewallIpsRules/{ruleId}` to update the IPS Control policy rule configuration for the specified ID.
  - Added `DELETE /firewallIpsRules/{ruleId}` to delete the IPS Control policy rule based on the specified ID.

ZIA File Type Control Policy
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /fileTypeRules` to retrieve the list of all File Type Control policy rules.
  - Added `GET /fileTypeRules/lite` to retrieve the list of all File Type Control policy rules.
  - Added `GET /fileTypeRules/{ruleId}` to retrieve the File Type Control policy rule information based on the specified ID.
  - Added `POST /fileTypeRules` to add a File Type Control policy rule.
  - Added `PUT /fileTypeRules/{ruleId}` to update the File Type Control policy rule configuration for the specified ID.
  - Added `DELETE /fileTypeRules/{ruleId}` to delete the File Type Control policy rule based on the specified ID.

ZIA Forwarding Control Policy - Proxy Gateways
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /proxyGateways` to retrieve the proxy gateway information.
  - Added `GET /proxyGateways/lite` to retrieve the name and ID of the proxy.

ZIA Cloud Nanolog Streaming Service (NSS)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /nssFeeds` to retrieve the cloud NSS feeds.
  - Added `GET /nssFeeds/{feedId}` to retrieve information about cloud NSS feed based on the specified ID.
  - Added `POST /nssFeeds` to add a new cloud NSS feed.
  - Added `PUT /nssFeeds/{feedId}` to update cloud NSS feed configuration based on the specified ID.
  - Added `DELETE /nssFeeds/{feedId}` to delete cloud NSS feed configuration based on the specified ID.
  - Added `GET /nssFeeds/feedOutputDefaults` to retrieve the default cloud NSS feed output format for different log types.
  - Added `GET /nssFeeds/testConnectivity/{feedId}` to test the connectivity of cloud NSS feed based on the specified ID
  - Added `POST /nssFeeds/validateFeedFormat` to validates the cloud NSS feed format and returns the validation result

ZIA Advanced Threat Protection Policy
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /cyberThreatProtection/advancedThreatSettings` to retrieve the advanced threat configuration settings.
  - Added `PUT /cyberThreatProtection/advancedThreatSettings` to update the advanced threat configuration settings.
  - Added `GET /cyberThreatProtection/maliciousUrls` to retrieve the malicious URLs added to the denylist in the Advanced Threat Protection (ATP) policy
  - Added `PUT /cyberThreatProtection/maliciousUrls` to updates the malicious URLs added to the denylist in ATP policy
  - Added `GET /cyberThreatProtection/securityExceptions` to retrieves information about the security exceptions configured for the ATP policy
  - Added `PUT /cyberThreatProtection/securityExceptions` to update security exceptions for the ATP policy

ZIA Advanced Threat Protection Policy
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /cyberThreatProtection/atpMalwareInspection` to retrieve the traffic inspection configurations of Malware Protection policy
  - Added `PUT /cyberThreatProtection/atpMalwareInspection` to update the traffic inspection configurations of Malware Protection policy.
  - Added `GET /cyberThreatProtection/atpMalwareProtocols` to retrieve the protocol inspection configurations of Malware Protection policy
  - Added `PUT /cyberThreatProtection/atpMalwareProtocols` to update the protocol inspection configurations of Malware Protection policy.
  - Added `GET /cyberThreatProtection/malwareSettings` to retrieve the malware protection policy configuration details
  - Added `PUT /cyberThreatProtection/malwareSettings` to update the malware protection policy configuration details.
  - Added `GET /cyberThreatProtection/malwarePolicy` to retrieve information about the security exceptions configured for the Malware Protection policy
  - Added `PUT /cyberThreatProtection/malwarePolicy` to update security exceptions for the Malware Protection policy.

ZIA URL & Cloud App Control Policy Settings
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /advancedUrlFilterAndCloudAppSettings` to retrieve information about URL and Cloud App Control advanced policy settings
  - Added `PUT /advancedUrlFilterAndCloudAppSettings` to update the URL and Cloud App Control advanced policy settings

ZIA Authentication Settings
^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /authSettings` to retrieve the organization's default authentication settings information, including authentication profile and Kerberos authentication information.
  - Added `GET /authSettings/lite` to retrieve organization's default authentication settings information.
  - Added `PUT /authSettings` to update the organization's default authentication settings information.

ZIA Advanced Settings
^^^^^^^^^^^^^^^^^^^^^

(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /advancedSettings` to retrieve information about the advanced settings.
  - Added `PUT /advancedSettings` to update the advanced settings configuration.

ZIA Cloud Applications
^^^^^^^^^^^^^^^^^^^^^^^

(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /cloudApplications/policy` Retrieves a list of Predefined and User Defined Cloud Applications associated with the DLP rules, Cloud App Control rules, Advanced Settings, Bandwidth Classes, and File Type Control rules.
  - Added `GET /cloudApplications/sslPolicy` Retrieves a list of Predefined and User Defined Cloud Applications associated with the SSL Inspection rules.

ZIA Shadow IT Report
^^^^^^^^^^^^^^^^^^^^

(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Added the following new ZIA API Endpoints:
- Added `PUT /cloudApplications/bulkUpdate` To Update application status and tag information for predefined or custom cloud applications based on the IDs specified
- Added `GET /cloudApplications/lite` Gets the list of predefined and custom cloud applications
- Added `GET /customTags` Gets the list of custom tags available to assign to cloud applications
- Added `POST /shadowIT/applications/export` Export the Shadow IT Report (in CSV format) for the cloud applications recognized by Zscaler based on their usage in your organization.
- Added `POST /shadowIT/applications/{entity}/exportCsv` Export the Shadow IT Report (in CSV format) for the list of users or known locations identified with using the cloud applications specified in the request.

ZIA Remote Assistance Support
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /remoteAssistance` to retrieve information about the Remote Assistance option.
  - Added `PUT /remoteAssistance` to update information about the Remote Assistance option. Using this option, you can allow Zscaler Support to access your organization’s ZIA Admin Portal for a specified time period to troubleshoot issues.

ZIA Organization Details
^^^^^^^^^^^^^^^^^^^^^^^^^

(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /orgInformation` to retrieve detailed organization information, including headquarter location, geolocation, address, and contact details.
  - Added `GET /orgInformation/lite` to retrieve minimal organization information.
  - Added `GET /subscriptions` to retrieve information about the list of subscriptions enabled for your tenant. Subscriptions define the various features and levels of functionality that are available to your organization.

ZIA End User Notification
^^^^^^^^^^^^^^^^^^^^^^^^^^
(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /eun` to retrieve information browser-based end user notification (EUN) configuration details.
  - Added `PUT /eun` to update the browser-based end user notification (EUN) configuration details.

ZIA Admin Audit Logs
^^^^^^^^^^^^^^^^^^^^^^^

(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /auditlogEntryReport` to retrieve the status of a request for an audit log report.
  - Added `POST /auditlogEntryReport` to create an audit log report for the specified time period and saves it as a CSV file.
  - Added `DELETE /auditlogEntryReport` to cancel the request to create an audit log report.
  - Added `GET /auditlogEntryReport/download` to download the most recently created audit log report.

ZIA Extranets
^^^^^^^^^^^^^^^^^^

(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /extranet` to retrieve the list of extranets configured for the organization
  - Added `GET /extranet/lite` Retrieves the name-ID pairs of all extranets configured for an organization
  - Added `GET /extranet/{Id}` Retrieves information about an extranet based on the specified ID.
  - Added `POST /extranet` Adds a new extranet for the organization.
  - Added `PUT /extranet/{Id}` Updates an extranet based on the specified ID
  - Added `DELETE /extranet/{Id}` Deletes an extranet based on the specified ID

ZIA IOT Endpoint
^^^^^^^^^^^^^^^^^^

(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Added the following new ZIA IOT API Endpoints:
  - Added `GET /iotDiscovery/deviceTypes` Retrieve the mapping between device type universally unique identifier (UUID) values and the device type names for all the device types supported by the Zscaler AI/ML.
  - Added `GET /iotDiscovery/categories` Retrieve the mapping between the device category universally unique identifier (UUID) values and the category names for all the device categories supported by the Zscaler AI/ML. The parent of device category is device type.
  - Added `GET /iotDiscovery/classifications` Retrieve the mapping between the device classification universally unique identifier (UUID) values and the classification names for all the device classifications supported by Zscaler AI/ML. The parent of device classification is device category.
  - Added `GET /iotDiscovery/deviceList` Retrieve a list of discovered devices with the following key contexts, IP address, location, ML auto-label, classification, category, and type.

ZIA 3rd-Party App Governance
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /apps/app` to search the 3rd-Party App Governance App Catalog by either app ID or URL.
  - Added `POST /apps/app` to submis an app for analysis in the 3rd-Party App Governance Sandbox.
  - Added `GET /apps/search` to search for an app by name. Any app whose name contains the search term (appName) is returned.
  - Added `GET /app_views/list` to retrieve the list of custom views that you have configured in the 3rd-Party App Governance.
  - Added `GET /app_views/{appViewId}/apps` to retrieves all assets (i.e., apps) that are related to a specified argument (i.e., custom view).

ZIA Admin Role Endpoints
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Added the following new ZIA API Endpoints:
    - Added `GET /adminRoles/{roleId}` Retrieves the admin role based on the specified ID
    - Added `GET /adminRoles/lite` Retrieves a name and ID dictionary of all admin roles. The list only includes the name and ID for all admin roles.
    - Added `POST /adminRoles` Adds an admin role.
    - Added `PUT /adminRoles/{roleId}` Updates the admin role based on the specified ID.
    - Added `DELETE /adminRoles/{roleId}` Deletes the admin role based on the specified ID.

ZPA Credential Pool (New)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Added new ZPA endpoint:
  - Added `GET /credential-pool` Gets the privileged credential pool details for the specified customer.
  - Added `GET /credential-pool/{id}` Gets the privileged credential pool details for the specified customer.
  - Added `GET /credential-pool/{id}/credential` Given Privileged credential pool id gets mapped privileged credential info
  - Added `POST /credential-pool` Adds a new privileged credential pool for the specified customer.
  - Added `PUT /credential-pool/{id}` Updates the existing credential pool for the specified customer.
  - Added `DELETE /credential-pool/{id}` Updates the existing credential pool for the specified customer.

ZWA - Zscaler Workflow Automation (NEW)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Added new ZWA endpoint:
  - Added `GET /dlp/v1/incidents/transactions/{transactionId}` Gets the list of all DLP incidents associated with the transaction ID
  - Added `GET /dlp/v1/incidents/{dlpIncidentId}` Gets the DLP incident details based on the incident ID.
  - Added `DELETE /dlp/v1/incidents/{dlpIncidentId}` Deletes the DLP incident for the specified incident ID.
  - Added `GET /dlp/v1/incidents{dlpIncidentId}/change-history` Gets the details of updates made to an incident based on the given ID and timeline.
  - Added `GET /dlp/v1/incidents/{dlpIncidentId}/tickets` Gets the information of the ticket generated for the incident. For example, ticket type, ticket ID, ticket status, etc.
  - Added `POST /dlp/v1/incidents/{dlpIncidentId}/incident-groups/search` Filters a list of DLP incident groups to which the specified incident ID belongs.
  - Added `POST /dlp/v1/incidents/{dlpIncidentId}/close` Updates the status of the incident to resolved and closes the incident with a resolution label and a resolution code.
  - Added `POST /dlp/v1/incidents/{dlpIncidentId}/notes` Adds notes to the incident during updates or status changes.
  - Added `POST /dlp/v1/incidents/{dlpIncidentId}/labels` Assign lables (a label name and it's associated value) to DLP incidents.
  - Added `POST /dlp/v1/incidents/search` Filters DLP incidents based on the given time range and the field values.
  - Added `GET /dlp/v1/incidents/{dlpIncidentId}/triggers` Downloads the actual data that triggered the incident.
  - Added `GET /dlp/v1/incidents/{dlpIncidentId}/evidence` Gets the evidence URL of the incident.

Cloud & Branch Connector - OneAPI Support
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Cloud & Branch Connector package is now compatible with OneAPI and Legacy API framework. Please refer to README for details.
(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Cloud & Branch Connector package has been renamed from `zcon` to `ztw`

ZTW Policy Management
^^^^^^^^^^^^^^^^^^^^^^^

(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Added the following new ZTW API Endpoints:
    - Added `GET /ecRules/ecRdr` Retrieves the list of traffic forwarding rules.
    - Added `PUT /ecRules/ecRdr/{ruleId}` Updates a traffic forwarding rule configuration based on the specified ID.
    - Added `POST /ecRules/ecRdr` Creates a new traffic forwarding rule.
    - Added `GET /ecRules/ecRdr/count` Retrieves the count of traffic forwarding rules available in the Cloud & Branch Connector Admin Portal.

ZTW Policy Resources
^^^^^^^^^^^^^^^^^^^^^

(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Added the following new ZTW API Endpoints:
    - Added `GET /ipSourceGroups` Retrieves the list of source IP groups.
    - Added `GET /ipSourceGroups/lite` Retrieves the list of source IP groups. This request retrieves basic information about the source IP groups, such as name and ID. For extensive details, use the GET /ipSourceGroups request.
    - Added `POST /ipSourceGroups` Adds a new custom source IP group.
    - Added `DELETE /ipSourceGroups/{ipGroupId}` Deletes a source IP group based on the specified ID.
    - Added `GET /ipDestinationGroups` Retrieves the list of destination IP groups.
    - Added `GET /ipDestinationGroups/lite` Retrieves the list of destination IP groups. This request retrieves basic information about the destination IP groups, ID, name, and type. For extensive details, use the GET /ipDestinationGroups request.
    - Added `POST /ipDestinationGroups` Adds a new custom destination IP group.
    - Added `DELETE /ipDestinationGroups/{ipGroupId}` Deletes the destination IP group based on the specified ID. Default destination groups that are automatically created cannot be deleted.
    - Added `GET /ipGroups` Retrieves the list of IP pools.
    - Added `GET /ipGroups/lite` Retrieves the list of IP pools. This request retrieves basic information about the IP pools, such as name and ID. For extensive details, use the GET /ipGroups request.
    - Added `POST /ipGroups` Adds a new custom IP pool.
    - Added `DELETE /ipGroups/{ipGroupId}` Deletes an IP pool based on the specified ID.
    - Added `GET /networkServices` Retrieves the list of all network services. The search parameters find matching values within the name or description attributes.
    - Added `POST /networkServices` Creates a new network service.
    - Added `PUT /networkServices/{serviceId}` Updates the network service information for the specified service ID.
    - Added `DELETE /networkServices/{serviceId}` Deletes the network service for the specified ID.
    - Added `GET /networkServicesGroups` Retrieves the list of network service groups.
    - Added `GET /zpaResources/applicationSegments` Retrieves the list of ZPA application segments that can be configured in traffic forwarding rule criteria.

1.0.1 (April, 22 2025) - BREAKING CHANGES
-----------------------------------------

Notes
-----

- Python Versions: **v3.8, v3.9, v3.10, v3.11**


Zscaler OneAPI Support
-----------------------

(`#259 <https://github.com/zscaler/zscaler-sdk-python/pull/259>`_): Added support for (`OneAPI <https://help.zscaler.com/zidentity/what-zidentity>`_) Oauth2 authentication support through (`Zidentity <https://help.zscaler.com/zidentity/what-zidentity>`_)

**NOTES**
  - Starting at v1.0.0 version this SDK provides dual API client functionality and is backwards compatible with the legacy Zscaler API framework.
  - The new OneAPI framework is compatible only with the following products `ZCC/ZIA/ZPA`.
  - The following products `ZTW` - Cloud Connector and `ZDX` and Zscaler Digital Experience, authentication methods remain unnaffected.
  - The package `ZCON` (Zscaler Cloud and Branch Connector) has been renamed to `ZTW`
  - The following products `ZWA` - Zscaler Workflow Automation authentication methods remain unnaffected.

Refer to the (`README <hhttps://github.com/zscaler/zscaler-sdk-python/blob/master/README.md>`_) page for details on client instantiation, and authentication requirements on each individual product.

**WARNING**: Attention Government customers. OneAPI and Zidentity is not currently supported for the following ZIA clouds: `zscalergov` and `zscalerten` or ZPA `GOV`, and `GOVUS`. 
See the Zscaler Legacy API Framework section in the (`README Docs <https://zscaler-sdk-python.readthedocs.io/en/latest/index.html>`_) for more information on how authenticate to these environments using the built-in Legacy API method.

(`#259 <https://github.com/zscaler/zscaler-sdk-python/pull/259>`_): All API clients now support Config Setter object `ZCC/ZTW/ZDX/ZIA/ZPA/ZWA`

ZCC New Endpoints
^^^^^^^^^^^^^^^^^

(`#259 <https://github.com/zscaler/zscaler-sdk-python/pull/259>`_) - Added the following new ZCC API Endpoints:
  - Added `GET /downloadServiceStatus` to download service status for all devices.
  - Added `GET /getDeviceCleanupInfo` to retrieve device cleanup information.
  - Added `PUT /setDeviceCleanupInfo` to cleanup device information.
  - Added `GET /getDeviceDetails` to retrieve device detailed information.
  - Added `GET /getAdminUsers` to retrieve mobile portal admin user.
  - Added `PUT /editAdminUser` to update mobile portal admin user.
  - Added `GET /getAdminUsersSyncInfo` to retrieve mobile portal admin user sync information.
  - Added `POST /syncZiaZdxAdminUsers` to retrieve mobile portal admin users ZIA and ZDX sync information.
  - Added `POST /syncZpaAdminUsers` to retrieve mobile portal admin users ZPA sync information.
  - Added `GET /getAdminRoles` to retrieve mobile portal admin roles.
  - Added `GET /getCompanyInfo` to retrieve company information.
  - Added `GET /getZdxGroupEntitlements` to retrieve ZDX Group entitlement enablement.
  - Added `PUT /updateZdxGroupEntitlement` to retrieve ZDX Group entitlement enablement.
  - Added `GET /updateZpaGroupEntitlement` to retrieve ZPA Group entitlement enablement.
  - Added `GET /web/policy/listByCompany` to retrieve Web Policy By Company ID.
  - Added `PUT /web/policy/activate` to activate mobile portal web policy
  - Added `PUT /web/policy/edit` to update mobile portal web policy
  - Added `DELETE /web/policy/{policyId}/delete` to delete mobile portal web policy.
  - Added `GET /webAppService/listByCompany` to retrieve Web App Service information By Company ID.
  - Added `GET /webFailOpenPolicy/listByCompany` to retrieve web Fail Open Policy information By Company ID.
  - Added `PUT /webFailOpenPolicy/edit` to update mobile portal web Fail Open Policy.
  - Added `GET /webForwardingProfile/listByCompany` to retrieve Web Forwarding Profile information By Company ID.
  - Added `POST /webForwardingProfile/edit` to create a Web Forwarding Profile.
  - Added `DELETE /webForwardingProfile/{profileId}/delete` to delete Web Forwarding Profile.
  - Added `GET /webTrustedNetwork/listByCompany` to retrieve multiple Web Trusted Network information By Company ID.
  - Added `POST /webTrustedNetwork/edit` to create Web Trusted Network resource.
  - Added `PUT /webTrustedNetwork/edit` to update Web Trusted Network resource.
  - Added `DELETE /webTrustedNetwork/{networkId}/delete` to delete Web Trusted Network resource.
  - Added `GET /getWebPrivacyInfo` to retrieve Web Privacy Info.
  - Added `GET /setWebPrivacyInfo` to update Web Privacy Info.

ZIA Sandbox Submission - BREAKING CHANGES
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#259 <https://github.com/zscaler/zscaler-sdk-python/pull/259>`_) - Authentication to Zscaler Sandbox now use the following attributes during client instantiation.
 - `sandboxToken` - Can also be sourced from the `ZSCALER_SANDBOX_TOKEN` environment variable.
 - `sandboxCloud` - Can also be sourced from the `ZSCALER_SANDBOX_CLOUD` environment variable.

**NOTE** The previous `ZIA_SANDBOX_TOKEN` has been deprecated.

ZIA Sandbox Rules
^^^^^^^^^^^^^^^^^^

(`#259 <https://github.com/zscaler/zscaler-sdk-python/pull/259>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /sandboxRules` to retrieve the list of all Sandbox policy rules.
  - Added `GET /sandboxRules/{ruleId}` to retrieve the Sandbox policy rule information based on the specified ID.
  - Added `POST /sandboxRules` to add a Sandbox policy rule.
  - Added `PUT /sandboxRules/{ruleId}` to update the Sandbox policy rule configuration for the specified ID.
  - Added `DELETE /sandboxRules/{ruleId}` to delete the Sandbox policy rule based on the specified ID.

ZIA DNS Control Rules
^^^^^^^^^^^^^^^^^^^^^^

(`#259 <https://github.com/zscaler/zscaler-sdk-python/pull/259>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /firewallDnsRules` to retrieve the list of all DNS Control policy rules.
  - Added `GET /firewallDnsRules/{ruleId}` to retrieve the DNS Control policy rule information based on the specified ID.
  - Added `POST /firewallDnsRules` to add a DNS Control policy rules.
  - Added `PUT /firewallDnsRules/{ruleId}` to update the DNS Control policy rule configuration for the specified ID.
  - Added `DELETE /firewallDnsRules/{ruleId}` to delete the DNS Control policy rule based on the specified ID.

ZIA IPS Control Rules
^^^^^^^^^^^^^^^^^^^^^

(`#259 <https://github.com/zscaler/zscaler-sdk-python/pull/259>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /firewallIpsRules` to retrieve the list of all IPS Control policy rules.
  - Added `GET /firewallIpsRules/{ruleId}` to retrieve the IPS Control policy rule information based on the specified ID.
  - Added `POST /firewallIpsRules` to add a IPS Control policy rule.
  - Added `PUT /firewallIpsRules/{ruleId}` to update the IPS Control policy rule configuration for the specified ID.
  - Added `DELETE /firewallIpsRules/{ruleId}` to delete the IPS Control policy rule based on the specified ID.

ZIA File Type Control Policy
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#259 <https://github.com/zscaler/zscaler-sdk-python/pull/259>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /fileTypeRules` to retrieve the list of all File Type Control policy rules.
  - Added `GET /fileTypeRules/lite` to retrieve the list of all File Type Control policy rules.
  - Added `GET /fileTypeRules/{ruleId}` to retrieve the File Type Control policy rule information based on the specified ID.
  - Added `POST /fileTypeRules` to add a File Type Control policy rule.
  - Added `PUT /fileTypeRules/{ruleId}` to update the File Type Control policy rule configuration for the specified ID.
  - Added `DELETE /fileTypeRules/{ruleId}` to delete the File Type Control policy rule based on the specified ID.

ZIA Forwarding Control Policy - Proxy Gateways
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#259 <https://github.com/zscaler/zscaler-sdk-python/pull/259>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /proxyGateways` to retrieve the proxy gateway information.
  - Added `GET /proxyGateways/lite` to retrieve the name and ID of the proxy.

ZIA Cloud Nanolog Streaming Service (NSS)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#259 <https://github.com/zscaler/zscaler-sdk-python/pull/259>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /nssFeeds` to retrieve the cloud NSS feeds.
  - Added `GET /nssFeeds/{feedId}` to retrieve information about cloud NSS feed based on the specified ID.
  - Added `POST /nssFeeds` to add a new cloud NSS feed.
  - Added `PUT /nssFeeds/{feedId}` to update cloud NSS feed configuration based on the specified ID.
  - Added `DELETE /nssFeeds/{feedId}` to delete cloud NSS feed configuration based on the specified ID.
  - Added `GET /nssFeeds/feedOutputDefaults` to retrieve the default cloud NSS feed output format for different log types.
  - Added `GET /nssFeeds/testConnectivity/{feedId}` to test the connectivity of cloud NSS feed based on the specified ID
  - Added `POST /nssFeeds/validateFeedFormat` to validates the cloud NSS feed format and returns the validation result

ZIA Advanced Threat Protection Policy
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#259 <https://github.com/zscaler/zscaler-sdk-python/pull/259>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /cyberThreatProtection/advancedThreatSettings` to retrieve the advanced threat configuration settings.
  - Added `PUT /cyberThreatProtection/advancedThreatSettings` to update the advanced threat configuration settings.
  - Added `GET /cyberThreatProtection/maliciousUrls` to retrieve the malicious URLs added to the denylist in the Advanced Threat Protection (ATP) policy
  - Added `PUT /cyberThreatProtection/maliciousUrls` to updates the malicious URLs added to the denylist in ATP policy
  - Added `GET /cyberThreatProtection/securityExceptions` to retrieves information about the security exceptions configured for the ATP policy
  - Added `PUT /cyberThreatProtection/securityExceptions` to update security exceptions for the ATP policy

ZIA Advanced Threat Protection Policy
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#259 <https://github.com/zscaler/zscaler-sdk-python/pull/259>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /cyberThreatProtection/atpMalwareInspection` to retrieve the traffic inspection configurations of Malware Protection policy
  - Added `PUT /cyberThreatProtection/atpMalwareInspection` to update the traffic inspection configurations of Malware Protection policy.
  - Added `GET /cyberThreatProtection/atpMalwareProtocols` to retrieve the protocol inspection configurations of Malware Protection policy
  - Added `PUT /cyberThreatProtection/atpMalwareProtocols` to update the protocol inspection configurations of Malware Protection policy.
  - Added `GET /cyberThreatProtection/malwareSettings` to retrieve the malware protection policy configuration details
  - Added `PUT /cyberThreatProtection/malwareSettings` to update the malware protection policy configuration details.
  - Added `GET /cyberThreatProtection/malwarePolicy` to retrieve information about the security exceptions configured for the Malware Protection policy
  - Added `PUT /cyberThreatProtection/malwarePolicy` to update security exceptions for the Malware Protection policy.

ZIA URL & Cloud App Control Policy Settings
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#259 <https://github.com/zscaler/zscaler-sdk-python/pull/259>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /advancedUrlFilterAndCloudAppSettings` to retrieve information about URL and Cloud App Control advanced policy settings
  - Added `PUT /advancedUrlFilterAndCloudAppSettings` to update the URL and Cloud App Control advanced policy settings

ZIA Authentication Settings
^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#259 <https://github.com/zscaler/zscaler-sdk-python/pull/259>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /authSettings` to retrieve the organization's default authentication settings information, including authentication profile and Kerberos authentication information.
  - Added `GET /authSettings/lite` to retrieve organization's default authentication settings information.
  - Added `PUT /authSettings` to update the organization's default authentication settings information.

ZIA Advanced Settings
^^^^^^^^^^^^^^^^^^^^^

(`#259 <https://github.com/zscaler/zscaler-sdk-python/pull/259>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /advancedSettings` to retrieve information about the advanced settings.
  - Added `PUT /advancedSettings` to update the advanced settings configuration.

ZIA Cloud Applications
^^^^^^^^^^^^^^^^^^^^^^^

(`#259 <https://github.com/zscaler/zscaler-sdk-python/pull/259>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /cloudApplications/policy` Retrieves a list of Predefined and User Defined Cloud Applications associated with the DLP rules, Cloud App Control rules, Advanced Settings, Bandwidth Classes, and File Type Control rules.
  - Added `GET /cloudApplications/sslPolicy` Retrieves a list of Predefined and User Defined Cloud Applications associated with the SSL Inspection rules.

ZIA Shadow IT Report
^^^^^^^^^^^^^^^^^^^^

(`#259 <https://github.com/zscaler/zscaler-sdk-python/pull/259>`_) - Added the following new ZIA API Endpoints:
- Added `PUT /cloudApplications/bulkUpdate` To Update application status and tag information for predefined or custom cloud applications based on the IDs specified
- Added `GET /cloudApplications/lite` Gets the list of predefined and custom cloud applications
- Added `GET /customTags` Gets the list of custom tags available to assign to cloud applications
- Added `POST /shadowIT/applications/export` Export the Shadow IT Report (in CSV format) for the cloud applications recognized by Zscaler based on their usage in your organization.
- Added `POST /shadowIT/applications/{entity}/exportCsv` Export the Shadow IT Report (in CSV format) for the list of users or known locations identified with using the cloud applications specified in the request.

ZIA Remote Assistance Support
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#259 <https://github.com/zscaler/zscaler-sdk-python/pull/259>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /remoteAssistance` to retrieve information about the Remote Assistance option.
  - Added `PUT /remoteAssistance` to update information about the Remote Assistance option. Using this option, you can allow Zscaler Support to access your organization’s ZIA Admin Portal for a specified time period to troubleshoot issues.

ZIA Organization Details
^^^^^^^^^^^^^^^^^^^^^^^^^

(`#259 <https://github.com/zscaler/zscaler-sdk-python/pull/259>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /orgInformation` to retrieve detailed organization information, including headquarter location, geolocation, address, and contact details.
  - Added `GET /orgInformation/lite` to retrieve minimal organization information.
  - Added `GET /subscriptions` to retrieve information about the list of subscriptions enabled for your tenant. Subscriptions define the various features and levels of functionality that are available to your organization.

ZIA End User Notification
^^^^^^^^^^^^^^^^^^^^^^^^^^
(`#259 <https://github.com/zscaler/zscaler-sdk-python/pull/259>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /eun` to retrieve information browser-based end user notification (EUN) configuration details.
  - Added `PUT /eun` to update the browser-based end user notification (EUN) configuration details.

ZIA Admin Audit Logs
^^^^^^^^^^^^^^^^^^^^^^^

(`#259 <https://github.com/zscaler/zscaler-sdk-python/pull/259>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /auditlogEntryReport` to retrieve the status of a request for an audit log report.
  - Added `POST /auditlogEntryReport` to create an audit log report for the specified time period and saves it as a CSV file.
  - Added `DELETE /auditlogEntryReport` to cancel the request to create an audit log report.
  - Added `GET /auditlogEntryReport/download` to download the most recently created audit log report.

ZIA Extranets
^^^^^^^^^^^^^^^^^^

(`#259 <https://github.com/zscaler/zscaler-sdk-python/pull/259>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /extranet` to retrieve the list of extranets configured for the organization
  - Added `GET /extranet/lite` Retrieves the name-ID pairs of all extranets configured for an organization
  - Added `GET /extranet/{Id}` Retrieves information about an extranet based on the specified ID.
  - Added `POST /extranet` Adds a new extranet for the organization.
  - Added `PUT /extranet/{Id}` Updates an extranet based on the specified ID
  - Added `DELETE /extranet/{Id}` Deletes an extranet based on the specified ID

ZIA IOT Endpoint
^^^^^^^^^^^^^^^^^^

(`#259 <https://github.com/zscaler/zscaler-sdk-python/pull/259>`_) - Added the following new ZIA IOT API Endpoints:
  - Added `GET /iotDiscovery/deviceTypes` Retrieve the mapping between device type universally unique identifier (UUID) values and the device type names for all the device types supported by the Zscaler AI/ML.
  - Added `GET /iotDiscovery/categories` Retrieve the mapping between the device category universally unique identifier (UUID) values and the category names for all the device categories supported by the Zscaler AI/ML. The parent of device category is device type.
  - Added `GET /iotDiscovery/classifications` Retrieve the mapping between the device classification universally unique identifier (UUID) values and the classification names for all the device classifications supported by Zscaler AI/ML. The parent of device classification is device category.
  - Added `GET /iotDiscovery/deviceList` Retrieve a list of discovered devices with the following key contexts, IP address, location, ML auto-label, classification, category, and type.

ZIA 3rd-Party App Governance
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#259 <https://github.com/zscaler/zscaler-sdk-python/pull/259>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /apps/app` to search the 3rd-Party App Governance App Catalog by either app ID or URL.
  - Added `POST /apps/app` to submis an app for analysis in the 3rd-Party App Governance Sandbox.
  - Added `GET /apps/search` to search for an app by name. Any app whose name contains the search term (appName) is returned.
  - Added `GET /app_views/list` to retrieve the list of custom views that you have configured in the 3rd-Party App Governance.
  - Added `GET /app_views/{appViewId}/apps` to retrieves all assets (i.e., apps) that are related to a specified argument (i.e., custom view).

ZIA Admin Role Endpoints
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#259 <https://github.com/zscaler/zscaler-sdk-python/pull/259>`_) - Added the following new ZIA API Endpoints:
    - Added `GET /adminRoles/{roleId}` Retrieves the admin role based on the specified ID
    - Added `GET /adminRoles/lite` Retrieves a name and ID dictionary of all admin roles. The list only includes the name and ID for all admin roles.
    - Added `POST /adminRoles` Adds an admin role.
    - Added `PUT /adminRoles/{roleId}` Updates the admin role based on the specified ID.
    - Added `DELETE /adminRoles/{roleId}` Deletes the admin role based on the specified ID.

ZPA Credential Pool (New)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#259 <https://github.com/zscaler/zscaler-sdk-python/pull/259>`_) - Added new ZPA endpoint:
  - Added `GET /credential-pool` Gets the privileged credential pool details for the specified customer.
  - Added `GET /credential-pool/{id}` Gets the privileged credential pool details for the specified customer.
  - Added `GET /credential-pool/{id}/credential` Given Privileged credential pool id gets mapped privileged credential info
  - Added `POST /credential-pool` Adds a new privileged credential pool for the specified customer.
  - Added `PUT /credential-pool/{id}` Updates the existing credential pool for the specified customer.
  - Added `DELETE /credential-pool/{id}` Updates the existing credential pool for the specified customer.

ZWA - Zscaler Workflow Automation (NEW)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#259 <https://github.com/zscaler/zscaler-sdk-python/pull/259>`_) - Added new ZWA endpoint:
  - Added `GET /dlp/v1/incidents/transactions/{transactionId}` Gets the list of all DLP incidents associated with the transaction ID
  - Added `GET /dlp/v1/incidents/{dlpIncidentId}` Gets the DLP incident details based on the incident ID.
  - Added `DELETE /dlp/v1/incidents/{dlpIncidentId}` Deletes the DLP incident for the specified incident ID.
  - Added `GET /dlp/v1/incidents{dlpIncidentId}/change-history` Gets the details of updates made to an incident based on the given ID and timeline.
  - Added `GET /dlp/v1/incidents/{dlpIncidentId}/tickets` Gets the information of the ticket generated for the incident. For example, ticket type, ticket ID, ticket status, etc.
  - Added `POST /dlp/v1/incidents/{dlpIncidentId}/incident-groups/search` Filters a list of DLP incident groups to which the specified incident ID belongs.
  - Added `POST /dlp/v1/incidents/{dlpIncidentId}/close` Updates the status of the incident to resolved and closes the incident with a resolution label and a resolution code.
  - Added `POST /dlp/v1/incidents/{dlpIncidentId}/notes` Adds notes to the incident during updates or status changes.
  - Added `POST /dlp/v1/incidents/{dlpIncidentId}/labels` Assign lables (a label name and it's associated value) to DLP incidents.
  - Added `POST /dlp/v1/incidents/search` Filters DLP incidents based on the given time range and the field values.
  - Added `GET /dlp/v1/incidents/{dlpIncidentId}/triggers` Downloads the actual data that triggered the incident.
  - Added `GET /dlp/v1/incidents/{dlpIncidentId}/evidence` Gets the evidence URL of the incident.

Cloud & Branch Connector - OneAPI Support
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(`#259 <https://github.com/zscaler/zscaler-sdk-python/pull/259>`_) - Cloud & Branch Connector package is now compatible with OneAPI and Legacy API framework. Please refer to README for details.
(`#259 <https://github.com/zscaler/zscaler-sdk-python/pull/259>`_) - Cloud & Branch Connector package has been renamed from `zcon` to `ztw`

ZTW Policy Management
^^^^^^^^^^^^^^^^^^^^^^^

(`#259 <https://github.com/zscaler/zscaler-sdk-python/pull/259>`_) - Added the following new ZTW API Endpoints:
    - Added `GET /ecRules/ecRdr` Retrieves the list of traffic forwarding rules.
    - Added `PUT /ecRules/ecRdr/{ruleId}` Updates a traffic forwarding rule configuration based on the specified ID.
    - Added `POST /ecRules/ecRdr` Creates a new traffic forwarding rule.
    - Added `GET /ecRules/ecRdr/count` Retrieves the count of traffic forwarding rules available in the Cloud & Branch Connector Admin Portal.

ZTW Policy Resources
^^^^^^^^^^^^^^^^^^^^^

(`#259 <https://github.com/zscaler/zscaler-sdk-python/pull/259>`_) - Added the following new ZTW API Endpoints:
    - Added `GET /ipSourceGroups` Retrieves the list of source IP groups.
    - Added `GET /ipSourceGroups/lite` Retrieves the list of source IP groups. This request retrieves basic information about the source IP groups, such as name and ID. For extensive details, use the GET /ipSourceGroups request.
    - Added `POST /ipSourceGroups` Adds a new custom source IP group.
    - Added `DELETE /ipSourceGroups/{ipGroupId}` Deletes a source IP group based on the specified ID.
    - Added `GET /ipDestinationGroups` Retrieves the list of destination IP groups.
    - Added `GET /ipDestinationGroups/lite` Retrieves the list of destination IP groups. This request retrieves basic information about the destination IP groups, ID, name, and type. For extensive details, use the GET /ipDestinationGroups request.
    - Added `POST /ipDestinationGroups` Adds a new custom destination IP group.
    - Added `DELETE /ipDestinationGroups/{ipGroupId}` Deletes the destination IP group based on the specified ID. Default destination groups that are automatically created cannot be deleted.
    - Added `GET /ipGroups` Retrieves the list of IP pools.
    - Added `GET /ipGroups/lite` Retrieves the list of IP pools. This request retrieves basic information about the IP pools, such as name and ID. For extensive details, use the GET /ipGroups request.
    - Added `POST /ipGroups` Adds a new custom IP pool.
    - Added `DELETE /ipGroups/{ipGroupId}` Deletes an IP pool based on the specified ID.
    - Added `GET /networkServices` Retrieves the list of all network services. The search parameters find matching values within the name or description attributes.
    - Added `POST /networkServices` Creates a new network service.
    - Added `PUT /networkServices/{serviceId}` Updates the network service information for the specified service ID.
    - Added `DELETE /networkServices/{serviceId}` Deletes the network service for the specified ID.
    - Added `GET /networkServicesGroups` Retrieves the list of network service groups.
    - Added `GET /zpaResources/applicationSegments` Retrieves the list of ZPA application segments that can be configured in traffic forwarding rule criteria.

1.0.1 (April, 22 2025) - BREAKING CHANGES
-----------------------------------------

Notes
-----

- Python Versions: **v3.8, v3.9, v3.10, v3.11**


Zscaler OneAPI Support
-----------------------

(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_): Added support for (`OneAPI <https://help.zscaler.com/zidentity/what-zidentity>`_) Oauth2 authentication support through (`Zidentity <https://help.zscaler.com/zidentity/what-zidentity>`_)

**NOTES**
  - Starting at v1.0.0 version this SDK provides dual API client functionality and is backwards compatible with the legacy Zscaler API framework.
  - The new OneAPI framework is compatible only with the following products `ZCC/ZIA/ZPA`.
  - The following products `ZTW` - Cloud Connector and `ZDX` and Zscaler Digital Experience, authentication methods remain unnaffected.
  - The package `ZCON` (Zscaler Cloud and Branch Connector) has been renamed to `ZTW`
  - The following products `ZWA` - Zscaler Workflow Automation authentication methods remain unnaffected.

Refer to the (`README <hhttps://github.com/zscaler/zscaler-sdk-python/blob/master/README.md>`_) page for details on client instantiation, and authentication requirements on each individual product.

**WARNING**: Attention Government customers. OneAPI and Zidentity is not currently supported for the following ZIA clouds: `zscalergov` and `zscalerten` or ZPA `GOV`, and `GOVUS`. 
See the Zscaler Legacy API Framework section in the (`README Docs <https://zscaler-sdk-python.readthedocs.io/en/latest/index.html>`_) for more information on how authenticate to these environments using the built-in Legacy API method.

(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_): All API clients now support Config Setter object `ZCC/ZTW/ZDX/ZIA/ZPA/ZWA`

ZCC New Endpoints
^^^^^^^^^^^^^^^^^

(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Added the following new ZCC API Endpoints:
  - Added `GET /downloadServiceStatus` to download service status for all devices.
  - Added `GET /getDeviceCleanupInfo` to retrieve device cleanup information.
  - Added `PUT /setDeviceCleanupInfo` to cleanup device information.
  - Added `GET /getDeviceDetails` to retrieve device detailed information.
  - Added `GET /getAdminUsers` to retrieve mobile portal admin user.
  - Added `PUT /editAdminUser` to update mobile portal admin user.
  - Added `GET /getAdminUsersSyncInfo` to retrieve mobile portal admin user sync information.
  - Added `POST /syncZiaZdxAdminUsers` to retrieve mobile portal admin users ZIA and ZDX sync information.
  - Added `POST /syncZpaAdminUsers` to retrieve mobile portal admin users ZPA sync information.
  - Added `GET /getAdminRoles` to retrieve mobile portal admin roles.
  - Added `GET /getCompanyInfo` to retrieve company information.
  - Added `GET /getZdxGroupEntitlements` to retrieve ZDX Group entitlement enablement.
  - Added `PUT /updateZdxGroupEntitlement` to retrieve ZDX Group entitlement enablement.
  - Added `GET /updateZpaGroupEntitlement` to retrieve ZPA Group entitlement enablement.
  - Added `GET /web/policy/listByCompany` to retrieve Web Policy By Company ID.
  - Added `PUT /web/policy/activate` to activate mobile portal web policy
  - Added `PUT /web/policy/edit` to update mobile portal web policy
  - Added `DELETE /web/policy/{policyId}/delete` to delete mobile portal web policy.
  - Added `GET /webAppService/listByCompany` to retrieve Web App Service information By Company ID.
  - Added `GET /webFailOpenPolicy/listByCompany` to retrieve web Fail Open Policy information By Company ID.
  - Added `PUT /webFailOpenPolicy/edit` to update mobile portal web Fail Open Policy.
  - Added `GET /webForwardingProfile/listByCompany` to retrieve Web Forwarding Profile information By Company ID.
  - Added `POST /webForwardingProfile/edit` to create a Web Forwarding Profile.
  - Added `DELETE /webForwardingProfile/{profileId}/delete` to delete Web Forwarding Profile.
  - Added `GET /webTrustedNetwork/listByCompany` to retrieve multiple Web Trusted Network information By Company ID.
  - Added `POST /webTrustedNetwork/edit` to create Web Trusted Network resource.
  - Added `PUT /webTrustedNetwork/edit` to update Web Trusted Network resource.
  - Added `DELETE /webTrustedNetwork/{networkId}/delete` to delete Web Trusted Network resource.
  - Added `GET /getWebPrivacyInfo` to retrieve Web Privacy Info.
  - Added `GET /setWebPrivacyInfo` to update Web Privacy Info.

ZIA Sandbox Submission - BREAKING CHANGES
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Authentication to Zscaler Sandbox now use the following attributes during client instantiation.
 - `sandboxToken` - Can also be sourced from the `ZSCALER_SANDBOX_TOKEN` environment variable.
 - `sandboxCloud` - Can also be sourced from the `ZSCALER_SANDBOX_CLOUD` environment variable.

**NOTE** The previous `ZIA_SANDBOX_TOKEN` has been deprecated.

ZIA Sandbox Rules
^^^^^^^^^^^^^^^^^^

(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /sandboxRules` to retrieve the list of all Sandbox policy rules.
  - Added `GET /sandboxRules/{ruleId}` to retrieve the Sandbox policy rule information based on the specified ID.
  - Added `POST /sandboxRules` to add a Sandbox policy rule.
  - Added `PUT /sandboxRules/{ruleId}` to update the Sandbox policy rule configuration for the specified ID.
  - Added `DELETE /sandboxRules/{ruleId}` to delete the Sandbox policy rule based on the specified ID.

ZIA DNS Control Rules
^^^^^^^^^^^^^^^^^^^^^^

(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /firewallDnsRules` to retrieve the list of all DNS Control policy rules.
  - Added `GET /firewallDnsRules/{ruleId}` to retrieve the DNS Control policy rule information based on the specified ID.
  - Added `POST /firewallDnsRules` to add a DNS Control policy rules.
  - Added `PUT /firewallDnsRules/{ruleId}` to update the DNS Control policy rule configuration for the specified ID.
  - Added `DELETE /firewallDnsRules/{ruleId}` to delete the DNS Control policy rule based on the specified ID.

ZIA IPS Control Rules
^^^^^^^^^^^^^^^^^^^^^

(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /firewallIpsRules` to retrieve the list of all IPS Control policy rules.
  - Added `GET /firewallIpsRules/{ruleId}` to retrieve the IPS Control policy rule information based on the specified ID.
  - Added `POST /firewallIpsRules` to add a IPS Control policy rule.
  - Added `PUT /firewallIpsRules/{ruleId}` to update the IPS Control policy rule configuration for the specified ID.
  - Added `DELETE /firewallIpsRules/{ruleId}` to delete the IPS Control policy rule based on the specified ID.

ZIA File Type Control Policy
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /fileTypeRules` to retrieve the list of all File Type Control policy rules.
  - Added `GET /fileTypeRules/lite` to retrieve the list of all File Type Control policy rules.
  - Added `GET /fileTypeRules/{ruleId}` to retrieve the File Type Control policy rule information based on the specified ID.
  - Added `POST /fileTypeRules` to add a File Type Control policy rule.
  - Added `PUT /fileTypeRules/{ruleId}` to update the File Type Control policy rule configuration for the specified ID.
  - Added `DELETE /fileTypeRules/{ruleId}` to delete the File Type Control policy rule based on the specified ID.

ZIA Forwarding Control Policy - Proxy Gateways
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /proxyGateways` to retrieve the proxy gateway information.
  - Added `GET /proxyGateways/lite` to retrieve the name and ID of the proxy.

ZIA Cloud Nanolog Streaming Service (NSS)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /nssFeeds` to retrieve the cloud NSS feeds.
  - Added `GET /nssFeeds/{feedId}` to retrieve information about cloud NSS feed based on the specified ID.
  - Added `POST /nssFeeds` to add a new cloud NSS feed.
  - Added `PUT /nssFeeds/{feedId}` to update cloud NSS feed configuration based on the specified ID.
  - Added `DELETE /nssFeeds/{feedId}` to delete cloud NSS feed configuration based on the specified ID.
  - Added `GET /nssFeeds/feedOutputDefaults` to retrieve the default cloud NSS feed output format for different log types.
  - Added `GET /nssFeeds/testConnectivity/{feedId}` to test the connectivity of cloud NSS feed based on the specified ID
  - Added `POST /nssFeeds/validateFeedFormat` to validates the cloud NSS feed format and returns the validation result

ZIA Advanced Threat Protection Policy
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /cyberThreatProtection/advancedThreatSettings` to retrieve the advanced threat configuration settings.
  - Added `PUT /cyberThreatProtection/advancedThreatSettings` to update the advanced threat configuration settings.
  - Added `GET /cyberThreatProtection/maliciousUrls` to retrieve the malicious URLs added to the denylist in the Advanced Threat Protection (ATP) policy
  - Added `PUT /cyberThreatProtection/maliciousUrls` to updates the malicious URLs added to the denylist in ATP policy
  - Added `GET /cyberThreatProtection/securityExceptions` to retrieves information about the security exceptions configured for the ATP policy
  - Added `PUT /cyberThreatProtection/securityExceptions` to update security exceptions for the ATP policy

ZIA Advanced Threat Protection Policy
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /cyberThreatProtection/atpMalwareInspection` to retrieve the traffic inspection configurations of Malware Protection policy
  - Added `PUT /cyberThreatProtection/atpMalwareInspection` to update the traffic inspection configurations of Malware Protection policy.
  - Added `GET /cyberThreatProtection/atpMalwareProtocols` to retrieve the protocol inspection configurations of Malware Protection policy
  - Added `PUT /cyberThreatProtection/atpMalwareProtocols` to update the protocol inspection configurations of Malware Protection policy.
  - Added `GET /cyberThreatProtection/malwareSettings` to retrieve the malware protection policy configuration details
  - Added `PUT /cyberThreatProtection/malwareSettings` to update the malware protection policy configuration details.
  - Added `GET /cyberThreatProtection/malwarePolicy` to retrieve information about the security exceptions configured for the Malware Protection policy
  - Added `PUT /cyberThreatProtection/malwarePolicy` to update security exceptions for the Malware Protection policy.

ZIA URL & Cloud App Control Policy Settings
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /advancedUrlFilterAndCloudAppSettings` to retrieve information about URL and Cloud App Control advanced policy settings
  - Added `PUT /advancedUrlFilterAndCloudAppSettings` to update the URL and Cloud App Control advanced policy settings

ZIA Authentication Settings
^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /authSettings` to retrieve the organization's default authentication settings information, including authentication profile and Kerberos authentication information.
  - Added `GET /authSettings/lite` to retrieve organization's default authentication settings information.
  - Added `PUT /authSettings` to update the organization's default authentication settings information.

ZIA Advanced Settings
^^^^^^^^^^^^^^^^^^^^^

(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /advancedSettings` to retrieve information about the advanced settings.
  - Added `PUT /advancedSettings` to update the advanced settings configuration.

ZIA Cloud Applications
^^^^^^^^^^^^^^^^^^^^^^^

(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /cloudApplications/policy` Retrieves a list of Predefined and User Defined Cloud Applications associated with the DLP rules, Cloud App Control rules, Advanced Settings, Bandwidth Classes, and File Type Control rules.
  - Added `GET /cloudApplications/sslPolicy` Retrieves a list of Predefined and User Defined Cloud Applications associated with the SSL Inspection rules.

ZIA Shadow IT Report
^^^^^^^^^^^^^^^^^^^^

(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Added the following new ZIA API Endpoints:
- Added `PUT /cloudApplications/bulkUpdate` To Update application status and tag information for predefined or custom cloud applications based on the IDs specified
- Added `GET /cloudApplications/lite` Gets the list of predefined and custom cloud applications
- Added `GET /customTags` Gets the list of custom tags available to assign to cloud applications
- Added `POST /shadowIT/applications/export` Export the Shadow IT Report (in CSV format) for the cloud applications recognized by Zscaler based on their usage in your organization.
- Added `POST /shadowIT/applications/{entity}/exportCsv` Export the Shadow IT Report (in CSV format) for the list of users or known locations identified with using the cloud applications specified in the request.

ZIA Remote Assistance Support
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /remoteAssistance` to retrieve information about the Remote Assistance option.
  - Added `PUT /remoteAssistance` to update information about the Remote Assistance option. Using this option, you can allow Zscaler Support to access your organization’s ZIA Admin Portal for a specified time period to troubleshoot issues.

ZIA Organization Details
^^^^^^^^^^^^^^^^^^^^^^^^^

(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /orgInformation` to retrieve detailed organization information, including headquarter location, geolocation, address, and contact details.
  - Added `GET /orgInformation/lite` to retrieve minimal organization information.
  - Added `GET /subscriptions` to retrieve information about the list of subscriptions enabled for your tenant. Subscriptions define the various features and levels of functionality that are available to your organization.

ZIA End User Notification
^^^^^^^^^^^^^^^^^^^^^^^^^^
(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /eun` to retrieve information browser-based end user notification (EUN) configuration details.
  - Added `PUT /eun` to update the browser-based end user notification (EUN) configuration details.

ZIA Admin Audit Logs
^^^^^^^^^^^^^^^^^^^^^^^

(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /auditlogEntryReport` to retrieve the status of a request for an audit log report.
  - Added `POST /auditlogEntryReport` to create an audit log report for the specified time period and saves it as a CSV file.
  - Added `DELETE /auditlogEntryReport` to cancel the request to create an audit log report.
  - Added `GET /auditlogEntryReport/download` to download the most recently created audit log report.

ZIA Extranets
^^^^^^^^^^^^^^^^^^

(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /extranet` to retrieve the list of extranets configured for the organization
  - Added `GET /extranet/lite` Retrieves the name-ID pairs of all extranets configured for an organization
  - Added `GET /extranet/{Id}` Retrieves information about an extranet based on the specified ID.
  - Added `POST /extranet` Adds a new extranet for the organization.
  - Added `PUT /extranet/{Id}` Updates an extranet based on the specified ID
  - Added `DELETE /extranet/{Id}` Deletes an extranet based on the specified ID

ZIA IOT Endpoint
^^^^^^^^^^^^^^^^^^

(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Added the following new ZIA IOT API Endpoints:
  - Added `GET /iotDiscovery/deviceTypes` Retrieve the mapping between device type universally unique identifier (UUID) values and the device type names for all the device types supported by the Zscaler AI/ML.
  - Added `GET /iotDiscovery/categories` Retrieve the mapping between the device category universally unique identifier (UUID) values and the category names for all the device categories supported by the Zscaler AI/ML. The parent of device category is device type.
  - Added `GET /iotDiscovery/classifications` Retrieve the mapping between the device classification universally unique identifier (UUID) values and the classification names for all the device classifications supported by Zscaler AI/ML. The parent of device classification is device category.
  - Added `GET /iotDiscovery/deviceList` Retrieve a list of discovered devices with the following key contexts, IP address, location, ML auto-label, classification, category, and type.

ZIA 3rd-Party App Governance
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /apps/app` to search the 3rd-Party App Governance App Catalog by either app ID or URL.
  - Added `POST /apps/app` to submis an app for analysis in the 3rd-Party App Governance Sandbox.
  - Added `GET /apps/search` to search for an app by name. Any app whose name contains the search term (appName) is returned.
  - Added `GET /app_views/list` to retrieve the list of custom views that you have configured in the 3rd-Party App Governance.
  - Added `GET /app_views/{appViewId}/apps` to retrieves all assets (i.e., apps) that are related to a specified argument (i.e., custom view).

ZIA Admin Role Endpoints
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Added the following new ZIA API Endpoints:
    - Added `GET /adminRoles/{roleId}` Retrieves the admin role based on the specified ID
    - Added `GET /adminRoles/lite` Retrieves a name and ID dictionary of all admin roles. The list only includes the name and ID for all admin roles.
    - Added `POST /adminRoles` Adds an admin role.
    - Added `PUT /adminRoles/{roleId}` Updates the admin role based on the specified ID.
    - Added `DELETE /adminRoles/{roleId}` Deletes the admin role based on the specified ID.

ZPA Credential Pool (New)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Added new ZPA endpoint:
  - Added `GET /credential-pool` Gets the privileged credential pool details for the specified customer.
  - Added `GET /credential-pool/{id}` Gets the privileged credential pool details for the specified customer.
  - Added `GET /credential-pool/{id}/credential` Given Privileged credential pool id gets mapped privileged credential info
  - Added `POST /credential-pool` Adds a new privileged credential pool for the specified customer.
  - Added `PUT /credential-pool/{id}` Updates the existing credential pool for the specified customer.
  - Added `DELETE /credential-pool/{id}` Updates the existing credential pool for the specified customer.

ZWA - Zscaler Workflow Automation (NEW)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Added new ZWA endpoint:
  - Added `GET /dlp/v1/incidents/transactions/{transactionId}` Gets the list of all DLP incidents associated with the transaction ID
  - Added `GET /dlp/v1/incidents/{dlpIncidentId}` Gets the DLP incident details based on the incident ID.
  - Added `DELETE /dlp/v1/incidents/{dlpIncidentId}` Deletes the DLP incident for the specified incident ID.
  - Added `GET /dlp/v1/incidents{dlpIncidentId}/change-history` Gets the details of updates made to an incident based on the given ID and timeline.
  - Added `GET /dlp/v1/incidents/{dlpIncidentId}/tickets` Gets the information of the ticket generated for the incident. For example, ticket type, ticket ID, ticket status, etc.
  - Added `POST /dlp/v1/incidents/{dlpIncidentId}/incident-groups/search` Filters a list of DLP incident groups to which the specified incident ID belongs.
  - Added `POST /dlp/v1/incidents/{dlpIncidentId}/close` Updates the status of the incident to resolved and closes the incident with a resolution label and a resolution code.
  - Added `POST /dlp/v1/incidents/{dlpIncidentId}/notes` Adds notes to the incident during updates or status changes.
  - Added `POST /dlp/v1/incidents/{dlpIncidentId}/labels` Assign lables (a label name and it's associated value) to DLP incidents.
  - Added `POST /dlp/v1/incidents/search` Filters DLP incidents based on the given time range and the field values.
  - Added `GET /dlp/v1/incidents/{dlpIncidentId}/triggers` Downloads the actual data that triggered the incident.
  - Added `GET /dlp/v1/incidents/{dlpIncidentId}/evidence` Gets the evidence URL of the incident.

Cloud & Branch Connector - OneAPI Support
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Cloud & Branch Connector package is now compatible with OneAPI and Legacy API framework. Please refer to README for details.
(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Cloud & Branch Connector package has been renamed from `zcon` to `ztw`

ZTW Policy Management
^^^^^^^^^^^^^^^^^^^^^^^

(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Added the following new ZTW API Endpoints:
    - Added `GET /ecRules/ecRdr` Retrieves the list of traffic forwarding rules.
    - Added `PUT /ecRules/ecRdr/{ruleId}` Updates a traffic forwarding rule configuration based on the specified ID.
    - Added `POST /ecRules/ecRdr` Creates a new traffic forwarding rule.
    - Added `GET /ecRules/ecRdr/count` Retrieves the count of traffic forwarding rules available in the Cloud & Branch Connector Admin Portal.

ZTW Policy Resources
^^^^^^^^^^^^^^^^^^^^^

(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Added the following new ZTW API Endpoints:
    - Added `GET /ipSourceGroups` Retrieves the list of source IP groups.
    - Added `GET /ipSourceGroups/lite` Retrieves the list of source IP groups. This request retrieves basic information about the source IP groups, such as name and ID. For extensive details, use the GET /ipSourceGroups request.
    - Added `POST /ipSourceGroups` Adds a new custom source IP group.
    - Added `DELETE /ipSourceGroups/{ipGroupId}` Deletes a source IP group based on the specified ID.
    - Added `GET /ipDestinationGroups` Retrieves the list of destination IP groups.
    - Added `GET /ipDestinationGroups/lite` Retrieves the list of destination IP groups. This request retrieves basic information about the destination IP groups, ID, name, and type. For extensive details, use the GET /ipDestinationGroups request.
    - Added `POST /ipDestinationGroups` Adds a new custom destination IP group.
    - Added `DELETE /ipDestinationGroups/{ipGroupId}` Deletes the destination IP group based on the specified ID. Default destination groups that are automatically created cannot be deleted.
    - Added `GET /ipGroups` Retrieves the list of IP pools.
    - Added `GET /ipGroups/lite` Retrieves the list of IP pools. This request retrieves basic information about the IP pools, such as name and ID. For extensive details, use the GET /ipGroups request.
    - Added `POST /ipGroups` Adds a new custom IP pool.
    - Added `DELETE /ipGroups/{ipGroupId}` Deletes an IP pool based on the specified ID.
    - Added `GET /networkServices` Retrieves the list of all network services. The search parameters find matching values within the name or description attributes.
    - Added `POST /networkServices` Creates a new network service.
    - Added `PUT /networkServices/{serviceId}` Updates the network service information for the specified service ID.
    - Added `DELETE /networkServices/{serviceId}` Deletes the network service for the specified ID.
    - Added `GET /networkServicesGroups` Retrieves the list of network service groups.
    - Added `GET /zpaResources/applicationSegments` Retrieves the list of ZPA application segments that can be configured in traffic forwarding rule criteria.

1.0.1 (April, 22 2025) - BREAKING CHANGES
-----------------------------------------

Notes
-----

- Python Versions: **v3.8, v3.9, v3.10, v3.11**


Zscaler OneAPI Support
-----------------------

(`#258 <https://github.com/zscaler/zscaler-sdk-python/pull/258>`_): Added support for (`OneAPI <https://help.zscaler.com/zidentity/what-zidentity>`_) Oauth2 authentication support through (`Zidentity <https://help.zscaler.com/zidentity/what-zidentity>`_)

**NOTES**
  - Starting at v1.0.0 version this SDK provides dual API client functionality and is backwards compatible with the legacy Zscaler API framework.
  - The new OneAPI framework is compatible only with the following products `ZCC/ZIA/ZPA`.
  - The following products `ZTW` - Cloud Connector and `ZDX` and Zscaler Digital Experience, authentication methods remain unnaffected.
  - The package `ZCON` (Zscaler Cloud and Branch Connector) has been renamed to `ZTW`
  - The following products `ZWA` - Zscaler Workflow Automation authentication methods remain unnaffected.

Refer to the (`README <hhttps://github.com/zscaler/zscaler-sdk-python/blob/master/README.md>`_) page for details on client instantiation, and authentication requirements on each individual product.

**WARNING**: Attention Government customers. OneAPI and Zidentity is not currently supported for the following ZIA clouds: `zscalergov` and `zscalerten` or ZPA `GOV`, and `GOVUS`. 
See the Zscaler Legacy API Framework section in the (`README Docs <https://zscaler-sdk-python.readthedocs.io/en/latest/index.html>`_) for more information on how authenticate to these environments using the built-in Legacy API method.

(`#258 <https://github.com/zscaler/zscaler-sdk-python/pull/258>`_): All API clients now support Config Setter object `ZCC/ZTW/ZDX/ZIA/ZPA/ZWA`

ZCC New Endpoints
^^^^^^^^^^^^^^^^^

(`#258 <https://github.com/zscaler/zscaler-sdk-python/pull/258>`_) - Added the following new ZCC API Endpoints:
  - Added `GET /downloadServiceStatus` to download service status for all devices.
  - Added `GET /getDeviceCleanupInfo` to retrieve device cleanup information.
  - Added `PUT /setDeviceCleanupInfo` to cleanup device information.
  - Added `GET /getDeviceDetails` to retrieve device detailed information.
  - Added `GET /getAdminUsers` to retrieve mobile portal admin user.
  - Added `PUT /editAdminUser` to update mobile portal admin user.
  - Added `GET /getAdminUsersSyncInfo` to retrieve mobile portal admin user sync information.
  - Added `POST /syncZiaZdxAdminUsers` to retrieve mobile portal admin users ZIA and ZDX sync information.
  - Added `POST /syncZpaAdminUsers` to retrieve mobile portal admin users ZPA sync information.
  - Added `GET /getAdminRoles` to retrieve mobile portal admin roles.
  - Added `GET /getCompanyInfo` to retrieve company information.
  - Added `GET /getZdxGroupEntitlements` to retrieve ZDX Group entitlement enablement.
  - Added `PUT /updateZdxGroupEntitlement` to retrieve ZDX Group entitlement enablement.
  - Added `GET /updateZpaGroupEntitlement` to retrieve ZPA Group entitlement enablement.
  - Added `GET /web/policy/listByCompany` to retrieve Web Policy By Company ID.
  - Added `PUT /web/policy/activate` to activate mobile portal web policy
  - Added `PUT /web/policy/edit` to update mobile portal web policy
  - Added `DELETE /web/policy/{policyId}/delete` to delete mobile portal web policy.
  - Added `GET /webAppService/listByCompany` to retrieve Web App Service information By Company ID.
  - Added `GET /webFailOpenPolicy/listByCompany` to retrieve web Fail Open Policy information By Company ID.
  - Added `PUT /webFailOpenPolicy/edit` to update mobile portal web Fail Open Policy.
  - Added `GET /webForwardingProfile/listByCompany` to retrieve Web Forwarding Profile information By Company ID.
  - Added `POST /webForwardingProfile/edit` to create a Web Forwarding Profile.
  - Added `DELETE /webForwardingProfile/{profileId}/delete` to delete Web Forwarding Profile.
  - Added `GET /webTrustedNetwork/listByCompany` to retrieve multiple Web Trusted Network information By Company ID.
  - Added `POST /webTrustedNetwork/edit` to create Web Trusted Network resource.
  - Added `PUT /webTrustedNetwork/edit` to update Web Trusted Network resource.
  - Added `DELETE /webTrustedNetwork/{networkId}/delete` to delete Web Trusted Network resource.
  - Added `GET /getWebPrivacyInfo` to retrieve Web Privacy Info.
  - Added `GET /setWebPrivacyInfo` to update Web Privacy Info.

ZIA Sandbox Submission - BREAKING CHANGES
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#258 <https://github.com/zscaler/zscaler-sdk-python/pull/258>`_) - Authentication to Zscaler Sandbox now use the following attributes during client instantiation.
 - `sandboxToken` - Can also be sourced from the `ZSCALER_SANDBOX_TOKEN` environment variable.
 - `sandboxCloud` - Can also be sourced from the `ZSCALER_SANDBOX_CLOUD` environment variable.

**NOTE** The previous `ZIA_SANDBOX_TOKEN` has been deprecated.

ZIA Sandbox Rules
^^^^^^^^^^^^^^^^^^

(`#258 <https://github.com/zscaler/zscaler-sdk-python/pull/258>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /sandboxRules` to retrieve the list of all Sandbox policy rules.
  - Added `GET /sandboxRules/{ruleId}` to retrieve the Sandbox policy rule information based on the specified ID.
  - Added `POST /sandboxRules` to add a Sandbox policy rule.
  - Added `PUT /sandboxRules/{ruleId}` to update the Sandbox policy rule configuration for the specified ID.
  - Added `DELETE /sandboxRules/{ruleId}` to delete the Sandbox policy rule based on the specified ID.

ZIA DNS Control Rules
^^^^^^^^^^^^^^^^^^^^^^

(`#258 <https://github.com/zscaler/zscaler-sdk-python/pull/258>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /firewallDnsRules` to retrieve the list of all DNS Control policy rules.
  - Added `GET /firewallDnsRules/{ruleId}` to retrieve the DNS Control policy rule information based on the specified ID.
  - Added `POST /firewallDnsRules` to add a DNS Control policy rules.
  - Added `PUT /firewallDnsRules/{ruleId}` to update the DNS Control policy rule configuration for the specified ID.
  - Added `DELETE /firewallDnsRules/{ruleId}` to delete the DNS Control policy rule based on the specified ID.

ZIA IPS Control Rules
^^^^^^^^^^^^^^^^^^^^^

(`#258 <https://github.com/zscaler/zscaler-sdk-python/pull/258>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /firewallIpsRules` to retrieve the list of all IPS Control policy rules.
  - Added `GET /firewallIpsRules/{ruleId}` to retrieve the IPS Control policy rule information based on the specified ID.
  - Added `POST /firewallIpsRules` to add a IPS Control policy rule.
  - Added `PUT /firewallIpsRules/{ruleId}` to update the IPS Control policy rule configuration for the specified ID.
  - Added `DELETE /firewallIpsRules/{ruleId}` to delete the IPS Control policy rule based on the specified ID.

ZIA File Type Control Policy
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#258 <https://github.com/zscaler/zscaler-sdk-python/pull/258>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /fileTypeRules` to retrieve the list of all File Type Control policy rules.
  - Added `GET /fileTypeRules/lite` to retrieve the list of all File Type Control policy rules.
  - Added `GET /fileTypeRules/{ruleId}` to retrieve the File Type Control policy rule information based on the specified ID.
  - Added `POST /fileTypeRules` to add a File Type Control policy rule.
  - Added `PUT /fileTypeRules/{ruleId}` to update the File Type Control policy rule configuration for the specified ID.
  - Added `DELETE /fileTypeRules/{ruleId}` to delete the File Type Control policy rule based on the specified ID.

ZIA Forwarding Control Policy - Proxy Gateways
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#258 <https://github.com/zscaler/zscaler-sdk-python/pull/258>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /proxyGateways` to retrieve the proxy gateway information.
  - Added `GET /proxyGateways/lite` to retrieve the name and ID of the proxy.

ZIA Cloud Nanolog Streaming Service (NSS)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#258 <https://github.com/zscaler/zscaler-sdk-python/pull/258>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /nssFeeds` to retrieve the cloud NSS feeds.
  - Added `GET /nssFeeds/{feedId}` to retrieve information about cloud NSS feed based on the specified ID.
  - Added `POST /nssFeeds` to add a new cloud NSS feed.
  - Added `PUT /nssFeeds/{feedId}` to update cloud NSS feed configuration based on the specified ID.
  - Added `DELETE /nssFeeds/{feedId}` to delete cloud NSS feed configuration based on the specified ID.
  - Added `GET /nssFeeds/feedOutputDefaults` to retrieve the default cloud NSS feed output format for different log types.
  - Added `GET /nssFeeds/testConnectivity/{feedId}` to test the connectivity of cloud NSS feed based on the specified ID
  - Added `POST /nssFeeds/validateFeedFormat` to validates the cloud NSS feed format and returns the validation result

ZIA Advanced Threat Protection Policy
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#258 <https://github.com/zscaler/zscaler-sdk-python/pull/258>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /cyberThreatProtection/advancedThreatSettings` to retrieve the advanced threat configuration settings.
  - Added `PUT /cyberThreatProtection/advancedThreatSettings` to update the advanced threat configuration settings.
  - Added `GET /cyberThreatProtection/maliciousUrls` to retrieve the malicious URLs added to the denylist in the Advanced Threat Protection (ATP) policy
  - Added `PUT /cyberThreatProtection/maliciousUrls` to updates the malicious URLs added to the denylist in ATP policy
  - Added `GET /cyberThreatProtection/securityExceptions` to retrieves information about the security exceptions configured for the ATP policy
  - Added `PUT /cyberThreatProtection/securityExceptions` to update security exceptions for the ATP policy

ZIA Advanced Threat Protection Policy
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#258 <https://github.com/zscaler/zscaler-sdk-python/pull/258>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /cyberThreatProtection/atpMalwareInspection` to retrieve the traffic inspection configurations of Malware Protection policy
  - Added `PUT /cyberThreatProtection/atpMalwareInspection` to update the traffic inspection configurations of Malware Protection policy.
  - Added `GET /cyberThreatProtection/atpMalwareProtocols` to retrieve the protocol inspection configurations of Malware Protection policy
  - Added `PUT /cyberThreatProtection/atpMalwareProtocols` to update the protocol inspection configurations of Malware Protection policy.
  - Added `GET /cyberThreatProtection/malwareSettings` to retrieve the malware protection policy configuration details
  - Added `PUT /cyberThreatProtection/malwareSettings` to update the malware protection policy configuration details.
  - Added `GET /cyberThreatProtection/malwarePolicy` to retrieve information about the security exceptions configured for the Malware Protection policy
  - Added `PUT /cyberThreatProtection/malwarePolicy` to update security exceptions for the Malware Protection policy.

ZIA URL & Cloud App Control Policy Settings
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#258 <https://github.com/zscaler/zscaler-sdk-python/pull/258>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /advancedUrlFilterAndCloudAppSettings` to retrieve information about URL and Cloud App Control advanced policy settings
  - Added `PUT /advancedUrlFilterAndCloudAppSettings` to update the URL and Cloud App Control advanced policy settings

ZIA Authentication Settings
^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#258 <https://github.com/zscaler/zscaler-sdk-python/pull/258>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /authSettings` to retrieve the organization's default authentication settings information, including authentication profile and Kerberos authentication information.
  - Added `GET /authSettings/lite` to retrieve organization's default authentication settings information.
  - Added `PUT /authSettings` to update the organization's default authentication settings information.

ZIA Advanced Settings
^^^^^^^^^^^^^^^^^^^^^

(`#258 <https://github.com/zscaler/zscaler-sdk-python/pull/258>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /advancedSettings` to retrieve information about the advanced settings.
  - Added `PUT /advancedSettings` to update the advanced settings configuration.

ZIA Cloud Applications
^^^^^^^^^^^^^^^^^^^^^^^

(`#258 <https://github.com/zscaler/zscaler-sdk-python/pull/258>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /cloudApplications/policy` Retrieves a list of Predefined and User Defined Cloud Applications associated with the DLP rules, Cloud App Control rules, Advanced Settings, Bandwidth Classes, and File Type Control rules.
  - Added `GET /cloudApplications/sslPolicy` Retrieves a list of Predefined and User Defined Cloud Applications associated with the SSL Inspection rules.

ZIA Shadow IT Report
^^^^^^^^^^^^^^^^^^^^

(`#258 <https://github.com/zscaler/zscaler-sdk-python/pull/258>`_) - Added the following new ZIA API Endpoints:
- Added `PUT /cloudApplications/bulkUpdate` To Update application status and tag information for predefined or custom cloud applications based on the IDs specified
- Added `GET /cloudApplications/lite` Gets the list of predefined and custom cloud applications
- Added `GET /customTags` Gets the list of custom tags available to assign to cloud applications
- Added `POST /shadowIT/applications/export` Export the Shadow IT Report (in CSV format) for the cloud applications recognized by Zscaler based on their usage in your organization.
- Added `POST /shadowIT/applications/{entity}/exportCsv` Export the Shadow IT Report (in CSV format) for the list of users or known locations identified with using the cloud applications specified in the request.

ZIA Remote Assistance Support
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#258 <https://github.com/zscaler/zscaler-sdk-python/pull/258>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /remoteAssistance` to retrieve information about the Remote Assistance option.
  - Added `PUT /remoteAssistance` to update information about the Remote Assistance option. Using this option, you can allow Zscaler Support to access your organization’s ZIA Admin Portal for a specified time period to troubleshoot issues.

ZIA Organization Details
^^^^^^^^^^^^^^^^^^^^^^^^^

(`#258 <https://github.com/zscaler/zscaler-sdk-python/pull/258>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /orgInformation` to retrieve detailed organization information, including headquarter location, geolocation, address, and contact details.
  - Added `GET /orgInformation/lite` to retrieve minimal organization information.
  - Added `GET /subscriptions` to retrieve information about the list of subscriptions enabled for your tenant. Subscriptions define the various features and levels of functionality that are available to your organization.

ZIA End User Notification
^^^^^^^^^^^^^^^^^^^^^^^^^^
(`#258 <https://github.com/zscaler/zscaler-sdk-python/pull/258>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /eun` to retrieve information browser-based end user notification (EUN) configuration details.
  - Added `PUT /eun` to update the browser-based end user notification (EUN) configuration details.

ZIA Admin Audit Logs
^^^^^^^^^^^^^^^^^^^^^^^

(`#258 <https://github.com/zscaler/zscaler-sdk-python/pull/258>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /auditlogEntryReport` to retrieve the status of a request for an audit log report.
  - Added `POST /auditlogEntryReport` to create an audit log report for the specified time period and saves it as a CSV file.
  - Added `DELETE /auditlogEntryReport` to cancel the request to create an audit log report.
  - Added `GET /auditlogEntryReport/download` to download the most recently created audit log report.

ZIA Extranets
^^^^^^^^^^^^^^^^^^

(`#258 <https://github.com/zscaler/zscaler-sdk-python/pull/258>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /extranet` to retrieve the list of extranets configured for the organization
  - Added `GET /extranet/lite` Retrieves the name-ID pairs of all extranets configured for an organization
  - Added `GET /extranet/{Id}` Retrieves information about an extranet based on the specified ID.
  - Added `POST /extranet` Adds a new extranet for the organization.
  - Added `PUT /extranet/{Id}` Updates an extranet based on the specified ID
  - Added `DELETE /extranet/{Id}` Deletes an extranet based on the specified ID

ZIA IOT Endpoint
^^^^^^^^^^^^^^^^^^

(`#258 <https://github.com/zscaler/zscaler-sdk-python/pull/258>`_) - Added the following new ZIA IOT API Endpoints:
  - Added `GET /iotDiscovery/deviceTypes` Retrieve the mapping between device type universally unique identifier (UUID) values and the device type names for all the device types supported by the Zscaler AI/ML.
  - Added `GET /iotDiscovery/categories` Retrieve the mapping between the device category universally unique identifier (UUID) values and the category names for all the device categories supported by the Zscaler AI/ML. The parent of device category is device type.
  - Added `GET /iotDiscovery/classifications` Retrieve the mapping between the device classification universally unique identifier (UUID) values and the classification names for all the device classifications supported by Zscaler AI/ML. The parent of device classification is device category.
  - Added `GET /iotDiscovery/deviceList` Retrieve a list of discovered devices with the following key contexts, IP address, location, ML auto-label, classification, category, and type.

ZIA 3rd-Party App Governance
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#258 <https://github.com/zscaler/zscaler-sdk-python/pull/258>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /apps/app` to search the 3rd-Party App Governance App Catalog by either app ID or URL.
  - Added `POST /apps/app` to submis an app for analysis in the 3rd-Party App Governance Sandbox.
  - Added `GET /apps/search` to search for an app by name. Any app whose name contains the search term (appName) is returned.
  - Added `GET /app_views/list` to retrieve the list of custom views that you have configured in the 3rd-Party App Governance.
  - Added `GET /app_views/{appViewId}/apps` to retrieves all assets (i.e., apps) that are related to a specified argument (i.e., custom view).

ZIA Admin Role Endpoints
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#258 <https://github.com/zscaler/zscaler-sdk-python/pull/258>`_) - Added the following new ZIA API Endpoints:
    - Added `GET /adminRoles/{roleId}` Retrieves the admin role based on the specified ID
    - Added `GET /adminRoles/lite` Retrieves a name and ID dictionary of all admin roles. The list only includes the name and ID for all admin roles.
    - Added `POST /adminRoles` Adds an admin role.
    - Added `PUT /adminRoles/{roleId}` Updates the admin role based on the specified ID.
    - Added `DELETE /adminRoles/{roleId}` Deletes the admin role based on the specified ID.

ZPA Credential Pool (New)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#258 <https://github.com/zscaler/zscaler-sdk-python/pull/258>`_) - Added new ZPA endpoint:
  - Added `GET /credential-pool` Gets the privileged credential pool details for the specified customer.
  - Added `GET /credential-pool/{id}` Gets the privileged credential pool details for the specified customer.
  - Added `GET /credential-pool/{id}/credential` Given Privileged credential pool id gets mapped privileged credential info
  - Added `POST /credential-pool` Adds a new privileged credential pool for the specified customer.
  - Added `PUT /credential-pool/{id}` Updates the existing credential pool for the specified customer.
  - Added `DELETE /credential-pool/{id}` Updates the existing credential pool for the specified customer.

ZWA - Zscaler Workflow Automation (NEW)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#258 <https://github.com/zscaler/zscaler-sdk-python/pull/258>`_) - Added new ZWA endpoint:
  - Added `GET /dlp/v1/incidents/transactions/{transactionId}` Gets the list of all DLP incidents associated with the transaction ID
  - Added `GET /dlp/v1/incidents/{dlpIncidentId}` Gets the DLP incident details based on the incident ID.
  - Added `DELETE /dlp/v1/incidents/{dlpIncidentId}` Deletes the DLP incident for the specified incident ID.
  - Added `GET /dlp/v1/incidents{dlpIncidentId}/change-history` Gets the details of updates made to an incident based on the given ID and timeline.
  - Added `GET /dlp/v1/incidents/{dlpIncidentId}/tickets` Gets the information of the ticket generated for the incident. For example, ticket type, ticket ID, ticket status, etc.
  - Added `POST /dlp/v1/incidents/{dlpIncidentId}/incident-groups/search` Filters a list of DLP incident groups to which the specified incident ID belongs.
  - Added `POST /dlp/v1/incidents/{dlpIncidentId}/close` Updates the status of the incident to resolved and closes the incident with a resolution label and a resolution code.
  - Added `POST /dlp/v1/incidents/{dlpIncidentId}/notes` Adds notes to the incident during updates or status changes.
  - Added `POST /dlp/v1/incidents/{dlpIncidentId}/labels` Assign lables (a label name and it's associated value) to DLP incidents.
  - Added `POST /dlp/v1/incidents/search` Filters DLP incidents based on the given time range and the field values.
  - Added `GET /dlp/v1/incidents/{dlpIncidentId}/triggers` Downloads the actual data that triggered the incident.
  - Added `GET /dlp/v1/incidents/{dlpIncidentId}/evidence` Gets the evidence URL of the incident.

Cloud & Branch Connector - OneAPI Support
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(`#258 <https://github.com/zscaler/zscaler-sdk-python/pull/258>`_) - Cloud & Branch Connector package is now compatible with OneAPI and Legacy API framework. Please refer to README for details.
(`#258 <https://github.com/zscaler/zscaler-sdk-python/pull/258>`_) - Cloud & Branch Connector package has been renamed from `zcon` to `ztw`

ZTW Policy Management
^^^^^^^^^^^^^^^^^^^^^^^

(`#258 <https://github.com/zscaler/zscaler-sdk-python/pull/258>`_) - Added the following new ZTW API Endpoints:
    - Added `GET /ecRules/ecRdr` Retrieves the list of traffic forwarding rules.
    - Added `PUT /ecRules/ecRdr/{ruleId}` Updates a traffic forwarding rule configuration based on the specified ID.
    - Added `POST /ecRules/ecRdr` Creates a new traffic forwarding rule.
    - Added `GET /ecRules/ecRdr/count` Retrieves the count of traffic forwarding rules available in the Cloud & Branch Connector Admin Portal.

ZTW Policy Resources
^^^^^^^^^^^^^^^^^^^^^

(`#258 <https://github.com/zscaler/zscaler-sdk-python/pull/258>`_) - Added the following new ZTW API Endpoints:
    - Added `GET /ipSourceGroups` Retrieves the list of source IP groups.
    - Added `GET /ipSourceGroups/lite` Retrieves the list of source IP groups. This request retrieves basic information about the source IP groups, such as name and ID. For extensive details, use the GET /ipSourceGroups request.
    - Added `POST /ipSourceGroups` Adds a new custom source IP group.
    - Added `DELETE /ipSourceGroups/{ipGroupId}` Deletes a source IP group based on the specified ID.
    - Added `GET /ipDestinationGroups` Retrieves the list of destination IP groups.
    - Added `GET /ipDestinationGroups/lite` Retrieves the list of destination IP groups. This request retrieves basic information about the destination IP groups, ID, name, and type. For extensive details, use the GET /ipDestinationGroups request.
    - Added `POST /ipDestinationGroups` Adds a new custom destination IP group.
    - Added `DELETE /ipDestinationGroups/{ipGroupId}` Deletes the destination IP group based on the specified ID. Default destination groups that are automatically created cannot be deleted.
    - Added `GET /ipGroups` Retrieves the list of IP pools.
    - Added `GET /ipGroups/lite` Retrieves the list of IP pools. This request retrieves basic information about the IP pools, such as name and ID. For extensive details, use the GET /ipGroups request.
    - Added `POST /ipGroups` Adds a new custom IP pool.
    - Added `DELETE /ipGroups/{ipGroupId}` Deletes an IP pool based on the specified ID.
    - Added `GET /networkServices` Retrieves the list of all network services. The search parameters find matching values within the name or description attributes.
    - Added `POST /networkServices` Creates a new network service.
    - Added `PUT /networkServices/{serviceId}` Updates the network service information for the specified service ID.
    - Added `DELETE /networkServices/{serviceId}` Deletes the network service for the specified ID.
    - Added `GET /networkServicesGroups` Retrieves the list of network service groups.
    - Added `GET /zpaResources/applicationSegments` Retrieves the list of ZPA application segments that can be configured in traffic forwarding rule criteria.

1.0.1 (April, 22 2025) - BREAKING CHANGES
-----------------------------------------

Notes
-----

- Python Versions: **v3.8, v3.9, v3.10, v3.11**


Zscaler OneAPI Support
-----------------------

(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_): Added support for (`OneAPI <https://help.zscaler.com/zidentity/what-zidentity>`_) Oauth2 authentication support through (`Zidentity <https://help.zscaler.com/zidentity/what-zidentity>`_)

**NOTES**
  - Starting at v1.0.0 version this SDK provides dual API client functionality and is backwards compatible with the legacy Zscaler API framework.
  - The new OneAPI framework is compatible only with the following products `ZCC/ZIA/ZPA`.
  - The following products `ZTW` - Cloud Connector and `ZDX` and Zscaler Digital Experience, authentication methods remain unnaffected.
  - The package `ZCON` (Zscaler Cloud and Branch Connector) has been renamed to `ZTW`
  - The following products `ZWA` - Zscaler Workflow Automation authentication methods remain unnaffected.

Refer to the (`README <hhttps://github.com/zscaler/zscaler-sdk-python/blob/master/README.md>`_) page for details on client instantiation, and authentication requirements on each individual product.

**WARNING**: Attention Government customers. OneAPI and Zidentity is not currently supported for the following ZIA clouds: `zscalergov` and `zscalerten` or ZPA `GOV`, and `GOVUS`. 
See the Zscaler Legacy API Framework section in the (`README Docs <https://zscaler-sdk-python.readthedocs.io/en/latest/index.html>`_) for more information on how authenticate to these environments using the built-in Legacy API method.

(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_): All API clients now support Config Setter object `ZCC/ZTW/ZDX/ZIA/ZPA/ZWA`

ZCC New Endpoints
^^^^^^^^^^^^^^^^^

(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Added the following new ZCC API Endpoints:
  - Added `GET /downloadServiceStatus` to download service status for all devices.
  - Added `GET /getDeviceCleanupInfo` to retrieve device cleanup information.
  - Added `PUT /setDeviceCleanupInfo` to cleanup device information.
  - Added `GET /getDeviceDetails` to retrieve device detailed information.
  - Added `GET /getAdminUsers` to retrieve mobile portal admin user.
  - Added `PUT /editAdminUser` to update mobile portal admin user.
  - Added `GET /getAdminUsersSyncInfo` to retrieve mobile portal admin user sync information.
  - Added `POST /syncZiaZdxAdminUsers` to retrieve mobile portal admin users ZIA and ZDX sync information.
  - Added `POST /syncZpaAdminUsers` to retrieve mobile portal admin users ZPA sync information.
  - Added `GET /getAdminRoles` to retrieve mobile portal admin roles.
  - Added `GET /getCompanyInfo` to retrieve company information.
  - Added `GET /getZdxGroupEntitlements` to retrieve ZDX Group entitlement enablement.
  - Added `PUT /updateZdxGroupEntitlement` to retrieve ZDX Group entitlement enablement.
  - Added `GET /updateZpaGroupEntitlement` to retrieve ZPA Group entitlement enablement.
  - Added `GET /web/policy/listByCompany` to retrieve Web Policy By Company ID.
  - Added `PUT /web/policy/activate` to activate mobile portal web policy
  - Added `PUT /web/policy/edit` to update mobile portal web policy
  - Added `DELETE /web/policy/{policyId}/delete` to delete mobile portal web policy.
  - Added `GET /webAppService/listByCompany` to retrieve Web App Service information By Company ID.
  - Added `GET /webFailOpenPolicy/listByCompany` to retrieve web Fail Open Policy information By Company ID.
  - Added `PUT /webFailOpenPolicy/edit` to update mobile portal web Fail Open Policy.
  - Added `GET /webForwardingProfile/listByCompany` to retrieve Web Forwarding Profile information By Company ID.
  - Added `POST /webForwardingProfile/edit` to create a Web Forwarding Profile.
  - Added `DELETE /webForwardingProfile/{profileId}/delete` to delete Web Forwarding Profile.
  - Added `GET /webTrustedNetwork/listByCompany` to retrieve multiple Web Trusted Network information By Company ID.
  - Added `POST /webTrustedNetwork/edit` to create Web Trusted Network resource.
  - Added `PUT /webTrustedNetwork/edit` to update Web Trusted Network resource.
  - Added `DELETE /webTrustedNetwork/{networkId}/delete` to delete Web Trusted Network resource.
  - Added `GET /getWebPrivacyInfo` to retrieve Web Privacy Info.
  - Added `GET /setWebPrivacyInfo` to update Web Privacy Info.

ZIA Sandbox Submission - BREAKING CHANGES
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Authentication to Zscaler Sandbox now use the following attributes during client instantiation.
 - `sandboxToken` - Can also be sourced from the `ZSCALER_SANDBOX_TOKEN` environment variable.
 - `sandboxCloud` - Can also be sourced from the `ZSCALER_SANDBOX_CLOUD` environment variable.

**NOTE** The previous `ZIA_SANDBOX_TOKEN` has been deprecated.

ZIA Sandbox Rules
^^^^^^^^^^^^^^^^^^

(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /sandboxRules` to retrieve the list of all Sandbox policy rules.
  - Added `GET /sandboxRules/{ruleId}` to retrieve the Sandbox policy rule information based on the specified ID.
  - Added `POST /sandboxRules` to add a Sandbox policy rule.
  - Added `PUT /sandboxRules/{ruleId}` to update the Sandbox policy rule configuration for the specified ID.
  - Added `DELETE /sandboxRules/{ruleId}` to delete the Sandbox policy rule based on the specified ID.

ZIA DNS Control Rules
^^^^^^^^^^^^^^^^^^^^^^

(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /firewallDnsRules` to retrieve the list of all DNS Control policy rules.
  - Added `GET /firewallDnsRules/{ruleId}` to retrieve the DNS Control policy rule information based on the specified ID.
  - Added `POST /firewallDnsRules` to add a DNS Control policy rules.
  - Added `PUT /firewallDnsRules/{ruleId}` to update the DNS Control policy rule configuration for the specified ID.
  - Added `DELETE /firewallDnsRules/{ruleId}` to delete the DNS Control policy rule based on the specified ID.

ZIA IPS Control Rules
^^^^^^^^^^^^^^^^^^^^^

(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /firewallIpsRules` to retrieve the list of all IPS Control policy rules.
  - Added `GET /firewallIpsRules/{ruleId}` to retrieve the IPS Control policy rule information based on the specified ID.
  - Added `POST /firewallIpsRules` to add a IPS Control policy rule.
  - Added `PUT /firewallIpsRules/{ruleId}` to update the IPS Control policy rule configuration for the specified ID.
  - Added `DELETE /firewallIpsRules/{ruleId}` to delete the IPS Control policy rule based on the specified ID.

ZIA File Type Control Policy
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /fileTypeRules` to retrieve the list of all File Type Control policy rules.
  - Added `GET /fileTypeRules/lite` to retrieve the list of all File Type Control policy rules.
  - Added `GET /fileTypeRules/{ruleId}` to retrieve the File Type Control policy rule information based on the specified ID.
  - Added `POST /fileTypeRules` to add a File Type Control policy rule.
  - Added `PUT /fileTypeRules/{ruleId}` to update the File Type Control policy rule configuration for the specified ID.
  - Added `DELETE /fileTypeRules/{ruleId}` to delete the File Type Control policy rule based on the specified ID.

ZIA Forwarding Control Policy - Proxy Gateways
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /proxyGateways` to retrieve the proxy gateway information.
  - Added `GET /proxyGateways/lite` to retrieve the name and ID of the proxy.

ZIA Cloud Nanolog Streaming Service (NSS)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /nssFeeds` to retrieve the cloud NSS feeds.
  - Added `GET /nssFeeds/{feedId}` to retrieve information about cloud NSS feed based on the specified ID.
  - Added `POST /nssFeeds` to add a new cloud NSS feed.
  - Added `PUT /nssFeeds/{feedId}` to update cloud NSS feed configuration based on the specified ID.
  - Added `DELETE /nssFeeds/{feedId}` to delete cloud NSS feed configuration based on the specified ID.
  - Added `GET /nssFeeds/feedOutputDefaults` to retrieve the default cloud NSS feed output format for different log types.
  - Added `GET /nssFeeds/testConnectivity/{feedId}` to test the connectivity of cloud NSS feed based on the specified ID
  - Added `POST /nssFeeds/validateFeedFormat` to validates the cloud NSS feed format and returns the validation result

ZIA Advanced Threat Protection Policy
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /cyberThreatProtection/advancedThreatSettings` to retrieve the advanced threat configuration settings.
  - Added `PUT /cyberThreatProtection/advancedThreatSettings` to update the advanced threat configuration settings.
  - Added `GET /cyberThreatProtection/maliciousUrls` to retrieve the malicious URLs added to the denylist in the Advanced Threat Protection (ATP) policy
  - Added `PUT /cyberThreatProtection/maliciousUrls` to updates the malicious URLs added to the denylist in ATP policy
  - Added `GET /cyberThreatProtection/securityExceptions` to retrieves information about the security exceptions configured for the ATP policy
  - Added `PUT /cyberThreatProtection/securityExceptions` to update security exceptions for the ATP policy

ZIA Advanced Threat Protection Policy
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /cyberThreatProtection/atpMalwareInspection` to retrieve the traffic inspection configurations of Malware Protection policy
  - Added `PUT /cyberThreatProtection/atpMalwareInspection` to update the traffic inspection configurations of Malware Protection policy.
  - Added `GET /cyberThreatProtection/atpMalwareProtocols` to retrieve the protocol inspection configurations of Malware Protection policy
  - Added `PUT /cyberThreatProtection/atpMalwareProtocols` to update the protocol inspection configurations of Malware Protection policy.
  - Added `GET /cyberThreatProtection/malwareSettings` to retrieve the malware protection policy configuration details
  - Added `PUT /cyberThreatProtection/malwareSettings` to update the malware protection policy configuration details.
  - Added `GET /cyberThreatProtection/malwarePolicy` to retrieve information about the security exceptions configured for the Malware Protection policy
  - Added `PUT /cyberThreatProtection/malwarePolicy` to update security exceptions for the Malware Protection policy.

ZIA URL & Cloud App Control Policy Settings
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /advancedUrlFilterAndCloudAppSettings` to retrieve information about URL and Cloud App Control advanced policy settings
  - Added `PUT /advancedUrlFilterAndCloudAppSettings` to update the URL and Cloud App Control advanced policy settings

ZIA Authentication Settings
^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /authSettings` to retrieve the organization's default authentication settings information, including authentication profile and Kerberos authentication information.
  - Added `GET /authSettings/lite` to retrieve organization's default authentication settings information.
  - Added `PUT /authSettings` to update the organization's default authentication settings information.

ZIA Advanced Settings
^^^^^^^^^^^^^^^^^^^^^

(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /advancedSettings` to retrieve information about the advanced settings.
  - Added `PUT /advancedSettings` to update the advanced settings configuration.

ZIA Cloud Applications
^^^^^^^^^^^^^^^^^^^^^^^

(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /cloudApplications/policy` Retrieves a list of Predefined and User Defined Cloud Applications associated with the DLP rules, Cloud App Control rules, Advanced Settings, Bandwidth Classes, and File Type Control rules.
  - Added `GET /cloudApplications/sslPolicy` Retrieves a list of Predefined and User Defined Cloud Applications associated with the SSL Inspection rules.

ZIA Shadow IT Report
^^^^^^^^^^^^^^^^^^^^

(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Added the following new ZIA API Endpoints:
- Added `PUT /cloudApplications/bulkUpdate` To Update application status and tag information for predefined or custom cloud applications based on the IDs specified
- Added `GET /cloudApplications/lite` Gets the list of predefined and custom cloud applications
- Added `GET /customTags` Gets the list of custom tags available to assign to cloud applications
- Added `POST /shadowIT/applications/export` Export the Shadow IT Report (in CSV format) for the cloud applications recognized by Zscaler based on their usage in your organization.
- Added `POST /shadowIT/applications/{entity}/exportCsv` Export the Shadow IT Report (in CSV format) for the list of users or known locations identified with using the cloud applications specified in the request.

ZIA Remote Assistance Support
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /remoteAssistance` to retrieve information about the Remote Assistance option.
  - Added `PUT /remoteAssistance` to update information about the Remote Assistance option. Using this option, you can allow Zscaler Support to access your organization’s ZIA Admin Portal for a specified time period to troubleshoot issues.

ZIA Organization Details
^^^^^^^^^^^^^^^^^^^^^^^^^

(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /orgInformation` to retrieve detailed organization information, including headquarter location, geolocation, address, and contact details.
  - Added `GET /orgInformation/lite` to retrieve minimal organization information.
  - Added `GET /subscriptions` to retrieve information about the list of subscriptions enabled for your tenant. Subscriptions define the various features and levels of functionality that are available to your organization.

ZIA End User Notification
^^^^^^^^^^^^^^^^^^^^^^^^^^
(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /eun` to retrieve information browser-based end user notification (EUN) configuration details.
  - Added `PUT /eun` to update the browser-based end user notification (EUN) configuration details.

ZIA Admin Audit Logs
^^^^^^^^^^^^^^^^^^^^^^^

(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /auditlogEntryReport` to retrieve the status of a request for an audit log report.
  - Added `POST /auditlogEntryReport` to create an audit log report for the specified time period and saves it as a CSV file.
  - Added `DELETE /auditlogEntryReport` to cancel the request to create an audit log report.
  - Added `GET /auditlogEntryReport/download` to download the most recently created audit log report.

ZIA Extranets
^^^^^^^^^^^^^^^^^^

(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /extranet` to retrieve the list of extranets configured for the organization
  - Added `GET /extranet/lite` Retrieves the name-ID pairs of all extranets configured for an organization
  - Added `GET /extranet/{Id}` Retrieves information about an extranet based on the specified ID.
  - Added `POST /extranet` Adds a new extranet for the organization.
  - Added `PUT /extranet/{Id}` Updates an extranet based on the specified ID
  - Added `DELETE /extranet/{Id}` Deletes an extranet based on the specified ID

ZIA IOT Endpoint
^^^^^^^^^^^^^^^^^^

(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Added the following new ZIA IOT API Endpoints:
  - Added `GET /iotDiscovery/deviceTypes` Retrieve the mapping between device type universally unique identifier (UUID) values and the device type names for all the device types supported by the Zscaler AI/ML.
  - Added `GET /iotDiscovery/categories` Retrieve the mapping between the device category universally unique identifier (UUID) values and the category names for all the device categories supported by the Zscaler AI/ML. The parent of device category is device type.
  - Added `GET /iotDiscovery/classifications` Retrieve the mapping between the device classification universally unique identifier (UUID) values and the classification names for all the device classifications supported by Zscaler AI/ML. The parent of device classification is device category.
  - Added `GET /iotDiscovery/deviceList` Retrieve a list of discovered devices with the following key contexts, IP address, location, ML auto-label, classification, category, and type.

ZIA 3rd-Party App Governance
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /apps/app` to search the 3rd-Party App Governance App Catalog by either app ID or URL.
  - Added `POST /apps/app` to submis an app for analysis in the 3rd-Party App Governance Sandbox.
  - Added `GET /apps/search` to search for an app by name. Any app whose name contains the search term (appName) is returned.
  - Added `GET /app_views/list` to retrieve the list of custom views that you have configured in the 3rd-Party App Governance.
  - Added `GET /app_views/{appViewId}/apps` to retrieves all assets (i.e., apps) that are related to a specified argument (i.e., custom view).

ZIA Admin Role Endpoints
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Added the following new ZIA API Endpoints:
    - Added `GET /adminRoles/{roleId}` Retrieves the admin role based on the specified ID
    - Added `GET /adminRoles/lite` Retrieves a name and ID dictionary of all admin roles. The list only includes the name and ID for all admin roles.
    - Added `POST /adminRoles` Adds an admin role.
    - Added `PUT /adminRoles/{roleId}` Updates the admin role based on the specified ID.
    - Added `DELETE /adminRoles/{roleId}` Deletes the admin role based on the specified ID.

ZPA Credential Pool (New)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Added new ZPA endpoint:
  - Added `GET /credential-pool` Gets the privileged credential pool details for the specified customer.
  - Added `GET /credential-pool/{id}` Gets the privileged credential pool details for the specified customer.
  - Added `GET /credential-pool/{id}/credential` Given Privileged credential pool id gets mapped privileged credential info
  - Added `POST /credential-pool` Adds a new privileged credential pool for the specified customer.
  - Added `PUT /credential-pool/{id}` Updates the existing credential pool for the specified customer.
  - Added `DELETE /credential-pool/{id}` Updates the existing credential pool for the specified customer.

ZWA - Zscaler Workflow Automation (NEW)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Added new ZWA endpoint:
  - Added `GET /dlp/v1/incidents/transactions/{transactionId}` Gets the list of all DLP incidents associated with the transaction ID
  - Added `GET /dlp/v1/incidents/{dlpIncidentId}` Gets the DLP incident details based on the incident ID.
  - Added `DELETE /dlp/v1/incidents/{dlpIncidentId}` Deletes the DLP incident for the specified incident ID.
  - Added `GET /dlp/v1/incidents{dlpIncidentId}/change-history` Gets the details of updates made to an incident based on the given ID and timeline.
  - Added `GET /dlp/v1/incidents/{dlpIncidentId}/tickets` Gets the information of the ticket generated for the incident. For example, ticket type, ticket ID, ticket status, etc.
  - Added `POST /dlp/v1/incidents/{dlpIncidentId}/incident-groups/search` Filters a list of DLP incident groups to which the specified incident ID belongs.
  - Added `POST /dlp/v1/incidents/{dlpIncidentId}/close` Updates the status of the incident to resolved and closes the incident with a resolution label and a resolution code.
  - Added `POST /dlp/v1/incidents/{dlpIncidentId}/notes` Adds notes to the incident during updates or status changes.
  - Added `POST /dlp/v1/incidents/{dlpIncidentId}/labels` Assign lables (a label name and it's associated value) to DLP incidents.
  - Added `POST /dlp/v1/incidents/search` Filters DLP incidents based on the given time range and the field values.
  - Added `GET /dlp/v1/incidents/{dlpIncidentId}/triggers` Downloads the actual data that triggered the incident.
  - Added `GET /dlp/v1/incidents/{dlpIncidentId}/evidence` Gets the evidence URL of the incident.

Cloud & Branch Connector - OneAPI Support
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Cloud & Branch Connector package is now compatible with OneAPI and Legacy API framework. Please refer to README for details.
(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Cloud & Branch Connector package has been renamed from `zcon` to `ztw`

ZTW Policy Management
^^^^^^^^^^^^^^^^^^^^^^^

(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Added the following new ZTW API Endpoints:
    - Added `GET /ecRules/ecRdr` Retrieves the list of traffic forwarding rules.
    - Added `PUT /ecRules/ecRdr/{ruleId}` Updates a traffic forwarding rule configuration based on the specified ID.
    - Added `POST /ecRules/ecRdr` Creates a new traffic forwarding rule.
    - Added `GET /ecRules/ecRdr/count` Retrieves the count of traffic forwarding rules available in the Cloud & Branch Connector Admin Portal.

ZTW Policy Resources
^^^^^^^^^^^^^^^^^^^^^

(`#257 <https://github.com/zscaler/zscaler-sdk-python/pull/257>`_) - Added the following new ZTW API Endpoints:
    - Added `GET /ipSourceGroups` Retrieves the list of source IP groups.
    - Added `GET /ipSourceGroups/lite` Retrieves the list of source IP groups. This request retrieves basic information about the source IP groups, such as name and ID. For extensive details, use the GET /ipSourceGroups request.
    - Added `POST /ipSourceGroups` Adds a new custom source IP group.
    - Added `DELETE /ipSourceGroups/{ipGroupId}` Deletes a source IP group based on the specified ID.
    - Added `GET /ipDestinationGroups` Retrieves the list of destination IP groups.
    - Added `GET /ipDestinationGroups/lite` Retrieves the list of destination IP groups. This request retrieves basic information about the destination IP groups, ID, name, and type. For extensive details, use the GET /ipDestinationGroups request.
    - Added `POST /ipDestinationGroups` Adds a new custom destination IP group.
    - Added `DELETE /ipDestinationGroups/{ipGroupId}` Deletes the destination IP group based on the specified ID. Default destination groups that are automatically created cannot be deleted.
    - Added `GET /ipGroups` Retrieves the list of IP pools.
    - Added `GET /ipGroups/lite` Retrieves the list of IP pools. This request retrieves basic information about the IP pools, such as name and ID. For extensive details, use the GET /ipGroups request.
    - Added `POST /ipGroups` Adds a new custom IP pool.
    - Added `DELETE /ipGroups/{ipGroupId}` Deletes an IP pool based on the specified ID.
    - Added `GET /networkServices` Retrieves the list of all network services. The search parameters find matching values within the name or description attributes.
    - Added `POST /networkServices` Creates a new network service.
    - Added `PUT /networkServices/{serviceId}` Updates the network service information for the specified service ID.
    - Added `DELETE /networkServices/{serviceId}` Deletes the network service for the specified ID.
    - Added `GET /networkServicesGroups` Retrieves the list of network service groups.
    - Added `GET /zpaResources/applicationSegments` Retrieves the list of ZPA application segments that can be configured in traffic forwarding rule criteria.

1.0.1 (April, 22 2025) - BREAKING CHANGES
-----------------------------------------

Notes
-----

- Python Versions: **v3.8, v3.9, v3.10, v3.11**


Zscaler OneAPI Support
-----------------------

(`#256 <https://github.com/zscaler/zscaler-sdk-python/pull/256>`_): Added support for (`OneAPI <https://help.zscaler.com/zidentity/what-zidentity>`_) Oauth2 authentication support through (`Zidentity <https://help.zscaler.com/zidentity/what-zidentity>`_)

**NOTES**
  - Starting at v1.0.0 version this SDK provides dual API client functionality and is backwards compatible with the legacy Zscaler API framework.
  - The new OneAPI framework is compatible only with the following products `ZCC/ZIA/ZPA`.
  - The following products `ZTW` - Cloud Connector and `ZDX` and Zscaler Digital Experience, authentication methods remain unnaffected.
  - The package `ZCON` (Zscaler Cloud and Branch Connector) has been renamed to `ZTW`
  - The following products `ZWA` - Zscaler Workflow Automation authentication methods remain unnaffected.

Refer to the (`README <hhttps://github.com/zscaler/zscaler-sdk-python/blob/master/README.md>`_) page for details on client instantiation, and authentication requirements on each individual product.

**WARNING**: Attention Government customers. OneAPI and Zidentity is not currently supported for the following ZIA clouds: `zscalergov` and `zscalerten` or ZPA `GOV`, and `GOVUS`. 
See the Zscaler Legacy API Framework section in the (`README Docs <https://zscaler-sdk-python.readthedocs.io/en/latest/index.html>`_) for more information on how authenticate to these environments using the built-in Legacy API method.

(`#256 <https://github.com/zscaler/zscaler-sdk-python/pull/256>`_): All API clients now support Config Setter object `ZCC/ZTW/ZDX/ZIA/ZPA/ZWA`

ZCC New Endpoints
^^^^^^^^^^^^^^^^^

(`#256 <https://github.com/zscaler/zscaler-sdk-python/pull/256>`_) - Added the following new ZCC API Endpoints:
  - Added `GET /downloadServiceStatus` to download service status for all devices.
  - Added `GET /getDeviceCleanupInfo` to retrieve device cleanup information.
  - Added `PUT /setDeviceCleanupInfo` to cleanup device information.
  - Added `GET /getDeviceDetails` to retrieve device detailed information.
  - Added `GET /getAdminUsers` to retrieve mobile portal admin user.
  - Added `PUT /editAdminUser` to update mobile portal admin user.
  - Added `GET /getAdminUsersSyncInfo` to retrieve mobile portal admin user sync information.
  - Added `POST /syncZiaZdxAdminUsers` to retrieve mobile portal admin users ZIA and ZDX sync information.
  - Added `POST /syncZpaAdminUsers` to retrieve mobile portal admin users ZPA sync information.
  - Added `GET /getAdminRoles` to retrieve mobile portal admin roles.
  - Added `GET /getCompanyInfo` to retrieve company information.
  - Added `GET /getZdxGroupEntitlements` to retrieve ZDX Group entitlement enablement.
  - Added `PUT /updateZdxGroupEntitlement` to retrieve ZDX Group entitlement enablement.
  - Added `GET /updateZpaGroupEntitlement` to retrieve ZPA Group entitlement enablement.
  - Added `GET /web/policy/listByCompany` to retrieve Web Policy By Company ID.
  - Added `PUT /web/policy/activate` to activate mobile portal web policy
  - Added `PUT /web/policy/edit` to update mobile portal web policy
  - Added `DELETE /web/policy/{policyId}/delete` to delete mobile portal web policy.
  - Added `GET /webAppService/listByCompany` to retrieve Web App Service information By Company ID.
  - Added `GET /webFailOpenPolicy/listByCompany` to retrieve web Fail Open Policy information By Company ID.
  - Added `PUT /webFailOpenPolicy/edit` to update mobile portal web Fail Open Policy.
  - Added `GET /webForwardingProfile/listByCompany` to retrieve Web Forwarding Profile information By Company ID.
  - Added `POST /webForwardingProfile/edit` to create a Web Forwarding Profile.
  - Added `DELETE /webForwardingProfile/{profileId}/delete` to delete Web Forwarding Profile.
  - Added `GET /webTrustedNetwork/listByCompany` to retrieve multiple Web Trusted Network information By Company ID.
  - Added `POST /webTrustedNetwork/edit` to create Web Trusted Network resource.
  - Added `PUT /webTrustedNetwork/edit` to update Web Trusted Network resource.
  - Added `DELETE /webTrustedNetwork/{networkId}/delete` to delete Web Trusted Network resource.
  - Added `GET /getWebPrivacyInfo` to retrieve Web Privacy Info.
  - Added `GET /setWebPrivacyInfo` to update Web Privacy Info.

ZIA Sandbox Submission - BREAKING CHANGES
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#256 <https://github.com/zscaler/zscaler-sdk-python/pull/256>`_) - Authentication to Zscaler Sandbox now use the following attributes during client instantiation.
 - `sandboxToken` - Can also be sourced from the `ZSCALER_SANDBOX_TOKEN` environment variable.
 - `sandboxCloud` - Can also be sourced from the `ZSCALER_SANDBOX_CLOUD` environment variable.

**NOTE** The previous `ZIA_SANDBOX_TOKEN` has been deprecated.

ZIA Sandbox Rules
^^^^^^^^^^^^^^^^^^

(`#256 <https://github.com/zscaler/zscaler-sdk-python/pull/256>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /sandboxRules` to retrieve the list of all Sandbox policy rules.
  - Added `GET /sandboxRules/{ruleId}` to retrieve the Sandbox policy rule information based on the specified ID.
  - Added `POST /sandboxRules` to add a Sandbox policy rule.
  - Added `PUT /sandboxRules/{ruleId}` to update the Sandbox policy rule configuration for the specified ID.
  - Added `DELETE /sandboxRules/{ruleId}` to delete the Sandbox policy rule based on the specified ID.

ZIA DNS Control Rules
^^^^^^^^^^^^^^^^^^^^^^

(`#256 <https://github.com/zscaler/zscaler-sdk-python/pull/256>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /firewallDnsRules` to retrieve the list of all DNS Control policy rules.
  - Added `GET /firewallDnsRules/{ruleId}` to retrieve the DNS Control policy rule information based on the specified ID.
  - Added `POST /firewallDnsRules` to add a DNS Control policy rules.
  - Added `PUT /firewallDnsRules/{ruleId}` to update the DNS Control policy rule configuration for the specified ID.
  - Added `DELETE /firewallDnsRules/{ruleId}` to delete the DNS Control policy rule based on the specified ID.

ZIA IPS Control Rules
^^^^^^^^^^^^^^^^^^^^^

(`#256 <https://github.com/zscaler/zscaler-sdk-python/pull/256>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /firewallIpsRules` to retrieve the list of all IPS Control policy rules.
  - Added `GET /firewallIpsRules/{ruleId}` to retrieve the IPS Control policy rule information based on the specified ID.
  - Added `POST /firewallIpsRules` to add a IPS Control policy rule.
  - Added `PUT /firewallIpsRules/{ruleId}` to update the IPS Control policy rule configuration for the specified ID.
  - Added `DELETE /firewallIpsRules/{ruleId}` to delete the IPS Control policy rule based on the specified ID.

ZIA File Type Control Policy
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#256 <https://github.com/zscaler/zscaler-sdk-python/pull/256>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /fileTypeRules` to retrieve the list of all File Type Control policy rules.
  - Added `GET /fileTypeRules/lite` to retrieve the list of all File Type Control policy rules.
  - Added `GET /fileTypeRules/{ruleId}` to retrieve the File Type Control policy rule information based on the specified ID.
  - Added `POST /fileTypeRules` to add a File Type Control policy rule.
  - Added `PUT /fileTypeRules/{ruleId}` to update the File Type Control policy rule configuration for the specified ID.
  - Added `DELETE /fileTypeRules/{ruleId}` to delete the File Type Control policy rule based on the specified ID.

ZIA Forwarding Control Policy - Proxy Gateways
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#256 <https://github.com/zscaler/zscaler-sdk-python/pull/256>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /proxyGateways` to retrieve the proxy gateway information.
  - Added `GET /proxyGateways/lite` to retrieve the name and ID of the proxy.

ZIA Cloud Nanolog Streaming Service (NSS)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#256 <https://github.com/zscaler/zscaler-sdk-python/pull/256>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /nssFeeds` to retrieve the cloud NSS feeds.
  - Added `GET /nssFeeds/{feedId}` to retrieve information about cloud NSS feed based on the specified ID.
  - Added `POST /nssFeeds` to add a new cloud NSS feed.
  - Added `PUT /nssFeeds/{feedId}` to update cloud NSS feed configuration based on the specified ID.
  - Added `DELETE /nssFeeds/{feedId}` to delete cloud NSS feed configuration based on the specified ID.
  - Added `GET /nssFeeds/feedOutputDefaults` to retrieve the default cloud NSS feed output format for different log types.
  - Added `GET /nssFeeds/testConnectivity/{feedId}` to test the connectivity of cloud NSS feed based on the specified ID
  - Added `POST /nssFeeds/validateFeedFormat` to validates the cloud NSS feed format and returns the validation result

ZIA Advanced Threat Protection Policy
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#256 <https://github.com/zscaler/zscaler-sdk-python/pull/256>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /cyberThreatProtection/advancedThreatSettings` to retrieve the advanced threat configuration settings.
  - Added `PUT /cyberThreatProtection/advancedThreatSettings` to update the advanced threat configuration settings.
  - Added `GET /cyberThreatProtection/maliciousUrls` to retrieve the malicious URLs added to the denylist in the Advanced Threat Protection (ATP) policy
  - Added `PUT /cyberThreatProtection/maliciousUrls` to updates the malicious URLs added to the denylist in ATP policy
  - Added `GET /cyberThreatProtection/securityExceptions` to retrieves information about the security exceptions configured for the ATP policy
  - Added `PUT /cyberThreatProtection/securityExceptions` to update security exceptions for the ATP policy

ZIA Advanced Threat Protection Policy
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#256 <https://github.com/zscaler/zscaler-sdk-python/pull/256>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /cyberThreatProtection/atpMalwareInspection` to retrieve the traffic inspection configurations of Malware Protection policy
  - Added `PUT /cyberThreatProtection/atpMalwareInspection` to update the traffic inspection configurations of Malware Protection policy.
  - Added `GET /cyberThreatProtection/atpMalwareProtocols` to retrieve the protocol inspection configurations of Malware Protection policy
  - Added `PUT /cyberThreatProtection/atpMalwareProtocols` to update the protocol inspection configurations of Malware Protection policy.
  - Added `GET /cyberThreatProtection/malwareSettings` to retrieve the malware protection policy configuration details
  - Added `PUT /cyberThreatProtection/malwareSettings` to update the malware protection policy configuration details.
  - Added `GET /cyberThreatProtection/malwarePolicy` to retrieve information about the security exceptions configured for the Malware Protection policy
  - Added `PUT /cyberThreatProtection/malwarePolicy` to update security exceptions for the Malware Protection policy.

ZIA URL & Cloud App Control Policy Settings
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#256 <https://github.com/zscaler/zscaler-sdk-python/pull/256>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /advancedUrlFilterAndCloudAppSettings` to retrieve information about URL and Cloud App Control advanced policy settings
  - Added `PUT /advancedUrlFilterAndCloudAppSettings` to update the URL and Cloud App Control advanced policy settings

ZIA Authentication Settings
^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#256 <https://github.com/zscaler/zscaler-sdk-python/pull/256>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /authSettings` to retrieve the organization's default authentication settings information, including authentication profile and Kerberos authentication information.
  - Added `GET /authSettings/lite` to retrieve organization's default authentication settings information.
  - Added `PUT /authSettings` to update the organization's default authentication settings information.

ZIA Advanced Settings
^^^^^^^^^^^^^^^^^^^^^

(`#256 <https://github.com/zscaler/zscaler-sdk-python/pull/256>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /advancedSettings` to retrieve information about the advanced settings.
  - Added `PUT /advancedSettings` to update the advanced settings configuration.

ZIA Cloud Applications
^^^^^^^^^^^^^^^^^^^^^^^

(`#256 <https://github.com/zscaler/zscaler-sdk-python/pull/256>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /cloudApplications/policy` Retrieves a list of Predefined and User Defined Cloud Applications associated with the DLP rules, Cloud App Control rules, Advanced Settings, Bandwidth Classes, and File Type Control rules.
  - Added `GET /cloudApplications/sslPolicy` Retrieves a list of Predefined and User Defined Cloud Applications associated with the SSL Inspection rules.

ZIA Shadow IT Report
^^^^^^^^^^^^^^^^^^^^

(`#256 <https://github.com/zscaler/zscaler-sdk-python/pull/256>`_) - Added the following new ZIA API Endpoints:
- Added `PUT /cloudApplications/bulkUpdate` To Update application status and tag information for predefined or custom cloud applications based on the IDs specified
- Added `GET /cloudApplications/lite` Gets the list of predefined and custom cloud applications
- Added `GET /customTags` Gets the list of custom tags available to assign to cloud applications
- Added `POST /shadowIT/applications/export` Export the Shadow IT Report (in CSV format) for the cloud applications recognized by Zscaler based on their usage in your organization.
- Added `POST /shadowIT/applications/{entity}/exportCsv` Export the Shadow IT Report (in CSV format) for the list of users or known locations identified with using the cloud applications specified in the request.

ZIA Remote Assistance Support
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#256 <https://github.com/zscaler/zscaler-sdk-python/pull/256>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /remoteAssistance` to retrieve information about the Remote Assistance option.
  - Added `PUT /remoteAssistance` to update information about the Remote Assistance option. Using this option, you can allow Zscaler Support to access your organization’s ZIA Admin Portal for a specified time period to troubleshoot issues.

ZIA Organization Details
^^^^^^^^^^^^^^^^^^^^^^^^^

(`#256 <https://github.com/zscaler/zscaler-sdk-python/pull/256>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /orgInformation` to retrieve detailed organization information, including headquarter location, geolocation, address, and contact details.
  - Added `GET /orgInformation/lite` to retrieve minimal organization information.
  - Added `GET /subscriptions` to retrieve information about the list of subscriptions enabled for your tenant. Subscriptions define the various features and levels of functionality that are available to your organization.

ZIA End User Notification
^^^^^^^^^^^^^^^^^^^^^^^^^^
(`#256 <https://github.com/zscaler/zscaler-sdk-python/pull/256>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /eun` to retrieve information browser-based end user notification (EUN) configuration details.
  - Added `PUT /eun` to update the browser-based end user notification (EUN) configuration details.

ZIA Admin Audit Logs
^^^^^^^^^^^^^^^^^^^^^^^

(`#256 <https://github.com/zscaler/zscaler-sdk-python/pull/256>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /auditlogEntryReport` to retrieve the status of a request for an audit log report.
  - Added `POST /auditlogEntryReport` to create an audit log report for the specified time period and saves it as a CSV file.
  - Added `DELETE /auditlogEntryReport` to cancel the request to create an audit log report.
  - Added `GET /auditlogEntryReport/download` to download the most recently created audit log report.

ZIA Extranets
^^^^^^^^^^^^^^^^^^

(`#256 <https://github.com/zscaler/zscaler-sdk-python/pull/256>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /extranet` to retrieve the list of extranets configured for the organization
  - Added `GET /extranet/lite` Retrieves the name-ID pairs of all extranets configured for an organization
  - Added `GET /extranet/{Id}` Retrieves information about an extranet based on the specified ID.
  - Added `POST /extranet` Adds a new extranet for the organization.
  - Added `PUT /extranet/{Id}` Updates an extranet based on the specified ID
  - Added `DELETE /extranet/{Id}` Deletes an extranet based on the specified ID

ZIA IOT Endpoint
^^^^^^^^^^^^^^^^^^

(`#256 <https://github.com/zscaler/zscaler-sdk-python/pull/256>`_) - Added the following new ZIA IOT API Endpoints:
  - Added `GET /iotDiscovery/deviceTypes` Retrieve the mapping between device type universally unique identifier (UUID) values and the device type names for all the device types supported by the Zscaler AI/ML.
  - Added `GET /iotDiscovery/categories` Retrieve the mapping between the device category universally unique identifier (UUID) values and the category names for all the device categories supported by the Zscaler AI/ML. The parent of device category is device type.
  - Added `GET /iotDiscovery/classifications` Retrieve the mapping between the device classification universally unique identifier (UUID) values and the classification names for all the device classifications supported by Zscaler AI/ML. The parent of device classification is device category.
  - Added `GET /iotDiscovery/deviceList` Retrieve a list of discovered devices with the following key contexts, IP address, location, ML auto-label, classification, category, and type.

ZIA 3rd-Party App Governance
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#256 <https://github.com/zscaler/zscaler-sdk-python/pull/256>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /apps/app` to search the 3rd-Party App Governance App Catalog by either app ID or URL.
  - Added `POST /apps/app` to submis an app for analysis in the 3rd-Party App Governance Sandbox.
  - Added `GET /apps/search` to search for an app by name. Any app whose name contains the search term (appName) is returned.
  - Added `GET /app_views/list` to retrieve the list of custom views that you have configured in the 3rd-Party App Governance.
  - Added `GET /app_views/{appViewId}/apps` to retrieves all assets (i.e., apps) that are related to a specified argument (i.e., custom view).

ZIA Admin Role Endpoints
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#256 <https://github.com/zscaler/zscaler-sdk-python/pull/256>`_) - Added the following new ZIA API Endpoints:
    - Added `GET /adminRoles/{roleId}` Retrieves the admin role based on the specified ID
    - Added `GET /adminRoles/lite` Retrieves a name and ID dictionary of all admin roles. The list only includes the name and ID for all admin roles.
    - Added `POST /adminRoles` Adds an admin role.
    - Added `PUT /adminRoles/{roleId}` Updates the admin role based on the specified ID.
    - Added `DELETE /adminRoles/{roleId}` Deletes the admin role based on the specified ID.

ZPA Credential Pool (New)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#256 <https://github.com/zscaler/zscaler-sdk-python/pull/256>`_) - Added new ZPA endpoint:
  - Added `GET /credential-pool` Gets the privileged credential pool details for the specified customer.
  - Added `GET /credential-pool/{id}` Gets the privileged credential pool details for the specified customer.
  - Added `GET /credential-pool/{id}/credential` Given Privileged credential pool id gets mapped privileged credential info
  - Added `POST /credential-pool` Adds a new privileged credential pool for the specified customer.
  - Added `PUT /credential-pool/{id}` Updates the existing credential pool for the specified customer.
  - Added `DELETE /credential-pool/{id}` Updates the existing credential pool for the specified customer.

ZWA - Zscaler Workflow Automation (NEW)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#256 <https://github.com/zscaler/zscaler-sdk-python/pull/256>`_) - Added new ZWA endpoint:
  - Added `GET /dlp/v1/incidents/transactions/{transactionId}` Gets the list of all DLP incidents associated with the transaction ID
  - Added `GET /dlp/v1/incidents/{dlpIncidentId}` Gets the DLP incident details based on the incident ID.
  - Added `DELETE /dlp/v1/incidents/{dlpIncidentId}` Deletes the DLP incident for the specified incident ID.
  - Added `GET /dlp/v1/incidents{dlpIncidentId}/change-history` Gets the details of updates made to an incident based on the given ID and timeline.
  - Added `GET /dlp/v1/incidents/{dlpIncidentId}/tickets` Gets the information of the ticket generated for the incident. For example, ticket type, ticket ID, ticket status, etc.
  - Added `POST /dlp/v1/incidents/{dlpIncidentId}/incident-groups/search` Filters a list of DLP incident groups to which the specified incident ID belongs.
  - Added `POST /dlp/v1/incidents/{dlpIncidentId}/close` Updates the status of the incident to resolved and closes the incident with a resolution label and a resolution code.
  - Added `POST /dlp/v1/incidents/{dlpIncidentId}/notes` Adds notes to the incident during updates or status changes.
  - Added `POST /dlp/v1/incidents/{dlpIncidentId}/labels` Assign lables (a label name and it's associated value) to DLP incidents.
  - Added `POST /dlp/v1/incidents/search` Filters DLP incidents based on the given time range and the field values.
  - Added `GET /dlp/v1/incidents/{dlpIncidentId}/triggers` Downloads the actual data that triggered the incident.
  - Added `GET /dlp/v1/incidents/{dlpIncidentId}/evidence` Gets the evidence URL of the incident.

Cloud & Branch Connector - OneAPI Support
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(`#256 <https://github.com/zscaler/zscaler-sdk-python/pull/256>`_) - Cloud & Branch Connector package is now compatible with OneAPI and Legacy API framework. Please refer to README for details.
(`#256 <https://github.com/zscaler/zscaler-sdk-python/pull/256>`_) - Cloud & Branch Connector package has been renamed from `zcon` to `ztw`

ZTW Policy Management
^^^^^^^^^^^^^^^^^^^^^^^

(`#256 <https://github.com/zscaler/zscaler-sdk-python/pull/256>`_) - Added the following new ZTW API Endpoints:
    - Added `GET /ecRules/ecRdr` Retrieves the list of traffic forwarding rules.
    - Added `PUT /ecRules/ecRdr/{ruleId}` Updates a traffic forwarding rule configuration based on the specified ID.
    - Added `POST /ecRules/ecRdr` Creates a new traffic forwarding rule.
    - Added `GET /ecRules/ecRdr/count` Retrieves the count of traffic forwarding rules available in the Cloud & Branch Connector Admin Portal.

ZTW Policy Resources
^^^^^^^^^^^^^^^^^^^^^

(`#256 <https://github.com/zscaler/zscaler-sdk-python/pull/256>`_) - Added the following new ZTW API Endpoints:
    - Added `GET /ipSourceGroups` Retrieves the list of source IP groups.
    - Added `GET /ipSourceGroups/lite` Retrieves the list of source IP groups. This request retrieves basic information about the source IP groups, such as name and ID. For extensive details, use the GET /ipSourceGroups request.
    - Added `POST /ipSourceGroups` Adds a new custom source IP group.
    - Added `DELETE /ipSourceGroups/{ipGroupId}` Deletes a source IP group based on the specified ID.
    - Added `GET /ipDestinationGroups` Retrieves the list of destination IP groups.
    - Added `GET /ipDestinationGroups/lite` Retrieves the list of destination IP groups. This request retrieves basic information about the destination IP groups, ID, name, and type. For extensive details, use the GET /ipDestinationGroups request.
    - Added `POST /ipDestinationGroups` Adds a new custom destination IP group.
    - Added `DELETE /ipDestinationGroups/{ipGroupId}` Deletes the destination IP group based on the specified ID. Default destination groups that are automatically created cannot be deleted.
    - Added `GET /ipGroups` Retrieves the list of IP pools.
    - Added `GET /ipGroups/lite` Retrieves the list of IP pools. This request retrieves basic information about the IP pools, such as name and ID. For extensive details, use the GET /ipGroups request.
    - Added `POST /ipGroups` Adds a new custom IP pool.
    - Added `DELETE /ipGroups/{ipGroupId}` Deletes an IP pool based on the specified ID.
    - Added `GET /networkServices` Retrieves the list of all network services. The search parameters find matching values within the name or description attributes.
    - Added `POST /networkServices` Creates a new network service.
    - Added `PUT /networkServices/{serviceId}` Updates the network service information for the specified service ID.
    - Added `DELETE /networkServices/{serviceId}` Deletes the network service for the specified ID.
    - Added `GET /networkServicesGroups` Retrieves the list of network service groups.
    - Added `GET /zpaResources/applicationSegments` Retrieves the list of ZPA application segments that can be configured in traffic forwarding rule criteria.

1.0.0 (April, 22 2025) - BREAKING CHANGES
-----------------------------------------

Notes
-----

- Python Versions: **v3.8, v3.9, v3.10, v3.11**


Zscaler OneAPI Support
-----------------------

(`#255 <https://github.com/zscaler/zscaler-sdk-python/pull/255>`_): Added support for (`OneAPI <https://help.zscaler.com/zidentity/what-zidentity>`_) Oauth2 authentication support through (`Zidentity <https://help.zscaler.com/zidentity/what-zidentity>`_)

**NOTES**
  - Starting at v1.0.0 version this SDK provides dual API client functionality and is backwards compatible with the legacy Zscaler API framework.
  - The new OneAPI framework is compatible only with the following products `ZCC/ZIA/ZPA`.
  - The following products `ZTW` - Cloud Connector and `ZDX` and Zscaler Digital Experience, authentication methods remain unnaffected.
  - The package `ZCON` (Zscaler Cloud and Branch Connector) has been renamed to `ZTW`
  - The following products `ZWA` - Zscaler Workflow Automation authentication methods remain unnaffected.

Refer to the (`README <hhttps://github.com/zscaler/zscaler-sdk-python/blob/master/README.md>`_) page for details on client instantiation, and authentication requirements on each individual product.

**WARNING**: Attention Government customers. OneAPI and Zidentity is not currently supported for the following ZIA clouds: `zscalergov` and `zscalerten` or ZPA `GOV`, and `GOVUS`. 
See the Zscaler Legacy API Framework section in the (`README Docs <https://zscaler-sdk-python.readthedocs.io/en/latest/index.html>`_) for more information on how authenticate to these environments using the built-in Legacy API method.

(`#255 <https://github.com/zscaler/zscaler-sdk-python/pull/255>`_): All API clients now support Config Setter object `ZCC/ZTW/ZDX/ZIA/ZPA/ZWA`

ZCC New Endpoints
^^^^^^^^^^^^^^^^^

(`#255 <https://github.com/zscaler/zscaler-sdk-python/pull/255>`_) - Added the following new ZCC API Endpoints:
  - Added `GET /downloadServiceStatus` to download service status for all devices.
  - Added `GET /getDeviceCleanupInfo` to retrieve device cleanup information.
  - Added `PUT /setDeviceCleanupInfo` to cleanup device information.
  - Added `GET /getDeviceDetails` to retrieve device detailed information.
  - Added `GET /getAdminUsers` to retrieve mobile portal admin user.
  - Added `PUT /editAdminUser` to update mobile portal admin user.
  - Added `GET /getAdminUsersSyncInfo` to retrieve mobile portal admin user sync information.
  - Added `POST /syncZiaZdxAdminUsers` to retrieve mobile portal admin users ZIA and ZDX sync information.
  - Added `POST /syncZpaAdminUsers` to retrieve mobile portal admin users ZPA sync information.
  - Added `GET /getAdminRoles` to retrieve mobile portal admin roles.
  - Added `GET /getCompanyInfo` to retrieve company information.
  - Added `GET /getZdxGroupEntitlements` to retrieve ZDX Group entitlement enablement.
  - Added `PUT /updateZdxGroupEntitlement` to retrieve ZDX Group entitlement enablement.
  - Added `GET /updateZpaGroupEntitlement` to retrieve ZPA Group entitlement enablement.
  - Added `GET /web/policy/listByCompany` to retrieve Web Policy By Company ID.
  - Added `PUT /web/policy/activate` to activate mobile portal web policy
  - Added `PUT /web/policy/edit` to update mobile portal web policy
  - Added `DELETE /web/policy/{policyId}/delete` to delete mobile portal web policy.
  - Added `GET /webAppService/listByCompany` to retrieve Web App Service information By Company ID.
  - Added `GET /webFailOpenPolicy/listByCompany` to retrieve web Fail Open Policy information By Company ID.
  - Added `PUT /webFailOpenPolicy/edit` to update mobile portal web Fail Open Policy.
  - Added `GET /webForwardingProfile/listByCompany` to retrieve Web Forwarding Profile information By Company ID.
  - Added `POST /webForwardingProfile/edit` to create a Web Forwarding Profile.
  - Added `DELETE /webForwardingProfile/{profileId}/delete` to delete Web Forwarding Profile.
  - Added `GET /webTrustedNetwork/listByCompany` to retrieve multiple Web Trusted Network information By Company ID.
  - Added `POST /webTrustedNetwork/edit` to create Web Trusted Network resource.
  - Added `PUT /webTrustedNetwork/edit` to update Web Trusted Network resource.
  - Added `DELETE /webTrustedNetwork/{networkId}/delete` to delete Web Trusted Network resource.
  - Added `GET /getWebPrivacyInfo` to retrieve Web Privacy Info.
  - Added `GET /setWebPrivacyInfo` to update Web Privacy Info.

ZIA Sandbox Submission - BREAKING CHANGES
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#255 <https://github.com/zscaler/zscaler-sdk-python/pull/255>`_) - Authentication to Zscaler Sandbox now use the following attributes during client instantiation.
 - `sandboxToken` - Can also be sourced from the `ZSCALER_SANDBOX_TOKEN` environment variable.
 - `sandboxCloud` - Can also be sourced from the `ZSCALER_SANDBOX_CLOUD` environment variable.

**NOTE** The previous `ZIA_SANDBOX_TOKEN` has been deprecated.

ZIA Sandbox Rules
^^^^^^^^^^^^^^^^^^

(`#255 <https://github.com/zscaler/zscaler-sdk-python/pull/255>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /sandboxRules` to retrieve the list of all Sandbox policy rules.
  - Added `GET /sandboxRules/{ruleId}` to retrieve the Sandbox policy rule information based on the specified ID.
  - Added `POST /sandboxRules` to add a Sandbox policy rule.
  - Added `PUT /sandboxRules/{ruleId}` to update the Sandbox policy rule configuration for the specified ID.
  - Added `DELETE /sandboxRules/{ruleId}` to delete the Sandbox policy rule based on the specified ID.

ZIA DNS Control Rules
^^^^^^^^^^^^^^^^^^^^^^

(`#255 <https://github.com/zscaler/zscaler-sdk-python/pull/255>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /firewallDnsRules` to retrieve the list of all DNS Control policy rules.
  - Added `GET /firewallDnsRules/{ruleId}` to retrieve the DNS Control policy rule information based on the specified ID.
  - Added `POST /firewallDnsRules` to add a DNS Control policy rules.
  - Added `PUT /firewallDnsRules/{ruleId}` to update the DNS Control policy rule configuration for the specified ID.
  - Added `DELETE /firewallDnsRules/{ruleId}` to delete the DNS Control policy rule based on the specified ID.

ZIA IPS Control Rules
^^^^^^^^^^^^^^^^^^^^^

(`#255 <https://github.com/zscaler/zscaler-sdk-python/pull/255>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /firewallIpsRules` to retrieve the list of all IPS Control policy rules.
  - Added `GET /firewallIpsRules/{ruleId}` to retrieve the IPS Control policy rule information based on the specified ID.
  - Added `POST /firewallIpsRules` to add a IPS Control policy rule.
  - Added `PUT /firewallIpsRules/{ruleId}` to update the IPS Control policy rule configuration for the specified ID.
  - Added `DELETE /firewallIpsRules/{ruleId}` to delete the IPS Control policy rule based on the specified ID.

ZIA File Type Control Policy
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#255 <https://github.com/zscaler/zscaler-sdk-python/pull/255>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /fileTypeRules` to retrieve the list of all File Type Control policy rules.
  - Added `GET /fileTypeRules/lite` to retrieve the list of all File Type Control policy rules.
  - Added `GET /fileTypeRules/{ruleId}` to retrieve the File Type Control policy rule information based on the specified ID.
  - Added `POST /fileTypeRules` to add a File Type Control policy rule.
  - Added `PUT /fileTypeRules/{ruleId}` to update the File Type Control policy rule configuration for the specified ID.
  - Added `DELETE /fileTypeRules/{ruleId}` to delete the File Type Control policy rule based on the specified ID.

ZIA Forwarding Control Policy - Proxy Gateways
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#255 <https://github.com/zscaler/zscaler-sdk-python/pull/255>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /proxyGateways` to retrieve the proxy gateway information.
  - Added `GET /proxyGateways/lite` to retrieve the name and ID of the proxy.

ZIA Cloud Nanolog Streaming Service (NSS)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#255 <https://github.com/zscaler/zscaler-sdk-python/pull/255>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /nssFeeds` to retrieve the cloud NSS feeds.
  - Added `GET /nssFeeds/{feedId}` to retrieve information about cloud NSS feed based on the specified ID.
  - Added `POST /nssFeeds` to add a new cloud NSS feed.
  - Added `PUT /nssFeeds/{feedId}` to update cloud NSS feed configuration based on the specified ID.
  - Added `DELETE /nssFeeds/{feedId}` to delete cloud NSS feed configuration based on the specified ID.
  - Added `GET /nssFeeds/feedOutputDefaults` to retrieve the default cloud NSS feed output format for different log types.
  - Added `GET /nssFeeds/testConnectivity/{feedId}` to test the connectivity of cloud NSS feed based on the specified ID
  - Added `POST /nssFeeds/validateFeedFormat` to validates the cloud NSS feed format and returns the validation result

ZIA Advanced Threat Protection Policy
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#255 <https://github.com/zscaler/zscaler-sdk-python/pull/255>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /cyberThreatProtection/advancedThreatSettings` to retrieve the advanced threat configuration settings.
  - Added `PUT /cyberThreatProtection/advancedThreatSettings` to update the advanced threat configuration settings.
  - Added `GET /cyberThreatProtection/maliciousUrls` to retrieve the malicious URLs added to the denylist in the Advanced Threat Protection (ATP) policy
  - Added `PUT /cyberThreatProtection/maliciousUrls` to updates the malicious URLs added to the denylist in ATP policy
  - Added `GET /cyberThreatProtection/securityExceptions` to retrieves information about the security exceptions configured for the ATP policy
  - Added `PUT /cyberThreatProtection/securityExceptions` to update security exceptions for the ATP policy

ZIA Advanced Threat Protection Policy
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#255 <https://github.com/zscaler/zscaler-sdk-python/pull/255>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /cyberThreatProtection/atpMalwareInspection` to retrieve the traffic inspection configurations of Malware Protection policy
  - Added `PUT /cyberThreatProtection/atpMalwareInspection` to update the traffic inspection configurations of Malware Protection policy.
  - Added `GET /cyberThreatProtection/atpMalwareProtocols` to retrieve the protocol inspection configurations of Malware Protection policy
  - Added `PUT /cyberThreatProtection/atpMalwareProtocols` to update the protocol inspection configurations of Malware Protection policy.
  - Added `GET /cyberThreatProtection/malwareSettings` to retrieve the malware protection policy configuration details
  - Added `PUT /cyberThreatProtection/malwareSettings` to update the malware protection policy configuration details.
  - Added `GET /cyberThreatProtection/malwarePolicy` to retrieve information about the security exceptions configured for the Malware Protection policy
  - Added `PUT /cyberThreatProtection/malwarePolicy` to update security exceptions for the Malware Protection policy.

ZIA URL & Cloud App Control Policy Settings
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#255 <https://github.com/zscaler/zscaler-sdk-python/pull/255>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /advancedUrlFilterAndCloudAppSettings` to retrieve information about URL and Cloud App Control advanced policy settings
  - Added `PUT /advancedUrlFilterAndCloudAppSettings` to update the URL and Cloud App Control advanced policy settings

ZIA Authentication Settings
^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#255 <https://github.com/zscaler/zscaler-sdk-python/pull/255>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /authSettings` to retrieve the organization's default authentication settings information, including authentication profile and Kerberos authentication information.
  - Added `GET /authSettings/lite` to retrieve organization's default authentication settings information.
  - Added `PUT /authSettings` to update the organization's default authentication settings information.

ZIA Advanced Settings
^^^^^^^^^^^^^^^^^^^^^

(`#255 <https://github.com/zscaler/zscaler-sdk-python/pull/255>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /advancedSettings` to retrieve information about the advanced settings.
  - Added `PUT /advancedSettings` to update the advanced settings configuration.

ZIA Cloud Applications
^^^^^^^^^^^^^^^^^^^^^^^

(`#255 <https://github.com/zscaler/zscaler-sdk-python/pull/255>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /cloudApplications/policy` Retrieves a list of Predefined and User Defined Cloud Applications associated with the DLP rules, Cloud App Control rules, Advanced Settings, Bandwidth Classes, and File Type Control rules.
  - Added `GET /cloudApplications/sslPolicy` Retrieves a list of Predefined and User Defined Cloud Applications associated with the SSL Inspection rules.

ZIA Shadow IT Report
^^^^^^^^^^^^^^^^^^^^

(`#255 <https://github.com/zscaler/zscaler-sdk-python/pull/255>`_) - Added the following new ZIA API Endpoints:
- Added `PUT /cloudApplications/bulkUpdate` To Update application status and tag information for predefined or custom cloud applications based on the IDs specified
- Added `GET /cloudApplications/lite` Gets the list of predefined and custom cloud applications
- Added `GET /customTags` Gets the list of custom tags available to assign to cloud applications
- Added `POST /shadowIT/applications/export` Export the Shadow IT Report (in CSV format) for the cloud applications recognized by Zscaler based on their usage in your organization.
- Added `POST /shadowIT/applications/{entity}/exportCsv` Export the Shadow IT Report (in CSV format) for the list of users or known locations identified with using the cloud applications specified in the request.

ZIA Remote Assistance Support
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#255 <https://github.com/zscaler/zscaler-sdk-python/pull/255>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /remoteAssistance` to retrieve information about the Remote Assistance option.
  - Added `PUT /remoteAssistance` to update information about the Remote Assistance option. Using this option, you can allow Zscaler Support to access your organization’s ZIA Admin Portal for a specified time period to troubleshoot issues.

ZIA Organization Details
^^^^^^^^^^^^^^^^^^^^^^^^^

(`#255 <https://github.com/zscaler/zscaler-sdk-python/pull/255>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /orgInformation` to retrieve detailed organization information, including headquarter location, geolocation, address, and contact details.
  - Added `GET /orgInformation/lite` to retrieve minimal organization information.
  - Added `GET /subscriptions` to retrieve information about the list of subscriptions enabled for your tenant. Subscriptions define the various features and levels of functionality that are available to your organization.

ZIA End User Notification
^^^^^^^^^^^^^^^^^^^^^^^^^^
(`#255 <https://github.com/zscaler/zscaler-sdk-python/pull/255>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /eun` to retrieve information browser-based end user notification (EUN) configuration details.
  - Added `PUT /eun` to update the browser-based end user notification (EUN) configuration details.

ZIA Admin Audit Logs
^^^^^^^^^^^^^^^^^^^^^^^

(`#255 <https://github.com/zscaler/zscaler-sdk-python/pull/255>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /auditlogEntryReport` to retrieve the status of a request for an audit log report.
  - Added `POST /auditlogEntryReport` to create an audit log report for the specified time period and saves it as a CSV file.
  - Added `DELETE /auditlogEntryReport` to cancel the request to create an audit log report.
  - Added `GET /auditlogEntryReport/download` to download the most recently created audit log report.

ZIA Extranets
^^^^^^^^^^^^^^^^^^

(`#255 <https://github.com/zscaler/zscaler-sdk-python/pull/255>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /extranet` to retrieve the list of extranets configured for the organization
  - Added `GET /extranet/lite` Retrieves the name-ID pairs of all extranets configured for an organization
  - Added `GET /extranet/{Id}` Retrieves information about an extranet based on the specified ID.
  - Added `POST /extranet` Adds a new extranet for the organization.
  - Added `PUT /extranet/{Id}` Updates an extranet based on the specified ID
  - Added `DELETE /extranet/{Id}` Deletes an extranet based on the specified ID

ZIA IOT Endpoint
^^^^^^^^^^^^^^^^^^

(`#255 <https://github.com/zscaler/zscaler-sdk-python/pull/255>`_) - Added the following new ZIA IOT API Endpoints:
  - Added `GET /iotDiscovery/deviceTypes` Retrieve the mapping between device type universally unique identifier (UUID) values and the device type names for all the device types supported by the Zscaler AI/ML.
  - Added `GET /iotDiscovery/categories` Retrieve the mapping between the device category universally unique identifier (UUID) values and the category names for all the device categories supported by the Zscaler AI/ML. The parent of device category is device type.
  - Added `GET /iotDiscovery/classifications` Retrieve the mapping between the device classification universally unique identifier (UUID) values and the classification names for all the device classifications supported by Zscaler AI/ML. The parent of device classification is device category.
  - Added `GET /iotDiscovery/deviceList` Retrieve a list of discovered devices with the following key contexts, IP address, location, ML auto-label, classification, category, and type.

ZIA 3rd-Party App Governance
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#255 <https://github.com/zscaler/zscaler-sdk-python/pull/255>`_) - Added the following new ZIA API Endpoints:
  - Added `GET /apps/app` to search the 3rd-Party App Governance App Catalog by either app ID or URL.
  - Added `POST /apps/app` to submis an app for analysis in the 3rd-Party App Governance Sandbox.
  - Added `GET /apps/search` to search for an app by name. Any app whose name contains the search term (appName) is returned.
  - Added `GET /app_views/list` to retrieve the list of custom views that you have configured in the 3rd-Party App Governance.
  - Added `GET /app_views/{appViewId}/apps` to retrieves all assets (i.e., apps) that are related to a specified argument (i.e., custom view).

ZIA Admin Role Endpoints
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#255 <https://github.com/zscaler/zscaler-sdk-python/pull/255>`_) - Added the following new ZIA API Endpoints:
    - Added `GET /adminRoles/{roleId}` Retrieves the admin role based on the specified ID
    - Added `GET /adminRoles/lite` Retrieves a name and ID dictionary of all admin roles. The list only includes the name and ID for all admin roles.
    - Added `POST /adminRoles` Adds an admin role.
    - Added `PUT /adminRoles/{roleId}` Updates the admin role based on the specified ID.
    - Added `DELETE /adminRoles/{roleId}` Deletes the admin role based on the specified ID.

ZPA Credential Pool (New)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#255 <https://github.com/zscaler/zscaler-sdk-python/pull/255>`_) - Added new ZPA endpoint:
  - Added `GET /credential-pool` Gets the privileged credential pool details for the specified customer.
  - Added `GET /credential-pool/{id}` Gets the privileged credential pool details for the specified customer.
  - Added `GET /credential-pool/{id}/credential` Given Privileged credential pool id gets mapped privileged credential info
  - Added `POST /credential-pool` Adds a new privileged credential pool for the specified customer.
  - Added `PUT /credential-pool/{id}` Updates the existing credential pool for the specified customer.
  - Added `DELETE /credential-pool/{id}` Updates the existing credential pool for the specified customer.

ZWA - Zscaler Workflow Automation (NEW)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(`#255 <https://github.com/zscaler/zscaler-sdk-python/pull/255>`_) - Added new ZWA endpoint:
  - Added `GET /dlp/v1/incidents/transactions/{transactionId}` Gets the list of all DLP incidents associated with the transaction ID
  - Added `GET /dlp/v1/incidents/{dlpIncidentId}` Gets the DLP incident details based on the incident ID.
  - Added `DELETE /dlp/v1/incidents/{dlpIncidentId}` Deletes the DLP incident for the specified incident ID.
  - Added `GET /dlp/v1/incidents{dlpIncidentId}/change-history` Gets the details of updates made to an incident based on the given ID and timeline.
  - Added `GET /dlp/v1/incidents/{dlpIncidentId}/tickets` Gets the information of the ticket generated for the incident. For example, ticket type, ticket ID, ticket status, etc.
  - Added `POST /dlp/v1/incidents/{dlpIncidentId}/incident-groups/search` Filters a list of DLP incident groups to which the specified incident ID belongs.
  - Added `POST /dlp/v1/incidents/{dlpIncidentId}/close` Updates the status of the incident to resolved and closes the incident with a resolution label and a resolution code.
  - Added `POST /dlp/v1/incidents/{dlpIncidentId}/notes` Adds notes to the incident during updates or status changes.
  - Added `POST /dlp/v1/incidents/{dlpIncidentId}/labels` Assign lables (a label name and it's associated value) to DLP incidents.
  - Added `POST /dlp/v1/incidents/search` Filters DLP incidents based on the given time range and the field values.
  - Added `GET /dlp/v1/incidents/{dlpIncidentId}/triggers` Downloads the actual data that triggered the incident.
  - Added `GET /dlp/v1/incidents/{dlpIncidentId}/evidence` Gets the evidence URL of the incident.

Cloud & Branch Connector - OneAPI Support
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(`#255 <https://github.com/zscaler/zscaler-sdk-python/pull/255>`_) - Cloud & Branch Connector package is now compatible with OneAPI and Legacy API framework. Please refer to README for details.
(`#255 <https://github.com/zscaler/zscaler-sdk-python/pull/255>`_) - Cloud & Branch Connector package has been renamed from `zcon` to `ztw`

ZTW Policy Management
^^^^^^^^^^^^^^^^^^^^^^^

(`#255 <https://github.com/zscaler/zscaler-sdk-python/pull/255>`_) - Added the following new ZTW API Endpoints:
    - Added `GET /ecRules/ecRdr` Retrieves the list of traffic forwarding rules.
    - Added `PUT /ecRules/ecRdr/{ruleId}` Updates a traffic forwarding rule configuration based on the specified ID.
    - Added `POST /ecRules/ecRdr` Creates a new traffic forwarding rule.
    - Added `GET /ecRules/ecRdr/count` Retrieves the count of traffic forwarding rules available in the Cloud & Branch Connector Admin Portal.

ZTW Policy Resources
^^^^^^^^^^^^^^^^^^^^^

(`#255 <https://github.com/zscaler/zscaler-sdk-python/pull/255>`_) - Added the following new ZTW API Endpoints:
    - Added `GET /ipSourceGroups` Retrieves the list of source IP groups.
    - Added `GET /ipSourceGroups/lite` Retrieves the list of source IP groups. This request retrieves basic information about the source IP groups, such as name and ID. For extensive details, use the GET /ipSourceGroups request.
    - Added `POST /ipSourceGroups` Adds a new custom source IP group.
    - Added `DELETE /ipSourceGroups/{ipGroupId}` Deletes a source IP group based on the specified ID.
    - Added `GET /ipDestinationGroups` Retrieves the list of destination IP groups.
    - Added `GET /ipDestinationGroups/lite` Retrieves the list of destination IP groups. This request retrieves basic information about the destination IP groups, ID, name, and type. For extensive details, use the GET /ipDestinationGroups request.
    - Added `POST /ipDestinationGroups` Adds a new custom destination IP group.
    - Added `DELETE /ipDestinationGroups/{ipGroupId}` Deletes the destination IP group based on the specified ID. Default destination groups that are automatically created cannot be deleted.
    - Added `GET /ipGroups` Retrieves the list of IP pools.
    - Added `GET /ipGroups/lite` Retrieves the list of IP pools. This request retrieves basic information about the IP pools, such as name and ID. For extensive details, use the GET /ipGroups request.
    - Added `POST /ipGroups` Adds a new custom IP pool.
    - Added `DELETE /ipGroups/{ipGroupId}` Deletes an IP pool based on the specified ID.
    - Added `GET /networkServices` Retrieves the list of all network services. The search parameters find matching values within the name or description attributes.
    - Added `POST /networkServices` Creates a new network service.
    - Added `PUT /networkServices/{serviceId}` Updates the network service information for the specified service ID.
    - Added `DELETE /networkServices/{serviceId}` Deletes the network service for the specified ID.
    - Added `GET /networkServicesGroups` Retrieves the list of network service groups.
    - Added `GET /zpaResources/applicationSegments` Retrieves the list of ZPA application segments that can be configured in traffic forwarding rule criteria.

0.10.7 (April,15 2025)

Notes
^^^^^^

- Python Versions: **v3.8, v3.9, v3.10, v3.11**

Bug Fixes
----------

* (`254 <https://github.com/zscaler/zscaler-sdk-python/pull/254>`_) Added retry-status code `408` to prevent random timeouts during unforseen issues.


0.10.6 (April,8 2025)

Notes
^^^^^^

- Python Versions: **v3.8, v3.9, v3.10, v3.11**

Bug Fixes
----------

* Fixed `_create_conditions_v1` in ZPA `policies` package to ensure proper `conditions` block configuration (`253 <https://github.com/zscaler/zscaler-sdk-python/pull/253>`_)
* Included new ZPA `policies` `object_types`. `RISK_FACTOR_TYPE` and `CHROME_ENTERPRISE`. (`253 <https://github.com/zscaler/zscaler-sdk-python/pull/253>`_)

0.10.5 (March,13 2025)

Notes
^^^^^^

- Python Versions: **v3.8, v3.9, v3.10, v3.11**

Bug Fixes
----------

* (`251 <https://github.com/zscaler/zscaler-sdk-python/pull/251>`_) - Enhanced `pac_files` function resources.
  - `clone_pac_file` - The function pre-checks if total number of pac file versions within a specific pac file is == 10. If so, it triggers a error requiring the use of the parameter/attribute `delete_version`.
    
**NOTE** A maximum of 10 pac file versions is supported. If the total limit is reached you must explicitly indicate via the `delete_version` parameter which version must be removed prior to invoking the `clone_pac_file` method again.

  - `update_pac_file` - The function now validates the current `pac_version_status` prior to attempting an update. The API endpoint behind the `update_pac_file` method requires the `pac_version_status` to have specific value in order to accept the call.

* (`251 <https://github.com/zscaler/zscaler-sdk-python/pull/251>`_) Fixed `ZIAClientHelper` to prevent KeyError issues during time expiry check.
* (`251 <https://github.com/zscaler/zscaler-sdk-python/pull/251>`_) - Fixed `cloud_apps.list_apps` function to support new pagination parameters `page_number` and `limit`
* (`251 <https://github.com/zscaler/zscaler-sdk-python/pull/251>`_) - Fixed pagination for `devices.list_devices` to support new pagination paramters.

0.10.4 (January,9 2025)

Notes
^^^^^^

- Python Versions: **v3.8, v3.9, v3.10, v3.11**

Bug Fixes
----------

* Fixed pagination parameters on ZIA `cloud_apps` resource. Cloud Apps use the following parameters during pagination: `limit` and `page_number`. (`237 <https://github.com/zscaler/zscaler-sdk-python/pull/237>`_) 

0.10.3 (January,8 2025)

Notes
^^^^^^

- Python Versions: **v3.8, v3.9, v3.10, v3.11**

Bug Fixes
----------

* Added missing `cloud_apps` property resource to ZIA package. (`235 <https://github.com/zscaler/zscaler-sdk-python/pull/235>`_) 

0.10.2 (January,6 2025)

Notes
^^^^^^

- Python Versions: **v3.8, v3.9, v3.10, v3.11**

Bug Fixes
----------

* (`231 <https://github.com/zscaler/zscaler-sdk-python/pull/231>`_) Improved ZIA pagination logic to enhance flexibility and address user-reported issues. The changes include:
  - Fixed behavior where `pagesize` was being ignored, defaulting to 100. The SDK now respects the user-specified `pagesize` value within API limits (100-10,000).
  - Added explicit handling for the `page` parameter. When provided, the SDK fetches data from only the specified page without iterating through all pages.
  - Updated docstrings and documentation to clarify the correct usage of `page` and `pagesize` parameters.

0.10.1 (December,18 2024)

Notes
^^^^^^

- Python Versions: **v3.8, v3.9, v3.10, v3.11**

Bug Fixes
----------

* Fixed ZPA policy condition template to support object_type aggregation. (`225 <https://github.com/zscaler/zscaler-sdk-python/pull/225>`_)
* Fixed ZIA PAC file `list_pac_files` docstring documentation. (`225 <https://github.com/zscaler/zscaler-sdk-python/pull/225>`_)

0.10.0 (November,15 2024)

Notes
^^^^^^

- Python Versions: **v3.8, v3.9, v3.10, v3.11**

Enhancements
------------

ZIA Pac Files
^^^^^^^^^^^^^

* Added `GET /pacFiles` to Retrieves the list of all PAC files which are in deployed state.(`203 <https://github.com/zscaler/zscaler-sdk-python/pull/203>`_)
* Added `GET /pacFiles/{pacId}/version` to Retrieves all versions of a PAC file based on the specified ID. (`203 <https://github.com/zscaler/zscaler-sdk-python/pull/203>`_)
* Added `GET /pacFiles/{pacId}/version/{pacVersion}` to Retrieves a specific version of a PAC file based on the specified ID. (`203 <https://github.com/zscaler/zscaler-sdk-python/pull/203>`_)
* Added `POST /pacFiles` to Adds a new custom PAC file.(`203 <https://github.com/zscaler/zscaler-sdk-python/pull/203>`_)
* Added `DELETE /pacFiles/{pacId}` to Deletes an existing PAC file including all of its versions based on the specified ID.(`203 <https://github.com/zscaler/zscaler-sdk-python/pull/203>`_)
* Added `PUT /pacFiles/{pacId}/version/{pacVersion}/action/{pacVersionAction}` to Performs the specified action on the PAC file version and updates the file status.(`203 <https://github.com/zscaler/zscaler-sdk-python/pull/203>`_)
* Added `POST /pacFiles/validate` to send the PAC file content for validation and returns the validation result.(`203 <https://github.com/zscaler/zscaler-sdk-python/pull/203>`_)
* Added `POST /pacFiles/{pacId}/version/{clonedPacVersion}` to Adds a new PAC file version by branching an existing version based on the specified ID. (`203 <https://github.com/zscaler/zscaler-sdk-python/pull/203>`_)

0.9.7 (November,1 2024)

Notes
^^^^^^

- Python Versions: **v3.8, v3.9, v3.10, v3.11**

Bug Fixes
----------

* Fixed ZPA Policy Set Controller complex Conditions template to support inner `AND/OR` operators (`199 <https://github.com/zscaler/zscaler-sdk-python/pull/199>`_). Issue (`198 <https://github.com/zscaler/zscaler-sdk-python/issues/198>`_)


0.9.6 (October,28 2024)

Notes
^^^^^^

- Python Versions: **v3.8, v3.9, v3.10, v3.11**

Bug Fixes
----------

* Fixed ZPA Policy Set Controller Conditions template to support nested conditions and operators (`194 <https://github.com/zscaler/zscaler-sdk-python/pull/194>`_)
* Fixed ZIA pagination by introducing the custom `get_paginated_data` function (`194 <https://github.com/zscaler/zscaler-sdk-python/pull/194>`_)


0.9.5 (October, 9 2024)

Notes
^^^^^^

- Python Versions: **v3.8, v3.9, v3.10, v3.11**

Bug Fixes
----------

* Fixed ZPA App Connector and Service Edge Bulk Delete functions due to return error (`182 <https://github.com/zscaler/zscaler-sdk-python/pull/182>`_)
* Deprecated the ZIA function `get_location_group_by_name`. Users must use Use `list_location_groups(name=group_name)` instead going forward. (`182 <https://github.com/zscaler/zscaler-sdk-python/pull/182>`_)

0.9.4 (October, 3 2024)
-------------------------

Notes
^^^^^^

- Python Versions: **v3.8, v3.9, v3.10, v3.11**

Bug Fixes
----------

* Fixed ZPA Microtenant Update method response processing.  (`173 <https://github.com/zscaler/zscaler-sdk-python/pull/173>`_)
* Fixed ZIA `check_static_ip` text parsing  (`173 <https://github.com/zscaler/zscaler-sdk-python/pull/173>`_)

0.9.3 (September, 16 2024)
---------------------------

Notes
^^^^^

- Python Versions: **v3.8, v3.9, v3.10, v3.11**

Bug Fixes
----------

* Added function `list_version_profiles` to ZPA `connectors` package  (`156 <https://github.com/zscaler/zscaler-sdk-python/pull/156>`_)

0.9.2 (August, 31 2024)
------------------------

Notes
^^^^^

- Python Versions: **v3.8, v3.9, v3.10, v3.11**

Bug Fixes
----------


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
