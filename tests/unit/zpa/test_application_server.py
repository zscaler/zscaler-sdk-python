from mocks import MockZPAClient, my_vcr, assert_responses_exclude_computed, get_client_config
import pytest

@pytest.mark.vcr
def test_get_application_server(request):
    client_config = get_client_config()
    client = MockZPAClient(**client_config)

    cassette_name = request.node.name + '.yaml'
    with my_vcr.use_cassette(cassette_name):
        response = client.servers.list_servers()

    actual_response = [response[0].to_dict()] if response else []

    # Adjusted expected response
    expected_response = [
        {
            "id": "72058304855063608",
            'modified_by': '72058304855015425',
            'modified_time': '1702800432',
            'creation_time': '1702800432',
            "name": "app01",
            "address": "192.168.1.1",
            "enabled": True,
            "description": "app01",
            "config_space": "DEFAULT"
        }
    ]

    assert_responses_exclude_computed(actual_response, expected_response)