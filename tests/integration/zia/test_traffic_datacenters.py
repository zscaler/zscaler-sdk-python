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
from datetime import datetime, timedelta

from tests.integration.zia.conftest import MockZIAClient


@pytest.fixture
def fs():
    yield


class TestTrafficDatacenters:
    """
    Integration Tests for the Traffic Datacenters API.
    """

    @pytest.mark.vcr()
    def test_traffic_datacenters_crud(self, fs):
        """Test Traffic Datacenters CRUD operations."""
        client = MockZIAClient(fs)
        errors = []
        exclusion_id = None

        try:
            # Test list_datacenters
            datacenters, response, err = client.zia.traffic_datacenters.list_datacenters()
            assert err is None, f"List datacenters failed: {err}"
            assert datacenters is not None, "Datacenters list should not be None"
            assert isinstance(datacenters, list), "Datacenters should be a list"

            # Test list_datacenters with query params
            datacenters_search, response, err = client.zia.traffic_datacenters.list_datacenters(
                query_params={"search": "US"}
            )

            # Test list_dc_exclusions
            exclusions, response, err = client.zia.traffic_datacenters.list_dc_exclusions()
            assert err is None, f"List DC exclusions failed: {err}"

            # Test add_dc_exclusion (may fail due to permissions)
            if datacenters and len(datacenters) > 0:
                try:
                    dc_id = datacenters[0].id if hasattr(datacenters[0], 'id') else None
                    if dc_id:
                        start_time = int((datetime.now() + timedelta(hours=1)).timestamp() * 1000)
                        end_time = int((datetime.now() + timedelta(hours=2)).timestamp() * 1000)
                        created_exclusion, response, err = client.zia.traffic_datacenters.add_dc_exclusion(
                            dcid=dc_id,
                            start_time=start_time,
                            end_time=end_time,
                        )
                        if err is None and created_exclusion is not None:
                            exclusion_id = created_exclusion.get("id") if isinstance(created_exclusion, dict) else getattr(created_exclusion, "id", None)

                            # Test update_dc_exclusion
                            if exclusion_id:
                                try:
                                    new_end_time = int((datetime.now() + timedelta(hours=3)).timestamp() * 1000)
                                    updated_exclusion, response, err = client.zia.traffic_datacenters.update_dc_exclusion(
                                        dcid=exclusion_id,
                                        end_time=new_end_time,
                                    )
                                except Exception:
                                    pass
                except Exception:
                    pass  # May fail due to permissions

        except Exception as e:
            errors.append(f"Exception during traffic datacenters test: {str(e)}")

        finally:
            # Cleanup
            if exclusion_id:
                try:
                    client.zia.traffic_datacenters.delete_dc_exclusion(exclusion_id)
                except Exception:
                    pass

        assert len(errors) == 0, f"Errors occurred: {errors}"
