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
            self.sweep_all_access_policies,
            self.sweep_pra_portal,
            self.sweep_pra_credential,
            self.sweep_pra_approval,
            self.sweep_pra_console,
            self.sweep_app_segments,
            self.sweep_microtenant,
            self.sweep_segment_group,
            self.sweep_server_group,
            self.sweep_provisioning_key,
            self.sweep_lss_controller,
            self.sweep_app_connector_group,
            self.sweep_application_server,
            self.sweep_isolation_banner,
            self.sweep_isolation_certificate,
            self.sweep_isolation_profile,
            self.sweep_service_edge_group,
        ]

        for func in sweep_functions:
            logging.info(f"Executing {func.__name__}")
            func()

    @suppress_warnings
    def sweep_all_access_policies(self):
        logging.info("Starting to sweep access policies")
        policy_types = [
            "access",
            "timeout",
            "client_forwarding",
            "isolation",
            "inspection",
            "redirection",
            "capabilities",
            "siem",
        ]

        try:
            for policy_type in policy_types:
                logging.info(f"Checking for policies of type '{policy_type}'")
                policies = self.client.policies.list_rules(policy_type=policy_type)
                test_policies = [pol for pol in policies if "name" in pol and pol["name"].startswith("tests-")]
                logging.info(f"Found {len(test_policies)} '{policy_type}' policies named starting with 'tests-' to delete.")

                for policy in test_policies:
                    logging.info(
                        f"sweep_all_access_policies: Attempting to delete '{policy_type}' policy: Name='{policy['name']}', ID='{policy['id']}'"
                    )
                    response_code = self.client.policies.delete_rule(policy_type=policy_type, rule_id=policy["id"])
                    if response_code == 204:
                        logging.info(
                            f"Successfully deleted '{policy_type}' policy with ID: {policy['id']}, Name: {policy['name']}"
                        )
                    else:
                        logging.error(
                            f"Failed to delete '{policy_type}' policy with ID: {policy['id']}, Name: {policy['name']} - Status code: {response_code}"
                        )
        except Exception as e:
            logging.error(f"An error occurred while sweeping access policies: {str(e)}")
            raise

    @suppress_warnings
    def sweep_pra_portal(self):
        logging.info("Starting to sweep pra portal")
        try:
            portals = self.client.privileged_remote_access.list_portals()
            test_portals = [pra for pra in portals if "name" in pra and pra["name"].startswith("tests-")]
            logging.info(f"Found {len(test_portals)} pra portal named starting with 'tests-' to delete.")

            for portal in test_portals:
                logging.info(
                    f"sweep_pra_portal: Attempting to delete pra portal : Name='{portal['name']}', ID='{portal['id']}'"
                )
                response_code = self.client.privileged_remote_access.delete_portal(portal_id=portal["id"])
                if response_code == 204:
                    logging.info(f"Successfully deleted pra portal with ID: {portal['id']}, Name: {portal['name']}")
                else:
                    logging.error(
                        f"Failed to delete pra portal with ID: {portal['id']}, Name: {portal['name']} - Status code: {response_code}"
                    )
        except Exception as e:
            logging.error(f"An error occurred while sweeping pra portal: {str(e)}")
            raise

    @suppress_warnings
    def sweep_pra_credential(self):
        logging.info("Starting to sweep pra credential")
        try:
            portals = self.client.privileged_remote_access.list_credentials()
            test_portals = [pra for pra in portals if "name" in pra and pra["name"].startswith("tests-")]
            logging.info(f"Found {len(test_portals)} pra credential named starting with 'tests-' to delete.")

            for credential in test_portals:
                logging.info(
                    f"sweep_pra_credential: Attempting to delete pra credential : Name='{credential['name']}', ID='{credential['id']}'"
                )
                response_code = self.client.privileged_remote_access.delete_credential(credential_id=credential["id"])
                if response_code == 204:
                    logging.info(
                        f"Successfully deleted pra credential with ID: {credential['id']}, Name: {credential['name']}"
                    )
                else:
                    logging.error(
                        f"Failed to delete pra credential with ID: {credential['id']}, Name: {credential['name']} - Status code: {response_code}"
                    )
        except Exception as e:
            logging.error(f"An error occurred while sweeping pra portal: {str(e)}")
            raise

    @suppress_warnings
    def sweep_pra_approval(self):
        logging.info("Starting to sweep pra approval")
        try:
            portals = self.client.privileged_remote_access.list_approval()
            test_portals = [
                pra for pra in portals if "email_ids" in pra and any("tests-" in email for email in pra["email_ids"])
            ]
            logging.info(f"Found {len(test_portals)} pra approvals with email IDs containing 'tests-' to delete.")

            for approval in test_portals:
                logging.info(
                    f"sweep_pra_approval: Attempting to delete pra approval: Name='{approval['name']}', ID='{approval['id']}'"
                )
                response_code = self.client.privileged_remote_access.delete_approval(approval_id=approval["id"])
                if response_code == 204:
                    logging.info(f"Successfully deleted pra approval with ID: {approval['id']}, Name: {approval['name']}")
                else:
                    logging.error(
                        f"Failed to delete pra approval with ID: {approval['id']}, Name: {approval['name']} - Status code: {response_code}"
                    )
        except Exception as e:
            logging.error(f"An error occurred while sweeping pra approvals: {str(e)}")
            raise

    @suppress_warnings
    def sweep_pra_console(self):
        logging.info("Starting to sweep pra console")
        try:
            portals = self.client.privileged_remote_access.list_consoles()
            test_portals = [pra for pra in portals if "name" in pra and pra["name"].startswith("tests-")]
            logging.info(f"Found {len(test_portals)} pra console named starting with 'tests-' to delete.")

            for console in test_portals:
                logging.info(
                    f"sweep_pra_consoles: Attempting to delete pra console : Name='{console['name']}', ID='{console['id']}'"
                )
                response_code = self.client.privileged_remote_access.delete_console(console_id=console["id"])
                if response_code == 204:
                    logging.info(f"Successfully deleted pra console with ID: {console['id']}, Name: {console['name']}")
                else:
                    logging.error(
                        f"Failed to delete pra console with ID: {console['id']}, Name: {console['name']} - Status code: {response_code}"
                    )
        except Exception as e:
            logging.error(f"An error occurred while sweeping pra console: {str(e)}")
            raise

    @suppress_warnings
    def sweep_microtenant(self):
        logging.info("Starting to sweep microtenant")
        try:
            microtenants = self.client.microtenants.list_microtenants()
            test_microtenants = [mic for mic in microtenants if "name" in mic and mic["name"].startswith("tests-")]
            logging.info(f"Found {len(test_microtenants)} microtenant named starting with 'tests-' to delete.")

            for microtenant in test_microtenants:
                logging.info(
                    f"sweep_microtenant: Attempting to delete microtenant : Name='{microtenant['name']}', ID='{microtenant['id']}'"
                )
                response_code = self.client.microtenants.delete_microtenant(console_id=microtenant["id"])
                if response_code == 204:
                    logging.info(f"Successfully deleted microtenant with ID: {microtenant['id']}, Name: {microtenant['name']}")
                else:
                    logging.error(
                        f"Failed to delete microtenant with ID: {microtenant['id']}, Name: {microtenant['name']} - Status code: {response_code}"
                    )
        except Exception as e:
            logging.error(f"An error occurred while sweeping microtenants: {str(e)}")
            raise

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
                    logging.error(
                        f"Failed to delete segment group with ID: {group['id']}, Name: {group['name']} - Status code: {response_code}"
                    )
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
                    logging.error(
                        f"Failed to delete server group with ID: {group['id']}, Name: {group['name']} - Status code: {response_code}"
                    )
        except Exception as e:
            logging.error(f"An error occurred while sweeping server groups: {str(e)}")
            raise

    @suppress_warnings
    def sweep_provisioning_key(self):
        logging.info("Starting to sweep provisioning keys")
        key_types = ["connector", "service_edge"]

        try:
            for key_type in key_types:
                logging.info(f"Checking for provisioning keys of type '{key_type}'")
                provisioning_keys = self.client.provisioning.list_provisioning_keys(key_type=key_type)
                test_provisioning_keys = [
                    key for key in provisioning_keys if "name" in key and key["name"].startswith("tests-")
                ]
                logging.info(f"Found {len(test_provisioning_keys)} '{key_type}' provisioning keys to delete.")

                for provisioning_key in test_provisioning_keys:
                    logging.info(
                        f"sweep_provisioning_key: Attempting to delete '{key_type}' provisioning key: Name='{provisioning_key['name']}', ID='{provisioning_key['id']}'"
                    )
                    response_code = self.client.provisioning.delete_provisioning_key(
                        key_id=provisioning_key["id"], key_type=key_type
                    )
                    if response_code == 204:
                        logging.info(
                            f"Successfully deleted '{key_type}' provisioning key with ID: {provisioning_key['id']}, Name: {provisioning_key['name']}"
                        )
                    else:
                        logging.error(
                            f"Failed to delete '{key_type}' provisioning key with ID: {provisioning_key['id']}, Name: {provisioning_key['name']} - Status code: {response_code}"
                        )
        except Exception as e:
            logging.error(f"An error occurred while sweeping provisioning keys: {str(e)}")
            raise

    @suppress_warnings
    def sweep_lss_controller(self):
        logging.info("Starting to sweep LSS controllers")
        try:
            list_controllers = self.client.lss.list_configs()
            test_controllers = [lss for lss in list_controllers if lss["config"]["name"].startswith("tests-")]
            logging.info(f"Found {len(test_controllers)} LSS controllers to delete.")

            for controller in test_controllers:
                logging.info(
                    f"sweep_lss_controller: Attempting to delete LSS controller: Name='{controller['config']['name']}', ID='{controller['id']}'"
                )
                response_code = self.client.lss.delete_lss_config(lss_config_id=controller["id"])
                if response_code == 204:
                    logging.info(
                        f"Successfully deleted LSS controller with ID: {controller['id']}, Name: {controller['config']['name']}"
                    )
                else:
                    logging.error(
                        f"Failed to delete LSS controller with ID: {controller['id']}, Name: {controller['config']['name']} - Status code: {response_code}"
                    )
        except Exception as e:
            logging.error(f"An error occurred while sweeping LSS controllers: {str(e)}")
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
                    logging.error(
                        f"Failed to delete app servers with ID: {server['id']}, Name: {server['name']} - Status code: {response_code}"
                    )
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
                    logging.error(
                        f"Failed to delete isolation banner with ID: {banner['id']}, Name: {banner['name']} - Status code: {response_code}"
                    )
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

    @suppress_warnings
    def sweep_isolation_certificate(self):
        logging.info("Starting to sweep isolation certificate")
        try:
            certificates = self.client.isolation.list_certificates()
            test_certificates = [cert for cert in certificates if cert["name"].startswith("tests-")]
            logging.info(f"Found {len(test_certificates)} isolation certificates to delete.")

            for certificate in test_certificates:
                logging.info(
                    f"sweep_isolation_certificate: Attempting to delete isolation certificate: Name='{certificate['name']}', ID='{certificate['id']}'"
                )
                response_code = self.client.isolation.delete_certificate(certificate_id=certificate["id"])
                if response_code == 200:
                    logging.info(
                        f"Successfully deleted isolation certificate with ID: {certificate['id']}, Name: {certificate['name']}"
                    )
                else:
                    logging.error(
                        f"Failed to delete isolation certificate with ID: {certificate['id']}, Name: {certificate['name']} - Status code: {response_code}"
                    )
        except Exception as e:
            logging.error(f"An error occurred while sweeping isolation certificates: {str(e)}")
            raise

    @suppress_warnings
    def sweep_service_edge_group(self):
        logging.info("Starting to sweep service edge group")
        try:
            app_connectors = self.client.service_edges.list_service_edge_groups()
            test_groups = [grp for grp in app_connectors if grp["name"].startswith("tests-")]
            logging.info(f"Found {len(test_groups)} service edge groups to delete.")

            for group in test_groups:
                logging.info(
                    f"sweep_service_edge_group: Attempting to delete service edge group: Name='{group['name']}', ID='{group['id']}'"
                )
                response_code = self.client.service_edges.delete_service_edge_group(group_id=group["id"])
                if response_code == 204:
                    logging.info(f"Successfully deleted service edge group with ID: {group['id']}, Name: {group['name']}")
                else:
                    logging.error(
                        f"Failed to delete service edge group with ID: {group['id']}, Name: {group['name']} - Status code: {response_code}"
                    )
        except Exception as e:
            logging.error(f"An error occurred while sweeping service edge groups: {str(e)}")
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
