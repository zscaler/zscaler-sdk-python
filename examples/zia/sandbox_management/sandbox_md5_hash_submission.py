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
sandbox_md5_hash_submission.py
==============================

CLI tool for interacting with Zscaler Cloud Sandbox through the Zscaler Python SDK for MD5 file hash submission.

Usage:
    python3 sandbox_md5_hash_submission.py --action <action> [--hashes <hashes>]

Actions:
    get_behavioral_analysis        Retrieves the custom list of MD5 file hashes that are blocked by Sandbox.
    add_hash_to_custom_list        Updates the custom list with provided MD5 hashes. Clears the list if no hash is provided.

Options:
    --hashes      A comma-separated list of MD5 hashes to be added to the custom block list. Leave empty to clear the list.

Examples:
    Retrieve the current custom block list:
    python3 sandbox_md5_hash_submission.py --action get_behavioral_analysis

    Add MD5 hashes to the custom block list:
    python3 sandbox_md5_hash_submission.py --action add_hash_to_custom_list --hashes 42914d6d213a20a2684064be5c80ffa9,c0202cf6aeab8437c638533d14563d35

    Clear the custom block list:
    python3 sandbox_md5_hash_submission.py --action add_hash_to_custom_list --hashes ""

"""

import argparse
import os
from zscaler import ZIAClientHelper
import json
import time  # Import the time module for the delay


def main():
    parser = argparse.ArgumentParser(description="CLI tool for Zscaler Cloud Sandbox operations.")
    parser.add_argument(
        "--action",
        required=True,
        choices=["get_behavioral_analysis", "add_hash_to_custom_list"],
        help="The action to perform.",
    )
    parser.add_argument(
        "--hashes",
        nargs="?",
        const="",
        help="Comma-separated list of MD5 hashes for 'add_hash_to_custom_list' action. Leave empty to clear the list.",
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

    if args.action == "get_behavioral_analysis":
        print("\nFetching the custom list of MD5 file hashes blocked by Sandbox...\n")
        behavioral_analysis = zia.sandbox.get_behavioral_analysis()
        print(json.dumps(behavioral_analysis.to_dict(), indent=4))

    elif args.action == "add_hash_to_custom_list":
        file_hashes_to_be_blocked = args.hashes.split(",") if args.hashes else []
        print("\nUpdating the custom list of MD5 file hashes blocked by Sandbox...\n")
        updated_list = zia.sandbox.add_hash_to_custom_list(file_hashes_to_be_blocked)
        print("Updated Custom Block List:")
        print(json.dumps(updated_list.to_dict(), indent=4))

        # Implement a 5-second delay before activating the changes
        print("\nActivating configuration changes...\n")
        time.sleep(5)  # Wait for 5 seconds
        activation_status = zia.activate.activate()  # Call the activate method
        print(f"Configuration activation status: {activation_status}")


if __name__ == "__main__":
    main()
