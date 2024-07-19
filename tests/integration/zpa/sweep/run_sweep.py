import os
import sys
import logging
from zscaler.zpa import ZPAClientHelper


class TestSweepUtility:
    def __init__(self):
        ZPA_CLIENT_ID = os.getenv("ZPA_CLIENT_ID")
        ZPA_CLIENT_SECRET = os.getenv("ZPA_CLIENT_SECRET")
        ZPA_CUSTOMER_ID = os.getenv("ZPA_CUSTOMER_ID")
        ZPA_CLOUD = os.getenv("ZPA_CLOUD")

        self.client = ZPAClientHelper(
            client_id=ZPA_CLIENT_ID, client_secret=ZPA_CLIENT_SECRET, customer_id=ZPA_CUSTOMER_ID, cloud=ZPA_CLOUD
        )

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
            self.sweep_app_segments,
            self.sweep_segment_group,
            self.sweep_server_group,
            self.sweep_app_connector_group,
            self.sweep_application_server,
            self.sweep_isolation_banner,
            self.sweep_isolation_profile,
        ]

        for func in sweep_functions:
            logging.info(f"Executing {func.__name__}")
            func()

    @suppress_warnings
    def sweep_app_segments(self):
        logging.info("Starting to sweep app segments")
        try:
            app_segments = self.client.app_segments.list_segments()
            test_segments = [seg for seg in app_segments if "name" in seg and seg["name"].startswith("tests-")]
            logging.info(f"Found {len(test_segments)} app segments named starting with 'tests-' to delete.")

            for segment in test_segments:
                logging.info(
                    f"sweep_app_segments: Attempting to delete app segment: Name='{segment['name']}', ID='{segment['id']}'"
                )
                response_code = self.client.app_segments.delete_segment(segment_id=segment["id"])
                if response_code == 204:
                    logging.info(f"Successfully deleted app segment with ID: {segment['id']}, Name: {segment['name']}")
                else:
                    logging.error(
                        f"Failed to delete app segment with ID: {segment['id']}, Name: {segment['name']} - Status code: {response_code}"
                    )
        except Exception as e:
            logging.error(f"An error occurred while sweeping app segments: {str(e)}")
            raise

    @suppress_warnings
    def sweep_segment_group(self):
        logging.info("Starting to sweep segment group")
        try:
            segment_groups = self.client.segment_groups.list_groups()
            test_groups = [grp for grp in segment_groups if grp["name"].startswith("tests-")]
            logging.info(f"Found {len(test_groups)} segment group to delete.")

            for group in test_groups:
                logging.info(
                    f"sweep_segment_group: Attempting to delete segment group: Name='{group['name']}', ID='{group['id']}'"
                )
                response_code = self.client.segment_groups.delete_group(group_id=group["id"])
                if response_code == 204:
                    logging.info(f"Successfully deleted segment group with ID: {group['id']}, Name: {group['name']}")
                else:
                    logging.error(f"Failed to delete segment group with ID: {group['id']}, Name: {group['name']} - Status code: {response_code}")
        except Exception as e:
            logging.error(f"An error occurred while sweeping segment groups: {str(e)}")
            raise

    @suppress_warnings
    def sweep_server_group(self):
        logging.info("Starting to sweep server group")
        try:
            server_groups = self.client.server_groups.list_groups()
            test_groups = [grp for grp in server_groups if grp["name"].startswith("tests-")]
            logging.info(f"Found {len(test_groups)} server groups to delete.")

            for group in test_groups:
                logging.info(
                    f"sweep_server_group: Attempting to delete server group: Name='{group['name']}', ID='{group['id']}'"
                )
                response_code = self.client.server_groups.delete_group(group_id=group["id"])
                if response_code == 204:
                    logging.info(f"Successfully deleted server group with ID: {group['id']}, Name: {group['name']}")
                else:
                    logging.error(f"Failed to delete server group with ID: {group['id']}, Name: {group['name']} - Status code: {response_code}")
        except Exception as e:
            logging.error(f"An error occurred while sweeping server groups: {str(e)}")
            raise

    @suppress_warnings
    def sweep_app_connector_group(self):
        logging.info("Starting to sweep app connector group")
        try:
            app_connectors = self.client.connectors.list_connector_groups()
            test_groups = [grp for grp in app_connectors if grp["name"].startswith("tests-")]
            logging.info(f"Found {len(test_groups)} app connector groups to delete.")

            for group in test_groups:
                logging.info(
                    f"sweep_app_connector_group: Attempting to delete app connector group: Name='{group['name']}', ID='{group['id']}'"
                )
                response_code = self.client.connectors.delete_connector_group(group_id=group["id"])
                if response_code == 204:
                    logging.info(f"Successfully deleted app connector group with ID: {group['id']}, Name: {group['name']}")
                else:
                    logging.error(
                        f"Failed to delete app connector group with ID: {group['id']}, Name: {group['name']} - Status code: {response_code}"
                    )
        except Exception as e:
            logging.error(f"An error occurred while sweeping app connector groups: {str(e)}")
            raise

    @suppress_warnings
    def sweep_application_server(self):
        logging.info("Starting to sweep app servers")
        try:
            app_servers = self.client.servers.list_servers()
            test_servers = [grp for grp in app_servers if grp["name"].startswith("tests-")]
            logging.info(f"Found {len(test_servers)} app servers to delete.")

            for server in test_servers:
                logging.info(
                    f"sweep_application_server: Attempting to delete app servers: Name='{server['name']}', ID='{server['id']}'"
                )
                response_code = self.client.servers.delete_server(server_id=server["id"])
                if response_code == 204:
                    logging.info(f"Successfully deleted app servers with ID: {server['id']}, Name: {server['name']}")
                else:
                    logging.error(f"Failed to delete app servers with ID: {server['id']}, Name: {server['name']} - Status code: {response_code}")
        except Exception as e:
            logging.error(f"An error occurred while sweeping app servers: {str(e)}")
            raise

    @suppress_warnings
    def sweep_isolation_banner(self):
        logging.info("Starting to sweep isolation banner")
        try:
            banners = self.client.isolation.list_banners()
            test_banners = [grp for grp in banners if grp["name"].startswith("tests-")]
            logging.info(f"Found {len(test_banners)} isolation banners to delete.")

            for banner in test_banners:
                logging.info(
                    f"sweep_isolation_banner: Attempting to delete isolation banner: Name='{banner['name']}', ID='{banner['id']}'"
                )
                response_code = self.client.isolation.delete_banner(banner_id=banner["id"])
                if response_code == 200:
                    logging.info(f"Successfully deleted isolation banner with ID: {banner['id']}, Name: {banner['name']}")
                else:
                    logging.error(f"Failed to delete isolation banner with ID: {banner['id']}, Name: {banner['name']} - Status code: {response_code}")
        except Exception as e:
            logging.error(f"An error occurred while sweeping isolation banners: {str(e)}")
            raise

    @suppress_warnings
    def sweep_isolation_profile(self):
        logging.info("Starting to sweep isolation profile")
        try:
            profiles = self.client.isolation.list_cbi_profiles()
            test_profiles = [grp for grp in profiles if grp["name"].startswith("tests-")]
            logging.info(f"Found {len(test_profiles)} isolation profiles to delete.")

            for profile in test_profiles:
                logging.info(
                    f"sweep_isolation_profile: Attempting to delete isolation profile: Name='{profile['name']}', ID='{profile['id']}'"
                )
                response_code = self.client.isolation.delete_cbi_profile(profile_id=profile["id"])
                if response_code == 204:
                    logging.info(f"Successfully deleted isolation profile with ID: {profile['id']}, Name: {profile['name']}")
                else:
                    logging.error(
                        f"Failed to delete isolation profile with ID: {profile['id']}, Name: {profile['name']} - Status code: {response_code}"
                    )
        except Exception as e:
            logging.error(f"An error occurred while sweeping isolation profiles: {str(e)}")
            raise


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    # Ensure the environment variable is set
    if not os.getenv("ZPA_SDK_TEST_SWEEP"):
        os.environ["ZPA_SDK_TEST_SWEEP"] = "true"
        logging.info("Environment variable ZPA_SDK_TEST_SWEEP was not set. Setting it to true.")

    env_var = os.getenv("ZPA_SDK_TEST_SWEEP")
    flag_present = "--sweep" in sys.argv
    logging.info(f"Environment variable ZPA_SDK_TEST_SWEEP: {env_var}")
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
        logging.info("Sweep flag not set or environment variable ZPA_SDK_TEST_SWEEP is not set to true. Skipping sweep.")