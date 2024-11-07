#!/usr/bin/env python

# Copyright (c) 2023, Zscaler Inc.
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

"""
sandbox_md5_hash_query.py
======================

CLI tool for interacting with Zscaler Cloud Sandbox through the Zscaler Python SDK.

Usage:
    python3 sandbox_md5_hash_query.py --action <action> [--md5 <md5_hash>] [--details <report_details>]

Actions:
    get_quota                  Retrieves the Cloud Sandbox API quota information.
    get_report                 Fetches the Cloud Sandbox report for a given MD5 hash.

Options:
    --md5 <md5_hash>           The MD5 hash of the file to retrieve the report for. Required for 'get_report'.
    --details <report_details> The detail level of the report ('summary' or 'full'). Defaults to 'summary'.

Examples:
    python3 sandbox_md5_hash_query.py --action get_quota
    python3 sandbox_md5_hash_query.py --action get_report --md5 <md5_hash> --details full
"""

import argparse
import os
from zscaler import ZIAClientHelper
import json


def is_md5hash_suspicious(report):
    """Determine if the MD5 hash report indicates the file is suspicious."""
    classification = report.get("summary", {}).get("classification", {})
    # Assuming a score above 50 and type "SUSPICIOUS" as suspicious
    if classification.get("score", 0) > 50 and classification.get("type") == "SUSPICIOUS":
        return True
    return False


def is_md5hash_malicious(report):
    """Determine if the MD5 hash report indicates the file is malicious."""
    classification = report.get("summary", {}).get("classification", {})
    # Assuming a score above 80 and type "MALICIOUS" as malicious
    if classification.get("score", 0) > 80 and classification.get("type") == "MALICIOUS":
        return True
    return False


def main():
    parser = argparse.ArgumentParser(description="CLI tool for Zscaler Cloud Sandbox operations.")
    parser.add_argument(
        "--action",
        required=True,
        choices=["get_quota", "get_report"],
        help="The action to perform.",
    )
    parser.add_argument(
        "--md5",
        help="The MD5 hash of the file to get the report for. Required for 'get_report'.",
    )
    parser.add_argument(
        "--details",
        default="summary",
        choices=["summary", "full"],
        help="The detail level of the report. Defaults to 'summary'.",
    )

    args = parser.parse_args()

    # Initialize ZIAClientHelper
    ZIA_USERNAME = os.getenv("ZIA_USERNAME")
    ZIA_PASSWORD = os.getenv("ZIA_PASSWORD")
    ZIA_API_KEY = os.getenv("ZIA_API_KEY")
    ZIA_CLOUD = os.getenv("ZIA_CLOUD")

    zia = ZIAClientHelper(
        username=ZIA_USERNAME,
        password=ZIA_PASSWORD,
        api_key=ZIA_API_KEY,
        cloud=ZIA_CLOUD,
    )

    if args.action == "get_quota":
        print("\nFetching Cloud Sandbox Quota Information...\n")
        quota_info = zia.sandbox.get_quota()
        print(json.dumps(quota_info.to_dict(), indent=4))

    elif args.action == "get_report":
        if not args.md5:
            print("Error: --md5 option is required for 'get_report' action.")
            return

        print(f"\nQuery Cloud Sandbox Report for MD5: {args.md5} with details: {args.details}\n")
        report = zia.sandbox.get_report(md5_hash=args.md5, report_details=args.details).to_dict()
        print(json.dumps(report, indent=4))

        # Parsing the report
        print("\n\n ########## Parsing report output ########## \n\n")
        if is_md5hash_suspicious(report):
            print("The File Is Suspicious\n\n")
        elif is_md5hash_malicious(report):
            print("The File Is Malicious\n\n")
        else:
            print("The File Is Not Suspicious or Malicious\n\n")


if __name__ == "__main__":
    main()
