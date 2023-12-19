from mocks import MockZPAClient, my_vcr, assert_responses_exclude_computed, get_client_config
import pytest

@pytest.mark.vcr
def test_get_posture_profile(request):
    client_config = get_client_config()
    client = MockZPAClient(**client_config)

    # Use the name of the test function for the cassette file
    cassette_name = request.node.name + '.yaml'
    with my_vcr.use_cassette(cassette_name):
        response = client.posture_profiles.list_profiles()

    actual_response = [response[0].to_dict()] if response else []

    # Adjusted expected response
    expected_response = [
        {
            "id": "72058304855015457",
            "modified_time": "1634674517",
            "creation_time": "1634674517",
            "modified_by": "72057594037927995",
            "name": "CrowdStrike_ZPA_Pre-ZTA (zscalerbeta.net)",
            "posture_udid": "cfab2ee9-9bf4-4482-9dcc-dadf7311c49b",
            "zscaler_cloud": "zscalerbeta"
        }
    ]

    assert_responses_exclude_computed(actual_response, expected_response)