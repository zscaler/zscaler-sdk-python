# Zscaler Python SDK Changelog

## 1.0.0 (March,xx 2025)  - BREAKING CHANGES

### Notes

- Python Versions: **v3.8, v3.9, v3.10, v3.11**

#### Zscaler OneAPI Support
[PR #253](https://github.com/zscaler/zscaler-sdk-go/pull/253): Added support for [OneAPI](https://help.zscaler.com/oneapi/understanding-oneapi) Oauth2 authentication support through [Zidentity](https://help.zscaler.com/zidentity/what-zidentity).

**NOTES** 
  - Starting at v1.0.0 version this SDK provides dual API client functionality and is backwards compatible with the legacy Zscaler API framework.
  - The new OneAPI framework is compatible only with the following products `ZCC/ZIA/ZPA`.
  - The following products `ZCON`, `ZDX`, `ZWA` are only supported via the legacy API framework and have their own individual API client interfaces.
  - This SDK **no longer supports `python-box` (`Box`, `BoxList`)** and has fully transitioned to a **Pythonic dictionary-based approach** for all response handling.

Refer to the [README](https://github.com/zscaler/zscaler-sdk-python/blob/master/README.md) page for details on client instantiation, and authentication requirements on each individual product.

[PR #253](https://github.com/zscaler/zscaler-sdk-python/pull/253): All API clients now support Config Setter object `ZCC/ZCON/ZDX/ZIA/ZPA,ZWA`

#### ZCC New Endpoints
[PR #253](https://github.com/zscaler/zscaler-sdk-python/pull/253) - Added the following new ZCC API Endpoints:
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
[PR #253](https://github.com/zscaler/zscaler-sdk-python/pull/253) - Authentication to Zscaler Sandbox now use the following attributes during client instantiation.
 - `sandboxToken` - Can also be sourced from the `ZSCALER_SANDBOX_TOKEN` environment variable.
 - `sandboxCloud` - Can also be sourced from the `ZSCALER_SANDBOX_CLOUD` environment variable.

**NOTE** The previous `ZIA_SANDBOX_TOKEN` has been deprecated.

#### ZIA Sandbox Rules
[PR #253](https://github.com/zscaler/zscaler-sdk-python/pull/253) - Added the following new ZIA API Endpoints:
  - Added `GET /sandboxRules` to retrieve the list of all Sandbox policy rules.
  - Added `GET /sandboxRules/{ruleId}` to retrieve the Sandbox policy rule information based on the specified ID.
  - Added `POST /sandboxRules` to add a Sandbox policy rule. 
  - Added `PUT /sandboxRules/{ruleId}` to update the Sandbox policy rule configuration for the specified ID.
  - Added `DELETE /sandboxRules/{ruleId}` to delete the Sandbox policy rule based on the specified ID.

#### ZIA DNS Control Rules
[PR #253](https://github.com/zscaler/zscaler-sdk-python/pull/253) - Added the following new ZIA API Endpoints:
  - Added `GET /firewallDnsRules` to retrieve the list of all DNS Control policy rules.
  - Added `GET /firewallDnsRules/{ruleId}` to retrieve the DNS Control policy rule information based on the specified ID.
  - Added `POST /firewallDnsRules` to add a DNS Control policy rules. 
  - Added `PUT /firewallDnsRules/{ruleId}` to update the DNS Control policy rule configuration for the specified ID.
  - Added `DELETE /firewallDnsRules/{ruleId}` to delete the DNS Control policy rule based on the specified ID.

#### ZIA IPS Control Rules
[PR #253](https://github.com/zscaler/zscaler-sdk-python/pull/253) - Added the following new ZIA API Endpoints:
  - Added `GET /firewallIpsRules` to retrieve the list of all IPS Control policy rules.
  - Added `GET /firewallIpsRules/{ruleId}` to retrieve the IPS Control policy rule information based on the specified ID.
  - Added `POST /firewallIpsRules` to add a IPS Control policy rule. 
  - Added `PUT /firewallIpsRules/{ruleId}` to update the IPS Control policy rule configuration for the specified ID.
  - Added `DELETE /firewallIpsRules/{ruleId}` to delete the IPS Control policy rule based on the specified ID.

#### ZIA File Type Control Policy
[PR #253](https://github.com/zscaler/zscaler-sdk-python/pull/253) - Added the following new ZIA API Endpoints:
  - Added `GET /fileTypeRules` to retrieve the list of all File Type Control policy rules.
  - Added `GET /fileTypeRules/lite` to retrieve the list of all File Type Control policy rules.
  - Added `GET /fileTypeRules/{ruleId}` to retrieve the File Type Control policy rule information based on the specified ID.
  - Added `POST /fileTypeRules` to add a File Type Control policy rule. 
  - Added `PUT /fileTypeRules/{ruleId}` to update the File Type Control policy rule configuration for the specified ID.
  - Added `DELETE /fileTypeRules/{ruleId}` to delete the File Type Control policy rule based on the specified ID.

#### ZIA Forwarding Control Policy - Proxy Gateways
[PR #253](https://github.com/zscaler/zscaler-sdk-python/pull/253) - Added the following new ZIA API Endpoints:
  - Added `GET /proxyGateways` to retrieve the proxy gateway information.
  - Added `GET /proxyGateways/lite` to retrieve the name and ID of the proxy.

#### ZIA Cloud Nanolog Streaming Service (NSS)
[PR #253](https://github.com/zscaler/zscaler-sdk-python/pull/253) - Added the following new ZIA API Endpoints:
  - Added `GET /nssFeeds` to retrieve the cloud NSS feeds.
  - Added `GET /nssFeeds/{feedId}` to retrieve information about cloud NSS feed based on the specified ID.
  - Added `POST /nssFeeds` to add a new cloud NSS feed.
  - Added `PUT /nssFeeds/{feedId}` to update cloud NSS feed configuration based on the specified ID.
  - Added `DELETE /nssFeeds/{feedId}` to delete cloud NSS feed configuration based on the specified ID.
  - Added `GET /nssFeeds/feedOutputDefaults` to retrieve the default cloud NSS feed output format for different log types.
  - Added `GET /nssFeeds/testConnectivity/{feedId}` to test the connectivity of cloud NSS feed based on the specified ID
  - Added `POST /nssFeeds/validateFeedFormat` to validates the cloud NSS feed format and returns the validation result

#### ZIA Advanced Threat Protection Policy
[PR #253](https://github.com/zscaler/zscaler-sdk-python/pull/253) - Added the following new ZIA API Endpoints:
  - Added `GET /cyberThreatProtection/advancedThreatSettings` to retrieve the advanced threat configuration settings.
  - Added `PUT /cyberThreatProtection/advancedThreatSettings` to update the advanced threat configuration settings.
  - Added `GET /cyberThreatProtection/maliciousUrls` to retrieve the malicious URLs added to the denylist in the Advanced Threat Protection (ATP) policy
  - Added `PUT /cyberThreatProtection/maliciousUrls` to updates the malicious URLs added to the denylist in ATP policy
  - Added `GET /cyberThreatProtection/securityExceptions` to retrieves information about the security exceptions configured for the ATP policy
  - Added `PUT /cyberThreatProtection/securityExceptions` to update security exceptions for the ATP policy
  
#### ZIA Advanced Threat Protection Policy
[PR #253](https://github.com/zscaler/zscaler-sdk-python/pull/253) - Added the following new ZIA API Endpoints:
  - Added `GET /cyberThreatProtection/atpMalwareInspection` to retrieve the traffic inspection configurations of Malware Protection policy
  - Added `PUT /cyberThreatProtection/atpMalwareInspection` to update the traffic inspection configurations of Malware Protection policy.
  - Added `GET /cyberThreatProtection/atpMalwareProtocols` to retrieve the protocol inspection configurations of Malware Protection policy
  - Added `PUT /cyberThreatProtection/atpMalwareProtocols` to update the protocol inspection configurations of Malware Protection policy.
  - Added `GET /cyberThreatProtection/malwareSettings` to retrieve the malware protection policy configuration details
  - Added `PUT /cyberThreatProtection/malwareSettings` to update the malware protection policy configuration details.
  - Added `GET /cyberThreatProtection/malwarePolicy` to retrieve information about the security exceptions configured for the Malware Protection policy
  - Added `PUT /cyberThreatProtection/malwarePolicy` to update security exceptions for the Malware Protection policy. 

#### ZIA URL & Cloud App Control Policy Settings
[PR #253](https://github.com/zscaler/zscaler-sdk-python/pull/253) - Added the following new ZIA API Endpoints:
  - Added `GET /advancedUrlFilterAndCloudAppSettings` to retrieve information about URL and Cloud App Control advanced policy settings
  - Added `PUT /advancedUrlFilterAndCloudAppSettings` to update the URL and Cloud App Control advanced policy settings

#### ZIA Authentication Settings
[PR #253](https://github.com/zscaler/zscaler-sdk-python/pull/253) - Added the following new ZIA API Endpoints:
  - Added `GET /authSettings` to retrieve the organization's default authentication settings information, including authentication profile and Kerberos authentication information.
  - Added `GET /authSettings/lite` to retrieve organization's default authentication settings information.
  - Added `PUT /authSettings` to update the organization's default authentication settings information.

#### ZIA Advanced Settings
[PR #253](https://github.com/zscaler/zscaler-sdk-python/pull/253) - Added the following new ZIA API Endpoints:
  - Added `GET /advancedSettings` to retrieve information about the advanced settings.
  - Added `PUT /advancedSettings` to update the advanced settings configuration.

#### ZIA Cloud Applications
[PR #253](https://github.com/zscaler/zscaler-sdk-python/pull/253) - Added the following new ZIA API Endpoints:
  - Added `GET /cloudApplications/policy` Retrieves a list of Predefined and User Defined Cloud Applications associated with the DLP rules, Cloud App Control rules, Advanced Settings, Bandwidth Classes, and File Type Control rules.
  - Added `GET /cloudApplications/sslPolicy` Retrieves a list of Predefined and User Defined Cloud Applications associated with the SSL Inspection rules.

#### ZIA Shadow IT Report
[PR #253](https://github.com/zscaler/zscaler-sdk-python/pull/253) - Added the following new ZIA API Endpoints:
- Added `PUT /cloudApplications/bulkUpdate` To Update application status and tag information for predefined or custom cloud applications based on the IDs specified
- Added `GET /cloudApplications/lite` Gets the list of predefined and custom cloud applications
- Added `GET /customTags` Gets the list of custom tags available to assign to cloud applications
- Added `POST /shadowIT/applications/export` Export the Shadow IT Report (in CSV format) for the cloud applications recognized by Zscaler based on their usage in your organization.
- Added `POST /shadowIT/applications/{entity}/exportCsv` Export the Shadow IT Report (in CSV format) for the list of users or known locations identified with using the cloud applications specified in the request.

#### ZIA Remote Assistance Support
[PR #253](https://github.com/zscaler/zscaler-sdk-python/pull/253) - Added the following new ZIA API Endpoints:
  - Added `GET /remoteAssistance` to retrieve information about the Remote Assistance option.
  - Added `PUT /remoteAssistance` to update information about the Remote Assistance option. Using this option, you can allow Zscaler Support to access your organization’s ZIA Admin Portal for a specified time period to troubleshoot issues.

#### ZIA Organization Details
[PR #253](https://github.com/zscaler/zscaler-sdk-python/pull/253) - Added the following new ZIA API Endpoints:
  - Added `GET /orgInformation` to retrieve detailed organization information, including headquarter location, geolocation, address, and contact details.
  - Added `GET /orgInformation/lite` to retrieve minimal organization information.
  - Added `GET /subscriptions` to retrieve information about the list of subscriptions enabled for your tenant. Subscriptions define the various features and levels of functionality that are available to your organization.

#### ZIA End User Notification
[PR #253](https://github.com/zscaler/zscaler-sdk-python/pull/253) - Added the following new ZIA API Endpoints:
  - Added `GET /eun` to retrieve information browser-based end user notification (EUN) configuration details.
  - Added `PUT /eun` to update the browser-based end user notification (EUN) configuration details.

#### ZIA Admin Audit Logs
[PR #253](https://github.com/zscaler/zscaler-sdk-python/pull/253) - Added the following new ZIA API Endpoints:
  - Added `GET /auditlogEntryReport` to retrieve the status of a request for an audit log report.
  - Added `POST /auditlogEntryReport` to create an audit log report for the specified time period and saves it as a CSV file.
  - Added `DELETE /auditlogEntryReport` to cancel the request to create an audit log report.
  - Added `GET /auditlogEntryReport/download` to download the most recently created audit log report.

#### ZIA Extranets
[PR #253](https://github.com/zscaler/zscaler-sdk-python/pull/253) - Added the following new ZIA API Endpoints:
  - Added `GET /extranet` to retrieve the list of extranets configured for the organization
  - Added `GET /extranet/lite` Retrieves the name-ID pairs of all extranets configured for an organization
  - Added `GET /extranet/{Id}` Retrieves information about an extranet based on the specified ID.
  - Added `POST /extranet` Adds a new extranet for the organization.
  - Added `PUT /extranet/{Id}` Updates an extranet based on the specified ID
  - Added `DELETE /extranet/{Id}` Deletes an extranet based on the specified ID

#### ZIA IOT Endpoint
[PR #253](https://github.com/zscaler/zscaler-sdk-python/pull/253) - Added the following new ZIA IOT API Endpoints:
  - Added `GET /iotDiscovery/deviceTypes` Retrieve the mapping between device type universally unique identifier (UUID) values and the device type names for all the device types supported by the Zscaler AI/ML.
  - Added `GET /iotDiscovery/categories` Retrieve the mapping between the device category universally unique identifier (UUID) values and the category names for all the device categories supported by the Zscaler AI/ML. The parent of device category is device type.
  - Added `GET /iotDiscovery/classifications` Retrieve the mapping between the device classification universally unique identifier (UUID) values and the classification names for all the device classifications supported by Zscaler AI/ML. The parent of device classification is device category.
  - Added `GET /iotDiscovery/deviceList` Retrieve a list of discovered devices with the following key contexts, IP address, location, ML auto-label, classification, category, and type.

#### ZIA 3rd-Party App Governance
[PR #253](https://github.com/zscaler/zscaler-sdk-python/pull/253) - Added the following new ZIA API Endpoints:
  - Added `GET /apps/app` to search the 3rd-Party App Governance App Catalog by either app ID or URL.
  - Added `POST /apps/app` to submis an app for analysis in the 3rd-Party App Governance Sandbox.
  - Added `GET /apps/search` to search for an app by name. Any app whose name contains the search term (appName) is returned.
  - Added `GET /app_views/list` to retrieve the list of custom views that you have configured in the 3rd-Party App Governance.
  - Added `GET /app_views/{appViewId}/apps` to retrieves all assets (i.e., apps) that are related to a specified argument (i.e., custom view).

#### ZPA SCIM API
[PR #253](https://github.com/zscaler/zscaler-sdk-python/pull/253) - The ZPA SCIM API Client now supports instantiation via configSetter mode. See [README](https://github.com/zscaler/zscaler-sdk-go/blob/master/README.md)

# 2.74.0 (November 14, 2024)

## Notes
- Golang: **v1.22**

#### ZIA PAC Files
[PR #253](https://github.com/zscaler/zscaler-sdk-python/pull/253) - Added the following new ZIA API Endpoints:
  - Added `GET /pacFiles` to Retrieves the list of all PAC files which are in deployed state.
  - Added `GET /pacFiles/{pacId}/version` to Retrieves all versions of a PAC file based on the specified ID.
  - Added `GET /pacFiles/{pacId}/version/{pacVersion}` to Retrieves a specific version of a PAC file based on the specified ID.
  - Added `POST /pacFiles` to Adds a new custom PAC file.
  - Added `DELETE /pacFiles/{pacId}` to Deletes an existing PAC file including all of its versions based on the specified ID.
  - Added `PUT /pacFiles/{pacId}/version/{pacVersion}/action/{pacVersionAction}` to Performs the specified action on the PAC file version and updates the file status.
  - Added `POST /pacFiles/validate` to send the PAC file content for validation and returns the validation result.
  - Added `POST /pacFiles/{pacId}/version/{clonedPacVersion}` to Adds a new PAC file version by branching an existing version based on the specified ID.

#### ZWA - Zscaler Workflow Automation (NEW)
[PR #253](https://github.com/zscaler/zscaler-sdk-python/pull/253) - Added new ZWA endpoint:
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

**Notes** 
| Argument     | Description | Environment variable |
|--------------|-------------|-------------------|
| `key_id`       | _(String)_ The ZWA string that contains the API key ID.| `ZWA_CLIENT_ID` |    
| `key_secret`       | _(String)_ The ZWA string that contains the key secret.| `ZWA_CLIENT_SECRET` |
| `cloud`       | _(String)_ The ZWA string containing cloud provisioned for your organization.| `ZWA_CLOUD` |

## 0.10.5 (March,13 2025)

### Notes

- Python Versions: **v3.8, v3.9, v3.10, v3.11**

### Bug Fix:

* ([#252](https://github.com/zscaler/zscaler-sdk-python/pull/252)) - Enhanced `pac_files` function resources.
  - `clone_pac_file` - The function pre-checks if total number of pac file versions within a specific pac file is == 10. If so, it triggers a error requiring the use of the parameter/attribute `delete_version`.
    **NOTE** A maximum of 10 pac file versions is supported. If the total limit is reached you must explicitly indicate via the `delete_version` parameter which version must be removed prior to invoking the `clone_pac_file` method again.

  - `update_pac_file` - The function now validates the current `pac_version_status` prior to attempting an update. The API endpoint behind the `update_pac_file` method requires the `pac_version_status` to have specific value in order to accept the call.

* ([#252](https://github.com/zscaler/zscaler-sdk-python/pull/252)) - Fixed `ZIAClientHelper` to prevent KeyError issues during time expiry check. [Issue 250](https://github.com/zscaler/zscaler-sdk-python/issues/250)
* ([#252](https://github.com/zscaler/zscaler-sdk-python/pull/252)) - Fixed `cloud_apps.list_apps` function to support new pagination parameters `page_number` and `limit` 
* ([#252](https://github.com/zscaler/zscaler-sdk-python/pull/252)) - Fixed pagination for `devices.list_devices` to support new pagination paramters.

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