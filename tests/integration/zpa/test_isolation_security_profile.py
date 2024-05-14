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


class TestCBISecurityProfile:
    """
    Integration Tests for the Cloud Browser Isolation Security Profile
    """

    def test_cbi_security_profile(self, fs):
        client = MockZPAClient(fs)
        errors = []  # Initialize an empty list to collect errors

        profile_name = "tests-" + generate_random_string()
        profile_description = "tests-" + generate_random_string()
        profile_id = None  # Define profile_id here to ensure it's accessible throughout

        try:
            try:
                # Obtain the cbi certificate
                banners = client.isolation.list_banners()
                assert banners, "Failed to retrieve CBI banners"
                first_banner_id = banners[0]["id"]  # Assume banners returns a list of dictionaries with 'id' key
            except Exception as exc:
                errors.append(f"Retrieving CBI banners failed: {exc}")

            try:
                # Obtain the cbi certificate
                certs = client.isolation.list_certificates()
                assert certs, "Failed to retrieve CBI certificates"
                first_cert_id = certs[0]["id"]  # Assume certs returns a list of dictionaries with 'id' key
            except Exception as exc:
                errors.append(f"Retrieving CBI certificates failed: {exc}")

            try:
                regions = client.isolation.list_regions()
                assert isinstance(regions, list) and len(regions) >= 2, "Expected at least two CBI regions"
                tested_regions = [regions[0]["id"], regions[1]["id"]]  # Test the first two region IDs
            except AssertionError as exc:
                errors.append(f"Assertion error: {str(exc)}")
            except Exception as exc:
                errors.append(f"Listing CBI regions failed: {str(exc)}")

            try:
                # Create a new isolation profile
                created_profile = client.isolation.add_cbi_profile(
                    name=profile_name,
                    description=profile_description,
                    region_ids=tested_regions,
                    security_controls={
                        "document_viewer": True,
                        "allow_printing": True,
                        "watermark": {
                            "enabled": True,
                            "show_user_id": True,
                            "show_timestamp": True,
                            "show_message": True,
                            "message": "Test",
                        },
                        "flattened_pdf": False,
                        "upload_download": "all",
                        "restrict_keystrokes": True,
                        "copy_paste": "all",
                        "local_render": True,
                    },
                    debug_mode={
                        "allowed": True,
                        "file_password": "test-" + generate_random_string(),
                    },
                    banner_id=first_banner_id,
                    certificate_ids=[first_cert_id],
                )
                if created_profile and "id" in created_profile:
                    profile_id = created_profile["id"]
            except Exception as exc:
                errors.append(f"Profile creation failed: {exc}")

            try:
                # Assuming profile_id is valid and the profile was created successfully
                if profile_id:
                    # Update the isolation profile
                    updated_name = profile_name + " Updated"
                    client.isolation.update_cbi_profile(profile_id, name=updated_name)
                    updated_profile = client.isolation.get_cbi_profile(profile_id)
                    assert updated_profile["name"] == updated_name  # Verify update by checking the updated attribute

                    # List isolation profiles and ensure the updated profile is in the list
                    profiles_list = client.isolation.list_cbi_profiles()
                    assert any(profile["id"] == profile_id for profile in profiles_list)

            except Exception as exc:
                errors.append(exc)

        finally:
            # Attempt to delete the isolation profile if it was created
            if profile_id:
                try:
                    # Delete the isolation profile
                    delete_response_code = client.isolation.delete_cbi_profile(profile_id)
                    assert str(delete_response_code) == "200"  # Adjust to expect '200' as per API behavior
                except Exception as exc:
                    errors.append(exc)

        # Assert that no errors occurred during the test
        assert len(errors) == 0, f"Errors occurred during the isolation security profile lifecycle test: {errors}"
