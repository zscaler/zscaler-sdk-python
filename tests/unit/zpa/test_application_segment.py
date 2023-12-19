from mocks import MockZPAClient, my_vcr, assert_responses_exclude_computed, get_client_config
import pytest

@pytest.mark.vcr
def test_get_application_segment(request):
    client_config = get_client_config()
    client = MockZPAClient(**client_config)

    cassette_name = request.node.name + '.yaml'
    with my_vcr.use_cassette(cassette_name):
        response = client.app_segments.list_segments()

    actual_response = [response[0].to_dict()] if response else []

    # Adjusted expected response
    expected_response = [
            {
                "modified_time": "1702873898",
                "creation_time": "1702873898",
                "modified_by": "72058304855015425",
                "id": "72058304855063612",
                "domain_names": [
                    "app01.bd-hashicorp.com"
                ],
                "name": "app01.bd-hashicorp.com",
                "description": "app01.bd-hashicorp.com",
                "server_groups": [
                    {
                        "id": "72058304855063611",
                        "modified_time": "1702873898",
                        "creation_time": "1702873898",
                        "modified_by": "72058304855015425",
                        "name": "srvGroup01",
                        "enabled": True,
                        "description": "srvGroup01",
                        "config_space": "DEFAULT",
                        "dynamic_discovery": True
                    }
                ],
                "enabled": True,
                "passive_health_enabled": True,
                "tcp_port_ranges": [
                    "80",
                    "80"
                ],
                "udp_port_ranges": [
                    "80",
                    "80"
                ],
                "tcp_port_range": [
                    {
                        "from": "80",
                        "to": "80"
                    }
                ],
                "udp_port_range": [
                    {
                        "from": "80",
                        "to": "80"
                    }
                ],
                "double_encrypt": False,
                "config_space": "DEFAULT",
                "bypass_type": "NEVER",
                "health_check_type": "DEFAULT",
                "icmp_access_type": "PING",
                "is_cname_enabled": True,
                "ip_anchored": False,
                "bypass_on_reauth": False,
                "inspect_traffic_with_zia": False,
                "health_reporting": "ON_ACCESS",
                "use_in_dr_mode": False,
                "tcp_keep_alive": "1",
                "select_connector_close_to_app": False,
                "is_incomplete_dr_config": False,
                "adp_enabled": False,
                "fqdn_dns_check": False,
                "microtenant_name": "Default",
                "segment_group_id": "72058304855063610",
                "segment_group_name": "segGroup01"
            }
    ]

    assert_responses_exclude_computed(actual_response, expected_response)