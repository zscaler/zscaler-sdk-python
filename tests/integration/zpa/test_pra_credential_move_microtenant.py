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


class TestPRACredentialMoveMicrotenant:
    """
    Integration Tests for Privileged Credential Move to Microtenants
    """

    def test_pra_credential_move_microtenant(self, fs):
        client = MockZPAClient(fs)
        errors = []  # Initialize an empty list to collect errors

        credential_id = None
        microtenant_id = None

        microtenant_name = "tests-microtenant" + generate_random_string()
        microtenant_description = "tests-microtenant" + generate_random_string()

        credential_description = "tests-" + generate_random_string()
        # Generate a random password
        password = generate_random_password()

        # Step 1: Create Microtenant Resource along with a segment_group, app_connector_group, and server_group
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
            assert microtenant_id is not None, "microtenant_id is None"

            client.privileged_remote_access.credential_move(
                credential_id=credential_id,
                target_microtenant_id=microtenant_id,
                microtenant_id="0",
            )
        except Exception as exc:
            errors.append(f"Moving PRA Credential to Microtenant ID {microtenant_id} failed: {exc}")

        try:
            assert microtenant_id is not None, "microtenant_id is None"

            client.privileged_remote_access.credential_move(
                credential_id=credential_id,
                target_microtenant_id="0",
                microtenant_id=microtenant_id,
            )
        except Exception as exc:
            errors.append(f"Moving PRA Credential back to parent tenant from Microtenant ID {microtenant_id} failed: {exc}")

        finally:
            # Cleanup resources
            if microtenant_id:
                try:
                    client.microtenants.delete_microtenant(microtenant_id=microtenant_id)
                except Exception as exc:
                    errors.append(f"Deleting Microtenant failed: {exc}")

            if credential_id:
                try:
                    client.privileged_remote_access.delete_credential(credential_id=credential_id)
                except Exception as exc:
                    errors.append(f"Deleting credential failed: {exc}")

        assert len(errors) == 0, f"Errors occurred during the Privileged Credential Move test: {errors}"
