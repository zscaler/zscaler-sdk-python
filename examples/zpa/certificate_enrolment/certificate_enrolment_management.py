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
certificate_enrolment_management.py
===================================

Manages Enrollment Certificates for Zscaler Private Access (ZPA).

Usage:
    python3 certificate_enrolment_management.py [options]

Options:
    -l, --list                       List all enrollment certificates.
    -s, --search NAME                Search an enrollment certificate by name.

Examples:
    List all enrollment certificates:
        $ python3 certificate_enrolment_management.py -l

    Search an enrollment certificate by name:
        $ python3 certificate_enrolment_management.py -s "Certificate Name"
"""

import argparse
import json
import os
from zscaler import ZPAClientHelper


def main():
    parser = argparse.ArgumentParser(description="Manages Enrollment Certificates for ZPA.")
    parser.add_argument("-l", "--list", action="store_true", help="List all enrollment certificates.")
    parser.add_argument(
        "-s",
        "--search",
        metavar="NAME",
        help="Search an enrollment certificate by name.",
    )
    args = parser.parse_args()

    client = ZPAClientHelper(
        client_id=os.getenv("ZPA_CLIENT_ID"),
        client_secret=os.getenv("ZPA_CLIENT_SECRET"),
        customer_id=os.getenv("ZPA_CUSTOMER_ID"),
        cloud=os.getenv("ZPA_CLOUD"),
    )

    if args.list:
        list_enrolment(client)
    elif args.search:
        search_certificate_by_name(client, args.search)


def list_enrolment(client):
    certs = client.certificates.list_enrolment()
    print(json.dumps(certs, indent=4))


def search_certificate_by_name(client, name):
    certs = client.certificates.list_enrolment()
    matched_cert = next((cert for cert in certs if cert.get("name") == name), None)
    if matched_cert:
        print(json.dumps(matched_cert, indent=4))
    else:
        print(f"No certificate found with name '{name}'.")


if __name__ == "__main__":
    main()
