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


class TestPredefinedIPBasedApps:
    """
    Integration Tests for the ZCC Predefined IP-Based Apps API.

    The predefined IP-based apps resource only exposes two GET methods
    (no create/update/delete), so this lifecycle test:

      1. Lists predefined IP-based apps via ``get_predefined_ip_based_apps``.
      2. Picks the first app returned and retrieves it by ID via
         ``get_predefined_ip_based_app``.

    Because both calls are read-only it is safe to run in CI/CD against
    shared tenants without mutating any configuration.
    """

    @pytest.mark.vcr()
    def test_predefined_ip_based_apps(self, fs):
        client = MockZCCClient(fs)
        errors = []

        target = None
        target_app_id = None

        try:
            apps, _, err = client.zcc.predefined_ip_based_apps.get_predefined_ip_based_apps()
            assert err is None, f"Error listing predefined IP-based apps: {err}"
            assert isinstance(apps, list), "Expected a list of predefined IP-based apps"
            assert apps, "Expected at least one predefined IP-based app in the tenant"

            target = apps[0]
            assert hasattr(target, "as_dict"), "Predefined IP-based app should expose as_dict()"
            assert getattr(target, "id", None), "First predefined IP-based app is missing an ID"
            assert getattr(target, "app_name", None), "Expected non-empty app_name on first predefined IP-based app"

            target_app_id = str(target.id)
        except Exception as exc:
            errors.append(f"Listing predefined IP-based apps failed: {exc}")

        try:
            if target_app_id:
                fetched, _, err = client.zcc.predefined_ip_based_apps.get_predefined_ip_based_app(target_app_id)
                assert err is None, f"Error fetching predefined IP-based app {target_app_id}: {err}"
                assert fetched is not None, f"Expected an app for ID {target_app_id}"
                assert str(fetched.id) == target_app_id, f"Expected ID {target_app_id}, got {fetched.id}"
                assert getattr(fetched, "app_name", None), "Expected non-empty app_name on fetched app"
                # The Go test asserts a non-empty UID for the predefined IP app payload.
                assert getattr(fetched, "uid", None), "Expected non-empty uid on fetched app"
        except Exception as exc:
            errors.append(f"Predefined IP-based app operation failed: {exc}")

        assert len(errors) == 0, "Errors occurred during the predefined IP-based apps lifecycle test:\n" + "\n".join(errors)
