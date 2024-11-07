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
sandbox_file_submission.py
==========================

This CLI tool facilitates the submission of files to the Zscaler Internet Access (ZIA) Cloud Sandbox for analysis or inspection. It supports two main operations: submitting a file for detailed analysis and submitting a file for quick inspection.

Usage:
    python sandbox_file_submission.py --action <action> --file <file_path>

Actions:
    submit_analysis      Submit a file for detailed sandbox analysis. Use with --force to force reanalysis.
    submit_inspection    Submit a file for quick inspection.

Options:
    --file <file_path>   Path to the file you want to submit.
    --force              (Optional) Force the sandbox to analyze the file even if it has been previously submitted.

Examples:
    Submit a file named "suspicious.exe" for analysis:
    python3 sandbox_file_submission.py --action submit_analysis --file ./suspicious.exe

    Submit a file named "quick_check.zip" for inspection:
    python3 sandbox_file_submission.py --action submit_inspection --file ./quick_check.zip

Please ensure that the environment variables ZIA_USERNAME, ZIA_PASSWORD, ZIA_API_KEY, ZIA_CLOUD, and ZIA_SANDBOX_TOKEN are set before running this script.
"""

import argparse
import os
import json
from zscaler import ZIAClientHelper


def main():
    parser = argparse.ArgumentParser(description="CLI tool for Zscaler Cloud Sandbox operations.")
    parser.add_argument(
        "--action",
        choices=["submit_analysis", "submit_inspection"],
        required=True,
        help="Action to perform (submit_analysis or submit_inspection).",
    )
    parser.add_argument("--file", required=True, help="Path to the file you want to submit.")
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force the sandbox to analyze the file even if it has been previously submitted. Only applicable for submit_analysis action.",
    )

    args = parser.parse_args()

    # Initialize ZIAClientHelper with environment variables
    zia = ZIAClientHelper(
        username=os.getenv("ZIA_USERNAME"),
        password=os.getenv("ZIA_PASSWORD"),
        api_key=os.getenv("ZIA_API_KEY"),
        cloud=os.getenv("ZIA_CLOUD"),
        sandbox_token=os.getenv("ZIA_SANDBOX_TOKEN"),
    )

    if args.action == "submit_analysis":
        response = zia.sandbox.submit_file(file=args.file, force=args.force)
        print("File submitted for analysis. Response:", json.dumps(response, indent=4))
    elif args.action == "submit_inspection":
        response = zia.sandbox.submit_file_for_inspection(file=args.file)
        print("File submitted for inspection. Response:", json.dumps(response, indent=4))


if __name__ == "__main__":
    main()
