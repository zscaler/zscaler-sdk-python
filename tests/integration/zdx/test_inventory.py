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
from pprint import pprint
from tests.integration.zdx.conftest import MockZDXClient


@pytest.fixture
def fs():
    yield


class TestInventory:
    """
    Integration Tests for the inventory
    """

    def test_list_softwares(self, fs):
        client = MockZDXClient(fs)
        errors = []

        try:
            software_iterator = client.zdx.inventory.list_softwares()
            softwares = list(software_iterator)

            if not softwares:
                print("No software found within the specified time range.")
            else:
                print(f"Retrieved {len(softwares)} software")
                for software in softwares:
                    pprint(software)
        except Exception as e:
            errors.append(f"Exception occurred: {e}")

        assert not errors, "Errors occurred:\n{}".format("\n".join(errors))

    def test_list_software_keys(self, fs):
        client = MockZDXClient(fs)
        errors = []

        try:
            # List software to get a software key
            software_list, _, error = client.zdx.inventory.list_softwares()
            if error:
                errors.append(f"Error listing software list: {error}")
                return

            if not software_list or not isinstance(software_list, list):
                print("No software found within the specified time range.")
                return

            # Retrieve the first software object and extract its software_key attribute
            first_soft = software_list[0]
            software_key = getattr(first_soft, "software_key", None)

            if not software_key:
                raise ValueError(f"Software key not found in response: {first_soft.as_dict()}")

            print(f"Using Software Key: {software_key}")

            # List software keys using the retrieved software key
            software_keys_iterator = client.zdx.inventory.list_software_keys(software_key=software_key)
            software_keys = list(software_keys_iterator)

            if not software_keys:
                print("No software keys found within the specified time range.")
            else:
                print(f"Retrieved {len(software_keys)} software keys")
                for key in software_keys:
                    pprint(key)
        except Exception as e:
            errors.append(f"Exception occurred: {e}")

        assert not errors, "Errors occurred:\n{}".format("\n".join(errors))
