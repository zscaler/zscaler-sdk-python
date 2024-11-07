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
            created_credential = client.privileged_remote_access.add_credential(
                name="John Doe" + generate_random_string(),
                description=credential_description,
                credential_type="USERNAME_PASSWORD",
                user_domain="acme.com",
                username="jdoe" + generate_random_string(),
                password=password,
            )
            assert created_credential is not None, "Failed to create credential"
            credential_id = created_credential.id  # Assuming id is accessible like this

        except Exception as exc:
            errors.append(f"Error during credential creation: {exc}")

        try:
            # Test listing Credential
            all_credentials = client.privileged_remote_access.list_credentials()
            if not any(credential["id"] == credential_id for credential in all_credentials):
                raise AssertionError("Credential not found in list")
        except Exception as exc:
            errors.append(f"Listing Credential failed: {exc}")

        try:
            # Test retrieving the specific credential
            retrieved_credential = client.privileged_remote_access.get_credential(credential_id)
            if retrieved_credential["id"] != credential_id:
                raise AssertionError("Failed to retrieve the correct credential")
        except Exception as exc:
            errors.append(f"Retrieving credential failed: {exc}")

        try:
            # Update the credential
            updated_description = "Updated " + generate_random_string()
            updated_credential = client.privileged_remote_access.update_credential(
                credential_id,
                description=updated_description,
                credential_type="USERNAME_PASSWORD",
                user_domain="acme.com",
                username="jdoe",
                password=password,
            )
            if updated_credential["description"] != updated_description:
                raise AssertionError("Failed to update description for credential")
        except Exception as exc:
            errors.append(f"Updating credential failed: {exc}")

        finally:
            cleanup_errors = []

            try:
                # Attempt to delete resources created during the test
                if credential_id:
                    delete_status = client.privileged_remote_access.delete_credential(credential_id)
                    assert delete_status == 204, "Credential deletion failed"
            except Exception as exc:
                cleanup_errors.append(f"Deleting credential failed: {exc}")

            errors.extend(cleanup_errors)

        # Assert no errors occurred during the entire test process
        assert len(errors) == 0, f"Errors occurred during the credential lifecycle test: {errors}"
