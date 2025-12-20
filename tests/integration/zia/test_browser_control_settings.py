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


class TestBrowserControlSettings:
    """
    Integration Tests for the Browser Control Settings API.
    """

    @pytest.mark.vcr()
    def test_browser_control_settings(self, fs):
        client = MockZIAClient(fs)
        errors = []

        original_settings = None

        try:
            # Step 1: Get current browser control settings
            try:
                settings, _, error = client.zia.browser_control_settings.get_browser_control_settings()
                assert error is None, f"Error fetching browser control settings: {error}"
                assert settings is not None, "Browser control settings is None"
                original_settings = settings
            except Exception as exc:
                errors.append(f"Failed to get browser control settings: {exc}")

            # Step 2: Update browser control settings
            try:
                if original_settings:
                    updated_settings, _, error = client.zia.browser_control_settings.update_browser_control_settings(
                        plugin_check_frequency='DAILY',
                        bypass_plugins=['ACROBAT', 'FLASH'],
                        bypass_applications=['OUTLOOKEXP'],
                        bypass_all_browsers=False,
                        allow_all_browsers=True,
                        enable_warnings=True,
                    )
                    assert error is None, f"Error updating browser control settings: {error}"
                    assert updated_settings is not None, "Updated browser control settings is None"
            except Exception as exc:
                errors.append(f"Failed to update browser control settings: {exc}")

            # Step 3: Verify the updated settings
            try:
                verified_settings, _, error = client.zia.browser_control_settings.get_browser_control_settings()
                assert error is None, f"Error verifying browser control settings: {error}"
                assert verified_settings is not None, "Verified browser control settings is None"
            except Exception as exc:
                errors.append(f"Failed to verify browser control settings: {exc}")

            # Step 4: Update with blocked browser versions
            try:
                settings_with_blocked, _, error = client.zia.browser_control_settings.update_browser_control_settings(
                    plugin_check_frequency='WEEKLY',
                    blocked_chrome_versions=['CH143', 'CH142'],
                    blocked_firefox_versions=['MF145', 'MF144'],
                    allow_all_browsers=False,
                    enable_warnings=True,
                )
                assert error is None, f"Error updating browser control with blocked versions: {error}"
            except Exception as exc:
                errors.append(f"Failed to update browser control with blocked versions: {exc}")

        finally:
            # Cleanup: Restore original settings if possible
            try:
                if original_settings:
                    client.zia.browser_control_settings.update_browser_control_settings(
                        allow_all_browsers=True,
                        enable_warnings=False,
                    )
            except Exception:
                pass

        # Final assertion
        if errors:
            raise AssertionError(f"Integration Test Errors:\n{chr(10).join(errors)}")

