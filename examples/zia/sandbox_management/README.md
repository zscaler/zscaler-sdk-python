Sandbox Management Example
==========================

This set of scripts contains several examples that can be executed from the CLI to read/update/delete MD5 Hashes in the Zscaler Internet Access (ZIA) service. See the [README](../README.md) for authentication requirements. The examples in this folder assume that environment variables are being used as the authentication method.

### Sandbox Quota Query Example
This script is a CLI tool designed for interacting with the Zscaler Cloud Sandbox through the Zscaler Python SDK. It enables users to retrieve Cloud Sandbox API quota information.

Actions:
- ``get_quota``: Retrieves the Cloud Sandbox API quota information.

```shell
$ python3 sandbox_md5_hash_query.py --action get_quota
```

### Sandbox Report Query Example
This script is a CLI tool designed for interacting with the Zscaler Cloud Sandbox through the Zscaler Python SDK. It enables users to fetch both summarized and detailed Cloud Sandbox reports for specific MD5 file hashes.

Actions:
- ``get_report``: Fetches the Cloud Sandbox report for a given MD5 hash.

Options:

- --md5 <md5_hash>: The MD5 hash of the file to retrieve the report for. Required for get_report.
- --details <report_details>: The detail level of the report (``summary`` or ``full``). Defaults to summary.


```shell
python3 sandbox_md5_hash_query.py --action get_report --md5 <md5_hash> --details full
```

### Sandbox MD5 Hash Submission Example
This script is a CLI tool designed for submitting MD5 file hashes to the Zscaler Cloud Sandbox and managing the custom list of MD5 file hashes that are blocked by the Sandbox.

Actions:
* ``add_hash_to_custom_list``: Updates the custom list with provided MD5 hashes. Clears the list if no hash is provided.

Options:
* ``--hashes``: A comma-separated list of MD5 hashes to be added to the custom block list. Leave empty to clear the list.

```shell
$ python3 sandbox_md5_hash_submission.py --action <action> [--hashes <hashes>]
```

### Sandbox MD5 Hash Custom List Query Example
This script is a CLI tool designed for querying MD5 file hashes that are being blocked in the Zscaler Cloud Sandbox.

Actions:

* ``get_behavioral_analysis``: Retrieves the custom list of MD5 file hashes that are blocked by Sandbox.

```shell
$ python3 sandbox_md5_hash_submission.py --action get_behavioral_analysis
```


