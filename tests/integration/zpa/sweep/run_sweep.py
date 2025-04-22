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
        customer_id = config.get("customerId", os.getenv("ZPA_CUSTOMER_ID"))
        vanity_domain = config.get("vanityDomain", os.getenv("ZSCALER_VANITY_DOMAIN"))
        cloud = config.get("cloud", os.getenv("ZSCALER_CLOUD", "PRODUCTION"))

        logging_config = config.get("logging", {"enabled": False, "verbose": False})

        client_config = {
            "clientId": client_id,
            "clientSecret": client_secret,
            "customerId": customer_id,
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
                policies, _, error = self.client.zpa.policies.list_rules(policy_type=policy_type)
                if error:
                    raise Exception(f"Error listing rule: {error}")

                test_policies = [pol for pol in policies if hasattr(pol, "name") and pol.name.startswith("tests-")]
                logging.info(f"Found {len(test_policies)} '{policy_type}' policies named starting with 'tests-' to delete.")

                for policy in test_policies:
                    logging.info(
                        f"sweep_all_access_policies: Attempting to delete '{policy_type}' policy: Name='{policy.name}', ID='{policy.id}'"
                    )
                    _, _, error = self.client.zpa.policies.delete_rule(policy_type=policy_type, rule_id=policy.id)
                    if error:
                        logging.error(f"Failed to delete rule ID={policy.id} — {error}")
                    else:
                        logging.info(f"Successfully deleted rule ID={policy.id}")

        except Exception as e:
            logging.error(f"An error occurred while sweeping rule: {str(e)}")
            raise

    @suppress_warnings
    def sweep_pra_portal(self):
        logging.info("Starting to sweep pra portal")
        try:
            portals, _, error = self.client.zpa.pra_portal.list_portals()
            if error:
                raise Exception(f"Error listing rule labels: {error}")

            test_portals = [pra for pra in portals if hasattr(pra, "name") and pra.name.startswith("tests-")]
            logging.info(f"Found {len(test_portals)} pra portal named starting with 'tests-' to delete.")

            for portal in test_portals:
                logging.info(f"sweep_pra_portal: Attempting to delete pra portal : Name='{portal.name}', ID='{portal.id}'")
                _, _, error = self.client.zpa.pra_portal.delete_portal(portal_id=portal.id)
                if error:
                    logging.error(f"Failed to delete rule label ID={portal.id} — {error}")
                else:
                    logging.info(f"Successfully deleted rule label ID={portal.id}")

        except Exception as e:
            logging.error(f"An error occurred while sweeping rule labels: {str(e)}")
            raise

    @suppress_warnings
    def sweep_pra_credential(self):
        logging.info("Starting to sweep pra credential")
        try:
            portals, _, error = self.client.zpa.pra_credential.list_credentials()
            if error:
                raise Exception(f"Error listing credentials: {error}")

            test_portals = [pra for pra in portals if hasattr(pra, "name") and pra.name.startswith("tests-")]
            logging.info(f"Found {len(test_portals)} pra credential named starting with 'tests-' to delete.")

            for credential in test_portals:
                logging.info(
                    f"sweep_pra_credential: Attempting to delete pra credential : Name='{credential.name}', ID='{credential.id}'"
                )
                _, _, error = self.client.zpa.pra_credential.delete_credential(credential_id=credential.id)
                if error:
                    logging.error(f"Failed to delete credential ID={credential.id} — {error}")
                else:
                    logging.info(f"Successfully deleted credential ID={credential.id}")

        except Exception as e:
            logging.error(f"An error occurred while sweeping credentials: {str(e)}")
            raise

    @suppress_warnings
    def sweep_pra_approval(self):
        logging.info("Starting to sweep pra approval")
        try:
            portals, _, error = self.client.zpa.pra_approval.list_approval()
            if error:
                raise Exception(f"Error listing pra approvals: {error}")

            test_approvals = [
                pra for pra in portals if "email_ids" in pra and any("tests-" in email for email in pra.email_ids)
            ]
            logging.info(f"Found {len(test_approvals)} pra approvals with email IDs containing 'tests-' to delete.")

            for approval in test_approvals:
                logging.info(
                    f"sweep_pra_approval: Attempting to delete pra approval: Name='{approval.name}', ID='{approval.id}'"
                )
                _, _, error = self.client.zpa.pra_approval.delete_approval(approval_id=approval.id)
                if error:
                    logging.error(f"Failed to delete pra approval ID={approval.id} — {error}")
                else:
                    logging.info(f"Successfully deleted pra approval ID={approval.id}")

        except Exception as e:
            logging.error(f"An error occurred while sweeping pra approvals: {str(e)}")
            raise

    @suppress_warnings
    def sweep_pra_console(self):
        logging.info("Starting to sweep pra console")
        try:
            portals, _, error = self.client.zpa.pra_console.list_consoles()
            if error:
                raise Exception(f"Error listing pra consoles: {error}")

            test_portals = [pra for pra in portals if hasattr(pra, "name") and pra.name.startswith("tests-")]
            logging.info(f"Found {len(test_portals)} pra console named starting with 'tests-' to delete.")

            for console in test_portals:
                logging.info(f"sweep_pra_consoles: Attempting to delete pra console : Name='{console.id}', ID='{console.id}'")
                _, _, error = self.client.zpa.pra_console.delete_console(console_id=console.id)
                if error:
                    logging.error(f"Failed to delete pra console ID={console.id} — {error}")
                else:
                    logging.info(f"Successfully deleted pra console ID={console.id}")

        except Exception as e:
            logging.error(f"An error occurred while sweeping pra consoles: {str(e)}")
            raise

    @suppress_warnings
    def sweep_microtenant(self):
        logging.info("Starting to sweep microtenant")
        try:
            microtenants, _, error = self.client.zpa.microtenants.list_microtenants()
            if error:
                raise Exception(f"Error listing microtenants: {error}")

            test_microtenants = [mic for mic in microtenants if hasattr(mic, "name") and mic.name.startswith("tests-")]
            logging.info(f"Found {len(test_microtenants)} microtenant named starting with 'tests-' to delete.")

            for microtenant in test_microtenants:
                logging.info(
                    f"sweep_microtenant: Attempting to delete microtenant : Name='{microtenant.name}', ID='{microtenant.id}'"
                )
                _, _, error = self.client.zpa.microtenants.delete_microtenant(console_id=microtenant.id)
                if error:
                    logging.error(f"Failed to delete microtenant ID={microtenant.id} — {error}")
                else:
                    logging.info(f"Successfully deleted microtenant ID={microtenant.id}")

        except Exception as e:
            logging.error(f"An error occurred while sweeping rule labels: {str(e)}")
            raise

    @suppress_warnings
    def sweep_app_segments(self):
        logging.info("Starting to sweep app segments")
        try:
            app_segments, _, error = self.client.zpa.application_segment.list_segments()
            if error:
                raise Exception(f"Error listing application segments: {error}")

            test_segments = [seg for seg in app_segments if hasattr(seg, "name") and seg.name.startswith("tests-")]
            logging.info(f"Found {len(test_segments)} app segments named starting with 'tests-' to delete.")

            for segment in test_segments:
                logging.info(f"sweep_app_segments: Attempting to delete app segment: Name='{segment.name}', ID='{segment.id}'")
                _, _, error = self.client.zpa.application_segment.delete_segment(segment_id=segment.id)
                if error:
                    logging.error(f"Failed to delete application segment ID={segment.id} — {error}")
                else:
                    logging.info(f"Successfully deleted application segment ID={segment.id}")

        except Exception as e:
            logging.error(f"An error occurred while sweeping application segments: {str(e)}")
            raise

    @suppress_warnings
    def sweep_segment_group(self):
        logging.info("Starting to sweep segment group")
        try:
            segment_groups, _, error = self.client.zpa.segment_groups.list_groups()
            if error:
                raise Exception(f"Error listing segment groups: {error}")

            test_groups = [grp for grp in segment_groups if hasattr(grp, "name") and grp.name.startswith("tests-")]
            logging.info(f"Found {len(test_groups)} segment group to delete.")

            for group in test_groups:
                logging.info(f"sweep_segment_group: Attempting to delete segment group: Name='{group.name}', ID='{group.id}'")
                _, _, error = self.client.zpa.segment_groups.delete_group(group_id=group.id)
                if error:
                    logging.error(f"Failed to delete segment group ID={group.id} — {error}")
                else:
                    logging.info(f"Successfully deleted segment group ID={group.id}")

        except Exception as e:
            logging.error(f"An error occurred while sweeping segment groups: {str(e)}")
            raise

    @suppress_warnings
    def sweep_server_group(self):
        logging.info("Starting to sweep server group")
        try:
            server_groups, _, error = self.client.zpa.server_groups.list_groups()
            if error:
                raise Exception(f"Error listing rule labels: {error}")

            test_groups = [grp for grp in server_groups if hasattr(grp, "name") and grp.name.startswith("tests-")]
            logging.info(f"Found {len(test_groups)} server groups to delete.")

            for group in test_groups:
                logging.info(f"sweep_server_group: Attempting to delete server group: Name='{group.name}', ID='{group.id}'")
                _, _, error = self.client.zpa.server_groups.delete_group(group_id=group.id)
                if error:
                    logging.error(f"Failed to delete rule label ID={group.id} — {error}")
                else:
                    logging.info(f"Successfully deleted rule label ID={group.id}")

        except Exception as e:
            logging.error(f"An error occurred while sweeping rule labels: {str(e)}")
            raise

    @suppress_warnings
    def sweep_provisioning_key(self):
        logging.info("Starting to sweep provisioning keys")
        key_types = ["connector", "service_edge"]

        try:
            for key_type in key_types:
                logging.info(f"Checking for provisioning keys of type '{key_type}'")
                provisioning_keys, _, error = self.client.zpa.provisioning.list_provisioning_keys(key_type=key_type)
                if error:
                    raise Exception(f"Error listing provisioning keys: {error}")

                test_provisioning_keys = [
                    key for key in provisioning_keys if hasattr(key, "name") and key.name.startswith("tests-")
                ]
                logging.info(f"Found {len(test_provisioning_keys)} '{key_type}' provisioning keys to delete.")

                for provisioning_key in test_provisioning_keys:
                    logging.info(
                        f"sweep_provisioning_key: Attempting to delete '{key_type}' provisioning key: Name='{provisioning_key.name}', ID='{provisioning_key.id}'"
                    )
                    _, _, error = self.client.zpa.provisioning.delete_provisioning_key(
                        key_id=provisioning_key.id, key_type=key_type
                    )
                    if error:
                        logging.error(f"Failed to delete provisioning key ID={provisioning_key.id} — {error}")
                    else:
                        logging.info(f"Successfully deleted provisioning key ID={provisioning_key.id}")

        except Exception as e:
            logging.error(f"An error occurred while sweeping provisioning keys: {str(e)}")
            raise

    @suppress_warnings
    def sweep_lss_controller(self):
        logging.info("Starting to sweep LSS controllers")
        try:
            list_controllers, _, error = self.client.zpa.lss.list_configs()
            if error:
                raise Exception(f"Error listing LSS controllers: {error}")

            test_controllers = [lss for lss in list_controllers if hasattr(lss, "name") and lss.name.startswith("tests-")]
            logging.info(f"Found {len(test_controllers)} LSS controllers to delete.")

            for controller in test_controllers:
                logging.info(
                    f"sweep_lss_controller: Attempting to delete LSS controller: Name='{controller['config'].name}', ID='{controller.id}'"
                )
                _, _, error = self.client.zpa.lss.delete_lss_config(lss_config_id=controller.id)
                if error:
                    logging.error(f"Failed to delete LSS controller ID={controller.id} — {error}")
                else:
                    logging.info(f"Successfully deleted LSS controller ID={controller.id}")

        except Exception as e:
            logging.error(f"An error occurred while sweeping LSS controllers: {str(e)}")
            raise

    @suppress_warnings
    def sweep_app_connector_group(self):
        logging.info("Starting to sweep app connector group")
        try:
            app_connectors, _, error = self.client.zpa.app_connector_groups.list_connector_groups()
            if error:
                raise Exception(f"Error listing app connector groups: {error}")

            test_groups = [grp for grp in app_connectors if hasattr(grp, "name") and grp.name.startswith("tests-")]
            logging.info(f"Found {len(test_groups)} app connector groups to delete.")

            for group in test_groups:
                logging.info(
                    f"sweep_app_connector_group: Attempting to delete app connector group: Name='{group.name}', ID='{group.id}'"
                )
                _, _, error = self.client.zpa.app_connector_groups.delete_connector_group(group_id=group.id)
                if error:
                    logging.error(f"Failed to delete app connector group ID={group.id} — {error}")
                else:
                    logging.info(f"Successfully deleted app connector group ID={group.id}")

        except Exception as e:
            logging.error(f"An error occurred while sweeping app connector groups: {str(e)}")
            raise

    @suppress_warnings
    def sweep_application_server(self):
        logging.info("Starting to sweep app servers")
        try:
            app_servers, _, error = self.client.zpa.servers.list_servers()
            if error:
                raise Exception(f"Error listing app serverss: {error}")

            test_servers = [srv for srv in app_servers if hasattr(srv, "name") and srv.name.startswith("tests-")]
            logging.info(f"Found {len(test_servers)} app servers to delete.")

            for server in test_servers:
                logging.info(
                    f"sweep_application_server: Attempting to delete app servers: Name='{server.id}', ID='{server.id}'"
                )
                _, _, error = self.client.zpa.servers.delete_server(server_id=server.id)
                if error:
                    logging.error(f"Failed to delete app servers ID={server.id} — {error}")
                else:
                    logging.info(f"Successfully deleted app servers ID={server.id}")

        except Exception as e:
            logging.error(f"An error occurred while sweeping app serverss: {str(e)}")
            raise

    @suppress_warnings
    def sweep_isolation_banner(self):
        logging.info("Starting to sweep isolation banner")
        try:
            banners, _, error = self.client.zpa.cbi_banner.list_cbi_banners()
            if error:
                raise Exception(f"Error listing isolation banners: {error}")

            test_banners = [cbi for cbi in banners if hasattr(cbi, "name") and cbi.name.startswith("tests-")]
            logging.info(f"Found {len(test_banners)} isolation banners to delete.")

            for banner in test_banners:
                logging.info(
                    f"sweep_isolation_banner: Attempting to delete isolation banner: Name='{banner.name}', ID='{banner.id}'"
                )
                _, _, error = self.client.zpa.cbi_banner.delete_cbi_banner(banner_id=banner.id)
                if error:
                    logging.error(f"Failed to delete isolation banner ID={banner.id} — {error}")
                else:
                    logging.info(f"Successfully deleted isolation banner ID={banner.id}")

        except Exception as e:
            logging.error(f"An error occurred while sweeping isolation banners: {str(e)}")
            raise

    @suppress_warnings
    def sweep_isolation_profile(self):
        logging.info("Starting to sweep isolation profile")
        try:
            profiles, _, error = self.client.zpa.cbi_profile.list_cbi_profiles()
            if error:
                raise Exception(f"Error listing isolation profiles: {error}")

            test_profiles = [cbi for cbi in profiles if hasattr(cbi, "name") and cbi.name.startswith("tests-")]
            logging.info(f"Found {len(test_profiles)} isolation profiles to delete.")

            for profile in test_profiles:
                logging.info(
                    f"sweep_isolation_profile: Attempting to delete isolation profile: Name='{profile.name}', ID='{profile.id}'"
                )
                _, _, error = self.client.zpa.cbi_profile.delete_cbi_profile(profile_id=profile.id)
                if error:
                    logging.error(f"Failed to delete isolation profile ID={profile.id} — {error}")
                else:
                    logging.info(f"Successfully deleted isolation profile ID={profile.id}")

        except Exception as e:
            logging.error(f"An error occurred while sweeping isolation profiles: {str(e)}")
            raise

    @suppress_warnings
    def sweep_isolation_certificate(self):
        logging.info("Starting to sweep isolation certificate")
        try:
            certificates, _, error = self.client.zpa.cbi_certificate.list_cbi_certificates()
            if error:
                raise Exception(f"Error listing isolation certificates: {error}")

            test_certificates = [cbi for cbi in certificates if hasattr(cbi, "name") and cbi.name.startswith("tests-")]
            logging.info(f"Found {len(test_certificates)} isolation certificates to delete.")

            for certificate in test_certificates:
                logging.info(
                    f"sweep_isolation_certificate: Attempting to delete isolation certificate: Name='{certificate.name}', ID='{certificate.id}'"
                )
                _, _, error = self.client.zpa.cbi_certificate.delete_cbi_certificate(certificate_id=certificate.id)
                if error:
                    logging.error(f"Failed to delete isolation certificate ID={certificate.id} — {error}")
                else:
                    logging.info(f"Successfully deleted isolation certificate ID={certificate.id}")

        except Exception as e:
            logging.error(f"An error occurred while sweeping isolation certificates: {str(e)}")
            raise

    @suppress_warnings
    def sweep_service_edge_group(self):
        logging.info("Starting to sweep service edge group")
        try:
            service_edge_grps, _, error = self.client.zpa.service_edge_group.list_service_edge_groups()
            if error:
                raise Exception(f"Error listing service edge groups: {error}")

            test_groups = [grp for grp in service_edge_grps if hasattr(grp, "name") and grp.name.startswith("tests-")]
            logging.info(f"Found {len(test_groups)} service edge groups to delete.")

            for group in test_groups:
                logging.info(
                    f"sweep_service_edge_group: Attempting to delete service edge group: Name='{group.name}', ID='{group.id}'"
                )
                _, _, error = self.client.zpa.service_edge_group.delete_service_edge_group(group_id=group.id)
                if error:
                    logging.error(f"Failed to delete service edge group ID={group.id} — {error}")
                else:
                    logging.info(f"Successfully deleted service edge group ID={group.id}")

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
