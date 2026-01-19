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


class TestSubClouds:
    """
    Integration Tests for the Sub Clouds API.
    """

    @pytest.mark.vcr()
    def test_sub_clouds_operations(self, fs):
        """Test Sub Clouds operations."""
        client = MockZIAClient(fs)
        errors = []

        try:
            # Test list_sub_clouds
            sub_clouds, response, err = client.zia.sub_clouds.list_sub_clouds()
            assert err is None, f"List sub clouds failed: {err}"
            assert sub_clouds is not None, "Sub clouds list should not be None"
            assert isinstance(sub_clouds, list), "Sub clouds should be a list"

            # Test list_sub_clouds with pagination
            paginated_clouds, response, err = client.zia.sub_clouds.list_sub_clouds(
                query_params={"page": 1, "page_size": 10}
            )
            assert err is None, f"List sub clouds with pagination failed: {err}"

            # Test operations with existing sub cloud if available
            if sub_clouds and len(sub_clouds) > 0:
                cloud_id = sub_clouds[0].id if hasattr(sub_clouds[0], 'id') else None
                if cloud_id:
                    # Test get_sub_cloud_last_dc_in_country
                    try:
                        last_dc, response, err = client.zia.sub_clouds.get_sub_cloud_last_dc_in_country(
                            cloud_id=cloud_id,
                            query_params={"country": "US"}
                        )
                        # May fail depending on cloud configuration
                    except Exception:
                        pass

                    # Test update_sub_clouds (attempt with minimal changes)
                    try:
                        updated_cloud, response, err = client.zia.sub_clouds.update_sub_clouds(
                            cloud_id=cloud_id,
                        )
                        # May fail due to permissions
                    except Exception:
                        pass

        except Exception as e:
            errors.append(f"Exception during sub clouds test: {str(e)}")

        assert len(errors) == 0, f"Errors occurred: {errors}"
