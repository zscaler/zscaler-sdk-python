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
from tests.integration.zcon.conftest import MockZCONClient
from zscaler.zcon.activation import ECAdminActivation

@pytest.fixture
def fs():
    yield

class TestActivation:
    """
    Integration Tests for the ZCON Activation
    """

    def test_get_activation_status(self, fs):
        client = MockZCONClient(fs)
        errors = []
        try:
            status = client.activation.get_activation_status()
            assert status is not None, "Activation status should not be None"
            assert status.org_edit_status in ["EDITS_CLEARED", "EDITS_PRESENT", "EDITS_ACTIVATED_ON_RESTART"], "Unexpected org_edit_status"
            assert status.org_last_activate_status in ["CAC_ACTV_UNKNOWN", "CAC_ACTV_UI", "CAC_ACTV_OLD_UI", "CAC_ACTV_SUPERADMIN", "CAC_ACTV_AUTOSYNC", "CAC_ACTV_TIMER"], "Unexpected org_last_activate_status"
        except Exception as e:
            errors.append(f"Failed to get activation status: {e}")

        assert not errors, f"Errors occurred during the test: {errors}"

    def test_update_activation_status(self, fs):
        client = MockZCONClient(fs)
        errors = []
        try:
            update_activation = ECAdminActivation()  # Assuming default constructor works correctly
            updated_status = client.activation.update_activation_status(update_activation)
            assert updated_status is not None, "Updated status should not be None"
            assert updated_status.admin_activate_status in ["ADM_LOGGED_IN", "ADM_EDITING", "ADM_ACTV_QUEUED", "ADM_ACTIVATING", "ADM_ACTV_DONE", "ADM_ACTV_FAIL", "ADM_EXPIRED"], "Unexpected admin_activate_status"
        except Exception as e:
            errors.append(f"Failed to update activation status: {e}")

        assert not errors, f"Errors occurred during the test: {errors}"

    def test_force_activation_status(self, fs):
        client = MockZCONClient(fs)
        errors = []
        try:
            force_activation = ECAdminActivation()
            forced_status = client.activation.force_activation_status(force_activation)
            assert forced_status is not None, "Forced status should not be None"
            assert forced_status.admin_activate_status in ["ADM_LOGGED_IN", "ADM_EDITING", "ADM_ACTV_QUEUED", "ADM_ACTIVATING", "ADM_ACTV_DONE", "ADM_ACTV_FAIL", "ADM_EXPIRED"], "Unexpected admin_activate_status"
        except Exception as e:
            errors.append(f"Failed to force activation status: {e}")

        assert not errors, f"Errors occurred during the test: {errors}"