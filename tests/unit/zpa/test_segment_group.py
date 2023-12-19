from mocks import MockZPAClient, my_vcr, assert_responses_exclude_computed, get_client_config
import pytest

@pytest.mark.vcr
def test_get_segment_groups(request):
    client_config = get_client_config()
    client = MockZPAClient(**client_config)

    # Use the name of the test function for the cassette file
    cassette_name = request.node.name + '.yaml'
    with my_vcr.use_cassette(cassette_name):
        response = client.segment_groups.list_groups()

    actual_response = [response[0].to_dict()] if response else []

    # Adjusted expected response
    expected_response = [
        {
            "id": "72058304855063610",
            "modified_time": "1702873898",
            "creation_time": "1702873898",
            "modified_by": "72058304855015425",
            "name": "segGroup01",
            "description": "segGroup01",
            "enabled": True,
            "applications": [
                {
                    "id": "72058304855063612",
                    "modified_time": "1702873898",
                    "creation_time": "1702873898",
                    "modified_by": "72058304855015425",
                    "name": "app01.bd-hashicorp.com",
                    "domain_name": "app01.bd-hashicorp.com",
                    "domain_names": [
                        "app01.bd-hashicorp.com"
                    ],
                    "description": "app01.bd-hashicorp.com",
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
                    "double_encrypt": False,
                    "health_check_type": "DEFAULT",
                    "icmp_access_type": "PING",
                    "bypass_type": "NEVER",
                    "config_space": "DEFAULT",
                    "ip_anchored": False,
                    "bypass_on_reauth": False,
                    "inspect_traffic_with_zia": False,
                    "tcp_keep_alive": "1",
                    "use_in_dr_mode": False,
                    "select_connector_close_to_app": False,
                    "adp_enabled": False,
                    "fqdn_dns_check": False,
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
                    ]
                }
            ],
            "policy_migrated": True,
            "config_space": "DEFAULT",
            "tcp_keep_alive_enabled": "0",
            "microtenant_name": "Default"
        }
    ]

    assert_responses_exclude_computed(actual_response, expected_response)