import os
import sys
import logging
from zscaler.zia import ZIAClientHelper


class TestSweepUtility:
    def __init__(self):
        ZIA_USERNAME = os.getenv("ZIA_USERNAME")
        ZIA_PASSWORD = os.getenv("ZIA_PASSWORD")
        ZIA_API_KEY = os.getenv("ZIA_API_KEY")
        ZIA_CLOUD = os.getenv("ZIA_CLOUD")

        self.client = ZIAClientHelper(username=ZIA_USERNAME, password=ZIA_PASSWORD, api_key=ZIA_API_KEY, cloud=ZIA_CLOUD)

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
            self.sweep_rule_labels,
            self.sweep_cloud_firewall_rule,
            self.sweep_cloud_firewall_ip_source_group,
            self.sweep_cloud_firewall_ip_destination_group,
            self.sweep_cloud_firewall_network_app_group,
            self.sweep_cloud_firewall_network_service_group,
            self.sweep_cloud_firewall_network_service,
            self.sweep_dlp_web_rule,
            self.sweep_url_filtering_rule,
            self.sweep_location_management,
            self.sweep_gre_tunnels,
            self.sweep_vpn_credentials,
            self.sweep_static_ip,
            self.sweep_dlp_engine,
            self.sweep_dlp_dictionary,
            self.sweep_dlp_template,
            self.sweep_zpa_gateway,
        ]

        for func in sweep_functions:
            logging.info(f"Executing {func.__name__}")
            func()

    @suppress_warnings
    def sweep_rule_labels(self):
        logging.info("Starting to sweep rule labels")
        try:
            labels = self.client.labels.list_labels()
            test_labels = [lab for lab in labels if "name" in lab and lab["name"].startswith("tests-")]
            logging.info(f"Found {len(test_labels)} rule labels named starting with 'tests-' to delete.")

            for label in test_labels:
                logging.info(
                    f"sweep_rule_labels: Attempting to delete rule labels: Name='{label['name']}', ID='{label['id']}'"
                )
                response_code = self.client.labels.delete_label(label_id=label["id"])
                if response_code == 204:
                    logging.info(f"Successfully deleted rule label with ID: {label['id']}, Name: {label['name']}")
                else:
                    logging.error(
                        f"Failed to delete rule labelwith ID: {label['id']}, Name: {label['name']} - Status code: {response_code}"
                    )
        except Exception as e:
            logging.error(f"An error occurred while sweeping rule labels: {str(e)}")
            raise

    @suppress_warnings
    def sweep_cloud_firewall_rule(self):
        logging.info("Starting to sweep cloud firewall rule")
        try:
            rules = self.client.firewall.list_rules()
            test_rules = [fw for fw in rules if fw["name"].startswith("tests-")]
            logging.info(f"Found {len(test_rules)} cloud firewall rule to delete.")

            for rule in test_rules:
                logging.info(
                    f"sweep_cloud_firewall_rule: Attempting to delete cloud firewall rule: Name='{rule['name']}', ID='{rule['id']}'"
                )
                response_code = self.client.firewall.delete_rule(rule_id=rule["id"])
                if response_code == 204:
                    logging.info(f"Successfully deleted cloud firewall rule with ID: {rule['id']}, Name: {rule['name']}")
                else:
                    logging.error(
                        f"Failed to delete cloud firewall rule with ID: {rule['id']}, Name: {rule['name']} - Status code: {response_code}"
                    )
        except Exception as e:
            logging.error(f"An error occurred while sweeping cloud firewall rules: {str(e)}")
            raise

    @suppress_warnings
    def sweep_cloud_app_control_rule(self, rule_type: str):
        logging.info("Starting to sweep cloud app control rule")
        try:
            rules = self.client.cloudappcontrol.list_rules(rule_type)
            test_rules = [fw for fw in rules if fw["name"].startswith("tests-")]
            logging.info(f"Found {len(test_rules)} cloud app control rules to delete.")

            for rule in test_rules:
                logging.info(
                    f"sweep_cloud_app_control_rule: Attempting to delete cloud app control rule: Name='{rule['name']}', ID='{rule['id']}'"
                )
                response_code = self.client.cloudappcontrol.delete_rule(rule_type, rule["id"])
                if response_code == 204:
                    logging.info(f"Successfully deleted cloud app control rule with ID: {rule['id']}, Name: {rule['name']}")
                else:
                    logging.error(
                        f"Failed to delete cloud app control rule with ID: {rule['id']}, Name: {rule['name']} - Status code: {response_code}"
                    )
        except Exception as e:
            logging.error(f"An error occurred while sweeping cloud app control rules: {str(e)}")
            raise

    @suppress_warnings
    def sweep_cloud_firewall_ip_source_group(self):
        logging.info("Starting to sweep cloud firewall ip source group")
        try:
            groups = self.client.firewall.list_ip_source_groups()
            test_groups = [grp for grp in groups if grp["name"].startswith("tests-")]
            logging.info(f"Found {len(test_groups)} cloud firewall ip source group to delete.")

            for group in test_groups:
                logging.info(
                    f"sweep_cloud_firewall_ip_source_group: Attempting to delete cloud firewall ip source group: Name='{group['name']}', ID='{group['id']}'"
                )
                response_code = self.client.firewall.delete_ip_source_group(group_id=group["id"])
                if response_code == 204:
                    logging.info(
                        f"Successfully deleted cloud firewall ip source group with ID: {group['id']}, Name: {group['name']}"
                    )
                else:
                    logging.error(
                        f"Failed to delete cloud firewall ip source group with ID: {group['id']}, Name: {group['name']} - Status code: {response_code}"
                    )
        except Exception as e:
            logging.error(f"An error occurred while sweeping cloud firewall ip source groups: {str(e)}")
            raise

    @suppress_warnings
    def sweep_cloud_firewall_ip_destination_group(self):
        logging.info("Starting to sweep cloud firewall ip destination group")
        try:
            groups = self.client.firewall.list_ip_destination_groups()
            test_groups = [grp for grp in groups if grp["name"].startswith("tests-")]
            logging.info(f"Found {len(test_groups)} cloud firewall ip destination group to delete.")

            for group in test_groups:
                logging.info(
                    f"sweep_cloud_firewall_ip_destination_group: Attempting to delete cloud firewall ip destination group: Name='{group['name']}', ID='{group['id']}'"
                )
                response_code = self.client.firewall.delete_ip_destination_group(group_id=group["id"])
                if response_code == 204:
                    logging.info(
                        f"Successfully deleted cloud firewall ip destination group with ID: {group['id']}, Name: {group['name']}"
                    )
                else:
                    logging.error(
                        f"Failed to delete cloud firewall ip destination group with ID: {group['id']}, Name: {group['name']} - Status code: {response_code}"
                    )
        except Exception as e:
            logging.error(f"An error occurred while sweeping cloud firewall ip destination groups: {str(e)}")
            raise

    @suppress_warnings
    def sweep_cloud_firewall_network_app_group(self):
        logging.info("Starting to sweep cloud firewall network app group")
        try:
            groups = self.client.firewall.list_network_app_groups()
            test_groups = [grp for grp in groups if grp["name"].startswith("tests-")]
            logging.info(f"Found {len(test_groups)} cloud firewall network app group to delete.")

            for group in test_groups:
                logging.info(
                    f"sweep_cloud_firewall_network_app_group: Attempting to delete cloud firewall network app group: Name='{group['name']}', ID='{group['id']}'"
                )
                response_code = self.client.firewall.delete_network_app_group(group_id=group["id"])
                if response_code == 204:
                    logging.info(
                        f"Successfully deleted cloud firewall network app group with ID: {group['id']}, Name: {group['name']}"
                    )
                else:
                    logging.error(
                        f"Failed to delete cloud firewall network app group with ID: {group['id']}, Name: {group['name']} - Status code: {response_code}"
                    )
        except Exception as e:
            logging.error(f"An error occurred while sweeping cloud firewall network app groups: {str(e)}")
            raise

    @suppress_warnings
    def sweep_cloud_firewall_network_service_group(self):
        logging.info("Starting to sweep cloud firewall network service group")
        try:
            groups = self.client.firewall.list_network_svc_groups()
            test_groups = [grp for grp in groups if grp["name"].startswith("tests-")]
            logging.info(f"Found {len(test_groups)} cloud firewall network service group to delete.")

            for group in test_groups:
                logging.info(
                    f"sweep_cloud_firewall_network_service_group: Attempting to delete cloud firewall network service group: Name='{group['name']}', ID='{group['id']}'"
                )
                response_code = self.client.firewall.delete_network_svc_group(group_id=group["id"])
                if response_code == 204:
                    logging.info(
                        f"Successfully deleted cloud firewall network service group with ID: {group['id']}, Name: {group['name']}"
                    )
                else:
                    logging.error(
                        f"Failed to delete cloud firewall network service group with ID: {group['id']}, Name: {group['name']} - Status code: {response_code}"
                    )
        except Exception as e:
            logging.error(f"An error occurred while sweeping cloud firewall network service groups: {str(e)}")
            raise

    @suppress_warnings
    def sweep_cloud_firewall_network_service(self):
        logging.info("Starting to sweep cloud firewall network service")
        try:
            groups = self.client.firewall.list_network_services()
            test_groups = [grp for grp in groups if grp["name"].startswith("tests-")]
            logging.info(f"Found {len(test_groups)} cloud firewall network service to delete.")

            for group in test_groups:
                logging.info(
                    f"sweep_cloud_firewall_network_service: Attempting to delete cloud firewall network service: Name='{group['name']}', ID='{group['id']}'"
                )
                response_code = self.client.firewall.delete_network_service(group_id=group["id"])
                if response_code == 204:
                    logging.info(
                        f"Successfully deleted cloud firewall network service with ID: {group['id']}, Name: {group['name']}"
                    )
                else:
                    logging.error(
                        f"Failed to delete cloud firewall network service with ID: {group['id']}, Name: {group['name']} - Status code: {response_code}"
                    )
        except Exception as e:
            logging.error(f"An error occurred while sweeping cloud firewall network services: {str(e)}")
            raise

    @suppress_warnings
    def sweep_dlp_web_rule(self):
        logging.info("Starting to sweep dlp web rule")
        try:
            rules = self.client.web_dlp.list_rules()
            test_rules = [fw for fw in rules if fw["name"].startswith("tests-")]
            logging.info(f"Found {len(test_rules)} dlp web rule to delete.")

            for rule in test_rules:
                logging.info(
                    f"sweep_dlp_web_rule: Attempting to delete dlp web rule: Name='{rule['name']}', ID='{rule['id']}'"
                )
                response_code = self.client.web_dlp.delete_rule(rule_id=rule["id"])
                if response_code == 204:
                    logging.info(f"Successfully deleted url dlp web rule with ID: {rule['id']}, Name: {rule['name']}")
                else:
                    logging.error(
                        f"Failed to delete dlp web rule with ID: {rule['id']}, Name: {rule['name']} - Status code: {response_code}"
                    )
        except Exception as e:
            logging.error(f"An error occurred while sweeping dlp web rules: {str(e)}")
            raise

    @suppress_warnings
    def sweep_forwarding_control_rule(self):
        logging.info("Starting to sweep forwarding control rule")
        try:
            rules = self.client.forwarding_control.list_rules()
            test_rules = [fw for fw in rules if fw["name"].startswith("tests-")]
            logging.info(f"Found {len(test_rules)} forwarding control rule to delete.")

            for rule in test_rules:
                logging.info(
                    f"sweep_forwarding_control_rule: Attempting to delete forwarding control rule: Name='{rule['name']}', ID='{rule['id']}'"
                )
                response_code = self.client.forwarding_control.delete_rule(rule_id=rule["id"])
                if response_code == 204:
                    logging.info(f"Successfully deleted url forwarding control with ID: {rule['id']}, Name: {rule['name']}")
                else:
                    logging.error(
                        f"Failed to delete forwarding control rule with ID: {rule['id']}, Name: {rule['name']} - Status code: {response_code}"
                    )
        except Exception as e:
            logging.error(f"An error occurred while sweeping forwarding controlrules: {str(e)}")
            raise

    @suppress_warnings
    def sweep_url_filtering_rule(self):
        logging.info("Starting to sweep url filtering rule")
        try:
            rules = self.client.url_filtering.list_rules()
            test_rules = [fw for fw in rules if fw["name"].startswith("tests-")]
            logging.info(f"Found {len(test_rules)} url filtering rule to delete.")

            for rule in test_rules:
                logging.info(
                    f"sweep_url_filtering_rule: Attempting to delete url filtering rule: Name='{rule['name']}', ID='{rule['id']}'"
                )
                response_code = self.client.url_filtering.delete_rule(rule_id=rule["id"])
                if response_code == 204:
                    logging.info(f"Successfully deleted url filtering rule with ID: {rule['id']}, Name: {rule['name']}")
                else:
                    logging.error(
                        f"Failed to delete url filtering rule with ID: {rule['id']}, Name: {rule['name']} - Status code: {response_code}"
                    )
        except Exception as e:
            logging.error(f"An error occurred while sweeping url filtering rules: {str(e)}")
            raise

    @suppress_warnings
    def sweep_location_management(self):
        logging.info("Starting to sweep location management")
        try:
            locations = self.client.locations.list_locations()
            test_locations = [loc for loc in locations if loc["name"].startswith("tests-")]
            location_ids = [loc["id"] for loc in test_locations]
            logging.info(f"Found {len(test_locations)} location management to delete.")

            if location_ids:
                logging.info(f"sweep_location_management: Attempting to bulk delete location management: IDs={location_ids}")
                response_code = self.client.locations.bulk_delete_locations(location_ids=location_ids)
                if response_code == 204:
                    logging.info(f"Successfully bulk deleted location management with IDs: {location_ids}")
                else:
                    logging.error(
                        f"Failed to bulk delete location management with IDs: {location_ids} - Status code: {response_code}"
                    )
            else:
                logging.info("No test locations found to delete.")

        except Exception as e:
            logging.error(f"An error occurred while sweeping location management: {str(e)}")
            raise

    @suppress_warnings
    def sweep_vpn_credentials(self):
        logging.info("Starting to sweep VPN credentials")
        try:
            credentials = self.client.traffic.list_vpn_credentials(type="UFQDN")
            test_creds = [vpn for vpn in credentials if vpn["type"] == "UFQDN" and "fqdn" in vpn and "tests-" in vpn["fqdn"]]
            credential_ids = [vpn["id"] for vpn in test_creds]
            logging.info(f"Found {len(test_creds)} VPN credentials to delete.")

            if credential_ids:
                logging.info(f"sweep_vpn_credentials: Attempting to bulk delete VPN credentials: IDs={credential_ids}")
                response_code = self.client.traffic.bulk_delete_vpn_credentials(credential_ids=credential_ids)
                if response_code == 204:
                    logging.info(f"Successfully bulk deleted VPN credentials with IDs: {credential_ids}")
                else:
                    logging.error(
                        f"Failed to bulk delete VPN credentials with IDs: {credential_ids} - Status code: {response_code}"
                    )
            else:
                logging.info("No test VPN credentials found to delete.")

        except Exception as e:
            logging.error(f"An error occurred while sweeping VPN credentials: {str(e)}")
            raise

    @suppress_warnings
    def sweep_gre_tunnels(self):
        logging.info("Starting to gre tunnel")
        try:
            gre_tunnels = self.client.traffic.list_gre_tunnels()
            test_gre_tunnels = [gre for gre in gre_tunnels if "comment" in gre and gre["comment"].startswith("tests-")]
            logging.info(f"Found {len(test_gre_tunnels)} gre tunnel to delete.")

            for gre_tunnel in test_gre_tunnels:
                logging.info(
                    f"sweep_gre_tunnels: Attempting to delete gre tunnel: Comment='{gre_tunnel['comment']}', ID='{gre_tunnel['id']}'"
                )
                response_code = self.client.traffic.delete_gre_tunnel(tunnel_id=gre_tunnel["id"])
                if response_code == 204:
                    logging.info(
                        f"Successfully deleted gre tunnel with ID: {gre_tunnel['id']}, Comment: {gre_tunnel['comment']}"
                    )
                else:
                    logging.error(
                        f"Failed to delete gre tunnel with ID: {gre_tunnel['id']}, Comment: {gre_tunnel['comment']} - Status code: {response_code}"
                    )
        except Exception as e:
            logging.error(f"An error occurred while sweeping gre tunnels: {str(e)}")
            raise

    @suppress_warnings
    def sweep_static_ip(self):
        logging.info("Starting to static ip")
        try:
            static_ips = self.client.traffic.list_static_ips()
            test_static_ips = [ip for ip in static_ips if "comment" in ip and ip["comment"].startswith("tests-")]
            logging.info(f"Found {len(test_static_ips)} static ip to delete.")

            for static_ip in test_static_ips:
                logging.info(
                    f"sweep_static_ip: Attempting to delete static ip: Comment='{static_ip['comment']}', ID='{static_ip['id']}'"
                )
                response_code = self.client.traffic.delete_static_ip(static_ip_id=static_ip["id"])
                if response_code == 204:
                    logging.info(f"Successfully deleted static ip with ID: {static_ip['id']}, Comment: {static_ip['comment']}")
                else:
                    logging.error(
                        f"Failed to delete static ipwith ID: {static_ip['id']}, Comment: {static_ip['comment']} - Status code: {response_code}"
                    )
        except Exception as e:
            logging.error(f"An error occurred while sweeping static ips: {str(e)}")
            raise

    @suppress_warnings
    def sweep_dlp_engine(self):
        logging.info("Starting to sweep dlp engine")
        try:
            engines = self.client.dlp.list_dlp_engines()
            test_engines = [dlp for dlp in engines if "name" in dlp and dlp["name"].startswith("tests-")]
            logging.info(f"Found {len(test_engines)} dlp engines to delete.")

            for engine in test_engines:
                logging.info(
                    f"sweep_dlp_engine: Attempting to delete dlp engine: Name='{engine['name']}', ID='{engine['id']}'"
                )
                response_code = self.client.dlp.delete_dlp_engine(engine_id=engine["id"])
                if response_code == 204:
                    logging.info(f"Successfully deleted dlp engine with ID: {engine['id']}, Name: {engine['name']}")
                else:
                    logging.error(
                        f"Failed to delete dlp engine with ID: {engine['id']}, Name: {engine['name']} - Status code: {response_code}"
                    )
        except Exception as e:
            logging.error(f"An error occurred while sweeping dlp engines: {str(e)}")
            raise

    @suppress_warnings
    def sweep_dlp_dictionary(self):
        logging.info("Starting to sweep dlp dictionary")
        try:
            dictionaries = self.client.dlp.list_dicts()
            test_dictionaries = [dlp for dlp in dictionaries if "name" in dlp and dlp["name"].startswith("tests-")]
            logging.info(f"Found {len(test_dictionaries)} dlp dictionary to delete.")

            for dictionary in test_dictionaries:
                logging.info(
                    f"sweep_dlp_dictionary: Attempting to delete dlp dictionary: Name='{dictionary['name']}', ID='{dictionary['id']}'"
                )
                response_code = self.client.dlp.delete_dict(dict_id=dictionary["id"])
                if response_code == 204:
                    logging.info(
                        f"Successfully deleted dlp dictionary with ID: {dictionary['id']}, Name: {dictionary['name']}"
                    )
                else:
                    logging.error(
                        f"Failed to delete dlp dictionary with ID: {dictionary['id']}, Name: {dictionary['name']} - Status code: {response_code}"
                    )
        except Exception as e:
            logging.error(f"An error occurred while sweeping dlp dictionaries: {str(e)}")
            raise

    @suppress_warnings
    def sweep_dlp_template(self):
        logging.info("Starting to sweep dlp notification template")
        try:
            templates = self.client.dlp.list_dlp_templates()
            test_templates = [dlp for dlp in templates if "name" in dlp and dlp["name"].startswith("tests-")]
            logging.info(f"Found {len(test_templates)} dlp notification template to delete.")

            for template in test_templates:
                logging.info(
                    f"sweep_dlp_template: Attempting to delete dlp notification template: Name='{template['name']}', ID='{template['id']}'"
                )
                response_code = self.client.dlp.delete_dlp_template(template_id=template["id"])
                if response_code == 204:
                    logging.info(
                        f"Successfully deleted dlp notification template with ID: {template['id']}, Name: {template['name']}"
                    )
                else:
                    logging.error(
                        f"Failed to delete dlp notification template with ID: {template['id']}, Name: {template['name']} - Status code: {response_code}"
                    )
        except Exception as e:
            logging.error(f"An error occurred while sweeping dlp notification templates: {str(e)}")
            raise

    @suppress_warnings
    def sweep_zpa_gateway(self):
        logging.info("Starting to sweep zpa gateway")
        try:
            gateways = self.client.zpa_gateway.list_gateways()
            test_gateways = [gw for gw in gateways if "name" in gw and gw["name"].startswith("tests-")]
            logging.info(f"Found {len(test_gateways)} zpa gateway to delete.")

            for gateway in test_gateways:
                logging.info(
                    f"sweep_zpa_gateway: Attempting to delete zpa gateway: Name='{gateway['name']}', ID='{gateway['id']}'"
                )
                response_code = self.client.zpa_gateway.delete_gateway(gateway_id=gateway["id"])
                if response_code == 204:
                    logging.info(f"Successfully deleted zpa gateway with ID: {gateway['id']}, Name: {gateway['name']}")
                else:
                    logging.error(
                        f"Failed to delete zpa gateway with ID: {gateway['id']}, Name: {gateway['name']} - Status code: {response_code}"
                    )
        except Exception as e:
            logging.error(f"An error occurred while sweeping zpa gateways: {str(e)}")
            raise


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    # Ensure the environment variable is set
    if not os.getenv("ZIA_SDK_TEST_SWEEP"):
        os.environ["ZIA_SDK_TEST_SWEEP"] = "true"
        logging.info("Environment variable ZIA_SDK_TEST_SWEEP was not set. Setting it to true.")

    env_var = os.getenv("ZIA_SDK_TEST_SWEEP")
    flag_present = "--sweep" in sys.argv
    logging.info(f"Environment variable ZIA_SDK_TEST_SWEEP: {env_var}")
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
        logging.info("Sweep flag not set or environment variable ZIA_SDK_TEST_SWEEP is not set to true. Skipping sweep.")
