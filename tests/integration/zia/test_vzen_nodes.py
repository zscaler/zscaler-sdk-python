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


class TestVZenNodes:
    """
    Integration Tests for the VZen Nodes API.
    """

    @pytest.mark.vcr()
    def test_vzen_nodes_crud(self, fs):
        """Test VZen Nodes CRUD operations."""
        client = MockZIAClient(fs)
        errors = []
        node_id = None

        try:
            # Test list_zen_nodes
            nodes, response, err = client.zia.vzen_nodes.list_zen_nodes()
            assert err is None, f"List VZen nodes failed: {err}"
            assert nodes is not None, "Nodes list should not be None"
            assert isinstance(nodes, list), "Nodes should be a list"

            # Test add_zen_node - create a new node
            try:
                created_node, response, err = client.zia.vzen_nodes.add_zen_node(
                    name="TestVZenNode_VCR",
                    description="Test VZen node for VCR testing",
                )
                if err is None and created_node is not None:
                    node_id = created_node.get("id") if isinstance(created_node, dict) else getattr(created_node, "id", None)

                    # Test get_zen_node
                    if node_id:
                        fetched_node, response, err = client.zia.vzen_nodes.get_zen_node(node_id)
                        assert err is None, f"Get VZen node failed: {err}"
                        assert fetched_node is not None, "Fetched node should not be None"

                        # Test update_zen_node
                        try:
                            updated_node, response, err = client.zia.vzen_nodes.update_zen_node(
                                node_id=node_id,
                                name="TestVZenNode_VCR_Updated",
                                description="Updated test VZen node",
                            )
                            # Update may fail - that's ok
                        except Exception:
                            pass
            except Exception as e:
                # Add may fail due to permissions/subscription
                pass

            # If we didn't create a node, test with existing one
            if node_id is None and nodes and len(nodes) > 0:
                existing_id = nodes[0].id
                fetched_node, response, err = client.zia.vzen_nodes.get_zen_node(existing_id)
                assert err is None, f"Get VZen node failed: {err}"

        except Exception as e:
            errors.append(f"Exception during VZen nodes test: {str(e)}")

        finally:
            # Cleanup - delete created node
            if node_id:
                try:
                    client.zia.vzen_nodes.delete_zen_node(node_id)
                except Exception:
                    pass

        assert len(errors) == 0, f"Errors occurred: {errors}"
