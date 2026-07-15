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


class TestReportConfigs:
    """Integration tests for ZBI Report Configurations API."""

    @pytest.mark.vcr()
    def test_report_configs_lifecycle(self, zbi_client):
        client = zbi_client
        errors = []
        created_id = None

        try:
            # Create
            try:
                created, _, error = client.zbi.report_configs.create_report_config(
                    name="tests-zbi-daily-report",
                    sub_type="USERS",
                    enabled=True,
                    custom_ids=[1],
                    delivery_information=[
                        {
                            "delivery_method": "EMAIL",
                            "emails": ["test@example.com"],
                        }
                    ],
                    schedule_params={
                        "timezone": "UTC",
                        "frequency": "DAILY",
                    },
                )
                assert error is None, f"Create error: {error}"
                assert created is not None, "Create returned None"
                created_id = created.id
            except Exception as e:
                errors.append(f"Create: {e}")

            # List
            try:
                configs, _, error = client.zbi.report_configs.list_report_configs()
                assert error is None, f"List error: {error}"
                assert isinstance(configs, list), "List did not return a list"
            except Exception as e:
                errors.append(f"List: {e}")

            # Get by ID
            try:
                if created_id:
                    cfg, _, error = client.zbi.report_configs.get_report_config(created_id)
                    assert error is None, f"Get error: {error}"
                    assert cfg is not None, "Get returned None"
                    assert cfg.id == created_id, "ID mismatch"
            except Exception as e:
                errors.append(f"Get: {e}")

            # Update
            try:
                if created_id:
                    updated, _, error = client.zbi.report_configs.update_report_config(
                        created_id,
                        name="tests-zbi-weekly-report",
                        sub_type="USERS",
                        enabled=True,
                        custom_ids=[1],
                        delivery_information=[
                            {
                                "delivery_method": "EMAIL",
                                "emails": ["test@example.com"],
                            }
                        ],
                        schedule_params={
                            "timezone": "UTC",
                            "frequency": "WEEKLY",
                            "weekday": "MON",
                        },
                    )
                    assert error is None, f"Update error: {error}"
                    assert updated is not None, "Update returned None"
            except Exception as e:
                errors.append(f"Update: {e}")

        finally:
            if created_id:
                _, _, err = client.zbi.report_configs.delete_report_config(created_id)
                if err:
                    errors.append(f"Cleanup delete: {err}")

        if errors:
            raise AssertionError("\n".join(errors))
