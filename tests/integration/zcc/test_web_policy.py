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
from tests.integration.zcc.conftest import MockZCCClient
from tests.test_utils import generate_random_string

@pytest.fixture
def fs():
    yield


class TestWebPolicy:
    """
    Integration Tests for the ZCC Web Policy API.

    The lifecycle exercises ``web_policy_edit`` (create), the two list
    paths (``device_type`` server-side filter and JMESPath client-side
    filter on the same response), and ``delete_web_policy`` for cleanup.
    The ``activate_web_policy`` endpoint is intentionally skipped because
    it is currently unstable in the ZCC API.
    """

    @pytest.mark.vcr()
    def test_web_policy_lifecycle(self, fs):
        client = MockZCCClient(fs)
        errors = []

        policy_name = "tests-web-policy-" + generate_random_string()
        policy_id = None

        try:
            _, response, err = client.zcc.web_policy.web_policy_edit(
                rule_order=1,
                name=policy_name,
                group_ids=[62718389, 62718428, 62718420],
                user_ids=["5807211"],
                app_service_ids=[],
                group_all=0,
                description="",
                pac_url="",
                registry_path="",
                log_mode=-1,
                log_level=0,
                log_file_size=100,
                reactivate_web_security_minutes=0,
                tunnel_zapp_traffic=0,
                active="1",
                mdm=0,
                passcode="",
                exit_password="",
                send_disable_service_reason=0,
                highlight_active_control=0,
                pac_type=1,
                pac_data_path="",
                install_ssl_certs=1,
                reauth_period=8,
                disable_loop_back_restriction=0,
                remove_exempted_containers=1,
                override_wpad=0,
                restart_win_http_svc=0,
                flow_logger_config=None,
                domain_profile_detection_config=None,
                all_inbound_traffic_config=None,
                disable_parallel_ipv4_and_ipv6=-1,
                enforced=0,
                bypass_mms_apps=0,
                quota_in_roaming=0,
                wifi_ssid="",
                limit="1",
                billing_day="1",
                allowed_apps="",
                custom_text="",
                bypass_android_apps=[],
                clear_arp_cache=0,
                enable_zscaler_firewall=0,
                persistent_zscaler_firewall=0,
                dns_priority_ordering=[
                    "State:/Network/Service/com.cisco.anyconnect/DNS",
                ],
                install_windows_firewall_inbound_rule="1",
                force_location_refresh_sccm=0,
                wfp_mtr=0,
                enable_local_packet_capture_tab_value=0,
                captive_portal_url_id=[
                    {"label": "Zscaler", "value": 1},
                ],
                client_connector_ui_language_selected=[
                    {"label": "Use System Language", "value": 0},
                ],
                policy_extension={
                    "vpn_gateways": "",
                    "partner_domains": "",
                    "zcc_fail_close_settings_ip_bypasses": "",
                    "zcc_fail_close_settings_lockdown_on_tunnel_process_exit": "1",
                    "zcc_fail_close_settings_exit_uninstall_password": "",
                    "zcc_fail_close_settings_app_by_pass_ids": [],
                    "user_allowed_to_add_partner": "1",
                    "follow_global_for_partner_login": "1",
                    "follow_global_for_zpa_reauth": "1",
                    "zpa_reauth_config": None,
                    "zpa_auto_reauth_timeout": 30,
                    "follow_global_for_packet_capture": "1",
                    "enable_local_packet_capture": "0",
                    "enable_local_packet_capture_v2": 0,
                    "exit_password": "",
                    "follow_routing_table": "1",
                    "use_default_adapter_for_dns": "1",
                    "update_dns_search_order": "1",
                    "use_zscaler_notification_framework": "0",
                    "switch_focus_to_notification": "0",
                    "fallback_to_gateway_domain": "1",
                    "use_proxy_port_for_t1": "0",
                    "use_proxy_port_for_t2": "0",
                    "allow_pac_exclusions_only": "0",
                    "use_wsa_poll_for_zpa": "0",
                    "enable_zcc_revert": "0",
                    "zcc_revert_password": "",
                    "zpa_auth_exp_on_sleep": 0,
                    "zpa_auth_exp_on_sys_restart": 0,
                    "zpa_auth_exp_on_net_ip_change": 0,
                    "instant_force_zpa_reauth_state_update": 0,
                    "zpa_auth_exp_on_win_logon_session": 0,
                    "enable_set_proxy_on_vpn_adapters": 1,
                    "disable_dns_route_exclusion": 0,
                    "packet_tunnel_include_list_for_ipv6": "",
                    "intercept_zia_traffic_all_adapters": 0,
                    "enable_anti_tampering": 0,
                    "reactivate_anti_tampering_time": 0,
                    "zpa_auth_exp_session_lock_state_min_time_in_second": "0",
                    "zpa_auth_exp_on_win_session_lock": 0,
                    "source_port_based_bypasses": "3389:*",
                    "enforce_split_dns": 0,
                    "drop_quic_traffic": 0,
                    "zdp_disable_password": "",
                    "use_v8_js_engine": "1",
                    "zd_disable_password": "",
                    "zdx_disable_password": "",
                    "zpa_disable_password": "",
                    "advance_zpa_reauth": False,
                    "bypass_dns_traffic_using_udp_proxy": "0",
                    "reconnect_tun_on_wakeup": "0",
                    "enable_custom_theme": 0,
                    "delete_dhcp_option121_routes": "{\"trusted\":1,\"offTrusted\":1,\"vpnTrusted\":1,\"splitVpnTrusted\":1}",
                    "machine_idp_auth": False,
                    "nonce": "",
                    "packet_tunnel_dns_exclude_list": "",
                    "packet_tunnel_dns_include_list": "",
                    "packet_tunnel_exclude_list": (
                        "10.0.0.0/8,172.16.0.0/12,192.168.0.0/16,"
                        "224.0.0.0/4,255.255.255.255,169.254.0.0/16"
                    ),
                    "packet_tunnel_exclude_list_for_ipv6": "[FF00::/8],[FE80::/10],[FC00::/7]",
                    "packet_tunnel_include_list": "0.0.0.0/0",
                    "truncate_large_udpdns_response": 0,
                    "override_at_cmd_by_policy": 0,
                    "purge_kerberos_preferred_dc_cache": 0,
                    "rsc_mode_on_all_adapters": 0,
                    "enable_adapter_hardware_offloading": 0,
                    "support_zpa_search_domains_in_trp": 0,
                    "prioritize_dns_exclusions": 1,
                    "generate_cli_password_contract": {
                        "enable_cli": False,
                        "allow_zpa_disable_without_password": True,
                        "allow_zia_disable_without_password": True,
                        "allow_zdx_disable_without_password": True,
                    },
                    "location_ruleset_policies": {
                        "split_vpn_trusted": {"id": 0},
                        "vpn_trusted": {"id": 0},
                    },
                    "ddil_config": (
                        "{\"ddilEnabled\":0,"
                        "\"businessContinuityActivationDomain\":\"\","
                        "\"businessContinuityTestModeEnabled\":0}"
                    ),
                    "zcc_app_fail_open_policy": 0,
                    "zcc_tunnel_fail_policy": 0,
                    "allow_client_cert_caching_for_web_view2": "0",
                    "show_confirmation_dialog_for_cached_cert": "0",
                    "zcc_fail_close_settings_lockdown_on_firewall_error": "0",
                    "zcc_fail_close_settings_lockdown_on_driver_error": "0",
                    "enable_flow_based_tunnel": "0",
                    "one_id_mt_device_auth_enabled": "0",
                    "prevent_auto_reauth_during_device_lock": "0",
                    "client_connector_ui_language": 0,
                    "enable_network_traffic_process_mapping": 0,
                    "use_end_point_location_for_dc_selection": "0",
                    "recache_system_proxy": "0",
                    "enable_location_policy_override": 0,
                    "block_private_relay": "0",
                    "enable_automatic_packet_capture": "0",
                    "enable_apc_for_critical_sections": "1",
                    "enable_apc_for_other_sections": "1",
                    "enable_pc_additional_space": "1",
                    "pc_additional_space": "512",
                    "enable_custom_proxy_detection": "0",
                    "enable_crash_reporting": "0",
                    "zdx_lite_config_obj": (
                        "{\"localMetrics\":1,"
                        "\"endToEndDiagnostics\":{"
                        "\"trusted\":0,\"vpnTrusted\":0,"
                        "\"offTrusted\":0,\"splitVpnTrusted\":0"
                        "}}"
                    ),
                },
                refresh_kerberos_token=0,
                bypass_custom_app_ids=[],
                prioritize_dns_exclusions="1",
                allow_zpa_disable_without_password=False,
                allow_zia_disable_without_password=False,
                allow_zdx_disable_without_password=False,
                use_default_adapter_for_dns="1",
                update_dns_search_order="1",
                enforce_split_dns="0",
                disable_dns_route_exclusion="0",
                enable_set_proxy_on_vpn_adapters="0",
                drop_quic_traffic="0",
                follow_routing_table="1",
                rule_order_selected_option={"label": "2", "value": 2},
                billing_day_selected_option={"label": "1", "value": "1"},
                forwarding_profile_id=0,
                zia_posture_profile=[],
                users_option=0,
                users_selected=[],
                device_groups_option=0,
                device_groups=[],
                device_groups_selected=[],
                notification_template_selected=[],
                registry_name="",
                machine_token_option=0,
                machine_token_selected_option=0,
                zpa_auth_exp_session_lock_state_min_time_in_second="1",
                force_zpa_authentication_to_expire=[],
                log_mode_selected={"label": "Debug", "value": 3},
                ipv6_mode_selected={"label": "IPv6Native", "value": 4},
                flow_logging_selected=[],
                block_domain_selected=[],
                zpa_reauth_config=[],
                zpa_auto_reauth_timeout=[
                    {"label": "30", "value": 30},
                ],
                end_to_end_diagnostics_selected=[],
                block_inbound_traffic_selected=[],
                enable_captive_portal_detection=1,
                enable_fail_open=1,
                captive_portal_web_sec_disable_minutes=10,
                local_metrics=1,
                end_to_end_diagnostics={
                    "trusted": 0,
                    "vpn_trusted": 0,
                    "off_trusted": 0,
                    "split_vpn_trusted": 0,
                },
                reactivate_anti_tampering_time=0,
                zia_dr_method={"label": "Policy Based Access (Web only)", "value": 2},
                vpn_gateways=[],
                partner_domains=[],
                zcc_fail_close_settings_ip_bypasses=[],
                zcc_fail_close_settings_lockdown_on_tunnel_process_exit=1,
                zcc_fail_close_settings_exit_uninstall_password="",
                user_allowed_to_add_partner=1,
                follow_global_for_partner_login="1",
                follow_global_for_zpa_reauth="1",
                follow_global_for_packet_capture="1",
                enable_local_packet_capture="0",
                enable_local_packet_capture_v2=[],
                packet_tunnel_include_list=["0.0.0.0/0"],
                packet_tunnel_exclude_list=[
                    "10.0.0.0/8",
                    "172.16.0.0/12",
                    "192.168.0.0/16",
                    "224.0.0.0/4",
                    "255.255.255.255",
                    "169.254.0.0/16",
                ],
                packet_tunnel_include_list_for_ipv6=[],
                packet_tunnel_exclude_list_for_ipv6=[
                    "[FF00::/8]",
                    "[FE80::/10]",
                    "[FC00::/7]",
                ],
                packet_tunnel_dns_include_list=[],
                packet_tunnel_dns_exclude_list=[],
                source_port_based_bypasses=["3389:*"],
                use_v8_js_engine="1",
                disable_parallel_ipv4and_ipv6="-1",
                device_type=3,
                windows_policy={
                    "cache_system_proxy": "0",
                    "disable_password": "",
                    "disable_loop_back_restriction": "0",
                    "remove_exempted_containers": "1",
                    "disable_parallel_ipv4and_ipv6": "-1",
                    "flow_logger_config": "",
                    "domain_profile_detection_config": (
                        "{\"trusted\":0,\"vpnTrusted\":0,"
                        "\"offTrusted\":0,\"splitVpnTrusted\":0}"
                    ),
                    "zpa_reauth_config": (
                        "{\"trusted\":0,\"vpnTrusted\":0,"
                        "\"offTrusted\":0,\"splitVpnTrusted\":0}"
                    ),
                    "all_inbound_traffic_config": "",
                    "install_ssl_certs": 1,
                    "trigger_domain_profle_detection": 0,
                    "logout_password": "",
                    "override_wpad": 0,
                    "pac_data_path": "",
                    "pac_type": 1,
                    "prioritize_i_pv4": 0,
                    "restart_win_http_svc": 0,
                    "sccm_config": None,
                    "uninstall_password": "",
                    "wfp_driver": 0,
                    "captive_portal_config": (
                        "{\"automaticCapture\":1,"
                        "\"enableCaptivePortalDetection\":1,"
                        "\"enableFailOpen\":1,"
                        "\"captivePortalWebSecDisableMinutes\":10,"
                        "\"enableEmbeddedCaptivePortal\":0}"
                    ),
                    "install_windows_firewall_inbound_rule": "1",
                    "force_location_refresh_sccm": 0,
                    "wfp_mtr": 0,
                    "enable_custom_proxy_detection": "0",
                    "enable_zscaler_firewall": "0",
                    "captive_portal_url_id": 1,
                },
                enable_zcc_revert=False,
                disaster_recovery={
                    "allow_zia_test": False,
                    "allow_zpa_test": False,
                    "enable_zia_dr": False,
                    "enable_zpa_dr": False,
                    "zia_dr_method": 2,
                    "zia_custom_db_url": "",
                    "use_zia_global_db": True,
                    "zia_domain_name": "",
                    "zia_rsa_pub_key_name": "",
                    "zia_rsa_pub_key": "",
                    "zpa_domain_name": "",
                    "zpa_rsa_pub_key_name": "",
                    "zpa_rsa_pub_key": "",
                },
                custom_dns=[],
                enable_custom_proxy_detection="0",
                client_connector_ui_language=0,
                one_id_mt_device_auth_enabled="0",
                prevent_auto_reauth_during_device_lock="0",
                instant_force_zpa_reauth_state_update=0,
                enable_network_traffic_process_mapping=0,
                use_end_point_location_for_dc_selection="0",
                recache_system_proxy="0",
                enable_location_policy_override=0,
                vpn_trusted=[],
                split_vpn_trusted=[],
                trusted=[],
                off_trusted=[],
                block_private_relay="0",
                enable_crash_reporting="0",
                enable_automatic_packet_capture="0",
                enable_apc_for_critical_sections="1",
                enable_apc_for_other_sections="1",
                enable_pc_additional_space="1",
                pc_additional_space=[
                    {"label": "1GB", "value": "1024"},
                ],
                app_service_custom_ids_selected=[],
                bypass_app_ids=[],
                bypass_mac_app_ids=[],
                zcc_fail_close_settings_app_by_pass_selected=[],
                zcc_fail_close_settings_app_by_pass_ids=[],
                browser_auth_type={"label": "FOLLOW_GLOBAL_CONFIG", "value": -1},
                use_default_browser=0,
            )
            # The /web/policy/edit endpoint behaves like a fire-and-forget
            # PUT — it does NOT echo the persisted policy back. The only
            # body it returns is ``{"success": "true", "id": <new_id>}``,
            # and the only meaningful checks are therefore that the success
            # flag is "true" and that the returned id is non-zero. Anything
            # beyond that (name, description, nested config, etc.) is
            # round-tripped via list_by_company, not via this endpoint.
            #
            # Capture the new id eagerly — before the assertions — so that
            # the finally block can always clean up the policy on the live
            # tenant even if a later assertion fails.
            body = response.get_body() if response is not None else None
            if isinstance(body, dict):
                raw_id = body.get("id")
                if raw_id is not None:
                    try:
                        policy_id = int(raw_id)
                    except (TypeError, ValueError):
                        policy_id = None

            assert err is None, f"Error creating web policy: {err}"
            assert isinstance(body, dict), (
                f"Expected a dict response body, got {type(body).__name__}: {body!r}"
            )
            assert str(body.get("success", "")).lower() == "true", (
                f"Expected success='true', got {body.get('success')!r}"
            )
            assert policy_id, (
                f"Expected a non-zero id on the created web policy, got {body.get('id')!r}"
            )
        except Exception as exc:
            errors.append(f"Web policy creation failed: {exc}")

        try:
            if policy_id:
                policies, _, err = client.zcc.web_policy.list_by_company(
                    query_params={"device_type": "windows"}
                )
                assert err is None, f"Error listing web policies by device_type: {err}"
                assert isinstance(policies, list), "Expected a list of web policies"
                # Normalise to int — IDs may come back as int or float in
                # the listing depending on the underlying transport.
                assert any(
                    getattr(p, "id", None) is not None
                    and int(getattr(p, "id")) == int(policy_id)
                    for p in policies
                ), "Created policy not found in device_type=windows listing"
        except Exception as exc:
            errors.append(f"Listing web policies by device_type failed: {exc}")

        try:
            if policy_id:
                _, response, err = client.zcc.web_policy.list_by_company(
                    query_params={"device_type": "windows"}
                )
                assert err is None, f"Error listing web policies for JMESPath search: {err}"
                assert response is not None, "Expected a response object for client-side filtering"

                matches = response.search(f"[?name == '{policy_name}']")
                assert isinstance(matches, list), "Expected JMESPath search to return a list"
                assert any(
                    int(match.get("id", 0)) == int(policy_id) for match in matches
                ), f"JMESPath did not match the created policy id={policy_id}"
        except Exception as exc:
            errors.append(f"JMESPath search on web policy listing failed: {exc}")

        finally:
            if policy_id:
                try:
                    _, _, err = client.zcc.web_policy.delete_web_policy(policy_id)
                    assert err is None, f"Error deleting web policy {policy_id}: {err}"
                except Exception as cleanup_exc:
                    errors.append(
                        f"Cleanup failed for web policy ID {policy_id}: {cleanup_exc}"
                    )

        assert len(errors) == 0, (
            f"Errors occurred during the web policy lifecycle test:\n"
            f"{chr(10).join(errors)}"
        )
