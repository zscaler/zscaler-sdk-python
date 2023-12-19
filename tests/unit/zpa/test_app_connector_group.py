from mocks import MockZPAClient, my_vcr, assert_responses_exclude_computed, get_client_config
import pytest


@pytest.mark.vcr
def test_get_app_connector_group(request):
    client_config = get_client_config()
    client = MockZPAClient(**client_config)


    # Use the name of the test function for the cassette file
    cassette_name = request.node.name + '.yaml'
    with my_vcr.use_cassette(cassette_name):
        response = client.connectors.list_connector_groups()

    # Get only the first item from the response if it exists
    actual_response = [response[0].to_dict()] if response else []

    # Adjusted expected response
    expected_response = [
        {
            "id": "72058304855047746",
            "modified_time": "1702801118",
            "creation_time": "1700282878",
            "modified_by": "72058304855015425",
            "name": "SIPA_App_Connector_Group01",
            "enabled": True,
            "description": "DO NOT DELETE - USED FOR INTEGRATION TESTS",
            "version_profile_id": "0",
            "override_version_profile": True,
            "version_profile_name": "Default",
            "version_profile_visibility_scope": "ALL",
            "upgrade_time_in_secs": "28800",
            "upgrade_day": "MONDAY",
            "location": "San Jose, CA, USA",
            "latitude": "37.33874",
            "longitude": "-121.8852525",
            "dns_query_type": "IPV4",
            "city_country": "San Jose, US",
            "country_code": "US",
            "tcp_quick_ack_app": False,
            "tcp_quick_ack_assistant": False,
            "tcp_quick_ack_read_assistant": False,
            "pra_enabled": False,
            "use_in_dr_mode": False,
            "waf_disabled": False,
            "microtenant_name": "Default",
            "lss_app_connector_group": False
        }
    ]
    assert_responses_exclude_computed(actual_response, expected_response)