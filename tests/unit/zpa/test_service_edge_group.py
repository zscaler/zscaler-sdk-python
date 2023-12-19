from mocks import MockZPAClient, my_vcr, assert_responses_exclude_computed, get_client_config
import pytest

@pytest.mark.vcr
def test_get_service_edge_group(request):
    client_config = get_client_config()
    client = MockZPAClient(**client_config)

    # Use the name of the test function for the cassette file
    cassette_name = request.node.name + '.yaml'
    with my_vcr.use_cassette(cassette_name):
        response = client.service_edges.list_service_edge_groups()

    actual_response = [response[0].to_dict()] if response else []

    # Adjusted expected response
    expected_response = [
        {
            "id": "72058304855063609",
            "modified_time": "1702802935",
            "creation_time": "1702802935",
            "modified_by": "72058304855015425",
            "name": "example",
            "enabled": True,
            "version_profile_id": "0",
            "override_version_profile": False,
            "version_profile_name": "Default",
            "version_profile_visibility_scope": "ALL",
            "upgrade_time_in_secs": "28800",
            "upgrade_day": "MONDAY",
            "is_public": "FALSE",
            "location": "San Jose, CA, USA",
            "latitude": "37.33874",
            "longitude": "-121.8852525",
            "city_country": "San Jose, US",
            "country_code": "US",
            "use_in_dr_mode": False,
            "grace_distance_enabled": False,
            "microtenant_name": "Default"
        }
    ]
    assert_responses_exclude_computed(actual_response, expected_response)