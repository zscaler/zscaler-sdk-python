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
from tests.integration.ztw.conftest import MockZTWClient
from tests.test_utils import generate_random_string


@pytest.fixture
def fs():
    yield


class TestLocationTemplate:
    """
    Integration Tests for the ZIA Location Template
    """

    @pytest.mark.vcr()
    def test_location_template(self, fs):
        client = MockZTWClient(fs)
        errors = []
        template_id = None

        try:
            # Create Location Template
            try:
                template_name = generate_random_string()
                created_location = client.ztw.location_template.add_location_template(
                    name="tests-ztw-template-" + template_name,
                    desc="tests-ztw-template-" + template_name,
                    template={
                        "templatePrefix": "ztw-prefix-" + template_name,
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
                template_id = created_location.id if hasattr(created_location, 'id') else created_location.get("id", None)
                assert template_id is not None, "Location template creation failed"
            except Exception as exc:
                errors.append(f"Location template creation failed: {exc}")

            try:
                # Verify the location template by listing and finding it
                # Note: LocationTemplateAPI does not have a get_location_template() method
                templates = client.ztw.location_template.list_location_templates()
                retrieved_template = next(
                    (t for t in templates if (t.id if hasattr(t, 'id') else t.get("id")) == template_id),
                    None
                )
                assert retrieved_template is not None, f"Could not find template with ID {template_id}"
                retrieved_id = retrieved_template.id if hasattr(retrieved_template, 'id') else retrieved_template.get("id")
                assert retrieved_id == template_id, "Incorrect location template retrieved"
            except Exception as exc:
                errors.append(f"Retrieving Location Template failed: {exc}")

            try:
                # Update the location template
                # Note: The API requires `name` and `template` to be included in update requests
                template_name_for_update = "tests-ztw-template-" + template_name
                updated_description = "Updated integration test location template"
                updated_template = client.ztw.location_template.update_location_template(
                    template_id,
                    name=template_name_for_update,  # Name is mandatory for updates
                    desc=updated_description,
                    template={  # Template details are mandatory for updates
                        "templatePrefix": "ztw-prefix-" + template_name,
                        "xffForwardEnabled": True,
                        "authRequired": True,
                        "cautionEnabled": False,
                        "aupEnabled": True,
                        "aupTimeoutInDays": 30,
                        "ofwEnabled": True,
                        "ipsControl": True,
                        "enforceBandwidthControl": True,
                        "upBandwidth": 20,  # Changed value to verify update
                        "dnBandwidth": 20,  # Changed value to verify update
                    },
                )
                # Verify the update by listing again
                templates = client.ztw.location_template.list_location_templates()
                updated_location = next(
                    (t for t in templates if (t.id if hasattr(t, 'id') else t.get("id")) == template_id),
                    None
                )
                assert updated_location is not None, f"Could not find updated template with ID {template_id}"
                updated_desc = updated_location.desc if hasattr(updated_location, 'desc') else updated_location.get("desc")
                assert updated_desc == updated_description, "Location template update failed"
            except Exception as exc:
                errors.append(f"Updating location template failed: {exc}")

            try:
                # Retrieve the list of all templates
                locations = client.ztw.location_template.list_location_templates()
                # Check if the newly created location is in the list of templates
                found_location = any(
                    (loc.id if hasattr(loc, 'id') else loc.get("id")) == template_id for loc in locations
                )
                assert found_location, "Newly created location template not found in the list of templates."
            except Exception as exc:
                errors.append(f"Listing location templates failed: {exc}")

        finally:
            # Cleanup operations
            cleanup_errors = []
            if template_id:
                try:
                    _, response, error = client.ztw.location_template.delete_location_template(template_id)
                    # delete_location_template returns (None, response, None) on success
                    # Check response status code if available
                    if response and hasattr(response, 'status_code'):
                        assert response.status_code == 204, f"Location template deletion failed with status {response.status_code}"
                except Exception as exc:
                    cleanup_errors.append(f"Deleting location failed: {exc}")

            errors.extend(cleanup_errors)

        # Assert that no errors occurred during the test
        assert len(errors) == 0, f"Errors occurred during the location template lifecycle test: {errors}"
