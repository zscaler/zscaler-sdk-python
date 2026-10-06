"""
Testing ZPA policy rule payload construction
"""

from unittest.mock import Mock

import pytest

from zscaler.zpa.policies import PolicySetControllerAPI

APP_ID = "72058304855090128"


def _api():
    """Return an API whose policy-set lookup succeeds and whose PUT/POST body is captured."""
    executor = Mock()
    executor.create_request.return_value = ({}, None)
    response = Mock()
    response.get_body.return_value = {}
    executor.execute.return_value = (response, None)

    api = PolicySetControllerAPI(executor, {"client": {"customerId": "1234567890"}})
    api.get_policy = Mock(return_value=({"id": "72058304855090130"}, None, None))
    return api, executor


def _sent_body(executor):
    return executor.create_request.call_args.kwargs["body"]


@pytest.mark.parametrize("method", ["update_isolation_rule", "update_isolation_rule_v2"])
def test_update_isolation_rule_without_action(method):
    api, executor = _api()

    result, _, err = getattr(api, method)(rule_id="72058304855090129", description="partial update")

    assert err is None
    assert result.id == "72058304855090129"
    assert _sent_body(executor)["action"] is None


@pytest.mark.parametrize("method", ["update_isolation_rule", "update_isolation_rule_v2"])
def test_update_isolation_rule_action_is_uppercased(method):
    api, executor = _api()

    getattr(api, method)(rule_id="72058304855090129", action="isolate", zpn_isolation_profile_id="72058304855090131")

    body = _sent_body(executor)
    assert body["action"] == "ISOLATE"
    assert body["zpnIsolationProfileId"] == "72058304855090131"


def test_update_app_protection_rule_v2_sends_conditions():
    api, executor = _api()

    _, _, err = api.update_app_protection_rule_v2(
        rule_id="72058304855090129",
        name="rule-a",
        action="inspect",
        zpn_inspection_profile_id="72058304855090132",
        conditions=[("app", [APP_ID])],
    )

    assert err is None
    assert _sent_body(executor)["conditions"] == [{"operands": [{"objectType": "APP", "values": [APP_ID]}]}]


@pytest.mark.parametrize(
    "conditions",
    [
        [("app", [APP_ID])],
        [["app", [APP_ID]]],
        [["OR", ["app", [APP_ID]]]],
    ],
    ids=["tuple", "list", "list-with-operator"],
)
def test_create_conditions_v2_accepts_tuples_and_lists(conditions):
    api, _ = _api()

    assert api._create_conditions_v2(conditions) == [{"operands": [{"objectType": "APP", "values": [APP_ID]}]}]
