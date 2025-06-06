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
            self.sweep_rule_labels,
            self.sweep_bandwidth_rule,
            self.sweep_bandwidth_class,
            self.sweep_cloud_firewall_rule,
            self.sweep_cloud_firewall_ips_rule,
            self.sweep_cloud_firewall_dns_rule,
            self.sweep_file_type_control_rule,
            self.sweep_sandbox_rules,
            # self.sweep_cloud_firewall_ip_source_group,
            # self.sweep_cloud_firewall_ip_destination_group,
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
            # self.sweep_zpa_gateway,
            self.sweep_nss_servers,
            self.sweep_nat_control_policy,
        ]

        for func in sweep_functions:
            logging.info(f"Executing {func.__name__}")
            func()

    @suppress_warnings
    def sweep_rule_labels(self):
        logging.info("Starting to sweep rule labels")
        try:
            labels, _, error = self.client.zia.rule_labels.list_labels()
            if error:
                raise Exception(f"Error listing rule labels: {error}")

            test_labels = [lab for lab in labels if hasattr(lab, "name") and lab.name.startswith("tests-")]
            logging.info(f"Found {len(test_labels)} rule labels to delete.")

            for label in test_labels:
                logging.info(f"Deleting rule label ID={label.id}, Name={label.name}")
                _, _, error = self.client.zia.rule_labels.delete_label(label_id=label.id)
                if error:
                    logging.error(f"Failed to delete rule label ID={label.id} — {error}")
                else:
                    logging.info(f"Successfully deleted rule label ID={label.id}")

        except Exception as e:
            logging.error(f"An error occurred while sweeping rule labels: {str(e)}")
            raise

    @suppress_warnings
    def sweep_bandwidth_class(self):
        logging.info("Starting to sweep bandwidth class")
        try:
            classes, _, error = self.client.zia.bandwidth_classes.list_classes()
            if error:
                raise Exception(f"Error listing bandwidth classes: {error}")

            test_classes = [bw for bw in classes if hasattr(bw, "name") and bw.name.startswith("tests-")]
            logging.info(f"Found {len(test_classes)} bandwidth class to delete.")

            for bdw_class in test_classes:
                logging.info(
                    f"sweep_bandwidth_class: Attempting to delete bandwidth class: Name='{bdw_class.name}', ID='{bdw_class.id}'"
                )
                _, _, error = self.client.zia.bandwidth_classes.delete_class(class_id=bdw_class["id"])
                if error:
                    logging.error(f"Failed to delete bandwidth class ID={bdw_class['id']} — {error}")
                else:
                    logging.info(f"Successfully deleted bandwidth class ID={bdw_class['id']}")

        except Exception as e:
            logging.error(f"An error occurred while sweeping bandwidth classs: {str(e)}")
            raise

    @suppress_warnings
    def sweep_bandwidth_rule(self):
        logging.info("Starting to sweep bandwidth control rule")
        try:
            rules, _, error = self.client.zia.bandwidth_control_rules.list_rules()
            if error:
                raise Exception(f"Error listing bandwidth control rules: {error}")

            test_rules = [bw for bw in rules if hasattr(bw, "name") and bw.name.startswith("tests-")]
            logging.info(f"Found {len(test_rules)} bandwidth control rule to delete.")

            for rule in test_rules:
                logging.info(
                    f"sweep_cloud_firewall_rule: Attempting to delete bandwidth control rule: Name='{rule.name}', ID='{rule.id}'"
                )
                _, _, error = self.client.zia.bandwidth_control_rules.delete_rule(rule_id=rule["id"])
                if error:
                    logging.error(f"Failed to delete bandwidth control rule ID={rule['id']} — {error}")
                else:
                    logging.info(f"Successfully deleted bandwidth control rule ID={rule['id']}")

        except Exception as e:
            logging.error(f"An error occurred while sweeping bandwidth control rules: {str(e)}")
            raise

    @suppress_warnings
    def sweep_cloud_firewall_rule(self):
        logging.info("Starting to sweep cloud firewall rule")
        try:
            rules, _, error = self.client.zia.cloud_firewall_rules.list_rules()
            if error:
                raise Exception(f"Error listing cloud firewall rules: {error}")

            test_rules = [fw for fw in rules if hasattr(fw, "name") and fw.name.startswith("tests-")]
            logging.info(f"Found {len(test_rules)} cloud firewall rule to delete.")

            for rule in test_rules:
                logging.info(
                    f"sweep_cloud_firewall_rule: Attempting to delete cloud firewall rule: Name='{rule.name}', ID='{rule.id}'"
                )
                _, _, error = self.client.zia.cloud_firewall_rules.delete_rule(rule_id=rule["id"])
                if error:
                    logging.error(f"Failed to delete cloud firewall rule ID={rule['id']} — {error}")
                else:
                    logging.info(f"Successfully deleted cloud firewall rule ID={rule['id']}")

        except Exception as e:
            logging.error(f"An error occurred while sweeping cloud firewall rules: {str(e)}")
            raise

    @suppress_warnings
    def sweep_cloud_firewall_ips_rule(self):
        logging.info("Starting to sweep cloud firewall ips rule")
        try:
            rules, _, error = self.client.zia.cloud_firewall_ips.list_rules()
            if error:
                raise Exception(f"Error listing cloud firewall ips rules: {error}")

            test_rules = [fw for fw in rules if hasattr(fw, "name") and fw.name.startswith("tests-")]
            logging.info(f"Found {len(test_rules)} cloud firewall rule ips to delete.")

            for rule in test_rules:
                logging.info(
                    f"sweep_cloud_firewall_rule: Attempting to delete cloud firewall ips rule: Name='{rule.name}', ID='{rule.id}'"
                )
                _, _, error = self.client.zia.cloud_firewall_ips.delete_rule(rule_id=rule["id"])
                if error:
                    logging.error(f"Failed to delete cloud firewall ips rule ID={rule['id']} — {error}")
                else:
                    logging.info(f"Successfully deleted cloud firewall ips rule ID={rule['id']}")

        except Exception as e:
            logging.error(f"An error occurred while sweeping cloud firewall ips rules: {str(e)}")
            raise

    @suppress_warnings
    def sweep_cloud_firewall_dns_rule(self):
        logging.info("Starting to sweep cloud firewall dns rule")
        try:
            rules, _, error = self.client.zia.cloud_firewall_dns.list_rules()
            if error:
                raise Exception(f"Error listing cloud firewall dns rules: {error}")

            test_rules = [fw for fw in rules if hasattr(fw, "name") and fw.name.startswith("tests-")]
            logging.info(f"Found {len(test_rules)} cloud firewall dns rule to delete.")

            for rule in test_rules:
                logging.info(
                    f"sweep_cloud_firewall_rule: Attempting to delete cloud firewall dns rule: Name='{rule.name}', ID='{rule.id}'"
                )
                _, _, error = self.client.zia.cloud_firewall_dns.delete_rule(rule_id=rule["id"])
                if error:
                    logging.error(f"Failed to delete cloud firewall dns rule ID={rule['id']} — {error}")
                else:
                    logging.info(f"Successfully deleted cloud firewall dns rule ID={rule['id']}")

        except Exception as e:
            logging.error(f"An error occurred while sweeping cloud firewall dns rules: {str(e)}")
            raise

    @suppress_warnings
    def sweep_file_type_control_rule(self):
        logging.info("Starting to sweep file type control rule")
        try:
            rules, _, error = self.client.zia.file_type_control_rule.list_rules()
            if error:
                raise Exception(f"Error listing file type control rules: {error}")

            test_rules = [fw for fw in rules if hasattr(fw, "name") and fw.name.startswith("tests-")]
            logging.info(f"Found {len(test_rules)} file type control rule to delete.")

            for rule in test_rules:
                logging.info(
                    f"sweep_cloud_firewall_rule: Attempting to delete file type control rule: Name='{rule.name}', ID='{rule.id}'"
                )
                _, _, error = self.client.zia.file_type_control_rule.delete_rule(rule_id=rule["id"])
                if error:
                    logging.error(f"Failed to delete file type control rule ID={rule['id']} — {error}")
                else:
                    logging.info(f"Successfully deleted file type control rule ID={rule['id']}")

        except Exception as e:
            logging.error(f"An error occurred while sweeping file type control rules: {str(e)}")
            raise

    @suppress_warnings
    def sweep_sandbox_rules(self):
        logging.info("Starting to sweep sandbox rule")
        try:
            rules, _, error = self.client.zia.sandbox_rules.list_rules()
            if error:
                raise Exception(f"Error listing sandbox rules: {error}")

            test_rules = [fw for fw in rules if hasattr(fw, "name") and fw.name.startswith("tests-")]
            logging.info(f"Found {len(test_rules)} sandbox rule to delete.")

            for rule in test_rules:
                logging.info(
                    f"sweep_cloud_firewall_rule: Attempting to delete sandbox rule: Name='{rule.name}', ID='{rule.id}'"
                )
                _, _, error = self.client.zia.sandbox_rules.delete_rule(rule_id=rule["id"])
                if error:
                    logging.error(f"Failed to delete sandbox rule ID={rule['id']} — {error}")
                else:
                    logging.info(f"Successfully deleted sandbox rule ID={rule['id']}")

        except Exception as e:
            logging.error(f"An error occurred while sweeping sandbox rules: {str(e)}")
            raise

    @suppress_warnings
    def sweep_cloud_app_control_rule(self, rule_type: str):
        logging.info("Starting to sweep cloud app control rule")
        try:
            rules, _, error = self.client.zia.cloudappcontrol.list_rules(rule_type)
            if error:
                raise Exception(f"Error listing cloud app control rules: {error}")

            test_rules = [lab for lab in rules if hasattr(lab, "name") and lab.name.startswith("tests-")]
            logging.info(f"Found {len(test_rules)} cloud app control rules to delete.")

            for rule in test_rules:
                logging.info(
                    f"sweep_cloud_app_control_rule: Attempting to delete cloud app control rule: Name='{rule.name}', ID='{rule.id}'"
                )
                _, _, error = self.client.zia.cloudappcontrol.delete_rule(rule_type, rule["id"])
                if error:
                    logging.error(f"Failed to delete cloud app control rule ID={rule['id']} — {error}")
                else:
                    logging.info(f"Successfully deleted cloud app control rule ID={rule['id']}")

        except Exception as e:
            logging.error(f"An error occurred while sweeping cloud app control rules: {str(e)}")
            raise

    # @suppress_warnings
    # def sweep_cloud_firewall_ip_source_group(self):
    #     logging.info("Starting to sweep cloud firewall ip source group")
    #     try:
    #         groups, _, error = self.client.zia.cloud_firewall.list_ip_source_groups()
    #         if error:
    #             raise Exception(f"Error listing ip source groups: {error}")

    #         test_groups = [grp for grp in groups if hasattr(grp, "name") and grp.name.startswith("tests-")]
    #         logging.info(f"Found {len(test_groups)} cloud firewall ip source group to delete.")

    #         for group in test_groups:
    #             logging.info(
    #                 f"sweep_cloud_firewall_ip_source_group: Attempting to delete ip source group: Name='{group.name}', ID='{group.id}'"
    #             )
    #             _, _, error = self.client.zia.cloud_firewall.delete_ip_source_group(group_id=group.id)
    #             if error:
    #                 logging.error(f"Failed to delete ip source group ID={group.id} — {error}")
    #             else:
    #                 logging.info(f"Successfully deleted ip source group ID={group.id}")

    #     except Exception as e:
    #         logging.error(f"An error occurred while sweeping ip source groups: {str(e)}")
    #         raise

    # @suppress_warnings
    # def sweep_cloud_firewall_ip_destination_group(self):
    #     logging.info("Starting to sweep cloud firewall ip destination group")
    #     try:
    #         groups, _, error = self.client.zia.cloud_firewall.list_ip_destination_groups()
    #         if error:
    #             raise Exception(f"Error listing cloud firewall rules: {error}")

    #         test_groups = [grp for grp in groups if hasattr(grp, "name") and grp.name.startswith("tests-")]
    #         logging.info(f"Found {len(test_groups)} cloud firewall ip destination group to delete.")

    #         for group in test_groups:
    #             logging.info(
    #                 f"sweep_cloud_firewall_ip_destination_group: Attempting to delete ip destination group: Name='{group.name}', ID='{group.id}'"
    #             )
    #             _, _, error = self.client.zia.cloud_firewall.delete_ip_destination_group(group_id=group.id)
    #             if error:
    #                 logging.error(f"Failed to delete ip destination group ID={group.id} — {error}")
    #             else:
    #                 logging.info(f"Successfully deleted ip destination group ID={group.id}")

    #     except Exception as e:
    #         logging.error(f"An error occurred while sweeping ip destination groups: {str(e)}")
    #         raise

    @suppress_warnings
    def sweep_cloud_firewall_network_app_group(self):
        logging.info("Starting to sweep cloud firewall network app group")
        try:
            groups, _, error = self.client.zia.cloud_firewall.list_network_app_groups()
            if error:
                raise Exception(f"Error listing cloud firewall rules: {error}")

            test_groups = [grp for grp in groups if hasattr(grp, "name") and grp.name.startswith("tests-")]
            logging.info(f"Found {len(test_groups)} cloud firewall network app group to delete.")

            for group in test_groups:
                logging.info(
                    f"sweep_cloud_firewall_network_app_group: Attempting to delete cloud firewall network app group: Name='{group.name}', ID='{group.id}'"
                )
                _, _, error = self.client.zia.cloud_firewall.delete_network_app_group(group_id=group.id)
                if error:
                    logging.error(f"Failed to delete network app group ID={group.id} — {error}")
                else:
                    logging.info(f"Successfully deleted network app group ID={group.id}")

        except Exception as e:
            logging.error(f"An error occurred while sweeping ip source groups: {str(e)}")
            raise

    @suppress_warnings
    def sweep_cloud_firewall_network_service_group(self):
        logging.info("Starting to sweep cloud firewall network service group")
        try:
            groups, _, error = self.client.zia.cloud_firewall.list_network_svc_groups()
            if error:
                raise Exception(f"Error listing cloud firewall rules: {error}")

            test_groups = [grp for grp in groups if hasattr(grp, "name") and grp.name.startswith("tests-")]
            logging.info(f"Found {len(test_groups)} cloud firewall network service group to delete.")

            for group in test_groups:
                logging.info(
                    f"sweep_cloud_firewall_network_service_group: Attempting to delete cloud firewall network service group: Name='{group.name}', ID='{group.id}'"
                )
                _, _, error = self.client.zia.cloud_firewall.delete_network_svc_group(group_id=group.id)
                if error:
                    logging.error(f"Failed to delete network service group ID={group.id} — {error}")
                else:
                    logging.info(f"Successfully deleted network service group ID={group.id}")

        except Exception as e:
            logging.error(f"An error occurred while sweeping network service groups: {str(e)}")
            raise

    @suppress_warnings
    def sweep_cloud_firewall_network_service(self):
        logging.info("Starting to sweep cloud firewall network service")
        try:
            services, _, error = self.client.zia.cloud_firewall.list_network_services()
            if error:
                raise Exception(f"Error listing cloud firewall rules: {error}")

            test_services = [svc for svc in services if hasattr(svc, "name") and svc.name.startswith("tests-")]
            logging.info(f"Found {len(test_services)} cloud firewall network service to delete.")

            for service in test_services:
                logging.info(
                    f"sweep_cloud_firewall_network_service: Attempting to delete cloud firewall network service: Name='{service.name}', ID='{service.id}'"
                )
                _, _, error = self.client.zia.cloud_firewall.delete_network_service(service_id=service.id)
                if error:
                    logging.error(f"Failed to delete ip network service ID={service.id} — {error}")
                else:
                    logging.info(f"Successfully deleted ip network service ID={service.id}")

        except Exception as e:
            logging.error(f"An error occurred while sweeping ip network services: {str(e)}")
            raise

    @suppress_warnings
    def sweep_dlp_web_rule(self):
        logging.info("Starting to sweep dlp web rule")
        try:
            rules, _, error = self.client.zia.dlp_web_rules.list_rules()
            if error:
                raise Exception(f"Error listing dlp web rules: {error}")

            test_rules = [fw for fw in rules if hasattr(fw, "name") and fw.name.startswith("tests-")]
            logging.info(f"Found {len(test_rules)} dlp web rule to delete.")

            for rule in test_rules:
                logging.info(f"sweep_dlp_web_rule: Attempting to delete dlp web rule: Name='{rule.id}', ID='{rule.id}'")
                _, _, error = self.client.zia.dlp_web_rules.delete_rule(rule_id=rule.id)
                if error:
                    logging.error(f"Failed to delete dlp web rule ID={rule.id} — {error}")
                else:
                    logging.info(f"Successfully deleted dlp web rule ID={rule.id}")

        except Exception as e:
            logging.error(f"An error occurred while sweeping dlp web rules: {str(e)}")
            raise

    @suppress_warnings
    def sweep_forwarding_control_rule(self):
        logging.info("Starting to sweep forwarding control rule")
        try:
            rules, _, error = self.client.zia.forwarding_control.list_rules()
            if error:
                raise Exception(f"Error listing cloud firewall rules: {error}")

            test_rules = [fw for fw in rules if hasattr(fw, "name") and fw.name.startswith("tests-")]
            logging.info(f"Found {len(test_rules)} forwarding control rule to delete.")

            for rule in test_rules:
                logging.info(
                    f"sweep_forwarding_control_rule: Attempting to delete forwarding control rule: Name='{rule.id}', ID='{rule.id}'"
                )
                _, _, error = self.client.zia.forwarding_control.delete_rule(rule_id=rule.id)
                if error:
                    logging.error(f"Failed to delete rule label ID={rule.id} — {error}")
                else:
                    logging.info(f"Successfully deleted rule label ID={rule.id}")

        except Exception as e:
            logging.error(f"An error occurred while sweeping rule labels: {str(e)}")
            raise

    @suppress_warnings
    def sweep_url_filtering_rule(self):
        logging.info("Starting to sweep url filtering rule")
        try:
            rules, _, error = self.client.zia.url_filtering.list_rules()
            if error:
                raise Exception(f"Error listing url filtering rules: {error}")

            test_rules = [fw for fw in rules if hasattr(fw, "name") and fw.name.startswith("tests-")]
            logging.info(f"Found {len(test_rules)} url filtering rule to delete.")

            for rule in test_rules:
                logging.info(
                    f"sweep_url_filtering_rule: Attempting to delete url filtering rule: Name='{rule.id}', ID='{rule.id}'"
                )
                _, _, error = self.client.zia.url_filtering.delete_rule(rule_id=rule.id)
                if error:
                    logging.error(f"Failed to delete rule label ID={rule.id} — {error}")
                else:
                    logging.info(f"Successfully deleted rule label ID={rule.id}")

        except Exception as e:
            logging.error(f"An error occurred while sweeping rule labels: {str(e)}")
            raise

    @suppress_warnings
    def sweep_location_management(self):
        logging.info("Starting to sweep location management")
        try:
            locations, _, error = self.client.zia.locations.list_locations()
            if error:
                raise Exception(f"Error listing locations: {error}")

            test_locations = [loc for loc in locations if hasattr(loc, "name") and loc.name.startswith("tests-")]
            location_ids = [loc["id"] for loc in test_locations]
            logging.info(f"Found {len(test_locations)} location management to delete.")

            if location_ids:
                logging.info(f"sweep_location_management: Attempting to bulk delete location management: IDs={location_ids}")
                _, _, error = self.client.zia.locations.bulk_delete_locations(location_ids=location_ids)
                if error:
                    logging.error(f"Failed to delete locations ID={location_ids['id']} — {error}")
                else:
                    logging.info(f"Successfully deleted locations ID={location_ids['id']}")

        except Exception as e:
            logging.error(f"An error occurred while sweeping locationss: {str(e)}")
            raise

    @suppress_warnings
    def sweep_vpn_credentials(self):
        logging.info("Starting to sweep VPN credentials")
        try:
            credentials, _, error = self.client.zia.traffic_vpn_credentials.list_vpn_credentials(
                query_params={"type": "UFQDN"}
            )
            if error:
                raise Exception(f"Error listing vpn credentials: {error}")

            # Model-aware check
            test_creds = [
                vpn
                for vpn in credentials
                if getattr(vpn, "type", None) == "UFQDN" and hasattr(vpn, "fqdn") and vpn.fqdn.startswith("tests-")
            ]
            credential_ids = [vpn.id for vpn in test_creds]
            logging.info(f"Found {len(test_creds)} VPN credentials to delete.")

            if credential_ids:
                logging.info(f"sweep_vpn_credentials: Attempting to bulk delete VPN credentials: IDs={credential_ids}")
                _, _, error = self.client.zia.traffic_vpn_credentials.bulk_delete_vpn_credentials(
                    credential_ids=credential_ids
                )
                if error:
                    logging.error(f"Failed to bulk delete vpn credentials — {error}")
                else:
                    logging.info(f"Successfully bulk deleted VPN credentials: IDs={credential_ids}")

        except Exception as e:
            logging.error(f"An error occurred while sweeping vpn credentials: {str(e)}")
            raise

    @suppress_warnings
    def sweep_gre_tunnels(self):
        logging.info("Starting to sweep GRE tunnels")
        try:
            gre_tunnels, _, error = self.client.zia.gre_tunnel.list_gre_tunnels()
            if error:
                raise Exception(f"Error listing GRE tunnels: {error}")

            test_gre_tunnels = [
                gre
                for gre in gre_tunnels
                if hasattr(gre, "comment") and isinstance(gre.comment, str) and gre.comment.startswith("tests-")
            ]
            logging.info(f"Found {len(test_gre_tunnels)} GRE tunnels to delete.")

            for gre_tunnel in test_gre_tunnels:
                logging.info(
                    f"sweep_gre_tunnels: Attempting to delete GRE tunnel: Comment='{gre_tunnel.comment}', ID='{gre_tunnel.id}'"
                )
                _, _, error = self.client.zia.gre_tunnel.delete_gre_tunnel(tunnel_id=gre_tunnel.id)
                if error:
                    logging.error(f"Failed to delete GRE tunnel ID={gre_tunnel.id} — {error}")
                else:
                    logging.info(f"Successfully deleted GRE tunnel ID={gre_tunnel.id}")

        except Exception as e:
            logging.error(f"An error occurred while sweeping GRE tunnels: {str(e)}")
            raise

    @suppress_warnings
    def sweep_static_ip(self):
        logging.info("Starting to sweep static IPs")
        try:
            static_ips, _, error = self.client.zia.traffic_static_ip.list_static_ips()
            if error:
                raise Exception(f"Error listing static IPs: {error}")

            test_static_ips = [
                ip
                for ip in static_ips
                if hasattr(ip, "comment") and isinstance(ip.comment, str) and ip.comment.startswith("tests-")
            ]
            logging.info(f"Found {len(test_static_ips)} static IPs to delete.")

            for static_ip in test_static_ips:
                logging.info(
                    f"sweep_static_ip: Attempting to delete static IP: Comment='{static_ip.comment}', ID='{static_ip.id}'"
                )
                _, _, error = self.client.zia.traffic_static_ip.delete_static_ip(static_ip_id=static_ip.id)
                if error:
                    logging.error(f"Failed to delete static IP ID={static_ip.id} — {error}")
                else:
                    logging.info(f"Successfully deleted static IP ID={static_ip.id}")

        except Exception as e:
            logging.error(f"An error occurred while sweeping static IPs: {str(e)}")
            raise

    @suppress_warnings
    def sweep_dlp_engine(self):
        logging.info("Starting to sweep dlp engine")
        try:
            engines, _, error = self.client.zia.dlp_engine.list_dlp_engines()
            if error:
                raise Exception(f"Error listing dlp engines: {error}")

            test_engines = [
                ip for ip in engines if hasattr(ip, "comment") and isinstance(ip.name, str) and ip.name.startswith("tests-")
            ]
            logging.info(f"Found {len(test_engines)} static IPs to delete.")

            for engine in test_engines:
                logging.info(f"sweep_dlp_engine: Attempting to delete dlp engine: Name='{engine.id}', ID='{engine.id}'")
                _, _, error = self.client.zia.dlp_engine.delete_dlp_engine(engine_id=engine.id)
                if error:
                    logging.error(f"Failed to delete dlp engine ID={engine.id} — {error}")
                else:
                    logging.info(f"Successfully deleted dlp engineID={engine.id}")

        except Exception as e:
            logging.error(f"An error occurred while sweeping dlp engines: {str(e)}")
            raise

    @suppress_warnings
    def sweep_dlp_dictionary(self):
        logging.info("Starting to sweep dlp dictionary")
        try:
            dictionaries, _, error = self.client.zia.dlp_dictionary.list_dicts()
            if error:
                raise Exception(f"Error listing dlp dictionaries: {error}")

            test_dictionaries = [dlp for dlp in dictionaries if hasattr(dlp, "name") and dlp.name.startswith("tests-")]
            logging.info(f"Found {len(test_dictionaries)} dlp dictionary to delete.")

            for dictionary in test_dictionaries:
                logging.info(
                    f"sweep_dlp_dictionary: Attempting to delete dlp dictionary: Name='{dictionary.name}', ID='{dictionary.id}'"
                )
                _, _, error = self.client.zia.dlp_dictionary.delete_dict(dict_id=dictionary.id)
                if error:
                    logging.error(f"Failed to delete dlp dictionary ID={dictionary.id} — {error}")
                else:
                    logging.info(f"Successfully deleted dlp dictionary ID={dictionary.id}")

        except Exception as e:
            logging.error(f"An error occurred while sweeping dlp dictionaries: {str(e)}")
            raise

    @suppress_warnings
    def sweep_dlp_template(self):
        logging.info("Starting to sweep dlp notification template")
        try:
            templates, _, error = self.client.zia.dlp_templates.list_dlp_templates()
            if error:
                raise Exception(f"Error listing dlp notification templates: {error}")

            test_templates = [dlp for dlp in templates if hasattr(dlp, "name") and dlp.name.startswith("tests-")]
            logging.info(f"Found {len(test_templates)} dlp notification template to delete.")

            for template in test_templates:
                logging.info(
                    f"sweep_dlp_template: Attempting to delete dlp notification template: Name='{template.name}', ID='{template.id}'"
                )
                _, _, error = self.client.zia.dlp_templates.delete_dlp_template(template_id=template.id)
                if error:
                    logging.error(f"Failed to delete dlp notification template ID={template.id} — {error}")
                else:
                    logging.info(f"Successfully deleted dlp notification template ID={template.id}")

        except Exception as e:
            logging.error(f"An error occurred while sweeping dlp notification templates: {str(e)}")
            raise

    # @suppress_warnings
    # def sweep_zpa_gateway(self):
    #     logging.info("Starting to sweep zpa gateway")
    #     try:
    #         gateways, _, error = self.client.zia.zpa_gateway.list_gateways()
    #         if error:
    #             raise Exception(f"Error listing zpa gateways: {error}")

    #         test_gateways = [gw for gw in gateways if hasattr(gw, "name") and gw.name.startswith("tests-")]
    #         logging.info(f"Found {len(test_gateways)} zpa gateway to delete.")

    #         for gateway in test_gateways:
    #             logging.info(f"sweep_zpa_gateway: Attempting to delete zpa gateway: Name='{gateway.name}', ID='{gateway.id}'")
    #             _, _, error = self.client.zia.zpa_gateway.delete_gateway(gateway_id=gateway.id)
    #             if error:
    #                 logging.error(f"Failed to delete zpa gateway ID={gateway.id} — {error}")
    #             else:
    #                 logging.info(f"Successfully deleted zpa gateway ID={gateway.id}")

    #     except Exception as e:
    #         logging.error(f"An error occurred while sweeping zpa gateways: {str(e)}")
    #         raise

    @suppress_warnings
    def sweep_nss_servers(self):
        logging.info("Starting to sweep nss servers")
        try:
            nss_servers, _, error = self.client.zia.nss_servers.list_nss_servers()
            if error:
                raise Exception(f"Error listing nss servers: {error}")

            test_nss = [gw for gw in nss_servers if hasattr(gw, "name") and gw.name.startswith("tests-")]
            logging.info(f"Found {len(test_nss)} nss server to delete.")

            for nss in test_nss:
                logging.info(f"sweep_nss_servers: Attempting to delete nss server: Name='{nss.name}', ID='{nss.id}'")
                _, _, error = self.client.zia.nss_servers.delete_nss_server(nss_id=nss.id)
                if error:
                    logging.error(f"Failed to delete nss server ID={nss.id} — {error}")
                else:
                    logging.info(f"Successfully deleted nss server ID={nss.id}")

        except Exception as e:
            logging.error(f"An error occurred while sweeping nss servers: {str(e)}")
            raise

    @suppress_warnings
    def sweep_nat_control_policy(self):
        logging.info("Starting to sweep nat control rule")
        try:
            rules, _, error = self.client.zia.nat_control_policy.list_rules()
            if error:
                raise Exception(f"Error listing nat control rules: {error}")

            test_rules = [nat for nat in rules if hasattr(nat, "name") and nat.name.startswith("tests-")]
            logging.info(f"Found {len(test_rules)} nat control  rule to delete.")

            for rule in test_rules:
                logging.info(
                    f"sweep_nat_control_policy: Attempting to delete nat control  rule: Name='{rule.name}', ID='{rule.id}'"
                )
                _, _, error = self.client.zia.nat_control_policy.delete_rule(rule_id=rule["id"])
                if error:
                    logging.error(f"Failed to delete nat control rule ID={rule['id']} — {error}")
                else:
                    logging.info(f"Successfully deleted nat control rule ID={rule['id']}")

        except Exception as e:
            logging.error(f"An error occurred while sweeping nat control rules: {str(e)}")
            raise

    @suppress_warnings
    def sweep_vzen_clusters(self):
        logging.info("Starting to sweep vzen clusters")
        try:
            vzen_clusters, _, error = self.client.zia.vzen_clusters.list_vzen_clusters()
            if error:
                raise Exception(f"Error listing vzen clusters: {error}")

            test_vzen = [vzen for vzen in vzen_clusters if hasattr(vzen, "name") and vzen.name.startswith("tests")]
            logging.info(f"Found {len(test_vzen)} vzen cluster to delete.")

            for vzen in test_vzen:
                logging.info(f"sweep_nss_servers: Attempting to delete vzen cluster: Name='{vzen.name}', ID='{vzen.id}'")
                _, _, error = self.client.zia.vzen_clusters.delete_vzen_cluster(nss_id=vzen.id)
                if error:
                    logging.error(f"Failed to delete vzen cluster ID={vzen.id} — {error}")
                else:
                    logging.info(f"Successfully deleted vzen cluster ID={vzen.id}")

        except Exception as e:
            logging.error(f"An error occurred while sweeping vzen clusters: {str(e)}")
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
