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
isolation_profile_management.py
===========================

Retrieves Cloud Browser Isolation Profile for Zscaler Private Access (ZPA).

**Usage**::

    isolation_profile_management.py [-h] [-v] [-q] [-l] [-g PROFILE_ID] [-n PROFILE_NAME] [additional_args]

**Examples**:

List all Isolation Profile :
    $ python3 isolation_profile_management.py -l

Get details of a specific Isolation Profile by ID:
    $ python3 isolation_profile_management.py -g 99999

Get details of a specific Isolation Profile  by Name:
    $ python3 isolation_profile_management.py -n "Profile_Name"
"""


import argparse
import json
import os
from zscaler import ZPAClientHelper


def main():
    parser = argparse.ArgumentParser(description="Manage Isolation Profiles for ZPA.")
    parser.add_argument("-l", "--list", action="store_true", help="List all isolation profiles.")
    parser.add_argument(
        "-g",
        "--get",
        metavar="PROFILE_ID",
        help="Get details of an isolation profile by ID.",
    )
    parser.add_argument(
        "-n",
        "--get_by_name",
        metavar="NAME",
        help="Get details of an isolation profile by name.",
    )
    args = parser.parse_args()

    # Initialize ZIAClientHelper
    client = ZPAClientHelper(
        client_id=os.getenv("ZPA_CLIENT_ID"),
        client_secret=os.getenv("ZPA_CLIENT_SECRET"),
        customer_id=os.getenv("ZPA_CUSTOMER_ID"),
        cloud=os.getenv("ZPA_CLOUD"),
    )

    if args.list:
        list_profiles(client)
    elif args.get:
        get_profile_by_id(client, args.get)
    elif args.get_by_name:
        get_profile_by_name(client, args.get_by_name)


def list_profiles(client):
    profiles = client.isolation_profile.list_profiles()
    print(json.dumps(profiles, indent=4))


def get_profile_by_id(client, profile_id):
    profile = client.isolation_profile.get_profile_by_id(profile_id)
    if profile:
        print(json.dumps(profile, indent=4))
    else:
        print(f"No isolation profile found with ID {profile_id}")


def get_profile_by_name(client, name):
    profile = client.isolation_profile.get_profile_by_name(name)
    if profile:
        print(json.dumps(profile, indent=4))
    else:
        print(f"No isolation profile found with name {name}")


if __name__ == "__main__":
    main()
