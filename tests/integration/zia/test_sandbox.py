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

import pytest

from tests.integration.zia.conftest import MockZIAClient


@pytest.fixture
def fs():
    yield


class TestSandbox:
    """
    Integration Tests for the Sandbox Operations.

    These tests use VCR to record and replay HTTP interactions.
    """

    @pytest.mark.vcr()
    def test_sandbox_get_quota(self, fs):
        """Test retrieving sandbox quota."""
        client = MockZIAClient(fs)

        quota_info, _, err = client.zia.sandbox.get_quota()
        assert err is None, f"Error fetching sandbox quota: {err}"
        assert isinstance(quota_info, list), "Expected quota_info to be a list"

    @pytest.mark.vcr()
    def test_sandbox_get_report_summary(self, fs):
        """Test retrieving sandbox report summary."""
        client = MockZIAClient(fs)
        test_md5_hash = "F69CA01D65E6C8F9E3540029E5F6AB92"

        report, _, error = client.zia.sandbox.get_report(test_md5_hash, report_details="summary")
        assert error is None, f"Error fetching sandbox report: {error}"
        assert isinstance(report, dict), "Expected sandbox report to be a dictionary"

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
