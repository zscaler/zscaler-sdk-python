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

import pytest

from tests.integration.zpa.conftest import MockZPAClient
from tests.test_utils import generate_random_password, generate_random_string


@pytest.fixture
def fs():
    yield


# class TestPRACredentialMoveMicrotenant:
#     """
#     Integration Tests for Privileged Credential Move to Microtenants
#     """

#     def test_pra_credential_move_microtenant(self, fs):
#         client = MockZPAClient(fs)
#         errors = []

#         credential_id = None
#         microtenant_id = None

#         microtenant_name = "tests-microtenant" + generate_random_string()
#         microtenant_description = "tests-microtenant" + generate_random_string()

#         credential_description = "tests-" + generate_random_string()
#         password = generate_random_password()

#         # Step 1: Create Microtenant Resource directly with known criteria
#         try:
#             # Removed criteria_attribute_values as requested and rely only on criteria_attribute
#             created_microtenant, _, err = client.zpa.microtenants.add_microtenant(
#                 name=microtenant_name,
#                 description=microtenant_description,
#                 enabled=True,
#                 privileged_approvals_enabled=True,
#                 criteria_attribute="AuthDomain"
#             )
#             assert err is None, f"Error creating microtenant: {err}"
#             assert created_microtenant is not None, "Failed to create microtenant"
#             assert created_microtenant.name == microtenant_name
#             assert created_microtenant.description == microtenant_description
#             assert created_microtenant.enabled is True

#             microtenant_id = created_microtenant.id
#             assert microtenant_id is not None, "Failed to retrieve microtenant ID"
#         except Exception as exc:
#             errors.append(f"Error during microtenant creation: {exc}")

#         try:
#             # Create a new PRA credential
#             created_credential, _, err = client.zpa.pra_credential.add_credential(
#                 name="John Doe" + generate_random_string(),
#                 description=credential_description,
#                 credential_type="USERNAME_PASSWORD",
#                 user_domain="acme.com",
#                 username="jdoe" + generate_random_string(),
#                 password=password,
#             )
#             assert err is None, f"Error during credential creation: {err}"
#             assert created_credential is not None, "Failed to create credential"
#             credential_id = created_credential.id

#         except Exception as exc:
#             errors.append(f"Error during credential creation: {exc}")

#         try:
#             assert microtenant_id is not None, "microtenant_id is None"

#             # Move credential to microtenant
#             _, _, err = client.zpa.pra_credential.credential_move(
#                 credential_id=credential_id,
#                 query_params={
#                     "microtenant_id": "0",
#                     "target_microtenant_id": microtenant_id
#                 }
#             )
#             assert err is None, f"Error moving PRA Credential to Microtenant ID {microtenant_id}: {err}"

#         except Exception as exc:
#             errors.append(f"Moving PRA Credential to Microtenant ID {microtenant_id} failed: {exc}")

#         try:
#             assert microtenant_id is not None, "microtenant_id is None"

#             # Move credential back to parent tenant
#             _, _, err = client.zpa.pra_credential.credential_move(
#                 credential_id=credential_id,
#                 query_params={
#                     "microtenant_id": microtenant_id,
#                     "target_microtenant_id": "0"
#                 }

#             )
#             assert err is None, f"Error moving PRA Credential back to parent tenant from Microtenant ID {microtenant_id}: {err}"

#         except Exception as exc:
#             errors.append(f"Moving PRA Credential back to parent tenant from Microtenant ID {microtenant_id} failed: {exc}")

#         finally:
#             # Cleanup resources
#             if microtenant_id:
#                 try:
#                     client.zpa.microtenants.delete_microtenant(microtenant_id=microtenant_id)
#                 except Exception as exc:
#                     errors.append(f"Deleting Microtenant failed: {exc}")

#             if credential_id:
#                 try:
#                     client.zpa.pra_credential.delete_credential(credential_id=credential_id)
#                 except Exception as exc:
#                     errors.append(f"Deleting credential failed: {exc}")

#         assert len(errors) == 0, f"Errors occurred during the Privileged Credential Move test: {errors}"
