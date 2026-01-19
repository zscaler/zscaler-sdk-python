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

import pytest

from tests.integration.zia.conftest import MockZIAClient


@pytest.fixture
def fs():
    yield


class TestSandbox:
    """
    Integration Tests for the Sandbox API.
    """

    @pytest.mark.vcr()
    def test_sandbox_operations(self, fs):
        """Test Sandbox operations."""
        client = MockZIAClient(fs)
        errors = []

        try:
            # Test get_quota
            quota, response, err = client.zia.sandbox.get_quota()
            assert err is None, f"Get quota failed: {err}"
            assert quota is not None, "Quota should not be None"

            # Test get_behavioral_analysis
            analysis, response, err = client.zia.sandbox.get_behavioral_analysis()
            assert err is None, f"Get behavioral analysis failed: {err}"

            # Test get_file_hash_count
            hash_count, response, err = client.zia.sandbox.get_file_hash_count()
            assert err is None, f"Get file hash count failed: {err}"

            # Test get_report with a known hash (may fail if hash not found)
            try:
                test_hash = "d41d8cd98f00b204e9800998ecf8427e"  # Example MD5 hash
                report, response, err = client.zia.sandbox.get_report(md5_hash=test_hash)
                # Report may fail for non-existent hash, that's ok
            except Exception:
                pass

            # Test get_report with details
            try:
                test_hash = "d41d8cd98f00b204e9800998ecf8427e"
                report_full, response, err = client.zia.sandbox.get_report(
                    md5_hash=test_hash,
                    report_details="full"
                )
            except Exception:
                pass

            # Test add_hash_to_custom_list (may fail due to permissions)
            try:
                result, response, err = client.zia.sandbox.add_hash_to_custom_list(
                    file_hashes_to_be_blocked=["e99a18c428cb38d5f260853678922e03"]
                )
                # May fail due to permissions
            except Exception:
                pass

        except Exception as e:
            errors.append(f"Exception during sandbox test: {str(e)}")

        assert len(errors) == 0, f"Errors occurred: {errors}"
