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
import logging
from zscaler import ZscalerClient


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
        sweep_functions = [
            self.sweep_groups,
            # self.sweep_users,
        ]

        for func in sweep_functions:
            logging.info(f"Executing {func.__name__}")
            func()

    @suppress_warnings
    def sweep_groups(self):
        logging.info("Starting to sweep groups")
        try:
            groups_response = self.client.zidentity.groups.list_groups()
            # Access the records field from the response object
            groups = groups_response.records if hasattr(groups_response, 'records') else []
            test_groups = [pra for pra in groups if hasattr(pra, "name") and pra.name.startswith("tests-")]
            logging.info(f"Found {len(test_groups)} group named starting with 'tests-' to delete.")

            for group in test_groups:
                logging.info(f"sweep_groups: Attempting to delete pra portal : Name='{group.name}', ID='{group.id}'")
                _ = self.client.zidentity.groups.delete_group(portal_id=group.id)
                logging.info(f"Successfully deleted group ID={group.id}")

        except Exception as e:
            logging.error(f"An error occurred while sweeping groups: {str(e)}")
            raise

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    # Ensure the environment variable is set
    if not os.getenv("ZIDENTITY_SDK_TEST_SWEEP"):
        os.environ["ZIDENTITY_SDK_TEST_SWEEP"] = "true"
        logging.info("Environment variable ZIDENTITY_SDK_TEST_SWEEP was not set. Setting it to true.")

    env_var = os.getenv("ZIDENTITY_SDK_TEST_SWEEP")
    flag_present = "--sweep" in sys.argv
    logging.info(f"Environment variable ZIDENTITY_SDK_TEST_SWEEP: {env_var}")
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
        logging.info("Sweep flag not set or environment variable ZIDENTITY_SDK_TEST_SWEEP is not set to true. Skipping sweep.")
