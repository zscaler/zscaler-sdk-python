"""
Testing that ZIA and ZPA methods return the (result, response, error) APIResult tuple on every path
"""

from unittest.mock import Mock

import pytest

from zscaler.zia.locations import LocationsAPI
from zscaler.zia.outbound_email_dlp_rules import OutboundEmailDLPRulesAPI
from zscaler.zia.policy_export import PolicyExportAPI
from zscaler.zia.traffic_vpn_credentials import TrafficVPNCredentialAPI
from zscaler.zpa.c2c_ip_ranges import IPRangesAPI
from zscaler.zpa.client_settings import ClientSettingsAPI
from zscaler.zpa.enrollment_certificates import EnrollmentCertificateAPI
from zscaler.zpa.microtenants import MicrotenantsAPI
from zscaler.zpa.role_controller import RoleControllerAPI
from zscaler.zpa.saml_attributes import SAMLAttributesAPI
from zscaler.zpa.user_portal_controller import UserPortalControllerAPI
from zscaler.zpa.user_portal_link import UserPortalLinkAPI

ZPA_CONFIG = {"client": {"customerId": "1234567890"}}


def _executor(create_error=None, execute_error=None, body=None, content=b""):
    executor = Mock()
    executor.create_request.return_value = (None if create_error else {}, create_error)
    response = Mock()
    response.get_body.return_value = body
    response.content = content
    executor.execute.return_value = (response, execute_error)
    return executor, response


# (api factory, method, args, expected success result)
METHODS = [
    (LocationsAPI, "bulk_delete_locations", ([1, 2],), None),
    (TrafficVPNCredentialAPI, "bulk_delete_vpn_credentials", ([1, 2],), None),
    (OutboundEmailDLPRulesAPI, "get_actions", (), b"csv-bytes"),
    (PolicyExportAPI, "policy_export", (["URL_FILTERING"],), b"csv-bytes"),
    (lambda ex: IPRangesAPI(ex, ZPA_CONFIG), "delete_ip_range", ("1",), None),
    (lambda ex: ClientSettingsAPI(ex, ZPA_CONFIG), "delete_client_setting", (), None),
    (lambda ex: EnrollmentCertificateAPI(ex, ZPA_CONFIG), "delete_enrollment_certificate", ("1",), None),
    (lambda ex: RoleControllerAPI(ex, ZPA_CONFIG), "delete_role", ("1",), None),
    (lambda ex: SAMLAttributesAPI(ex, ZPA_CONFIG), "delete_saml_attribute", ("1",), None),
    (lambda ex: UserPortalControllerAPI(ex, ZPA_CONFIG), "delete_user_portal", ("1",), None),
    (lambda ex: UserPortalLinkAPI(ex, ZPA_CONFIG), "delete_portal_link", ("1",), None),
]
IDS = [method for _, method, _, _ in METHODS]


@pytest.mark.parametrize("factory, method, args, expected", METHODS, ids=IDS)
def test_success_returns_result_response_none(factory, method, args, expected):
    executor, response = _executor(content=b"csv-bytes")

    assert getattr(factory(executor), method)(*args) == (expected, response, None)


@pytest.mark.parametrize("factory, method, args, expected", METHODS, ids=IDS)
def test_create_request_error_returns_none_none_error(factory, method, args, expected):
    error = Exception("create failed")
    executor, _ = _executor(create_error=error)

    assert getattr(factory(executor), method)(*args) == (None, None, error)


@pytest.mark.parametrize("factory, method, args, expected", METHODS, ids=IDS)
def test_execute_error_returns_none_response_error(factory, method, args, expected):
    error = Exception("execute failed")
    executor, response = _executor(execute_error=error)

    assert getattr(factory(executor), method)(*args) == (None, response, error)


@pytest.mark.parametrize(
    "factory, method, ids",
    [
        (LocationsAPI, "bulk_delete_locations", []),
        (LocationsAPI, "bulk_delete_locations", list(range(101))),
        (TrafficVPNCredentialAPI, "bulk_delete_vpn_credentials", []),
        (TrafficVPNCredentialAPI, "bulk_delete_vpn_credentials", list(range(101))),
    ],
    ids=["locations-empty", "locations-over-100", "vpn-empty", "vpn-over-100"],
)
def test_bulk_delete_validation_errors(factory, method, ids):
    executor, _ = _executor()

    result, response, error = getattr(factory(executor), method)(ids)

    assert (result, response) == (None, None)
    assert isinstance(error, ValueError)
    executor.create_request.assert_not_called()


def test_get_microtenant_summary_returns_tuple():
    executor, response = _executor(body=[{"id": "1", "name": "tenant-a"}, {"id": "2", "name": "tenant-b"}])

    result, resp, err = MicrotenantsAPI(executor, ZPA_CONFIG).get_microtenant_summary()

    assert err is None
    assert resp is response
    assert [(m.id, m.name) for m in result] == [("1", "tenant-a"), ("2", "tenant-b")]


@pytest.mark.parametrize("create_error, execute_error", [(Exception("create"), None), (None, Exception("execute"))])
def test_get_microtenant_summary_errors(create_error, execute_error):
    executor, response = _executor(create_error=create_error, execute_error=execute_error)

    result, resp, err = MicrotenantsAPI(executor, ZPA_CONFIG).get_microtenant_summary()

    assert result is None
    assert err is (create_error or execute_error)
    assert resp is (None if create_error else response)
