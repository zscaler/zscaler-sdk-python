"""
Copyright (c) 2023, Zscaler Inc.

Permission to use, copy, modify, and/or distribute this software for any
purpose with or without fee is hereby granted, provided that the above
copyright notice and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
"""

# import os

# import pytest
# import requests

# from tests.integration.zia.conftest import MockZIAClient


# @pytest.fixture
# def fs():
#     yield


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


# class TestSandbox:
#     """
#     Integration Tests for the Sandbox Operations.
#     """

#     def test_sandbox_get_quota(self, fs):
#         client = MockZIAClient(fs)
#         errors = []

#         try:
#             quota_info, _, err = client.zia.sandbox.get_quota()
#             assert err is None, f"Error fetching sandbox quota: {err}"

#             assert isinstance(quota_info, list), "Expected quota_info to be a list"
#             assert quota_info, "Sandbox quota list is empty"

#             for entry in quota_info:
#                 assert isinstance(entry, dict), "Each quota entry should be a dictionary"
#                 assert "allowed" in entry, "'allowed' key missing in quota entry"
#                 assert isinstance(entry["allowed"], int), "'allowed' should be an integer"
#                 assert entry["allowed"] >= 0, "Allowed quota must be >= 0"

#         except Exception as exc:
#             pytest.fail(f"Sandbox quota retrieval failed: {exc}")

#     def test_sandbox_get_report_summary(self, fs):
#         client = MockZIAClient(fs)
#         test_md5_hash = "F69CA01D65E6C8F9E3540029E5F6AB92"

#         try:
#             report, _, error = client.zia.sandbox.get_report(test_md5_hash, report_details="summary")
#             assert error is None, f"Error fetching sandbox report: {error}"
#             assert isinstance(report, dict), "Expected sandbox report to be a dictionary"
#             assert "Summary" in report, "Missing 'Summary' key in report"
#             assert report["Summary"], "'Summary' section is empty in report"
#         except Exception as exc:
#             pytest.fail(f"Sandbox report retrieval failed: {exc}")

#     def test_add_hash_to_custom_list(self, fs):
#         client = MockZIAClient(fs)
#         test_hashes = [
#             "42914d6d213a20a2684064be5c80ffa9",
#             "c0202cf6aeab8437c638533d14563d35",
#         ]
#         errors = []

#         try:
#             updated_list, _, err = client.zia.sandbox.add_hash_to_custom_list(test_hashes)
#             assert err is None, f"Error adding hashes to custom list: {err}"
#             assert isinstance(updated_list, dict), "Expected a dictionary response"

#             blocked_hashes = updated_list.get("fileHashesToBeBlocked", [])
#             assert isinstance(blocked_hashes, list), "'fileHashesToBeBlocked' must be a list"
#             assert all(h in blocked_hashes for h in test_hashes), "Not all test hashes were added to the block list"

#         except Exception as exc:
#             pytest.fail(f"Adding hashes to custom list failed: {exc}")

    # def test_sandbox_submit_files(self, fs):
    #     client = MockZIAClient(fs)
    #     errors = []
    #     downloaded_files = []

    #     try:
    #         for file_name in FILE_NAMES:
    #             file_url = BASE_URL + file_name
    #             local_file_path = file_name

    #             try:
    #                 # Download file
    #                 response = requests.get(file_url)
    #                 response.raise_for_status()

    #                 with open(local_file_path, "wb") as f:
    #                     f.write(response.content)

    #                 downloaded_files.append(local_file_path)

    #                 # Submit to sandbox
    #                 submission_response, _, error = client.zia.sandbox.submit_file(
    #                     file_path=local_file_path,
    #                     force=True
    #                 )
    #                 assert error is None, f"Error submitting file: {error}"
    #                 assert isinstance(submission_response, dict), "Expected dict response from submit_file"
    #                 assert submission_response.get("code") == 200, f"Unexpected response code: {submission_response}"

    #             except Exception as exc:
    #                 errors.append(f"Sandbox file submission failed for {file_name}: {exc}")

    #     finally:
    #         # Cleanup downloaded files
    #         for file in downloaded_files:
    #             if os.path.exists(file):
    #                 os.remove(file)

    #     assert not errors, f"Errors occurred during sandbox file submission:\n{chr(10).join(errors)}"

    # def test_submit_file_for_inspection(self, fs):
    #     client = MockZIAClient(fs)
    #     errors = []
    #     script_dir = os.path.dirname(os.path.abspath(__file__))
    #     downloaded_files = []

    #     for file_name in FILE_NAMES:
    #         file_url = BASE_URL + file_name
    #         local_file_path = os.path.join(script_dir, file_name)

    #         try:
    #             # Download and write the file locally
    #             response = requests.get(file_url)
    #             response.raise_for_status()

    #             with open(local_file_path, "wb") as f:
    #                 f.write(response.content)

    #             downloaded_files.append(local_file_path)

    #             # Submit the file for inspection
    #             submission_response, _, error = client.zia.sandbox.submit_file_for_inspection(local_file_path)
    #             assert error is None, f"Error submitting {file_name} for inspection: {error}"
    #             assert isinstance(submission_response, dict), "Expected dictionary response"
    #             assert submission_response.get("code") == 200, f"Unexpected response: {submission_response}"

    #         except Exception as exc:
    #             errors.append(f"Sandbox file inspection submission failed for {file_name}: {exc}")

    #     # Cleanup
    #     for file_path in downloaded_files:
    #         if os.path.exists(file_path):
    #             os.remove(file_path)

    #     # Final assertion
    #     assert not errors, f"Errors occurred during sandbox file inspection submission:\n{chr(10).join(errors)}"

    # def test_get_behavioral_analysis(self, fs):
    #     client = MockZIAClient(fs)
    #     try:
    #         behavioral_analysis = client.zia.sandbox.get_behavioral_analysis()
    #         assert behavioral_analysis, "Retrieving behavioral analysis failed."
    #     except Exception as exc:
    #         pytest.fail(f"Retrieving behavioral analysis failed: {exc}")
