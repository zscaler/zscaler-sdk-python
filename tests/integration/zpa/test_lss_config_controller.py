# -*- coding: utf-8 -*-

# Copyright (c) 2023, Zscaler Inc.
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

import pytest

from tests.integration.zpa.conftest import MockZPAClient
from tests.test_utils import generate_random_string


@pytest.fixture
def fs():
    yield


class TestLSSConfigController:
    """
    Integration Tests for the LSS Config Controller
    """

    def test_lss_config_controller(self, fs):
        client = MockZPAClient(fs)
        errors = []

        # Initialize IDs for cleanup
        lss_config_id = None
        app_connector_group_id = None

        try:
            try:
                # Get IDP by name "BD_Okta_Users"
                idp = client.idp.get_idp_by_name("BD_Okta_Users")
                if not idp:
                    raise ValueError("IDP 'BD_Okta_Users' not found")
                idp_id = idp["id"]
            except Exception as exc:
                errors.append(f"Retrieving IdP ID failed: {exc}")

            # Search and get SCIM Group IDs
            scim_group_ids = []
            for group_name in ["A000", "B000"]:
                try:
                    groups = client.scim_groups.list_groups(idp_id, search=group_name, sort_order="ASC")
                    group = next((g for g in groups if g.name == group_name), None)
                    if group is None:
                        raise ValueError(f"SCIM Group '{group_name}' not found")
                    scim_group_ids.append((idp_id, group.id))
                except Exception as exc:
                    errors.append(f"Searching SCIM Group '{group_name}' failed: {exc}")

            # Create an App Connector Group
            try:
                app_connector_group_name = "tests-" + generate_random_string()
                app_connector_group_description = "tests-" + generate_random_string()
                created_app_connector_group = client.connectors.add_connector_group(
                    name=app_connector_group_name,
                    description=app_connector_group_description,
                    enabled=True,
                    latitude="37.33874",
                    longitude="-121.8852525",
                    location="San Jose, CA, USA",
                    upgrade_day="SUNDAY",
                    upgrade_time_in_secs="66600",
                    override_version_profile=True,
                    version_profile_name="Default",
                    version_profile_id="0",
                    dns_query_type="IPV4_IPV6",
                    pra_enabled=True,
                    tcp_quick_ack_app=True,
                    tcp_quick_ack_assistant=True,
                    tcp_quick_ack_read_assistant=True,
                )
                app_connector_group_id = created_app_connector_group["id"]
            except Exception as exc:
                errors.append(f"Creating App Connector Group failed: {exc}")

            # Create an LSS Config
            try:
                lss_config_name = "tests-" + generate_random_string()
                lss_config_description = "tests-" + generate_random_string()
                lss_config = client.lss.add_lss_config(
                    name=lss_config_name,
                    description=lss_config_description,
                    enabled=True,
                    use_tls=True,
                    source_log_type="user_activity",
                    source_log_format="json",
                    lss_host="192.168.100.1",
                    lss_port="5000",
                    audit_message='{"logType":"User Activity","tcpPort":"5000","appConnectorGroups":[{"name":"tests-obuedxxtkw","id":"216199618143358305"}],"domainOrIpAddress":"192.168.100.1","logStreamContent":"{\\"LogTimestamp\\": %j{LogTimestamp:time},\\"Customer\\": %j{Customer},\\"SessionID\\": %j{SessionID},\\"ConnectionID\\": %j{ConnectionID},\\"InternalReason\\": %j{InternalReason},\\"ConnectionStatus\\": %j{ConnectionStatus},\\"IPProtocol\\": %d{IPProtocol},\\"DoubleEncryption\\": %d{DoubleEncryption},\\"Username\\": %j{Username},\\"ServicePort\\": %d{ServicePort},\\"ClientPublicIP\\": %j{ClientPublicIP},\\"ClientPrivateIP\\": %j{ClientPrivateIP},\\"ClientLatitude\\": %f{ClientLatitude},\\"ClientLongitude\\": %f{ClientLongitude},\\"ClientCountryCode\\": %j{ClientCountryCode},\\"ClientZEN\\": %j{ClientZEN},\\"Policy\\": %j{Policy},\\"Connector\\": %j{Connector},\\"ConnectorZEN\\": %j{ConnectorZEN},\\"ConnectorIP\\": %j{ConnectorIP},\\"ConnectorPort\\": %d{ConnectorPort},\\"Host\\": %j{Host},\\"Application\\": %j{Application},\\"AppGroup\\": %j{AppGroup},\\"Server\\": %j{Server},\\"ServerIP\\": %j{ServerIP},\\"ServerPort\\": %d{ServerPort},\\"PolicyProcessingTime\\": %d{PolicyProcessingTime},\\"ServerSetupTime\\": %d{ServerSetupTime},\\"TimestampConnectionStart\\": %j{TimestampConnectionStart:iso8601},\\"TimestampConnectionEnd\\": %j{TimestampConnectionEnd:iso8601},\\"TimestampCATx\\": %j{TimestampCATx:iso8601},\\"TimestampCARx\\": %j{TimestampCARx:iso8601},\\"TimestampAppLearnStart\\": %j{TimestampAppLearnStart:iso8601},\\"TimestampZENFirstRxClient\\": %j{TimestampZENFirstRxClient:iso8601},\\"TimestampZENFirstTxClient\\": %j{TimestampZENFirstTxClient:iso8601},\\"TimestampZENLastRxClient\\": %j{TimestampZENLastRxClient:iso8601},\\"TimestampZENLastTxClient\\": %j{TimestampZENLastTxClient:iso8601},\\"TimestampConnectorZENSetupComplete\\": %j{TimestampConnectorZENSetupComplete:iso8601},\\"TimestampZENFirstRxConnector\\": %j{TimestampZENFirstRxConnector:iso8601},\\"TimestampZENFirstTxConnector\\": %j{TimestampZENFirstTxConnector:iso8601},\\"TimestampZENLastRxConnector\\": %j{TimestampZENLastRxConnector:iso8601},\\"TimestampZENLastTxConnector\\": %j{TimestampZENLastTxConnector:iso8601},\\"ZENTotalBytesRxClient\\": %d{ZENTotalBytesRxClient},\\"ZENBytesRxClient\\": %d{ZENBytesRxClient},\\"ZENTotalBytesTxClient\\": %d{ZENTotalBytesTxClient},\\"ZENBytesTxClient\\": %d{ZENBytesTxClient},\\"ZENTotalBytesRxConnector\\": %d{ZENTotalBytesRxConnector},\\"ZENBytesRxConnector\\": %d{ZENBytesRxConnector},\\"ZENTotalBytesTxConnector\\": %d{ZENTotalBytesTxConnector},\\"ZENBytesTxConnector\\": %d{ZENBytesTxConnector},\\"Idp\\": %j{Idp},\\"ClientToClient\\": %j{c2c},\\"ClientCity\\": %j{ClientCity},\\"MicroTenantID\\": %j{MicroTenantID},\\"AppMicroTenantID\\": %j{AppMicroTenantID},\\"PRAConnectionID\\": %j{PRAConnectionID},\\"PRAConsoleType\\": %j{PRAConsoleType},\\"PRAApprovalID\\": %d{PRAApprovalID},\\"PRACapabilityPolicyID\\": %d{PRACapabilityPolicyID},\\"PRACredentialPolicyID\\": %d{PRACredentialPolicyID},\\"PRACredentialUserName\\": %j{PRACredentialUserName},\\"PRACredentialLoginType\\": %j{PRACredentialLoginType},\\"PRAErrorStatus\\": %j{PRAErrorStatus},\\"PRAFileTransferList\\": %j{PRAFileTransferList},\\"PRARecordingStatus\\": %j{PRARecordingStatus},\\"PRASharedUsersList\\": %j{PRASharedUsersList},\\"PRASessionType\\": %j{PRASessionType},\\"PRASharedMode\\": %j{PRASharedMode}}\\\\n","name":"tests-magtastamw","description":null,"sessionStatuses":null,"enabled":true,"useTls":true,"policy":{"policyType":"Log Receiver Policy","name":"SIEM selection rule for tests-magtastamw","action":"LOG","status":"enabled"}}',
                    app_connector_group_ids=[app_connector_group_id],
                    policy_rules=[
                        ("idp", [idp_id]),
                        ("client_type", ["web_browser", "client_connector"]),
                        ("scim_group", scim_group_ids),
                    ],
                )
                lss_config_id = lss_config["id"]
            except Exception as exc:
                errors.append(f"Creating LSS Config failed: {exc}")

            try:
                # Test listing LSS Config
                all_lss_configs = client.lss.list_configs()
                if not any(lss["id"] == lss_config_id for lss in all_lss_configs):
                    raise AssertionError("LSS Config not found in list")
            except Exception as exc:
                errors.append(f"Listing LSS Config  failed: {exc}")

            # Test retrieving the specific LSS Config
            try:
                remote_lss = client.lss.get_config(lss_config_id=lss_config_id)
                if remote_lss is None:
                    raise ValueError("Failed to retrieve LSS Config.")
                assert remote_lss["id"] == lss_config_id, "Retrieved LSS Config ID does not match"
            except Exception as exc:
                errors.append(f"Retrieving LSS Config failed: {exc}")

            # Update the LSS Config, particularly changing 'use_tls' to False
            try:
                updated_description = "Updated " + generate_random_string()
                client.lss.update_lss_config(
                    lss_config_id, description=updated_description, use_tls=False  # Explicitly setting use_tls to False
                )

                # Fetch the updated config to verify changes
                updated_lss_config = client.lss.get_config(lss_config_id)
                if updated_lss_config["config"]["use_tls"] is not False:
                    raise AssertionError("Failed to update use_tls to False for LSS Config")

            except Exception as exc:
                errors.append(f"Updating LSS Config failed: {exc}")

        finally:
            # Cleanup resources
            if lss_config_id:
                try:
                    client.lss.delete_lss_config(lss_config_id=lss_config_id)
                except Exception as exc:
                    errors.append(f"Deleting LSS Config failed: {exc}")

            if app_connector_group_id:
                try:
                    client.connectors.delete_connector_group(group_id=app_connector_group_id)
                except Exception as exc:
                    errors.append(f"Deleting App Connector Group failed: {exc}")

        assert not errors, f"Errors occurred during the LSS Config lifecycle test: {errors}"
