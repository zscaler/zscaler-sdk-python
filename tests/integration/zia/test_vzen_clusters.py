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
import random


@pytest.fixture
def fs():
    yield


class TestVZENClusters:
    """
    Integration Tests for the Virtual Service Edge
    """

    def test_vzen_clusters(self, fs):
        client = MockZIAClient(fs)
        errors = []
        cluster_id = None
        update_cluster = None

        try:
            try:
                create_cluster, _, error = client.zia.vzen_clusters.add_vzen_cluster(
                    name=f"testsAddVZEN{random.randint(1000, 10000)}", 
                    enabled=True,
                    type='VIP',
                    ip_address='192.168.90.7',
                    subnet_mask='255.255.255.0',
                    default_gateway='192.168.90.254',
                    ip_sec_enabled=False,
                )
                assert error is None, f"Add Cluster Error: {error}"
                assert create_cluster is not None, "Cluster creation failed."
                cluster_id = create_cluster.id
            except Exception as e:
                errors.append(f"Exception during add_vzen_cluster: {str(e)}")

            try:
                if cluster_id:
                    update_cluster, _, error = client.zia.vzen_clusters.update_vzen_cluster(
                        cluster_id=cluster_id,
                        name=f"testsUpdateVZEN{random.randint(1000, 10000)}",
                        enabled=True,
                        type='VIP',
                        ip_address='192.168.90.7',
                        subnet_mask='255.255.255.0',
                        default_gateway='192.168.90.254',
                        ip_sec_enabled=False,
                    )
                    assert error is None, f"Update Cluster Error: {error}"
                    assert update_cluster is not None, "Cluster update returned None."
            except Exception as e:
                errors.append(f"Exception during update_vzen_cluster: {str(e)}")

            try:
                if update_cluster:
                    cluster, _, error = client.zia.vzen_clusters.get_vzen_cluster(update_cluster.id)
                    assert error is None, f"Get Cluster Error: {error}"
                    assert cluster.id == cluster_id, "Retrieved cluster ID mismatch."
            except Exception as e:
                errors.append(f"Exception during get_vzen_cluster: {str(e)}")

            try:
                if update_cluster:
                    clusters, _, error = client.zia.vzen_clusters.list_vzen_clusters(query_params={"search": update_cluster.name})
                    assert error is None, f"List clusters Error: {error}"
                    assert clusters is not None and isinstance(clusters, list), "No clusters found or invalid format."
            except Exception as e:
                errors.append(f"Exception during list_vzen_clusters: {str(e)}")

        finally:
            try:
                if update_cluster:
                    _, _, error = client.zia.vzen_clusters.delete_vzen_cluster(update_cluster.id)
                    assert error is None, f"Delete Cluster Error: {error}"
            except Exception as e:
                errors.append(f"Exception during delete_vzen_cluster: {str(e)}")

        if errors:
            raise AssertionError(f"Integration Test Errors:\n{chr(10).join(errors)}")
