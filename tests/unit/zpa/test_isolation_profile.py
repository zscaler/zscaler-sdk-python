from mocks import MockZPAClient, my_vcr, assert_responses_exclude_computed, get_client_config
import pytest

@pytest.mark.vcr
def test_get_isolation_profile(request):
    client_config = get_client_config()
    client = MockZPAClient(**client_config)

    # Use the name of the test function for the cassette file
    cassette_name = request.node.name + '.yaml'
    with my_vcr.use_cassette(cassette_name):
      response = client.isolation_profile.list_profiles()

    actual_response = [response[0].to_dict()] if response else []

    # Adjusted expected response
    expected_response = [
    {
      "id": "72058304855039035",
      "creation_time": "1697861956",
      "modified_by": "72058304855021669",
      "name": "BD   SA   Profile",
      "description": "BD   SA   Profile",
      "enabled": True,
      "isolation_tenant_id": "f4056f5b-1758-41ab-b046-d700a8f569f6",
      "isolation_profile_id": "6a1cef8b-8c40-4fa6-8bcd-b0e5b4c43c8a",
      "isolation_url": "https://redirect.isolation-beta.zscaler.com/tenant/support/profile/6a1cef8b-8c40-4fa6-8bcd-b0e5b4c43c8a/zpa/render"
    },
    {
      "id": "72058304855039034",
      "creation_time": "1697861956",
      "modified_by": "72058304855021669",
      "name": "BD  SA Profile",
      "description": "BD  SA Profile",
      "enabled": True,
      "isolation_tenant_id": "f4056f5b-1758-41ab-b046-d700a8f569f6",
      "isolation_profile_id": "76578fc4-b47e-4fe4-aaea-224c46ccc6fa",
      "isolation_url": "https://redirect.isolation-beta.zscaler.com/tenant/support/profile/76578fc4-b47e-4fe4-aaea-224c46ccc6fa/zpa/render"
    },
    {
      "id": "72058304855039033",
      "creation_time": "1697861956",
      "modified_by": "72058304855021669",
      "name": "BD SA Profile",
      "description": "BD SA Profile",
      "enabled": True,
      "isolation_tenant_id": "f4056f5b-1758-41ab-b046-d700a8f569f6",
      "isolation_profile_id": "e1d2fb99-af9a-4975-8cfa-a652c08ca4c7",
      "isolation_url": "https://redirect.isolation-beta.zscaler.com/tenant/support/profile/e1d2fb99-af9a-4975-8cfa-a652c08ca4c7/zpa/render"
    },
    {
      "id": "72058304855021636",
      "creation_time": "1689807124",
      "modified_by": "72058304855015425",
      "name": "BD_SA_Profile1",
      "description": "BD_SA_Profile1",
      "enabled": True,
      "isolation_tenant_id": "f4056f5b-1758-41ab-b046-d700a8f569f6",
      "isolation_profile_id": "539fb9cc-f6e7-476d-ac5e-de555df1b9ab",
      "isolation_url": "https://redirect.isolation-beta.zscaler.com/tenant/support/profile/539fb9cc-f6e7-476d-ac5e-de555df1b9ab/zpa/render"
    },
    {
      "id": "72058304855021637",
      "creation_time": "1689807142",
      "modified_by": "72058304855015425",
      "name": "BD_SA_Profile2",
      "description": "BD_SA_Profile2",
      "enabled": True,
      "isolation_tenant_id": "f4056f5b-1758-41ab-b046-d700a8f569f6",
      "isolation_profile_id": "4aa60e1d-fad2-48ba-92ab-5230b1c16bc5",
      "isolation_url": "https://redirect.isolation-beta.zscaler.com/tenant/support/profile/4aa60e1d-fad2-48ba-92ab-5230b1c16bc5/zpa/render"
    }
    ]

    # Debug: Print actual and expected name fields
    for actual_item, expected_item in zip(actual_response, expected_response):
        print(f"Actual name: {actual_item.get('name')}, Expected name: {expected_item.get('name')}")

    assert_responses_exclude_computed(actual_response, expected_response)