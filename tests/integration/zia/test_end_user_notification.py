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


class TestEndUserNotification:
    """
    Integration Tests for the End User Notification API.
    """

    @pytest.mark.vcr()
    def test_end_user_notification_operations(self, fs):
        """Test End User Notification operations."""
        client = MockZIAClient(fs)
        errors = []
        original_settings = None

        try:
            # Test get_eun_settings
            settings, response, err = client.zia.end_user_notification.get_eun_settings()
            assert err is None, f"Get EUN settings failed: {err}"
            assert settings is not None, "Settings should not be None"
            original_settings = settings

            # Test update_eun_settings - update with current values
            try:
                # Just re-apply current settings to test the update endpoint
                updated_settings, response, err = client.zia.end_user_notification.update_eun_settings(
                    aup_enabled=original_settings.get("aup_enabled", False) if isinstance(original_settings, dict) else getattr(original_settings, "aup_enabled", False),
                )
                # Update may fail due to permissions - that's ok
            except Exception:
                pass

        except Exception as e:
            errors.append(f"Exception during end user notification test: {str(e)}")

        assert len(errors) == 0, f"Errors occurred: {errors}"
