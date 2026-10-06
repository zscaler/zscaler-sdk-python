"""
Testing ZPA enrollment certificate lookup for App Connector and Service Edge groups
"""

from unittest.mock import Mock

import pytest

from zscaler.zpa.app_connector_groups import AppConnectorGroupAPI
from zscaler.zpa.enrollment_certificates import EnrollmentCertificateAPI
from zscaler.zpa.models.enrollment_certificates import EnrollmentCertificate
from zscaler.zpa.service_edge_group import ServiceEdgeGroupAPI

CONFIG = {"client": {"customerId": "1234567890"}}
GROUP_ID = "72058304855090128"

GROUP_METHODS = [
    (AppConnectorGroupAPI, "add_connector_group", (), "Connector"),
    (AppConnectorGroupAPI, "update_connector_group", (GROUP_ID,), "Connector"),
    (ServiceEdgeGroupAPI, "add_service_edge_group", (), "Service Edge"),
    (ServiceEdgeGroupAPI, "update_service_edge_group", (GROUP_ID,), "Service Edge"),
]
METHOD_IDS = [f"{cls.__name__}.{method}" for cls, method, _, _ in GROUP_METHODS]


def _group_api(api_cls, cert=None, lookup_error=None):
    executor = Mock()
    executor.create_request.return_value = ({}, None)
    response = Mock()
    response.get_body.return_value = {}
    executor.execute.return_value = (response, None)

    api = api_cls(executor, CONFIG)
    api._enrollment_certificates.get_enrolment_by_name = Mock(return_value=(cert, None, lookup_error))
    return api, executor


def _sent_body(executor):
    call = executor.create_request.call_args
    return call.kwargs["body"] if "body" in call.kwargs else call.args[2]


@pytest.mark.parametrize("api_cls, method, args, cert_name", GROUP_METHODS, ids=METHOD_IDS)
def test_enrollment_cert_id_is_looked_up_when_missing(api_cls, method, args, cert_name):
    api, executor = _group_api(api_cls, cert=EnrollmentCertificate({"id": "6573", "name": cert_name}))

    _, _, err = getattr(api, method)(*args, name="group-a")

    assert err is None
    api._enrollment_certificates.get_enrolment_by_name.assert_called_once_with(cert_name)
    assert _sent_body(executor)["enrollment_cert_id"] == "6573"


@pytest.mark.parametrize("api_cls, method, args, cert_name", GROUP_METHODS, ids=METHOD_IDS)
def test_explicit_enrollment_cert_id_is_kept(api_cls, method, args, cert_name):
    api, executor = _group_api(api_cls)

    _, _, err = getattr(api, method)(*args, name="group-a", enrollment_cert_id="9999")

    assert err is None
    api._enrollment_certificates.get_enrolment_by_name.assert_not_called()
    assert _sent_body(executor)["enrollment_cert_id"] == "9999"


@pytest.mark.parametrize("api_cls, method, args, cert_name", GROUP_METHODS, ids=METHOD_IDS)
def test_lookup_error_is_returned(api_cls, method, args, cert_name):
    error = ValueError(f"Enrollment certificate '{cert_name}' not found")
    api, executor = _group_api(api_cls, lookup_error=error)

    assert getattr(api, method)(*args, name="group-a") == (None, None, error)
    executor.create_request.assert_not_called()


def _cert_api(certs, error=None):
    api = EnrollmentCertificateAPI(Mock(), CONFIG)
    api.list_enrolment = Mock(return_value=(certs, None, error))
    return api


def test_get_enrolment_by_name_returns_exact_match():
    api = _cert_api(
        [
            EnrollmentCertificate({"id": "1", "name": "Connector-Custom"}),
            EnrollmentCertificate({"id": "6573", "name": "Connector"}),
        ]
    )

    cert, _, err = api.get_enrolment_by_name("connector")

    assert err is None
    assert cert.id == "6573"
    api.list_enrolment.assert_called_once_with(query_params={"search": "connector"})


def test_get_enrolment_by_name_not_found():
    api = _cert_api([EnrollmentCertificate({"id": "1", "name": "Connector-Custom"})])

    cert, _, err = api.get_enrolment_by_name("Connector")

    assert cert is None
    assert isinstance(err, ValueError)
    assert str(err) == "Enrollment certificate 'Connector' not found"


def test_get_enrolment_by_name_propagates_list_error():
    error = Exception("boom")
    api = _cert_api(None, error=error)

    assert api.get_enrolment_by_name("Connector") == (None, None, error)
