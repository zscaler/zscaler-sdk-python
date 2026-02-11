# Zscaler Python SDK Changelog

## 1.9.14 (February 10, 2026)

### Notes

- Python Versions: **v3.9, v3.10, v3.11, v3.12**

### Enhancements:

#### Zscaler AI Guard

* [PR #457](https://github.com/zscaler/zscaler-sdk-python/pull/457) - Added new Zscaler AI Guard API endpoints
  - `/detection/execute-policy`
  - `/detection/resolve-and-execute-policy`

### ZTW API

* [PR #457](https://github.com/zscaler/zscaler-sdk-python/pull/457) - Added `DELETE` method for `forwarding_rules` resource. 

* [PR #457](https://github.com/zscaler/zscaler-sdk-python/pull/457) - Added new attributes `url_type`, `regex_patterns`,  and `regex_patterns_retaining_parent_category` to `zia_url_categories` resource to specify whether the category uses exact URLs or regex patterns. Supported values are `EXACT` and `REGEX`. See [Zscaler Release Notes](https://help.zscaler.com/zia/release-upgrade-summary-2026) for details. To enable this feature, contact Zscaler Support.

### Bug Fixes

* [PR #457](https://github.com/zscaler/zscaler-sdk-python/pull/457) - Replaced `flatdict` dependency with internal `flatten_dict`/`unflatten_dict` helpers to fix build failures on `setuptools 82+`. Thanks [@pankaj28843](https://github.com/pankaj28843) for reporting [#454](https://github.com/zscaler/zscaler-sdk-python/issues/454) and [@enza252](https://github.com/enza252) for the [initial implementation](https://github.com/zscaler/zscaler-sdk-python/pull/455).

## 1.9.13 (January 22, 2026)

### Notes

- Python Versions: **v3.9, v3.10, v3.11, v3.12**

* [PR #450](https://github.com/zscaler/zscaler-sdk-python/pull/450) - Added new CRUD functioins for ZTW `provisioning_url` resource api.
* [PR #450](https://github.com/zscaler/zscaler-sdk-python/pull/450) - Added new attribute `dest_workload_groups_ids` to ZTW `forwarding_rules` resource 
* [PR #450](https://github.com/zscaler/zscaler-sdk-python/pull/450) - Added new function `get_rule_type_label` to retrieves a list of rule labels based on the specified rule type


## 1.9.12 (January 19, 2026)

### Notes

- Python Versions: **v3.9, v3.10, v3.11, v3.12**

* [PR 444](https://github.com/zscaler/zscaler-sdk-python/pull/444) - Added new pagination parameters to ZIA `url_filtering_rule`

## 1.9.11 (December 16, 2025)

### Notes

- Python Versions: **v3.9, v3.10, v3.11, v3.12**

* [PR #443](https://github.com/zscaler/zscaler-sdk-python/pull/443) - Removed extraneous Z-Insights domain modules (data_protection, genai, industry_peer, news_feed, risk_score, sandbox) that were incorrectly created for GraphQL types not exposed in the root Query. Z-Insights now correctly implements only the 6 queryable domains.

## 1.9.10 (December 16, 2025)

### Notes

- Python Versions: **v3.9, v3.10, v3.11, v3.12**

### Enhancements:

#### Z-Insights Analytics API Support (GraphQL)

* [PR #442](https://github.com/zscaler/zscaler-sdk-python/pull/442) - Added comprehensive support for Z-Insights Analytics GraphQL API. Z-Insights provides unified real-time visibility into security analytics across web traffic, cyber security incidents, firewall activity, IoT devices, SaaS security, and Shadow IT discovery.
  - Added `client.zinsights` service with domain-specific API clients:
    - `web_traffic` - Web traffic analytics (location, protocols, threat categories, trends)
    - `cyber_security` - Security incidents and threat analysis
    - `firewall` - Zero Trust Firewall traffic and actions
    - `saas_security` - Cloud Access Security Broker (CASB) reports
    - `shadow_it` - Discovered application analytics and risk assessment
    - `iot` - IoT device visibility and classification statistics
  - Added GraphQL-specific error handling with `GraphQLAPIError` exception class
  - Implemented comprehensive input models with DRY architecture:
    - `StringFilter` - Universal filter supporting eq, ne, in, nin operations
    - Base classes `BaseNameFilterBy` and `BaseNameTotalOrderBy` for code reuse
    - Domain-specific filters and ordering options for all API domains
  - Added 14 enum types for type-safe API interactions (SortOrder, WebTrafficUnits, TrendInterval, etc.)
  - Included 6 comprehensive example scripts demonstrating real-world usage patterns
  - Full support for filtering, ordering, pagination, trend data, and nested GraphQL queries
  - Compatible with OneAPI authentication only (OAuth2.0 via Zidentity) 

## 1.9.9 (December 11, 2025)

### Notes

- Python Versions: **v3.9, v3.10, v3.11, v3.12**

## 1.9.9 (December 11, 2025)

### Notes

- Python Versions: **v3.9, v3.10, v3.11, v3.12**

### Bug Fixes:

* [PR #439](https://github.com/zscaler/zscaler-sdk-python/pull/439) - Fixed ZPA legacy client `retry-after` header parsing for non-standard format with 's' suffix (e.g., `"8s"` instead of `"8"`).
* [PR #439](https://github.com/zscaler/zscaler-sdk-python/pull/439) - Fixed ZIA legacy client `Retry-After` header parsing for format with " seconds" suffix (e.g., `"0 seconds"`).
* [PR #439](https://github.com/zscaler/zscaler-sdk-python/pull/439) - Fixed ZTW legacy client `Retry-After` header parsing for format with " seconds" suffix (e.g., `"0 seconds"`).

## 1.9.8 (December 10, 2025)

### Notes

- Python Versions: **v3.9, v3.10, v3.11, v3.12**

### Bug Fixes:

* [PR #438](https://github.com/zscaler/zscaler-sdk-python/pull/438) - Fixed ZPA Legacy Client missing 429 rate limiting handling. The `send()` method now properly retries on 429 responses using `retry-after` header with fallback to default 2 seconds.
* [PR #438](https://github.com/zscaler/zscaler-sdk-python/pull/438) - Added unit tests for legacy client rate limiting across all legacy clients (ZPA, ZIA, ZCC, ZDX, ZTW, ZWA).

## 1.9.7 (December 8, 2025)

### Notes

- Python Versions: **v3.9, v3.10, v3.11, v3.12**

### Bug Fixes:

* [PR #437](https://github.com/zscaler/zscaler-sdk-python/pull/437) - Fixed 204 No Content responses returning `None` for response object, now returns `ZscalerAPIResponse` with status code accessible via `response.get_status()`.
* [PR #437](https://github.com/zscaler/zscaler-sdk-python/pull/437) - Fixed ZPA update operations returning objects with `id=None` due to empty response body handling.

## 1.9.6 (December 2, 2025)

### Notes

- Python Versions: **v3.9, v3.10, v3.11, v3.12**

### Enhancements:

* [PR #433](https://github.com/zscaler/zscaler-sdk-python/pull/433) - Added External Attach Surface Management(EASM) Endpoints

### Bug Fixes:

* [PR #433](https://github.com/zscaler/zscaler-sdk-python/pull/433) - Fixed missing `creation_time`, `modified_time`, `modified_by` attributes in ZPA `ApplicationSegments` model.
* [PR #433](https://github.com/zscaler/zscaler-sdk-python/pull/433) - Fixed missing `id` attribute in ZCC `PolicyExtension` model causing `AttributeError`.
* [PR #433](https://github.com/zscaler/zscaler-sdk-python/pull/433) - Fixed ZCC camelCase edge cases in `helpers.py` for attributes like `truncateLargeUDPDNSResponse`, `enforceSplitDNS`, `packetTunnelExcludeListForIPv6`.
* [PR #433](https://github.com/zscaler/zscaler-sdk-python/pull/433) - Added `device_type` parameter mapping support in ZCC `zcc_param_mapper`.

## 1.9.5 (November 26, 2025)

### Notes

- Python Versions: **v3.9, v3.10, v3.11, v3.12**

### Enhancements:

* [PR #428](https://github.com/zscaler/zscaler-sdk-python/pull/428) - Added VCR-based integration testing with recorded HTTP cassettes for faster, deterministic test execution.

## 1.9.4 (November 26, 2025)

### Notes

- Python Versions: **v3.9, v3.10, v3.11, v3.12**

### Enhancements:

* [PR #427](https://github.com/zscaler/zscaler-sdk-python/pull/427) - Added VCR-based integration testing with recorded HTTP cassettes for faster, deterministic test execution.

## 1.9.3 (November 25, 2025)

### Notes

- Python Versions: **v3.9, v3.10, v3.11, v3.12**

### Enhancements:

* [PR #426](https://github.com/zscaler/zscaler-sdk-python/pull/426) - Added official support for Python 3.12.

### Bug Fixes:

* [PR #426](https://github.com/zscaler/zscaler-sdk-python/pull/426) - Fixed pagination `has_next()` returning `True` for flat list API responses causing infinite loops.
* [PR #426](https://github.com/zscaler/zscaler-sdk-python/pull/426) - Added missing parameter `type` to ZIA `url_categories`

## 1.9.2 (November 18, 2025)

### Notes

- Python Versions: **v3.8, v3.9, v3.10, v3.11**

### Bug Fixes:

* [PR #423](https://github.com/zscaler/zscaler-sdk-python/pull/423) - Fixed type hints for Cloud Firewall list functions.

### New ZIA Endpoint - Traffic Capture Policy

* [PR #423](https://github.com/zscaler/zscaler-sdk-python/pull/423) - Added the following new ZIA Endpoints
    - Added `GET /trafficCaptureRules` Retrieves the list of Traffic Capture policy rules
    - Added `GET /trafficCaptureRules/{ruleId}` Retrieves the Traffic Capture policy rule based on the specified rule ID
    - Added `PUT /trafficCaptureRules/{ruleId}` Updates information for the Traffic Capture policy rule based on the specified rule ID
    - Added `DELETE /trafficCaptureRules/{ruleId}` Deletes the Traffic Capture policy rule based on the specified rule ID
    - Added `GET /trafficCaptureRules/count` Retrieves the rule count for Traffic Capture policy based on the specified search criteria
    - Added `GET /trafficCaptureRules/order` Retrieves the rule order information for the Traffic Capture policy
    - Added `GET /trafficCaptureRules/ruleLabels` Retrieves the list of rule labels associated with the Traffic Capture policy rules

## 1.9.2 (November 18, 2025)

### Notes

- Python Versions: **v3.8, v3.9, v3.10, v3.11**

### Bug Fixes:

* [PR #422](https://github.com/zscaler/zscaler-sdk-python/pull/422) - Fixed type hints for Cloud Firewall list functions.

### New ZIA Endpoint - Traffic Capture Policy

* [PR #422](https://github.com/zscaler/zscaler-sdk-python/pull/422) - Added the following new ZIA Endpoints
    - Added `GET /trafficCaptureRules` Retrieves the list of Traffic Capture policy rules
    - Added `GET /trafficCaptureRules/{ruleId}` Retrieves the Traffic Capture policy rule based on the specified rule ID
    - Added `PUT /trafficCaptureRules/{ruleId}` Updates information for the Traffic Capture policy rule based on the specified rule ID
    - Added `DELETE /trafficCaptureRules/{ruleId}` Deletes the Traffic Capture policy rule based on the specified rule ID
    - Added `GET /trafficCaptureRules/count` Retrieves the rule count for Traffic Capture policy based on the specified search criteria
    - Added `GET /trafficCaptureRules/order` Retrieves the rule order information for the Traffic Capture policy
    - Added `GET /trafficCaptureRules/ruleLabels` Retrieves the list of rule labels associated with the Traffic Capture policy rules

## 1.9.1 (November 7, 2025)

### Notes

- Python Versions: **v3.8, v3.9, v3.10, v3.11**

### Bug Fixes:

* [PR #413](https://github.com/zscaler/zscaler-sdk-python/pull/413) - Ensure legacy service accessors in `oneapi_client.py` raise a clear error when no legacy helper is supplied, preventing `None` from leaking to callers.

* [PR #413](https://github.com/zscaler/zscaler-sdk-python/pull/413) - Added missing `python-jose` dependency to the documentation build so Read the Docs renders SDK pages correctly.

## 1.9.0 (November 3, 2025)

### Notes

- Python Versions: **v3.8, v3.9, v3.10, v3.11**

### New ZPA Endpoint - Application Server Controller

* [PR #410](https://github.com/zscaler/zscaler-sdk-python/pull/410) - Added the following new ZPA Endpoints
    - Added `GET /server/summary` Get all the configured application servers Name and IDs

### New ZPA Endpoint - Application Segment Controller

* [PR #410](https://github.com/zscaler/zscaler-sdk-python/pull/410) - Added the following new ZPA Endpoints
    - Added `GET /application/{applicationId}/mappings` Get the application segment mapping details
    - Added `DELETE /application/{applicationId}/deleteAppByType` Delete a BA/Inspection and PRA Application
    - Added `POST /application/{applicationId}/validate` Validate conflicting wildcard domain names. Expect the applicationID to be populated in the case of update
    - Added `GET /application/configured/count` Returns the count of configured application Segment for the provided customer between the date range passed in request body.
    - Added `GET /application/count/currentAndMaxLimit` get current Applications count of domains and maxLimit configured for a given customer

### New ZPA Endpoint - App Connector Group

* [PR #410](https://github.com/zscaler/zscaler-sdk-python/pull/410) - Added the following new ZPA Endpoints
    - Added `GET /appConnectorGroup/summary` Get all the configured App Connector Group id and name.

### New ZPA Endpoint - Branch Connector Controller

* [PR #410](https://github.com/zscaler/zscaler-sdk-python/pull/410) - Added the following new ZPA Endpoints
    - Added `GET /branchConnector` Get all BranchConnectors configured for a given customer.

### New ZPA Endpoint - Branch Connector Group Controller

* [PR #410](https://github.com/zscaler/zscaler-sdk-python/pull/410) - Added the following new ZPA Endpoints
    - Added `GET /branchConnectorGroup/summary` Get all branch connector group id and names configured for a given customer.
    - Added `GET /branchConnectorGroup` Get all configured Branch Connector Groups.

### New ZPA Endpoint - Browser Protection Profile Controller

* [PR #410](https://github.com/zscaler/zscaler-sdk-python/pull/410) - Added the following new ZPA Endpoints
    - Added `GET /activeBrowserProtectionProfile` Get the active browser protection profile details for the specified customer.
    - Added `GET /browserProtectionProfile` Gets all configured browser protection profiles for the specified customer.
    - Added `PUT /browserProtectionProfile/setActive/{browserProtectionProfileId}` Updates a specified browser protection profile as active for the specified customer.

### New ZPA Endpoint - Customer Config Controller

* [PR #410](https://github.com/zscaler/zscaler-sdk-python/pull/410) - Added the following new ZPA Endpoints
    - Added `GET /config/isZiaCloudConfigAvailable` Check if zia cloud config for a given customer is available.
    - Added `GET /config/ziaCloudConfig` Get zia cloud service config for a given customer.
    - Added `POST /config/ziaCloudConfig` Add or update zia cloud service config for a given customer.
    - Added `GET /sessionTerminationOnReauth` Get session termination on reauth for a given customer.
    - Added `PUT /sessionTerminationOnReauth` Add /update boolean value for session termination on reauth.

### New ZPA Endpoint - Customer DR Tool Version Controller

* [PR #410](https://github.com/zscaler/zscaler-sdk-python/pull/410) - Added the following new ZPA Endpoints
    - Added `GET /customerDRToolVersion` Fetch latest the Customer Support DR Tool Versions sorted by latest filter

### New ZPA Endpoint - Customer Version Profile Controller

* [PR #410](https://github.com/zscaler/zscaler-sdk-python/pull/410) - Added the following new ZPA Endpoints
    - Added `GET /versionProfiles/{versionProfileId}` Update Version Profile for customer

### New ZPA Endpoint - Cloud Connector Group Controller

* [PR #410](https://github.com/zscaler/zscaler-sdk-python/pull/410) - Added the following new ZPA Endpoints
    - Added `GET /cloudConnectorGroup/summary` Get all edge connector group id and names configured for a given customer

### New ZPA Endpoint - Extranet Resource Controller

* [PR #410](https://github.com/zscaler/zscaler-sdk-python/pull/410) - Added the following new ZPA Endpoints
    - Added `GET /extranetResource/partner` Get all extranet resources

### New ZPA Endpoint - Machine Group Controller

* [PR #410](https://github.com/zscaler/zscaler-sdk-python/pull/410) - Added the following new ZPA Endpoints
    - Added `GET /machineGroup/summary` Get all Machine Group Id and Names configured for a given customer

### New ZPA Endpoint - Managed Browser Profile Controller

* [PR #410](https://github.com/zscaler/zscaler-sdk-python/pull/410) - Added the following new ZPA Endpoints
    - Added `GET /managedBrowserProfile/search` Gets all the managed browser profiles for a customer

### New ZPA Endpoint - Provisioning Key Controller

* [PR #410](https://github.com/zscaler/zscaler-sdk-python/pull/410) - Added the following new ZPA Endpoints
    - Added `GET /associationType/{associationType}/zcomponent/{zcomponentId}/provisioningKey` get provisioningKey details by zcomponentId for associationType.

### New ZPA Endpoint - OAuth User Code Controller

* [PR #410](https://github.com/zscaler/zscaler-sdk-python/pull/410) - Added the following new ZPA Endpoints
    - Added `POST /{associationType}/usercodes` Verifies the provided list of user codes for a given component provisioning.
    - Added `POST /{associationType}/usercodes/status` Adds a new Provisioning Key for the specified customer.

### New ZPA Endpoint - Policy-Set Controller

* [PR #410](https://github.com/zscaler/zscaler-sdk-python/pull/410) - Added the following new ZPA Endpoints
    - Added `GET /riskScoreValues` Gets values of risk scores for the specified customer.
    - Added `GET /policySet/rules/policyType/{policyType}/count` For a customer, get count of policy rules for a given policy type. Providing only endtime would give cumulative count till the endTime.Providing both startTime and endtime would give count between that time period.Not Providing startTime and endtime would give overall count.
    - Added `GET /policySet/rules/policyType/{policyType/application/{applicationId}` Gets paginated policy rules for the specified policy type by application id

### New ZPA Endpoint - Server Group Controller

* [PR #410](https://github.com/zscaler/zscaler-sdk-python/pull/410) - Added the following new ZPA Endpoints
    - Added `GET /serverGroup/summary` Get all Server Group id and names configured for a given customer

### New ZPA Endpoint - Step up Auth Level Controller

* [PR #410](https://github.com/zscaler/zscaler-sdk-python/pull/410) - Added the following new ZPA Endpoints
    - Added `GET /stepupauthlevel/summary` Get a step up auth levels.

### New ZPA Endpoint - Step up Auth Level Controller

* [PR #410](https://github.com/zscaler/zscaler-sdk-python/pull/410) - Added the following new ZPA Endpoints
    - Added `GET /userportal/aup/{id}` Get user portal aup
    - Added `PUT /userportal/aup/{id}` Update user portal aup
    - Added `DELETE /userportal/aup/{id}` Delete user portal aup
    - Added `GET /userportal/aup` Get all AUPs configured for a given customer
    - Added `POST /userportal/aup` Add a new aup for a given customer.

### New ZPA Endpoint - ZPN Location Controller

* [PR #410](https://github.com/zscaler/zscaler-sdk-python/pull/410) -Added the following new ZPA Endpoints
    - Added `GET /location/extranetResource/{zpnErId}`
    - Added `PUT /location/summary` Get all Location id and names configured for a given customer.

### New ZPA Endpoint - ZPN Location Group Controller

* [PR #410](https://github.com/zscaler/zscaler-sdk-python/pull/410) - Added the following new ZPA Endpoints
    - Added `GET /locationGroup/extranetResource/{zpnErId}`

### New ZPA Endpoint - Workload Tag Group Controller

* [PR #410](https://github.com/zscaler/zscaler-sdk-python/pull/410) - Added the following new ZPA Endpoints
    - Added `GET /workloadTagGroup/summary`

### New ZTW Endpoint - Partner Integrations - Public Account Info

* [PR #410](https://github.com/zscaler/zscaler-sdk-python/pull/410) - Added the following new ZPA Endpoints
    - Added `GET /publicCloudInfo` - Retrieves the list of AWS accounts with metadata
    - Added `POST /publicCloudInfo` - Creates a new AWS account with the provided account and region details.
    - Added `GET /publicCloudInfo/cloudFormationTemplate` - Retrieves the CloudFormation template URL.
    - Added `GET /publicCloudInfo/count` - Retrieves the total number of AWS accounts.
    - Added `POST /publicCloudInfo/generateExternalId` - Creates an external ID for an AWS account.
    - Added `GET /publicCloudInfo/lite` - Retrieves basic information about the AWS cloud accounts
    - Added `GET /publicCloudInfo/supportedRegions` - Retrieves a list of AWS regions supported for workload discovery settings (WDS).
    - Added `GET /publicCloudInfo/{id}` - Retrieves the existing AWS account details based on the provided ID.
    - Added `PUT /publicCloudInfo/{id}` - Updates the existing AWS account details based on the provided ID.
    - Added `DELETE /publicCloudInfo/{id}` - Removes a specific AWS account based on the provided ID.
    - Added `DELETE /publicCloudInfo/{id}/changeState` - Enables or disables a specific AWS account in all regions based on the provided ID.

### New ZTW Endpoint - Partner Integrations - Workload Discovery Service

* [PR #410](https://github.com/zscaler/zscaler-sdk-python/pull/410) - Added the following new ZPA Endpoints
    - Added `GET /discoveryService/workloadDiscoverySettings` - Retrieves the workload discovery service settings.
    - Added `PUT /discoveryService/{id}/permissions` - Verifies the specified AWS account permissions using the discovery role and external ID.

### New ZTW Endpoint - Partner Integrations - Account Groups

* [PR #410](https://github.com/zscaler/zscaler-sdk-python/pull/410) - Added the following new ZPA Endpoints
    - Added `GET /accountGroups` - Retrieves the details of AWS account groups with metadata.
    - Added `POST /accountGroups` - Creates an AWS account group. You can create a maximum of 128 groups in each organization. 
    - Added `GET /accountGroups/count` - Retrieves the total number of AWS account groups.
    - Added `GET /accountGroups/lite` - Retrieves the ID and name of all the AWS account groups.
    - Added `PUT /accountGroups/{id}` - Updates the existing AWS account group details based on the provided ID.
    - Added `DELETE /accountGroups/{id}` - Removes a specific AWS account group based on the provided ID.
  
### Enhancements

* [PR #410](https://github.com/zscaler/zscaler-sdk-python/pull/410) - Added comprehensive type hints to ~856 API methods across all packages (ZIA, ZPA, ZCC, ZDX, ZTW, ZWA, ZIdentity) enabling IDE autocomplete and intellisense support. Introduced `APIResult[T]` type alias for standardized return type annotations.

* [PR #410](https://github.com/zscaler/zscaler-sdk-python/pull/410) - Fixed `check_static_ip` method to correctly return `is_valid=True` when IP is available. The method now properly handles HTTP 200 responses with plain text "SUCCESS" body, ignoring non-JSON response errors that were incorrectly causing the validation to fail. 

* [PR #410](https://github.com/zscaler/zscaler-sdk-python/pull/410) - Added support for ZPA filtering API format in search parameters. Simple search strings are automatically converted to `name+EQ+<value>` format for exact name matching, while advanced filter formats (e.g., `enabled+EQ+true`) can be provided explicitly. This resolves issues where search terms containing keywords like "Segment" were incorrectly interpreted as filter operands.

* [PR #410](https://github.com/zscaler/zscaler-sdk-python/pull/410) - Added automatic `x-partner-id` header injection for all API requests when `partnerId` is provided in the configuration. The header is automatically included in all requests across OneAPI and Legacy clients (ZIA, ZPA, ZTW, ZCC, ZDX, ZWA) when `partnerId` is specified via config dictionary or `ZSCALER_PARTNER_ID` environment variable.

### Bug Fixes:

* [PR #410](https://github.com/zscaler/zscaler-sdk-python/pull/410) - Fixed context manager deauthentication for ZTW and ZIA services to only trigger on mutations (POST/PUT/DELETE operations). GET-only sessions no longer invoke unnecessary deauthentication, improving performance and reducing API calls.

## 1.8.6 (October 20, 2025)

### Notes

- Python Versions: **v3.8, v3.9, v3.10, v3.11**

* [PR #404](https://github.com/zscaler/zscaler-sdk-python/pull/404) - Fix OAuth authentication to respect proxy configuration. OAuth requests now use the same proxy settings as regular API calls, resolving issues where authentication would fail when proxy was configured.

## 1.8.5 (October 8, 2025)

### Notes

- Python Versions: **v3.8, v3.9, v3.10, v3.11**

### Security Enhancements:

* [PR #396](https://github.com/zscaler/zscaler-sdk-python/pull/396) - Added RSA key strength validation for OAuth JWT authentication. The SDK now enforces a minimum 2048-bit key size for RSA private keys (NIST recommendation), rejecting weak keys with clear error messages.

* [PR #396](https://github.com/zscaler/zscaler-sdk-python/pull/396) - Migrated from PyJWT to python-jose for consistency with the Go SDK. This addresses CWE-326 concerns and is transparent to users (API compatible).

* Added comprehensive security documentation (`SECURITY.md`) with JWT library assessment, security best practices, and key management recommendations.

## 1.8.4 (October 2, 2025)

### Notes

- Python Versions: **v3.8, v3.9, v3.10, v3.11**

### Bug Fixes:

* [PR #393](https://github.com/zscaler/zscaler-sdk-python/pull/393) - Fixed ZIA pagination to use correct API parameter names (`page` and `pageSize` instead of `pageNumber`). Removed forced default page sizes to respect each API's native defaults (ZIA: 100, ZPA: 20). Improved pagination termination logic to stop when partial pages are returned, preventing unnecessary API calls.

* [PR #393](https://github.com/zscaler/zscaler-sdk-python/pull/393) - Fixed `check_static_ip()` method to correctly return `True` for available IPs (HTTP 200 "SUCCESS") instead of treating the plain text response as an error. The method now properly validates IP availability by checking the actual HTTP status code.

* [PR #393](https://github.com/zscaler/zscaler-sdk-python/pull/393) - Fixed regex escape sequence deprecation warnings in `dlp_dictionary.py` docstrings by using raw strings (`r"""`).

## 1.8.3 (September 24, 2025)

### Notes

- Python Versions: **v3.8, v3.9, v3.10, v3.11**

### Bug Fixes:

* [PR #384](https://github.com/zscaler/zscaler-sdk-python/pull/384) - Fixed ZTW EC Group Endpoint Formatting

## 1.8.2 (September 18, 2025)

### Notes

- Python Versions: **v3.8, v3.9, v3.10, v3.11**

### Bug Fixes:

* [PR #380](https://github.com/zscaler/zscaler-sdk-python/pull/380) - Added `.get()` method to `ZscalerObject` base class to support dictionary-like access with default values. This resolves issues where users expected `.get()` method to be available on returned objects from API calls like `list_segments()`.

## 1.8.1 (September 18, 2025)

### Notes

- Python Versions: **v3.8, v3.9, v3.10, v3.11**

### Bug Fixes:

* [PR #378](https://github.com/zscaler/zscaler-sdk-python/pull/378) - Enhanced `download_disable_reasons` function with support for date range filtering, OS type filtering, and timezone specification. Added automatic date format validation and conversion to ZCC API format (YYYY-MM-DD HH:MM:SS GMT). Extended `zcc_param_mapper` decorator to handle new parameters: `start_date`, `end_date`, and `time_zone`.

* [PR #378](https://github.com/zscaler/zscaler-sdk-python/pull/378) - Fixed ZPA pagination issue where subsequent pages used inconsistent page sizes, causing data gaps. Removed automatic pagesize override for ZPA service to let API handle its own default behavior, ensuring consistent pagination throughout all pages.

### Enhancements

* [PR #378](https://github.com/zscaler/zscaler-sdk-python/pull/378) - Added new ZPA model `DesktopPolicyMappingsDTO` and enhanced policy set controllers (v1 and v2) with `device_posture_failure_notification_enabled` and `desktopPolicyMappings` attributes for improved desktop policy management.

## 1.8.0 (September xx, 2025)

### Notes

- Python Versions: **v3.8, v3.9, v3.10, v3.11**

#### NEW ZIA Endpoints

[PR #370](https://github.com/zscaler/zscaler-sdk-python/pull/370) - Added the following new ZIA API Endpoints:
    - Added `GET /virtualZenNodes` Retrieves the ZIA Virtual Service Edge for an organization
    - Added `GET /virtualZenNodes/{id}` Retrieves the ZIA Virtual Service Edge for an organization based on the specified ID
    - Added `POST /virtualZenNodes` Adds a ZIA Virtual Service Edge for an organization
    - Added `PUT /virtualZenNodes/{id}` Updates the ZIA Virtual Service Edge for an organization based on the specified ID
    - Added `DELETE /virtualZenNodes/{id}` Deletes the ZIA Virtual Service Edge for an organization based on the specified ID

[PR #370](https://github.com/zscaler/zscaler-sdk-python/pull/370) - Added the following new ZIA API Endpoints:
    - Added `GET /workloadGroups/{id}` Retrieves the workload group based on the specified ID
    - Added `POST /workloadGroups` Adds a workload group for an organization
    - Added `PUT /workloadGroups/{id}` Updates the workload group for an organization based on the specified ID
    - Added `DELETE /workloadGroups/{id}` Updates the workload group based on the specified ID

[PR #370](https://github.com/zscaler/zscaler-sdk-python/pull/370) - Added the following new ZIA API Endpoints:
    - Added `GET /casbTenant/scanInfo` Retrieves the SaaS Security Scan Configuration information

#### NEW ZPA Endpoints

[PR #370](https://github.com/zscaler/zscaler-sdk-python/pull/370) - Added the following new ZPA API Endpoints:
    - Added `GET /application/bulkUpdateMultiMatch` Update multimatch feature in multiple application segments.
    - Added `GET /application/multimatchUnsupportedReferences` Get the unsupported feature references for multimatch for domains.
  
### Bug Fixes:

[PR #370](https://github.com/zscaler/zscaler-sdk-python/pull/370) -  Fixed ZIA service deauthentication to only occur for POST/PUT/DELETE requests, not GET requests. This improves efficiency by avoiding unnecessary deauthentication calls for read-only operations.

## 1.7.9 (September 4, 2025)

### Notes

- Python Versions: **v3.8, v3.9, v3.10, v3.11**

### Bug Fixes:

* [PR #365](https://github.com/zscaler/zscaler-sdk-python/pull/365) - Enhanced session management for ZIA Legacy client to handle 5-minute idle timeout with proactive session validation and refresh capabilities
Please refer to the [Developer Guide](https://help.zscaler.com/zia/getting-started-zia-api#CreateSession) for more details.

## 1.7.8 (August 29, 2025)

### Notes

- Python Versions: **v3.8, v3.9, v3.10, v3.11**

### Bug Fixes:

* [PR #361](https://github.com/zscaler/zscaler-sdk-python/pull/361) - Fixed non standard camelCase attribute `surrogateIPEnforcedForKnownBrowsers` in ZIA `location_management` model to ensure proper value parsing during response.

## 1.7.7 (August 27, 2025)

### Notes

- Python Versions: **v3.8, v3.9, v3.10, v3.11**

### Bug Fixes:

* [PR #360](https://github.com/zscaler/zscaler-sdk-python/pull/360) - Fixed non standard camelCase attribute `surrogateIPEnforcedForKnownBrowsers` in ZIA `location_management` model to ensure proper value parsing during response.

### Enhancements:

* [PR #360](https://github.com/zscaler/zscaler-sdk-python/pull/360) - Included the following new request parameters in ZIA Cloud Firewall at the `list_rules` function
    - `rule_name` - Filters rules based on rule names using the specified keywords
    - `rule_label` - Filters rules based on rule labels using the specified keywords
    - `rule_order` - Filters rules based on rule order using the specified keywords
    - `rule_description` - Filters rules based on rule descriptions using the specified keywords
    - `rule_action` - Filters rules based on rule actions using the specified keywords
    - `location` - Filters rules based on locations using the specified keywords
    - `department` - Filters rules based on user departments using the specified keywords
    - `group` - Filters rules based on user groups using the specified keywords
    - `user` - Filters rules based on users using the specified keywords
    - `device` - Filters rules based on devices using the specified keywords
    - `device_group` - Filters rules based on device groups using the specified keywords
    - `device_trust_level` - Filters rules based on device trust levels using the specified keywords
    - `src_ips` - Filters rules based on source IP addresses using the specified keywords
    - `dest_addresses` - Filters rules based on destination IP addresses using the specified keywords
    - `src_ip_groups` - Filters rules based on source IP groups using the specified keywords
    - `dest_ip_groups` - Filters rules based on destination IP groups using the specified keywords
    - `nw_application` - Filters rules based on network applications using the specified keywords
    - `nw_services` - Filters rules based on network services using the specified keywords
    - `dest_ip_categories` - Filters rules based on destination URL categories using the specified keywords
    - `page` - Specifies the page offset
    - `page_size` - Specifies the page size. The default size is set to 5,000, if not specified

## 1.7.6 (August 14, 2025)

### Notes

- Python Versions: **v3.8, v3.9, v3.10, v3.11**

### Enhancements:

* [PR #356](https://github.com/zscaler/zscaler-sdk-python/pull/356) - Enhanced OAuth token management with improved caching and simplified expiration handling for OneAPI clients:
  - **Token Caching**: Added optional in-memory token caching with configurable TTL/TTI for improved performance
  - **Simplified Token Expiration**: Implemented natural token expiration handling using `expires_in` attribute from OAuth responses
  - **Cache Key Generation**: Unique cache keys based on client configuration to prevent conflicts
  - **Token Information Monitoring**: Added `get_token_info()` method for real-time token status monitoring
  - **Legacy Client Compatibility**: Enhanced OAuth client gracefully handles legacy client configurations without affecting existing functionality
  - **Singleton Pattern**: OAuth instances are shared across requests with the same configuration for optimal resource usage
  - **Error Handling**: Improved error handling for cache operations and configuration validation
  - **Security-First Approach**: In-memory caching only, no token persistence to disk, following industry best practices
  - **Comprehensive Testing**: Added complete test suite (`tests/test_enhanced_oauth_client.py`) with 12 test cases covering all OAuth functionality

### Bug Fixes:

* [PR #356](https://github.com/zscaler/zscaler-sdk-python/pull/356) - Fixed `dlp_engines` attribute within the `ZIA` `dlp_web_rules` model to ensure attribute is correctly parsed during API response.

## 1.7.5 (August 12, 2025)

### Notes

- Python Versions: **v3.8, v3.9, v3.10, v3.11**

### New ZIA Endpoint - Activation

[PR #354](https://github.com/zscaler/zscaler-sdk-python/pull/354) Added the following new ZIA API Endpoints:
    - Added `GET /eusaStatus/latest` Retrieves the End User Subscription Agreement (EUSA) acceptance status
    - Added `PUT /eusaStatus/{eusaStatusId}` Updates the EUSA status based on the specified status ID

### Bug Fixes:

* [PR #354](https://github.com/zscaler/zscaler-sdk-python/pull/354) ZIA: Fixed deauthentication URL construction for production cloud to use `https://api.zsapi.net`, and non-production to use `https://api.<cloud>.zsapi.net`. This resolves DNS errors like `api.%7bself.cloud%7d.zsapi.net` during context exit.
* [PR #354](https://github.com/zscaler/zscaler-sdk-python/pull/354) ZIA: Deauthentication is now only triggered after mutating requests (POST/PUT/DELETE). GET-only flows will skip deauth to avoid unnecessary calls.
* [PR #354](https://github.com/zscaler/zscaler-sdk-python/pull/354) ZIA: Treat HTTP 204 as a successful deauthentication response in addition to 200.
* [PR #354](https://github.com/zscaler/zscaler-sdk-python/pull/354) Fixed PAC file validation endpoint to send raw data without encoding or escaping, ensuring proper transmission of PAC file content for validation.
* [PR #354](https://github.com/zscaler/zscaler-sdk-python/pull/354) Fixed ZCC `get_device_details()` method to handle mixed snake_case/camelCase API responses and return properly populated DeviceDetails object

### Enhancements:

* [PR #354](https://github.com/zscaler/zscaler-sdk-python/pull/354) ZIA: Include a new `dlpContentLocationsScopes` attribute in the WebDlpRule model used in `/webDlpRules` endpoints
* [PR #354](https://github.com/zscaler/zscaler-sdk-python/pull/354) ZIA: Include a new `passwordProtected` attribute in the File Type Rules model used in `/fileTypeRules` endpoints  
* [PR #354](https://github.com/zscaler/zscaler-sdk-python/pull/354) ZIA: Include a new new query parameter `fetchLocations` is available for the `GET /locations/groups` endpoint

## 1.7.4 (August 12, 2025)

### Notes

- Python Versions: **v3.8, v3.9, v3.10, v3.11**

### New ZIA Endpoint - Activation

[PR #354](https://github.com/zscaler/zscaler-sdk-python/pull/354) Added the following new ZIA API Endpoints:
    - Added `GET /eusaStatus/latest` Retrieves the End User Subscription Agreement (EUSA) acceptance status
    - Added `PUT /eusaStatus/{eusaStatusId}` Updates the EUSA status based on the specified status ID

### Bug Fixes:

* [PR #354](https://github.com/zscaler/zscaler-sdk-python/pull/354) ZIA: Fixed deauthentication URL construction for production cloud to use `https://api.zsapi.net`, and non-production to use `https://api.<cloud>.zsapi.net`. This resolves DNS errors like `api.%7bself.cloud%7d.zsapi.net` during context exit.
* [PR #354](https://github.com/zscaler/zscaler-sdk-python/pull/354) ZIA: Deauthentication is now only triggered after mutating requests (POST/PUT/DELETE). GET-only flows will skip deauth to avoid unnecessary calls.
* [PR #354](https://github.com/zscaler/zscaler-sdk-python/pull/354) ZIA: Treat HTTP 204 as a successful deauthentication response in addition to 200.
* [PR #354](https://github.com/zscaler/zscaler-sdk-python/pull/354) Fixed PAC file validation endpoint to send raw data without encoding or escaping, ensuring proper transmission of PAC file content for validation.
* [PR #354](https://github.com/zscaler/zscaler-sdk-python/pull/354) Fixed ZCC `get_device_details()` method to handle mixed snake_case/camelCase API responses and return properly populated DeviceDetails object

### Enhancements:

* [PR #354](https://github.com/zscaler/zscaler-sdk-python/pull/354) ZIA: Include a new `dlpContentLocationsScopes` attribute in the WebDlpRule model used in `/webDlpRules` endpoints
* [PR #354](https://github.com/zscaler/zscaler-sdk-python/pull/354) ZIA: Include a new `passwordProtected` attribute in the File Type Rules model used in `/fileTypeRules` endpoints  
* [PR #354](https://github.com/zscaler/zscaler-sdk-python/pull/354) ZIA: Include a new new query parameter `fetchLocations` is available for the `GET /locations/groups` endpoint

## 1.7.3 (August 6, 2025)

### Notes

- Python Versions: **v3.8, v3.9, v3.10, v3.11**

### Enhancements:

* [PR #345](https://github.com/zscaler/zscaler-sdk-python/pull/345) - Fixed ZDX models and on demand pagination via `next_offset` parameter
* [PR #345](https://github.com/zscaler/zscaler-sdk-python/pull/345) - Added new ZDX Endpoint `/snapshot/alert`

## 1.7.2 (August 5, 2025)

### Notes

- Python Versions: **v3.8, v3.9, v3.10, v3.11**

### Bug Fixes:

* [PR #344](https://github.com/zscaler/zscaler-sdk-python/pull/344) - Fixed Zidentity pagination support to properly handle API responses with `records` field and pagination metadata

## 1.7.1 (August 5, 2025)

### Notes

- Python Versions: **v3.8, v3.9, v3.10, v3.11**

### Bug Fixes:

* [PR #343](https://github.com/zscaler/zscaler-sdk-python/pull/343) - Fixed Zidentity pagination support to properly handle API responses with `records` field and pagination metadata


## 1.7.0 (August 2, 2025)

### Notes

- Python Versions: **v3.8, v3.9, v3.10, v3.11**

#### NEW Enhancement - ZIdentity API Support

[PR #341](https://github.com/zscaler/zscaler-sdk-python/pull/341): Zscaler [Zidentity](https://help.zscaler.com/zidentity/what-zidentity) API is now available and is supported by this SDK. See [Documentation](https://zscaler-sdk-python.readthedocs.io/en/latest/?badge=latest) for authentication instructions.

### ZIdentity API Client

[PR #341](https://github.com/zscaler/zscaler-sdk-python/pull/341) - Added the following new ZIdentity API Endpoints:
    - Added `GET /api-clients` Retrieves a paginated list of API clients.
    - Added `GET /api-clients/{id}` Retrieves detailed information about a specific API client using its ID.
    - Added `POST /api-clients` Creates a new API client with authentication settings and assigned roles.
    - Added `PUT /api-clients/{id}` Updates the existing API client details based on the provided ID.
    - Added `DELETE /api-clients/{id}` Removes an existing API client from the system.
    - Added `GET /api-clients/{id}/secrets` Retrieves a list of secrets associated with a specific API client using its ID.
    - Added `POST /api-clients/{id}/secrets` Creates and associates a new secret with a specified API client ID
    - Added `DELETE /api-clients/{id}/secrets/{secretId}` Removes a specific secret associated with an API client using the Client ID and secret ID

### ZIdentity Groups

[PR #341](https://github.com/zscaler/zscaler-sdk-python/pull/341) - Added the following new ZIdentity API Endpoints:
    - Added `GET /groups` Retrieves a paginated list of groups with optional query parameters for pagination and filtering by group name or dynamic group status
    - Added `GET /groups/{id}` Retrieves detailed information about a specific group using its unique identifier ID
    - Added `POST /groups` Creates a new group with the specified name and description.
    - Added `PUT /groups/{id}` Update an existing group based on the provided group ID.
    - Added `DELETE /groups/{id}` Deletes an existing group based on the provided group ID.
    - Added `GET /groups/{id}/users` Retrieves the list of users details for a specific group using the group ID.
    - Added `POST /groups/{id}/users` Adds users to an existing group using the unique identifier ID of the group.
    - Added `PUT /groups/{id}/users` Replaces the list of users in a specific group using the group ID.
    - Added `POST /groups/{id}/users/{userId}` Adds a specific user to an existing group using the group ID and the user ID.
    - Added `DELETE /groups/{id}/users/{userId}` Removes a specific user from an existing group using the group ID and the user ID.

### ZIdentity Users

[PR #341](https://github.com/zscaler/zscaler-sdk-python/pull/341) - Added the following new ZIdentity API Endpoints:
    - Added `GET /users` Retrieves a list of users with optional query parameters for pagination and filtering.
    - Added `POST /users` Creates a new user using the provided details.
    - Added `GET /users/{id}` Retrieves detailed information about a specific user using the provided user ID.
    - Added `PUT /users/{id}` Updates the details of an existing user based on the provided user ID.
    - Added `DELETE /users/{id}` Deletes an existing user from the system by the provided user ID.
    - Added `GET /users/{id}/groups` Retrieves a paginated list of groups associated with a specific user ID.

### ZIdentity Entitlements

[PR #341](https://github.com/zscaler/zscaler-sdk-python/pull/341) - Added the following new ZIdentity API Endpoints:
    - Added `GET /users/{id}/admin-entitlements` Retrieves the administrative entitlements for a specific user by their user ID.
    - Added `GET /users/{id}/service-entitlements` Retrieves service entitlements for a specified user ID.

### ZIdentity Resource Servers

[PR #341](https://github.com/zscaler/zscaler-sdk-python/pull/341) - Added the following new ZIdentity API Endpoints:
    - Added `GET /resource-servers` Retrieves a paginated list of resource servers with an optional query parameters for pagination.
    - Added `GET /resource-servers/{id}` Retrieves details about a specific resource server using the server ID

### New ZIA Endpoint - Cloud-to-Cloud DLP Incident Receiver

[PR #341](https://github.com/zscaler/zscaler-sdk-python/pull/341) Added the following new ZIA API Endpoints:
    - Added `GET cloudToCloudIR` Retrieves the list of DLP Incident Receivers configured for Cloud-to-Cloud Incident Forwarding
    - Added `GET cloudToCloudIR/{id}` Retrieves the list of DLP Incident Receivers configured for Cloud-to-Cloud Incident Forwarding
    - Added `GET cloudToCloudIR/lite` Retrieves the list of DLP Incident Receivers configured for Cloud-to-Cloud DLP Incident Forwarding with a subset of information for each Incident Receiver
    - Added `GET cloudToCloudIR/count` Retrieves the number of DLP Incident Receivers configured for Cloud-to-Cloud Incident Forwarding
    - Added `GET cloudToCloudIR/config/{id}/validateDelete` Validates the specified cloud storage configuration (e.g., Amazon S3 bucket configuration) of a Cloud-to-Cloud DLP Incident Receiver

### Bug Fixes

[PR #341](https://github.com/zscaler/zscaler-sdk-python/pull/341) Removed `@staticmethod` from `check_response_for_error` function.

### Documentation

[PR #341](https://github.com/zscaler/zscaler-sdk-python/pull/341) Updated README and other documention. Include Sandbox client instantition examples.

## 1.6.0 (July 30, 2025)

### Notes

- Python Versions: **v3.8, v3.9, v3.10, v3.11**

### New ZPA Endpoint - Admin SSO Configuration Controller

[PR #338](https://github.com/zscaler/zscaler-sdk-python/pull/338) Added the following new ZPA API Endpoints:
    - Added `GET /v2/ssoLoginOptions` Get SSO Login Details
    - Added `POST /v2/ssoLoginOptions` Updates SSO Options for customer

### New ZPA Endpoint - C2C IP Ranges

[PR #338](https://github.com/zscaler/zscaler-sdk-python/pull/338) Added the following new ZPA API Endpoints:
    - Added `POST /v2/ipRanges/search` Get the IP Range by `page` and `pageSize`
    - Added `GET /v2/ipRanges` Get All the IP Range
    - Added `POST /v2/ipRanges` Add new IP Range
    - Added `GET /v2/ipRanges/{ipRangeId}` Get the IP Range Details
    - Added `PUT /v2/ipRanges/{ipRangeId}` Update the IP Range Details
    - Added `DELETE /v2/ipRanges/{ipRangeId}` Delete IP Range

### New ZPA Endpoint - API Keys

[PR #338](https://github.com/zscaler/zscaler-sdk-python/pull/338) Added the following new ZPA API Endpoints:
    - Added `GET /apiKeys` Get all apiKeys details
    - Added `POST /apiKeys` Create api keys for customer
    - Added `GET /apiKeys/{id}` Get apiKeys details by ID
    - Added `PUT /apiKeys/{id}` Update apiKeys by ID
    - Added `DELETE /apiKeys/{id}` Delete apiKeys

### New ZPA Endpoint - Customer Controller

[PR #338](https://github.com/zscaler/zscaler-sdk-python/pull/338) Added the following new ZPA API Endpoints:
    - Added `GET /v2/associationtype/{type}/domains` Get domains for a customer
    - Added `POST /v2/associationtype/{type}/domains` Add or update domains for a customer.

### New ZPA Endpoint - NPClient

[PR #338](https://github.com/zscaler/zscaler-sdk-python/pull/338) Added the following new ZPA API Endpoints:
    - Added `GET /vpnConnectedUsers` Get all applications configuired for a given customer

### New ZPA Endpoint - Private Cloud Controller Group

[PR #338](https://github.com/zscaler/zscaler-sdk-python/pull/338) Added the following new ZPA API Endpoints:
    - Added `GET /privateCloudControllerGroup` Get details of all configured Private Cloud Controller Groups
    - Added `POST /privateCloudControllerGroup` Add a new Private Cloud Controller Groups
    - Added `GET /privateCloudControllerGroup/{privateCloudControllerGroupId}` Get the Private Cloud Controller Group details for the specified ID
    - Added `PUT /privateCloudControllerGroup/{privateCloudControllerGroupId}` Update the Private Cloud Controller Group details for the specified ID
    - Added `DELETE /privateCloudControllerGroup/{privateCloudControllerGroupId}` Delete the Private Cloud Controller Group for the specified ID
    - Added `DELETE /privateCloudControllerGroup/summary` Get all the configured Private Cloud Controller Group ID and Name

### New ZPA Endpoint - Private Cloud Controller Group

[PR #338](https://github.com/zscaler/zscaler-sdk-python/pull/338) Added the following new ZPA API Endpoints:
    - Added `GET /privateCloudController` Get all the configured Private Cloud Controller details
    - Added `PUT /privateCloudController/{privateCloudControllerGroupId}/restart` Trigger restart of the Private Cloud Controller
    - Added `GET /privateCloudController/{privateCloudControllerId}` Gets the Private Cloud Controller details for the specified ID.
    - Added `PUT /privateCloudController/{privateCloudControllerId}` Updates the Private Cloud Controller for the specified ID
    - Added `DELETE /privateCloudController/{privateCloudControllerId}` Delete the Private Cloud Controller for the specified ID

### New ZPA Endpoint - User Portal Controller

[PR #338](https://github.com/zscaler/zscaler-sdk-python/pull/338) Added the following new ZPA API Endpoints:
    - Added `GET /userPortal` Get all configured User Portals
    - Added `GET /userPortal/{id}` Get User Portal for the specified ID
    - Added `PUT /userPortal/{Id}` Update User Portal for the specified ID
    - Added `POST /userPortal` Add a new User Portal
    - Added `DELETE /userPortal/{Id}` Delete a User Portal

### New ZPA Endpoint - User Portal Link Controller

[PR #338](https://github.com/zscaler/zscaler-sdk-python/pull/338) Added the following new ZPA API Endpoints:
    - Added `GET /userPortalLink` Get all configured User Portal Links
    - Added `GET /userPortalLink/{id}` Get User Portal Link for the specified ID
    - Added `GET /userPortalLink/userPortal/{portalId}` Get User Portal Link for a given portal
    - Added `PUT /userPortalLink/{Id}` Update User Portal Link for the specified ID
    - Added `POST /userPortalLink` Add a new User Portal Link
    - Added `POST /userPortalLink/bulk` Add list of User Portal Link
    - Added `DELETE /userPortalLink/{Id}` Delete a User Portal Link for the specified ID

### New ZPA Endpoint - Z-Path Config Override Controller

[PR #338](https://github.com/zscaler/zscaler-sdk-python/pull/338) Added the following new ZPA API Endpoints:
    - Added `GET /configOverrides/{id}` Get config-override details by configId
    - Added `GET /configOverrides` Get all config-override details
    - Added `PUT /configOverrides/{id}` Update config-override for the specified ID
    - Added `POST /configOverrides` Create config-override

## 1.5.9 (July 17, 2025)

### Notes

- Python Versions: **v3.8, v3.9, v3.10, v3.11**

### Bug Fixes:

* [PR #335](https://github.com/zscaler/zscaler-sdk-python/pull/335) - Fixed ZIA functions `add_role` and `update_role` in the `admin_roles` package to preserve uppercase keys in `feature_permissions` attribute as required by the API.
* [PR #335](https://github.com/zscaler/zscaler-sdk-python/pull/335) - Fixed ZIA function `add_admin_user` and `update_admin_user` in the `admin_users` package to properly parse the attributes `scope_entity_ids`
* [PR #335](https://github.com/zscaler/zscaler-sdk-python/pull/335) - Fixed OneAPI client context manager to properly deauthenticate Zscaler sessions when using legacy clients, ensuring staged configurations are activated upon exit.
* [PR #335](https://github.com/zscaler/zscaler-sdk-python/pull/335) - Enhanced OneAPI client context manager to properly deauthenticate Zscaler sessions for both `ZIA` and `ZTW` services. The deauthentication now includes bearer tokens and uses the correct service-specific endpoints (`/zia/api/v1/authenticatedSession` for `ZIA` and `/ztw/api/v1/auth` for `ZTW`), ensuring staged configurations are activated upon context manager exit.

## 1.5.8 (July 11, 2025)

### Notes

- Python Versions: **v3.8, v3.9, v3.10, v3.11**

### Bug Fixes:

* [PR #327](https://github.com/zscaler/zscaler-sdk-python/pull/327) - Fixed `bulk_update` function in `shadow_it_report` package to gracefully handle `204 No Content` responses returned by the ZIA API. The function now returns an empty dictionary `{}` instead of raising an error when no response body is present, ensuring consistency with other update methods across the SDK.

## 1.5.7 (July 10, 2025)

### Notes

- Python Versions: **v3.8, v3.9, v3.10, v3.11**

### Bug Fixes:

* [PR #325](https://github.com/zscaler/zscaler-sdk-python/pull/325) - Fixed `oneapi_response` pagination engine to support `shadow_it_report` custom pagination parameters and prevent backwards pagination retrieval when invoking `resp.next()`.

## 1.5.6 (July 9, 2025)

### Notes

- Python Versions: **v3.8, v3.9, v3.10, v3.11**

### Bug Fixes:

* [PR #323](https://github.com/zscaler/zscaler-sdk-python/pull/323) - Fixed `shadow_it_report` `bulk_update` function and added examples.

## 1.5.5 (July 9, 2025)

### Notes

- Python Versions: **v3.8, v3.9, v3.10, v3.11**

### Bug Fixes:

* [PR #321](https://github.com/zscaler/zscaler-sdk-python/pull/321) - Added ZIA `shadow_it_report` specific pagination parameters `page_number` and `limit`. These parameters are specific to the Shadow IT endpoints.


## 1.5.4 (July 3, 2025)

### Notes

- Python Versions: **v3.8, v3.9, v3.10, v3.11**

### Bug Fixes:

* [PR #317](https://github.com/zscaler/zscaler-sdk-python/pull/317) - Fixed `get_pac_file` response parsing and examples in the ZIA `pac_files` package.

## 1.5.3 (June 25, 2025)

### Notes

- Python Versions: **v3.8, v3.9, v3.10, v3.11**

### Bug Fixes:

* [PR #314](https://github.com/zscaler/zscaler-sdk-python/pull/314) - Enhanced ZIA URL Categories `update_url_category` function to support incremental updates via optional `action` parameter. Users can now perform full updates (replace all URLs) or incremental updates (add/remove specific URLs) using a single method while maintaining backward compatibility with existing specialized functions.

## 1.5.2 (June 23, 2025)

### Notes

- Python Versions: **v3.8, v3.9, v3.10, v3.11**

### Bug Fixes:

* [PR #312](https://github.com/zscaler/zscaler-sdk-python/pull/312) - Removed `url` positional argument from `add_url_category`

## 1.5.1 (June 23, 2025)

### Notes

- Python Versions: **v3.8, v3.9, v3.10, v3.11**

### Bug Fixes:

* [PR #312](https://github.com/zscaler/zscaler-sdk-python/pull/312) - Refactored ZIA Cloud Firewall Rules client to assign `state` from `enabled` directly on request body for improved clarity and maintainability.
* [PR #312](https://github.com/zscaler/zscaler-sdk-python/pull/312) - Removed `url` positional argument from `add_url_category`

## 1.5.0 (June 18, 2025)

### Notes

- Python Versions: **v3.8, v3.9, v3.10, v3.11**

### New ZIA Endpoint - Browser Control Policy

[PR #309](https://github.com/zscaler/zscaler-sdk-python/pull/309) Added the following new ZIA API Endpoints:
    - Added `GET /browserControlSettings` Retrieves the Browser Control status and the list of configured browsers in the Browser Control policy
    - Added `PUT /browserControlSettings` Updates the Browser Control settings.

### New ZIA Endpoint - SaaS Security API (Casb DLP Rules)

[PR #309](https://github.com/zscaler/zscaler-sdk-python/pull/309) Added the following new ZIA API Endpoints:
    - Added `GET /casbDlpRules` Retrieves the SaaS Security Data at Rest Scanning Data Loss Prevention (DLP) rules based on the specified rule type.
    - Added `GET /casbDlpRules/{ruleId}` Retrieves the SaaS Security Data at Rest Scanning DLP rule based on the specified ID
    - Added `GET /casbDlpRules/all` Retrieves all the SaaS Security Data at Rest Scanning DLP rules
    - Added `POST /casbDlpRules` Adds a new SaaS Security Data at Rest Scanning DLP rule
    - Added `PUT /casbDlpRules/{ruleId}` Updates the SaaS Security Data at Rest Scanning DLP rule based on the specified ID
    - Added `DELETE /casbDlpRules/{ruleId}` Deletes the SaaS Security Data at Rest Scanning DLP rule based on the specified ID

### New ZIA Endpoint - SaaS Security API (Casb Malware Rules)

[PR #309](https://github.com/zscaler/zscaler-sdk-python/pull/309) Added the following new ZIA API Endpoints:
    - Added `GET /casbMalwareRules` Retrieves the SaaS Security Data at Rest Scanning Malware Detection rules based on the specified rule type.
    - Added `GET /casbMalwareRules/{ruleId}` Retrieves the SaaS Security Data at Rest Scanning Malware Detection rule based on the specified ID
    - Added `GET /casbMalwareRules/all` Retrieves all the SaaS Security Data at Rest Scanning Malware Detection rules
    - Added `POST /casbMalwareRules` Adds a new SaaS Security Data at Rest Scanning Malware Detection rule.
    - Added `PUT /casbMalwareRules/{ruleId}` Updates the SaaS Security Data at Rest Scanning Malware Detection rule based on the specified ID
    - Added `DELETE /casbMalwareRules/{ruleId}` Deletes the SaaS Security Data at Rest Scanning Malware Detection rule based on the specified ID

### New ZIA Endpoint - SaaS Security API

[PR #309](https://github.com/zscaler/zscaler-sdk-python/pull/309) Added the following new ZIA API Endpoints:
    - Added `GET /domainProfiles/lite` Retrieves the domain profile summary.
    - Added `GET /quarantineTombstoneTemplate/lite` Retrieves the templates for the tombstone file created when a file is quarantined
    - Added `GET /casbEmailLabel/lite` Retrieves the email labels generated for the SaaS Security API policies in a user's email account
    - Added `GET /casbTenant/{tenantId}/tags/policy` Retrieves the tags used in the policy rules associated with a tenant, based on the tenant ID.
    - Added `GET /casbTenant/lite` Retrieves information about the SaaS application tenant

### Enhancements:

[PR #309](https://github.com/zscaler/zscaler-sdk-python/pull/309) - Added support for rateLimit.`maxRetrySeconds` in OneAPI client config to cap retry wait duration when encountering rate-limiting (HTTP 429). Raises zscaler.RetryTooLong if exceeded [Issue #303](https://github.com/zscaler/zscaler-sdk-python/issues/303). This enhancement addresses API limitations with the ZCC endpoints below due to daily hard limits:
  - `/downloadDevices`
  - `/downloadServiceStatus`

### Bug Fixes:

[PR #309](https://github.com/zscaler/zscaler-sdk-python/pull/309) - Fixed JSON serialization for the method `lookup` in the ZIA package to ensure consistency on payload processing between Legacy client path and OneAPI.
[PR #309](https://github.com/zscaler/zscaler-sdk-python/pull/309) - Fixed ZDX `devices` model to address dictionary processing.

## 1.4.4 (June 6, 2025)

### Notes

- Python Versions: **v3.8, v3.9, v3.10, v3.11**

### New ZIA Endpoint - Virtual ZEN Clusters:

* [PR #299](https://github.com/zscaler/zscaler-sdk-python/pull/299) - Added the following new ZIA API Endpoints:
    - Added `GET /virtualZenClusters` Retrieves a list of ZIA Virtual Service Edge clusters.
    - Added `GET /virtualZenClusters/{cluster_id}` Retrieves the Virtual Service Edge cluster based on the specified ID
    - Added `POST /virtualZenClusters` Adds a new Virtual Service Edge cluster. 
    - Added `PUT /virtualZenClusters/{cluster_id}` Updates the Virtual Service Edge cluster based on the specified ID
    - Added `DELETE /virtualZenClusters/{cluster_id}` Deletes the Virtual Service Edge cluster based on the specified ID

### New ZIA Endpoint - Alert Subscription

* [PR #299](https://github.com/zscaler/zscaler-sdk-python/pull/299) - Added the following new ZIA API Endpoints:
    - Added `DELETE /alertSubscriptions/{subscription_id}` Deletes the Alert Subscription based on the specified ID

### Documentation

* [PR #299](https://github.com/zscaler/zscaler-sdk-python/pull/299) - Fixed and added several documentations and included examples.

## 1.4.3 (June 3, 2025)

### Notes

- Python Versions: **v3.8, v3.9, v3.10, v3.11**

### Bug Fixes:

* [PR #296](https://github.com/zscaler/zscaler-sdk-python/pull/296) - Added the following new functions in the ZPA `policies` package: `add_browser_protection_rule_v2` and `update_browser_protection_rule_v2` to support `CLIENTLESS_SESSION_PROTECTION_POLICY` policy type for Browser Protection Rule configuration.
* [PR #296](https://github.com/zscaler/zscaler-sdk-python/pull/296) - Added the following new `object_type` `USER_PORTAL` in the ZPA conditions template `_create_conditions_v2` to support `CLIENTLESS_SESSION_PROTECTION_POLICY` policy type for Browser Protection Rule configuration.
* [PR #296](https://github.com/zscaler/zscaler-sdk-python/pull/296) - Fixed `update_segment()` behavior in all ZPA Application Segment client to ensure that port fields (`tcpPortRange`, `udpPortRange`, `tcpPortRanges`, `udpPortRanges`) are properly cleared when omitted. Previously, omitting these fields during update would leave existing port configurations intact instead of removing them.

## 1.4.2 (May, 29 2025)

### Notes

- Python Versions: **v3.8, v3.9, v3.10, v3.11**

### Bug Fixes:

* [PR #294](https://github.com/zscaler/zscaler-sdk-python/pull/294) - Fixed ZIA `cloud_firewall_rules` model `nw_services` attribute
* [PR #294](https://github.com/zscaler/zscaler-sdk-python/pull/294) - Fixed ZPA `cbi_certficate` pem model attribute
* [PR #294](https://github.com/zscaler/zscaler-sdk-python/pull/294) - Fixed an issue where SDK logging configuration interfered with user-defined loggers. The SDK no longer overrides global logging behavior or disables logs for external modules.

## 1.4.1 (May, 27 2025)

### Notes

- Python Versions: **v3.8, v3.9, v3.10, v3.11**

### Bug Fixes:

* [PR #292](https://github.com/zscaler/zscaler-sdk-python/pull/292) - Fixed ZPA `application_segment` model missing attribute `passive_health_enabled`
* [PR #292](https://github.com/zscaler/zscaler-sdk-python/pull/292) - Added missing ZIA attribute `nw_services` to `reformat_params` list

## 1.4.0 (May, 26 2025)

### Notes

- Python Versions: **v3.8, v3.9, v3.10, v3.11**

#### Zscaler OneAPI Support for Cloud & Branch Connector API
[PR #287](https://github.com/zscaler/zscaler-sdk-python/pull/287): Cloud & Branch Connector API are now supported via [OneAPI](https://help.zscaler.com/oneapi/understanding-oneapi) with Oauth2 authentication support through [Zidentity](https://help.zscaler.com/zidentity/what-zidentity)

### ZPA Application Segment Provision
[PR #287](https://github.com/zscaler/zscaler-sdk-python/pull/287) - Added the following new ZPA API Endpoints:
    - Added `POST /provision` Provision a new application for a given customer by creating all related objects if necessary

### ZPA Application Segment Weighted Load Balancer
[PR #287](https://github.com/zscaler/zscaler-sdk-python/pull/287) - Added the following new ZPA API Endpoints:
    - Added `GET /weightedLbConfig` Get Weighted Load Balancer Config for AppSegment
    - Added `PUT /weightedLbConfig` Update Weighted Load Balancer Config for AppSegment

### ZPA Browser Access Application Segment
[PR #287](https://github.com/zscaler/zscaler-sdk-python/pull/287) - Added dedicated resource `app_segments_ba` for ZPA Browser Access Application Segment provisioning.
[PR #287](https://github.com/zscaler/zscaler-sdk-python/pull/287) - Added dedicated resource `app_segments_ba_v2` for ZPA Browser Access Application Segment provisioning using newly recommended format via block `common_apps_dto.apps_config`

### ZPA Policy-Set-Controller Condition - New Object Type
* [PR #287](https://github.com/zscaler/zscaler-sdk-python/pull/287) - Added the following new `object_types` to function `_create_conditions_v2` in the `policies` package: `CHROME_ENTERPRISE` and `CHROME_POSTURE_PROFILE`

### Zscaler Client Connector (Legacy) New Rate Limiting Headers
* [PR #287](https://github.com/zscaler/zscaler-sdk-python/pull/287) - Enhanced `LegacyZCCClientHelper` rate limiting logic with new headers for more accurate retry-calculations.
  - `X-Rate-Limit-Retry-After-Seconds` - This header is only returned when rate limit for `/downloadDevices` and `downloadServiceStatus` is reached. 
  - The endpoint handler `/downloadDevices` and `downloadServiceStatus` has a rate limit of 3 calls per day.
  - `X-Rate-Limit-Remaining` - This header is returned for all other endpoints. ZCC endpoints called from a specific IP address are subjected to a rate limit of 100 calls per hour. See [Zscaler Client Connector API](https://help.zscaler.com/oneapi/understanding-rate-limiting)

### Bug Fixes:

* [PR #287](https://github.com/zscaler/zscaler-sdk-python/pull/287) - Fixed ZCC functions `remove_devices` and `force_remove_devices` to use custom decorator `zcc_param_mapper` for `os_type` attribute
* [PR #287](https://github.com/zscaler/zscaler-sdk-python/pull/287) - Removed incorrect validation from ZIA `url_categories` function `add_url_category` - [Issue #284](https://github.com/zscaler/zscaler-sdk-python/issues/284)
* [PR #287](https://github.com/zscaler/zscaler-sdk-python/pull/287) - Fixed ZPA `application_segment_pra` model attribute  `common_apps_dto`.
* [PR #287](https://github.com/zscaler/zscaler-sdk-python/pull/287) - Fixed ZPA resources `add_privileged_credential_rule_v2`, and `update_privileged_credential_rule_v2` 
* [PR #287](https://github.com/zscaler/zscaler-sdk-python/pull/287) - Fixed ZPA Application segment v2 Port formatting issue: [Issue #288](https://github.com/zscaler/zscaler-sdk-python/issues/288)
* [PR #287](https://github.com/zscaler/zscaler-sdk-python/pull/287) - Added new ZPA attribute models to support `extranet` features across `server_groups` and `application_segments`
* [PR #287](https://github.com/zscaler/zscaler-sdk-python/pull/287) - Added pre-check on all ZPA  `application_segment` resources to prevent port overlap configuration.
* [PR #287](https://github.com/zscaler/zscaler-sdk-python/pull/287) - Added additional `CLIENT_TYPE` validation within the ZPA policy functions `add_redirection_rule_v2` and `update_redirection_rule_v2`
* [PR #287](https://github.com/zscaler/zscaler-sdk-python/pull/287) - Enhanced `_create_conditions_v2` function used on ZPA Policy v2 condition block.

### Internal Enhancements
* [PR #287](https://github.com/zscaler/zscaler-sdk-python/pull/287) - Enhanced `check_response_for_error` function to parse and display API error messages more clearly.
* [PR #287](https://github.com/zscaler/zscaler-sdk-python/pull/287) - Consolidated all application segment resource models into a single model shared across all Application Segment package resources.

## 1.3.0 (May, 12 2025)

### Notes

- Python Versions: **v3.8, v3.9, v3.10, v3.11**

### ZPA Administrator Controller
[PR #280](https://github.com/zscaler/zscaler-sdk-python/pull/280) - Added the following new ZPA API Endpoints:
    - Added `GET /administrators` Retrieves a list of administrators in a tenant. A maximum of 200 administrators are returned per request.
    - Added `GET /administrators/{admin_id}` Retrieves administrator details for a specific `{admin_id}`
    - Added `POST /administrators` Create an local administrator account
    - Added `PUT /administrators/{admin_id}` Update a local administrator account for a specific `{admin_id}`
    - Added `DELETE /administrators/{admin_id}` Delete a local administrator account for a specific `{admin_id}`

### ZPA Role Controller
[PR #280](https://github.com/zscaler/zscaler-sdk-python/pull/280) - Added the following new ZPA API Endpoints:
    - Added `GET /permissionGroups` Retrieves all the default permission groups.
    - Added `GET /roles` Retrieves a list of all configured roles in a tenant.
    - Added `GET /roles/{admin_id}` Retrieves a role details for a specific `{role_id}`
    - Added `POST /roles` Adds a new role for a tenant.
    - Added `PUT /roles/{admin_id}` Update a role for a specific `{role_id}`
    - Added `DELETE /roles/{role_id}` Delete a role for a specific `{role_id}`

### ZPA Enrollment Certificate Controller
[PR #280](https://github.com/zscaler/zscaler-sdk-python/pull/280) - Added the following new ZPA API Endpoints:
    - Added `POST /enrollmentCert/csr/generate` Creates a CSR for a new enrollment Certificate
    - Added `POST /enrollmentCert/selfsigned/generate` Creates a self signed Enrollment Certificate
    - Added `POST /enrollmentCert` Creates a enrollment Certificate
    - Added `PUT /enrollmentCert/{cert_id}` Update an existing enrollment Certificate
    - Added `DELETE /enrollmentCert/{cert_id}` Delete an existing enrollment Certificate

### ZPA SAML Attribute Controller
[PR #280](https://github.com/zscaler/zscaler-sdk-python/pull/280) - Added the following new ZPA API Endpoints:
    - Added `POST /samlAttribute` Adds a new `SamlAttribute` for a given tenant
    - Added `PUT /samlAttribute/{attr_id}` Update an existing `SamlAttribute` for a given tenant
    - Added `DELETE /samlAttribute/{attr_id}` Delete an existing `SamlAttribute` for a given tenant

### ZPA Client-Settings Controller
[PR #280](https://github.com/zscaler/zscaler-sdk-python/pull/280) - Added the following new ZPA API Endpoints:
    - Added `GET /clientSetting` Retrieves `clientSetting` details. `ClientCertType` defaults to `CLIENT_CONNECTOR`
    - Added `POST /clientSetting` Create or update `clientSetting` for a customer. `ClientCertType` defaults to `CLIENT_CONNECTOR`
    - Added `DELETE /clientSetting` Delete an existing `clientSetting`. `ClientCertType` defaults to `CLIENT_CONNECTOR`
    - Added `GET /clientSetting/all` Retrieves all `clientSetting` details.

### Bug Fixes:

* [PR #280](https://github.com/zscaler/zscaler-sdk-python/pull/280) - Fixed `username` parameter in the ZCC `devices` model for the correct non-standard `snake_case` vs `cameCase` format.
* [PR #280](https://github.com/zscaler/zscaler-sdk-python/pull/280) - Added missing `user_risk_score_levels` and `source_ip_groups` attributes to `dlp_web_rules`

## 1.2.4 (May, 9 2025)

### Notes

- Python Versions: **v3.8, v3.9, v3.10, v3.11**

### Bug Fixes:

* ([#277](https://github.com/zscaler/zscaler-sdk-python/pull/277)) - Fixed documentation formatting.

## 1.2.3 (May, 9 2025)

### Notes

- Python Versions: **v3.8, v3.9, v3.10, v3.11**

### Bug Fixes:

* ([#276](https://github.com/zscaler/zscaler-sdk-python/pull/276)) - Fixed ZCC `download_devices` method to support `octet-stream` header
* ([#276](https://github.com/zscaler/zscaler-sdk-python/pull/276)) - Fixed ZCC `devices` model attributes and attribute edge cases.
* ([#276](https://github.com/zscaler/zscaler-sdk-python/pull/276)) - Fixed missing link for resource `cloud_apps` in both `legacy` and `OneAPI` client
* ([#276](https://github.com/zscaler/zscaler-sdk-python/pull/276)) - `cloud_apps` resource has been renamed to `shadow_it_report` for consistency.

## 1.2.2 (May, 7 2025)

### Notes

- Python Versions: **v3.8, v3.9, v3.10, v3.11**

### Bug Fixes:

* ([#274](https://github.com/zscaler/zscaler-sdk-python/pull/274)) - Fixed ZPA pagination across several resources.
* ([#274](https://github.com/zscaler/zscaler-sdk-python/pull/274)) - Fixed ZCC pagination function resources
* ([#274](https://github.com/zscaler/zscaler-sdk-python/pull/274)) - Fixed ZCC Device resource models
* ([#274](https://github.com/zscaler/zscaler-sdk-python/pull/274)) - Fixed debug logging activation

## 1.2.1 (May, 6 2025)

### Notes

- Python Versions: **v3.8, v3.9, v3.10, v3.11**

### Bug Fix:

* ([#273](https://github.com/zscaler/zscaler-sdk-python/pull/273)) - Fixed ZIA `bandwidth_classes` function names
* ([#273](https://github.com/zscaler/zscaler-sdk-python/pull/273)) - Fixed ZIA `LegacyZIAClient` API client incorrect variable assignment.

## 1.2.0 (May, 5 2025)

### Notes

- Python Versions: **v3.8, v3.9, v3.10, v3.11**

### ZIA NAT Control Policy
[PR #270](https://github.com/zscaler/zscaler-sdk-python/pull/270) - Added the following new ZIA API Endpoints:
    - Added `GET /dnatRules` Retrieves a list of all configured and predefined DNAT Control policies.
    - Added `GET /dnatRules/{rule_id}` Retrieves the DNAT Control policy rule information based on the specified ID
    - Added `POST /dnatRules` Adds a new DNAT Control policy rule. 
    - Added `PUT /dnatRules/{rule_id}` Updates the DNAT Control policy rule information based on the specified ID
    - Added `DELETE /dnatRules/{rule_id}` Deletes the DNAT Control policy rule information based on the specified ID

### ZIA NSS Servers
[PR #270](https://github.com/zscaler/zscaler-sdk-python/pull/270) - Added the following new ZIA API Endpoints:
    - Added `GET /nssServers` Retrieves a list of registered NSS servers.
    - Added `GET /nssServers/{nss_id}` Retrieves the registered NSS server based on the specified ID
    - Added `POST /nssServers` Adds a new NSS server.
    - Added `PUT /nssServers/{nss_id}` Updates an NSS server based on the specified ID
    - Added `DELETE /nssServers/{nss_id}` Deletes an NSS server based on the specified ID

### Enhancements
[PR #270](https://github.com/zscaler/zscaler-sdk-python/pull/270) - Enhanced exceptions handling for clarity during configuration or API errors.
[PR #270](https://github.com/zscaler/zscaler-sdk-python/pull/270) - Enhanced retry mechanism to include `408`, `409` status codes.
[PR #270](https://github.com/zscaler/zscaler-sdk-python/pull/270) - Improved SDK logging behavior to prevent interference with user-defined loggers. Added example for custom logging setup.

## 1.1.0 (April, 28 2025)

### Notes

- Python Versions: **v3.8, v3.9, v3.10, v3.11**

### ZIA Password Expiry Settings
[PR #267](https://github.com/zscaler/zscaler-sdk-python/pull/267) - Added the following new ZIA API Endpoints:
    - Added `GET /passwordExpiry/settings` Retrieves the password expiration information for all the admins
    - Added `PUT /passwordExpiry/settings` Updates the password expiration information for all the admins.

### ZIA Alerts
[PR #267](https://github.com/zscaler/zscaler-sdk-python/pull/267) - Added the following new ZIA API Endpoints:
    - Added `GET /alertSubscriptions` Retrieves a list of all alert subscriptions
    - Added `GET /alertSubscriptions/{subscription_id}` Retrieves the alert subscription information based on the specified ID
    - Added `POST /alertSubscriptions` Adds a new alert subscription.
    - Added `PUT /alertSubscriptions/{subscription_id}` Updates an existing alert subscription based on the specified ID

### ZIA Bandwidth Classes
[PR #267](https://github.com/zscaler/zscaler-sdk-python/pull/267) - Added the following new ZIA API Endpoints:
    - Added `GET /bandwidthClasses` Retrieves a list of bandwidth classes for an organization.
    - Added `GET /bandwidthClasses/lite` Retrieves a list of bandwidth classes for an organization
    - Added `GET /bandwidthClasses/{class_id}` Retrieves the alert subscription information based on the specified ID
    - Added `POST /bandwidthClasses` Adds a new bandwidth class.
    - Added `PUT /bandwidthClasses/{class_id}` Updates a bandwidth class based on the specified ID
    - Added `DELETE /bandwidthClasses/{class_id}` Deletes a bandwidth class based on the specified ID

### ZIA Bandwidth Control Rules
[PR #267](https://github.com/zscaler/zscaler-sdk-python/pull/267) - Added the following new ZIA API Endpoints:
    - Added `GET /bandwidthControlRules` Retrieves all the rules in the Bandwidth Control policy.
    - Added `GET /bandwidthControlRules/lite` Retrieves all the rules in the Bandwidth Control policy
    - Added `GET /bandwidthControlRules/{rule_id}` Retrieves the Bandwidth Control policy rule based on the specified ID
    - Added `POST /bandwidthControlRules` Adds a new Bandwidth Control policy rule.
    - Added `PUT /bandwidthControlRules/{rule_id}` Updates the Bandwidth Control policy rule based on the specified ID
    - Added `DELETE /bandwidthControlRules/{rule_id}` Deletes a Bandwidth Control policy rule based on the specified ID

### ZIA Risk Profiles
[PR #267](https://github.com/zscaler/zscaler-sdk-python/pull/267) - Added the following new ZIA API Endpoints:
    - Added `GET /riskProfiles` Retrieves the cloud application risk profile.
    - Added `GET /riskProfiles/lite` Retrieves the cloud application risk profile
    - Added `GET /riskProfiles/{profile_id}` Retrieves the cloud application risk profile based on the specified ID
    - Added `POST /riskProfiles` Adds a new cloud application risk profile. 
    - Added `PUT /riskProfiles/{profile_id}` Updates the cloud application risk profile based on the specified ID
    - Added `DELETE /riskProfiles/{profile_id}` Deletes the cloud application risk profile based on the specified ID

### ZIA Cloud Application Instances
[PR #267](https://github.com/zscaler/zscaler-sdk-python/pull/267) - Added the following new ZIA API Endpoints:
    - Added `GET /cloudApplicationInstances` Retrieves the list of cloud application instances configured in the ZIA Admin Portal.
    - Added `GET /cloudApplicationInstances/{instance_id}` Retrieves information about a cloud application instance based on the specified ID
    - Added `POST /cloudApplicationInstances` Add a new cloud application instance. 
    - Added `PUT /cloudApplicationInstances/{instance_id}` Updates information about a cloud application instance based on the specified ID
    - Added `DELETE /cloudApplicationInstances/{instance_id}` Deletes a cloud application instance based on the specified ID

### ZIA Cloud Application Instances
[PR #267](https://github.com/zscaler/zscaler-sdk-python/pull/267) - Added the following new ZIA API Endpoints:
    - Added `GET /cloudApplicationInstances` Retrieves the list of cloud application instances configured in the ZIA Admin Portal.
    - Added `GET /cloudApplicationInstances/{instance_id}` Retrieves information about a cloud application instance based on the specified ID
    - Added `POST /cloudApplicationInstances` Add a new cloud application instance. 
    - Added `PUT /cloudApplicationInstances/{instance_id}` Updates information about a cloud application instance based on the specified ID
    - Added `DELETE /cloudApplicationInstances/{instance_id}` Deletes a cloud application instance based on the specified ID

### ZIA Tenancy Restriction Profile
[PR #267](https://github.com/zscaler/zscaler-sdk-python/pull/267) - Added the following new ZIA API Endpoints:
    - Added `GET /tenancyRestrictionProfile` Retrieves all the restricted tenant profiles.
    - Added `GET /tenancyRestrictionProfile/{profile_id}`Retrieves the restricted tenant profile based on the specified ID
    - Added `POST /tenancyRestrictionProfile` Creates restricted tenant profiles. 
    - Added `PUT /tenancyRestrictionProfile/{profile_id}` Updates the restricted tenant profile based on the specified ID
    - Added `DELETE /tenancyRestrictionProfile/{profile_id}` Deletes the restricted tenant profile based on the specified ID
    - Added `GET /tenancyRestrictionProfile/app-item-count/{app_type}/{item_type}` Retrieves the item count of the specified item type for a given application, excluding any specified profile

### ZIA Tenancy Restriction Profile
[PR #267](https://github.com/zscaler/zscaler-sdk-python/pull/267) - Added the following new ZIA API Endpoints:
    - Added `GET /tenancyRestrictionProfile` Retrieves all the restricted tenant profiles.
    - Added `GET /tenancyRestrictionProfile/{profile_id}`Retrieves the restricted tenant profile based on the specified ID
    - Added `POST /tenancyRestrictionProfile` Creates restricted tenant profiles. 
    - Added `PUT /tenancyRestrictionProfile/{profile_id}` Updates the restricted tenant profile based on the specified ID
    - Added `DELETE /tenancyRestrictionProfile/{profile_id}` Deletes the restricted tenant profile based on the specified ID

### ZIA DNS Gateway
[PR #267](https://github.com/zscaler/zscaler-sdk-python/pull/267) - Added the following new ZIA API Endpoints:
    - Added `GET /dnsGateways` Retrieves a list of DNS Gateways.
    - Added `GET /dnsGateways/lite` Retrieves a list of DNS Gateways
    - Added `GET /dnsGateways/{gateway_id}` Retrieves the DNS Gateway based on the specified ID
    - Added `POST /dnsGateways` Adds a new DNS Gateway.
    - Added `PUT /dnsGateways/{gateway_id}` Updates the DNS Gateway based on the specified ID
    - Added `DELETE /dnsGateways/{gateway_id}` Deletes a DNS Gateway based on the specified ID

### ZIA Proxies
[PR #267](https://github.com/zscaler/zscaler-sdk-python/pull/267) - Added the following new ZIA API Endpoints:
    - Added `GET /proxies` Retrieves a list of all proxies configured for third-party proxy services.
    - Added `GET /proxies/lite` Retrieves a list of all proxies configured for third-party proxy services
    - Added `GET /proxies/{proxy_id}` Retrieves the proxy information based on the specified ID
    - Added `POST /proxies` Adds a new proxy for a third-party proxy service.
    - Added `PUT /proxies/{proxy_id}` Updates an existing proxy based on the specified ID
    - Added `DELETE /proxies/{proxy_id}` Deletes an existing proxy based on the specified ID
    - Added `DELETE /dedicatedIPGateways/lite` Retrieves a list of dedicated IP gateways.

### ZIA FTP Settings
[PR #267](https://github.com/zscaler/zscaler-sdk-python/pull/267) - Added the following new ZIA API Endpoints:
    - Added `GET /ftpSettings` Retrieves the FTP Control status and the list of URL categories for which FTP is allowed.
    - Added `PUT /ftpSettings` Updates the FTP Control settings.

### ZIA Mobile Malware Protection Policy
[PR #267](https://github.com/zscaler/zscaler-sdk-python/pull/267) - Added the following new ZIA API Endpoints:
    - Added `GET /mobileAdvanceThreatSettings` Retrieves all the rules in the Mobile Malware Protection policy
    - Added `PUT /mobileAdvanceThreatSettings` Updates the Mobile Malware Protection rule information. 

### ZIA Mobile Malware Protection Policy
[PR #267](https://github.com/zscaler/zscaler-sdk-python/pull/267) - Added the following new ZIA API Endpoints:
    - Added `GET /configAudit` Retrieves the System Audit Report.
    - Added `GET /configAudit/ipVisibility` Retrieves the IP visibility audit report.
    - Added `GET /configAudit/pacFile` Retrieves the PAC file audit report.
**Note**: This endpoint is accessible via Zscaler OneAPI only.

### ZIA Time Intervals
[PR #267](https://github.com/zscaler/zscaler-sdk-python/pull/267) - Added the following new ZIA API Endpoints:
    - Added `GET /timeIntervals` Retrieves the System Audit Report.
    - Added `GET /timeIntervals/{interval_id}` Retrieves the configured time interval based on the specified ID
    - Added `POST /timeIntervals/{interval_id}` Adds a new time interval.
    - Added `PUT /timeIntervals/{interval_id}` Updates the time interval based on the specified ID
    - Added `DELETE /timeIntervals/{interval_id}` Deletes a time interval based on the specified ID

### ZIA Data Center Exclusions
[PR #267](https://github.com/zscaler/zscaler-sdk-python/pull/267) - Added the following new ZIA API Endpoints:
    - Added `GET /dcExclusions` Retrieves the list of Zscaler data centers (DCs) that are currently excluded from service to your organization based on configured exclusions in the ZIA Admin Portal
    - Added `POST /dcExclusions/{dc_id}` Adds a data center (DC) exclusion to disable the tunnels terminating at a virtual IP address of a Zscaler DC
    - Added `PUT /dcExclusions/{dc_id}` Updates a Zscaler data center (DC) exclusion configuration based on the specified ID.
    - Added `DELETE /dcExclusions/{dc_id}` Deletes a Zscaler data center (DC) exclusion configuration based on the specified ID. 
    - Added `GET /datacenters` Retrieves the list of Zscaler data centers (DCs) that can be excluded from service to your organization

## 1.0.3 (April, 28 2025) - BREAKING CHANGES

### Notes

- Python Versions: **v3.8, v3.9, v3.10, v3.11**


#### Zscaler OneAPI Support
[PR #257](https://github.com/zscaler/zscaler-sdk-python/pull/257): Added support for [OneAPI](https://help.zscaler.com/oneapi/understanding-oneapi) Oauth2 authentication support through [Zidentity](https://help.zscaler.com/zidentity/what-zidentity).

**NOTES**
  - Starting at v1.0.0 version this SDK provides dual API client functionality and is backwards compatible with the legacy Zscaler API framework.
  - The new OneAPI framework is compatible only with the following products `ZCC/ZIA/ZPA`.
  - The following products `ZTW` - Cloud Connector and `ZDX` and Zscaler Digital Experience, authentication methods remain unnaffected.
  - The package `ZCON` (Zscaler Cloud and Branch Connector) has been renamed to `ZTW`
  - The following products `ZWA` - Zscaler Workflow Automation authentication methods remain unnaffected.

Refer to the [README](https://github.com/zscaler/zscaler-sdk-python/blob/master/README.md) page for details on client instantiation, and authentication requirements on each individual product.

**WARNING**: Attention Government customers. OneAPI and Zidentity is not currently supported for the following ZIA clouds: `zscalergov` and `zscalerten` or ZPA `GOV`, and `GOVUS`. Please refer to the Zscaler Legacy API Framework section in the [README](https://github.com/zscaler/zscaler-sdk-python/blob/master/README.md) for more information on how authenticate to these environments using the built-in Legacy API method.

[PR #257](https://github.com/zscaler/zscaler-sdk-python/pull/257): All API clients now support Config Setter object `ZCC/ZTW/ZDX/ZIA/ZPA/ZWA`

#### ZCC New Endpoints
[PR #261](https://github.com/zscaler/zscaler-sdk-python/pull/261) - Added the following new ZCC API Endpoints:
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

#### ZIA Sandbox Submission - BREAKING CHANGES
[PR #261](https://github.com/zscaler/zscaler-sdk-python/pull/261) - Authentication to Zscaler Sandbox now use the following attributes during client instantiation.
 - `sandboxToken` - Can also be sourced from the `ZSCALER_SANDBOX_TOKEN` environment variable.
 - `sandboxCloud` - Can also be sourced from the `ZSCALER_SANDBOX_CLOUD` environment variable.

**NOTE** The previous `ZIA_SANDBOX_TOKEN` has been deprecated.

#### ZIA Sandbox Rules
[PR #261](https://github.com/zscaler/zscaler-sdk-python/pull/261) - Added the following new ZIA API Endpoints:
  - Added `GET /sandboxRules` to retrieve the list of all Sandbox policy rules.
  - Added `GET /sandboxRules/{ruleId}` to retrieve the Sandbox policy rule information based on the specified ID.
  - Added `POST /sandboxRules` to add a Sandbox policy rule.
  - Added `PUT /sandboxRules/{ruleId}` to update the Sandbox policy rule configuration for the specified ID.
  - Added `DELETE /sandboxRules/{ruleId}` to delete the Sandbox policy rule based on the specified ID.

#### ZIA DNS Control Rules
[PR #261](https://github.com/zscaler/zscaler-sdk-python/pull/261) - Added the following new ZIA API Endpoints:
  - Added `GET /firewallDnsRules` to retrieve the list of all DNS Control policy rules.
  - Added `GET /firewallDnsRules/{ruleId}` to retrieve the DNS Control policy rule information based on the specified ID.
  - Added `POST /firewallDnsRules` to add a DNS Control policy rules.
  - Added `PUT /firewallDnsRules/{ruleId}` to update the DNS Control policy rule configuration for the specified ID.
  - Added `DELETE /firewallDnsRules/{ruleId}` to delete the DNS Control policy rule based on the specified ID.

#### ZIA IPS Control Rules
[PR #261](https://github.com/zscaler/zscaler-sdk-python/pull/261) - Added the following new ZIA API Endpoints:
  - Added `GET /firewallIpsRules` to retrieve the list of all IPS Control policy rules.
  - Added `GET /firewallIpsRules/{ruleId}` to retrieve the IPS Control policy rule information based on the specified ID.
  - Added `POST /firewallIpsRules` to add a IPS Control policy rule.
  - Added `PUT /firewallIpsRules/{ruleId}` to update the IPS Control policy rule configuration for the specified ID.
  - Added `DELETE /firewallIpsRules/{ruleId}` to delete the IPS Control policy rule based on the specified ID.

#### ZIA File Type Control Policy
[PR #261](https://github.com/zscaler/zscaler-sdk-python/pull/261) - Added the following new ZIA API Endpoints:
  - Added `GET /fileTypeRules` to retrieve the list of all File Type Control policy rules.
  - Added `GET /fileTypeRules/lite` to retrieve the list of all File Type Control policy rules.
  - Added `GET /fileTypeRules/{ruleId}` to retrieve the File Type Control policy rule information based on the specified ID.
  - Added `POST /fileTypeRules` to add a File Type Control policy rule.
  - Added `PUT /fileTypeRules/{ruleId}` to update the File Type Control policy rule configuration for the specified ID.
  - Added `DELETE /fileTypeRules/{ruleId}` to delete the File Type Control policy rule based on the specified ID.

#### ZIA Forwarding Control Policy - Proxy Gateways
[PR #261](https://github.com/zscaler/zscaler-sdk-python/pull/261) - Added the following new ZIA API Endpoints:
  - Added `GET /proxyGateways` to retrieve the proxy gateway information.
  - Added `GET /proxyGateways/lite` to retrieve the name and ID of the proxy.

#### ZIA Cloud Nanolog Streaming Service (NSS)
[PR #261](https://github.com/zscaler/zscaler-sdk-python/pull/261) - Added the following new ZIA API Endpoints:
  - Added `GET /nssFeeds` to retrieve the cloud NSS feeds.
  - Added `GET /nssFeeds/{feedId}` to retrieve information about cloud NSS feed based on the specified ID.
  - Added `POST /nssFeeds` to add a new cloud NSS feed.
  - Added `PUT /nssFeeds/{feedId}` to update cloud NSS feed configuration based on the specified ID.
  - Added `DELETE /nssFeeds/{feedId}` to delete cloud NSS feed configuration based on the specified ID.
  - Added `GET /nssFeeds/feedOutputDefaults` to retrieve the default cloud NSS feed output format for different log types.
  - Added `GET /nssFeeds/testConnectivity/{feedId}` to test the connectivity of cloud NSS feed based on the specified ID
  - Added `POST /nssFeeds/validateFeedFormat` to validates the cloud NSS feed format and returns the validation result

#### ZIA Advanced Threat Protection Policy
[PR #261](https://github.com/zscaler/zscaler-sdk-python/pull/261) - Added the following new ZIA API Endpoints:
  - Added `GET /cyberThreatProtection/advancedThreatSettings` to retrieve the advanced threat configuration settings.
  - Added `PUT /cyberThreatProtection/advancedThreatSettings` to update the advanced threat configuration settings.
  - Added `GET /cyberThreatProtection/maliciousUrls` to retrieve the malicious URLs added to the denylist in the Advanced Threat Protection (ATP) policy
  - Added `PUT /cyberThreatProtection/maliciousUrls` to updates the malicious URLs added to the denylist in ATP policy
  - Added `GET /cyberThreatProtection/securityExceptions` to retrieves information about the security exceptions configured for the ATP policy
  - Added `PUT /cyberThreatProtection/securityExceptions` to update security exceptions for the ATP policy

#### ZIA Advanced Threat Protection Policy
[PR #261](https://github.com/zscaler/zscaler-sdk-python/pull/261) - Added the following new ZIA API Endpoints:
  - Added `GET /cyberThreatProtection/atpMalwareInspection` to retrieve the traffic inspection configurations of Malware Protection policy
  - Added `PUT /cyberThreatProtection/atpMalwareInspection` to update the traffic inspection configurations of Malware Protection policy.
  - Added `GET /cyberThreatProtection/atpMalwareProtocols` to retrieve the protocol inspection configurations of Malware Protection policy
  - Added `PUT /cyberThreatProtection/atpMalwareProtocols` to update the protocol inspection configurations of Malware Protection policy.
  - Added `GET /cyberThreatProtection/malwareSettings` to retrieve the malware protection policy configuration details
  - Added `PUT /cyberThreatProtection/malwareSettings` to update the malware protection policy configuration details.
  - Added `GET /cyberThreatProtection/malwarePolicy` to retrieve information about the security exceptions configured for the Malware Protection policy
  - Added `PUT /cyberThreatProtection/malwarePolicy` to update security exceptions for the Malware Protection policy.

#### ZIA URL & Cloud App Control Policy Settings
[PR #261](https://github.com/zscaler/zscaler-sdk-python/pull/261) - Added the following new ZIA API Endpoints:
  - Added `GET /advancedUrlFilterAndCloudAppSettings` to retrieve information about URL and Cloud App Control advanced policy settings
  - Added `PUT /advancedUrlFilterAndCloudAppSettings` to update the URL and Cloud App Control advanced policy settings

#### ZIA Authentication Settings
[PR #261](https://github.com/zscaler/zscaler-sdk-python/pull/261) - Added the following new ZIA API Endpoints:
  - Added `GET /authSettings` to retrieve the organization's default authentication settings information, including authentication profile and Kerberos authentication information.
  - Added `GET /authSettings/lite` to retrieve organization's default authentication settings information.
  - Added `PUT /authSettings` to update the organization's default authentication settings information.

#### ZIA Advanced Settings
[PR #261](https://github.com/zscaler/zscaler-sdk-python/pull/261) - Added the following new ZIA API Endpoints:
  - Added `GET /advancedSettings` to retrieve information about the advanced settings.
  - Added `PUT /advancedSettings` to update the advanced settings configuration.

#### ZIA Cloud Applications
[PR #261](https://github.com/zscaler/zscaler-sdk-python/pull/261) - Added the following new ZIA API Endpoints:
  - Added `GET /cloudApplications/policy` Retrieves a list of Predefined and User Defined Cloud Applications associated with the DLP rules, Cloud App Control rules, Advanced Settings, Bandwidth Classes, and File Type Control rules.
  - Added `GET /cloudApplications/sslPolicy` Retrieves a list of Predefined and User Defined Cloud Applications associated with the SSL Inspection rules.

#### ZIA Shadow IT Report
[PR #261](https://github.com/zscaler/zscaler-sdk-python/pull/261) - Added the following new ZIA API Endpoints:
- Added `PUT /cloudApplications/bulkUpdate` To Update application status and tag information for predefined or custom cloud applications based on the IDs specified
- Added `GET /cloudApplications/lite` Gets the list of predefined and custom cloud applications
- Added `GET /customTags` Gets the list of custom tags available to assign to cloud applications
- Added `POST /shadowIT/applications/export` Export the Shadow IT Report (in CSV format) for the cloud applications recognized by Zscaler based on their usage in your organization.
- Added `POST /shadowIT/applications/{entity}/exportCsv` Export the Shadow IT Report (in CSV format) for the list of users or known locations identified with using the cloud applications specified in the request.

#### ZIA Remote Assistance Support
[PR #261](https://github.com/zscaler/zscaler-sdk-python/pull/261) - Added the following new ZIA API Endpoints:
  - Added `GET /remoteAssistance` to retrieve information about the Remote Assistance option.
  - Added `PUT /remoteAssistance` to update information about the Remote Assistance option. Using this option, you can allow Zscaler Support to access your organization’s ZIA Admin Portal for a specified time period to troubleshoot issues.

#### ZIA Organization Details
[PR #261](https://github.com/zscaler/zscaler-sdk-python/pull/261) - Added the following new ZIA API Endpoints:
  - Added `GET /orgInformation` to retrieve detailed organization information, including headquarter location, geolocation, address, and contact details.
  - Added `GET /orgInformation/lite` to retrieve minimal organization information.
  - Added `GET /subscriptions` to retrieve information about the list of subscriptions enabled for your tenant. Subscriptions define the various features and levels of functionality that are available to your organization.

#### ZIA End User Notification
[PR #261](https://github.com/zscaler/zscaler-sdk-python/pull/261) - Added the following new ZIA API Endpoints:
  - Added `GET /eun` to retrieve information browser-based end user notification (EUN) configuration details.
  - Added `PUT /eun` to update the browser-based end user notification (EUN) configuration details.

#### ZIA Admin Audit Logs
[PR #261](https://github.com/zscaler/zscaler-sdk-python/pull/261) - Added the following new ZIA API Endpoints:
  - Added `GET /auditlogEntryReport` to retrieve the status of a request for an audit log report.
  - Added `POST /auditlogEntryReport` to create an audit log report for the specified time period and saves it as a CSV file.
  - Added `DELETE /auditlogEntryReport` to cancel the request to create an audit log report.
  - Added `GET /auditlogEntryReport/download` to download the most recently created audit log report.

#### ZIA Extranets
[PR #261](https://github.com/zscaler/zscaler-sdk-python/pull/261) - Added the following new ZIA API Endpoints:
  - Added `GET /extranet` to retrieve the list of extranets configured for the organization
  - Added `GET /extranet/lite` Retrieves the name-ID pairs of all extranets configured for an organization
  - Added `GET /extranet/{Id}` Retrieves information about an extranet based on the specified ID.
  - Added `POST /extranet` Adds a new extranet for the organization.
  - Added `PUT /extranet/{Id}` Updates an extranet based on the specified ID
  - Added `DELETE /extranet/{Id}` Deletes an extranet based on the specified ID

#### ZIA IOT Endpoint
[PR #261](https://github.com/zscaler/zscaler-sdk-python/pull/261) - Added the following new ZIA IOT API Endpoints:
  - Added `GET /iotDiscovery/deviceTypes` Retrieve the mapping between device type universally unique identifier (UUID) values and the device type names for all the device types supported by the Zscaler AI/ML.
  - Added `GET /iotDiscovery/categories` Retrieve the mapping between the device category universally unique identifier (UUID) values and the category names for all the device categories supported by the Zscaler AI/ML. The parent of device category is device type.
  - Added `GET /iotDiscovery/classifications` Retrieve the mapping between the device classification universally unique identifier (UUID) values and the classification names for all the device classifications supported by Zscaler AI/ML. The parent of device classification is device category.
  - Added `GET /iotDiscovery/deviceList` Retrieve a list of discovered devices with the following key contexts, IP address, location, ML auto-label, classification, category, and type.

#### ZIA 3rd-Party App Governance
[PR #261](https://github.com/zscaler/zscaler-sdk-python/pull/261) - Added the following new ZIA API Endpoints:
  - Added `GET /apps/app` to search the 3rd-Party App Governance App Catalog by either app ID or URL.
  - Added `POST /apps/app` to submis an app for analysis in the 3rd-Party App Governance Sandbox.
  - Added `GET /apps/search` to search for an app by name. Any app whose name contains the search term (appName) is returned.
  - Added `GET /app_views/list` to retrieve the list of custom views that you have configured in the 3rd-Party App Governance.
  - Added `GET /app_views/{appViewId}/apps` to retrieves all assets (i.e., apps) that are related to a specified argument (i.e., custom view).

### ZIA Admin Role Endpoints
[PR #261](https://github.com/zscaler/zscaler-sdk-python/pull/261) - Added the following new ZIA API Endpoints:
    - Added `GET /adminRoles/{roleId}` Retrieves the admin role based on the specified ID
    - Added `GET /adminRoles/lite` Retrieves a name and ID dictionary of all admin roles. The list only includes the name and ID for all admin roles.
    - Added `POST /adminRoles` Adds an admin role.
    - Added `PUT /adminRoles/{roleId}` Updates the admin role based on the specified ID.
    - Added `DELETE /adminRoles/{roleId}` Deletes the admin role based on the specified ID.

### ZPA Credential Pool (New)
[PR #261](https://github.com/zscaler/zscaler-sdk-python/pull/261) - Added new ZPA endpoint:
  - Added `GET /credential-pool` Gets the privileged credential pool details for the specified customer.
  - Added `GET /credential-pool/{id}` Gets the privileged credential pool details for the specified customer.
  - Added `GET /credential-pool/{id}/credential` Given Privileged credential pool id gets mapped privileged credential info
  - Added `POST /credential-pool` Adds a new privileged credential pool for the specified customer.
  - Added `PUT /credential-pool/{id}` Updates the existing credential pool for the specified customer.
  - Added `DELETE /credential-pool/{id}` Updates the existing credential pool for the specified customer.

#### ZWA - Zscaler Workflow Automation (NEW)
[PR #261](https://github.com/zscaler/zscaler-sdk-python/pull/261) - Added new ZWA endpoint:
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

### Cloud & Branch Connector - OneAPI Support
[PR #261](https://github.com/zscaler/zscaler-sdk-python/pull/261) - Cloud & Branch Connector package is now compatible with OneAPI and Legacy API framework. Please refer to README for details.
[PR #261](https://github.com/zscaler/zscaler-sdk-python/pull/261) - Cloud & Branch Connector package has been renamed from `zcon` to `ztw`

### ZTW Policy Management
[PR #261](https://github.com/zscaler/zscaler-sdk-python/pull/261) - Added the following new ZTW API Endpoints:
    - Added `GET /ecRules/ecRdr` Retrieves the list of traffic forwarding rules.
    - Added `PUT /ecRules/ecRdr/{ruleId}` Updates a traffic forwarding rule configuration based on the specified ID.
    - Added `POST /ecRules/ecRdr` Creates a new traffic forwarding rule.
    - Added `GET /ecRules/ecRdr/count` Retrieves the count of traffic forwarding rules available in the Cloud & Branch Connector Admin Portal.

### ZTW Policy Resources
[PR #261](https://github.com/zscaler/zscaler-sdk-python/pull/261) - Added the following new ZTW API Endpoints:
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

## 1.0.2 (April, 22 2025) - BREAKING CHANGES

### Notes

- Python Versions: **v3.8, v3.9, v3.10, v3.11**


#### Zscaler OneAPI Support
[PR #257](https://github.com/zscaler/zscaler-sdk-python/pull/257): Added support for [OneAPI](https://help.zscaler.com/oneapi/understanding-oneapi) Oauth2 authentication support through [Zidentity](https://help.zscaler.com/zidentity/what-zidentity).

**NOTES**
  - Starting at v1.0.0 version this SDK provides dual API client functionality and is backwards compatible with the legacy Zscaler API framework.
  - The new OneAPI framework is compatible only with the following products `ZCC/ZIA/ZPA`.
  - The following products `ZTW` - Cloud Connector and `ZDX` and Zscaler Digital Experience, authentication methods remain unnaffected.
  - The package `ZCON` (Zscaler Cloud and Branch Connector) has been renamed to `ZTW`
  - The following products `ZWA` - Zscaler Workflow Automation authentication methods remain unnaffected.

Refer to the [README](https://github.com/zscaler/zscaler-sdk-python/blob/master/README.md) page for details on client instantiation, and authentication requirements on each individual product.

**WARNING**: Attention Government customers. OneAPI and Zidentity is not currently supported for the following ZIA clouds: `zscalergov` and `zscalerten` or ZPA `GOV`, and `GOVUS`. Please refer to the Zscaler Legacy API Framework section in the [README](https://github.com/zscaler/zscaler-sdk-python/blob/master/README.md) for more information on how authenticate to these environments using the built-in Legacy API method.

[PR #257](https://github.com/zscaler/zscaler-sdk-python/pull/257): All API clients now support Config Setter object `ZCC/ZTW/ZDX/ZIA/ZPA/ZWA`

#### ZCC New Endpoints
[PR #260](https://github.com/zscaler/zscaler-sdk-python/pull/260) - Added the following new ZCC API Endpoints:
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

#### ZIA Sandbox Submission - BREAKING CHANGES
[PR #260](https://github.com/zscaler/zscaler-sdk-python/pull/260) - Authentication to Zscaler Sandbox now use the following attributes during client instantiation.
 - `sandboxToken` - Can also be sourced from the `ZSCALER_SANDBOX_TOKEN` environment variable.
 - `sandboxCloud` - Can also be sourced from the `ZSCALER_SANDBOX_CLOUD` environment variable.

**NOTE** The previous `ZIA_SANDBOX_TOKEN` has been deprecated.

#### ZIA Sandbox Rules
[PR #260](https://github.com/zscaler/zscaler-sdk-python/pull/260) - Added the following new ZIA API Endpoints:
  - Added `GET /sandboxRules` to retrieve the list of all Sandbox policy rules.
  - Added `GET /sandboxRules/{ruleId}` to retrieve the Sandbox policy rule information based on the specified ID.
  - Added `POST /sandboxRules` to add a Sandbox policy rule.
  - Added `PUT /sandboxRules/{ruleId}` to update the Sandbox policy rule configuration for the specified ID.
  - Added `DELETE /sandboxRules/{ruleId}` to delete the Sandbox policy rule based on the specified ID.

#### ZIA DNS Control Rules
[PR #260](https://github.com/zscaler/zscaler-sdk-python/pull/260) - Added the following new ZIA API Endpoints:
  - Added `GET /firewallDnsRules` to retrieve the list of all DNS Control policy rules.
  - Added `GET /firewallDnsRules/{ruleId}` to retrieve the DNS Control policy rule information based on the specified ID.
  - Added `POST /firewallDnsRules` to add a DNS Control policy rules.
  - Added `PUT /firewallDnsRules/{ruleId}` to update the DNS Control policy rule configuration for the specified ID.
  - Added `DELETE /firewallDnsRules/{ruleId}` to delete the DNS Control policy rule based on the specified ID.

#### ZIA IPS Control Rules
[PR #260](https://github.com/zscaler/zscaler-sdk-python/pull/260) - Added the following new ZIA API Endpoints:
  - Added `GET /firewallIpsRules` to retrieve the list of all IPS Control policy rules.
  - Added `GET /firewallIpsRules/{ruleId}` to retrieve the IPS Control policy rule information based on the specified ID.
  - Added `POST /firewallIpsRules` to add a IPS Control policy rule.
  - Added `PUT /firewallIpsRules/{ruleId}` to update the IPS Control policy rule configuration for the specified ID.
  - Added `DELETE /firewallIpsRules/{ruleId}` to delete the IPS Control policy rule based on the specified ID.

#### ZIA File Type Control Policy
[PR #260](https://github.com/zscaler/zscaler-sdk-python/pull/260) - Added the following new ZIA API Endpoints:
  - Added `GET /fileTypeRules` to retrieve the list of all File Type Control policy rules.
  - Added `GET /fileTypeRules/lite` to retrieve the list of all File Type Control policy rules.
  - Added `GET /fileTypeRules/{ruleId}` to retrieve the File Type Control policy rule information based on the specified ID.
  - Added `POST /fileTypeRules` to add a File Type Control policy rule.
  - Added `PUT /fileTypeRules/{ruleId}` to update the File Type Control policy rule configuration for the specified ID.
  - Added `DELETE /fileTypeRules/{ruleId}` to delete the File Type Control policy rule based on the specified ID.

#### ZIA Forwarding Control Policy - Proxy Gateways
[PR #260](https://github.com/zscaler/zscaler-sdk-python/pull/260) - Added the following new ZIA API Endpoints:
  - Added `GET /proxyGateways` to retrieve the proxy gateway information.
  - Added `GET /proxyGateways/lite` to retrieve the name and ID of the proxy.

#### ZIA Cloud Nanolog Streaming Service (NSS)
[PR #260](https://github.com/zscaler/zscaler-sdk-python/pull/260) - Added the following new ZIA API Endpoints:
  - Added `GET /nssFeeds` to retrieve the cloud NSS feeds.
  - Added `GET /nssFeeds/{feedId}` to retrieve information about cloud NSS feed based on the specified ID.
  - Added `POST /nssFeeds` to add a new cloud NSS feed.
  - Added `PUT /nssFeeds/{feedId}` to update cloud NSS feed configuration based on the specified ID.
  - Added `DELETE /nssFeeds/{feedId}` to delete cloud NSS feed configuration based on the specified ID.
  - Added `GET /nssFeeds/feedOutputDefaults` to retrieve the default cloud NSS feed output format for different log types.
  - Added `GET /nssFeeds/testConnectivity/{feedId}` to test the connectivity of cloud NSS feed based on the specified ID
  - Added `POST /nssFeeds/validateFeedFormat` to validates the cloud NSS feed format and returns the validation result

#### ZIA Advanced Threat Protection Policy
[PR #260](https://github.com/zscaler/zscaler-sdk-python/pull/260) - Added the following new ZIA API Endpoints:
  - Added `GET /cyberThreatProtection/advancedThreatSettings` to retrieve the advanced threat configuration settings.
  - Added `PUT /cyberThreatProtection/advancedThreatSettings` to update the advanced threat configuration settings.
  - Added `GET /cyberThreatProtection/maliciousUrls` to retrieve the malicious URLs added to the denylist in the Advanced Threat Protection (ATP) policy
  - Added `PUT /cyberThreatProtection/maliciousUrls` to updates the malicious URLs added to the denylist in ATP policy
  - Added `GET /cyberThreatProtection/securityExceptions` to retrieves information about the security exceptions configured for the ATP policy
  - Added `PUT /cyberThreatProtection/securityExceptions` to update security exceptions for the ATP policy

#### ZIA Advanced Threat Protection Policy
[PR #260](https://github.com/zscaler/zscaler-sdk-python/pull/260) - Added the following new ZIA API Endpoints:
  - Added `GET /cyberThreatProtection/atpMalwareInspection` to retrieve the traffic inspection configurations of Malware Protection policy
  - Added `PUT /cyberThreatProtection/atpMalwareInspection` to update the traffic inspection configurations of Malware Protection policy.
  - Added `GET /cyberThreatProtection/atpMalwareProtocols` to retrieve the protocol inspection configurations of Malware Protection policy
  - Added `PUT /cyberThreatProtection/atpMalwareProtocols` to update the protocol inspection configurations of Malware Protection policy.
  - Added `GET /cyberThreatProtection/malwareSettings` to retrieve the malware protection policy configuration details
  - Added `PUT /cyberThreatProtection/malwareSettings` to update the malware protection policy configuration details.
  - Added `GET /cyberThreatProtection/malwarePolicy` to retrieve information about the security exceptions configured for the Malware Protection policy
  - Added `PUT /cyberThreatProtection/malwarePolicy` to update security exceptions for the Malware Protection policy.

#### ZIA URL & Cloud App Control Policy Settings
[PR #260](https://github.com/zscaler/zscaler-sdk-python/pull/260) - Added the following new ZIA API Endpoints:
  - Added `GET /advancedUrlFilterAndCloudAppSettings` to retrieve information about URL and Cloud App Control advanced policy settings
  - Added `PUT /advancedUrlFilterAndCloudAppSettings` to update the URL and Cloud App Control advanced policy settings

#### ZIA Authentication Settings
[PR #260](https://github.com/zscaler/zscaler-sdk-python/pull/260) - Added the following new ZIA API Endpoints:
  - Added `GET /authSettings` to retrieve the organization's default authentication settings information, including authentication profile and Kerberos authentication information.
  - Added `GET /authSettings/lite` to retrieve organization's default authentication settings information.
  - Added `PUT /authSettings` to update the organization's default authentication settings information.

#### ZIA Advanced Settings
[PR #260](https://github.com/zscaler/zscaler-sdk-python/pull/260) - Added the following new ZIA API Endpoints:
  - Added `GET /advancedSettings` to retrieve information about the advanced settings.
  - Added `PUT /advancedSettings` to update the advanced settings configuration.

#### ZIA Cloud Applications
[PR #260](https://github.com/zscaler/zscaler-sdk-python/pull/260) - Added the following new ZIA API Endpoints:
  - Added `GET /cloudApplications/policy` Retrieves a list of Predefined and User Defined Cloud Applications associated with the DLP rules, Cloud App Control rules, Advanced Settings, Bandwidth Classes, and File Type Control rules.
  - Added `GET /cloudApplications/sslPolicy` Retrieves a list of Predefined and User Defined Cloud Applications associated with the SSL Inspection rules.

#### ZIA Shadow IT Report
[PR #260](https://github.com/zscaler/zscaler-sdk-python/pull/260) - Added the following new ZIA API Endpoints:
- Added `PUT /cloudApplications/bulkUpdate` To Update application status and tag information for predefined or custom cloud applications based on the IDs specified
- Added `GET /cloudApplications/lite` Gets the list of predefined and custom cloud applications
- Added `GET /customTags` Gets the list of custom tags available to assign to cloud applications
- Added `POST /shadowIT/applications/export` Export the Shadow IT Report (in CSV format) for the cloud applications recognized by Zscaler based on their usage in your organization.
- Added `POST /shadowIT/applications/{entity}/exportCsv` Export the Shadow IT Report (in CSV format) for the list of users or known locations identified with using the cloud applications specified in the request.

#### ZIA Remote Assistance Support
[PR #260](https://github.com/zscaler/zscaler-sdk-python/pull/260) - Added the following new ZIA API Endpoints:
  - Added `GET /remoteAssistance` to retrieve information about the Remote Assistance option.
  - Added `PUT /remoteAssistance` to update information about the Remote Assistance option. Using this option, you can allow Zscaler Support to access your organization’s ZIA Admin Portal for a specified time period to troubleshoot issues.

#### ZIA Organization Details
[PR #260](https://github.com/zscaler/zscaler-sdk-python/pull/260) - Added the following new ZIA API Endpoints:
  - Added `GET /orgInformation` to retrieve detailed organization information, including headquarter location, geolocation, address, and contact details.
  - Added `GET /orgInformation/lite` to retrieve minimal organization information.
  - Added `GET /subscriptions` to retrieve information about the list of subscriptions enabled for your tenant. Subscriptions define the various features and levels of functionality that are available to your organization.

#### ZIA End User Notification
[PR #260](https://github.com/zscaler/zscaler-sdk-python/pull/260) - Added the following new ZIA API Endpoints:
  - Added `GET /eun` to retrieve information browser-based end user notification (EUN) configuration details.
  - Added `PUT /eun` to update the browser-based end user notification (EUN) configuration details.

#### ZIA Admin Audit Logs
[PR #260](https://github.com/zscaler/zscaler-sdk-python/pull/260) - Added the following new ZIA API Endpoints:
  - Added `GET /auditlogEntryReport` to retrieve the status of a request for an audit log report.
  - Added `POST /auditlogEntryReport` to create an audit log report for the specified time period and saves it as a CSV file.
  - Added `DELETE /auditlogEntryReport` to cancel the request to create an audit log report.
  - Added `GET /auditlogEntryReport/download` to download the most recently created audit log report.

#### ZIA Extranets
[PR #260](https://github.com/zscaler/zscaler-sdk-python/pull/260) - Added the following new ZIA API Endpoints:
  - Added `GET /extranet` to retrieve the list of extranets configured for the organization
  - Added `GET /extranet/lite` Retrieves the name-ID pairs of all extranets configured for an organization
  - Added `GET /extranet/{Id}` Retrieves information about an extranet based on the specified ID.
  - Added `POST /extranet` Adds a new extranet for the organization.
  - Added `PUT /extranet/{Id}` Updates an extranet based on the specified ID
  - Added `DELETE /extranet/{Id}` Deletes an extranet based on the specified ID

#### ZIA IOT Endpoint
[PR #260](https://github.com/zscaler/zscaler-sdk-python/pull/260) - Added the following new ZIA IOT API Endpoints:
  - Added `GET /iotDiscovery/deviceTypes` Retrieve the mapping between device type universally unique identifier (UUID) values and the device type names for all the device types supported by the Zscaler AI/ML.
  - Added `GET /iotDiscovery/categories` Retrieve the mapping between the device category universally unique identifier (UUID) values and the category names for all the device categories supported by the Zscaler AI/ML. The parent of device category is device type.
  - Added `GET /iotDiscovery/classifications` Retrieve the mapping between the device classification universally unique identifier (UUID) values and the classification names for all the device classifications supported by Zscaler AI/ML. The parent of device classification is device category.
  - Added `GET /iotDiscovery/deviceList` Retrieve a list of discovered devices with the following key contexts, IP address, location, ML auto-label, classification, category, and type.

#### ZIA 3rd-Party App Governance
[PR #260](https://github.com/zscaler/zscaler-sdk-python/pull/260) - Added the following new ZIA API Endpoints:
  - Added `GET /apps/app` to search the 3rd-Party App Governance App Catalog by either app ID or URL.
  - Added `POST /apps/app` to submis an app for analysis in the 3rd-Party App Governance Sandbox.
  - Added `GET /apps/search` to search for an app by name. Any app whose name contains the search term (appName) is returned.
  - Added `GET /app_views/list` to retrieve the list of custom views that you have configured in the 3rd-Party App Governance.
  - Added `GET /app_views/{appViewId}/apps` to retrieves all assets (i.e., apps) that are related to a specified argument (i.e., custom view).

### ZIA Admin Role Endpoints
[PR #260](https://github.com/zscaler/zscaler-sdk-python/pull/260) - Added the following new ZIA API Endpoints:
    - Added `GET /adminRoles/{roleId}` Retrieves the admin role based on the specified ID
    - Added `GET /adminRoles/lite` Retrieves a name and ID dictionary of all admin roles. The list only includes the name and ID for all admin roles.
    - Added `POST /adminRoles` Adds an admin role.
    - Added `PUT /adminRoles/{roleId}` Updates the admin role based on the specified ID.
    - Added `DELETE /adminRoles/{roleId}` Deletes the admin role based on the specified ID.

### ZPA Credential Pool (New)
[PR #260](https://github.com/zscaler/zscaler-sdk-python/pull/260) - Added new ZPA endpoint:
  - Added `GET /credential-pool` Gets the privileged credential pool details for the specified customer.
  - Added `GET /credential-pool/{id}` Gets the privileged credential pool details for the specified customer.
  - Added `GET /credential-pool/{id}/credential` Given Privileged credential pool id gets mapped privileged credential info
  - Added `POST /credential-pool` Adds a new privileged credential pool for the specified customer.
  - Added `PUT /credential-pool/{id}` Updates the existing credential pool for the specified customer.
  - Added `DELETE /credential-pool/{id}` Updates the existing credential pool for the specified customer.

#### ZWA - Zscaler Workflow Automation (NEW)
[PR #260](https://github.com/zscaler/zscaler-sdk-python/pull/260) - Added new ZWA endpoint:
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

### Cloud & Branch Connector - OneAPI Support
[PR #260](https://github.com/zscaler/zscaler-sdk-python/pull/260) - Cloud & Branch Connector package is now compatible with OneAPI and Legacy API framework. Please refer to README for details.
[PR #260](https://github.com/zscaler/zscaler-sdk-python/pull/260) - Cloud & Branch Connector package has been renamed from `zcon` to `ztw`

### ZTW Policy Management
[PR #260](https://github.com/zscaler/zscaler-sdk-python/pull/260) - Added the following new ZTW API Endpoints:
    - Added `GET /ecRules/ecRdr` Retrieves the list of traffic forwarding rules.
    - Added `PUT /ecRules/ecRdr/{ruleId}` Updates a traffic forwarding rule configuration based on the specified ID.
    - Added `POST /ecRules/ecRdr` Creates a new traffic forwarding rule.
    - Added `GET /ecRules/ecRdr/count` Retrieves the count of traffic forwarding rules available in the Cloud & Branch Connector Admin Portal.

### ZTW Policy Resources
[PR #260](https://github.com/zscaler/zscaler-sdk-python/pull/260) - Added the following new ZTW API Endpoints:
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

## 1.0.1 (April, 22 2025) - BREAKING CHANGES

### Notes

- Python Versions: **v3.8, v3.9, v3.10, v3.11**


#### Zscaler OneAPI Support
[PR #260](https://github.com/zscaler/zscaler-sdk-python/pull/260): Added support for [OneAPI](https://help.zscaler.com/oneapi/understanding-oneapi) Oauth2 authentication support through [Zidentity](https://help.zscaler.com/zidentity/what-zidentity).

**NOTES**
  - Starting at v1.0.0 version this SDK provides dual API client functionality and is backwards compatible with the legacy Zscaler API framework.
  - The new OneAPI framework is compatible only with the following products `ZCC/ZIA/ZPA`.
  - The following products `ZTW` - Cloud Connector and `ZDX` and Zscaler Digital Experience, authentication methods remain unnaffected.
  - The package `ZCON` (Zscaler Cloud and Branch Connector) has been renamed to `ZTW`
  - The following products `ZWA` - Zscaler Workflow Automation authentication methods remain unnaffected.

Refer to the [README](https://github.com/zscaler/zscaler-sdk-python/blob/master/README.md) page for details on client instantiation, and authentication requirements on each individual product.

**WARNING**: Attention Government customers. OneAPI and Zidentity is not currently supported for the following ZIA clouds: `zscalergov` and `zscalerten` or ZPA `GOV`, and `GOVUS`. Please refer to the Zscaler Legacy API Framework section in the [README](https://github.com/zscaler/zscaler-sdk-python/blob/master/README.md) for more information on how authenticate to these environments using the built-in Legacy API method.

[PR #260](https://github.com/zscaler/zscaler-sdk-python/pull/260): All API clients now support Config Setter object `ZCC/ZTW/ZDX/ZIA/ZPA/ZWA`

#### ZCC New Endpoints
[PR #260](https://github.com/zscaler/zscaler-sdk-python/pull/260) - Added the following new ZCC API Endpoints:
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

#### ZIA Sandbox Submission - BREAKING CHANGES
[PR #260](https://github.com/zscaler/zscaler-sdk-python/pull/260) - Authentication to Zscaler Sandbox now use the following attributes during client instantiation.
 - `sandboxToken` - Can also be sourced from the `ZSCALER_SANDBOX_TOKEN` environment variable.
 - `sandboxCloud` - Can also be sourced from the `ZSCALER_SANDBOX_CLOUD` environment variable.

**NOTE** The previous `ZIA_SANDBOX_TOKEN` has been deprecated.

#### ZIA Sandbox Rules
[PR #260](https://github.com/zscaler/zscaler-sdk-python/pull/260) - Added the following new ZIA API Endpoints:
  - Added `GET /sandboxRules` to retrieve the list of all Sandbox policy rules.
  - Added `GET /sandboxRules/{ruleId}` to retrieve the Sandbox policy rule information based on the specified ID.
  - Added `POST /sandboxRules` to add a Sandbox policy rule.
  - Added `PUT /sandboxRules/{ruleId}` to update the Sandbox policy rule configuration for the specified ID.
  - Added `DELETE /sandboxRules/{ruleId}` to delete the Sandbox policy rule based on the specified ID.

#### ZIA DNS Control Rules
[PR #260](https://github.com/zscaler/zscaler-sdk-python/pull/260) - Added the following new ZIA API Endpoints:
  - Added `GET /firewallDnsRules` to retrieve the list of all DNS Control policy rules.
  - Added `GET /firewallDnsRules/{ruleId}` to retrieve the DNS Control policy rule information based on the specified ID.
  - Added `POST /firewallDnsRules` to add a DNS Control policy rules.
  - Added `PUT /firewallDnsRules/{ruleId}` to update the DNS Control policy rule configuration for the specified ID.
  - Added `DELETE /firewallDnsRules/{ruleId}` to delete the DNS Control policy rule based on the specified ID.

#### ZIA IPS Control Rules
[PR #260](https://github.com/zscaler/zscaler-sdk-python/pull/260) - Added the following new ZIA API Endpoints:
  - Added `GET /firewallIpsRules` to retrieve the list of all IPS Control policy rules.
  - Added `GET /firewallIpsRules/{ruleId}` to retrieve the IPS Control policy rule information based on the specified ID.
  - Added `POST /firewallIpsRules` to add a IPS Control policy rule.
  - Added `PUT /firewallIpsRules/{ruleId}` to update the IPS Control policy rule configuration for the specified ID.
  - Added `DELETE /firewallIpsRules/{ruleId}` to delete the IPS Control policy rule based on the specified ID.

#### ZIA File Type Control Policy
[PR #260](https://github.com/zscaler/zscaler-sdk-python/pull/260) - Added the following new ZIA API Endpoints:
  - Added `GET /fileTypeRules` to retrieve the list of all File Type Control policy rules.
  - Added `GET /fileTypeRules/lite` to retrieve the list of all File Type Control policy rules.
  - Added `GET /fileTypeRules/{ruleId}` to retrieve the File Type Control policy rule information based on the specified ID.
  - Added `POST /fileTypeRules` to add a File Type Control policy rule.
  - Added `PUT /fileTypeRules/{ruleId}` to update the File Type Control policy rule configuration for the specified ID.
  - Added `DELETE /fileTypeRules/{ruleId}` to delete the File Type Control policy rule based on the specified ID.

#### ZIA Forwarding Control Policy - Proxy Gateways
[PR #260](https://github.com/zscaler/zscaler-sdk-python/pull/260) - Added the following new ZIA API Endpoints:
  - Added `GET /proxyGateways` to retrieve the proxy gateway information.
  - Added `GET /proxyGateways/lite` to retrieve the name and ID of the proxy.

#### ZIA Cloud Nanolog Streaming Service (NSS)
[PR #260](https://github.com/zscaler/zscaler-sdk-python/pull/260) - Added the following new ZIA API Endpoints:
  - Added `GET /nssFeeds` to retrieve the cloud NSS feeds.
  - Added `GET /nssFeeds/{feedId}` to retrieve information about cloud NSS feed based on the specified ID.
  - Added `POST /nssFeeds` to add a new cloud NSS feed.
  - Added `PUT /nssFeeds/{feedId}` to update cloud NSS feed configuration based on the specified ID.
  - Added `DELETE /nssFeeds/{feedId}` to delete cloud NSS feed configuration based on the specified ID.
  - Added `GET /nssFeeds/feedOutputDefaults` to retrieve the default cloud NSS feed output format for different log types.
  - Added `GET /nssFeeds/testConnectivity/{feedId}` to test the connectivity of cloud NSS feed based on the specified ID
  - Added `POST /nssFeeds/validateFeedFormat` to validates the cloud NSS feed format and returns the validation result

#### ZIA Advanced Threat Protection Policy
[PR #260](https://github.com/zscaler/zscaler-sdk-python/pull/260) - Added the following new ZIA API Endpoints:
  - Added `GET /cyberThreatProtection/advancedThreatSettings` to retrieve the advanced threat configuration settings.
  - Added `PUT /cyberThreatProtection/advancedThreatSettings` to update the advanced threat configuration settings.
  - Added `GET /cyberThreatProtection/maliciousUrls` to retrieve the malicious URLs added to the denylist in the Advanced Threat Protection (ATP) policy
  - Added `PUT /cyberThreatProtection/maliciousUrls` to updates the malicious URLs added to the denylist in ATP policy
  - Added `GET /cyberThreatProtection/securityExceptions` to retrieves information about the security exceptions configured for the ATP policy
  - Added `PUT /cyberThreatProtection/securityExceptions` to update security exceptions for the ATP policy

#### ZIA Advanced Threat Protection Policy
[PR #260](https://github.com/zscaler/zscaler-sdk-python/pull/260) - Added the following new ZIA API Endpoints:
  - Added `GET /cyberThreatProtection/atpMalwareInspection` to retrieve the traffic inspection configurations of Malware Protection policy
  - Added `PUT /cyberThreatProtection/atpMalwareInspection` to update the traffic inspection configurations of Malware Protection policy.
  - Added `GET /cyberThreatProtection/atpMalwareProtocols` to retrieve the protocol inspection configurations of Malware Protection policy
  - Added `PUT /cyberThreatProtection/atpMalwareProtocols` to update the protocol inspection configurations of Malware Protection policy.
  - Added `GET /cyberThreatProtection/malwareSettings` to retrieve the malware protection policy configuration details
  - Added `PUT /cyberThreatProtection/malwareSettings` to update the malware protection policy configuration details.
  - Added `GET /cyberThreatProtection/malwarePolicy` to retrieve information about the security exceptions configured for the Malware Protection policy
  - Added `PUT /cyberThreatProtection/malwarePolicy` to update security exceptions for the Malware Protection policy.

#### ZIA URL & Cloud App Control Policy Settings
[PR #260](https://github.com/zscaler/zscaler-sdk-python/pull/260) - Added the following new ZIA API Endpoints:
  - Added `GET /advancedUrlFilterAndCloudAppSettings` to retrieve information about URL and Cloud App Control advanced policy settings
  - Added `PUT /advancedUrlFilterAndCloudAppSettings` to update the URL and Cloud App Control advanced policy settings

#### ZIA Authentication Settings
[PR #260](https://github.com/zscaler/zscaler-sdk-python/pull/260) - Added the following new ZIA API Endpoints:
  - Added `GET /authSettings` to retrieve the organization's default authentication settings information, including authentication profile and Kerberos authentication information.
  - Added `GET /authSettings/lite` to retrieve organization's default authentication settings information.
  - Added `PUT /authSettings` to update the organization's default authentication settings information.

#### ZIA Advanced Settings
[PR #260](https://github.com/zscaler/zscaler-sdk-python/pull/260) - Added the following new ZIA API Endpoints:
  - Added `GET /advancedSettings` to retrieve information about the advanced settings.
  - Added `PUT /advancedSettings` to update the advanced settings configuration.

#### ZIA Cloud Applications
[PR #260](https://github.com/zscaler/zscaler-sdk-python/pull/260) - Added the following new ZIA API Endpoints:
  - Added `GET /cloudApplications/policy` Retrieves a list of Predefined and User Defined Cloud Applications associated with the DLP rules, Cloud App Control rules, Advanced Settings, Bandwidth Classes, and File Type Control rules.
  - Added `GET /cloudApplications/sslPolicy` Retrieves a list of Predefined and User Defined Cloud Applications associated with the SSL Inspection rules.

#### ZIA Shadow IT Report
[PR #260](https://github.com/zscaler/zscaler-sdk-python/pull/260) - Added the following new ZIA API Endpoints:
- Added `PUT /cloudApplications/bulkUpdate` To Update application status and tag information for predefined or custom cloud applications based on the IDs specified
- Added `GET /cloudApplications/lite` Gets the list of predefined and custom cloud applications
- Added `GET /customTags` Gets the list of custom tags available to assign to cloud applications
- Added `POST /shadowIT/applications/export` Export the Shadow IT Report (in CSV format) for the cloud applications recognized by Zscaler based on their usage in your organization.
- Added `POST /shadowIT/applications/{entity}/exportCsv` Export the Shadow IT Report (in CSV format) for the list of users or known locations identified with using the cloud applications specified in the request.

#### ZIA Remote Assistance Support
[PR #260](https://github.com/zscaler/zscaler-sdk-python/pull/260) - Added the following new ZIA API Endpoints:
  - Added `GET /remoteAssistance` to retrieve information about the Remote Assistance option.
  - Added `PUT /remoteAssistance` to update information about the Remote Assistance option. Using this option, you can allow Zscaler Support to access your organization’s ZIA Admin Portal for a specified time period to troubleshoot issues.

#### ZIA Organization Details
[PR #260](https://github.com/zscaler/zscaler-sdk-python/pull/260) - Added the following new ZIA API Endpoints:
  - Added `GET /orgInformation` to retrieve detailed organization information, including headquarter location, geolocation, address, and contact details.
  - Added `GET /orgInformation/lite` to retrieve minimal organization information.
  - Added `GET /subscriptions` to retrieve information about the list of subscriptions enabled for your tenant. Subscriptions define the various features and levels of functionality that are available to your organization.

#### ZIA End User Notification
[PR #260](https://github.com/zscaler/zscaler-sdk-python/pull/260) - Added the following new ZIA API Endpoints:
  - Added `GET /eun` to retrieve information browser-based end user notification (EUN) configuration details.
  - Added `PUT /eun` to update the browser-based end user notification (EUN) configuration details.

#### ZIA Admin Audit Logs
[PR #260](https://github.com/zscaler/zscaler-sdk-python/pull/260) - Added the following new ZIA API Endpoints:
  - Added `GET /auditlogEntryReport` to retrieve the status of a request for an audit log report.
  - Added `POST /auditlogEntryReport` to create an audit log report for the specified time period and saves it as a CSV file.
  - Added `DELETE /auditlogEntryReport` to cancel the request to create an audit log report.
  - Added `GET /auditlogEntryReport/download` to download the most recently created audit log report.

#### ZIA Extranets
[PR #260](https://github.com/zscaler/zscaler-sdk-python/pull/260) - Added the following new ZIA API Endpoints:
  - Added `GET /extranet` to retrieve the list of extranets configured for the organization
  - Added `GET /extranet/lite` Retrieves the name-ID pairs of all extranets configured for an organization
  - Added `GET /extranet/{Id}` Retrieves information about an extranet based on the specified ID.
  - Added `POST /extranet` Adds a new extranet for the organization.
  - Added `PUT /extranet/{Id}` Updates an extranet based on the specified ID
  - Added `DELETE /extranet/{Id}` Deletes an extranet based on the specified ID

#### ZIA IOT Endpoint
[PR #260](https://github.com/zscaler/zscaler-sdk-python/pull/260) - Added the following new ZIA IOT API Endpoints:
  - Added `GET /iotDiscovery/deviceTypes` Retrieve the mapping between device type universally unique identifier (UUID) values and the device type names for all the device types supported by the Zscaler AI/ML.
  - Added `GET /iotDiscovery/categories` Retrieve the mapping between the device category universally unique identifier (UUID) values and the category names for all the device categories supported by the Zscaler AI/ML. The parent of device category is device type.
  - Added `GET /iotDiscovery/classifications` Retrieve the mapping between the device classification universally unique identifier (UUID) values and the classification names for all the device classifications supported by Zscaler AI/ML. The parent of device classification is device category.
  - Added `GET /iotDiscovery/deviceList` Retrieve a list of discovered devices with the following key contexts, IP address, location, ML auto-label, classification, category, and type.

#### ZIA 3rd-Party App Governance
[PR #260](https://github.com/zscaler/zscaler-sdk-python/pull/260) - Added the following new ZIA API Endpoints:
  - Added `GET /apps/app` to search the 3rd-Party App Governance App Catalog by either app ID or URL.
  - Added `POST /apps/app` to submis an app for analysis in the 3rd-Party App Governance Sandbox.
  - Added `GET /apps/search` to search for an app by name. Any app whose name contains the search term (appName) is returned.
  - Added `GET /app_views/list` to retrieve the list of custom views that you have configured in the 3rd-Party App Governance.
  - Added `GET /app_views/{appViewId}/apps` to retrieves all assets (i.e., apps) that are related to a specified argument (i.e., custom view).

### ZIA Admin Role Endpoints
[PR #260](https://github.com/zscaler/zscaler-sdk-python/pull/260) - Added the following new ZIA API Endpoints:
    - Added `GET /adminRoles/{roleId}` Retrieves the admin role based on the specified ID
    - Added `GET /adminRoles/lite` Retrieves a name and ID dictionary of all admin roles. The list only includes the name and ID for all admin roles.
    - Added `POST /adminRoles` Adds an admin role.
    - Added `PUT /adminRoles/{roleId}` Updates the admin role based on the specified ID.
    - Added `DELETE /adminRoles/{roleId}` Deletes the admin role based on the specified ID.

### ZPA Credential Pool (New)
[PR #260](https://github.com/zscaler/zscaler-sdk-python/pull/260) - Added new ZPA endpoint:
  - Added `GET /credential-pool` Gets the privileged credential pool details for the specified customer.
  - Added `GET /credential-pool/{id}` Gets the privileged credential pool details for the specified customer.
  - Added `GET /credential-pool/{id}/credential` Given Privileged credential pool id gets mapped privileged credential info
  - Added `POST /credential-pool` Adds a new privileged credential pool for the specified customer.
  - Added `PUT /credential-pool/{id}` Updates the existing credential pool for the specified customer.
  - Added `DELETE /credential-pool/{id}` Updates the existing credential pool for the specified customer.

#### ZWA - Zscaler Workflow Automation (NEW)
[PR #260](https://github.com/zscaler/zscaler-sdk-python/pull/260) - Added new ZWA endpoint:
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

### Cloud & Branch Connector - OneAPI Support
[PR #260](https://github.com/zscaler/zscaler-sdk-python/pull/260) - Cloud & Branch Connector package is now compatible with OneAPI and Legacy API framework. Please refer to README for details.
[PR #260](https://github.com/zscaler/zscaler-sdk-python/pull/260) - Cloud & Branch Connector package has been renamed from `zcon` to `ztw`

### ZTW Policy Management
[PR #260](https://github.com/zscaler/zscaler-sdk-python/pull/260) - Added the following new ZTW API Endpoints:
    - Added `GET /ecRules/ecRdr` Retrieves the list of traffic forwarding rules.
    - Added `PUT /ecRules/ecRdr/{ruleId}` Updates a traffic forwarding rule configuration based on the specified ID.
    - Added `POST /ecRules/ecRdr` Creates a new traffic forwarding rule.
    - Added `GET /ecRules/ecRdr/count` Retrieves the count of traffic forwarding rules available in the Cloud & Branch Connector Admin Portal.

### ZTW Policy Resources
[PR #260](https://github.com/zscaler/zscaler-sdk-python/pull/260) - Added the following new ZTW API Endpoints:
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
  
## 1.0.1 (April, 22 2025) - BREAKING CHANGES

### Notes

- Python Versions: **v3.8, v3.9, v3.10, v3.11**


#### Zscaler OneAPI Support
[PR #257](https://github.com/zscaler/zscaler-sdk-python/pull/257): Added support for [OneAPI](https://help.zscaler.com/oneapi/understanding-oneapi) Oauth2 authentication support through [Zidentity](https://help.zscaler.com/zidentity/what-zidentity).

**NOTES**
  - Starting at v1.0.0 version this SDK provides dual API client functionality and is backwards compatible with the legacy Zscaler API framework.
  - The new OneAPI framework is compatible only with the following products `ZCC/ZIA/ZPA`.
  - The following products `ZTW` - Cloud Connector and `ZDX` and Zscaler Digital Experience, authentication methods remain unnaffected.
  - The package `ZCON` (Zscaler Cloud and Branch Connector) has been renamed to `ZTW`
  - The following products `ZWA` - Zscaler Workflow Automation authentication methods remain unnaffected.

Refer to the [README](https://github.com/zscaler/zscaler-sdk-python/blob/master/README.md) page for details on client instantiation, and authentication requirements on each individual product.

**WARNING**: Attention Government customers. OneAPI and Zidentity is not currently supported for the following ZIA clouds: `zscalergov` and `zscalerten` or ZPA `GOV`, and `GOVUS`. Please refer to the Zscaler Legacy API Framework section in the [README](https://github.com/zscaler/zscaler-sdk-python/blob/master/README.md) for more information on how authenticate to these environments using the built-in Legacy API method.

[PR #257](https://github.com/zscaler/zscaler-sdk-python/pull/257): All API clients now support Config Setter object `ZCC/ZTW/ZDX/ZIA/ZPA/ZWA`

#### ZCC New Endpoints
[PR #259](https://github.com/zscaler/zscaler-sdk-python/pull/259) - Added the following new ZCC API Endpoints:
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

#### ZIA Sandbox Submission - BREAKING CHANGES
[PR #259](https://github.com/zscaler/zscaler-sdk-python/pull/259) - Authentication to Zscaler Sandbox now use the following attributes during client instantiation.
 - `sandboxToken` - Can also be sourced from the `ZSCALER_SANDBOX_TOKEN` environment variable.
 - `sandboxCloud` - Can also be sourced from the `ZSCALER_SANDBOX_CLOUD` environment variable.

**NOTE** The previous `ZIA_SANDBOX_TOKEN` has been deprecated.

#### ZIA Sandbox Rules
[PR #259](https://github.com/zscaler/zscaler-sdk-python/pull/259) - Added the following new ZIA API Endpoints:
  - Added `GET /sandboxRules` to retrieve the list of all Sandbox policy rules.
  - Added `GET /sandboxRules/{ruleId}` to retrieve the Sandbox policy rule information based on the specified ID.
  - Added `POST /sandboxRules` to add a Sandbox policy rule.
  - Added `PUT /sandboxRules/{ruleId}` to update the Sandbox policy rule configuration for the specified ID.
  - Added `DELETE /sandboxRules/{ruleId}` to delete the Sandbox policy rule based on the specified ID.

#### ZIA DNS Control Rules
[PR #259](https://github.com/zscaler/zscaler-sdk-python/pull/259) - Added the following new ZIA API Endpoints:
  - Added `GET /firewallDnsRules` to retrieve the list of all DNS Control policy rules.
  - Added `GET /firewallDnsRules/{ruleId}` to retrieve the DNS Control policy rule information based on the specified ID.
  - Added `POST /firewallDnsRules` to add a DNS Control policy rules.
  - Added `PUT /firewallDnsRules/{ruleId}` to update the DNS Control policy rule configuration for the specified ID.
  - Added `DELETE /firewallDnsRules/{ruleId}` to delete the DNS Control policy rule based on the specified ID.

#### ZIA IPS Control Rules
[PR #259](https://github.com/zscaler/zscaler-sdk-python/pull/259) - Added the following new ZIA API Endpoints:
  - Added `GET /firewallIpsRules` to retrieve the list of all IPS Control policy rules.
  - Added `GET /firewallIpsRules/{ruleId}` to retrieve the IPS Control policy rule information based on the specified ID.
  - Added `POST /firewallIpsRules` to add a IPS Control policy rule.
  - Added `PUT /firewallIpsRules/{ruleId}` to update the IPS Control policy rule configuration for the specified ID.
  - Added `DELETE /firewallIpsRules/{ruleId}` to delete the IPS Control policy rule based on the specified ID.

#### ZIA File Type Control Policy
[PR #259](https://github.com/zscaler/zscaler-sdk-python/pull/259) - Added the following new ZIA API Endpoints:
  - Added `GET /fileTypeRules` to retrieve the list of all File Type Control policy rules.
  - Added `GET /fileTypeRules/lite` to retrieve the list of all File Type Control policy rules.
  - Added `GET /fileTypeRules/{ruleId}` to retrieve the File Type Control policy rule information based on the specified ID.
  - Added `POST /fileTypeRules` to add a File Type Control policy rule.
  - Added `PUT /fileTypeRules/{ruleId}` to update the File Type Control policy rule configuration for the specified ID.
  - Added `DELETE /fileTypeRules/{ruleId}` to delete the File Type Control policy rule based on the specified ID.

#### ZIA Forwarding Control Policy - Proxy Gateways
[PR #259](https://github.com/zscaler/zscaler-sdk-python/pull/259) - Added the following new ZIA API Endpoints:
  - Added `GET /proxyGateways` to retrieve the proxy gateway information.
  - Added `GET /proxyGateways/lite` to retrieve the name and ID of the proxy.

#### ZIA Cloud Nanolog Streaming Service (NSS)
[PR #259](https://github.com/zscaler/zscaler-sdk-python/pull/259) - Added the following new ZIA API Endpoints:
  - Added `GET /nssFeeds` to retrieve the cloud NSS feeds.
  - Added `GET /nssFeeds/{feedId}` to retrieve information about cloud NSS feed based on the specified ID.
  - Added `POST /nssFeeds` to add a new cloud NSS feed.
  - Added `PUT /nssFeeds/{feedId}` to update cloud NSS feed configuration based on the specified ID.
  - Added `DELETE /nssFeeds/{feedId}` to delete cloud NSS feed configuration based on the specified ID.
  - Added `GET /nssFeeds/feedOutputDefaults` to retrieve the default cloud NSS feed output format for different log types.
  - Added `GET /nssFeeds/testConnectivity/{feedId}` to test the connectivity of cloud NSS feed based on the specified ID
  - Added `POST /nssFeeds/validateFeedFormat` to validates the cloud NSS feed format and returns the validation result

#### ZIA Advanced Threat Protection Policy
[PR #259](https://github.com/zscaler/zscaler-sdk-python/pull/259) - Added the following new ZIA API Endpoints:
  - Added `GET /cyberThreatProtection/advancedThreatSettings` to retrieve the advanced threat configuration settings.
  - Added `PUT /cyberThreatProtection/advancedThreatSettings` to update the advanced threat configuration settings.
  - Added `GET /cyberThreatProtection/maliciousUrls` to retrieve the malicious URLs added to the denylist in the Advanced Threat Protection (ATP) policy
  - Added `PUT /cyberThreatProtection/maliciousUrls` to updates the malicious URLs added to the denylist in ATP policy
  - Added `GET /cyberThreatProtection/securityExceptions` to retrieves information about the security exceptions configured for the ATP policy
  - Added `PUT /cyberThreatProtection/securityExceptions` to update security exceptions for the ATP policy

#### ZIA Advanced Threat Protection Policy
[PR #259](https://github.com/zscaler/zscaler-sdk-python/pull/259) - Added the following new ZIA API Endpoints:
  - Added `GET /cyberThreatProtection/atpMalwareInspection` to retrieve the traffic inspection configurations of Malware Protection policy
  - Added `PUT /cyberThreatProtection/atpMalwareInspection` to update the traffic inspection configurations of Malware Protection policy.
  - Added `GET /cyberThreatProtection/atpMalwareProtocols` to retrieve the protocol inspection configurations of Malware Protection policy
  - Added `PUT /cyberThreatProtection/atpMalwareProtocols` to update the protocol inspection configurations of Malware Protection policy.
  - Added `GET /cyberThreatProtection/malwareSettings` to retrieve the malware protection policy configuration details
  - Added `PUT /cyberThreatProtection/malwareSettings` to update the malware protection policy configuration details.
  - Added `GET /cyberThreatProtection/malwarePolicy` to retrieve information about the security exceptions configured for the Malware Protection policy
  - Added `PUT /cyberThreatProtection/malwarePolicy` to update security exceptions for the Malware Protection policy.

#### ZIA URL & Cloud App Control Policy Settings
[PR #259](https://github.com/zscaler/zscaler-sdk-python/pull/259) - Added the following new ZIA API Endpoints:
  - Added `GET /advancedUrlFilterAndCloudAppSettings` to retrieve information about URL and Cloud App Control advanced policy settings
  - Added `PUT /advancedUrlFilterAndCloudAppSettings` to update the URL and Cloud App Control advanced policy settings

#### ZIA Authentication Settings
[PR #259](https://github.com/zscaler/zscaler-sdk-python/pull/259) - Added the following new ZIA API Endpoints:
  - Added `GET /authSettings` to retrieve the organization's default authentication settings information, including authentication profile and Kerberos authentication information.
  - Added `GET /authSettings/lite` to retrieve organization's default authentication settings information.
  - Added `PUT /authSettings` to update the organization's default authentication settings information.

#### ZIA Advanced Settings
[PR #259](https://github.com/zscaler/zscaler-sdk-python/pull/259) - Added the following new ZIA API Endpoints:
  - Added `GET /advancedSettings` to retrieve information about the advanced settings.
  - Added `PUT /advancedSettings` to update the advanced settings configuration.

#### ZIA Cloud Applications
[PR #259](https://github.com/zscaler/zscaler-sdk-python/pull/259) - Added the following new ZIA API Endpoints:
  - Added `GET /cloudApplications/policy` Retrieves a list of Predefined and User Defined Cloud Applications associated with the DLP rules, Cloud App Control rules, Advanced Settings, Bandwidth Classes, and File Type Control rules.
  - Added `GET /cloudApplications/sslPolicy` Retrieves a list of Predefined and User Defined Cloud Applications associated with the SSL Inspection rules.

#### ZIA Shadow IT Report
[PR #259](https://github.com/zscaler/zscaler-sdk-python/pull/259) - Added the following new ZIA API Endpoints:
- Added `PUT /cloudApplications/bulkUpdate` To Update application status and tag information for predefined or custom cloud applications based on the IDs specified
- Added `GET /cloudApplications/lite` Gets the list of predefined and custom cloud applications
- Added `GET /customTags` Gets the list of custom tags available to assign to cloud applications
- Added `POST /shadowIT/applications/export` Export the Shadow IT Report (in CSV format) for the cloud applications recognized by Zscaler based on their usage in your organization.
- Added `POST /shadowIT/applications/{entity}/exportCsv` Export the Shadow IT Report (in CSV format) for the list of users or known locations identified with using the cloud applications specified in the request.

#### ZIA Remote Assistance Support
[PR #259](https://github.com/zscaler/zscaler-sdk-python/pull/259) - Added the following new ZIA API Endpoints:
  - Added `GET /remoteAssistance` to retrieve information about the Remote Assistance option.
  - Added `PUT /remoteAssistance` to update information about the Remote Assistance option. Using this option, you can allow Zscaler Support to access your organization’s ZIA Admin Portal for a specified time period to troubleshoot issues.

#### ZIA Organization Details
[PR #259](https://github.com/zscaler/zscaler-sdk-python/pull/259) - Added the following new ZIA API Endpoints:
  - Added `GET /orgInformation` to retrieve detailed organization information, including headquarter location, geolocation, address, and contact details.
  - Added `GET /orgInformation/lite` to retrieve minimal organization information.
  - Added `GET /subscriptions` to retrieve information about the list of subscriptions enabled for your tenant. Subscriptions define the various features and levels of functionality that are available to your organization.

#### ZIA End User Notification
[PR #259](https://github.com/zscaler/zscaler-sdk-python/pull/259) - Added the following new ZIA API Endpoints:
  - Added `GET /eun` to retrieve information browser-based end user notification (EUN) configuration details.
  - Added `PUT /eun` to update the browser-based end user notification (EUN) configuration details.

#### ZIA Admin Audit Logs
[PR #259](https://github.com/zscaler/zscaler-sdk-python/pull/259) - Added the following new ZIA API Endpoints:
  - Added `GET /auditlogEntryReport` to retrieve the status of a request for an audit log report.
  - Added `POST /auditlogEntryReport` to create an audit log report for the specified time period and saves it as a CSV file.
  - Added `DELETE /auditlogEntryReport` to cancel the request to create an audit log report.
  - Added `GET /auditlogEntryReport/download` to download the most recently created audit log report.

#### ZIA Extranets
[PR #259](https://github.com/zscaler/zscaler-sdk-python/pull/259) - Added the following new ZIA API Endpoints:
  - Added `GET /extranet` to retrieve the list of extranets configured for the organization
  - Added `GET /extranet/lite` Retrieves the name-ID pairs of all extranets configured for an organization
  - Added `GET /extranet/{Id}` Retrieves information about an extranet based on the specified ID.
  - Added `POST /extranet` Adds a new extranet for the organization.
  - Added `PUT /extranet/{Id}` Updates an extranet based on the specified ID
  - Added `DELETE /extranet/{Id}` Deletes an extranet based on the specified ID

#### ZIA IOT Endpoint
[PR #259](https://github.com/zscaler/zscaler-sdk-python/pull/259) - Added the following new ZIA IOT API Endpoints:
  - Added `GET /iotDiscovery/deviceTypes` Retrieve the mapping between device type universally unique identifier (UUID) values and the device type names for all the device types supported by the Zscaler AI/ML.
  - Added `GET /iotDiscovery/categories` Retrieve the mapping between the device category universally unique identifier (UUID) values and the category names for all the device categories supported by the Zscaler AI/ML. The parent of device category is device type.
  - Added `GET /iotDiscovery/classifications` Retrieve the mapping between the device classification universally unique identifier (UUID) values and the classification names for all the device classifications supported by Zscaler AI/ML. The parent of device classification is device category.
  - Added `GET /iotDiscovery/deviceList` Retrieve a list of discovered devices with the following key contexts, IP address, location, ML auto-label, classification, category, and type.

#### ZIA 3rd-Party App Governance
[PR #259](https://github.com/zscaler/zscaler-sdk-python/pull/259) - Added the following new ZIA API Endpoints:
  - Added `GET /apps/app` to search the 3rd-Party App Governance App Catalog by either app ID or URL.
  - Added `POST /apps/app` to submis an app for analysis in the 3rd-Party App Governance Sandbox.
  - Added `GET /apps/search` to search for an app by name. Any app whose name contains the search term (appName) is returned.
  - Added `GET /app_views/list` to retrieve the list of custom views that you have configured in the 3rd-Party App Governance.
  - Added `GET /app_views/{appViewId}/apps` to retrieves all assets (i.e., apps) that are related to a specified argument (i.e., custom view).

### ZIA Admin Role Endpoints
[PR #259](https://github.com/zscaler/zscaler-sdk-python/pull/259) - Added the following new ZIA API Endpoints:
    - Added `GET /adminRoles/{roleId}` Retrieves the admin role based on the specified ID
    - Added `GET /adminRoles/lite` Retrieves a name and ID dictionary of all admin roles. The list only includes the name and ID for all admin roles.
    - Added `POST /adminRoles` Adds an admin role.
    - Added `PUT /adminRoles/{roleId}` Updates the admin role based on the specified ID.
    - Added `DELETE /adminRoles/{roleId}` Deletes the admin role based on the specified ID.

### ZPA Credential Pool (New)
[PR #259](https://github.com/zscaler/zscaler-sdk-python/pull/259) - Added new ZPA endpoint:
  - Added `GET /credential-pool` Gets the privileged credential pool details for the specified customer.
  - Added `GET /credential-pool/{id}` Gets the privileged credential pool details for the specified customer.
  - Added `GET /credential-pool/{id}/credential` Given Privileged credential pool id gets mapped privileged credential info
  - Added `POST /credential-pool` Adds a new privileged credential pool for the specified customer.
  - Added `PUT /credential-pool/{id}` Updates the existing credential pool for the specified customer.
  - Added `DELETE /credential-pool/{id}` Updates the existing credential pool for the specified customer.

#### ZWA - Zscaler Workflow Automation (NEW)
[PR #259](https://github.com/zscaler/zscaler-sdk-python/pull/259) - Added new ZWA endpoint:
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

### Cloud & Branch Connector - OneAPI Support
[PR #259](https://github.com/zscaler/zscaler-sdk-python/pull/259) - Cloud & Branch Connector package is now compatible with OneAPI and Legacy API framework. Please refer to README for details.
[PR #259](https://github.com/zscaler/zscaler-sdk-python/pull/259) - Cloud & Branch Connector package has been renamed from `zcon` to `ztw`

### ZTW Policy Management
[PR #259](https://github.com/zscaler/zscaler-sdk-python/pull/259) - Added the following new ZTW API Endpoints:
    - Added `GET /ecRules/ecRdr` Retrieves the list of traffic forwarding rules.
    - Added `PUT /ecRules/ecRdr/{ruleId}` Updates a traffic forwarding rule configuration based on the specified ID.
    - Added `POST /ecRules/ecRdr` Creates a new traffic forwarding rule.
    - Added `GET /ecRules/ecRdr/count` Retrieves the count of traffic forwarding rules available in the Cloud & Branch Connector Admin Portal.

### ZTW Policy Resources
[PR #259](https://github.com/zscaler/zscaler-sdk-python/pull/259) - Added the following new ZTW API Endpoints:
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

## 1.0.1 (April, 22 2025) - BREAKING CHANGES

### Notes

- Python Versions: **v3.8, v3.9, v3.10, v3.11**


#### Zscaler OneAPI Support
[PR #259](https://github.com/zscaler/zscaler-sdk-python/pull/259): Added support for [OneAPI](https://help.zscaler.com/oneapi/understanding-oneapi) Oauth2 authentication support through [Zidentity](https://help.zscaler.com/zidentity/what-zidentity).

**NOTES**
  - Starting at v1.0.0 version this SDK provides dual API client functionality and is backwards compatible with the legacy Zscaler API framework.
  - The new OneAPI framework is compatible only with the following products `ZCC/ZIA/ZPA`.
  - The following products `ZTW` - Cloud Connector and `ZDX` and Zscaler Digital Experience, authentication methods remain unnaffected.
  - The package `ZCON` (Zscaler Cloud and Branch Connector) has been renamed to `ZTW`
  - The following products `ZWA` - Zscaler Workflow Automation authentication methods remain unnaffected.

Refer to the [README](https://github.com/zscaler/zscaler-sdk-python/blob/master/README.md) page for details on client instantiation, and authentication requirements on each individual product.

**WARNING**: Attention Government customers. OneAPI and Zidentity is not currently supported for the following ZIA clouds: `zscalergov` and `zscalerten` or ZPA `GOV`, and `GOVUS`. Please refer to the Zscaler Legacy API Framework section in the [README](https://github.com/zscaler/zscaler-sdk-python/blob/master/README.md) for more information on how authenticate to these environments using the built-in Legacy API method.

[PR #259](https://github.com/zscaler/zscaler-sdk-python/pull/259): All API clients now support Config Setter object `ZCC/ZTW/ZDX/ZIA/ZPA/ZWA`

#### ZCC New Endpoints
[PR #259](https://github.com/zscaler/zscaler-sdk-python/pull/259) - Added the following new ZCC API Endpoints:
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

#### ZIA Sandbox Submission - BREAKING CHANGES
[PR #259](https://github.com/zscaler/zscaler-sdk-python/pull/259) - Authentication to Zscaler Sandbox now use the following attributes during client instantiation.
 - `sandboxToken` - Can also be sourced from the `ZSCALER_SANDBOX_TOKEN` environment variable.
 - `sandboxCloud` - Can also be sourced from the `ZSCALER_SANDBOX_CLOUD` environment variable.

**NOTE** The previous `ZIA_SANDBOX_TOKEN` has been deprecated.

#### ZIA Sandbox Rules
[PR #259](https://github.com/zscaler/zscaler-sdk-python/pull/259) - Added the following new ZIA API Endpoints:
  - Added `GET /sandboxRules` to retrieve the list of all Sandbox policy rules.
  - Added `GET /sandboxRules/{ruleId}` to retrieve the Sandbox policy rule information based on the specified ID.
  - Added `POST /sandboxRules` to add a Sandbox policy rule.
  - Added `PUT /sandboxRules/{ruleId}` to update the Sandbox policy rule configuration for the specified ID.
  - Added `DELETE /sandboxRules/{ruleId}` to delete the Sandbox policy rule based on the specified ID.

#### ZIA DNS Control Rules
[PR #259](https://github.com/zscaler/zscaler-sdk-python/pull/259) - Added the following new ZIA API Endpoints:
  - Added `GET /firewallDnsRules` to retrieve the list of all DNS Control policy rules.
  - Added `GET /firewallDnsRules/{ruleId}` to retrieve the DNS Control policy rule information based on the specified ID.
  - Added `POST /firewallDnsRules` to add a DNS Control policy rules.
  - Added `PUT /firewallDnsRules/{ruleId}` to update the DNS Control policy rule configuration for the specified ID.
  - Added `DELETE /firewallDnsRules/{ruleId}` to delete the DNS Control policy rule based on the specified ID.

#### ZIA IPS Control Rules
[PR #259](https://github.com/zscaler/zscaler-sdk-python/pull/259) - Added the following new ZIA API Endpoints:
  - Added `GET /firewallIpsRules` to retrieve the list of all IPS Control policy rules.
  - Added `GET /firewallIpsRules/{ruleId}` to retrieve the IPS Control policy rule information based on the specified ID.
  - Added `POST /firewallIpsRules` to add a IPS Control policy rule.
  - Added `PUT /firewallIpsRules/{ruleId}` to update the IPS Control policy rule configuration for the specified ID.
  - Added `DELETE /firewallIpsRules/{ruleId}` to delete the IPS Control policy rule based on the specified ID.

#### ZIA File Type Control Policy
[PR #259](https://github.com/zscaler/zscaler-sdk-python/pull/259) - Added the following new ZIA API Endpoints:
  - Added `GET /fileTypeRules` to retrieve the list of all File Type Control policy rules.
  - Added `GET /fileTypeRules/lite` to retrieve the list of all File Type Control policy rules.
  - Added `GET /fileTypeRules/{ruleId}` to retrieve the File Type Control policy rule information based on the specified ID.
  - Added `POST /fileTypeRules` to add a File Type Control policy rule.
  - Added `PUT /fileTypeRules/{ruleId}` to update the File Type Control policy rule configuration for the specified ID.
  - Added `DELETE /fileTypeRules/{ruleId}` to delete the File Type Control policy rule based on the specified ID.

#### ZIA Forwarding Control Policy - Proxy Gateways
[PR #259](https://github.com/zscaler/zscaler-sdk-python/pull/259) - Added the following new ZIA API Endpoints:
  - Added `GET /proxyGateways` to retrieve the proxy gateway information.
  - Added `GET /proxyGateways/lite` to retrieve the name and ID of the proxy.

#### ZIA Cloud Nanolog Streaming Service (NSS)
[PR #259](https://github.com/zscaler/zscaler-sdk-python/pull/259) - Added the following new ZIA API Endpoints:
  - Added `GET /nssFeeds` to retrieve the cloud NSS feeds.
  - Added `GET /nssFeeds/{feedId}` to retrieve information about cloud NSS feed based on the specified ID.
  - Added `POST /nssFeeds` to add a new cloud NSS feed.
  - Added `PUT /nssFeeds/{feedId}` to update cloud NSS feed configuration based on the specified ID.
  - Added `DELETE /nssFeeds/{feedId}` to delete cloud NSS feed configuration based on the specified ID.
  - Added `GET /nssFeeds/feedOutputDefaults` to retrieve the default cloud NSS feed output format for different log types.
  - Added `GET /nssFeeds/testConnectivity/{feedId}` to test the connectivity of cloud NSS feed based on the specified ID
  - Added `POST /nssFeeds/validateFeedFormat` to validates the cloud NSS feed format and returns the validation result

#### ZIA Advanced Threat Protection Policy
[PR #259](https://github.com/zscaler/zscaler-sdk-python/pull/259) - Added the following new ZIA API Endpoints:
  - Added `GET /cyberThreatProtection/advancedThreatSettings` to retrieve the advanced threat configuration settings.
  - Added `PUT /cyberThreatProtection/advancedThreatSettings` to update the advanced threat configuration settings.
  - Added `GET /cyberThreatProtection/maliciousUrls` to retrieve the malicious URLs added to the denylist in the Advanced Threat Protection (ATP) policy
  - Added `PUT /cyberThreatProtection/maliciousUrls` to updates the malicious URLs added to the denylist in ATP policy
  - Added `GET /cyberThreatProtection/securityExceptions` to retrieves information about the security exceptions configured for the ATP policy
  - Added `PUT /cyberThreatProtection/securityExceptions` to update security exceptions for the ATP policy

#### ZIA Advanced Threat Protection Policy
[PR #259](https://github.com/zscaler/zscaler-sdk-python/pull/259) - Added the following new ZIA API Endpoints:
  - Added `GET /cyberThreatProtection/atpMalwareInspection` to retrieve the traffic inspection configurations of Malware Protection policy
  - Added `PUT /cyberThreatProtection/atpMalwareInspection` to update the traffic inspection configurations of Malware Protection policy.
  - Added `GET /cyberThreatProtection/atpMalwareProtocols` to retrieve the protocol inspection configurations of Malware Protection policy
  - Added `PUT /cyberThreatProtection/atpMalwareProtocols` to update the protocol inspection configurations of Malware Protection policy.
  - Added `GET /cyberThreatProtection/malwareSettings` to retrieve the malware protection policy configuration details
  - Added `PUT /cyberThreatProtection/malwareSettings` to update the malware protection policy configuration details.
  - Added `GET /cyberThreatProtection/malwarePolicy` to retrieve information about the security exceptions configured for the Malware Protection policy
  - Added `PUT /cyberThreatProtection/malwarePolicy` to update security exceptions for the Malware Protection policy.

#### ZIA URL & Cloud App Control Policy Settings
[PR #259](https://github.com/zscaler/zscaler-sdk-python/pull/259) - Added the following new ZIA API Endpoints:
  - Added `GET /advancedUrlFilterAndCloudAppSettings` to retrieve information about URL and Cloud App Control advanced policy settings
  - Added `PUT /advancedUrlFilterAndCloudAppSettings` to update the URL and Cloud App Control advanced policy settings

#### ZIA Authentication Settings
[PR #259](https://github.com/zscaler/zscaler-sdk-python/pull/259) - Added the following new ZIA API Endpoints:
  - Added `GET /authSettings` to retrieve the organization's default authentication settings information, including authentication profile and Kerberos authentication information.
  - Added `GET /authSettings/lite` to retrieve organization's default authentication settings information.
  - Added `PUT /authSettings` to update the organization's default authentication settings information.

#### ZIA Advanced Settings
[PR #259](https://github.com/zscaler/zscaler-sdk-python/pull/259) - Added the following new ZIA API Endpoints:
  - Added `GET /advancedSettings` to retrieve information about the advanced settings.
  - Added `PUT /advancedSettings` to update the advanced settings configuration.

#### ZIA Cloud Applications
[PR #259](https://github.com/zscaler/zscaler-sdk-python/pull/259) - Added the following new ZIA API Endpoints:
  - Added `GET /cloudApplications/policy` Retrieves a list of Predefined and User Defined Cloud Applications associated with the DLP rules, Cloud App Control rules, Advanced Settings, Bandwidth Classes, and File Type Control rules.
  - Added `GET /cloudApplications/sslPolicy` Retrieves a list of Predefined and User Defined Cloud Applications associated with the SSL Inspection rules.

#### ZIA Shadow IT Report
[PR #259](https://github.com/zscaler/zscaler-sdk-python/pull/259) - Added the following new ZIA API Endpoints:
- Added `PUT /cloudApplications/bulkUpdate` To Update application status and tag information for predefined or custom cloud applications based on the IDs specified
- Added `GET /cloudApplications/lite` Gets the list of predefined and custom cloud applications
- Added `GET /customTags` Gets the list of custom tags available to assign to cloud applications
- Added `POST /shadowIT/applications/export` Export the Shadow IT Report (in CSV format) for the cloud applications recognized by Zscaler based on their usage in your organization.
- Added `POST /shadowIT/applications/{entity}/exportCsv` Export the Shadow IT Report (in CSV format) for the list of users or known locations identified with using the cloud applications specified in the request.

#### ZIA Remote Assistance Support
[PR #259](https://github.com/zscaler/zscaler-sdk-python/pull/259) - Added the following new ZIA API Endpoints:
  - Added `GET /remoteAssistance` to retrieve information about the Remote Assistance option.
  - Added `PUT /remoteAssistance` to update information about the Remote Assistance option. Using this option, you can allow Zscaler Support to access your organization’s ZIA Admin Portal for a specified time period to troubleshoot issues.

#### ZIA Organization Details
[PR #259](https://github.com/zscaler/zscaler-sdk-python/pull/259) - Added the following new ZIA API Endpoints:
  - Added `GET /orgInformation` to retrieve detailed organization information, including headquarter location, geolocation, address, and contact details.
  - Added `GET /orgInformation/lite` to retrieve minimal organization information.
  - Added `GET /subscriptions` to retrieve information about the list of subscriptions enabled for your tenant. Subscriptions define the various features and levels of functionality that are available to your organization.

#### ZIA End User Notification
[PR #259](https://github.com/zscaler/zscaler-sdk-python/pull/259) - Added the following new ZIA API Endpoints:
  - Added `GET /eun` to retrieve information browser-based end user notification (EUN) configuration details.
  - Added `PUT /eun` to update the browser-based end user notification (EUN) configuration details.

#### ZIA Admin Audit Logs
[PR #259](https://github.com/zscaler/zscaler-sdk-python/pull/259) - Added the following new ZIA API Endpoints:
  - Added `GET /auditlogEntryReport` to retrieve the status of a request for an audit log report.
  - Added `POST /auditlogEntryReport` to create an audit log report for the specified time period and saves it as a CSV file.
  - Added `DELETE /auditlogEntryReport` to cancel the request to create an audit log report.
  - Added `GET /auditlogEntryReport/download` to download the most recently created audit log report.

#### ZIA Extranets
[PR #259](https://github.com/zscaler/zscaler-sdk-python/pull/259) - Added the following new ZIA API Endpoints:
  - Added `GET /extranet` to retrieve the list of extranets configured for the organization
  - Added `GET /extranet/lite` Retrieves the name-ID pairs of all extranets configured for an organization
  - Added `GET /extranet/{Id}` Retrieves information about an extranet based on the specified ID.
  - Added `POST /extranet` Adds a new extranet for the organization.
  - Added `PUT /extranet/{Id}` Updates an extranet based on the specified ID
  - Added `DELETE /extranet/{Id}` Deletes an extranet based on the specified ID

#### ZIA IOT Endpoint
[PR #259](https://github.com/zscaler/zscaler-sdk-python/pull/259) - Added the following new ZIA IOT API Endpoints:
  - Added `GET /iotDiscovery/deviceTypes` Retrieve the mapping between device type universally unique identifier (UUID) values and the device type names for all the device types supported by the Zscaler AI/ML.
  - Added `GET /iotDiscovery/categories` Retrieve the mapping between the device category universally unique identifier (UUID) values and the category names for all the device categories supported by the Zscaler AI/ML. The parent of device category is device type.
  - Added `GET /iotDiscovery/classifications` Retrieve the mapping between the device classification universally unique identifier (UUID) values and the classification names for all the device classifications supported by Zscaler AI/ML. The parent of device classification is device category.
  - Added `GET /iotDiscovery/deviceList` Retrieve a list of discovered devices with the following key contexts, IP address, location, ML auto-label, classification, category, and type.

#### ZIA 3rd-Party App Governance
[PR #259](https://github.com/zscaler/zscaler-sdk-python/pull/259) - Added the following new ZIA API Endpoints:
  - Added `GET /apps/app` to search the 3rd-Party App Governance App Catalog by either app ID or URL.
  - Added `POST /apps/app` to submis an app for analysis in the 3rd-Party App Governance Sandbox.
  - Added `GET /apps/search` to search for an app by name. Any app whose name contains the search term (appName) is returned.
  - Added `GET /app_views/list` to retrieve the list of custom views that you have configured in the 3rd-Party App Governance.
  - Added `GET /app_views/{appViewId}/apps` to retrieves all assets (i.e., apps) that are related to a specified argument (i.e., custom view).

### ZIA Admin Role Endpoints
[PR #259](https://github.com/zscaler/zscaler-sdk-python/pull/259) - Added the following new ZIA API Endpoints:
    - Added `GET /adminRoles/{roleId}` Retrieves the admin role based on the specified ID
    - Added `GET /adminRoles/lite` Retrieves a name and ID dictionary of all admin roles. The list only includes the name and ID for all admin roles.
    - Added `POST /adminRoles` Adds an admin role.
    - Added `PUT /adminRoles/{roleId}` Updates the admin role based on the specified ID.
    - Added `DELETE /adminRoles/{roleId}` Deletes the admin role based on the specified ID.

### ZPA Credential Pool (New)
[PR #259](https://github.com/zscaler/zscaler-sdk-python/pull/259) - Added new ZPA endpoint:
  - Added `GET /credential-pool` Gets the privileged credential pool details for the specified customer.
  - Added `GET /credential-pool/{id}` Gets the privileged credential pool details for the specified customer.
  - Added `GET /credential-pool/{id}/credential` Given Privileged credential pool id gets mapped privileged credential info
  - Added `POST /credential-pool` Adds a new privileged credential pool for the specified customer.
  - Added `PUT /credential-pool/{id}` Updates the existing credential pool for the specified customer.
  - Added `DELETE /credential-pool/{id}` Updates the existing credential pool for the specified customer.

#### ZWA - Zscaler Workflow Automation (NEW)
[PR #259](https://github.com/zscaler/zscaler-sdk-python/pull/259) - Added new ZWA endpoint:
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

### Cloud & Branch Connector - OneAPI Support
[PR #259](https://github.com/zscaler/zscaler-sdk-python/pull/259) - Cloud & Branch Connector package is now compatible with OneAPI and Legacy API framework. Please refer to README for details.
[PR #259](https://github.com/zscaler/zscaler-sdk-python/pull/259) - Cloud & Branch Connector package has been renamed from `zcon` to `ztw`

### ZTW Policy Management
[PR #259](https://github.com/zscaler/zscaler-sdk-python/pull/259) - Added the following new ZTW API Endpoints:
    - Added `GET /ecRules/ecRdr` Retrieves the list of traffic forwarding rules.
    - Added `PUT /ecRules/ecRdr/{ruleId}` Updates a traffic forwarding rule configuration based on the specified ID.
    - Added `POST /ecRules/ecRdr` Creates a new traffic forwarding rule.
    - Added `GET /ecRules/ecRdr/count` Retrieves the count of traffic forwarding rules available in the Cloud & Branch Connector Admin Portal.

### ZTW Policy Resources
[PR #259](https://github.com/zscaler/zscaler-sdk-python/pull/259) - Added the following new ZTW API Endpoints:
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

## 1.0.1 (April, 22 2025) - BREAKING CHANGES

### Notes

- Python Versions: **v3.8, v3.9, v3.10, v3.11**


#### Zscaler OneAPI Support
[PR #257](https://github.com/zscaler/zscaler-sdk-python/pull/257): Added support for [OneAPI](https://help.zscaler.com/oneapi/understanding-oneapi) Oauth2 authentication support through [Zidentity](https://help.zscaler.com/zidentity/what-zidentity).

**NOTES**
  - Starting at v1.0.0 version this SDK provides dual API client functionality and is backwards compatible with the legacy Zscaler API framework.
  - The new OneAPI framework is compatible only with the following products `ZCC/ZIA/ZPA`.
  - The following products `ZTW` - Cloud Connector and `ZDX` and Zscaler Digital Experience, authentication methods remain unnaffected.
  - The package `ZCON` (Zscaler Cloud and Branch Connector) has been renamed to `ZTW`
  - The following products `ZWA` - Zscaler Workflow Automation authentication methods remain unnaffected.

Refer to the [README](https://github.com/zscaler/zscaler-sdk-python/blob/master/README.md) page for details on client instantiation, and authentication requirements on each individual product.

**WARNING**: Attention Government customers. OneAPI and Zidentity is not currently supported for the following ZIA clouds: `zscalergov` and `zscalerten` or ZPA `GOV`, and `GOVUS`. Please refer to the Zscaler Legacy API Framework section in the [README](https://github.com/zscaler/zscaler-sdk-python/blob/master/README.md) for more information on how authenticate to these environments using the built-in Legacy API method.

[PR #257](https://github.com/zscaler/zscaler-sdk-python/pull/257): All API clients now support Config Setter object `ZCC/ZTW/ZDX/ZIA/ZPA/ZWA`

#### ZCC New Endpoints
[PR #258](https://github.com/zscaler/zscaler-sdk-python/pull/258) - Added the following new ZCC API Endpoints:
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

#### ZIA Sandbox Submission - BREAKING CHANGES
[PR #258](https://github.com/zscaler/zscaler-sdk-python/pull/258) - Authentication to Zscaler Sandbox now use the following attributes during client instantiation.
 - `sandboxToken` - Can also be sourced from the `ZSCALER_SANDBOX_TOKEN` environment variable.
 - `sandboxCloud` - Can also be sourced from the `ZSCALER_SANDBOX_CLOUD` environment variable.

**NOTE** The previous `ZIA_SANDBOX_TOKEN` has been deprecated.

#### ZIA Sandbox Rules
[PR #258](https://github.com/zscaler/zscaler-sdk-python/pull/258) - Added the following new ZIA API Endpoints:
  - Added `GET /sandboxRules` to retrieve the list of all Sandbox policy rules.
  - Added `GET /sandboxRules/{ruleId}` to retrieve the Sandbox policy rule information based on the specified ID.
  - Added `POST /sandboxRules` to add a Sandbox policy rule.
  - Added `PUT /sandboxRules/{ruleId}` to update the Sandbox policy rule configuration for the specified ID.
  - Added `DELETE /sandboxRules/{ruleId}` to delete the Sandbox policy rule based on the specified ID.

#### ZIA DNS Control Rules
[PR #258](https://github.com/zscaler/zscaler-sdk-python/pull/258) - Added the following new ZIA API Endpoints:
  - Added `GET /firewallDnsRules` to retrieve the list of all DNS Control policy rules.
  - Added `GET /firewallDnsRules/{ruleId}` to retrieve the DNS Control policy rule information based on the specified ID.
  - Added `POST /firewallDnsRules` to add a DNS Control policy rules.
  - Added `PUT /firewallDnsRules/{ruleId}` to update the DNS Control policy rule configuration for the specified ID.
  - Added `DELETE /firewallDnsRules/{ruleId}` to delete the DNS Control policy rule based on the specified ID.

#### ZIA IPS Control Rules
[PR #258](https://github.com/zscaler/zscaler-sdk-python/pull/258) - Added the following new ZIA API Endpoints:
  - Added `GET /firewallIpsRules` to retrieve the list of all IPS Control policy rules.
  - Added `GET /firewallIpsRules/{ruleId}` to retrieve the IPS Control policy rule information based on the specified ID.
  - Added `POST /firewallIpsRules` to add a IPS Control policy rule.
  - Added `PUT /firewallIpsRules/{ruleId}` to update the IPS Control policy rule configuration for the specified ID.
  - Added `DELETE /firewallIpsRules/{ruleId}` to delete the IPS Control policy rule based on the specified ID.

#### ZIA File Type Control Policy
[PR #258](https://github.com/zscaler/zscaler-sdk-python/pull/258) - Added the following new ZIA API Endpoints:
  - Added `GET /fileTypeRules` to retrieve the list of all File Type Control policy rules.
  - Added `GET /fileTypeRules/lite` to retrieve the list of all File Type Control policy rules.
  - Added `GET /fileTypeRules/{ruleId}` to retrieve the File Type Control policy rule information based on the specified ID.
  - Added `POST /fileTypeRules` to add a File Type Control policy rule.
  - Added `PUT /fileTypeRules/{ruleId}` to update the File Type Control policy rule configuration for the specified ID.
  - Added `DELETE /fileTypeRules/{ruleId}` to delete the File Type Control policy rule based on the specified ID.

#### ZIA Forwarding Control Policy - Proxy Gateways
[PR #258](https://github.com/zscaler/zscaler-sdk-python/pull/258) - Added the following new ZIA API Endpoints:
  - Added `GET /proxyGateways` to retrieve the proxy gateway information.
  - Added `GET /proxyGateways/lite` to retrieve the name and ID of the proxy.

#### ZIA Cloud Nanolog Streaming Service (NSS)
[PR #258](https://github.com/zscaler/zscaler-sdk-python/pull/258) - Added the following new ZIA API Endpoints:
  - Added `GET /nssFeeds` to retrieve the cloud NSS feeds.
  - Added `GET /nssFeeds/{feedId}` to retrieve information about cloud NSS feed based on the specified ID.
  - Added `POST /nssFeeds` to add a new cloud NSS feed.
  - Added `PUT /nssFeeds/{feedId}` to update cloud NSS feed configuration based on the specified ID.
  - Added `DELETE /nssFeeds/{feedId}` to delete cloud NSS feed configuration based on the specified ID.
  - Added `GET /nssFeeds/feedOutputDefaults` to retrieve the default cloud NSS feed output format for different log types.
  - Added `GET /nssFeeds/testConnectivity/{feedId}` to test the connectivity of cloud NSS feed based on the specified ID
  - Added `POST /nssFeeds/validateFeedFormat` to validates the cloud NSS feed format and returns the validation result

#### ZIA Advanced Threat Protection Policy
[PR #258](https://github.com/zscaler/zscaler-sdk-python/pull/258) - Added the following new ZIA API Endpoints:
  - Added `GET /cyberThreatProtection/advancedThreatSettings` to retrieve the advanced threat configuration settings.
  - Added `PUT /cyberThreatProtection/advancedThreatSettings` to update the advanced threat configuration settings.
  - Added `GET /cyberThreatProtection/maliciousUrls` to retrieve the malicious URLs added to the denylist in the Advanced Threat Protection (ATP) policy
  - Added `PUT /cyberThreatProtection/maliciousUrls` to updates the malicious URLs added to the denylist in ATP policy
  - Added `GET /cyberThreatProtection/securityExceptions` to retrieves information about the security exceptions configured for the ATP policy
  - Added `PUT /cyberThreatProtection/securityExceptions` to update security exceptions for the ATP policy

#### ZIA Advanced Threat Protection Policy
[PR #258](https://github.com/zscaler/zscaler-sdk-python/pull/258) - Added the following new ZIA API Endpoints:
  - Added `GET /cyberThreatProtection/atpMalwareInspection` to retrieve the traffic inspection configurations of Malware Protection policy
  - Added `PUT /cyberThreatProtection/atpMalwareInspection` to update the traffic inspection configurations of Malware Protection policy.
  - Added `GET /cyberThreatProtection/atpMalwareProtocols` to retrieve the protocol inspection configurations of Malware Protection policy
  - Added `PUT /cyberThreatProtection/atpMalwareProtocols` to update the protocol inspection configurations of Malware Protection policy.
  - Added `GET /cyberThreatProtection/malwareSettings` to retrieve the malware protection policy configuration details
  - Added `PUT /cyberThreatProtection/malwareSettings` to update the malware protection policy configuration details.
  - Added `GET /cyberThreatProtection/malwarePolicy` to retrieve information about the security exceptions configured for the Malware Protection policy
  - Added `PUT /cyberThreatProtection/malwarePolicy` to update security exceptions for the Malware Protection policy.

#### ZIA URL & Cloud App Control Policy Settings
[PR #258](https://github.com/zscaler/zscaler-sdk-python/pull/258) - Added the following new ZIA API Endpoints:
  - Added `GET /advancedUrlFilterAndCloudAppSettings` to retrieve information about URL and Cloud App Control advanced policy settings
  - Added `PUT /advancedUrlFilterAndCloudAppSettings` to update the URL and Cloud App Control advanced policy settings

#### ZIA Authentication Settings
[PR #258](https://github.com/zscaler/zscaler-sdk-python/pull/258) - Added the following new ZIA API Endpoints:
  - Added `GET /authSettings` to retrieve the organization's default authentication settings information, including authentication profile and Kerberos authentication information.
  - Added `GET /authSettings/lite` to retrieve organization's default authentication settings information.
  - Added `PUT /authSettings` to update the organization's default authentication settings information.

#### ZIA Advanced Settings
[PR #258](https://github.com/zscaler/zscaler-sdk-python/pull/258) - Added the following new ZIA API Endpoints:
  - Added `GET /advancedSettings` to retrieve information about the advanced settings.
  - Added `PUT /advancedSettings` to update the advanced settings configuration.

#### ZIA Cloud Applications
[PR #258](https://github.com/zscaler/zscaler-sdk-python/pull/258) - Added the following new ZIA API Endpoints:
  - Added `GET /cloudApplications/policy` Retrieves a list of Predefined and User Defined Cloud Applications associated with the DLP rules, Cloud App Control rules, Advanced Settings, Bandwidth Classes, and File Type Control rules.
  - Added `GET /cloudApplications/sslPolicy` Retrieves a list of Predefined and User Defined Cloud Applications associated with the SSL Inspection rules.

#### ZIA Shadow IT Report
[PR #258](https://github.com/zscaler/zscaler-sdk-python/pull/258) - Added the following new ZIA API Endpoints:
- Added `PUT /cloudApplications/bulkUpdate` To Update application status and tag information for predefined or custom cloud applications based on the IDs specified
- Added `GET /cloudApplications/lite` Gets the list of predefined and custom cloud applications
- Added `GET /customTags` Gets the list of custom tags available to assign to cloud applications
- Added `POST /shadowIT/applications/export` Export the Shadow IT Report (in CSV format) for the cloud applications recognized by Zscaler based on their usage in your organization.
- Added `POST /shadowIT/applications/{entity}/exportCsv` Export the Shadow IT Report (in CSV format) for the list of users or known locations identified with using the cloud applications specified in the request.

#### ZIA Remote Assistance Support
[PR #258](https://github.com/zscaler/zscaler-sdk-python/pull/258) - Added the following new ZIA API Endpoints:
  - Added `GET /remoteAssistance` to retrieve information about the Remote Assistance option.
  - Added `PUT /remoteAssistance` to update information about the Remote Assistance option. Using this option, you can allow Zscaler Support to access your organization’s ZIA Admin Portal for a specified time period to troubleshoot issues.

#### ZIA Organization Details
[PR #258](https://github.com/zscaler/zscaler-sdk-python/pull/258) - Added the following new ZIA API Endpoints:
  - Added `GET /orgInformation` to retrieve detailed organization information, including headquarter location, geolocation, address, and contact details.
  - Added `GET /orgInformation/lite` to retrieve minimal organization information.
  - Added `GET /subscriptions` to retrieve information about the list of subscriptions enabled for your tenant. Subscriptions define the various features and levels of functionality that are available to your organization.

#### ZIA End User Notification
[PR #258](https://github.com/zscaler/zscaler-sdk-python/pull/258) - Added the following new ZIA API Endpoints:
  - Added `GET /eun` to retrieve information browser-based end user notification (EUN) configuration details.
  - Added `PUT /eun` to update the browser-based end user notification (EUN) configuration details.

#### ZIA Admin Audit Logs
[PR #258](https://github.com/zscaler/zscaler-sdk-python/pull/258) - Added the following new ZIA API Endpoints:
  - Added `GET /auditlogEntryReport` to retrieve the status of a request for an audit log report.
  - Added `POST /auditlogEntryReport` to create an audit log report for the specified time period and saves it as a CSV file.
  - Added `DELETE /auditlogEntryReport` to cancel the request to create an audit log report.
  - Added `GET /auditlogEntryReport/download` to download the most recently created audit log report.

#### ZIA Extranets
[PR #258](https://github.com/zscaler/zscaler-sdk-python/pull/258) - Added the following new ZIA API Endpoints:
  - Added `GET /extranet` to retrieve the list of extranets configured for the organization
  - Added `GET /extranet/lite` Retrieves the name-ID pairs of all extranets configured for an organization
  - Added `GET /extranet/{Id}` Retrieves information about an extranet based on the specified ID.
  - Added `POST /extranet` Adds a new extranet for the organization.
  - Added `PUT /extranet/{Id}` Updates an extranet based on the specified ID
  - Added `DELETE /extranet/{Id}` Deletes an extranet based on the specified ID

#### ZIA IOT Endpoint
[PR #258](https://github.com/zscaler/zscaler-sdk-python/pull/258) - Added the following new ZIA IOT API Endpoints:
  - Added `GET /iotDiscovery/deviceTypes` Retrieve the mapping between device type universally unique identifier (UUID) values and the device type names for all the device types supported by the Zscaler AI/ML.
  - Added `GET /iotDiscovery/categories` Retrieve the mapping between the device category universally unique identifier (UUID) values and the category names for all the device categories supported by the Zscaler AI/ML. The parent of device category is device type.
  - Added `GET /iotDiscovery/classifications` Retrieve the mapping between the device classification universally unique identifier (UUID) values and the classification names for all the device classifications supported by Zscaler AI/ML. The parent of device classification is device category.
  - Added `GET /iotDiscovery/deviceList` Retrieve a list of discovered devices with the following key contexts, IP address, location, ML auto-label, classification, category, and type.

#### ZIA 3rd-Party App Governance
[PR #258](https://github.com/zscaler/zscaler-sdk-python/pull/258) - Added the following new ZIA API Endpoints:
  - Added `GET /apps/app` to search the 3rd-Party App Governance App Catalog by either app ID or URL.
  - Added `POST /apps/app` to submis an app for analysis in the 3rd-Party App Governance Sandbox.
  - Added `GET /apps/search` to search for an app by name. Any app whose name contains the search term (appName) is returned.
  - Added `GET /app_views/list` to retrieve the list of custom views that you have configured in the 3rd-Party App Governance.
  - Added `GET /app_views/{appViewId}/apps` to retrieves all assets (i.e., apps) that are related to a specified argument (i.e., custom view).

### ZIA Admin Role Endpoints
[PR #258](https://github.com/zscaler/zscaler-sdk-python/pull/258) - Added the following new ZIA API Endpoints:
    - Added `GET /adminRoles/{roleId}` Retrieves the admin role based on the specified ID
    - Added `GET /adminRoles/lite` Retrieves a name and ID dictionary of all admin roles. The list only includes the name and ID for all admin roles.
    - Added `POST /adminRoles` Adds an admin role.
    - Added `PUT /adminRoles/{roleId}` Updates the admin role based on the specified ID.
    - Added `DELETE /adminRoles/{roleId}` Deletes the admin role based on the specified ID.

### ZPA Credential Pool (New)
[PR #258](https://github.com/zscaler/zscaler-sdk-python/pull/258) - Added new ZPA endpoint:
  - Added `GET /credential-pool` Gets the privileged credential pool details for the specified customer.
  - Added `GET /credential-pool/{id}` Gets the privileged credential pool details for the specified customer.
  - Added `GET /credential-pool/{id}/credential` Given Privileged credential pool id gets mapped privileged credential info
  - Added `POST /credential-pool` Adds a new privileged credential pool for the specified customer.
  - Added `PUT /credential-pool/{id}` Updates the existing credential pool for the specified customer.
  - Added `DELETE /credential-pool/{id}` Updates the existing credential pool for the specified customer.

#### ZWA - Zscaler Workflow Automation (NEW)
[PR #258](https://github.com/zscaler/zscaler-sdk-python/pull/258) - Added new ZWA endpoint:
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

### Cloud & Branch Connector - OneAPI Support
[PR #258](https://github.com/zscaler/zscaler-sdk-python/pull/258) - Cloud & Branch Connector package is now compatible with OneAPI and Legacy API framework. Please refer to README for details.
[PR #258](https://github.com/zscaler/zscaler-sdk-python/pull/258) - Cloud & Branch Connector package has been renamed from `zcon` to `ztw`

### ZTW Policy Management
[PR #258](https://github.com/zscaler/zscaler-sdk-python/pull/258) - Added the following new ZTW API Endpoints:
    - Added `GET /ecRules/ecRdr` Retrieves the list of traffic forwarding rules.
    - Added `PUT /ecRules/ecRdr/{ruleId}` Updates a traffic forwarding rule configuration based on the specified ID.
    - Added `POST /ecRules/ecRdr` Creates a new traffic forwarding rule.
    - Added `GET /ecRules/ecRdr/count` Retrieves the count of traffic forwarding rules available in the Cloud & Branch Connector Admin Portal.

### ZTW Policy Resources
[PR #258](https://github.com/zscaler/zscaler-sdk-python/pull/258) - Added the following new ZTW API Endpoints:
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

## 1.0.1 (April, 22 2025) - BREAKING CHANGES

### Notes

- Python Versions: **v3.8, v3.9, v3.10, v3.11**


#### Zscaler OneAPI Support
[PR #258](https://github.com/zscaler/zscaler-sdk-python/pull/258): Added support for [OneAPI](https://help.zscaler.com/oneapi/understanding-oneapi) Oauth2 authentication support through [Zidentity](https://help.zscaler.com/zidentity/what-zidentity).

**NOTES**
  - Starting at v1.0.0 version this SDK provides dual API client functionality and is backwards compatible with the legacy Zscaler API framework.
  - The new OneAPI framework is compatible only with the following products `ZCC/ZIA/ZPA`.
  - The following products `ZTW` - Cloud Connector and `ZDX` and Zscaler Digital Experience, authentication methods remain unnaffected.
  - The package `ZCON` (Zscaler Cloud and Branch Connector) has been renamed to `ZTW`
  - The following products `ZWA` - Zscaler Workflow Automation authentication methods remain unnaffected.

Refer to the [README](https://github.com/zscaler/zscaler-sdk-python/blob/master/README.md) page for details on client instantiation, and authentication requirements on each individual product.

**WARNING**: Attention Government customers. OneAPI and Zidentity is not currently supported for the following ZIA clouds: `zscalergov` and `zscalerten` or ZPA `GOV`, and `GOVUS`. Please refer to the Zscaler Legacy API Framework section in the [README](https://github.com/zscaler/zscaler-sdk-python/blob/master/README.md) for more information on how authenticate to these environments using the built-in Legacy API method.

[PR #258](https://github.com/zscaler/zscaler-sdk-python/pull/258): All API clients now support Config Setter object `ZCC/ZTW/ZDX/ZIA/ZPA/ZWA`

#### ZCC New Endpoints
[PR #258](https://github.com/zscaler/zscaler-sdk-python/pull/258) - Added the following new ZCC API Endpoints:
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

#### ZIA Sandbox Submission - BREAKING CHANGES
[PR #258](https://github.com/zscaler/zscaler-sdk-python/pull/258) - Authentication to Zscaler Sandbox now use the following attributes during client instantiation.
 - `sandboxToken` - Can also be sourced from the `ZSCALER_SANDBOX_TOKEN` environment variable.
 - `sandboxCloud` - Can also be sourced from the `ZSCALER_SANDBOX_CLOUD` environment variable.

**NOTE** The previous `ZIA_SANDBOX_TOKEN` has been deprecated.

#### ZIA Sandbox Rules
[PR #258](https://github.com/zscaler/zscaler-sdk-python/pull/258) - Added the following new ZIA API Endpoints:
  - Added `GET /sandboxRules` to retrieve the list of all Sandbox policy rules.
  - Added `GET /sandboxRules/{ruleId}` to retrieve the Sandbox policy rule information based on the specified ID.
  - Added `POST /sandboxRules` to add a Sandbox policy rule.
  - Added `PUT /sandboxRules/{ruleId}` to update the Sandbox policy rule configuration for the specified ID.
  - Added `DELETE /sandboxRules/{ruleId}` to delete the Sandbox policy rule based on the specified ID.

#### ZIA DNS Control Rules
[PR #258](https://github.com/zscaler/zscaler-sdk-python/pull/258) - Added the following new ZIA API Endpoints:
  - Added `GET /firewallDnsRules` to retrieve the list of all DNS Control policy rules.
  - Added `GET /firewallDnsRules/{ruleId}` to retrieve the DNS Control policy rule information based on the specified ID.
  - Added `POST /firewallDnsRules` to add a DNS Control policy rules.
  - Added `PUT /firewallDnsRules/{ruleId}` to update the DNS Control policy rule configuration for the specified ID.
  - Added `DELETE /firewallDnsRules/{ruleId}` to delete the DNS Control policy rule based on the specified ID.

#### ZIA IPS Control Rules
[PR #258](https://github.com/zscaler/zscaler-sdk-python/pull/258) - Added the following new ZIA API Endpoints:
  - Added `GET /firewallIpsRules` to retrieve the list of all IPS Control policy rules.
  - Added `GET /firewallIpsRules/{ruleId}` to retrieve the IPS Control policy rule information based on the specified ID.
  - Added `POST /firewallIpsRules` to add a IPS Control policy rule.
  - Added `PUT /firewallIpsRules/{ruleId}` to update the IPS Control policy rule configuration for the specified ID.
  - Added `DELETE /firewallIpsRules/{ruleId}` to delete the IPS Control policy rule based on the specified ID.

#### ZIA File Type Control Policy
[PR #258](https://github.com/zscaler/zscaler-sdk-python/pull/258) - Added the following new ZIA API Endpoints:
  - Added `GET /fileTypeRules` to retrieve the list of all File Type Control policy rules.
  - Added `GET /fileTypeRules/lite` to retrieve the list of all File Type Control policy rules.
  - Added `GET /fileTypeRules/{ruleId}` to retrieve the File Type Control policy rule information based on the specified ID.
  - Added `POST /fileTypeRules` to add a File Type Control policy rule.
  - Added `PUT /fileTypeRules/{ruleId}` to update the File Type Control policy rule configuration for the specified ID.
  - Added `DELETE /fileTypeRules/{ruleId}` to delete the File Type Control policy rule based on the specified ID.

#### ZIA Forwarding Control Policy - Proxy Gateways
[PR #258](https://github.com/zscaler/zscaler-sdk-python/pull/258) - Added the following new ZIA API Endpoints:
  - Added `GET /proxyGateways` to retrieve the proxy gateway information.
  - Added `GET /proxyGateways/lite` to retrieve the name and ID of the proxy.

#### ZIA Cloud Nanolog Streaming Service (NSS)
[PR #258](https://github.com/zscaler/zscaler-sdk-python/pull/258) - Added the following new ZIA API Endpoints:
  - Added `GET /nssFeeds` to retrieve the cloud NSS feeds.
  - Added `GET /nssFeeds/{feedId}` to retrieve information about cloud NSS feed based on the specified ID.
  - Added `POST /nssFeeds` to add a new cloud NSS feed.
  - Added `PUT /nssFeeds/{feedId}` to update cloud NSS feed configuration based on the specified ID.
  - Added `DELETE /nssFeeds/{feedId}` to delete cloud NSS feed configuration based on the specified ID.
  - Added `GET /nssFeeds/feedOutputDefaults` to retrieve the default cloud NSS feed output format for different log types.
  - Added `GET /nssFeeds/testConnectivity/{feedId}` to test the connectivity of cloud NSS feed based on the specified ID
  - Added `POST /nssFeeds/validateFeedFormat` to validates the cloud NSS feed format and returns the validation result

#### ZIA Advanced Threat Protection Policy
[PR #258](https://github.com/zscaler/zscaler-sdk-python/pull/258) - Added the following new ZIA API Endpoints:
  - Added `GET /cyberThreatProtection/advancedThreatSettings` to retrieve the advanced threat configuration settings.
  - Added `PUT /cyberThreatProtection/advancedThreatSettings` to update the advanced threat configuration settings.
  - Added `GET /cyberThreatProtection/maliciousUrls` to retrieve the malicious URLs added to the denylist in the Advanced Threat Protection (ATP) policy
  - Added `PUT /cyberThreatProtection/maliciousUrls` to updates the malicious URLs added to the denylist in ATP policy
  - Added `GET /cyberThreatProtection/securityExceptions` to retrieves information about the security exceptions configured for the ATP policy
  - Added `PUT /cyberThreatProtection/securityExceptions` to update security exceptions for the ATP policy

#### ZIA Advanced Threat Protection Policy
[PR #258](https://github.com/zscaler/zscaler-sdk-python/pull/258) - Added the following new ZIA API Endpoints:
  - Added `GET /cyberThreatProtection/atpMalwareInspection` to retrieve the traffic inspection configurations of Malware Protection policy
  - Added `PUT /cyberThreatProtection/atpMalwareInspection` to update the traffic inspection configurations of Malware Protection policy.
  - Added `GET /cyberThreatProtection/atpMalwareProtocols` to retrieve the protocol inspection configurations of Malware Protection policy
  - Added `PUT /cyberThreatProtection/atpMalwareProtocols` to update the protocol inspection configurations of Malware Protection policy.
  - Added `GET /cyberThreatProtection/malwareSettings` to retrieve the malware protection policy configuration details
  - Added `PUT /cyberThreatProtection/malwareSettings` to update the malware protection policy configuration details.
  - Added `GET /cyberThreatProtection/malwarePolicy` to retrieve information about the security exceptions configured for the Malware Protection policy
  - Added `PUT /cyberThreatProtection/malwarePolicy` to update security exceptions for the Malware Protection policy.

#### ZIA URL & Cloud App Control Policy Settings
[PR #258](https://github.com/zscaler/zscaler-sdk-python/pull/258) - Added the following new ZIA API Endpoints:
  - Added `GET /advancedUrlFilterAndCloudAppSettings` to retrieve information about URL and Cloud App Control advanced policy settings
  - Added `PUT /advancedUrlFilterAndCloudAppSettings` to update the URL and Cloud App Control advanced policy settings

#### ZIA Authentication Settings
[PR #258](https://github.com/zscaler/zscaler-sdk-python/pull/258) - Added the following new ZIA API Endpoints:
  - Added `GET /authSettings` to retrieve the organization's default authentication settings information, including authentication profile and Kerberos authentication information.
  - Added `GET /authSettings/lite` to retrieve organization's default authentication settings information.
  - Added `PUT /authSettings` to update the organization's default authentication settings information.

#### ZIA Advanced Settings
[PR #258](https://github.com/zscaler/zscaler-sdk-python/pull/258) - Added the following new ZIA API Endpoints:
  - Added `GET /advancedSettings` to retrieve information about the advanced settings.
  - Added `PUT /advancedSettings` to update the advanced settings configuration.

#### ZIA Cloud Applications
[PR #258](https://github.com/zscaler/zscaler-sdk-python/pull/258) - Added the following new ZIA API Endpoints:
  - Added `GET /cloudApplications/policy` Retrieves a list of Predefined and User Defined Cloud Applications associated with the DLP rules, Cloud App Control rules, Advanced Settings, Bandwidth Classes, and File Type Control rules.
  - Added `GET /cloudApplications/sslPolicy` Retrieves a list of Predefined and User Defined Cloud Applications associated with the SSL Inspection rules.

#### ZIA Shadow IT Report
[PR #258](https://github.com/zscaler/zscaler-sdk-python/pull/258) - Added the following new ZIA API Endpoints:
- Added `PUT /cloudApplications/bulkUpdate` To Update application status and tag information for predefined or custom cloud applications based on the IDs specified
- Added `GET /cloudApplications/lite` Gets the list of predefined and custom cloud applications
- Added `GET /customTags` Gets the list of custom tags available to assign to cloud applications
- Added `POST /shadowIT/applications/export` Export the Shadow IT Report (in CSV format) for the cloud applications recognized by Zscaler based on their usage in your organization.
- Added `POST /shadowIT/applications/{entity}/exportCsv` Export the Shadow IT Report (in CSV format) for the list of users or known locations identified with using the cloud applications specified in the request.

#### ZIA Remote Assistance Support
[PR #258](https://github.com/zscaler/zscaler-sdk-python/pull/258) - Added the following new ZIA API Endpoints:
  - Added `GET /remoteAssistance` to retrieve information about the Remote Assistance option.
  - Added `PUT /remoteAssistance` to update information about the Remote Assistance option. Using this option, you can allow Zscaler Support to access your organization’s ZIA Admin Portal for a specified time period to troubleshoot issues.

#### ZIA Organization Details
[PR #258](https://github.com/zscaler/zscaler-sdk-python/pull/258) - Added the following new ZIA API Endpoints:
  - Added `GET /orgInformation` to retrieve detailed organization information, including headquarter location, geolocation, address, and contact details.
  - Added `GET /orgInformation/lite` to retrieve minimal organization information.
  - Added `GET /subscriptions` to retrieve information about the list of subscriptions enabled for your tenant. Subscriptions define the various features and levels of functionality that are available to your organization.

#### ZIA End User Notification
[PR #258](https://github.com/zscaler/zscaler-sdk-python/pull/258) - Added the following new ZIA API Endpoints:
  - Added `GET /eun` to retrieve information browser-based end user notification (EUN) configuration details.
  - Added `PUT /eun` to update the browser-based end user notification (EUN) configuration details.

#### ZIA Admin Audit Logs
[PR #258](https://github.com/zscaler/zscaler-sdk-python/pull/258) - Added the following new ZIA API Endpoints:
  - Added `GET /auditlogEntryReport` to retrieve the status of a request for an audit log report.
  - Added `POST /auditlogEntryReport` to create an audit log report for the specified time period and saves it as a CSV file.
  - Added `DELETE /auditlogEntryReport` to cancel the request to create an audit log report.
  - Added `GET /auditlogEntryReport/download` to download the most recently created audit log report.

#### ZIA Extranets
[PR #258](https://github.com/zscaler/zscaler-sdk-python/pull/258) - Added the following new ZIA API Endpoints:
  - Added `GET /extranet` to retrieve the list of extranets configured for the organization
  - Added `GET /extranet/lite` Retrieves the name-ID pairs of all extranets configured for an organization
  - Added `GET /extranet/{Id}` Retrieves information about an extranet based on the specified ID.
  - Added `POST /extranet` Adds a new extranet for the organization.
  - Added `PUT /extranet/{Id}` Updates an extranet based on the specified ID
  - Added `DELETE /extranet/{Id}` Deletes an extranet based on the specified ID

#### ZIA IOT Endpoint
[PR #258](https://github.com/zscaler/zscaler-sdk-python/pull/258) - Added the following new ZIA IOT API Endpoints:
  - Added `GET /iotDiscovery/deviceTypes` Retrieve the mapping between device type universally unique identifier (UUID) values and the device type names for all the device types supported by the Zscaler AI/ML.
  - Added `GET /iotDiscovery/categories` Retrieve the mapping between the device category universally unique identifier (UUID) values and the category names for all the device categories supported by the Zscaler AI/ML. The parent of device category is device type.
  - Added `GET /iotDiscovery/classifications` Retrieve the mapping between the device classification universally unique identifier (UUID) values and the classification names for all the device classifications supported by Zscaler AI/ML. The parent of device classification is device category.
  - Added `GET /iotDiscovery/deviceList` Retrieve a list of discovered devices with the following key contexts, IP address, location, ML auto-label, classification, category, and type.

#### ZIA 3rd-Party App Governance
[PR #258](https://github.com/zscaler/zscaler-sdk-python/pull/258) - Added the following new ZIA API Endpoints:
  - Added `GET /apps/app` to search the 3rd-Party App Governance App Catalog by either app ID or URL.
  - Added `POST /apps/app` to submis an app for analysis in the 3rd-Party App Governance Sandbox.
  - Added `GET /apps/search` to search for an app by name. Any app whose name contains the search term (appName) is returned.
  - Added `GET /app_views/list` to retrieve the list of custom views that you have configured in the 3rd-Party App Governance.
  - Added `GET /app_views/{appViewId}/apps` to retrieves all assets (i.e., apps) that are related to a specified argument (i.e., custom view).

### ZIA Admin Role Endpoints
[PR #258](https://github.com/zscaler/zscaler-sdk-python/pull/258) - Added the following new ZIA API Endpoints:
    - Added `GET /adminRoles/{roleId}` Retrieves the admin role based on the specified ID
    - Added `GET /adminRoles/lite` Retrieves a name and ID dictionary of all admin roles. The list only includes the name and ID for all admin roles.
    - Added `POST /adminRoles` Adds an admin role.
    - Added `PUT /adminRoles/{roleId}` Updates the admin role based on the specified ID.
    - Added `DELETE /adminRoles/{roleId}` Deletes the admin role based on the specified ID.

### ZPA Credential Pool (New)
[PR #258](https://github.com/zscaler/zscaler-sdk-python/pull/258) - Added new ZPA endpoint:
  - Added `GET /credential-pool` Gets the privileged credential pool details for the specified customer.
  - Added `GET /credential-pool/{id}` Gets the privileged credential pool details for the specified customer.
  - Added `GET /credential-pool/{id}/credential` Given Privileged credential pool id gets mapped privileged credential info
  - Added `POST /credential-pool` Adds a new privileged credential pool for the specified customer.
  - Added `PUT /credential-pool/{id}` Updates the existing credential pool for the specified customer.
  - Added `DELETE /credential-pool/{id}` Updates the existing credential pool for the specified customer.

#### ZWA - Zscaler Workflow Automation (NEW)
[PR #258](https://github.com/zscaler/zscaler-sdk-python/pull/258) - Added new ZWA endpoint:
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

### Cloud & Branch Connector - OneAPI Support
[PR #258](https://github.com/zscaler/zscaler-sdk-python/pull/258) - Cloud & Branch Connector package is now compatible with OneAPI and Legacy API framework. Please refer to README for details.
[PR #258](https://github.com/zscaler/zscaler-sdk-python/pull/258) - Cloud & Branch Connector package has been renamed from `zcon` to `ztw`

### ZTW Policy Management
[PR #258](https://github.com/zscaler/zscaler-sdk-python/pull/258) - Added the following new ZTW API Endpoints:
    - Added `GET /ecRules/ecRdr` Retrieves the list of traffic forwarding rules.
    - Added `PUT /ecRules/ecRdr/{ruleId}` Updates a traffic forwarding rule configuration based on the specified ID.
    - Added `POST /ecRules/ecRdr` Creates a new traffic forwarding rule.
    - Added `GET /ecRules/ecRdr/count` Retrieves the count of traffic forwarding rules available in the Cloud & Branch Connector Admin Portal.

### ZTW Policy Resources
[PR #258](https://github.com/zscaler/zscaler-sdk-python/pull/258) - Added the following new ZTW API Endpoints:
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

## 1.0.1 (April, 22 2025) - BREAKING CHANGES

### Notes

- Python Versions: **v3.8, v3.9, v3.10, v3.11**


#### Zscaler OneAPI Support
[PR #257](https://github.com/zscaler/zscaler-sdk-python/pull/257): Added support for [OneAPI](https://help.zscaler.com/oneapi/understanding-oneapi) Oauth2 authentication support through [Zidentity](https://help.zscaler.com/zidentity/what-zidentity).

**NOTES**
  - Starting at v1.0.0 version this SDK provides dual API client functionality and is backwards compatible with the legacy Zscaler API framework.
  - The new OneAPI framework is compatible only with the following products `ZCC/ZIA/ZPA`.
  - The following products `ZTW` - Cloud Connector and `ZDX` and Zscaler Digital Experience, authentication methods remain unnaffected.
  - The package `ZCON` (Zscaler Cloud and Branch Connector) has been renamed to `ZTW`
  - The following products `ZWA` - Zscaler Workflow Automation authentication methods remain unnaffected.

Refer to the [README](https://github.com/zscaler/zscaler-sdk-python/blob/master/README.md) page for details on client instantiation, and authentication requirements on each individual product.

**WARNING**: Attention Government customers. OneAPI and Zidentity is not currently supported for the following ZIA clouds: `zscalergov` and `zscalerten` or ZPA `GOV`, and `GOVUS`. Please refer to the Zscaler Legacy API Framework section in the [README](https://github.com/zscaler/zscaler-sdk-python/blob/master/README.md) for more information on how authenticate to these environments using the built-in Legacy API method.

[PR #257](https://github.com/zscaler/zscaler-sdk-python/pull/257): All API clients now support Config Setter object `ZCC/ZTW/ZDX/ZIA/ZPA/ZWA`

#### ZCC New Endpoints
[PR #256](https://github.com/zscaler/zscaler-sdk-python/pull/256) - Added the following new ZCC API Endpoints:
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

#### ZIA Sandbox Submission - BREAKING CHANGES
[PR #256](https://github.com/zscaler/zscaler-sdk-python/pull/256) - Authentication to Zscaler Sandbox now use the following attributes during client instantiation.
 - `sandboxToken` - Can also be sourced from the `ZSCALER_SANDBOX_TOKEN` environment variable.
 - `sandboxCloud` - Can also be sourced from the `ZSCALER_SANDBOX_CLOUD` environment variable.

**NOTE** The previous `ZIA_SANDBOX_TOKEN` has been deprecated.

#### ZIA Sandbox Rules
[PR #256](https://github.com/zscaler/zscaler-sdk-python/pull/256) - Added the following new ZIA API Endpoints:
  - Added `GET /sandboxRules` to retrieve the list of all Sandbox policy rules.
  - Added `GET /sandboxRules/{ruleId}` to retrieve the Sandbox policy rule information based on the specified ID.
  - Added `POST /sandboxRules` to add a Sandbox policy rule.
  - Added `PUT /sandboxRules/{ruleId}` to update the Sandbox policy rule configuration for the specified ID.
  - Added `DELETE /sandboxRules/{ruleId}` to delete the Sandbox policy rule based on the specified ID.

#### ZIA DNS Control Rules
[PR #256](https://github.com/zscaler/zscaler-sdk-python/pull/256) - Added the following new ZIA API Endpoints:
  - Added `GET /firewallDnsRules` to retrieve the list of all DNS Control policy rules.
  - Added `GET /firewallDnsRules/{ruleId}` to retrieve the DNS Control policy rule information based on the specified ID.
  - Added `POST /firewallDnsRules` to add a DNS Control policy rules.
  - Added `PUT /firewallDnsRules/{ruleId}` to update the DNS Control policy rule configuration for the specified ID.
  - Added `DELETE /firewallDnsRules/{ruleId}` to delete the DNS Control policy rule based on the specified ID.

#### ZIA IPS Control Rules
[PR #256](https://github.com/zscaler/zscaler-sdk-python/pull/256) - Added the following new ZIA API Endpoints:
  - Added `GET /firewallIpsRules` to retrieve the list of all IPS Control policy rules.
  - Added `GET /firewallIpsRules/{ruleId}` to retrieve the IPS Control policy rule information based on the specified ID.
  - Added `POST /firewallIpsRules` to add a IPS Control policy rule.
  - Added `PUT /firewallIpsRules/{ruleId}` to update the IPS Control policy rule configuration for the specified ID.
  - Added `DELETE /firewallIpsRules/{ruleId}` to delete the IPS Control policy rule based on the specified ID.

#### ZIA File Type Control Policy
[PR #256](https://github.com/zscaler/zscaler-sdk-python/pull/256) - Added the following new ZIA API Endpoints:
  - Added `GET /fileTypeRules` to retrieve the list of all File Type Control policy rules.
  - Added `GET /fileTypeRules/lite` to retrieve the list of all File Type Control policy rules.
  - Added `GET /fileTypeRules/{ruleId}` to retrieve the File Type Control policy rule information based on the specified ID.
  - Added `POST /fileTypeRules` to add a File Type Control policy rule.
  - Added `PUT /fileTypeRules/{ruleId}` to update the File Type Control policy rule configuration for the specified ID.
  - Added `DELETE /fileTypeRules/{ruleId}` to delete the File Type Control policy rule based on the specified ID.

#### ZIA Forwarding Control Policy - Proxy Gateways
[PR #256](https://github.com/zscaler/zscaler-sdk-python/pull/256) - Added the following new ZIA API Endpoints:
  - Added `GET /proxyGateways` to retrieve the proxy gateway information.
  - Added `GET /proxyGateways/lite` to retrieve the name and ID of the proxy.

#### ZIA Cloud Nanolog Streaming Service (NSS)
[PR #256](https://github.com/zscaler/zscaler-sdk-python/pull/256) - Added the following new ZIA API Endpoints:
  - Added `GET /nssFeeds` to retrieve the cloud NSS feeds.
  - Added `GET /nssFeeds/{feedId}` to retrieve information about cloud NSS feed based on the specified ID.
  - Added `POST /nssFeeds` to add a new cloud NSS feed.
  - Added `PUT /nssFeeds/{feedId}` to update cloud NSS feed configuration based on the specified ID.
  - Added `DELETE /nssFeeds/{feedId}` to delete cloud NSS feed configuration based on the specified ID.
  - Added `GET /nssFeeds/feedOutputDefaults` to retrieve the default cloud NSS feed output format for different log types.
  - Added `GET /nssFeeds/testConnectivity/{feedId}` to test the connectivity of cloud NSS feed based on the specified ID
  - Added `POST /nssFeeds/validateFeedFormat` to validates the cloud NSS feed format and returns the validation result

#### ZIA Advanced Threat Protection Policy
[PR #256](https://github.com/zscaler/zscaler-sdk-python/pull/256) - Added the following new ZIA API Endpoints:
  - Added `GET /cyberThreatProtection/advancedThreatSettings` to retrieve the advanced threat configuration settings.
  - Added `PUT /cyberThreatProtection/advancedThreatSettings` to update the advanced threat configuration settings.
  - Added `GET /cyberThreatProtection/maliciousUrls` to retrieve the malicious URLs added to the denylist in the Advanced Threat Protection (ATP) policy
  - Added `PUT /cyberThreatProtection/maliciousUrls` to updates the malicious URLs added to the denylist in ATP policy
  - Added `GET /cyberThreatProtection/securityExceptions` to retrieves information about the security exceptions configured for the ATP policy
  - Added `PUT /cyberThreatProtection/securityExceptions` to update security exceptions for the ATP policy

#### ZIA Advanced Threat Protection Policy
[PR #256](https://github.com/zscaler/zscaler-sdk-python/pull/256) - Added the following new ZIA API Endpoints:
  - Added `GET /cyberThreatProtection/atpMalwareInspection` to retrieve the traffic inspection configurations of Malware Protection policy
  - Added `PUT /cyberThreatProtection/atpMalwareInspection` to update the traffic inspection configurations of Malware Protection policy.
  - Added `GET /cyberThreatProtection/atpMalwareProtocols` to retrieve the protocol inspection configurations of Malware Protection policy
  - Added `PUT /cyberThreatProtection/atpMalwareProtocols` to update the protocol inspection configurations of Malware Protection policy.
  - Added `GET /cyberThreatProtection/malwareSettings` to retrieve the malware protection policy configuration details
  - Added `PUT /cyberThreatProtection/malwareSettings` to update the malware protection policy configuration details.
  - Added `GET /cyberThreatProtection/malwarePolicy` to retrieve information about the security exceptions configured for the Malware Protection policy
  - Added `PUT /cyberThreatProtection/malwarePolicy` to update security exceptions for the Malware Protection policy.

#### ZIA URL & Cloud App Control Policy Settings
[PR #256](https://github.com/zscaler/zscaler-sdk-python/pull/256) - Added the following new ZIA API Endpoints:
  - Added `GET /advancedUrlFilterAndCloudAppSettings` to retrieve information about URL and Cloud App Control advanced policy settings
  - Added `PUT /advancedUrlFilterAndCloudAppSettings` to update the URL and Cloud App Control advanced policy settings

#### ZIA Authentication Settings
[PR #256](https://github.com/zscaler/zscaler-sdk-python/pull/256) - Added the following new ZIA API Endpoints:
  - Added `GET /authSettings` to retrieve the organization's default authentication settings information, including authentication profile and Kerberos authentication information.
  - Added `GET /authSettings/lite` to retrieve organization's default authentication settings information.
  - Added `PUT /authSettings` to update the organization's default authentication settings information.

#### ZIA Advanced Settings
[PR #256](https://github.com/zscaler/zscaler-sdk-python/pull/256) - Added the following new ZIA API Endpoints:
  - Added `GET /advancedSettings` to retrieve information about the advanced settings.
  - Added `PUT /advancedSettings` to update the advanced settings configuration.

#### ZIA Cloud Applications
[PR #256](https://github.com/zscaler/zscaler-sdk-python/pull/256) - Added the following new ZIA API Endpoints:
  - Added `GET /cloudApplications/policy` Retrieves a list of Predefined and User Defined Cloud Applications associated with the DLP rules, Cloud App Control rules, Advanced Settings, Bandwidth Classes, and File Type Control rules.
  - Added `GET /cloudApplications/sslPolicy` Retrieves a list of Predefined and User Defined Cloud Applications associated with the SSL Inspection rules.

#### ZIA Shadow IT Report
[PR #256](https://github.com/zscaler/zscaler-sdk-python/pull/256) - Added the following new ZIA API Endpoints:
- Added `PUT /cloudApplications/bulkUpdate` To Update application status and tag information for predefined or custom cloud applications based on the IDs specified
- Added `GET /cloudApplications/lite` Gets the list of predefined and custom cloud applications
- Added `GET /customTags` Gets the list of custom tags available to assign to cloud applications
- Added `POST /shadowIT/applications/export` Export the Shadow IT Report (in CSV format) for the cloud applications recognized by Zscaler based on their usage in your organization.
- Added `POST /shadowIT/applications/{entity}/exportCsv` Export the Shadow IT Report (in CSV format) for the list of users or known locations identified with using the cloud applications specified in the request.

#### ZIA Remote Assistance Support
[PR #256](https://github.com/zscaler/zscaler-sdk-python/pull/256) - Added the following new ZIA API Endpoints:
  - Added `GET /remoteAssistance` to retrieve information about the Remote Assistance option.
  - Added `PUT /remoteAssistance` to update information about the Remote Assistance option. Using this option, you can allow Zscaler Support to access your organization’s ZIA Admin Portal for a specified time period to troubleshoot issues.

#### ZIA Organization Details
[PR #256](https://github.com/zscaler/zscaler-sdk-python/pull/256) - Added the following new ZIA API Endpoints:
  - Added `GET /orgInformation` to retrieve detailed organization information, including headquarter location, geolocation, address, and contact details.
  - Added `GET /orgInformation/lite` to retrieve minimal organization information.
  - Added `GET /subscriptions` to retrieve information about the list of subscriptions enabled for your tenant. Subscriptions define the various features and levels of functionality that are available to your organization.

#### ZIA End User Notification
[PR #256](https://github.com/zscaler/zscaler-sdk-python/pull/256) - Added the following new ZIA API Endpoints:
  - Added `GET /eun` to retrieve information browser-based end user notification (EUN) configuration details.
  - Added `PUT /eun` to update the browser-based end user notification (EUN) configuration details.

#### ZIA Admin Audit Logs
[PR #256](https://github.com/zscaler/zscaler-sdk-python/pull/256) - Added the following new ZIA API Endpoints:
  - Added `GET /auditlogEntryReport` to retrieve the status of a request for an audit log report.
  - Added `POST /auditlogEntryReport` to create an audit log report for the specified time period and saves it as a CSV file.
  - Added `DELETE /auditlogEntryReport` to cancel the request to create an audit log report.
  - Added `GET /auditlogEntryReport/download` to download the most recently created audit log report.

#### ZIA Extranets
[PR #256](https://github.com/zscaler/zscaler-sdk-python/pull/256) - Added the following new ZIA API Endpoints:
  - Added `GET /extranet` to retrieve the list of extranets configured for the organization
  - Added `GET /extranet/lite` Retrieves the name-ID pairs of all extranets configured for an organization
  - Added `GET /extranet/{Id}` Retrieves information about an extranet based on the specified ID.
  - Added `POST /extranet` Adds a new extranet for the organization.
  - Added `PUT /extranet/{Id}` Updates an extranet based on the specified ID
  - Added `DELETE /extranet/{Id}` Deletes an extranet based on the specified ID

#### ZIA IOT Endpoint
[PR #256](https://github.com/zscaler/zscaler-sdk-python/pull/256) - Added the following new ZIA IOT API Endpoints:
  - Added `GET /iotDiscovery/deviceTypes` Retrieve the mapping between device type universally unique identifier (UUID) values and the device type names for all the device types supported by the Zscaler AI/ML.
  - Added `GET /iotDiscovery/categories` Retrieve the mapping between the device category universally unique identifier (UUID) values and the category names for all the device categories supported by the Zscaler AI/ML. The parent of device category is device type.
  - Added `GET /iotDiscovery/classifications` Retrieve the mapping between the device classification universally unique identifier (UUID) values and the classification names for all the device classifications supported by Zscaler AI/ML. The parent of device classification is device category.
  - Added `GET /iotDiscovery/deviceList` Retrieve a list of discovered devices with the following key contexts, IP address, location, ML auto-label, classification, category, and type.

#### ZIA 3rd-Party App Governance
[PR #256](https://github.com/zscaler/zscaler-sdk-python/pull/256) - Added the following new ZIA API Endpoints:
  - Added `GET /apps/app` to search the 3rd-Party App Governance App Catalog by either app ID or URL.
  - Added `POST /apps/app` to submis an app for analysis in the 3rd-Party App Governance Sandbox.
  - Added `GET /apps/search` to search for an app by name. Any app whose name contains the search term (appName) is returned.
  - Added `GET /app_views/list` to retrieve the list of custom views that you have configured in the 3rd-Party App Governance.
  - Added `GET /app_views/{appViewId}/apps` to retrieves all assets (i.e., apps) that are related to a specified argument (i.e., custom view).

### ZIA Admin Role Endpoints
[PR #256](https://github.com/zscaler/zscaler-sdk-python/pull/256) - Added the following new ZIA API Endpoints:
    - Added `GET /adminRoles/{roleId}` Retrieves the admin role based on the specified ID
    - Added `GET /adminRoles/lite` Retrieves a name and ID dictionary of all admin roles. The list only includes the name and ID for all admin roles.
    - Added `POST /adminRoles` Adds an admin role.
    - Added `PUT /adminRoles/{roleId}` Updates the admin role based on the specified ID.
    - Added `DELETE /adminRoles/{roleId}` Deletes the admin role based on the specified ID.

### ZPA Credential Pool (New)
[PR #256](https://github.com/zscaler/zscaler-sdk-python/pull/256) - Added new ZPA endpoint:
  - Added `GET /credential-pool` Gets the privileged credential pool details for the specified customer.
  - Added `GET /credential-pool/{id}` Gets the privileged credential pool details for the specified customer.
  - Added `GET /credential-pool/{id}/credential` Given Privileged credential pool id gets mapped privileged credential info
  - Added `POST /credential-pool` Adds a new privileged credential pool for the specified customer.
  - Added `PUT /credential-pool/{id}` Updates the existing credential pool for the specified customer.
  - Added `DELETE /credential-pool/{id}` Updates the existing credential pool for the specified customer.

#### ZWA - Zscaler Workflow Automation (NEW)
[PR #256](https://github.com/zscaler/zscaler-sdk-python/pull/256) - Added new ZWA endpoint:
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

### Cloud & Branch Connector - OneAPI Support
[PR #256](https://github.com/zscaler/zscaler-sdk-python/pull/256) - Cloud & Branch Connector package is now compatible with OneAPI and Legacy API framework. Please refer to README for details.
[PR #256](https://github.com/zscaler/zscaler-sdk-python/pull/256) - Cloud & Branch Connector package has been renamed from `zcon` to `ztw`

### ZTW Policy Management
[PR #256](https://github.com/zscaler/zscaler-sdk-python/pull/256) - Added the following new ZTW API Endpoints:
    - Added `GET /ecRules/ecRdr` Retrieves the list of traffic forwarding rules.
    - Added `PUT /ecRules/ecRdr/{ruleId}` Updates a traffic forwarding rule configuration based on the specified ID.
    - Added `POST /ecRules/ecRdr` Creates a new traffic forwarding rule.
    - Added `GET /ecRules/ecRdr/count` Retrieves the count of traffic forwarding rules available in the Cloud & Branch Connector Admin Portal.

### ZTW Policy Resources
[PR #256](https://github.com/zscaler/zscaler-sdk-python/pull/256) - Added the following new ZTW API Endpoints:
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

## 1.0.1 (April, 22 2025) - BREAKING CHANGES

### Notes

- Python Versions: **v3.8, v3.9, v3.10, v3.11**


#### Zscaler OneAPI Support
[PR #256](https://github.com/zscaler/zscaler-sdk-python/pull/256): Added support for [OneAPI](https://help.zscaler.com/oneapi/understanding-oneapi) Oauth2 authentication support through [Zidentity](https://help.zscaler.com/zidentity/what-zidentity).

**NOTES**
  - Starting at v1.0.0 version this SDK provides dual API client functionality and is backwards compatible with the legacy Zscaler API framework.
  - The new OneAPI framework is compatible only with the following products `ZCC/ZIA/ZPA`.
  - The following products `ZTW` - Cloud Connector and `ZDX` and Zscaler Digital Experience, authentication methods remain unnaffected.
  - The package `ZCON` (Zscaler Cloud and Branch Connector) has been renamed to `ZTW`
  - The following products `ZWA` - Zscaler Workflow Automation authentication methods remain unnaffected.

Refer to the [README](https://github.com/zscaler/zscaler-sdk-python/blob/master/README.md) page for details on client instantiation, and authentication requirements on each individual product.

**WARNING**: Attention Government customers. OneAPI and Zidentity is not currently supported for the following ZIA clouds: `zscalergov` and `zscalerten` or ZPA `GOV`, and `GOVUS`. Please refer to the Zscaler Legacy API Framework section in the [README](https://github.com/zscaler/zscaler-sdk-python/blob/master/README.md) for more information on how authenticate to these environments using the built-in Legacy API method.

[PR #256](https://github.com/zscaler/zscaler-sdk-python/pull/256): All API clients now support Config Setter object `ZCC/ZTW/ZDX/ZIA/ZPA/ZWA`

#### ZCC New Endpoints
[PR #256](https://github.com/zscaler/zscaler-sdk-python/pull/256) - Added the following new ZCC API Endpoints:
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

#### ZIA Sandbox Submission - BREAKING CHANGES
[PR #256](https://github.com/zscaler/zscaler-sdk-python/pull/256) - Authentication to Zscaler Sandbox now use the following attributes during client instantiation.
 - `sandboxToken` - Can also be sourced from the `ZSCALER_SANDBOX_TOKEN` environment variable.
 - `sandboxCloud` - Can also be sourced from the `ZSCALER_SANDBOX_CLOUD` environment variable.

**NOTE** The previous `ZIA_SANDBOX_TOKEN` has been deprecated.

#### ZIA Sandbox Rules
[PR #256](https://github.com/zscaler/zscaler-sdk-python/pull/256) - Added the following new ZIA API Endpoints:
  - Added `GET /sandboxRules` to retrieve the list of all Sandbox policy rules.
  - Added `GET /sandboxRules/{ruleId}` to retrieve the Sandbox policy rule information based on the specified ID.
  - Added `POST /sandboxRules` to add a Sandbox policy rule.
  - Added `PUT /sandboxRules/{ruleId}` to update the Sandbox policy rule configuration for the specified ID.
  - Added `DELETE /sandboxRules/{ruleId}` to delete the Sandbox policy rule based on the specified ID.

#### ZIA DNS Control Rules
[PR #256](https://github.com/zscaler/zscaler-sdk-python/pull/256) - Added the following new ZIA API Endpoints:
  - Added `GET /firewallDnsRules` to retrieve the list of all DNS Control policy rules.
  - Added `GET /firewallDnsRules/{ruleId}` to retrieve the DNS Control policy rule information based on the specified ID.
  - Added `POST /firewallDnsRules` to add a DNS Control policy rules.
  - Added `PUT /firewallDnsRules/{ruleId}` to update the DNS Control policy rule configuration for the specified ID.
  - Added `DELETE /firewallDnsRules/{ruleId}` to delete the DNS Control policy rule based on the specified ID.

#### ZIA IPS Control Rules
[PR #256](https://github.com/zscaler/zscaler-sdk-python/pull/256) - Added the following new ZIA API Endpoints:
  - Added `GET /firewallIpsRules` to retrieve the list of all IPS Control policy rules.
  - Added `GET /firewallIpsRules/{ruleId}` to retrieve the IPS Control policy rule information based on the specified ID.
  - Added `POST /firewallIpsRules` to add a IPS Control policy rule.
  - Added `PUT /firewallIpsRules/{ruleId}` to update the IPS Control policy rule configuration for the specified ID.
  - Added `DELETE /firewallIpsRules/{ruleId}` to delete the IPS Control policy rule based on the specified ID.

#### ZIA File Type Control Policy
[PR #256](https://github.com/zscaler/zscaler-sdk-python/pull/256) - Added the following new ZIA API Endpoints:
  - Added `GET /fileTypeRules` to retrieve the list of all File Type Control policy rules.
  - Added `GET /fileTypeRules/lite` to retrieve the list of all File Type Control policy rules.
  - Added `GET /fileTypeRules/{ruleId}` to retrieve the File Type Control policy rule information based on the specified ID.
  - Added `POST /fileTypeRules` to add a File Type Control policy rule.
  - Added `PUT /fileTypeRules/{ruleId}` to update the File Type Control policy rule configuration for the specified ID.
  - Added `DELETE /fileTypeRules/{ruleId}` to delete the File Type Control policy rule based on the specified ID.

#### ZIA Forwarding Control Policy - Proxy Gateways
[PR #256](https://github.com/zscaler/zscaler-sdk-python/pull/256) - Added the following new ZIA API Endpoints:
  - Added `GET /proxyGateways` to retrieve the proxy gateway information.
  - Added `GET /proxyGateways/lite` to retrieve the name and ID of the proxy.

#### ZIA Cloud Nanolog Streaming Service (NSS)
[PR #256](https://github.com/zscaler/zscaler-sdk-python/pull/256) - Added the following new ZIA API Endpoints:
  - Added `GET /nssFeeds` to retrieve the cloud NSS feeds.
  - Added `GET /nssFeeds/{feedId}` to retrieve information about cloud NSS feed based on the specified ID.
  - Added `POST /nssFeeds` to add a new cloud NSS feed.
  - Added `PUT /nssFeeds/{feedId}` to update cloud NSS feed configuration based on the specified ID.
  - Added `DELETE /nssFeeds/{feedId}` to delete cloud NSS feed configuration based on the specified ID.
  - Added `GET /nssFeeds/feedOutputDefaults` to retrieve the default cloud NSS feed output format for different log types.
  - Added `GET /nssFeeds/testConnectivity/{feedId}` to test the connectivity of cloud NSS feed based on the specified ID
  - Added `POST /nssFeeds/validateFeedFormat` to validates the cloud NSS feed format and returns the validation result

#### ZIA Advanced Threat Protection Policy
[PR #256](https://github.com/zscaler/zscaler-sdk-python/pull/256) - Added the following new ZIA API Endpoints:
  - Added `GET /cyberThreatProtection/advancedThreatSettings` to retrieve the advanced threat configuration settings.
  - Added `PUT /cyberThreatProtection/advancedThreatSettings` to update the advanced threat configuration settings.
  - Added `GET /cyberThreatProtection/maliciousUrls` to retrieve the malicious URLs added to the denylist in the Advanced Threat Protection (ATP) policy
  - Added `PUT /cyberThreatProtection/maliciousUrls` to updates the malicious URLs added to the denylist in ATP policy
  - Added `GET /cyberThreatProtection/securityExceptions` to retrieves information about the security exceptions configured for the ATP policy
  - Added `PUT /cyberThreatProtection/securityExceptions` to update security exceptions for the ATP policy

#### ZIA Advanced Threat Protection Policy
[PR #256](https://github.com/zscaler/zscaler-sdk-python/pull/256) - Added the following new ZIA API Endpoints:
  - Added `GET /cyberThreatProtection/atpMalwareInspection` to retrieve the traffic inspection configurations of Malware Protection policy
  - Added `PUT /cyberThreatProtection/atpMalwareInspection` to update the traffic inspection configurations of Malware Protection policy.
  - Added `GET /cyberThreatProtection/atpMalwareProtocols` to retrieve the protocol inspection configurations of Malware Protection policy
  - Added `PUT /cyberThreatProtection/atpMalwareProtocols` to update the protocol inspection configurations of Malware Protection policy.
  - Added `GET /cyberThreatProtection/malwareSettings` to retrieve the malware protection policy configuration details
  - Added `PUT /cyberThreatProtection/malwareSettings` to update the malware protection policy configuration details.
  - Added `GET /cyberThreatProtection/malwarePolicy` to retrieve information about the security exceptions configured for the Malware Protection policy
  - Added `PUT /cyberThreatProtection/malwarePolicy` to update security exceptions for the Malware Protection policy.

#### ZIA URL & Cloud App Control Policy Settings
[PR #256](https://github.com/zscaler/zscaler-sdk-python/pull/256) - Added the following new ZIA API Endpoints:
  - Added `GET /advancedUrlFilterAndCloudAppSettings` to retrieve information about URL and Cloud App Control advanced policy settings
  - Added `PUT /advancedUrlFilterAndCloudAppSettings` to update the URL and Cloud App Control advanced policy settings

#### ZIA Authentication Settings
[PR #256](https://github.com/zscaler/zscaler-sdk-python/pull/256) - Added the following new ZIA API Endpoints:
  - Added `GET /authSettings` to retrieve the organization's default authentication settings information, including authentication profile and Kerberos authentication information.
  - Added `GET /authSettings/lite` to retrieve organization's default authentication settings information.
  - Added `PUT /authSettings` to update the organization's default authentication settings information.

#### ZIA Advanced Settings
[PR #256](https://github.com/zscaler/zscaler-sdk-python/pull/256) - Added the following new ZIA API Endpoints:
  - Added `GET /advancedSettings` to retrieve information about the advanced settings.
  - Added `PUT /advancedSettings` to update the advanced settings configuration.

#### ZIA Cloud Applications
[PR #256](https://github.com/zscaler/zscaler-sdk-python/pull/256) - Added the following new ZIA API Endpoints:
  - Added `GET /cloudApplications/policy` Retrieves a list of Predefined and User Defined Cloud Applications associated with the DLP rules, Cloud App Control rules, Advanced Settings, Bandwidth Classes, and File Type Control rules.
  - Added `GET /cloudApplications/sslPolicy` Retrieves a list of Predefined and User Defined Cloud Applications associated with the SSL Inspection rules.

#### ZIA Shadow IT Report
[PR #256](https://github.com/zscaler/zscaler-sdk-python/pull/256) - Added the following new ZIA API Endpoints:
- Added `PUT /cloudApplications/bulkUpdate` To Update application status and tag information for predefined or custom cloud applications based on the IDs specified
- Added `GET /cloudApplications/lite` Gets the list of predefined and custom cloud applications
- Added `GET /customTags` Gets the list of custom tags available to assign to cloud applications
- Added `POST /shadowIT/applications/export` Export the Shadow IT Report (in CSV format) for the cloud applications recognized by Zscaler based on their usage in your organization.
- Added `POST /shadowIT/applications/{entity}/exportCsv` Export the Shadow IT Report (in CSV format) for the list of users or known locations identified with using the cloud applications specified in the request.

#### ZIA Remote Assistance Support
[PR #256](https://github.com/zscaler/zscaler-sdk-python/pull/256) - Added the following new ZIA API Endpoints:
  - Added `GET /remoteAssistance` to retrieve information about the Remote Assistance option.
  - Added `PUT /remoteAssistance` to update information about the Remote Assistance option. Using this option, you can allow Zscaler Support to access your organization’s ZIA Admin Portal for a specified time period to troubleshoot issues.

#### ZIA Organization Details
[PR #256](https://github.com/zscaler/zscaler-sdk-python/pull/256) - Added the following new ZIA API Endpoints:
  - Added `GET /orgInformation` to retrieve detailed organization information, including headquarter location, geolocation, address, and contact details.
  - Added `GET /orgInformation/lite` to retrieve minimal organization information.
  - Added `GET /subscriptions` to retrieve information about the list of subscriptions enabled for your tenant. Subscriptions define the various features and levels of functionality that are available to your organization.

#### ZIA End User Notification
[PR #256](https://github.com/zscaler/zscaler-sdk-python/pull/256) - Added the following new ZIA API Endpoints:
  - Added `GET /eun` to retrieve information browser-based end user notification (EUN) configuration details.
  - Added `PUT /eun` to update the browser-based end user notification (EUN) configuration details.

#### ZIA Admin Audit Logs
[PR #256](https://github.com/zscaler/zscaler-sdk-python/pull/256) - Added the following new ZIA API Endpoints:
  - Added `GET /auditlogEntryReport` to retrieve the status of a request for an audit log report.
  - Added `POST /auditlogEntryReport` to create an audit log report for the specified time period and saves it as a CSV file.
  - Added `DELETE /auditlogEntryReport` to cancel the request to create an audit log report.
  - Added `GET /auditlogEntryReport/download` to download the most recently created audit log report.

#### ZIA Extranets
[PR #256](https://github.com/zscaler/zscaler-sdk-python/pull/256) - Added the following new ZIA API Endpoints:
  - Added `GET /extranet` to retrieve the list of extranets configured for the organization
  - Added `GET /extranet/lite` Retrieves the name-ID pairs of all extranets configured for an organization
  - Added `GET /extranet/{Id}` Retrieves information about an extranet based on the specified ID.
  - Added `POST /extranet` Adds a new extranet for the organization.
  - Added `PUT /extranet/{Id}` Updates an extranet based on the specified ID
  - Added `DELETE /extranet/{Id}` Deletes an extranet based on the specified ID

#### ZIA IOT Endpoint
[PR #256](https://github.com/zscaler/zscaler-sdk-python/pull/256) - Added the following new ZIA IOT API Endpoints:
  - Added `GET /iotDiscovery/deviceTypes` Retrieve the mapping between device type universally unique identifier (UUID) values and the device type names for all the device types supported by the Zscaler AI/ML.
  - Added `GET /iotDiscovery/categories` Retrieve the mapping between the device category universally unique identifier (UUID) values and the category names for all the device categories supported by the Zscaler AI/ML. The parent of device category is device type.
  - Added `GET /iotDiscovery/classifications` Retrieve the mapping between the device classification universally unique identifier (UUID) values and the classification names for all the device classifications supported by Zscaler AI/ML. The parent of device classification is device category.
  - Added `GET /iotDiscovery/deviceList` Retrieve a list of discovered devices with the following key contexts, IP address, location, ML auto-label, classification, category, and type.

#### ZIA 3rd-Party App Governance
[PR #256](https://github.com/zscaler/zscaler-sdk-python/pull/256) - Added the following new ZIA API Endpoints:
  - Added `GET /apps/app` to search the 3rd-Party App Governance App Catalog by either app ID or URL.
  - Added `POST /apps/app` to submis an app for analysis in the 3rd-Party App Governance Sandbox.
  - Added `GET /apps/search` to search for an app by name. Any app whose name contains the search term (appName) is returned.
  - Added `GET /app_views/list` to retrieve the list of custom views that you have configured in the 3rd-Party App Governance.
  - Added `GET /app_views/{appViewId}/apps` to retrieves all assets (i.e., apps) that are related to a specified argument (i.e., custom view).

### ZIA Admin Role Endpoints
[PR #256](https://github.com/zscaler/zscaler-sdk-python/pull/256) - Added the following new ZIA API Endpoints:
    - Added `GET /adminRoles/{roleId}` Retrieves the admin role based on the specified ID
    - Added `GET /adminRoles/lite` Retrieves a name and ID dictionary of all admin roles. The list only includes the name and ID for all admin roles.
    - Added `POST /adminRoles` Adds an admin role.
    - Added `PUT /adminRoles/{roleId}` Updates the admin role based on the specified ID.
    - Added `DELETE /adminRoles/{roleId}` Deletes the admin role based on the specified ID.

### ZPA Credential Pool (New)
[PR #256](https://github.com/zscaler/zscaler-sdk-python/pull/256) - Added new ZPA endpoint:
  - Added `GET /credential-pool` Gets the privileged credential pool details for the specified customer.
  - Added `GET /credential-pool/{id}` Gets the privileged credential pool details for the specified customer.
  - Added `GET /credential-pool/{id}/credential` Given Privileged credential pool id gets mapped privileged credential info
  - Added `POST /credential-pool` Adds a new privileged credential pool for the specified customer.
  - Added `PUT /credential-pool/{id}` Updates the existing credential pool for the specified customer.
  - Added `DELETE /credential-pool/{id}` Updates the existing credential pool for the specified customer.

#### ZWA - Zscaler Workflow Automation (NEW)
[PR #256](https://github.com/zscaler/zscaler-sdk-python/pull/256) - Added new ZWA endpoint:
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

### Cloud & Branch Connector - OneAPI Support
[PR #256](https://github.com/zscaler/zscaler-sdk-python/pull/256) - Cloud & Branch Connector package is now compatible with OneAPI and Legacy API framework. Please refer to README for details.
[PR #256](https://github.com/zscaler/zscaler-sdk-python/pull/256) - Cloud & Branch Connector package has been renamed from `zcon` to `ztw`

### ZTW Policy Management
[PR #256](https://github.com/zscaler/zscaler-sdk-python/pull/256) - Added the following new ZTW API Endpoints:
    - Added `GET /ecRules/ecRdr` Retrieves the list of traffic forwarding rules.
    - Added `PUT /ecRules/ecRdr/{ruleId}` Updates a traffic forwarding rule configuration based on the specified ID.
    - Added `POST /ecRules/ecRdr` Creates a new traffic forwarding rule.
    - Added `GET /ecRules/ecRdr/count` Retrieves the count of traffic forwarding rules available in the Cloud & Branch Connector Admin Portal.

### ZTW Policy Resources
[PR #256](https://github.com/zscaler/zscaler-sdk-python/pull/256) - Added the following new ZTW API Endpoints:
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
  
## 1.0.0 (April, 22 2025) - BREAKING CHANGES

### Notes

- Python Versions: **v3.8, v3.9, v3.10, v3.11**


#### Zscaler OneAPI Support
[PR #255](https://github.com/zscaler/zscaler-sdk-python/pull/255): Added support for [OneAPI](https://help.zscaler.com/oneapi/understanding-oneapi) Oauth2 authentication support through [Zidentity](https://help.zscaler.com/zidentity/what-zidentity).

**NOTES**
  - Starting at v1.0.0 version this SDK provides dual API client functionality and is backwards compatible with the legacy Zscaler API framework.
  - The new OneAPI framework is compatible only with the following products `ZCC/ZIA/ZPA`.
  - The following products `ZTW` - Cloud Connector and `ZDX` and Zscaler Digital Experience, authentication methods remain unnaffected.
  - The package `ZCON` (Zscaler Cloud and Branch Connector) has been renamed to `ZTW`
  - The following products `ZWA` - Zscaler Workflow Automation authentication methods remain unnaffected.

Refer to the [README](https://github.com/zscaler/zscaler-sdk-python/blob/master/README.md) page for details on client instantiation, and authentication requirements on each individual product.

**WARNING**: Attention Government customers. OneAPI and Zidentity is not currently supported for the following ZIA clouds: `zscalergov` and `zscalerten` or ZPA `GOV`, and `GOVUS`. Please refer to the Zscaler Legacy API Framework section in the [README](https://github.com/zscaler/zscaler-sdk-python/blob/master/README.md) for more information on how authenticate to these environments using the built-in Legacy API method.

[PR #255](https://github.com/zscaler/zscaler-sdk-python/pull/255): All API clients now support Config Setter object `ZCC/ZTW/ZDX/ZIA/ZPA/ZWA`

#### ZCC New Endpoints
[PR #255](https://github.com/zscaler/zscaler-sdk-python/pull/255) - Added the following new ZCC API Endpoints:
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

#### ZIA Sandbox Submission - BREAKING CHANGES
[PR #255](https://github.com/zscaler/zscaler-sdk-python/pull/255) - Authentication to Zscaler Sandbox now use the following attributes during client instantiation.
 - `sandboxToken` - Can also be sourced from the `ZSCALER_SANDBOX_TOKEN` environment variable.
 - `sandboxCloud` - Can also be sourced from the `ZSCALER_SANDBOX_CLOUD` environment variable.

**NOTE** The previous `ZIA_SANDBOX_TOKEN` has been deprecated.

#### ZIA Sandbox Rules
[PR #255](https://github.com/zscaler/zscaler-sdk-python/pull/255) - Added the following new ZIA API Endpoints:
  - Added `GET /sandboxRules` to retrieve the list of all Sandbox policy rules.
  - Added `GET /sandboxRules/{ruleId}` to retrieve the Sandbox policy rule information based on the specified ID.
  - Added `POST /sandboxRules` to add a Sandbox policy rule.
  - Added `PUT /sandboxRules/{ruleId}` to update the Sandbox policy rule configuration for the specified ID.
  - Added `DELETE /sandboxRules/{ruleId}` to delete the Sandbox policy rule based on the specified ID.

#### ZIA DNS Control Rules
[PR #255](https://github.com/zscaler/zscaler-sdk-python/pull/255) - Added the following new ZIA API Endpoints:
  - Added `GET /firewallDnsRules` to retrieve the list of all DNS Control policy rules.
  - Added `GET /firewallDnsRules/{ruleId}` to retrieve the DNS Control policy rule information based on the specified ID.
  - Added `POST /firewallDnsRules` to add a DNS Control policy rules.
  - Added `PUT /firewallDnsRules/{ruleId}` to update the DNS Control policy rule configuration for the specified ID.
  - Added `DELETE /firewallDnsRules/{ruleId}` to delete the DNS Control policy rule based on the specified ID.

#### ZIA IPS Control Rules
[PR #255](https://github.com/zscaler/zscaler-sdk-python/pull/255) - Added the following new ZIA API Endpoints:
  - Added `GET /firewallIpsRules` to retrieve the list of all IPS Control policy rules.
  - Added `GET /firewallIpsRules/{ruleId}` to retrieve the IPS Control policy rule information based on the specified ID.
  - Added `POST /firewallIpsRules` to add a IPS Control policy rule.
  - Added `PUT /firewallIpsRules/{ruleId}` to update the IPS Control policy rule configuration for the specified ID.
  - Added `DELETE /firewallIpsRules/{ruleId}` to delete the IPS Control policy rule based on the specified ID.

#### ZIA File Type Control Policy
[PR #255](https://github.com/zscaler/zscaler-sdk-python/pull/255) - Added the following new ZIA API Endpoints:
  - Added `GET /fileTypeRules` to retrieve the list of all File Type Control policy rules.
  - Added `GET /fileTypeRules/lite` to retrieve the list of all File Type Control policy rules.
  - Added `GET /fileTypeRules/{ruleId}` to retrieve the File Type Control policy rule information based on the specified ID.
  - Added `POST /fileTypeRules` to add a File Type Control policy rule.
  - Added `PUT /fileTypeRules/{ruleId}` to update the File Type Control policy rule configuration for the specified ID.
  - Added `DELETE /fileTypeRules/{ruleId}` to delete the File Type Control policy rule based on the specified ID.

#### ZIA Forwarding Control Policy - Proxy Gateways
[PR #255](https://github.com/zscaler/zscaler-sdk-python/pull/255) - Added the following new ZIA API Endpoints:
  - Added `GET /proxyGateways` to retrieve the proxy gateway information.
  - Added `GET /proxyGateways/lite` to retrieve the name and ID of the proxy.

#### ZIA Cloud Nanolog Streaming Service (NSS)
[PR #255](https://github.com/zscaler/zscaler-sdk-python/pull/255) - Added the following new ZIA API Endpoints:
  - Added `GET /nssFeeds` to retrieve the cloud NSS feeds.
  - Added `GET /nssFeeds/{feedId}` to retrieve information about cloud NSS feed based on the specified ID.
  - Added `POST /nssFeeds` to add a new cloud NSS feed.
  - Added `PUT /nssFeeds/{feedId}` to update cloud NSS feed configuration based on the specified ID.
  - Added `DELETE /nssFeeds/{feedId}` to delete cloud NSS feed configuration based on the specified ID.
  - Added `GET /nssFeeds/feedOutputDefaults` to retrieve the default cloud NSS feed output format for different log types.
  - Added `GET /nssFeeds/testConnectivity/{feedId}` to test the connectivity of cloud NSS feed based on the specified ID
  - Added `POST /nssFeeds/validateFeedFormat` to validates the cloud NSS feed format and returns the validation result

#### ZIA Advanced Threat Protection Policy
[PR #255](https://github.com/zscaler/zscaler-sdk-python/pull/255) - Added the following new ZIA API Endpoints:
  - Added `GET /cyberThreatProtection/advancedThreatSettings` to retrieve the advanced threat configuration settings.
  - Added `PUT /cyberThreatProtection/advancedThreatSettings` to update the advanced threat configuration settings.
  - Added `GET /cyberThreatProtection/maliciousUrls` to retrieve the malicious URLs added to the denylist in the Advanced Threat Protection (ATP) policy
  - Added `PUT /cyberThreatProtection/maliciousUrls` to updates the malicious URLs added to the denylist in ATP policy
  - Added `GET /cyberThreatProtection/securityExceptions` to retrieves information about the security exceptions configured for the ATP policy
  - Added `PUT /cyberThreatProtection/securityExceptions` to update security exceptions for the ATP policy

#### ZIA Advanced Threat Protection Policy
[PR #255](https://github.com/zscaler/zscaler-sdk-python/pull/255) - Added the following new ZIA API Endpoints:
  - Added `GET /cyberThreatProtection/atpMalwareInspection` to retrieve the traffic inspection configurations of Malware Protection policy
  - Added `PUT /cyberThreatProtection/atpMalwareInspection` to update the traffic inspection configurations of Malware Protection policy.
  - Added `GET /cyberThreatProtection/atpMalwareProtocols` to retrieve the protocol inspection configurations of Malware Protection policy
  - Added `PUT /cyberThreatProtection/atpMalwareProtocols` to update the protocol inspection configurations of Malware Protection policy.
  - Added `GET /cyberThreatProtection/malwareSettings` to retrieve the malware protection policy configuration details
  - Added `PUT /cyberThreatProtection/malwareSettings` to update the malware protection policy configuration details.
  - Added `GET /cyberThreatProtection/malwarePolicy` to retrieve information about the security exceptions configured for the Malware Protection policy
  - Added `PUT /cyberThreatProtection/malwarePolicy` to update security exceptions for the Malware Protection policy.

#### ZIA URL & Cloud App Control Policy Settings
[PR #255](https://github.com/zscaler/zscaler-sdk-python/pull/255) - Added the following new ZIA API Endpoints:
  - Added `GET /advancedUrlFilterAndCloudAppSettings` to retrieve information about URL and Cloud App Control advanced policy settings
  - Added `PUT /advancedUrlFilterAndCloudAppSettings` to update the URL and Cloud App Control advanced policy settings

#### ZIA Authentication Settings
[PR #255](https://github.com/zscaler/zscaler-sdk-python/pull/255) - Added the following new ZIA API Endpoints:
  - Added `GET /authSettings` to retrieve the organization's default authentication settings information, including authentication profile and Kerberos authentication information.
  - Added `GET /authSettings/lite` to retrieve organization's default authentication settings information.
  - Added `PUT /authSettings` to update the organization's default authentication settings information.

#### ZIA Advanced Settings
[PR #255](https://github.com/zscaler/zscaler-sdk-python/pull/255) - Added the following new ZIA API Endpoints:
  - Added `GET /advancedSettings` to retrieve information about the advanced settings.
  - Added `PUT /advancedSettings` to update the advanced settings configuration.

#### ZIA Cloud Applications
[PR #255](https://github.com/zscaler/zscaler-sdk-python/pull/255) - Added the following new ZIA API Endpoints:
  - Added `GET /cloudApplications/policy` Retrieves a list of Predefined and User Defined Cloud Applications associated with the DLP rules, Cloud App Control rules, Advanced Settings, Bandwidth Classes, and File Type Control rules.
  - Added `GET /cloudApplications/sslPolicy` Retrieves a list of Predefined and User Defined Cloud Applications associated with the SSL Inspection rules.

#### ZIA Shadow IT Report
[PR #255](https://github.com/zscaler/zscaler-sdk-python/pull/255) - Added the following new ZIA API Endpoints:
- Added `PUT /cloudApplications/bulkUpdate` To Update application status and tag information for predefined or custom cloud applications based on the IDs specified
- Added `GET /cloudApplications/lite` Gets the list of predefined and custom cloud applications
- Added `GET /customTags` Gets the list of custom tags available to assign to cloud applications
- Added `POST /shadowIT/applications/export` Export the Shadow IT Report (in CSV format) for the cloud applications recognized by Zscaler based on their usage in your organization.
- Added `POST /shadowIT/applications/{entity}/exportCsv` Export the Shadow IT Report (in CSV format) for the list of users or known locations identified with using the cloud applications specified in the request.

#### ZIA Remote Assistance Support
[PR #255](https://github.com/zscaler/zscaler-sdk-python/pull/255) - Added the following new ZIA API Endpoints:
  - Added `GET /remoteAssistance` to retrieve information about the Remote Assistance option.
  - Added `PUT /remoteAssistance` to update information about the Remote Assistance option. Using this option, you can allow Zscaler Support to access your organization’s ZIA Admin Portal for a specified time period to troubleshoot issues.

#### ZIA Organization Details
[PR #255](https://github.com/zscaler/zscaler-sdk-python/pull/255) - Added the following new ZIA API Endpoints:
  - Added `GET /orgInformation` to retrieve detailed organization information, including headquarter location, geolocation, address, and contact details.
  - Added `GET /orgInformation/lite` to retrieve minimal organization information.
  - Added `GET /subscriptions` to retrieve information about the list of subscriptions enabled for your tenant. Subscriptions define the various features and levels of functionality that are available to your organization.

#### ZIA End User Notification
[PR #255](https://github.com/zscaler/zscaler-sdk-python/pull/255) - Added the following new ZIA API Endpoints:
  - Added `GET /eun` to retrieve information browser-based end user notification (EUN) configuration details.
  - Added `PUT /eun` to update the browser-based end user notification (EUN) configuration details.

#### ZIA Admin Audit Logs
[PR #255](https://github.com/zscaler/zscaler-sdk-python/pull/255) - Added the following new ZIA API Endpoints:
  - Added `GET /auditlogEntryReport` to retrieve the status of a request for an audit log report.
  - Added `POST /auditlogEntryReport` to create an audit log report for the specified time period and saves it as a CSV file.
  - Added `DELETE /auditlogEntryReport` to cancel the request to create an audit log report.
  - Added `GET /auditlogEntryReport/download` to download the most recently created audit log report.

#### ZIA Extranets
[PR #255](https://github.com/zscaler/zscaler-sdk-python/pull/255) - Added the following new ZIA API Endpoints:
  - Added `GET /extranet` to retrieve the list of extranets configured for the organization
  - Added `GET /extranet/lite` Retrieves the name-ID pairs of all extranets configured for an organization
  - Added `GET /extranet/{Id}` Retrieves information about an extranet based on the specified ID.
  - Added `POST /extranet` Adds a new extranet for the organization.
  - Added `PUT /extranet/{Id}` Updates an extranet based on the specified ID
  - Added `DELETE /extranet/{Id}` Deletes an extranet based on the specified ID

#### ZIA IOT Endpoint
[PR #255](https://github.com/zscaler/zscaler-sdk-python/pull/255) - Added the following new ZIA IOT API Endpoints:
  - Added `GET /iotDiscovery/deviceTypes` Retrieve the mapping between device type universally unique identifier (UUID) values and the device type names for all the device types supported by the Zscaler AI/ML.
  - Added `GET /iotDiscovery/categories` Retrieve the mapping between the device category universally unique identifier (UUID) values and the category names for all the device categories supported by the Zscaler AI/ML. The parent of device category is device type.
  - Added `GET /iotDiscovery/classifications` Retrieve the mapping between the device classification universally unique identifier (UUID) values and the classification names for all the device classifications supported by Zscaler AI/ML. The parent of device classification is device category.
  - Added `GET /iotDiscovery/deviceList` Retrieve a list of discovered devices with the following key contexts, IP address, location, ML auto-label, classification, category, and type.

#### ZIA 3rd-Party App Governance
[PR #255](https://github.com/zscaler/zscaler-sdk-python/pull/255) - Added the following new ZIA API Endpoints:
  - Added `GET /apps/app` to search the 3rd-Party App Governance App Catalog by either app ID or URL.
  - Added `POST /apps/app` to submis an app for analysis in the 3rd-Party App Governance Sandbox.
  - Added `GET /apps/search` to search for an app by name. Any app whose name contains the search term (appName) is returned.
  - Added `GET /app_views/list` to retrieve the list of custom views that you have configured in the 3rd-Party App Governance.
  - Added `GET /app_views/{appViewId}/apps` to retrieves all assets (i.e., apps) that are related to a specified argument (i.e., custom view).

### ZIA Admin Role Endpoints
[PR #255](https://github.com/zscaler/zscaler-sdk-python/pull/255) - Added the following new ZIA API Endpoints:
    - Added `GET /adminRoles/{roleId}` Retrieves the admin role based on the specified ID
    - Added `GET /adminRoles/lite` Retrieves a name and ID dictionary of all admin roles. The list only includes the name and ID for all admin roles.
    - Added `POST /adminRoles` Adds an admin role.
    - Added `PUT /adminRoles/{roleId}` Updates the admin role based on the specified ID.
    - Added `DELETE /adminRoles/{roleId}` Deletes the admin role based on the specified ID.

### ZPA Credential Pool (New)
[PR #255](https://github.com/zscaler/zscaler-sdk-python/pull/255) - Added new ZPA endpoint:
  - Added `GET /credential-pool` Gets the privileged credential pool details for the specified customer.
  - Added `GET /credential-pool/{id}` Gets the privileged credential pool details for the specified customer.
  - Added `GET /credential-pool/{id}/credential` Given Privileged credential pool id gets mapped privileged credential info
  - Added `POST /credential-pool` Adds a new privileged credential pool for the specified customer.
  - Added `PUT /credential-pool/{id}` Updates the existing credential pool for the specified customer.
  - Added `DELETE /credential-pool/{id}` Updates the existing credential pool for the specified customer.

#### ZWA - Zscaler Workflow Automation (NEW)
[PR #255](https://github.com/zscaler/zscaler-sdk-python/pull/255) - Added new ZWA endpoint:
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

### Cloud & Branch Connector - OneAPI Support
[PR #255](https://github.com/zscaler/zscaler-sdk-python/pull/255) - Cloud & Branch Connector package is now compatible with OneAPI and Legacy API framework. Please refer to README for details.
[PR #255](https://github.com/zscaler/zscaler-sdk-python/pull/255) - Cloud & Branch Connector package has been renamed from `zcon` to `ztw`

### ZTW Policy Management
[PR #255](https://github.com/zscaler/zscaler-sdk-python/pull/255) - Added the following new ZTW API Endpoints:
    - Added `GET /ecRules/ecRdr` Retrieves the list of traffic forwarding rules.
    - Added `PUT /ecRules/ecRdr/{ruleId}` Updates a traffic forwarding rule configuration based on the specified ID.
    - Added `POST /ecRules/ecRdr` Creates a new traffic forwarding rule.
    - Added `GET /ecRules/ecRdr/count` Retrieves the count of traffic forwarding rules available in the Cloud & Branch Connector Admin Portal.

### ZTW Policy Resources
[PR #255](https://github.com/zscaler/zscaler-sdk-python/pull/255) - Added the following new ZTW API Endpoints:
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

## 0.10.7 (April,15 2025)

### Notes

- Python Versions: **v3.8, v3.9, v3.10, v3.11**

### Bug Fix:

* ([#254](https://github.com/zscaler/zscaler-sdk-python/pull/254)) - Added retry-status code `408` to prevent random timeouts during unforseen issues.

## 0.10.6 (April,8 2025)

### Notes

- Python Versions: **v3.8, v3.9, v3.10, v3.11**

### Bug Fix:

* ([#253](https://github.com/zscaler/zscaler-sdk-python/pull/253)) - Fixed `_create_conditions_v1` in ZPA `policies` package to ensure proper `conditions` block configuration
* ([#253](https://github.com/zscaler/zscaler-sdk-python/pull/253)) - Included new ZPA `policies` `object_types`. `RISK_FACTOR_TYPE` and `CHROME_ENTERPRISE`.

## 0.10.5 (March,13 2025)

### Notes

- Python Versions: **v3.8, v3.9, v3.10, v3.11**

### Bug Fix:

* ([#251](https://github.com/zscaler/zscaler-sdk-python/pull/251)) - Enhanced `pac_files` function resources.
  - `clone_pac_file` - The function pre-checks if total number of pac file versions within a specific pac file is == 10. If so, it triggers a error requiring the use of the parameter/attribute `delete_version`.
    **NOTE** A maximum of 10 pac file versions is supported. If the total limit is reached you must explicitly indicate via the `delete_version` parameter which version must be removed prior to invoking the `clone_pac_file` method again.

  - `update_pac_file` - The function now validates the current `pac_version_status` prior to attempting an update. The API endpoint behind the `update_pac_file` method requires the `pac_version_status` to have specific value in order to accept the call.

* ([#251](https://github.com/zscaler/zscaler-sdk-python/pull/251)) - Fixed `ZIAClientHelper` to prevent KeyError issues during time expiry check. [Issue 250](https://github.com/zscaler/zscaler-sdk-python/issues/250)
* ([#251](https://github.com/zscaler/zscaler-sdk-python/pull/251)) - Fixed `cloud_apps.list_apps` function to support new pagination parameters `page_number` and `limit`
* ([#251](https://github.com/zscaler/zscaler-sdk-python/pull/251)) - Fixed pagination for `devices.list_devices` to support new pagination paramters.

## 0.10.4 (January,9 2025)

### Notes

- Python Versions: **v3.8, v3.9, v3.10, v3.11**

### Bug Fix:

* ([#237](https://github.com/zscaler/zscaler-sdk-python/pull/237)) - Fixed pagination parameters on ZIA `cloud_apps` resource. Cloud Apps use the following parameters during pagination: `limit` and `page_number`.

## 0.10.3 (January,8 2025)

### Notes

- Python Versions: **v3.8, v3.9, v3.10, v3.11**

### Bug Fix:

* ([#235](https://github.com/zscaler/zscaler-sdk-python/pull/235)) - Added missing `cloud_apps` property resource to ZIA package.

## 0.10.2 (January,6 2025)

### Notes

- Python Versions: **v3.8, v3.9, v3.10, v3.11**

### Bug Fix:

* ([#231](https://github.com/zscaler/zscaler-sdk-python/pull/231)) - Improved ZIA pagination logic to enhance flexibility and address user-reported issues. The changes include:
  - Fixed behavior where `pagesize` was being ignored, defaulting to 100. The SDK now respects the user-specified `pagesize` value within API limits (100-10,000).
  - Added explicit handling for the `page` parameter. When provided, the SDK fetches data from only the specified page without iterating through all pages.
  - Updated docstrings and documentation to clarify the correct usage of `page` and `pagesize` parameters.


## 0.10.1 (December,18 2024)

### Notes

- Python Versions: **v3.8, v3.9, v3.10, v3.11**

### Bug Fix:

* ([#225](https://github.com/zscaler/zscaler-sdk-python/pull/225)) - Fixed ZPA policy condition template to support object_type aggregation. Issue #214
* ([#225](https://github.com/zscaler/zscaler-sdk-python/pull/225)) - Fixed ZIA PAC file `list_pac_files` docstring documentation.

## 0.10.0 (November,15 2024)

### Notes

- Python Versions: **v3.8, v3.9, v3.10, v3.11**

### Enhancements

#### ZIA Pac Files
* Added `GET /pacFiles` to Retrieves the list of all PAC files which are in deployed state.([#203](https://github.com/zscaler/zscaler-sdk-python/pull/203))
* Added `GET /pacFiles/{pacId}/version` to Retrieves all versions of a PAC file based on the specified ID. ([#203](https://github.com/zscaler/zscaler-sdk-python/pull/203))
* Added `GET /pacFiles/{pacId}/version/{pacVersion}` to Retrieves a specific version of a PAC file based on the specified ID. ([#203](https://github.com/zscaler/zscaler-sdk-python/pull/203))
* Added `POST /pacFiles` to Adds a new custom PAC file.([#203](https://github.com/zscaler/zscaler-sdk-python/pull/203))
* Added `DELETE /pacFiles/{pacId}` to Deletes an existing PAC file including all of its versions based on the specified ID.([#203](https://github.com/zscaler/zscaler-sdk-python/pull/203))
* Added `PUT /pacFiles/{pacId}/version/{pacVersion}/action/{pacVersionAction}` to Performs the specified action on the PAC file version and updates the file status.([#203](https://github.com/zscaler/zscaler-sdk-python/pull/203))
* Added `POST /pacFiles/validate` to send the PAC file content for validation and returns the validation result.([#203](https://github.com/zscaler/zscaler-sdk-python/pull/203))
* Added `POST /pacFiles/{pacId}/version/{clonedPacVersion}` to Adds a new PAC file version by branching an existing version based on the specified ID. ([#203](https://github.com/zscaler/zscaler-sdk-python/pull/203))

## 0.9.7 (November,1 2024)

### Notes

- Python Versions: **v3.8, v3.9, v3.10, v3.11**

### Bug Fixes

* Fixed ZPA Policy Set Controller complex Conditions template to support inner `AND/OR` operators ([#199](https://github.com/zscaler/zscaler-sdk-python/pull/199)). Issue #([#198](https://github.com/zscaler/zscaler-sdk-python/pull/198))


## 0.9.6 (October,28 2024)

### Notes

- Python Versions: **v3.8, v3.9, v3.10, v3.11**

### Bug Fixes

* Fixed ZPA Policy Set Controller Conditions template to support nested conditions and operators ([#194](https://github.com/zscaler/zscaler-sdk-python/pull/194)).
* Fixed ZIA pagination by introducing the custom `get_paginated_data` function ([#194](https://github.com/zscaler/zscaler-sdk-python/pull/194)).

## 0.9.5 (October, 9 2024)

### Notes

- Python Versions: **v3.8, v3.9, v3.10, v3.11**

### Bug Fixes

* Fixed ZPA App Connector and Service Edge Bulk Delete functions due to return error ([#182](https://github.com/zscaler/zscaler-sdk-python/pull/182))
* Deprecated the ZIA function `get_location_group_by_name`. Users must use Use `list_location_groups(name=group_name)` instead going forward. ([#182](https://github.com/zscaler/zscaler-sdk-python/pull/182))

## 0.9.4 (October, 3 2024)

### Notes

- Python Versions: **v3.8, v3.9, v3.10, v3.11**

### Bug Fixes

* Fixed ZPA Microtenant Update method response processing.  ([#173](https://github.com/zscaler/zscaler-sdk-python/pull/173))
* Fixed ZIA `check_static_ip` text parsing  ([#173](https://github.com/zscaler/zscaler-sdk-python/pull/173))

## 0.9.3 (September, 16 2024)

### Notes

- Python Versions: **v3.8, v3.9, v3.10, v3.11**

### Bug Fixes

* Added function `list_version_profiles` to ZPA `connectors` package  ([#156](https://github.com/zscaler/zscaler-sdk-python/pull/156))


## 0.9.2 (September, 12 2024)

### Notes

- Python Versions: **v3.8, v3.9, v3.10, v3.11**

### Bug Fixes

* Fixed ZIA DLP Engine `description` missing attribute in payload construction ([#154](https://github.com/zscaler/zscaler-sdk-python/pull/154))

## 0.9.1 (August, 31 2024)

### Notes

- Python Versions: **v3.8, v3.9, v3.10, v3.11**

### Bug Fixes

* Added Zscaler Mobile Admin Portal package ([#142](https://github.com/zscaler/zscaler-sdk-python/pull/142))

## 0.9.0 (August, 23 2024)

### Notes

- Python Versions: **v3.8, v3.9, v3.10, v3.11**

### Bug Fixes

* Added new ZPA PUT v2 Endpoint for Segment Group Updates ([#136](https://github.com/zscaler/zscaler-sdk-python/pull/136))

## 0.8.0 (August, 17 2024)

### Notes

- Python Versions: **v3.8, v3.9, v3.10, v3.11**

### Bug Fixes

* Added new ZIA Cloud App Control Rule and URL Domain Review Endpoints ([#132](https://github.com/zscaler/zscaler-sdk-python/pull/132))

## 0.7.0 (August, 17 2024)

### Notes

- Python Versions: **v3.8, v3.9, v3.10, v3.11**

### Bug Fixes

* Added Zscaler Cloud and Branch Connector Endpoints ([#135](https://github.com/zscaler/zscaler-sdk-python/pull/135))

## 0.6.2 (July, 19 2024)

### Notes

- Python Versions: **v3.8, v3.9, v3.10, v3.11**

### Bug Fixes

* Fixed ZPA Resources and ZIA is_expired method ([#125](https://github.com/zscaler/zscaler-sdk-python/pull/125))

## 0.6.1 (July, 4 2024)

### Notes

- Python Versions: **v3.8, v3.9, v3.10, v3.11**

### Bug Fixes

* Fixed ZPA Pagination pagesize parameter to the maximum supported of `500` ([#118](https://github.com/zscaler/zscaler-sdk-python/pull/118))
* Fixed ZIA Isolation Profile method misconfiguration ([#118](https://github.com/zscaler/zscaler-sdk-python/pull/118))

### Enhancements

* Added the following new ZIA location management endpoints ([#118](https://github.com/zscaler/zscaler-sdk-python/pull/118))
    * `locations/bulkDelete`
    * `locations/groups/count`


## 0.6.0 (June, 28 2024)

### Notes

- Python Versions: **v3.8, v3.9, v3.10, v3.11**

### Bug Fixes

* Added ZDX Endpoints, Tests and Examples ([#116](https://github.com/zscaler/zscaler-sdk-python/pull/116))

## 0.5.2 (June, 24 2024)

### Notes

- Python Versions: **v3.8, v3.9, v3.10, v3.11**

### Bug Fixes

* Fixed ZIA Integration Test for Cloud Firewall Network Services ([#113](https://github.com/zscaler/zscaler-sdk-python/pull/113))

## 0.5.1 (June, 20 2024)

### Notes

- Python Versions: **v3.8, v3.9, v3.10, v3.11**

### Bug Fixes

* Added and Fixed ZIA integration tests. ([#112](https://github.com/zscaler/zscaler-sdk-python/pull/112))

## 0.5.0 (June, 19 2024)

### Notes

- Python Versions: **v3.8, v3.9, v3.10, v3.11**

### Bug Fixes

* Fixed ZIA `forwarding_control` nested attribute formatting. ([#105](https://github.com/zscaler/zscaler-sdk-python/pull/105))
* Fixed ZIA `zpa_gateway` nested attribute formatting. ([#105](https://github.com/zscaler/zscaler-sdk-python/pull/105))

## 0.4.0 (June, 07 2024)

### Notes

- Python Versions: **v3.8, v3.9, v3.10, v3.11**

### Enhancements

* Added support to ZPA Microtenant endpoints ([#105](https://github.com/zscaler/zscaler-sdk-python/pull/105))

## 0.3.1 (May, 29 2024)

### Notes

- Python Versions: **v3.8, v3.9, v3.10, v3.11**

### Enhancements

* Enhanced zpa rate-limit with retry-after header tracking ([#100](https://github.com/zscaler/zscaler-sdk-python/pull/100))

## 0.3.0 (May, 25 2024)

### Notes

- Python Versions: **v3.8, v3.9, v3.10, v3.11**

### Enhancements

* Added support the zpa policy set v2 endpoints ([#96](https://github.com/zscaler/zscaler-sdk-python/pull/96))

## 0.2.0 (May, 14 2024)

### Notes

- Python Versions: **v3.8, v3.9, v3.10, v3.11**

### Enhancements

* Added Cloud Browser Isolation Endpoints and Tests ([#86](https://github.com/zscaler/zscaler-sdk-python/pull/86))

## 0.1.8 (May, 06 2024)

### Notes

- Python Versions: **v3.8, v3.9, v3.10, v3.11**

### Bug Fixes

* Fixed privileged remote access add_portal method return response ([#86](https://github.com/zscaler/zscaler-sdk-python/pull/86))

## 0.1.7 (May, 06 2024)

### Notes

- Python Versions: **v3.8, v3.9, v3.10, v3.11**

### Internal Changes

* Upgraded python-box to v7.1.1

## 0.1.6 (April, 30 2024)

### Notes

- Python Versions: **v3.8, v3.9, v3.10, v3.11**

### Internal Changes

* Added CodeCov workflow step([#83](https://github.com/zscaler/zscaler-sdk-python/pull/83))

## 0.1.5 (April, 26 2024)

### Notes

- Python Versions: **v3.8, v3.9, v3.10, v3.11**

### Bug Fixes

* Update ZPA LSS clientTypes and log formats to new lss v2 endpoint([#77](https://github.com/zscaler/zscaler-sdk-python/pull/77))

## 0.1.4 (April, 26 2024)

### Notes

- Python Versions: **v3.8, v3.9, v3.10, v3.11**

### Bug Fixes

* Fixed ZPA Connector Schedule functions due to endpoint handler change([#76](https://github.com/zscaler/zscaler-sdk-python/pull/76))

## 0.1.3 (April, 24 2024)

### Notes

- Python Versions: **v3.8, v3.9, v3.10, v3.11**

### Internal Changes

* Removed .devcontainer directory and updated makefile ([#75](https://github.com/zscaler/zscaler-sdk-python/pull/75))
* Transition from setup.py to Poetry ([#75](https://github.com/zscaler/zscaler-sdk-python/pull/75))

## 0.1.2 (April, 20 2024)

### Notes

- Python Versions: **v3.8, v3.9, v3.10, v3.11**

### Bug Fixes

* Fixed ZIA `list_dlp_incident_receiver` method to return proper `Box` response ([#67](https://github.com/zscaler/zscaler-sdk-python/pull/67))
* Fixed ZIA sandbox `get_file_hash_count` to properly parse the API response ([#67](https://github.com/zscaler/zscaler-sdk-python/pull/67))
* Removed pre-shared-key randomization from `add_vpn_credential` ([#67](https://github.com/zscaler/zscaler-sdk-python/pull/67))

## 0.1.1 (April, 19 2024)

### Notes

- Python Versions: **v3.8, v3.9, v3.10, v3.11**

### Internal Changes

* Refactored `setup.py` for better packaging and improved long description through README.md ([#57](https://github.com/zscaler/zscaler-sdk-python/pull/57))
* Refactored Integration Tests by removing `async` decorators ([#63](https://github.com/zscaler/zscaler-sdk-python/pull/63))


## 0.1.0 (April, 18 2024)

### Notes

- Python Versions: **v3.8, v3.9, v3.10, v3.11**

🎉 **Initial Release** 🎉
