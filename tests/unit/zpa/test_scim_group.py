from mocks import MockZPAClient, my_vcr, assert_responses_exclude_computed, get_client_config
import pytest

@pytest.mark.vcr
def test_get_scim_group(request):
    client_config = get_client_config()
    client = MockZPAClient(**client_config)

    # Use the name of the test function for the cassette file
    cassette_name = request.node.name + '.yaml'
    with my_vcr.use_cassette(cassette_name):
        response = client.scim_groups.list_groups('72058304855015570')

    actual_response = [response[0].to_dict()] if response else []

    # Adjusted expected response
    expected_response = [
        {
            "id": 125379,
            "modified_time": 1680672466,
            "creation_time": 1680672466,
            "name": "Developer",
            "idp_id": 72058304855015570,
            "internal_id": "5b8f4f26-59e0-4a49-a13c-7198d1344fc9"
        }
    ]

    assert_responses_exclude_computed(actual_response, expected_response)