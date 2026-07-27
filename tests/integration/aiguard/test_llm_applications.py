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


class TestLlmApplications:
    """
    Integration Tests for the AI Guard LLM Applications.

    These tests use VCR to record and replay HTTP interactions.
    """

    @pytest.mark.vcr()
    def test_llm_applications(self, fs):
        client = MockAIGuardClient(fs)
        errors = []  # Initialize an empty list to collect errors

        application_name = "tests-la-" + generate_random_string()
        owner_email = "tests-la-" + generate_random_string() + "@acme.com"
        application_settings = {
            "includeEventContents": True,
            "encryptEventContents": False,
        }
        application_id = None  # Initialize application_id

        try:
            # Create a new LLM application
            created_application, _, err = client.aiguard.llm_applications.add_application(
                name=application_name,
                ownerEmail=owner_email,
                applicationSettings=application_settings,
            )
            assert err is None, f"Error creating LLM application: {err}"
            assert created_application is not None
            assert created_application.name == application_name
            # NOTE: tests/conftest.py redacts any quoted value containing "@" from recorded
            # responses, so owner_email always reads back as "REDACTED" and is not asserted.
            assert created_application.application_settings.include_event_contents is True
            assert created_application.application_settings.encrypt_event_contents is False

            application_id = created_application.id  # Capture the application_id for later use
        except Exception as exc:
            errors.append(f"Error during LLM application creation: {exc}")

        try:
            if application_id:
                # Retrieve the created LLM application by ID
                retrieved_application, _, err = client.aiguard.llm_applications.get_application(application_id)
                assert err is None, f"Error fetching LLM application: {err}"
                assert retrieved_application.id == application_id
                assert retrieved_application.name == application_name

                # Retrieve the created LLM application by name
                application_by_name, _, err = client.aiguard.llm_applications.get_application_by_name(application_name)
                assert err is None, f"Error fetching LLM application by name: {err}"
                assert application_by_name.id == application_id
                assert application_by_name.name == application_name

                # Update the LLM application. NOTE: encryptEventContents is left False --
                # enabling it requires a customer-managed key (CMK) configured in tenant
                # settings, which the API rejects otherwise.
                updated_application_name = application_name + "Updated"
                _, _, err = client.aiguard.llm_applications.update_application(
                    application_id,
                    name=updated_application_name,
                    ownerEmail=owner_email,
                    applicationSettings=application_settings,
                )
                assert err is None, f"Error updating LLM application: {err}"

                updated_application, _, err = client.aiguard.llm_applications.get_application(application_id)
                assert err is None, f"Error fetching updated LLM application: {err}"
                assert updated_application.name == updated_application_name

                # List LLM applications and ensure the created application is in the list
                applications_list, _, err = client.aiguard.llm_applications.list_applications()
                assert err is None, f"Error listing LLM applications: {err}"
                assert any(application.id == application_id for application in applications_list)
        except Exception as exc:
            errors.append(f"LLM application operation failed: {exc}")

        finally:
            # Cleanup: Delete the LLM application if it was created
            if application_id:
                try:
                    delete_response, _, err = client.aiguard.llm_applications.delete_application(application_id)
                    assert err is None, f"Error deleting LLM application: {err}"
                    # Since a 204 No Content response returns None, we assert that delete_response is None
                    assert delete_response is None, f"Expected None for 204 No Content, got {delete_response}"
                except Exception as cleanup_exc:
                    errors.append(f"Cleanup failed for LLM application ID {application_id}: {cleanup_exc}")

        assert len(errors) == 0, f"Errors occurred during the LLM application lifecycle test: {errors}"
