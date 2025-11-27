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


class TestPRACredential:
    """
    Integration Tests for the PRA Credential.
    """

    @pytest.mark.vcr()
    def test_pra_credential(self, fs):
        client = MockZPAClient(fs)
        errors = []
        credential_id = None

        credential_name = "John-pracred-" + generate_random_string()
        credential_description = "tests-pracred-" + generate_random_string()
        password = generate_random_password()
        user_domain = "securitygeek.io"

        try:
            # Step 1: Create credential
            try:
                created_credential, _, err = client.zpa.pra_credential.add_credential(
                    name=credential_name,
                    description=credential_description,
                    credential_type="PASSWORD",  # FIX: must be PASSWORD, not USERNAME_PASSWORD
                    user_domain=user_domain,
                    password=password,
                )
                assert err is None, f"Error creating credential: {err}"
                assert created_credential is not None
                assert created_credential.description == credential_description
                credential_id = created_credential.id
            except Exception as exc:
                errors.append(f"Credential creation failed: {exc}")

            # Step 2: List and verify presence
            try:
                credentials_list, _, err = client.zpa.pra_credential.list_credentials()
                assert err is None, f"Error listing PRA credentials: {err}"
                assert any(cred.id == credential_id for cred in credentials_list), "Credential not found in list"
            except Exception as exc:
                errors.append(f"Listing PRA credentials failed: {exc}")

            # Step 3: Retrieve by ID
            try:
                retrieved_credential, _, err = client.zpa.pra_credential.get_credential(credential_id)
                assert err is None, f"Error fetching PRA credential: {err}"
                assert retrieved_credential.id == credential_id
            except Exception as exc:
                errors.append(f"Retrieving PRA credential failed: {exc}")

            # Step 4: Update credential
            try:
                updated_description = "Updated " + generate_random_string()
                _, _, err = client.zpa.pra_credential.update_credential(
                    credential_id=credential_id,
                    name="John-pracred-" + generate_random_string(),
                    description=updated_description,
                    credential_type="PASSWORD",  # FIX: remains PASSWORD
                    user_domain=user_domain,
                    password=password,
                )
                if err and "Response is None" in str(err):
                    err = None  # Treat 204 No Content as success
                assert err is None, f"Error updating PRA credential: {err}"

                # Confirm it's still in the list
                credential_list, _, err = client.zpa.pra_credential.list_credentials()
                assert err is None, f"Error re-listing PRA credentials: {err}"
                assert any(cred.id == credential_id for cred in credential_list), "Credential not found after update"
            except Exception as exc:
                errors.append(f"Credential update failed: {exc}")

        finally:
            cleanup_errors = []
            try:
                if credential_id:
                    _, _, err = client.zpa.pra_credential.delete_credential(credential_id)
                    assert err is None, f"Credential deletion failed: {err}"
            except Exception as exc:
                cleanup_errors.append(f"Deleting credential failed: {exc}")

            errors.extend(cleanup_errors)

        # Final assertion
        assert not errors, f"Errors occurred during the Credential lifecycle test:\n{chr(10).join(map(str, errors))}"
