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

from tests.integration.aiguard.conftest import MockAIGuardClient
from tests.test_utils import generate_random_string


@pytest.fixture
def fs():
    yield


class TestLlmProviderCredentials:
    """
    Integration Tests for the AI Guard LLM Provider Credentials.

    These tests use VCR to record and replay HTTP interactions.
    """

    @pytest.mark.vcr()
    def test_llm_provider_credentials(self, fs):
        client = MockAIGuardClient(fs)
        errors = []  # Initialize an empty list to collect errors

        provider_name = "Default Anthropic Provider"
        credential_name = "tests-lpc-" + generate_random_string()
        api_credentials = {"type": "API_KEY", "key": "REDACTED_TEST_KEY"}
        provider_id = None  # Initialize provider_id
        credential_id = None  # Initialize credential_id

        try:
            # Resolve the provider id by name so it can be passed to the credential payload
            provider, _, err = client.aiguard.llm_providers.get_provider_by_name(provider_name)
            assert err is None, f"Error fetching LLM provider by name: {err}"
            assert provider is not None, f"LLM provider '{provider_name}' was not found"
            provider_id = provider.id
            assert provider_id is not None
        except Exception as exc:
            errors.append(f"Error resolving the LLM provider '{provider_name}': {exc}")

        try:
            if provider_id:
                # Create a new LLM provider credential
                created_credential, response, err = client.aiguard.llm_provider_credentials.add_credential(
                    providerId=provider_id,
                    name=credential_name,
                    apiCredentials=api_credentials,
                )
                assert err is None, f"Error creating LLM provider credential: {err}"
                assert created_credential is not None
                assert created_credential.name == credential_name
                assert created_credential.provider_id == provider_id

                # The credential model does not expose an id attribute, so read it from the raw body
                credential_id = (response.get_body() or {}).get("id")
        except Exception as exc:
            errors.append(f"Error during LLM provider credential creation: {exc}")

        try:
            if credential_id:
                # Retrieve the created LLM provider credential by ID
                retrieved_credential, _, err = client.aiguard.llm_provider_credentials.get_credential(credential_id)
                assert err is None, f"Error fetching LLM provider credential: {err}"
                assert retrieved_credential.name == credential_name
                assert retrieved_credential.provider_id == provider_id

                # Retrieve the created LLM provider credential by name
                credential_by_name, _, err = client.aiguard.llm_provider_credentials.get_credential_by_name(credential_name)
                assert err is None, f"Error fetching LLM provider credential by name: {err}"
                assert credential_by_name.name == credential_name

                # Update the LLM provider credential
                updated_credential_name = credential_name + "Updated"
                _, _, err = client.aiguard.llm_provider_credentials.update_credential(
                    credential_id,
                    providerId=provider_id,
                    name=updated_credential_name,
                    apiCredentials=api_credentials,
                )
                assert err is None, f"Error updating LLM provider credential: {err}"

                updated_credential, _, err = client.aiguard.llm_provider_credentials.get_credential(credential_id)
                assert err is None, f"Error fetching updated LLM provider credential: {err}"
                assert updated_credential.name == updated_credential_name

                # List LLM provider credentials and ensure the created credential is in the list
                credentials_list, _, err = client.aiguard.llm_provider_credentials.list_credentials()
                assert err is None, f"Error listing LLM provider credentials: {err}"
                assert any(credential.name == updated_credential_name for credential in credentials_list)
        except Exception as exc:
            errors.append(f"LLM provider credential operation failed: {exc}")

        finally:
            # Cleanup: Delete the LLM provider credential if it was created
            if credential_id:
                try:
                    delete_response, _, err = client.aiguard.llm_provider_credentials.delete_credential(credential_id)
                    assert err is None, f"Error deleting LLM provider credential: {err}"
                    # Since a 204 No Content response returns None, we assert that delete_response is None
                    assert delete_response is None, f"Expected None for 204 No Content, got {delete_response}"
                except Exception as cleanup_exc:
                    errors.append(f"Cleanup failed for LLM provider credential ID {credential_id}: {cleanup_exc}")

        assert len(errors) == 0, f"Errors occurred during the LLM provider credential lifecycle test: {errors}"
