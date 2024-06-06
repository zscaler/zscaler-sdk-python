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
from tests.test_utils import generate_random_string


@pytest.fixture
def fs():
    yield


class TestMicrotenants:
    """
    Integration Tests for the Microtenants
    """

    def test_microtenants(self, fs):
        client = MockZPAClient(fs)
        errors = []  # Initialize an empty list to collect errors
        microtenant_id = None

        microtenant_name = "tests-microtenant" + generate_random_string()
        microtenant_description = "tests-microtenant" + generate_random_string()

        # Retrieve available authentication domains
        try:
            auth_domains = client.authdomains.get_auth_domains()
            available_domains = auth_domains.auth_domains
            if not available_domains:
                errors.append("No available authentication domains found.")
                assert False, "No available authentication domains found."
        except Exception as exc:
            errors.append(f"Error retrieving authentication domains: {exc}")
            assert False, f"Error retrieving authentication domains: {exc}"

        for domain in available_domains:
            try:
                # Create a new microtenant with the current domain
                created_microtenant = client.microtenants.add_microtenant(
                    name=microtenant_name,
                    description=microtenant_description,
                    enabled=True,
                    privileged_approvals_enabled=True,
                    criteria_attribute="AuthDomain",
                    criteria_attribute_values=[domain],
                )
                assert created_microtenant is not None
                assert created_microtenant.name == microtenant_name
                assert created_microtenant.description == microtenant_description
                assert created_microtenant.enabled is True

                # Extract the microtenant ID
                microtenant_id = created_microtenant.id
                assert microtenant_id is not None, "Failed to retrieve microtenant ID"
                break
            except Exception as exc:
                if "domains.already.exists.in.other.microtenant" in str(exc) or "domains.does.not.belong.to.customer" in str(
                    exc
                ):
                    continue  # Try the next domain
                else:
                    errors.append(exc)
                    break

        if not microtenant_id:
            errors.append("Failed to create microtenant with available domains.")
            assert False, "Failed to create microtenant with available domains."

        if microtenant_id:
            try:
                # Retrieve the created microtenant by ID
                retrieved_microtenant = client.microtenants.get_microtenant(microtenant_id)
                assert retrieved_microtenant is not None
                assert retrieved_microtenant.id == microtenant_id
                assert retrieved_microtenant.name == microtenant_name
            except Exception as exc:
                errors.append(exc)

            try:
                # Update the microtenant
                updated_name = microtenant_name + " Updated"
                client.microtenants.update_microtenant(
                    microtenant_id,
                    name=updated_name,
                    privileged_approvals_enabled=False,
                )

                updated_microtenant = client.microtenants.get_microtenant(microtenant_id)
                assert updated_microtenant is not None
                assert updated_microtenant.name == updated_name
            except Exception as exc:
                errors.append(exc)

            try:
                # List microtenants and ensure the updated microtenant is in the list
                microtenants_list = client.microtenants.list_microtenants()
                assert any(microtenant.id == microtenant_id for microtenant in microtenants_list)
            except Exception as exc:
                errors.append(exc)

            try:
                # Search for the microtenant by name
                search_result = client.microtenants.get_microtenant_by_name(updated_name)
                assert search_result is not None
                assert search_result.id == microtenant_id
            except Exception as exc:
                errors.append(exc)

            try:
                # Retrieve microtenant summary
                microtenant_summary = client.microtenants.get_microtenant_summary()
                assert microtenant_summary is not None
                assert any(summary.id == microtenant_id and summary.name == updated_name for summary in microtenant_summary)
            except Exception as exc:
                errors.append(exc)

            finally:
                # Cleanup: Delete the microtenant if it was created
                try:
                    delete_response_code = client.microtenants.delete_microtenant(microtenant_id)
                    assert delete_response_code == 204, f"Failed to delete microtenant with ID {microtenant_id}"
                except Exception as cleanup_exc:
                    errors.append(f"Cleanup failed for microtenant ID {microtenant_id}: {cleanup_exc}")

        # Assert that no errors occurred during the test
        assert len(errors) == 0, f"Errors occurred during the microtenant lifecycle test: {errors}"
