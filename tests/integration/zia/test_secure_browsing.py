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


class TestSecureBrowsing:
    """
    Integration Tests for the ZIA Secure Browsing API.

    These tests use VCR to record and replay HTTP interactions.
    """

    @pytest.mark.vcr()
    def test_secure_browsing_workflow(self, fs):
        client = MockZIAClient(fs)
        errors = []

        # Step 1: Retrieve current Browser Control settings
        try:
            current_settings, _, err = client.zia.secure_browsing.get_browser_control_settings()
            assert err is None, f"Error retrieving Browser Control settings: {err}"
            assert current_settings is not None, "Browser Control settings should not be None"
        except Exception as exc:
            errors.append(f"Failed to retrieve Browser Control settings: {exc}")

        # Step 2: Update Browser Control settings with a known-good payload
        try:
            updated_settings, _, err = client.zia.secure_browsing.update_browser_control_settings(
                plugin_check_frequency="DAILY",
                bypass_plugins=["ACROBAT", "FLASH"],
                bypass_applications=["OUTLOOKEXP"],
                bypass_all_browsers=False,
                allow_all_browsers=True,
                enable_warnings=True,
            )
            assert err is None, f"Error updating Browser Control settings: {err}"
            assert updated_settings.plugin_check_frequency == "DAILY", "Plugin check frequency was not updated"
            assert updated_settings.enable_warnings is True, "Warnings flag was not updated"
        except Exception as exc:
            errors.append(f"Failed to update Browser Control settings: {exc}")

        # Step 3: Update Browser Control with blocked browser versions
        try:
            blocked_settings, _, err = client.zia.secure_browsing.update_browser_control_settings(
                plugin_check_frequency="WEEKLY",
                blocked_chrome_versions=["CH143", "CH142"],
                blocked_firefox_versions=["MF145", "MF144"],
                allow_all_browsers=False,
                enable_warnings=True,
            )
            assert err is None, f"Error updating Browser Control with blocked versions: {err}"
            assert blocked_settings.blocked_chrome_versions == ["CH143", "CH142"], "Blocked Chrome versions mismatch"
            assert blocked_settings.blocked_firefox_versions == ["MF145", "MF144"], "Blocked Firefox versions mismatch"
            assert blocked_settings.allow_all_browsers is False, "allow_all_browsers was not updated"
        except Exception as exc:
            errors.append(f"Failed to update Browser Control with blocked versions: {exc}")

        # Step 4: List all supported browser versions
        #
        # Regression guard: the API returns a JSON array (one entry per
        # browser type). A prior bug wrapped the entire array as a single
        # model, producing empty ``versions`` / ``older_versions``. Assert
        # the list is non-empty and every entry carries populated fields.
        try:
            browsers, _, err = client.zia.secure_browsing.get_supported_browser_versions()
            assert err is None, f"Error fetching supported browser versions: {err}"
            assert len(browsers) > 0, "Supported browser versions list is empty"
            for entry in browsers:
                assert entry.browser_type, f"Browser entry is missing browser_type: {entry}"
                assert (len(entry.versions) + len(entry.older_versions)) > 0, (
                    f"Browser {entry.browser_type!r} returned no current or older versions "
                    "(regression: list was wrapped as a single object)"
                )
        except Exception as exc:
            errors.append(f"Failed to list supported browser versions: {exc}")

        # Step 5: Disable Smart Browser Isolation
        try:
            smart, _, err = client.zia.secure_browsing.update_smart_isolation(
                enable_smart_browser_isolation=False,
            )
            assert err is None, f"Error updating Smart Browser Isolation settings: {err}"
            assert smart.enable_smart_browser_isolation is False, "Smart Browser Isolation flag was not updated"
        except Exception as exc:
            errors.append(f"Failed to update Smart Browser Isolation settings: {exc}")

        assert len(errors) == 0, f"Errors occurred during secure browsing test:\n{chr(10).join(errors)}"
