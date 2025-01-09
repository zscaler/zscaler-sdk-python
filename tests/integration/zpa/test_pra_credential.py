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

    def test_pra_credential(self, fs):
        client = MockZPAClient(fs)
        errors = []  # Initialize an empty list to collect errors
        credential_id = None

        credential_description = "tests-" + generate_random_string()
        # Generate a random password
        password = generate_random_password()

        try:
            # Create a new pra credential
            created_credential, _, err = client.zpa.pra_credential.add_credential(
                name="John Doe" + generate_random_string(),
                description=credential_description,
                credential_type="USERNAME_PASSWORD",
                user_domain="acme.com",
                username="jdoe" + generate_random_string(),
                password=password,
            )
            assert err is None, f"Failed to create portal: {err}"
            assert created_credential is not None
            assert created_credential.description == credential_description
            
            credential_id = created_credential.id  # Assuming id is accessible like this
        except Exception as exc:
            errors.append(f"Error during portal creation: {exc}")

        try:
            # Test listing Credential
            credentials_list, _, err = client.zpa.pra_credential.list_credentials()
            assert err is None, f"Error listing PRA credentials: {err}"
            assert any(credential.id == credential_id for credential in credentials_list)
        except Exception as exc:
            errors.append(f"Listing PRA credentials failed: {exc}")

        try:
            # Test retrieving the specific credential
            retrieved_credential, _, err = client.zpa.pra_credential.get_credential(credential_id)
            assert err is None, f"Error fetching PRA credential: {err}"
            assert retrieved_credential.id == credential_id
        except Exception as exc:
            errors.append(f"Retrieving PRA credential failed: {exc}")

        try:
            if credential_id:
                # Retrieve the created app pra portal by ID
                retrieved_credential, _, err = client.zpa.pra_credential.get_credential(credential_id)
                assert err is None, f"Error fetching credential: {err}"
                assert retrieved_credential.id == credential_id

            # Update the credential
            updated_description = "Updated " + generate_random_string()
            _, _, err  = client.zpa.pra_credential.update_credential(
                credential_id,
                description=updated_description,
                credential_type="USERNAME_PASSWORD",
                user_domain="acme.com",
                username="jdoe",
                password=password,
            )
                        # If err is "Response is None", treat it as success since PUT 204 no content is expected
            if err is not None and "Response is None" in str(err):
                err = None
            assert err is None, f"Error updating pra credential: {err}"
            
            # List app pra portal and ensure the updated group is in the list
            credetial_list, _, err = client.zpa.pra_credential.list_credentials()
            assert err is None, f"Error listing pra portals: {err}"
            assert any(group.id == credential_id for group in credetial_list)
        except Exception as exc:
            errors.append(exc)

        finally:
            cleanup_errors = []

            try:
                # Attempt to delete resources created during the test
                if credential_id:
                    delete_response, _, err = client.zpa.pra_credential.delete_credential(credential_id)
                    assert err is None, f"Credential deletion failed: {err}"
                    assert delete_response is None, f"Expected None for 204 No Content, got {delete_response}"
            except Exception as exc:
                cleanup_errors.append(f"Deleting Credential failed: {exc}")

            errors.extend(cleanup_errors)

        # Assert no errors occurred during the entire test process
        assert len(errors) == 0, f"Errors occurred during the Credential lifecycle test: {errors}"

