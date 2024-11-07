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

from tests.integration.zpa.conftest import MockZPAClient
from tests.test_utils import generate_random_string


@pytest.fixture
def fs():
    yield


class TestAppProtectionCustomControl:
    """
    Integration Tests for the App Protection Custom Control
    """

    def test_app_protection_custom_control(self, fs):
        client = MockZPAClient(fs)
        errors = []  # Initialize an empty list to collect errors

        control_name = "tests-" + generate_random_string()
        control_id = None  # Define control_id here to ensure it's accessible throughout

        try:
            # Create a new custom control
            created_control = client.inspection.add_custom_control(
                name=control_name,
                description=control_name,
                action="PASS",
                default_action="PASS",
                paranoia_level="1",
                severity="CRITICAL",
                type="RESPONSE",
                rules=[
                    {
                        "names": ["test"],
                        "type": "RESPONSE_HEADERS",
                        "conditions": [
                            {"lhs": "SIZE", "op": "GE", "rhs": "1000"},
                        ],
                    },
                    {
                        "type": "RESPONSE_BODY",
                        "conditions": [{"lhs": "SIZE", "op": "GE", "rhs": "1000"}],
                    },
                ],
            )
            if created_control and "id" in created_control:
                control_id = created_control.id
                assert control_id is not None  # Asserting that a non-null ID is returned
            else:
                errors.append("Custom control creation failed or returned unexpected data")

            # Assuming control_id is valid and the banner was created successfully
            if control_id:
                # Update the custom control
                updated_name = control_name + " Updated"
                client.inspection.update_custom_control(control_id, name=updated_name)
                updated_control = client.inspection.get_custom_control(control_id)
                assert updated_control.name == updated_name  # Verify update by checking the updated attribute

                # List custom controls and ensure the updated banner is in the list
                controls_list = client.inspection.list_custom_controls()
                assert any(control.id == control_id for control in controls_list)

        except Exception as exc:
            errors.append(exc)

        finally:
            # Cleanup resources
            if control_id:
                try:
                    client.inspection.delete_custom_control(control_id=control_id)
                except Exception as exc:
                    errors.append(f"Deleting custom control failed: {exc}")

        # Assert that no errors occurred during the test
        assert not errors, f"Errors occurred during the custom control lifecycle test: {errors}"
