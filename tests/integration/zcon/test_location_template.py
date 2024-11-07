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
from tests.test_utils import generate_random_string


@pytest.fixture
def fs():
    yield


class TestLocationTemplate:
    """
    Integration Tests for the ZIA Location Template
    """

    def test_location_template(self, fs):
        client = MockZCONClient(fs)
        errors = []
        template_id = None

        try:
            # Create Location Template
            try:
                template_name = generate_random_string()
                created_location = client.locations.add_location_template(
                    name="voluptate consectetur",
                    desc="officia fugiat voluptate proident",
                    template={
                        "templatePrefix": "zcon-prefix" + template_name,
                        "xffForwardEnabled": True,
                        "authRequired": True,
                        "cautionEnabled": False,
                        "aupEnabled": True,
                        "aupTimeoutInDays": 30,
                        "ofwEnabled": True,
                        "ipsControl": True,
                        "enforceBandwidthControl": True,
                        "upBandwidth": 10,
                        "dnBandwidth": 10,
                    },
                )
                template_id = created_location.get("id", None)
                assert template_id is not None, "Location template creation failed"
            except Exception as exc:
                errors.append(f"Location template creation failed: {exc}")

            try:
                # Verify the location template by retrieving it
                retrieved_template = client.locations.get_location_template(template_id)
                assert retrieved_template["id"] == template_id, "Incorrect location template retrieved"
            except Exception as exc:
                errors.append(f"Retrieving Location Template failed: {exc}")

            try:
                # Update the location template
                updated_description = "Updated integration test location template"
                client.locations.update_location_template(
                    template_id,
                    desc=updated_description,  # Use `desc` instead of `description`
                )
                updated_location = client.locations.get_location_template(template_id)
                assert updated_location.get("desc") == updated_description, "Location template update failed"
            except Exception as exc:
                errors.append(f"Updating location template failed: {exc}")

            try:
                # Retrieve the list of all templates
                locations = client.locations.list_location_templates()
                # Check if the newly created location is in the list of templates
                found_location = any(location["id"] == template_id for location in locations)
                assert found_location, "Newly created location template not found in the list of templates."
            except Exception as exc:
                errors.append(f"Listing location templates failed: {exc}")

        finally:
            # Cleanup operations
            cleanup_errors = []
            if template_id:
                try:
                    delete_status_location = client.locations.delete_location_template(template_id)
                    assert delete_status_location == 204, "Location template deletion failed"
                except Exception as exc:
                    cleanup_errors.append(f"Deleting location failed: {exc}")

            errors.extend(cleanup_errors)

        # Assert that no errors occurred during the test
        assert len(errors) == 0, f"Errors occurred during the location template lifecycle test: {errors}"
