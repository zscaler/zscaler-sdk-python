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

# from tests.integration.zia.conftest import MockZIAClient
# from tests.test_utils import generate_random_string


# @pytest.fixture
# def fs():
#     yield


# class TestNATControlRules:
#     """
#     Integration Tests for the ZIA NAT Control Rules
#     """

#     @pytest.mark.vcr()
#     def test_firewall_rule(self, fs):
#         client = MockZIAClient(fs)
#         errors = []
#         dst_group_id = None
#         src_group_id = None
#         rule_id = None

#         try:
#             # Step 1: Create a Destination IP Group
#             try:
#                 created_dst_group = client.zia.cloud_firewall.add_ip_destination_group(
#                     name="tests-" + generate_random_string(),
#                     description="tests-" + generate_random_string(),
#                     type="DSTN_IP",
#                     addresses=["192.168.100.4", "192.168.100.5"],
#                 )
#                 assert error is None, f"Error adding IP destination group: {error}"
#                 assert created_dst_group is not None, "Failed to create IP destination group"
#                 dst_group_id = created_dst_group.id
#                 assert created_dst_group.name.startswith("tests-"), "Group name mismatch in creation"
#                 # (Optionally) Assert the description if needed
#             except Exception as exc:
#                 errors.append(f"Destination IP Group creation failed: {exc}")

#             # Step 2: Create a Source IP Group
#             try:
#                 created_src_group = client.zia.cloud_firewall.add_ip_source_group(
#                     name="tests-" + generate_random_string(),
#                     description="Integration test source group",
#                     ip_addresses=["192.168.100.1", "192.168.100.2", "192.168.100.3"],
#                 )
#                 assert error is None, f"Error creating source IP group: {error}"
#                 assert created_src_group is not None, "Source IP Group creation returned None"
#                 src_group_id = created_src_group.id
#             except Exception as exc:
#                 errors.append(f"Source IP Group creation failed: {exc}")

#             # Step 3: Create a NAT Control Rule
#             try:
#                 rule_name = "tests-" + generate_random_string()
#                 created_rule = client.zia.nat_control_policy.add_rule(
#                     name=rule_name,
#                     description="Integration test NAT Control Rule",
#                     enabled=True,
#                     order=1,
#                     rank=7,
#                     src_ip_groups=[src_group_id],
#                     dest_ip_groups=[dst_group_id],
#                     redirect_port="2000",
#                     redirect_ip="1.1.1.1",
#                     src_ips=["192.168.100.0/24", "192.168.200.1"],
#                     dest_addresses=[
#                         "3.217.228.0-3.217.231.255",
#                         "3.235.112.0-3.235.119.255",
#                         "35.80.88.0-35.80.95.255",
#                         "server1.acme.com",
#                         "*.acme.com",
#                     ],
#                 )
#                 assert error is None, f"NAT Control Rule creation failed: {error}"
#                 assert created_rule is not None, "NAT Control Rule creation returned None"
#                 rule_id = created_rule.id
#             except Exception as exc:
#                 errors.append(f"NAT Control Rule creation failed: {exc}")

#             # Step 4: Retrieve the NAT Control Rule by ID
#             try:
#                 retrieved_rule = client.zia.nat_control_policy.get_rule(rule_id)
#                 assert error is None, f"Error retrieving NAT Control Rule: {error}"
#                 assert retrieved_rule is not None, "Retrieved NAT Control Rule is None"
#                 assert retrieved_rule.id == rule_id, "Incorrect rule retrieved"
#             except Exception as exc:
#                 errors.append(f"Retrieving NAT Control Rule failed: {exc}")

#             # Step 5: Update the NAT Control Rule
#             try:
#                 updated_description = "Updated integration test NAT Control Rule"
#                 updated_rule = client.zia.nat_control_policy.update_rule(
#                     rule_id=rule_id,
#                     name=rule_name,
#                     description=updated_description,
#                     enabled=True,
#                     order=1,
#                     rank=7,
#                     redirect_port="2000",
#                     redirect_ip="1.1.1.1",
#                     src_ips=["192.168.100.0/24", "192.168.200.1"],
#                     dest_addresses=["3.217.228.0-3.217.231.255", "3.235.112.0-3.235.119.255", "35.80.88.0-35.80.95.255"],
#                 )
#                 assert error is None, f"Error updating NAT Control Rule: {error}"
#                 assert updated_rule is not None, "Updated NAT Control Rule is None"
#                 assert (
#                     updated_rule.description == updated_description
#                 ), f"NAT Control Rule update failed: {updated_rule.as_dict()}"
#             except Exception as exc:
#                 errors.append(f"Updating NAT Control Rule failed: {exc}")

#             # Step 6: List NAT Control Rules and verify the rule is present
#             try:
#                 rules = client.zia.nat_control_policy.list_rules()
#                 assert error is None, f"Error listing NAT Control Rules: {error}"
#                 assert rules is not None, "NAT Control Rules list is None"
#                 assert any(rule.id == rule_id for rule in rules), "Newly created rule not found in the list of rules."
#             except Exception as exc:
#                 errors.append(f"Listing NAT Control Rules failed: {exc}")

#         finally:
#             cleanup_errors = []
#             try:
#                 if rule_id:
#                     # Delete the NAT Control Rule
#                     _ = client.zia.nat_control_policy.delete_rule(rule_id)
#                     assert error is None, f"Error deleting NAT Control Rule: {error}"
#             except Exception as exc:
#                 cleanup_errors.append(f"Deleting NAT Control Rule failed: {exc}")

#             try:
#                 if dst_group_id:
#                     # Delete the destination IP group
#                     _ = client.zia.cloud_firewall.delete_ip_destination_group(dst_group_id)
#                     # No assertion needed here if deletion returns status code in a different manner; adjust as needed.
#                     # For consistency, you may check error is None.
#                     assert error is None, f"Error deleting Destination IP Group: {error}"
#             except Exception as exc:
#                 cleanup_errors.append(f"Deleting Destination IP Group failed: {exc}")

#             try:
#                 if src_group_id:
#                     # Delete the source IP group
#                     _ = client.zia.cloud_firewall.delete_ip_source_group(src_group_id)
#                     assert error is None, f"Error deleting Source IP Group: {error}"
#             except Exception as exc:
#                 cleanup_errors.append(f"Deleting Source IP Group failed: {exc}")

#             errors.extend(cleanup_errors)

#         if errors:
#             raise AssertionError(f"Integration Test Errors:\n{chr(10).join(errors)}")
