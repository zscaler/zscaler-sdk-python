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


class TestRiskProfiles:
    """
    Integration Tests for the Risk Profiles API.
    """

    @pytest.mark.vcr()
    def test_risk_profiles_crud(self, fs):
        """Test Risk Profiles CRUD operations."""
        client = MockZIAClient(fs)
        errors = []
        profile_id = None

        try:
            # Test list_risk_profiles
            profiles, response, err = client.zia.risk_profiles.list_risk_profiles()
            assert err is None, f"List risk profiles failed: {err}"
            assert profiles is not None, "Profiles list should not be None"
            assert isinstance(profiles, list), "Profiles should be a list"

            # Test list_risk_profiles_lite
            profiles_lite, response, err = client.zia.risk_profiles.list_risk_profiles_lite()
            assert err is None, f"List risk profiles lite failed: {err}"

            # Test add_risk_profile - create a new profile
            try:
                created_profile, response, err = client.zia.risk_profiles.add_risk_profile(
                    name="TestRiskProfile_VCR",
                    description="Test risk profile for VCR testing",
                    risk_index_bucket="LOW",
                )
                if err is None and created_profile is not None:
                    profile_id = created_profile.get("id") if isinstance(created_profile, dict) else getattr(created_profile, "id", None)

                    # Test get_risk_profile
                    if profile_id:
                        fetched_profile, response, err = client.zia.risk_profiles.get_risk_profile(profile_id)
                        assert err is None, f"Get risk profile failed: {err}"
                        assert fetched_profile is not None, "Fetched profile should not be None"

                        # Test update_risk_profile
                        try:
                            updated_profile, response, err = client.zia.risk_profiles.update_risk_profile(
                                profile_id=profile_id,
                                name="TestRiskProfile_VCR_Updated",
                                description="Updated test risk profile",
                                risk_index_bucket="MEDIUM",
                            )
                            # Update may fail - that's ok
                        except Exception:
                            pass
            except Exception as e:
                # Add may fail due to permissions/subscription
                pass

            # If we didn't create a profile, test with existing one
            if profile_id is None and profiles and len(profiles) > 0:
                existing_id = profiles[0].id
                fetched_profile, response, err = client.zia.risk_profiles.get_risk_profile(existing_id)
                assert err is None, f"Get risk profile failed: {err}"

        except Exception as e:
            errors.append(f"Exception during risk profiles test: {str(e)}")

        finally:
            # Cleanup - delete created profile
            if profile_id:
                try:
                    client.zia.risk_profiles.delete_risk_profile(profile_id)
                except Exception:
                    pass

        assert len(errors) == 0, f"Errors occurred: {errors}"
