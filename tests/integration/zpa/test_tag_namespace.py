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

from tests.integration.zpa.conftest import MockZPAClient
from tests.test_utils import generate_random_string
from zscaler.zpa.models.tag_namespace import Namespace, UpdateStatusRequest


@pytest.fixture
def fs():
    yield


class TestTagNamespace:
    """
    Integration Tests for the Tag Namespace resource.

    These tests use VCR to record and replay HTTP interactions.
    """

    @pytest.mark.vcr()
    def test_tag_namespace_lifecycle(self, fs):
        client = MockZPAClient(fs)
        errors = []

        namespace_name = "tests-ns-" + generate_random_string()
        namespace_description = "tests-ns-" + generate_random_string()
        namespace_id = None

        try:
            # Create a tag namespace
            namespace = Namespace(
                {
                    "name": namespace_name,
                    "description": namespace_description,
                    "enabled": True,
                    "origin": "CUSTOM",
                    "type": "STATIC",
                }
            )
            created_ns, _, err = client.zpa.tag_namespace.create_namespace(namespace)
            assert err is None, f"Error creating namespace: {err}"
            assert created_ns is not None
            assert created_ns.name == namespace_name
            assert created_ns.description == namespace_description
            assert created_ns.enabled is True

            namespace_id = created_ns.id
        except Exception as exc:
            errors.append(f"Error during namespace creation: {exc}")

        try:
            if namespace_id:
                # Get by ID
                retrieved_ns, _, err = client.zpa.tag_namespace.get_namespace(namespace_id)
                assert err is None, f"Error fetching namespace: {err}"
                assert retrieved_ns.id == namespace_id
                assert retrieved_ns.name == namespace_name

                # Update
                updated_name = namespace_name + " Updated"
                updated_ns = Namespace(
                    {
                        "id": namespace_id,
                        "name": updated_name,
                        "description": namespace_description,
                        "enabled": True,
                        "origin": "CUSTOM",
                        "type": "STATIC",
                    }
                )
                _, _, err = client.zpa.tag_namespace.update_namespace(namespace_id, updated_ns)
                assert err is None, f"Error updating namespace: {err}"

                # Get by name
                got_by_name, _, err = client.zpa.tag_namespace.get_namespace_by_name(updated_name)
                assert err is None, f"Error fetching namespace by name: {err}"
                assert got_by_name.id == namespace_id
                assert got_by_name.name == updated_name

                # Update status (optional - may fail on some API versions)
                status_req = UpdateStatusRequest({"enabled": False})
                _, _, status_err = client.zpa.tag_namespace.update_namespace_status(namespace_id, status_req)
                if status_err and "resource.not.found" not in str(status_err):
                    errors.append(f"Update status failed: {status_err}")

                # List namespaces
                namespaces_list, _, err = client.zpa.tag_namespace.list_namespaces()
                assert err is None, f"Error listing namespaces: {err}"
                assert any(ns.id == namespace_id for ns in namespaces_list)
        except Exception as exc:
            errors.append(f"Tag namespace operation failed: {exc}")

        finally:
            if namespace_id:
                try:
                    _, _, err = client.zpa.tag_namespace.delete_namespace(namespace_id)
                    assert err is None, f"Error deleting namespace: {err}"
                except Exception as cleanup_exc:
                    errors.append(f"Cleanup failed for namespace ID {namespace_id}: {cleanup_exc}")

        assert len(errors) == 0, f"Errors occurred during the tag namespace lifecycle test: {errors}"
