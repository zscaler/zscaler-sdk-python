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
url_blacklist_management.py
===========================

A CLI tool for managing a URL blacklist using the ZIAClientHelper.

Usage:
    python url_blacklist_management.py <action> [options]

Actions:
    get        Retrieve the current blacklist
    add        Add URLs to the blacklist
    remove     Remove URLs from the blacklist
    replace    Replace the entire blacklist with new URLs

Options:
    -u, --urls    URLs to add or remove, separated by commas (required for add, remove, and replace actions)

Examples:
    python3 url_blacklist_management.py get
    python3 url_blacklist_management.py add --urls example.com,web.example.com
    python3 url_blacklist_management.py remove --urls example.com
    python3 url_blacklist_management.py replace --urls newexample.com

"""

import argparse
import os
import time
from zscaler import ZIAClientHelper


def main():
    parser = argparse.ArgumentParser(description="Manage a URL blacklist using the ZIAClientHelper.")
    parser.add_argument(
        "action",
        choices=["get", "add", "remove", "replace", "erase"],
        help="Action to perform",
    )
    parser.add_argument(
        "-u",
        "--urls",
        help="Comma-separated list of URLs (for add, remove, and replace actions)",
        default="",
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

    changes_made = False

    if args.action == "get":
        blacklist = zia.security.get_blacklist()
        print("Current Blacklist URLs:")
        for url in blacklist:
            print(url)

    else:
        if not args.urls and args.action != "erase":
            parser.error("The '-u/--urls' option is required for the 'add', 'remove', and 'replace' actions.")
        url_list = args.urls.split(",") if args.urls else []

        if args.action == "add":
            zia.security.add_urls_to_blacklist(url_list)
            print("URLs added to blacklist.")
            changes_made = True

        elif args.action == "remove":
            zia.security.delete_urls_from_blacklist(url_list)
            print("URLs removed from blacklist.")
            changes_made = True

        elif args.action == "replace":
            zia.security.replace_blacklist(url_list)
            print("Blacklist replaced.")
            changes_made = True

        elif args.action == "erase":
            zia.security.replace_blacklist([])
            print("Blacklist erased.")
            changes_made = True

        # Activate changes if any modifications were made
        if changes_made:
            print("Activating configuration changes. Please wait...")
            time.sleep(5)  # Delay for 5 seconds before activating
            activation_status = zia.activate.activate()
            print(
                "Configuration changes activated successfully. Status:",
                activation_status,
            )


if __name__ == "__main__":
    main()
