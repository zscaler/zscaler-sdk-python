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

from tests.integration.zia.conftest import MockZIAClient


@pytest.fixture
def fs():
    yield


class TestDLPIcapServer:
    """
    Integration Tests for the DLP ICAP Server
    """

    @pytest.mark.vcr()
    def test_dlp_icap_server(self, fs):
        client = MockZIAClient(fs)
        errors = []

        try:
            # Step 1: List all ICAP servers
            icaps, _, error = client.zia.dlp_resources.list_dlp_icap_servers()
            assert error is None, f"List ICAP Servers Error: {error}"
            assert isinstance(icaps, list), "Expected a list of ICAPs"

            if icaps:
                # Step 2: Select first ICAP
                first_icap = icaps[0]
                icap_server_id = first_icap.id  # ✅ FIXED: access via model

                # Step 3: Fetch by ID
                try:
                    fetched_icap, _, error = client.zia.dlp_resources.get_dlp_icap_servers(icap_server_id)
                    assert error is None, f"Get ICAP Server Error: {error}"
                    assert fetched_icap is not None, "Expected a valid ICAP object"
                    assert fetched_icap.id == icap_server_id, "Mismatch in ICAP ID"
                except Exception as exc:
                    errors.append(f"Fetching ICAP by ID failed: {exc}")

        except Exception as exc:
            errors.append(f"Listing ICAPs failed: {exc}")

        # Final assertion
        if errors:
            raise AssertionError(f"Integration Test Errors:\n{chr(10).join(errors)}")
