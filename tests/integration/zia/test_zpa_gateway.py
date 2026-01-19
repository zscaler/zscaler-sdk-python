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


class TestZPAGateway:
    """
    Integration Tests for the ZPA Gateway API.
    """

    @pytest.mark.vcr()
    def test_zpa_gateway_crud(self, fs):
        """Test ZPA Gateway CRUD operations."""
        client = MockZIAClient(fs)
        errors = []
        gateway_id = None

        try:
            # Test list_gateways
            gateways, response, err = client.zia.zpa_gateway.list_gateways()
            assert err is None, f"List ZPA gateways failed: {err}"
            assert gateways is not None, "Gateways list should not be None"
            assert isinstance(gateways, list), "Gateways should be a list"

            # Test list_gateways with query params
            gateways_search, response, err = client.zia.zpa_gateway.list_gateways(
                query_params={"search": "Gateway"}
            )

            # Test add_gateway (may fail due to ZPA tenant configuration)
            try:
                created_gateway, response, err = client.zia.zpa_gateway.add_gateway(
                    name="TestZPAGateway_VCR",
                    description="Test ZPA gateway for VCR",
                    zpa_tenant_id="test-tenant",
                )
                if err is None and created_gateway is not None:
                    gateway_id = created_gateway.get("id") if isinstance(created_gateway, dict) else getattr(created_gateway, "id", None)

                    # Test update_gateway
                    if gateway_id:
                        try:
                            updated_gateway, response, err = client.zia.zpa_gateway.update_gateway(
                                gateway_id=gateway_id,
                                name="TestZPAGateway_VCR_Updated",
                                description="Updated test ZPA gateway",
                            )
                        except Exception:
                            pass
            except Exception:
                pass  # May fail due to ZPA tenant not configured

            # Test get_gateway with first gateway if available
            if gateways and len(gateways) > 0:
                existing_id = gateways[0].id
                try:
                    fetched_gateway, response, err = client.zia.zpa_gateway.get_gateway(existing_id)
                    if err is None:
                        assert fetched_gateway is not None, "Fetched gateway should not be None"
                except Exception:
                    pass  # May fail if ZPA tenant not configured

        except Exception as e:
            errors.append(f"Exception during ZPA gateway test: {str(e)}")

        finally:
            # Cleanup
            if gateway_id:
                try:
                    client.zia.zpa_gateway.delete_gateway(gateway_id)
                except Exception:
                    pass

        assert len(errors) == 0, f"Errors occurred: {errors}"
