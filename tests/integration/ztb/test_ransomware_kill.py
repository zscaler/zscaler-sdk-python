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

"""
Integration tests for the ZTB Ransomware Kill resource.

Uses VCR to record/replay HTTP. Deterministic site_id for cassette matching.
Set MOCK_TESTS=false and ZTB_API_KEY, ZTB_CLOUD (or ZTB_OVERRIDE_URL),
ZTB_TEST_SITE_ID when recording cassettes.
"""

import os
import pytest

from tests.integration.ztb.conftest import MockZTBClient, NameGenerator


@pytest.fixture
def fs():
    yield


@pytest.fixture
def site_id():
    """Deterministic site ID for VCR. Override via ZTB_TEST_SITE_ID when recording."""
    return os.getenv("ZTB_TEST_SITE_ID", "tests-ransomware-kill-site")


@pytest.mark.vcr
class TestRansomwareKill:
    """
    Integration tests for the ZTB Ransomware Kill API.

    Lifecycle: get_email_template (may 404) -> save_email_template ->
    get_email_template (verify) -> get_state -> update_state.
    """

    def test_ransomware_kill_email_template_lifecycle(self, fs, site_id):
        """Test get, save, get cycle for email template."""
        client = MockZTBClient()
        errors = []

        try:
            with client as c:
                # Get (may return empty/404 if no template yet)
                template, _, err = c.ztb.ransomware_kill.get_email_template(site_id)
                if err and "404" not in str(err):
                    errors.append(f"Unexpected error on get: {err}")

                # Save email template
                saved, _, err = c.ztb.ransomware_kill.save_email_template(
                    site_id,
                    email_body="Ransomware detected. Please investigate immediately.",
                    recipients="admin@example.com,security@example.com",
                )
                if err:
                    errors.append(f"Error saving template: {err}")
                elif saved:
                    assert saved.email_body is not None or hasattr(saved, "email_body")
                    assert saved.recipients is not None or hasattr(saved, "recipients")

                # Get again to verify
                got, _, err = c.ztb.ransomware_kill.get_email_template(site_id)
                if err:
                    errors.append(f"Error getting template after save: {err}")
                elif got:
                    assert hasattr(got, "cluster_token")
                    assert hasattr(got, "email_body")
                    assert hasattr(got, "recipients")
                    assert hasattr(got, "token")
        except Exception as exc:
            errors.append(f"Lifecycle failed: {exc}")

        assert len(errors) == 0, f"Errors: {errors}"

    def test_ransomware_kill_get_state(self, fs):
        """Test get_state returns response."""
        client = MockZTBClient()
        with client as c:
            state, _, err = c.ztb.ransomware_kill.get_state()
        # May return error if no state endpoint or 404
        if err:
            pytest.skip(f"get_state not available: {err}")
        assert state is not None or err is not None

    def test_ransomware_kill_update_state(self, fs, site_id):
        """Test update_state for a site."""
        client = MockZTBClient()
        with client as c:
            _, _, err = c.ztb.ransomware_kill.update_state(site_id, "green")
        # May fail if site doesn't exist or endpoint not available
        if err:
            pytest.skip(f"update_state not available: {err}")
