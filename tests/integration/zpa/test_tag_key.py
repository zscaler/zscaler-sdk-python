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

# import pytest

# from tests.integration.zpa.conftest import MockZPAClient
# from tests.test_utils import generate_random_string
# from zscaler.zpa.models.tag_namespace import Namespace
# from zscaler.zpa.models.tag_key import TagKey, TagValue, BulkUpdateStatusRequest


# @pytest.fixture
# def fs():
#     yield


# class TestTagKey:
#     """
#     Integration Tests for the Tag Key resource.

#     Tag keys are scoped to a namespace. These tests create a namespace first,
#     then exercise tag key CRUD. They use VCR to record and replay HTTP interactions.
#     """

#     @pytest.mark.vcr()
#     def test_tag_key_lifecycle(self, fs):
#         client = MockZPAClient(fs)
#         errors = []

#         namespace_name = "tests-ns-" + generate_random_string()
#         tag_key_name = "tests-tk-" + generate_random_string()
#         tag_val1 = "val-" + generate_random_string()
#         tag_val2 = "val-" + generate_random_string()
#         namespace_id = None
#         tag_key_id = None

#         try:
#             # Create namespace first (tag keys live within a namespace)
#             namespace = Namespace(
#                 {
#                     "name": namespace_name,
#                     "description": namespace_name,
#                     "enabled": True,
#                     "origin": "CUSTOM",
#                     "type": "STATIC",
#                 }
#             )
#             created_ns, _, err = client.zpa.tag_namespace.create_namespace(namespace)
#             assert err is None, f"Error creating namespace: {err}"
#             assert created_ns is not None
#             namespace_id = created_ns.id
#         except Exception as exc:
#             errors.append(f"Error creating namespace: {exc}")

#         try:
#             if namespace_id:
#                 # Create tag key with tag values
#                 tag_key = TagKey(
#                     {
#                         "name": tag_key_name,
#                         "description": tag_key_name,
#                         "enabled": True,
#                         "origin": "CUSTOM",
#                         "type": "STATIC",
#                         "tagValues": [
#                             {"name": tag_val1},
#                             {"name": tag_val2},
#                         ],
#                     }
#                 )
#                 created_key, _, err = client.zpa.tag_key.create_tag_key(namespace_id, tag_key)
#                 assert err is None, f"Error creating tag key: {err}"
#                 assert created_key is not None
#                 assert created_key.name == tag_key_name
#                 assert created_key.enabled is True

#                 tag_key_id = created_key.id
#         except Exception as exc:
#             errors.append(f"Error creating tag key: {exc}")

#         try:
#             if namespace_id and tag_key_id:
#                 # Get by ID
#                 retrieved_key, _, err = client.zpa.tag_key.get_tag_key(namespace_id, tag_key_id)
#                 assert err is None, f"Error fetching tag key: {err}"
#                 assert retrieved_key.id == tag_key_id
#                 assert retrieved_key.name == tag_key_name

#                 # Update
#                 updated_name = tag_key_name + " Updated"
#                 updated_key = TagKey(
#                     {
#                         "id": tag_key_id,
#                         "name": updated_name,
#                         "description": tag_key_name,
#                         "enabled": True,
#                         "origin": "CUSTOM",
#                         "type": "STATIC",
#                         "tagValues": [{"name": tag_val1}, {"name": tag_val2}],
#                     }
#                 )
#                 _, _, err = client.zpa.tag_key.update_tag_key(namespace_id, tag_key_id, updated_key)
#                 assert err is None, f"Error updating tag key: {err}"

#                 # Get by name
#                 got_by_name, _, err = client.zpa.tag_key.get_tag_key_by_name(namespace_id, updated_name)
#                 assert err is None, f"Error fetching tag key by name: {err}"
#                 assert got_by_name.id == tag_key_id
#                 assert got_by_name.name == updated_name

#                 # Bulk update status (optional)
#                 bulk_req = BulkUpdateStatusRequest(
#                     {
#                         "enabled": False,
#                         "tagKeyIds": [tag_key_id],
#                     }
#                 )
#                 _, _, bulk_err = client.zpa.tag_key.bulk_update_status(namespace_id, bulk_req)
#                 if bulk_err:
#                     errors.append(f"Bulk update status failed: {bulk_err}")

#                 # List tag keys
#                 keys_list, _, err = client.zpa.tag_key.list_tag_keys(namespace_id)
#                 assert err is None, f"Error listing tag keys: {err}"
#                 assert any(k.id == tag_key_id for k in keys_list)
#         except Exception as exc:
#             errors.append(f"Tag key operation failed: {exc}")

#         finally:
#             if namespace_id and tag_key_id:
#                 try:
#                     _, _, err = client.zpa.tag_key.delete_tag_key(namespace_id, tag_key_id)
#                     assert err is None, f"Error deleting tag key: {err}"
#                 except Exception as cleanup_exc:
#                     errors.append(f"Cleanup failed for tag key: {cleanup_exc}")
#             if namespace_id:
#                 try:
#                     _, _, err = client.zpa.tag_namespace.delete_namespace(namespace_id)
#                     assert err is None, f"Error deleting namespace: {err}"
#                 except Exception as cleanup_exc:
#                     errors.append(f"Cleanup failed for namespace: {cleanup_exc}")

#         assert len(errors) == 0, f"Errors occurred during the tag key lifecycle test: {errors}"
