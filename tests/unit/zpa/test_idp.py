from mocks import MockZPAClient, my_vcr, assert_responses_exclude_computed, get_client_config
import pytest

@pytest.mark.vcr
def test_get_idp(request):
    client_config = get_client_config()
    client = MockZPAClient(**client_config)

    # Use the name of the test function for the cassette file
    cassette_name = request.node.name + '.yaml'
    with my_vcr.use_cassette(cassette_name):
        response = client.idp.list_idps()

    actual_response = [response[0].to_dict()] if response else []

    # Adjusted expected response
    expected_response = [
        {
            "id": "72058304855015572",
            "modified_time": "1688516838",
            "creation_time": "1678900488",
            "modified_by": "72058304855015425",
            "name": "BD_Okta_Admin",
            "certificates": [
                {
                    "cname": "dev-151399",
                    "serial_no": "1678900597535",
                    "certificate": "-----BEGIN CERTIFICATE-----\nMIIDpDCCAoygAwIBAgIGAYbmRhMfMA0GCSqGSIb3DQEBCwUAMIGSMQswCQYDVQQG\nEwJVUzETMBEGA1UECAwKQ2FsaWZvcm5pYTEWMBQGA1UEBwwNU2FuIEZyYW5jaXNj\nbzENMAsGA1UECgwET2t0YTEUMBIGA1UECwwLU1NPUHJvdmlkZXIxEzARBgNVBAMM\nCmRldi0xNTEzOTkxHDAaBgkqhkiG9w0BCQEWDWluZm9Ab2t0YS5jb20wHhcNMjMw\nMzE1MTcxNTM3WhcNMzMwMzE1MTcxNjM3WjCBkjELMAkGA1UEBhMCVVMxEzARBgNV\nBAgMCkNhbGlmb3JuaWExFjAUBgNVBAcMDVNhbiBGcmFuY2lzY28xDTALBgNVBAoM\nBE9rdGExFDASBgNVBAsMC1NTT1Byb3ZpZGVyMRMwEQYDVQQDDApkZXYtMTUxMzk5\nMRwwGgYJKoZIhvcNAQkBFg1pbmZvQG9rdGEuY29tMIIBIjANBgkqhkiG9w0BAQEF\nAAOCAQ8AMIIBCgKCAQEA3RNfMfh9FxFRErVAF1C3KpoJagsEuTIuRy2LscZintaI\nMioRzXqslbjcPHFZGS7499aihvX6CzjDnuy+JD46Fjlhv0a9vEPW6BIhI6XNSoCi\n/Wjwt2atbxScR2sAVeLNpiZ81ExEFnQ2dSdShNTP7aqNBRW+BaSyYM2JKlbPp7TW\n3RngJMTj7mA9wXPoA3rtwIfeQf3DRymkAko+G/1OnqlLcxmicl+Qnvynd3WNWpnF\nys1Ub+hfJHZ6m0E5VKq1s1uQ9EDRsC+H0O6Xs9JthGdOxK4QfASYffmMdiHm1zu2\n8Sejz3v8hv1CayKUZROPBkr80gtpLqmaTQ/nM8TiaQIDAQABMA0GCSqGSIb3DQEB\nCwUAA4IBAQAh0QLHhU1mVYQM1hp5V3tfM2eJ8miHu413LAII19OKhSQrhfCbbVhV\nGpcVMqLqHVl9UiHu4qXIhlyp76fZZ2frph1/M/Yb03BAqYgGkXCOsi0D2arTIvXg\nNlGw/tHlkaQZ8oWlRMitudFJplYu1EXPJyQ57NBigN0xrlbH+0QWPDBQx3JgjBvi\njRezIz5jPNxn0EPmBZtE/s7hLA7tFlYXXqr42HRW+jgWucEjIjQsTLELWCgIHjcJ\nx9aaEE+uUsMpeTQ1QqU8rgkuG1Y9kRJ5N2GkVQY58j5+4z8+GultxaMu5rWWobAU\npIw0EakAdtOhEcppP8MWo+fHXKcbDWVb\n-----END CERTIFICATE-----\n",
                    "valid_from_in_sec": "1678900537",
                    "valid_to_in_sec": "1994519797"
                }
            ],
            "login_url": "https://dev-151399.okta.com/app/zscaler_private_access/exkbs3vq6zwBQ93ov4x7/sso/saml",
            "idp_entity_id": "http://www.okta.com/exkbs3vq6zwBQ93ov4x7",
            "auto_provision": "0",
            "sign_saml_request": "1",
            "sso_type": [
                "ADMIN"
            ],
            "domain_list": [
                "securitygeek.io"
            ],
            "use_custom_sp_metadata": True,
            "scim_enabled": False,
            "enable_scim_based_policy": False,
            "disable_saml_based_policy": False,
            "reauth_on_user_update": False,
            "admin_sp_signing_cert_id": "0",
            "enable_arbitrary_auth_domains": "0",
            "admin_metadata": {
                "sp_entity_id": "https://adminsamlsp.zpabeta.net/auth/metadata/72058304855015572",
                "sp_post_url": "https://adminsamlsp.zpabeta.net/auth/72058304855015572/sso",
                "certificate_url": "https://adminsamlsp.zpabeta.net/auth/72058304855015572/certificate",
                "sp_metadata_url": "https://adminsamlsp.zpabeta.net/auth/72058304855015572/metadata",
                "sp_base_url": "https://adminsamlsp.zpabeta.net/auth"
            },
            "one_identity_enabled": False,
            "scim_service_provider_endpoint": "https://scim1.zpabeta.net/scim/1/72058304855015572/v2",
            "scim_shared_secret_exists": False,
            "force_auth": False,
            "login_hint": True,
            "enabled": True,
            "redirect_binding": True,
            "delta": "bccf20da4bc72363799f72f6eee18b0d"
        },
    ]

    # Debug: Print actual and expected name fields
    for actual_item, expected_item in zip(actual_response, expected_response):
        print(f"Actual name: {actual_item.get('name')}, Expected name: {expected_item.get('name')}")

    # Assert ignoring computed fields
    assert_responses_exclude_computed(actual_response, expected_response)