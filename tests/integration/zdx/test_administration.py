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

    def test_list_departments(self, fs):
        client = MockZDXClient(fs)
        errors = []

        try:
            departments_iterator = client.zdx.admin.list_departments(query_params={"since": 2})
            departments = list(departments_iterator)

            if not departments:
                print("No departments found within the specified time range.")
            else:
                print(f"Retrieved {len(departments)} departments")
                for department in departments:
                    pprint(department)
        except Exception as e:
            errors.append(f"Exception occurred: {e}")

        assert not errors, "Errors occurred:\n{}".format("\n".join(errors))

    def test_list_locations(self, fs):
        client = MockZDXClient(fs)
        errors = []

        try:
            locations_iterator = client.zdx.admin.list_locations(query_params={"since": 2})
            locations = list(locations_iterator)

            if not locations:
                print("No locations found within the specified time range.")
            else:
                print(f"Retrieved {len(locations)} locations")
                for location in locations:
                    pprint(location)
        except Exception as e:
            errors.append(f"Exception occurred: {e}")

        assert not errors, "Errors occurred:\n{}".format("\n".join(errors))
