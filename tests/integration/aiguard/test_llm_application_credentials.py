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


class TestLlmApplicationCredentials:
    """
    Integration Tests for the AI Guard LLM Application Credentials.

    These tests use VCR to record and replay HTTP interactions.
    """

    @pytest.mark.vcr()
    def test_llm_application_credentials(self, fs):
        client = MockAIGuardClient(fs)
        errors = []  # Initialize an empty list to collect errors

        provider_name = "Default Anthropic Provider"
        application_name = "App01"
        credential_name = "tests-lac-" + generate_random_string()
        credential_mode = "PROXY"
        provider_id = None  # Initialize provider_id
        application_id = None  # Initialize application_id
        provider_credentials_id = None  # Initialize provider_credentials_id
        credential_id = None  # Initialize credential_id

        try:
            # Resolve the provider id by name so it can be passed to the credential payload
            provider, _, err = client.aiguard.llm_providers.get_provider_by_name(provider_name)
            assert err is None, f"Error fetching LLM provider by name: {err}"
            assert provider is not None, f"LLM provider '{provider_name}' was not found"
            provider_id = provider.id
            assert provider_id is not None

            # Resolve the application id by name so it can be passed to the credential payload
            application, _, err = client.aiguard.llm_applications.get_application_by_name(application_name)
            assert err is None, f"Error fetching LLM application by name: {err}"
            assert application is not None, f"LLM application '{application_name}' was not found"
            application_id = application.id
            assert application_id is not None

            # Resolve the provider credentials id belonging to the resolved provider. The
            # provider credential model does not expose an id attribute, so the id is read
            # from the raw response body.
            _, response, err = client.aiguard.llm_provider_credentials.list_credentials()
            assert err is None, f"Error listing LLM provider credentials: {err}"
            for item in (response.get_body() or {}).get("items", []):
                if item.get("providerId") == provider_id:
                    provider_credentials_id = item.get("id")
                    break
            assert provider_credentials_id is not None, f"No provider credential found for provider '{provider_name}'"
        except Exception as exc:
            errors.append(f"Error resolving the LLM application credential dependencies: {exc}")

        try:
            if application_id and provider_id and provider_credentials_id:
                # Create a new LLM application credential
                created_credential, _, err = client.aiguard.llm_application_credentials.add_credential(
                    applicationId=application_id,
                    providerId=provider_id,
                    providerCredentialsId=provider_credentials_id,
                    name=credential_name,
                    mode=credential_mode,
                )
                assert err is None, f"Error creating LLM application credential: {err}"
                assert created_credential is not None
                assert created_credential.name == credential_name
                assert created_credential.mode == credential_mode
                assert created_credential.application_id == application_id
                assert created_credential.provider_id == provider_id
                assert created_credential.provider_credentials_id == provider_credentials_id

                credential_id = created_credential.id  # Capture the credential_id for later use
        except Exception as exc:
            errors.append(f"Error during LLM application credential creation: {exc}")

        try:
            if credential_id:
                # Retrieve the created LLM application credential by ID
                retrieved_credential, _, err = client.aiguard.llm_application_credentials.get_credential(credential_id)
                assert err is None, f"Error fetching LLM application credential: {err}"
                assert retrieved_credential.id == credential_id
                assert retrieved_credential.name == credential_name

                # Retrieve the created LLM application credential by name
                credential_by_name, _, err = client.aiguard.llm_application_credentials.get_credential_by_name(credential_name)
                assert err is None, f"Error fetching LLM application credential by name: {err}"
                assert credential_by_name.id == credential_id
                assert credential_by_name.name == credential_name

                # Update the LLM application credential
                updated_credential_name = credential_name + "Updated"
                _, _, err = client.aiguard.llm_application_credentials.update_credential(
                    credential_id,
                    applicationId=application_id,
                    providerId=provider_id,
                    providerCredentialsId=provider_credentials_id,
                    name=updated_credential_name,
                    mode=credential_mode,
                )
                assert err is None, f"Error updating LLM application credential: {err}"

                updated_credential, _, err = client.aiguard.llm_application_credentials.get_credential(credential_id)
                assert err is None, f"Error fetching updated LLM application credential: {err}"
                assert updated_credential.name == updated_credential_name

                # List LLM application credentials and ensure the created credential is in the list
                credentials_list, _, err = client.aiguard.llm_application_credentials.list_credentials()
                assert err is None, f"Error listing LLM application credentials: {err}"
                assert any(credential.id == credential_id for credential in credentials_list)
        except Exception as exc:
            errors.append(f"LLM application credential operation failed: {exc}")

        finally:
            # Cleanup: Delete the LLM application credential if it was created
            if credential_id:
                try:
                    delete_response, _, err = client.aiguard.llm_application_credentials.delete_credential(credential_id)
                    assert err is None, f"Error deleting LLM application credential: {err}"
                    # Since a 204 No Content response returns None, we assert that delete_response is None
                    assert delete_response is None, f"Expected None for 204 No Content, got {delete_response}"
                except Exception as cleanup_exc:
                    errors.append(f"Cleanup failed for LLM application credential ID {credential_id}: {cleanup_exc}")

        assert len(errors) == 0, f"Errors occurred during the LLM application credential lifecycle test: {errors}"
