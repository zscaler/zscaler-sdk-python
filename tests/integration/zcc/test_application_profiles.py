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
from tests.integration.zcc.conftest import MockZCCClient


@pytest.fixture
def fs():
    yield


# The PATCH endpoint expects a friendly device_type ("ios", "android", ...)
# whereas GET responses report the raw API enum ("DEVICE_TYPE_IOS", ...).
_DEVICE_TYPE_TO_FRIENDLY = {
    "DEVICE_TYPE_IOS": "ios",
    "DEVICE_TYPE_ANDROID": "android",
    "DEVICE_TYPE_WINDOWS": "windows",
    "DEVICE_TYPE_MAC": "macos",
    "DEVICE_TYPE_LINUX": "linux",
}


class TestApplicationProfiles:
    """
    Integration Tests for the ZCC Application Profiles API.

    The application profiles resource only exposes two GET methods and a
    single PATCH method (no create/delete), so this lifecycle test:

      1. Lists application profiles via ``get_application_profiles``.
      2. Picks the first profile returned and retrieves it by ID via
         ``get_application_profile``.
      3. Issues a no-op PATCH via ``update_application_profile`` that
         mirrors the existing ``name``, ``description``, ``device_type``
         and ``packet_tunnel_exclude_list`` back to the API. This keeps
         the test safe to run in CI/CD against shared tenants because
         it never mutates the tenant configuration.
    """

    @pytest.mark.vcr()
    def test_application_profiles(self, fs):
        client = MockZCCClient(fs)
        errors = []

        target = None
        target_profile_id = None

        try:
            profiles, _, err = client.zcc.application_profiles.get_application_profiles()
            assert err is None, f"Error listing application profiles: {err}"
            assert isinstance(profiles, list), "Expected a list of application profiles"
            assert profiles, "Expected at least one application profile in the tenant"

            target = profiles[0]
            assert getattr(target, "id", None), "First application profile is missing an ID"
            target_profile_id = str(target.id)
        except Exception as exc:
            errors.append(f"Listing application profiles failed: {exc}")

        try:
            if target_profile_id:
                fetched, _, err = client.zcc.application_profiles.get_application_profile(target_profile_id)
                assert err is None, f"Error fetching application profile {target_profile_id}: {err}"
                assert fetched is not None, f"Expected a profile for ID {target_profile_id}"
                assert str(fetched.id) == target_profile_id, f"Expected ID {target_profile_id}, got {fetched.id}"

                policy_extension = getattr(fetched, "policy_extension", None)
                existing_packet_tunnel_exclude_list = getattr(policy_extension, "packet_tunnel_exclude_list", None)

                update_kwargs = {
                    "name": fetched.name,
                    "description": fetched.description,
                }

                friendly_device_type = _DEVICE_TYPE_TO_FRIENDLY.get(getattr(fetched, "device_type", None))
                if friendly_device_type:
                    update_kwargs["device_type"] = friendly_device_type

                if existing_packet_tunnel_exclude_list is not None:
                    update_kwargs["packet_tunnel_exclude_list"] = existing_packet_tunnel_exclude_list

                updated, _, err = client.zcc.application_profiles.update_application_profile(
                    profile_id=target_profile_id,
                    **update_kwargs,
                )
                assert err is None, f"Error updating application profile {target_profile_id}: {err}"
                assert updated is not None, "Expected an updated profile object"
                assert hasattr(updated, "as_dict"), "Updated profile should expose as_dict()"
        except Exception as exc:
            errors.append(f"Application profile operation failed: {exc}")

        assert len(errors) == 0, "Errors occurred during the application profile lifecycle test:\n" + "\n".join(errors)
