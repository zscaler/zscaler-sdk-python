# -*- coding: utf-8 -*-

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


import os

import pytest
import requests

from tests.integration.zia.conftest import MockZIAClient


@pytest.fixture
def fs():
    yield


# FILE_NAMES = [
#     # "2a961d4e5a2100570c942ed20a29735b.bin",
#     # "327bd8a60fb54aaaba8718c890dda09d.bin",
#     # "7665f6ee9017276dd817d15212e99ca7.bin",
#     # "cefb4323ba4deb9dea94dcbe3faa139f.bin",
#     # "8356bd54e47b000c5fdcf8dc5f6a69fa.apk",
#     # "841abdc66ea1e208f63d717ebd11a5e9.apk",
#     "test-pe-file.exe",
# ]

# BASE_URL = "https://github.com/SecurityGeekIO/malware-samples/raw/main/"


class TestSandbox:
    """
    Integration Tests for the Sandbox Operations.
    """

    def test_sandbox_get_quota(self, fs):
        client = MockZIAClient(fs)
        try:
            quota = client.sandbox.get_quota()
            assert quota.allowed > 0, "Sandbox quota retrieval failed."
        except Exception as exc:
            pytest.fail(f"Sandbox quota retrieval failed: {exc}")

    # def test_sandbox_get_report_summary(self, fs):
    #     client = MockZIAClient(fs)
    #     test_md5_hash = "F69CA01D65E6C8F9E3540029E5F6AB92"
    #     try:
    #         report = client.sandbox.get_report(test_md5_hash)
    #         assert report.summary, "Sandbox report retrieval failed."
    #     except Exception as exc:
    #         pytest.fail(f"Sandbox report retrieval failed: {exc}")

    # def test_sandbox_submit_files(fs):
    #     client = MockZIAClient(fs)
    #     errors = []

    #     for file_name in FILE_NAMES:
    #         file_url = BASE_URL + file_name
    #         local_file_path = (
    #             file_name  # You may choose to download/locate files differently
    #         )

    #         try:
    #             # Simulate file download
    #             response = requests.get(file_url)
    #             response.raise_for_status()  # Ensure we got a valid response

    #             # Write the content to a local file
    #             with open(local_file_path, "wb") as f:
    #                 f.write(response.content)

    #             # Submit the file to the sandbox
    #             submission_response = client.sandbox.submit_file(
    #                 local_file_path, force=True
    #             )
    #             assert (
    #                 submission_response.code == 200
    #             ), f"Sandbox file submission failed for {file_name}."

    #         except Exception as exc:
    #             errors.append(f"Sandbox file submission failed for {file_name}: {exc}")

    #     finally:
    #         # Clean up by removing the downloaded file
    #         if os.path.exists(local_file_path):
    #             os.remove(local_file_path)

    # # Assert no errors occurred during the test
    # assert not errors, f"Errors occurred during sandbox file submission: {errors}"

    # def test_submit_file_for_inspection(self, fs):
    #     client = MockZIAClient(fs)
    #     errors = []

    #     for file_name in FILE_NAMES:
    #         file_url = BASE_URL + file_name
    #         local_file_path = (
    #             file_name  # You may choose to download/locate files differently
    #         )

    #         try:
    #             # Simulate file download
    #             response = requests.get(file_url)
    #             response.raise_for_status()  # Ensure we got a valid response

    #             # Write the content to a local file
    #             with open(local_file_path, "wb") as f:
    #                 f.write(response.content)

    #             # Submit the file to the sandbox
    #             submission_response = client.sandbox.submit_file_for_inspection(
    #                 local_file_path
    #             )
    #             assert (
    #                 submission_response.code == 200
    #             ), f"Sandbox file submission failed for {file_name}."

    #         except Exception as exc:
    #             errors.append(f"Sandbox file submission failed for {file_name}: {exc}")

    #         finally:
    #             # Clean up by removing the downloaded file
    #             if os.path.exists(local_file_path):
    #                 os.remove(local_file_path)

    #     # Assert no errors occurred during the test
    #     assert not errors, f"Errors occurred during sandbox file submission: {errors}"

    def test_get_behavioral_analysis(self, fs):
        client = MockZIAClient(fs)
        try:
            behavioral_analysis = client.sandbox.get_behavioral_analysis()
            assert behavioral_analysis, "Retrieving behavioral analysis failed."
        except Exception as exc:
            pytest.fail(f"Retrieving behavioral analysis failed: {exc}")

    def test_add_hash_to_custom_list(self, fs):
        client = MockZIAClient(fs)
        test_hashes = [
            "42914d6d213a20a2684064be5c80ffa9",
            "c0202cf6aeab8437c638533d14563d35",
        ]
        try:
            updated_list = client.sandbox.add_hash_to_custom_list(test_hashes)
            assert all(
                hash in updated_list.file_hashes_to_be_blocked for hash in test_hashes
            ), "Adding hashes to custom list failed."
        except Exception as exc:
            pytest.fail(f"Adding hashes to custom list failed: {exc}")
