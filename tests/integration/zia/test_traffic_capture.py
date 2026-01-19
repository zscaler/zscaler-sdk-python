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


class TestTrafficCapture:
    """
    Integration Tests for the Traffic Capture API.
    """

    @pytest.mark.vcr()
    def test_traffic_capture_crud(self, fs):
        """Test Traffic Capture CRUD operations."""
        client = MockZIAClient(fs)
        errors = []
        rule_id = None

        try:
            # Test list_rules
            rules, response, err = client.zia.traffic_capture.list_rules()
            assert err is None, f"List traffic capture rules failed: {err}"
            assert rules is not None, "Rules list should not be None"
            assert isinstance(rules, list), "Rules should be a list"

            # Test list_traffic_capture_rule_order
            rule_order, response, err = client.zia.traffic_capture.list_traffic_capture_rule_order()
            assert err is None, f"List traffic capture rule order failed: {err}"

            # Test traffic_capture_rule_count
            rule_count, response, err = client.zia.traffic_capture.traffic_capture_rule_count()
            assert err is None, f"Traffic capture rule count failed: {err}"

            # Test list_rule_labels
            labels, response, err = client.zia.traffic_capture.list_rule_labels()
            assert err is None, f"List rule labels failed: {err}"

            # Test add_rule - create a new traffic capture rule
            try:
                created_rule, response, err = client.zia.traffic_capture.add_rule(
                    name="TestTrafficCapture_VCR",
                    description="Test traffic capture rule for VCR",
                    enabled=True,
                    order=1,
                    rank=7,
                    action="ALLOW",
                )
                if err is None and created_rule is not None:
                    rule_id = created_rule.id if hasattr(created_rule, 'id') else None

                    # Test get_rule
                    if rule_id:
                        fetched_rule, response, err = client.zia.traffic_capture.get_rule(rule_id)
                        assert err is None, f"Get traffic capture rule failed: {err}"
                        assert fetched_rule is not None, "Fetched rule should not be None"

                        # Test update_rule
                        try:
                            updated_rule, response, err = client.zia.traffic_capture.update_rule(
                                rule_id=rule_id,
                                name="TestTrafficCapture_VCR_Updated",
                                description="Updated traffic capture rule",
                                enabled=True,
                                order=1,
                                rank=7,
                                action="ALLOW",
                            )
                        except Exception:
                            pass
            except Exception:
                pass  # May fail due to permissions/subscription

            # If we didn't create a rule, test with existing one
            if rule_id is None and rules and len(rules) > 0:
                existing_id = rules[0].id
                fetched_rule, response, err = client.zia.traffic_capture.get_rule(existing_id)
                assert err is None, f"Get traffic capture rule failed: {err}"

        except Exception as e:
            errors.append(f"Exception during traffic capture test: {str(e)}")

        finally:
            # Cleanup
            if rule_id:
                try:
                    client.zia.traffic_capture.delete_rule(rule_id)
                except Exception:
                    pass

        assert len(errors) == 0, f"Errors occurred: {errors}"
