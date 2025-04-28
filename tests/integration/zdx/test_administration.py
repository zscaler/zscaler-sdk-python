"""
Copyright (c) 2023, Zscaler Inc.

Permission to use, copy, modify, and/or distribute this software for any
purpose with or without fee is hereby granted, provided that the above
copyright notice and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
"""

import pytest
import time
from pprint import pprint
from tests.integration.zdx.conftest import MockZDXClient


@pytest.fixture
def fs():
    yield


class TestAdministration:
    """
    Integration Tests for the administration
    """

    def test_list_departments(self, fs, zdx_client):
        client = zdx_client
        errors = []

        try:
            departments, _, err = client.zdx.admin.list_departments(query_params={"since": 2})
            assert err is None, f"Error listing departments: {err}"
            assert isinstance(departments, list), "Expected departments to be a list"

            if not departments:
                print("No departments found within the specified time range.")
            else:
                print(f"Retrieved {len(departments)} departments")
                for department in departments:
                    pprint(department.as_dict())
        except Exception as e:
            errors.append(f"Exception occurred in departments: {e}")

        assert not errors, "Errors occurred:\n{}".format("\n".join(errors))

    def test_list_locations(self, fs, zdx_client):
        client = zdx_client
        errors = []

        try:
            locations, _, err = client.zdx.admin.list_locations(query_params={"since": 2})
            assert err is None, f"Error listing locations: {err}"
            assert isinstance(locations, list), "Expected locations to be a list"

            if not locations:
                print("No locations found within the specified time range.")
            else:
                print(f"Retrieved {len(locations)} locations")
                for location in locations:
                    pprint(location.as_dict())
        except Exception as e:
            errors.append(f"Exception occurred in locations: {e}")

        assert not errors, "Errors occurred:\n{}".format("\n".join(errors))
