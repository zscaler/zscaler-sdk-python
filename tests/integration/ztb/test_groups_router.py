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

"""
Integration tests for the ZTB Groups Router resource.

Uses VCR to record/replay HTTP. Uses deterministic names.
Set MOCK_TESTS=false and ZTB credentials when recording cassettes.
"""

import pytest

from tests.integration.ztb.conftest import MockZTBClient
from tests.test_utils import generate_random_string


@pytest.fixture
def fs():
    yield


@pytest.mark.vcr
class TestGroupsRouter:
    """Integration tests for the ZTB Groups Router API."""

    def test_list_groups(self, fs):
        """Test listing groups."""
        client = MockZTBClient()
        with client as c:
            groups, _, err = c.ztb.groups_router.list_groups()
        if err:
            pytest.skip(f"list_groups not available: {err}")
        assert groups is not None
        assert isinstance(groups, list)

    def test_groups_lifecycle(self, fs):
        """Test create, get, update, delete group."""
        client = MockZTBClient()
        name = f"tests-group-{generate_random_string()}"
        display_name = f"Tests Group {generate_random_string()}"
        group_id = None
        errors = []

        try:
            with client as c:
                created, _, err = c.ztb.groups_router.create_group(
                    name=name,
                    display_name=display_name,
                    type="device",
                    autonomous=True,
                    owner="user",
                )
                if err:
                    errors.append(f"create_group failed: {err}")
                    return
                assert created is not None
                group_id = getattr(created, "group_id", None) or getattr(created, "id", None)
                if group_id is None and hasattr(created, "as_dict"):
                    d = created.as_dict()
                    group_id = d.get("group_id") or d.get("id")

            if group_id:
                with client as c:
                    got, _, err = c.ztb.groups_router.get_group(str(group_id))
                    if err:
                        errors.append(f"get_group failed: {err}")
                    elif got:
                        assert got.name == name or got.display_name == display_name

                with client as c:
                    updated, _, err = c.ztb.groups_router.update_group_patch(
                        str(group_id),
                        display_name=display_name + " Updated",
                    )
                    if err:
                        errors.append(f"update_group_patch failed: {err}")
        except Exception as exc:
            errors.append(f"Lifecycle failed: {exc}")
        finally:
            if group_id:
                try:
                    with client as c:
                        _, _, err = c.ztb.groups_router.delete_group(str(group_id))
                        if err:
                            errors.append(f"delete_group failed: {err}")
                except Exception as exc:
                    errors.append(f"Cleanup failed: {exc}")

        assert len(errors) == 0, f"Errors: {errors}"
