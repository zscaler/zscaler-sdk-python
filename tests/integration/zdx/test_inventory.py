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
import time
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
            # time.sleep(5)  # Sleep for 5 seconds before making the request
            # now = int(time.time())
            # from_time = now - 2 * 60 * 60  # 2 hours ago
            # to_time = now

            # kwargs = {
            #     "from_time": from_time,
            #     "to": to_time,
            # }

            software_iterator = client.inventory.list_softwares()
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
            # time.sleep(5)  # Sleep for 5 seconds before making the request
            # now = int(time.time())
            # from_time = now - 2 * 60 * 60  # 2 hours ago
            # to_time = now

            # kwargs = {
            #     "from_time": from_time,
            #     "to": to_time,
            # }

            # List software to get a software key
            software_iterator = client.inventory.list_softwares()
            softwares = list(software_iterator)

            if not softwares:
                print("No software found within the specified time range.")
            else:
                software_key = softwares[0].software_key
                print(f"Using software key {software_key} for list_software_keys test")

                # List software keys using the retrieved software key
                software_keys_iterator = client.inventory.list_software_keys(software_key=software_key)
                software_keys = list(software_keys_iterator)

                if not software_keys:
                    print("No software keys found within the specified time range.")
                else:
                    print(f"Retrieved {len(software_keys)} software keys")
                    for software_key in software_keys:
                        pprint(software_key)
        except Exception as e:
            errors.append(f"Exception occurred: {e}")

        assert not errors, "Errors occurred:\n{}".format("\n".join(errors))
