"""
Unit tests for zscaler.utils.transform_common_id_fields.

These tests pin the request/response asymmetry between ZIA/ZTW (which require
integer IDs on the wire) and ZPA (which uses 19-digit string IDs that must
not be coerced to int).
"""

import pytest

from zscaler.utils import transform_common_id_fields

# ---------------------------------------------------------------------------
# Default (coerce_ids=True): ZIA / ZTW behavior
# ---------------------------------------------------------------------------


class TestTransformCommonIdFieldsCoerce:
    """Default mode: numeric-looking strings get coerced to int (ZIA/ZTW)."""

    def test_list_of_string_ids_coerced_to_int(self):
        body = {"groups": ["123", "456"]}
        transform_common_id_fields([("groups", "groups")], body, body)
        assert body == {"groups": [{"id": 123}, {"id": 456}]}

    def test_list_of_int_ids_pass_through(self):
        body = {"groups": [123, 456]}
        transform_common_id_fields([("groups", "groups")], body, body)
        assert body == {"groups": [{"id": 123}, {"id": 456}]}

    def test_list_of_dicts_coerced_to_int(self):
        body = {"groups": [{"id": "123"}, {"id": "456"}]}
        transform_common_id_fields([("groups", "groups")], body, body)
        assert body == {"groups": [{"id": 123}, {"id": 456}]}

    def test_non_numeric_string_ids_preserved(self):
        body = {"groups": ["alpha", "beta"]}
        transform_common_id_fields([("groups", "groups")], body, body)
        assert body == {"groups": [{"id": "alpha"}, {"id": "beta"}]}

    def test_snake_to_wire_remap(self):
        body = {"group_ids": ["1", "2"]}
        transform_common_id_fields([("group_ids", "groups")], body, body)
        assert "group_ids" not in body
        assert body == {"groups": [{"id": 1}, {"id": 2}]}

    def test_missing_key_is_noop(self):
        body = {"name": "rule"}
        transform_common_id_fields([("group_ids", "groups")], body, body)
        assert body == {"name": "rule"}

    def test_single_dict_value_coerced(self):
        body = {"location": {"id": "789"}}
        transform_common_id_fields([("location", "location")], body, body)
        assert body == {"location": {"id": 789}}


# ---------------------------------------------------------------------------
# coerce_ids=False: ZPA behavior
# ---------------------------------------------------------------------------


class TestTransformCommonIdFieldsPreserve:
    """ZPA mode: string IDs are preserved verbatim (19-digit bigints)."""

    ZPA_ID_A = "216196257331405454"
    ZPA_ID_B = "216196257331405455"

    def test_zpa_string_ids_preserved_in_list(self):
        body = {"server_group_ids": [self.ZPA_ID_A, self.ZPA_ID_B]}
        transform_common_id_fields([("server_group_ids", "serverGroups")], body, body, coerce_ids=False)
        assert body == {"serverGroups": [{"id": self.ZPA_ID_A}, {"id": self.ZPA_ID_B}]}

    def test_zpa_dict_form_preserved(self):
        body = {"server_group_ids": [{"id": self.ZPA_ID_A}]}
        transform_common_id_fields([("server_group_ids", "serverGroups")], body, body, coerce_ids=False)
        assert body == {"serverGroups": [{"id": self.ZPA_ID_A}]}

    def test_zpa_int_ids_pass_through_unchanged(self):
        body = {"server_group_ids": [42]}
        transform_common_id_fields([("server_group_ids", "serverGroups")], body, body, coerce_ids=False)
        assert body == {"serverGroups": [{"id": 42}]}

    def test_zpa_string_id_not_corrupted_to_float_or_int(self):
        """Regression guard: 19-digit IDs must stay string under coerce_ids=False."""
        body = {"server_group_ids": [self.ZPA_ID_A]}
        transform_common_id_fields([("server_group_ids", "serverGroups")], body, body, coerce_ids=False)
        emitted = body["serverGroups"][0]["id"]
        assert isinstance(emitted, str)
        assert emitted == self.ZPA_ID_A

    def test_default_param_matches_zia_ztw_callers(self):
        """Sanity: omitting coerce_ids must equal coerce_ids=True (no behaviour drift)."""
        body_default = {"groups": ["123"]}
        body_explicit = {"groups": ["123"]}
        transform_common_id_fields([("groups", "groups")], body_default, body_default)
        transform_common_id_fields([("groups", "groups")], body_explicit, body_explicit, coerce_ids=True)
        assert body_default == body_explicit == {"groups": [{"id": 123}]}


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
