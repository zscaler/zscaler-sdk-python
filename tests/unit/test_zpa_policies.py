"""
Unit tests for ZPA Policy Set Controller rule updates.

Tests that a partial update which omits the optional ``action`` keyword
is still sent to the API instead of raising ``AttributeError``.
"""

from unittest.mock import Mock

import pytest

from zscaler.zpa.policies import PolicySetControllerAPI

CUSTOMER_ID = "72058304855090128"
POLICY_SET_ID = "72058304855090130"
RULE_ID = "72058304855090129"


def build_api():
    """Return a PolicySetControllerAPI and the request executor it was given."""
    policy_set = Mock()
    policy_set.get_body.return_value = {"id": POLICY_SET_ID}

    mock_executor = Mock()
    mock_executor.create_request.return_value = ({}, None)
    # First execute() resolves the policy set, the second performs the rule update.
    mock_executor.execute.side_effect = [(policy_set, None), (None, None)]

    return PolicySetControllerAPI(mock_executor, {"client": {"customerId": CUSTOMER_ID}}), mock_executor


class TestUpdateIsolationRuleWithoutAction:
    """Test update_isolation_rule and update_isolation_rule_v2 partial updates."""

    @pytest.mark.parametrize("method_name", ["update_isolation_rule", "update_isolation_rule_v2"])
    def test_update_without_action_sends_request(self, method_name):
        """Test omitting the optional action keyword still issues the update request."""
        # Setup
        api, mock_executor = build_api()

        # Test
        rule, _, error = getattr(api, method_name)(rule_id=RULE_ID, description="partial update")

        # Assertions
        assert error is None
        assert rule.id == RULE_ID

        payload = mock_executor.create_request.call_args.kwargs["body"]
        assert payload["action"] is None
        assert payload["description"] == "partial update"
