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


class TestLlmProviders:
    """
    Integration Tests for the AI Guard LLM Providers.

    These tests use VCR to record and replay HTTP interactions.
    """

    @pytest.mark.vcr()
    def test_llm_providers(self, fs):
        client = MockAIGuardClient(fs)
        errors = []  # Initialize an empty list to collect errors

        provider_name = "tests-lp-" + generate_random_string()
        provider_type = "xai"
        # NOTE: provider create/update is constrained on both sides -- a public provider
        # is not editable ("A public provider is not editable"), and a private one requires
        # a `servers` payload ("'servers' is required for a private (public=false)
        # provider."). The test therefore creates a public provider and skips the update.
        provider_public = True
        provider_id = None  # Initialize provider_id

        try:
            # Create a new LLM provider
            created_provider, _, err = client.aiguard.llm_providers.add_provider(
                name=provider_name,
                type=provider_type,
                public=provider_public,
            )
            assert err is None, f"Error creating LLM provider: {err}"
            assert created_provider is not None
            assert created_provider.name == provider_name
            assert created_provider.type == provider_type
            assert created_provider.public is provider_public

            provider_id = created_provider.id  # Capture the provider_id for later use
        except Exception as exc:
            errors.append(f"Error during LLM provider creation: {exc}")

        try:
            if provider_id:
                # Retrieve the created LLM provider by ID
                retrieved_provider, _, err = client.aiguard.llm_providers.get_provider(provider_id)
                assert err is None, f"Error fetching LLM provider: {err}"
                assert retrieved_provider.id == provider_id
                assert retrieved_provider.name == provider_name

                # Retrieve the created LLM provider by name
                provider_by_name, _, err = client.aiguard.llm_providers.get_provider_by_name(provider_name)
                assert err is None, f"Error fetching LLM provider by name: {err}"
                assert provider_by_name.id == provider_id
                assert provider_by_name.name == provider_name

                # List the supported LLM provider types
                provider_types, _, err = client.aiguard.llm_providers.list_provider_types()
                assert err is None, f"Error listing LLM provider types: {err}"
                assert provider_types is not None

                # Retrieve the LLM provider type used by the created provider
                retrieved_type, _, err = client.aiguard.llm_providers.get_provider_type(provider_type)
                assert err is None, f"Error fetching LLM provider type: {err}"
                assert retrieved_type is not None

                # List LLM providers and ensure the created provider is in the list
                providers_list, _, err = client.aiguard.llm_providers.list_providers()
                assert err is None, f"Error listing LLM providers: {err}"
                assert any(provider.id == provider_id for provider in providers_list)
        except Exception as exc:
            errors.append(f"LLM provider operation failed: {exc}")

        finally:
            # Cleanup: Delete the LLM provider if it was created
            if provider_id:
                try:
                    delete_response, _, err = client.aiguard.llm_providers.delete_provider(provider_id)
                    assert err is None, f"Error deleting LLM provider: {err}"
                    # Since a 204 No Content response returns None, we assert that delete_response is None
                    assert delete_response is None, f"Expected None for 204 No Content, got {delete_response}"
                except Exception as cleanup_exc:
                    errors.append(f"Cleanup failed for LLM provider ID {provider_id}: {cleanup_exc}")

        assert len(errors) == 0, f"Errors occurred during the LLM provider lifecycle test: {errors}"
