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
from tests.integration.zcon.conftest import MockZCONClient
from tests.test_utils import generate_random_string


@pytest.fixture
def fs():
    yield


class TestProvisioningUrl:
    """
    Integration Tests for the ZIA Provisioning URLs
    """

    def test_provisioning(self, fs):
        client = MockZCONClient(fs)
        errors = []
        provision_id = None

        try:
            # Test list_provisioning_url function
            try:
                urls = client.provisioning.list_provisioning_url()
                assert isinstance(urls, list), "Expected a list of provisioning urls"
                assert len(urls) > 0, "Expected at least one provisioning url"
                provision_id = urls[0].get("id")
                assert provision_id is not None, "Expected the first provisioning url to have an ID"
            except Exception as exc:
                errors.append(f"Listing provisioning urls failed: {exc}")

            # Test get_location function using the provision_id from the previous step
            if provision_id:
                try:
                    provisioning_url_details = client.provisioning.get_provisioning_url(provision_id)
                    assert provisioning_url_details is not None, "Expected valid provisioning url details"
                    assert provisioning_url_details.get("id") == provision_id, "Mismatch in provisioning url ID"
                except Exception as exc:
                    errors.append(f"Fetching provisioning url by ID failed: {exc}")

        except Exception as exc:
            errors.append(f"Test Locations suite failed: {exc}")

        # Assert that no errors occurred during the test
        assert len(errors) == 0, f"Errors occurred during locations test: {errors}"
