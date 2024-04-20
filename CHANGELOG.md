# Zscaler Python SDK Changelog

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