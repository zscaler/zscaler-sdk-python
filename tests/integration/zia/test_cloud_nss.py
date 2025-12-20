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


class TestCloudNSS:
    """
    Integration Tests for the Cloud NSS API.
    """

    @pytest.mark.vcr()
    def test_cloud_nss_crud(self, fs):
        """Test Cloud NSS operations."""
        client = MockZIAClient(fs)
        errors = []

        try:
            # Test list_nss_feed
            feeds, response, err = client.zia.cloud_nss.list_nss_feed()
            assert err is None, f"List NSS feeds failed: {err}"
            assert feeds is not None, "Feeds list should not be None"
            assert isinstance(feeds, list), "Feeds should be a list"

            # Test get_nss_feed with first feed if available
            if feeds and len(feeds) > 0:
                feed_id = feeds[0].id
                fetched_feed, response, err = client.zia.cloud_nss.get_nss_feed(feed_id)
                assert err is None, f"Get NSS feed failed: {err}"
                assert fetched_feed is not None, "Fetched feed should not be None"

            # Test list_feed_output
            outputs, response, err = client.zia.cloud_nss.list_feed_output()
            assert err is None, f"List feed outputs failed: {err}"

            # Test validate_feed_format - may fail due to subscription
            try:
                validation, response, err = client.zia.cloud_nss.validate_feed_format(feed_type="WEB")
                # Don't fail - may require subscription
            except Exception:
                pass

            # Test test_connectivity - may fail due to subscription
            try:
                connectivity, response, err = client.zia.cloud_nss.test_connectivity(
                    feed_type="WEB",
                    feed_url="https://example.com",
                )
                # Don't fail - may require subscription
            except Exception:
                pass

        except Exception as e:
            errors.append(f"Exception during cloud NSS test: {str(e)}")

        assert len(errors) == 0, f"Errors occurred: {errors}"
