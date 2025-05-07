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
            auth_domains, _, err = client.zpa.customer_controller.get_auth_domains()
            assert err is None, f"Error retrieving authentication domains: {err}"
            assert auth_domains is not None, "Auth domains response is None"
            assert isinstance(auth_domains, dict), "Auth domains should be a dictionary"
            assert "authDomains" in auth_domains, "Missing 'authDomains' key in response"
            available_domains = auth_domains["authDomains"]
            assert isinstance(available_domains, list), "'authDomains' should be a list"
            assert len(available_domains) > 0, "No available authentication domains found."
        except Exception as exc:
            errors.append(f"Error retrieving authentication domains: {exc}")
            assert False, f"Error retrieving authentication domains: {exc}"

        for domain in available_domains:
            try:
                # Create a new microtenant with the current domain
                created_microtenant, _, err = client.zpa.microtenants.add_microtenant(
                    name=microtenant_name,
                    description=microtenant_description,
                    enabled=True,
                    privileged_approvals_enabled=True,
                    criteria_attribute="AuthDomain",
                    # criteria_attribute_values=[domain],
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

        try:
            # Test retrieving the specific portal
            retrieved_microtenant, _, err = client.zpa.microtenants.get_microtenant(microtenant_id)
            assert err is None, f"Error fetching Microtenant: {err}"
            assert retrieved_microtenant.id == microtenant_id
            assert retrieved_microtenant.name == microtenant_name
        except Exception as exc:
            errors.append(f"Retrieving Microtenant failed: {exc}")

        try:
            if microtenant_id:
                update_microtenant, _, error = client.zpa.microtenants.update_microtenant(
                    microtenant_id=microtenant_id,
                    name=microtenant_name,
                    description=microtenant_name,
                    enabled=True,
                    privileged_approvals_enabled=True,
                    criteria_attribute="AuthDomain",
                )
                assert error is None, f"Update Microtenant Error: {error}"
                assert update_microtenant is not None, "Microtenant update returned None."
        except Exception as e:
            errors.append(f"Exception during update_microtenant: {str(e)}")

        try:
            if update_microtenant:
                microtenants, _, error = client.zpa.microtenants.list_microtenants(query_params={"search": update_microtenant.name})
                assert error is None, f"List Microtenants Error: {error}"
                assert microtenants is not None and isinstance(microtenants, list), "No Microtenants found or invalid format."
        except Exception as e:
            errors.append(f"Exception during list_microtenants: {str(e)}")

        try:
            # Retrieve microtenant summary
            microtenant_summary = client.zpa.microtenants.get_microtenant_summary()
            assert microtenant_summary is not None
            # assert any(summary.id == microtenant_id and summary.name == updated_name for summary in microtenant_summary)
        except Exception as exc:
            errors.append(exc)

        finally:
            cleanup_errors = []

            try:
                # Attempt to delete resources created during the test
                if microtenant_id:
                    delete_response, _, err = client.zpa.microtenants.delete_microtenant(microtenant_id)
                    assert err is None, f"Microtenant deletion failed: {err}"
                    assert delete_response is None, f"Expected None for 204 No Content, got {delete_response}"
            except Exception as exc:
                cleanup_errors.append(f"Deleting Microtenant failed: {exc}")

            errors.extend(cleanup_errors)

        # Assert that no errors occurred during the test
        assert len(errors) == 0, f"Errors occurred during the microtenant lifecycle test: {errors}"
