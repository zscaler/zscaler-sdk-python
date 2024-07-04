# Zscaler Python SDK Changelog

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