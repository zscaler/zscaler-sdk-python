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
# import asyncio
# import os
# import time
# from tests.integration.zpa.conftest import MockZPAClient
# from okta.client import Client as OktaClient
# from pprint import pprint
# from tests.test_utils import generate_random_string


# @pytest.fixture
# def fs():
#     yield


# class TestEmergencyAccessIntegration:
#     """
#     Integration Tests for the Emergency Access API
#     """

#     def test_emergency_access(self, fs):
#         client = MockZPAClient(fs)
#         errors = []  # Initialize an empty list to collect errors

#         user_id = None
#         okta_user_id = None

#         try:
#             # Step 1: Create an Emergency Access User
#             try:
#                 email_id = "tests-" + generate_random_string() + "@bd-hashicorp.com"
#                 first_name = "UserTest" + generate_random_string()
#                 last_name = "Access" + generate_random_string()
#                 user_id = "user1" + generate_random_string()
#                 created_user, _, err = client.zpa.emergency_access.add_user(
#                     email_id=email_id,
#                     first_name=first_name,
#                     last_name=last_name,
#                     user_id=user_id,
#                     activate_now=True,
#                 )
#                 assert err is None, f"Error creating emergency access user: {err}"
#                 assert created_user is not None, "Failed to create emergency access user"
#                 pprint(created_user.as_dict())
#                 user_id = created_user.id
#                 okta_user_id = created_user.id
#             except Exception as exc:
#                 errors.append(f"Error during user creation: {exc}")

#             # Step 2: Get User
#             try:
#                 got_user, _, err = client.zpa.emergency_access.get_user(user_id)
#                 assert err is None, f"Error retrieving emergency access user: {err}"
#                 assert got_user is not None, "get_user returned None"
#                 assert got_user.id == user_id, "Failed to get the correct emergency access user"
#                 pprint(got_user.as_dict())
#             except Exception as exc:
#                 errors.append(f"Error during get user: {exc}")

#             # Sleep for 20-30 seconds to ensure the user is properly provisioned
#             time.sleep(30)

#             # Step 3: Update User
#             try:
#                 updated_first_name = "UpdatedUser1"
#                 updated_user, _, err = client.zpa.emergency_access.update_user(
#                     user_id, first_name=updated_first_name
#                 )
#                 assert err is None, f"Error updating emergency access user: {err}"
#                 assert updated_user is not None, "update_user returned None"
#                 assert updated_user.first_name == updated_first_name, "Failed to update the emergency access user"
#                 pprint(updated_user.as_dict())
#             except Exception as exc:
#                 errors.append(f"Error during update user: {exc}")

#             # Step 4: Deactivate User
#             try:
#                 _, _, err = client.zpa.emergency_access.deactivate_user(user_id)
#                 assert err is None, f"Error deactivating emergency access user: {err}"
#                 print(f"Deactivated user with ID: {user_id}")
#             except Exception as exc:
#                 errors.append(f"Error during deactivate user: {exc}")

#             # Step 5: Activate User
#             try:
#                 _, _, err = client.zpa.emergency_access.activate_user(user_id, send_email=True)
#                 assert err is None, f"Error activating emergency access user: {err}"
#                 print(f"Activated user with ID: {user_id}")
#             except Exception as exc:
#                 errors.append(f"Error during activate user: {exc}")

#             # Step 6: Deactivate User Again Before Deletion
#             try:
#                 _, _, err = client.zpa.emergency_access.deactivate_user(user_id)
#                 assert err is None, f"Error during final deactivate user: {err}"
#                 print(f"Final deactivation of user with ID: {user_id} completed")
#             except Exception as exc:
#                 errors.append(f"Error during final deactivate user: {exc}")

#         except Exception as exc:
#             errors.append(f"Error during emergency access user operations: {exc}")

#         finally:
#             # Cleanup: Ensure proper deletion of the user
#             if okta_user_id:
#                 try:
#                     # Deactivate the user in Okta and then delete
#                     asyncio.run(delete_user_in_okta(okta_user_id))
#                 except Exception as cleanup_exc:
#                     errors.append(f"Cleanup failed: {cleanup_exc}")

#         # Assert that no errors occurred during the test
#         assert len(errors) == 0, f"Errors occurred during the Emergency Access operations test: {errors}"


# async def delete_user_in_okta(user_id: str):
#     # Fetch Okta domain and API token from environment variables
#     okta_domain = os.getenv("OKTA_CLIENT_ORGURL")
#     token = os.getenv("OKTA_CLIENT_TOKEN")

#     # Initialize Okta client with environment variables and logging
#     client = OktaClient({"orgUrl": f"https://{okta_domain}", "token": token})

#     # Deactivate and delete the user in Okta
#     try:
#         user = await client.get_user(user_id)
#         print(f"User fetched from Okta: {user}")

#         if user[0].status != "DEPROVISIONED":
#             resp = await client.deactivate_or_delete_user(user[0].id)
#             print(f"Deactivation response: {resp}")
#             time.sleep(5)  # Wait for deactivation

#         resp = await client.deactivate_or_delete_user(user[0].id)  # Deletion
#         print(f"Deletion response: {resp}")
#         print(f"User {user[0].id} deleted successfully in Okta")
#     except Exception as e:
#         print(f"Failed to delete user {user_id} in Okta: {e}")
#         raise
