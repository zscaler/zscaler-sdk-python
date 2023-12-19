from mocks import MockZPAClient, my_vcr, assert_responses_exclude_computed, get_client_config
import pytest

@pytest.mark.vcr
def test_get_scim_attribute_header(request):
    client_config = get_client_config()
    client = MockZPAClient(**client_config)

    # Use the name of the test function for the cassette file
    cassette_name = request.node.name + '.yaml'
    with my_vcr.use_cassette(cassette_name):
        response = client.scim_attributes.list_attributes_by_idp('72058304855015574')

    actual_response = [response[0].to_dict()] if response else []

    # Adjusted expected response
    expected_response = [
        {
            "id": "72058304855015582",
            "creation_time": "1678901732",
            "modified_by": "72058304855015425",
            "name": "active",
            "idp_id": "72058304855015574",
            "data_type": "Boolean",
            "multivalued": False,
            "required": False,
            "case_sensitive": False,
            "mutability": "readWrite",
            "returned": "default",
            "uniqueness": False,
            "delta": "f8b30ccace71f0089117dae8a02065e4"
        }
    ]

    assert_responses_exclude_computed(actual_response, expected_response)