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


class TestDLPIcapServer:
    """
    Integration Tests for the DLP Icap Server
    """

    def test_dlp_icap_server(self, fs):
        client = MockZIAClient(fs)
        errors = []  # Initialize an empty list to collect errors

        try:
            # List all icaps
            icaps = client.dlp.list_dlp_icap_servers()
            assert isinstance(icaps, list), "Expected a list of icaps"
            if icaps:  # If there are any icaps
                # Select the first icap for further testing
                first_icap = icaps[0]
                icap_server_id = first_icap.get("id")

                # Fetch the selected icap by its ID
                try:
                    fetched_icap = client.dlp.get_dlp_icap_servers(icap_server_id)
                    assert fetched_icap is not None, "Expected a valid icap object"
                    assert fetched_icap.get("id") == icap_server_id, "Mismatch in icap ID"
                except Exception as exc:
                    errors.append(f"Fetching icap by ID failed: {exc}")

                # Attempt to retrieve the icap by name
                try:
                    icap_name = first_icap.get("name")
                    icap_by_name = client.dlp.get_dlp_icap_by_name(icap_name)
                    assert icap_by_name is not None, "Expected a valid icap object when searching by name"
                    assert icap_by_name.get("id") == icap_server_id, "Mismatch in icap ID when searching by name"
                except Exception as exc:
                    errors.append(f"Fetching icap by name failed: {exc}")

        except Exception as exc:
            errors.append(f"Listing icaps failed: {exc}")

        # Assert that no errors occurred during the test
        assert len(errors) == 0, f"Errors occurred during icaps test: {errors}"
