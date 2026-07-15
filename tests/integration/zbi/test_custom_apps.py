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


@pytest.fixture
def fs():
    yield


class TestCustomApps:
    """Integration tests for ZBI Custom Applications API."""

    @pytest.mark.vcr()
    def test_custom_apps_lifecycle(self, zbi_client):
        client = zbi_client
        errors = []
        created_id = None

        try:
            # Create
            try:
                created, _, error = client.zbi.custom_apps.create_custom_app(
                    name="tests-zbi-custom-app",
                    description="Integration test custom app",
                    signatures=[
                        {
                            "type": "HOST",
                            "matchLevel": "EXACT",
                            "value": "test-zbi-app.example.com",
                        }
                    ],
                )
                assert error is None, f"Create error: {error}"
                assert created is not None, "Create returned None"
                created_id = created.id
            except Exception as e:
                errors.append(f"Create: {e}")

            # List
            try:
                apps, _, error = client.zbi.custom_apps.list_custom_apps()
                assert error is None, f"List error: {error}"
                assert isinstance(apps, list), "List did not return a list"
            except Exception as e:
                errors.append(f"List: {e}")

            # Get by ID
            try:
                if created_id:
                    app, _, error = client.zbi.custom_apps.get_custom_app(created_id)
                    assert error is None, f"Get error: {error}"
                    assert app is not None, "Get returned None"
                    assert app.id == created_id, "ID mismatch"
            except Exception as e:
                errors.append(f"Get: {e}")

            # Update
            try:
                if created_id:
                    updated, _, error = client.zbi.custom_apps.update_custom_app(
                        created_id,
                        name="tests-zbi-custom-app-updated",
                        description="Updated integration test",
                        signatures=[
                            {
                                "type": "HOST",
                                "matchLevel": "EXACT",
                                "value": "test-zbi-app.example.com",
                            },
                            {
                                "type": "HOST",
                                "matchLevel": "CONTAINS",
                                "value": "example.com",
                            },
                        ],
                    )
                    assert error is None, f"Update error: {error}"
                    assert updated is not None, "Update returned None"
            except Exception as e:
                errors.append(f"Update: {e}")

        finally:
            if created_id:
                _, _, err = client.zbi.custom_apps.delete_custom_app(created_id)
                if err:
                    errors.append(f"Cleanup delete: {err}")

        if errors:
            raise AssertionError("\n".join(errors))
