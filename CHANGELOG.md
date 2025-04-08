# Zscaler Python SDK Changelog

## 0.10.6 (April,8 2025)

### Notes

- Python Versions: **v3.8, v3.9, v3.10, v3.11**

### Bug Fix:

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