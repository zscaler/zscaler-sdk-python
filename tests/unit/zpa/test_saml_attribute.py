from mocks import MockZPAClient, my_vcr, assert_responses_exclude_computed, get_client_config
import pytest

@pytest.mark.vcr
def test_get_saml_attributes(request):
    client_config = get_client_config()
    client = MockZPAClient(**client_config)

    # Use the name of the test function for the cassette file
    cassette_name = request.node.name + '.yaml'
    with my_vcr.use_cassette(cassette_name):
        response = client.saml_attributes.list_attributes()

    actual_response = [response[0].to_dict()] if response else []

    # Adjusted expected response
    expected_response = [
        {
            "id": "72058304855021552",
            "modified_time": "1688516960",
            "creation_time": "1688516931",
            "modified_by": "72058304855015425",
            "name": "DepartmentName_BD_Okta_Users",
            "user_attribute": False,
            "idp_id": "72058304855015574",
            "saml_name": "DepartmentName",
            "idp_name": "BD_Okta_Users"
        }
    ]

    assert_responses_exclude_computed(actual_response, expected_response)