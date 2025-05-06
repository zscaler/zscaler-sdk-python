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
# from tests.test_utils import generate_random_password, generate_random_string
# import time


# @pytest.fixture
# def fs():
#     yield


# class TestUsers:
#     """
#     Integration Tests for the User Management
#     """

#     def test_users(self, fs):
#         client = MockZIAClient(fs)
#         errors = []
#         user_id = None
#         department_id = None
#         group_id = None
#         user_name = f"tests-{generate_random_string()}"
#         user_email = f"{user_name}@securitygeek.io"

#         try:
#             # Step 1: Retrieve department
#             try:
#                 departments, _, error = client.zia.user_management.list_departments(query_params={"search": "A000"})
#                 assert error is None, f"Department listing error: {error}"
#                 department = next((d for d in departments if hasattr(d, "id")), None)
#                 assert department, "No valid departments available for assignment"
#                 department_id = department.id
#             except Exception as exc:
#                 errors.append(f"Department retrieval failed: {exc}")

#             # Step 2: Retrieve group
#             try:
#                 groups, _, error = client.zia.user_management.list_groups(query_params={"search": "A000"})
#                 assert error is None, f"Group listing error: {error}"
#                 group = next((g for g in groups if hasattr(g, "id")), None)
#                 assert group, "No valid groups available for assignment"
#                 group_id = group.id
#             except Exception as exc:
#                 errors.append(f"Group retrieval failed: {exc}")

#             # Step 3: Create user
#             if department_id and group_id:
#                 try:
#                     created_user, _, error = client.zia.user_management.add_user(
#                         name=user_name,
#                         email=user_email,
#                         comments="Test user creation",
#                         password=generate_random_password(),
#                         groups=[{"id": group_id}],
#                         department={"id": department_id},
#                     )
#                     assert error is None, f"User creation error: {error}"
#                     assert created_user and hasattr(created_user, "id"), "User creation returned no valid ID"
#                     user_id = created_user.id
#                 except Exception as exc:
#                     errors.append(f"User creation failed: {exc}")

#             # Step 4: Fetch user
#             time.sleep(2)
#             if user_id:
#                 try:
#                     retrieved_user, _, error = client.zia.user_management.get_user(user_id)
#                     assert error is None, f"User fetch error: {error}"
#                     assert retrieved_user.id == user_id, "Mismatch in fetched user ID"
#                 except Exception as exc:
#                     errors.append(f"Retrieving user account failed: {exc}")

#             # Step 5: Update user (must re-send all required fields)
#             time.sleep(2)
#             if user_id:
#                 try:
#                     updated_password = generate_random_password()
#                     updated_user, _, error = client.zia.user_management.update_user(
#                         user_id=user_id,
#                         name=user_name,
#                         email=user_email,
#                         comments="Updated test user via integration test",
#                         password=updated_password,
#                         groups=[{"id": group_id}],
#                         department={"id": department_id},
#                     )
#                     assert error is None, f"User update error: {error}"
#                     assert (
#                         updated_user and updated_user.comments == "Updated test user via integration test"
#                     ), "Update verification failed"
#                 except Exception as exc:
#                     errors.append(f"Updating user account failed: {exc}")

#         finally:
#             time.sleep(2)
#             # Step 6: Delete user
#             if user_id:
#                 try:
#                     _, _, error = client.zia.user_management.delete_user(user_id)
#                     assert error is None, f"Delete user error: {error}"
#                 except Exception as e:
#                     errors.append(f"Exception during delete_user: {str(e)}")

#             # Final assertion
#             if errors:
#                 raise AssertionError("Errors occurred during the user management test:\n" + "\n".join(errors))
