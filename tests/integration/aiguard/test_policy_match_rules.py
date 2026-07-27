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


class TestPolicyMatchRules:
    """
    Integration Tests for the AI Guard Policy Match Rules.

    These tests use VCR to record and replay HTTP interactions.
    """

    @pytest.mark.vcr()
    def test_policy_match_rules(self, fs):
        client = MockAIGuardClient(fs)
        errors = []  # Initialize an empty list to collect errors

        provider_name = "Default Anthropic Provider"
        policy_name = "tests-pol-" + generate_random_string()
        application_name = "tests-la-" + generate_random_string()
        app_credential_name = "tests-lac-" + generate_random_string()
        rule_name = "tests-pmr-" + generate_random_string()
        policy_input_detector_policies = [
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
        policy_output_detector_policies = [
            {
                "detector": "toxicity",
                "enabled": True,
                "severity": "CRITICAL",
                "configuration": {"action": "BLOCK", "threshold": 0.87},
            },
        ]
        application_settings = {"includeEventContents": True, "encryptEventContents": False}
        policy_id = None  # Initialize policy_id
        application_id = None  # Initialize application_id
        provider_id = None  # Initialize provider_id
        provider_credentials_id = None  # Initialize provider_credentials_id
        app_credential_id = None  # Initialize app_credential_id
        rule_id = None  # Initialize rule_id

        try:
            # A policy match rule references a policy, an application and an application
            # credential, so each prerequisite is created (or resolved) first and its id
            # captured for the match rule payload.

            # Create the detection policy the match rule attaches to
            created_policy, _, err = client.aiguard.policies.add_policy(
                name=policy_name,
                inputDetectorPolicies=policy_input_detector_policies,
                outputDetectorPolicies=policy_output_detector_policies,
            )
            assert err is None, f"Error creating detection policy: {err}"
            assert created_policy is not None
            policy_id = created_policy.id
            assert policy_id is not None

            # Create the LLM application the match criteria points at
            created_application, _, err = client.aiguard.llm_applications.add_application(
                name=application_name,
                ownerEmail=application_name + "@acme.com",
                applicationSettings=application_settings,
            )
            assert err is None, f"Error creating LLM application: {err}"
            assert created_application is not None
            application_id = created_application.id
            assert application_id is not None

            # Resolve the provider id by name
            provider, _, err = client.aiguard.llm_providers.get_provider_by_name(provider_name)
            assert err is None, f"Error fetching LLM provider by name: {err}"
            assert provider is not None, f"LLM provider '{provider_name}' was not found"
            provider_id = provider.id
            assert provider_id is not None

            # Resolve a provider credential belonging to the resolved provider. The provider
            # credential model does not expose an id attribute, so it is read from the raw body.
            _, response, err = client.aiguard.llm_provider_credentials.list_credentials()
            assert err is None, f"Error listing LLM provider credentials: {err}"
            for item in (response.get_body() or {}).get("items", []):
                if item.get("providerId") == provider_id:
                    provider_credentials_id = item.get("id")
                    break
            assert provider_credentials_id is not None, f"No provider credential found for provider '{provider_name}'"

            # Create the application credential referenced by the match criteria
            created_app_credential, _, err = client.aiguard.llm_application_credentials.add_credential(
                applicationId=application_id,
                providerId=provider_id,
                providerCredentialsId=provider_credentials_id,
                name=app_credential_name,
                mode="PROXY",
            )
            assert err is None, f"Error creating LLM application credential: {err}"
            assert created_app_credential is not None
            app_credential_id = created_app_credential.id
            assert app_credential_id is not None
        except Exception as exc:
            errors.append(f"Error resolving the policy match rule dependencies: {exc}")

        try:
            if policy_id and application_id and app_credential_id:
                # Create a new policy match rule
                created_rule, _, err = client.aiguard.policy_match_rules.add_rule(
                    policyId=policy_id,
                    name=rule_name,
                    enabled=True,
                    ruleOrder=2,
                    matchCriteria={
                        "llmApplications": [
                            {
                                "applicationId": application_id,
                                "applicationCredentialsIds": [app_credential_id],
                            }
                        ],
                        "type": "DAS_APPLICATION",
                    },
                )
                assert err is None, f"Error creating policy match rule: {err}"
                assert created_rule is not None
                assert created_rule.name == rule_name
                assert created_rule.policy_id == policy_id
                assert created_rule.enabled is True
                assert created_rule.rule_order == 2
                assert created_rule.match_criteria.type == "DAS_APPLICATION"
                assert len(created_rule.match_criteria.llm_applications) == 1
                assert created_rule.match_criteria.llm_applications[0].application_id == application_id
                assert created_rule.match_criteria.llm_applications[0].application_credentials_ids == [app_credential_id]

                rule_id = created_rule.id  # Capture the rule_id for later use
        except Exception as exc:
            errors.append(f"Error during policy match rule creation: {exc}")

        try:
            if rule_id:
                # Retrieve the created policy match rule by ID
                retrieved_rule, _, err = client.aiguard.policy_match_rules.get_rule(rule_id)
                assert err is None, f"Error fetching policy match rule: {err}"
                assert retrieved_rule.id == rule_id
                assert retrieved_rule.name == rule_name

                # Retrieve the created policy match rule by name
                rule_by_name, _, err = client.aiguard.policy_match_rules.get_rule_by_name(rule_name)
                assert err is None, f"Error fetching policy match rule by name: {err}"
                assert rule_by_name.id == rule_id
                assert rule_by_name.name == rule_name

                # Update the policy match rule
                updated_rule_name = rule_name + "Updated"
                _, _, err = client.aiguard.policy_match_rules.update_rule(
                    rule_id,
                    policyId=policy_id,
                    name=updated_rule_name,
                    enabled=True,
                    ruleOrder=2,
                    matchCriteria={
                        "llmApplications": [
                            {
                                "applicationId": application_id,
                                "applicationCredentialsIds": [app_credential_id],
                            }
                        ],
                        "type": "DAS_APPLICATION",
                    },
                )
                assert err is None, f"Error updating policy match rule: {err}"

                updated_rule, _, err = client.aiguard.policy_match_rules.get_rule(rule_id)
                assert err is None, f"Error fetching updated policy match rule: {err}"
                assert updated_rule.name == updated_rule_name

                # List policy match rules and ensure the created rule is in the list
                rules_list, _, err = client.aiguard.policy_match_rules.list_rules()
                assert err is None, f"Error listing policy match rules: {err}"
                assert any(rule.id == rule_id for rule in rules_list)
        except Exception as exc:
            errors.append(f"Policy match rule operation failed: {exc}")

        finally:
            # Cleanup runs in reverse dependency order so each resource is removed before
            # the resource it references.
            if rule_id:
                try:
                    delete_response, _, err = client.aiguard.policy_match_rules.delete_rule(rule_id)
                    assert err is None, f"Error deleting policy match rule: {err}"
                    # Since a 204 No Content response returns None, we assert that delete_response is None
                    assert delete_response is None, f"Expected None for 204 No Content, got {delete_response}"
                except Exception as cleanup_exc:
                    errors.append(f"Cleanup failed for policy match rule ID {rule_id}: {cleanup_exc}")

            if app_credential_id:
                try:
                    _, _, err = client.aiguard.llm_application_credentials.delete_credential(app_credential_id)
                    assert err is None, f"Error deleting LLM application credential: {err}"
                except Exception as cleanup_exc:
                    errors.append(f"Cleanup failed for LLM application credential ID {app_credential_id}: {cleanup_exc}")

            if application_id:
                try:
                    _, _, err = client.aiguard.llm_applications.delete_application(application_id)
                    assert err is None, f"Error deleting LLM application: {err}"
                except Exception as cleanup_exc:
                    errors.append(f"Cleanup failed for LLM application ID {application_id}: {cleanup_exc}")

            if policy_id:
                try:
                    _, _, err = client.aiguard.policies.delete_policy(policy_id)
                    assert err is None, f"Error deleting detection policy: {err}"
                except Exception as cleanup_exc:
                    errors.append(f"Cleanup failed for detection policy ID {policy_id}: {cleanup_exc}")

        assert len(errors) == 0, f"Errors occurred during the policy match rule lifecycle test: {errors}"
