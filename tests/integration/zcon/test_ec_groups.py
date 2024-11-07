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


# import pytest
# from tests.integration.zcon.conftest import MockZCONClient


# @pytest.fixture
# def fs():
#     yield


# class TestECGroups:
#     """
#     Integration Tests for the ZIA EC Groups
#     """

#     def test_ec_group(self, fs):
#         client = MockZCONClient(fs)
#         errors = []  # Initialize an empty list to collect errors
#         group_id = None

#         try:
#             # Test list_ec_groups function
#             try:
#                 groups = client.ecgroups.list_ec_groups()
#                 assert isinstance(groups, list), "Expected a list of groups"
#                 assert len(groups) > 0, "Expected at least one group"
#                 group_id = groups[0].get("id")
#                 assert group_id is not None, "Expected the first group to have an ID"
#             except Exception as exc:
#                 errors.append(f"Listing groups failed: {exc}")

#             # Test get_location function using the group_id from the previous step
#             if group_id:
#                 try:
#                     ec_group_details = client.ecgroups.get_ec_group(group_id)
#                     assert ec_group_details is not None, "Expected valid ec group details"
#                     assert ec_group_details.get("id") == group_id, "Mismatch in ec group ID"
#                 except Exception as exc:
#                     errors.append(f"Fetching ec group by ID failed: {exc}")

#             # Test list_ec_groups_lite function
#             try:
#                 ec_groups_lite = client.ecgroups.list_ec_group_lite()
#                 assert isinstance(ec_groups_lite, list), "Expected a list of lite ec groups"
#                 assert len(ec_groups_lite) > 0, "Expected at least one lite ec group"
#                 first_lite_group_id = ec_groups_lite[0].get("id")
#                 assert first_lite_group_id is not None, "Expected the first lite ec group to have an ID"
#             except Exception as exc:
#                 errors.append(f"Listing lite ec groups failed: {exc}")

#             # Test list_ec_instance_lite function
#             try:
#                 ec_instance_lite = client.ecgroups.list_ec_instance_lite()
#                 assert isinstance(ec_instance_lite, list), "Expected a list of lite ec instance"
#                 assert len(ec_instance_lite) > 0, "Expected at least one lite ec instance"
#                 first_lite_instance_id = ec_instance_lite[0].get("id")
#                 assert first_lite_instance_id is not None, "Expected the first lite ec instance to have an ID"
#             except Exception as exc:
#                 errors.append(f"Listing lite ec instances failed: {exc}")

#             # Test list_ec_instance_lite function
#             try:
#                 ecvm_lite = client.ecgroups.list_ecvm_lite()
#                 assert isinstance(ecvm_lite, list), "Expected a list of lite ecvm"
#                 assert len(ecvm_lite) > 0, "Expected at least one lite ecvm"
#                 first_lite_vm_id = ecvm_lite[0].get("id")
#                 assert first_lite_vm_id is not None, "Expected the first lite ecvm to have an ID"
#             except Exception as exc:
#                 errors.append(f"Listing lite ecvm failed: {exc}")

#         except Exception as exc:
#             errors.append(f"Test ecvm suite failed: {exc}")

#         # Assert that no errors occurred during the test
#         assert len(errors) == 0, f"Errors occurred during ec groups test: {errors}"
