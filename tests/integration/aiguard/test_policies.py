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


class TestPolicies:
    """
    Integration Tests for the AI Guard Detection Policies.

    These tests use VCR to record and replay HTTP interactions.
    """

    @pytest.mark.vcr()
    def test_policies(self, fs):
        client = MockAIGuardClient(fs)
        errors = []  # Initialize an empty list to collect errors

        policy_name = "tests-pol-" + generate_random_string()
        input_detector_policies = [
            {
                "detector": "toxicity",
                "enabled": True,
                "severity": "HIGH",
                "configuration": {"action": "BLOCK", "threshold": 0.87},
            },
            {
                "detector": "prompt_injection",
                "enabled": True,
                "severity": "CRITICAL",
                "configuration": {"action": "BLOCK", "threshold": 0.75},
            },
        ]
        output_detector_policies = [
            {
                "detector": "toxicity",
                "enabled": True,
                "severity": "CRITICAL",
                "configuration": {"action": "BLOCK", "threshold": 0.87},
            },
            {
                "detector": "pii",
                "enabled": False,
                "severity": "CRITICAL",
                "configuration": {
                    "entities": [
                        {"action": "DETECT", "entityType": "CRYPTO"},
                        {"action": "DETECT", "entityType": "EMAIL_ADDRESS"},
                        {"action": "DETECT", "entityType": "IP_ADDRESS"},
                        {"action": "DETECT", "entityType": "LOCATION"},
                        {"action": "DETECT", "entityType": "US_ITIN"},
                        {"action": "DETECT", "entityType": "DATE_TIME"},
                        {"action": "DETECT", "entityType": "URL"},
                        {"action": "DETECT", "entityType": "MEDICAL_LICENSE"},
                        {"action": "DETECT", "entityType": "STREET_ADDRESS"},
                        {"action": "DETECT", "entityType": "DATE_OF_BIRTH"},
                        {"action": "DETECT", "entityType": "US_DEA_NUMBER"},
                        {"action": "BLOCK", "entityType": "CREDIT_CARD"},
                        {"action": "BLOCK", "entityType": "US_SSN"},
                        {"action": "DETECT", "entityType": "PERSON"},
                        {"action": "BLOCK", "entityType": "US_PASSPORT"},
                        {"action": "BLOCK", "entityType": "US_BANK_NUMBER"},
                        {"action": "BLOCK", "entityType": "US_DRIVER_LICENSE"},
                        {"action": "BLOCK", "entityType": "IBAN_CODE"},
                        {"action": "BLOCK", "entityType": "SWIFT_CODE"},
                        {"action": "ALLOW", "entityType": "PHONE_NUMBER"},
                    ],
                    "threshold": 0.5,
                    "anonymization": "NONE",
                    "defaultAction": "BLOCK",
                    "replaceWithMaskedContent": False,
                },
            },
        ]
        policy_id = None  # Initialize policy_id

        try:
            # Create a new detection policy
            created_policy, _, err = client.aiguard.policies.add_policy(
                name=policy_name,
                inputDetectorPolicies=input_detector_policies,
                outputDetectorPolicies=output_detector_policies,
            )
            assert err is None, f"Error creating policy: {err}"
            assert created_policy is not None
            assert created_policy.name == policy_name
            assert len(created_policy.input_detector_policies) == 2
            assert len(created_policy.output_detector_policies) == 2

            policy_id = created_policy.id  # Capture the policy_id for later use
        except Exception as exc:
            errors.append(f"Error during detection policy creation: {exc}")

        try:
            if policy_id:
                # Retrieve the created detection policy by ID
                retrieved_policy, _, err = client.aiguard.policies.get_policy(policy_id)
                assert err is None, f"Error fetching policy: {err}"
                assert retrieved_policy.id == policy_id
                assert retrieved_policy.name == policy_name

                # Retrieve the created detection policy by name
                policy_by_name, _, err = client.aiguard.policies.get_policy_by_name(policy_name)
                assert err is None, f"Error fetching policy by name: {err}"
                assert policy_by_name.name == policy_name

                # Update the detection policy
                updated_name = policy_name + "Updated"
                _, _, err = client.aiguard.policies.update_policy(
                    policy_id,
                    name=updated_name,
                    inputDetectorPolicies=input_detector_policies,
                    outputDetectorPolicies=output_detector_policies,
                )
                assert err is None, f"Error updating policy: {err}"

                updated_policy, _, err = client.aiguard.policies.get_policy(policy_id)
                assert err is None, f"Error fetching updated policy: {err}"
                assert updated_policy.name == updated_name

                # List detection policies and ensure the updated policy is in the list
                policies_list, _, err = client.aiguard.policies.list_policies()
                assert err is None, f"Error listing policies: {err}"
                assert any(policy.id == policy_id for policy in policies_list)
        except Exception as exc:
            errors.append(f"Detection policy operation failed: {exc}")

        finally:
            # Cleanup: Delete the detection policy if it was created
            if policy_id:
                try:
                    delete_response, _, err = client.aiguard.policies.delete_policy(policy_id)
                    assert err is None, f"Error deleting policy: {err}"
                    # Since a 204 No Content response returns None, we assert that delete_response is None
                    assert delete_response is None, f"Expected None for 204 No Content, got {delete_response}"
                except Exception as cleanup_exc:
                    errors.append(f"Cleanup failed for detection policy ID {policy_id}: {cleanup_exc}")

        assert len(errors) == 0, f"Errors occurred during the detection policy lifecycle test: {errors}"
