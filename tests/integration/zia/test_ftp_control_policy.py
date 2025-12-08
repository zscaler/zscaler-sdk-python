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


class TestFTPControlPolicy:
    """
    Integration Tests for the FTP Control Policy
    """

    @pytest.mark.vcr()
    def test_ftp_control_policy(self, fs):
        client = MockZIAClient(fs)
        errors = []

        # Step 1: Retrieve current settings
        try:
            current_settings = client.zia.ftp_control_policy.get_ftp_settings()
            assert hasattr(current_settings, "ftp_enabled"), "Missing expected attribute: ftp_enabled"
        except Exception as exc:
            errors.append(f"Failed to retrieve ftp control policy: {exc}")

        # Step 2: Update ftp control policy with valid fields only
        try:
            updated_settings = client.zia.ftp_control_policy.update_ftp_settings(
                ftp_over_http_enabled=True,
                ftp_enabled=True,
                url_categories=["AI_ML_APPS", "PROFESSIONAL_SERVICES", "GENERAL_AI_ML"],
                urls = ["test1.acme.com", "test1.acme.com"]
            )
            assert hasattr(updated_settings, "ftp_enabled"), "Missing expected attribute after update"

        except Exception as exc:
            errors.append(f"Failed to update ftp control policy: {exc}")

        assert len(errors) == 0, f"Errors occurred during ftp control policy test:\n{chr(10).join(errors)}"
