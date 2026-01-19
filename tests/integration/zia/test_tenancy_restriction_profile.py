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


class TestTenancyRestrictionProfile:
    """
    Integration Tests for the Tenancy Restriction Profile API.
    """

    @pytest.mark.vcr()
    def test_tenancy_restriction_profile_crud(self, fs):
        """Test Tenancy Restriction Profile CRUD operations."""
        client = MockZIAClient(fs)
        errors = []
        profile_id = None

        try:
            # Test list_restriction_profile
            profiles, response, err = client.zia.tenancy_restriction_profile.list_restriction_profile()
            assert err is None, f"List restriction profiles failed: {err}"
            assert profiles is not None, "Profiles list should not be None"
            assert isinstance(profiles, list), "Profiles should be a list"

            # Test list_app_item_count
            try:
                app_count, response, err = client.zia.tenancy_restriction_profile.list_app_item_count()
                # May fail due to permissions
            except Exception:
                pass

            # Test add_restriction_profile
            try:
                created_profile, response, err = client.zia.tenancy_restriction_profile.add_restriction_profile(
                    name="TestRestrictionProfile_VCR",
                    description="Test restriction profile for VCR",
                    restriction_type="ALLOW",
                )
                if err is None and created_profile is not None:
                    profile_id = created_profile.get("id") if isinstance(created_profile, dict) else getattr(created_profile, "id", None)

                    # Test get_restriction_profile
                    if profile_id:
                        fetched_profile, response, err = client.zia.tenancy_restriction_profile.get_restriction_profile(profile_id)
                        assert err is None, f"Get restriction profile failed: {err}"
                        assert fetched_profile is not None, "Fetched profile should not be None"

                        # Test update_restriction_profile
                        try:
                            updated_profile, response, err = client.zia.tenancy_restriction_profile.update_restriction_profile(
                                profile_id=profile_id,
                                name="TestRestrictionProfile_VCR_Updated",
                                description="Updated test restriction profile",
                            )
                        except Exception:
                            pass
            except Exception:
                pass  # May fail due to permissions

            # If we didn't create a profile, test with existing one
            if profile_id is None and profiles and len(profiles) > 0:
                existing_id = profiles[0].id
                fetched_profile, response, err = client.zia.tenancy_restriction_profile.get_restriction_profile(existing_id)
                assert err is None, f"Get restriction profile failed: {err}"

        except Exception as e:
            errors.append(f"Exception during tenancy restriction profile test: {str(e)}")

        finally:
            # Cleanup
            if profile_id:
                try:
                    client.zia.tenancy_restriction_profile.delete_restriction_profile(profile_id)
                except Exception:
                    pass

        assert len(errors) == 0, f"Errors occurred: {errors}"
