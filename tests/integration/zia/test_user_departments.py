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

# from tests.integration.zia.conftest import MockZIAClient
# import random


# @pytest.fixture
# def fs():
#     yield


# class TestUserDepartment:
#     """
#     Integration Tests for the User Department
#     """

#     def test_user_departments(self, fs):
#         client = MockZIAClient(fs)
#         errors = []
#         department_id = None
#         update_dept = None

#         try:
#             # Test: Add Department
#             try:
#                 create_dept = client.zia.user_management.add_department(
#                     name=f"NewDepartment_{random.randint(1000, 10000)}",
#                     comments=f"NewDepartment_{random.randint(1000, 10000)}",
#                 )
#                 assert error is None, f"Add Department Error: {error}"
#                 assert create_dept is not None, "Department creation failed."
#                 department_id = create_dept.id
#             except Exception as e:
#                 errors.append(f"Exception during add_department: {str(e)}")

#             # Test: Update Department
#             try:
#                 if department_id:
#                     update_dept = client.zia.user_management.update_department(
#                         department_id=department_id,
#                         name=f"UpdateDepartment_{random.randint(1000, 10000)}",
#                         comments=f"UpdateDepartment_{random.randint(1000, 10000)}",
#                     )
#                     assert error is None, f"Update Department Error: {error}"
#                     assert update_dept is not None, "Department update returned None."
#             except Exception as e:
#                 errors.append(f"Exception during update_department: {str(e)}")

#             # Test: Get Department
#             try:
#                 if update_dept:
#                     dept = client.zia.user_management.get_department(update_dept.id)
#                     assert error is None, f"Get Department Error: {error}"
#                     assert dept.id == department_id, "Retrieved department ID mismatch."
#             except Exception as e:
#                 errors.append(f"Exception during get_department: {str(e)}")

#             # Test: List Departments
#             try:
#                 if update_dept:
#                     depts = client.zia.user_management.list_departments(query_params={"search": update_dept.name})
#                     assert error is None, f"List Departments Error: {error}"
#                     assert depts is not None and isinstance(depts, list), "No departments found or invalid format."
#             except Exception as e:
#                 errors.append(f"Exception during list_departments: {str(e)}")

#         finally:
#             # Ensure Department cleanup
#             try:
#                 if update_dept:
#                     _ = client.zia.user_management.delete_department(update_dept.id)
#                     assert error is None, f"Delete Department Error: {error}"
#             except Exception as e:
#                 errors.append(f"Exception during delete_department: {str(e)}")

#         # Final Assertion
#         if errors:
#             raise AssertionError(f"Integration Test Errors:\n{chr(10).join(errors)}")
