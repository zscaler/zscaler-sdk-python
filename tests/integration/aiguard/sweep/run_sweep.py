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

import os
import sys
from pathlib import Path

# Add project root to path so zscaler is importable when run as script
_project_root = Path(__file__).resolve().parent.parent.parent.parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

import logging  # noqa: E402

from zscaler import ZscalerClient  # noqa: E402


class TestSweepUtility:
    def __init__(self, config=None):
        """
        Initializes the TestSweepUtility with ZscalerClient configuration.
        """
        config = config or {}

        client_id = config.get("clientId", os.getenv("ZSCALER_CLIENT_ID"))
        client_secret = config.get("clientSecret", os.getenv("ZSCALER_CLIENT_SECRET"))
        vanity_domain = config.get("vanityDomain", os.getenv("ZSCALER_VANITY_DOMAIN"))
        cloud = config.get("cloud", os.getenv("ZSCALER_CLOUD", "PRODUCTION"))

        logging_config = config.get("logging", {"enabled": False, "verbose": False})

        client_config = {
            "clientId": client_id,
            "clientSecret": client_secret,
            "vanityDomain": vanity_domain,
            "cloud": cloud,
            "logging": {"enabled": logging_config.get("enabled", True), "verbose": logging_config.get("verbose", True)},
        }

        self.client = ZscalerClient(client_config)

    def suppress_warnings(func):
        def wrapper(*args, **kwargs):
            previous_level = logging.getLogger().level
            logging.getLogger().setLevel(logging.ERROR)
            result = func(*args, **kwargs)
            logging.getLogger().setLevel(previous_level)
            return result

        return wrapper

    def run_sweep_functions(self):
        # Ordered so that dependent resources are removed before their parents.
        sweep_functions = [
            self.sweep_llm_application_credentials,
            self.sweep_llm_provider_credentials,
            self.sweep_policy_match_rules,
            self.sweep_policies,
            self.sweep_llm_applications,
            self.sweep_llm_providers,
        ]

        for func in sweep_functions:
            logging.info(f"Executing {func.__name__}")
            func()

    @suppress_warnings
    def sweep_policies(self):
        logging.info("Starting to sweep detection policies")
        try:
            policies, _, error = self.client.aiguard.policies.list_policies()
            if error:
                raise Exception(f"Error listing detection policies: {error}")

            test_policies = [p for p in (policies or []) if hasattr(p, "name") and p.name.startswith("tests-")]
            logging.info(f"Found {len(test_policies)} detection policies named starting with 'tests-' to delete.")

            for policy in test_policies:
                logging.info(f"sweep_policies: Attempting to delete detection policy: Name='{policy.name}', ID='{policy.id}'")
                _, _, error = self.client.aiguard.policies.delete_policy(policy.id)
                if error:
                    logging.error(f"Failed to delete detection policy ID={policy.id} — {error}")
                else:
                    logging.info(f"Successfully deleted detection policy ID={policy.id}")

        except Exception as e:
            logging.error(f"An error occurred while sweeping detection policies: {str(e)}")
            raise

    @suppress_warnings
    def sweep_policy_match_rules(self):
        logging.info("Starting to sweep policy match rules")
        try:
            rules, _, error = self.client.aiguard.policy_match_rules.list_rules()
            if error:
                raise Exception(f"Error listing policy match rules: {error}")

            test_rules = [r for r in (rules or []) if hasattr(r, "name") and r.name.startswith("tests-")]
            logging.info(f"Found {len(test_rules)} policy match rules named starting with 'tests-' to delete.")

            for rule in test_rules:
                logging.info(
                    f"sweep_policy_match_rules: Attempting to delete policy match rule: Name='{rule.name}', ID='{rule.id}'"
                )
                _, _, error = self.client.aiguard.policy_match_rules.delete_rule(rule.id)
                if error:
                    logging.error(f"Failed to delete policy match rule ID={rule.id} — {error}")
                else:
                    logging.info(f"Successfully deleted policy match rule ID={rule.id}")

        except Exception as e:
            logging.error(f"An error occurred while sweeping policy match rules: {str(e)}")
            raise

    @suppress_warnings
    def sweep_llm_applications(self):
        logging.info("Starting to sweep LLM applications")
        try:
            applications, _, error = self.client.aiguard.llm_applications.list_applications()
            if error:
                raise Exception(f"Error listing LLM applications: {error}")

            test_applications = [a for a in (applications or []) if hasattr(a, "name") and a.name.startswith("tests-")]
            logging.info(f"Found {len(test_applications)} LLM applications named starting with 'tests-' to delete.")

            for application in test_applications:
                logging.info(
                    f"sweep_llm_applications: Attempting to delete LLM application: "
                    f"Name='{application.name}', ID='{application.id}'"
                )
                _, _, error = self.client.aiguard.llm_applications.delete_application(application.id)
                if error:
                    logging.error(f"Failed to delete LLM application ID={application.id} — {error}")
                else:
                    logging.info(f"Successfully deleted LLM application ID={application.id}")

        except Exception as e:
            logging.error(f"An error occurred while sweeping LLM applications: {str(e)}")
            raise

    @suppress_warnings
    def sweep_llm_providers(self):
        logging.info("Starting to sweep LLM providers")
        try:
            providers, _, error = self.client.aiguard.llm_providers.list_providers()
            if error:
                raise Exception(f"Error listing LLM providers: {error}")

            test_providers = [p for p in (providers or []) if hasattr(p, "name") and p.name.startswith("tests-")]
            logging.info(f"Found {len(test_providers)} LLM providers named starting with 'tests-' to delete.")

            for provider in test_providers:
                logging.info(
                    f"sweep_llm_providers: Attempting to delete LLM provider: Name='{provider.name}', ID='{provider.id}'"
                )
                _, _, error = self.client.aiguard.llm_providers.delete_provider(provider.id)
                if error:
                    logging.error(f"Failed to delete LLM provider ID={provider.id} — {error}")
                else:
                    logging.info(f"Successfully deleted LLM provider ID={provider.id}")

        except Exception as e:
            logging.error(f"An error occurred while sweeping LLM providers: {str(e)}")
            raise

    @suppress_warnings
    def sweep_llm_provider_credentials(self):
        logging.info("Starting to sweep LLM provider credentials")
        try:
            # The LlmProviderCredentials model does not expose an id attribute, so the raw
            # response body is used to pair each credential name with its id.
            _, response, error = self.client.aiguard.llm_provider_credentials.list_credentials()
            if error:
                raise Exception(f"Error listing LLM provider credentials: {error}")

            items = (response.get_body() or {}).get("items", []) if response else []
            test_credentials = [i for i in items if str(i.get("name", "")).startswith("tests-")]
            logging.info(f"Found {len(test_credentials)} LLM provider credentials named starting with 'tests-' to delete.")

            for credential in test_credentials:
                logging.info(
                    f"sweep_llm_provider_credentials: Attempting to delete LLM provider credential: "
                    f"Name='{credential.get('name')}', ID='{credential.get('id')}'"
                )
                _, _, error = self.client.aiguard.llm_provider_credentials.delete_credential(credential.get("id"))
                if error:
                    logging.error(f"Failed to delete LLM provider credential ID={credential.get('id')} — {error}")
                else:
                    logging.info(f"Successfully deleted LLM provider credential ID={credential.get('id')}")

        except Exception as e:
            logging.error(f"An error occurred while sweeping LLM provider credentials: {str(e)}")
            raise

    @suppress_warnings
    def sweep_llm_application_credentials(self):
        logging.info("Starting to sweep LLM application credentials")
        try:
            credentials, _, error = self.client.aiguard.llm_application_credentials.list_credentials()
            if error:
                raise Exception(f"Error listing LLM application credentials: {error}")

            test_credentials = [c for c in (credentials or []) if hasattr(c, "name") and c.name.startswith("tests-")]
            logging.info(f"Found {len(test_credentials)} LLM application credentials named starting with 'tests-' to delete.")

            for credential in test_credentials:
                logging.info(
                    f"sweep_llm_application_credentials: Attempting to delete LLM application credential: "
                    f"Name='{credential.name}', ID='{credential.id}'"
                )
                _, _, error = self.client.aiguard.llm_application_credentials.delete_credential(credential.id)
                if error:
                    logging.error(f"Failed to delete LLM application credential ID={credential.id} — {error}")
                else:
                    logging.info(f"Successfully deleted LLM application credential ID={credential.id}")

        except Exception as e:
            logging.error(f"An error occurred while sweeping LLM application credentials: {str(e)}")
            raise


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    # Ensure the environment variable is set
    if not os.getenv("AIGUARD_SDK_TEST_SWEEP"):
        os.environ["AIGUARD_SDK_TEST_SWEEP"] = "true"
        logging.info("Environment variable AIGUARD_SDK_TEST_SWEEP was not set. Setting it to true.")

    env_var = os.getenv("AIGUARD_SDK_TEST_SWEEP")
    flag_present = "--sweep" in sys.argv
    logging.info(f"Environment variable AIGUARD_SDK_TEST_SWEEP: {env_var}")
    logging.info(f"Sweep flag presence: {flag_present}")

    if env_var == "true" and flag_present:
        sweeper = TestSweepUtility()

        # Pre-test sweep
        logging.info("Running pre-test sweep.")
        sweeper.run_sweep_functions()

        # Placeholder for main test execution
        logging.info("Executing main test suite...")
        # Insert your test suite execution here

        # Post-test sweep
        logging.info("Running post-test sweep.")
        sweeper.run_sweep_functions()
    else:
        logging.info("Sweep flag not set or environment variable AIGUARD_SDK_TEST_SWEEP is not set to true. Skipping sweep.")
