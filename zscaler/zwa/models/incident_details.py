"""
Copyright (c) 2023, Zscaler Inc.

Permission to use, copy, modify, and/or distribute this software for any
purpose with or without fee is hereby granted, provided that the above
copyright notice and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
"""

from zscaler.oneapi_object import ZscalerObject
from zscaler.oneapi_collection import ZscalerCollection
from zscaler.zwa.models import common as common


class IncidentDLPDetails(ZscalerObject):
    """
    A class for DLPDetails objects.
    """

    def __init__(self, config=None):
        """
        Initialize the DLPDetails model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.internal_id = config["internalId"] if "internalId" in config else None
            self.integration_type = config["integrationType"] if "integrationType" in config else None
            self.transaction_id = config["transactionId"] if "transactionId" in config else None
            self.source_type = config["sourceType"] if "sourceType" in config else None
            self.source_sub_type = config["sourceSubType"] if "sourceSubType" in config else None
            self.source_actions = ZscalerCollection.form_list(
                config["sourceActions"] if "sourceActions" in config else [], str
            )
            self.severity = config["severity"] if "severity" in config else None
            self.priority = config["priority"] if "priority" in config else None
            self.match_count = config["matchCount"] if "matchCount" in config else None
            self.created_at = config["createdAt"] if "createdAt" in config else None
            self.last_updated_at = config["lastUpdatedAt"] if "lastUpdatedAt" in config else None
            self.source_first_observed_at = config["sourceFirstObservedAt"] if "sourceFirstObservedAt" in config else None
            self.source_last_observed_at = config["sourceLastObservedAt"] if "sourceLastObservedAt" in config else None
            self.metadata_file_url = config["metadataFileUrl"] if "metadataFileUrl" in config else None
            self.status = config["status"] if "status" in config else None
            self.resolution = config["resolution"] if "resolution" in config else None
            self.assigned_admin = config["assignedAdmin"] if "assignedAdmin" in config else None

            self.closed_code = config["closedCode"] if "closedCode" in config else None

            self.incident_group_ids = ZscalerCollection.form_list(
                config["incidentGroupIds"] if "incidentGroupIds" in config else [], str
            )

            self.labels = ZscalerCollection.form_list(config["labels"] if "labels" in config else [], common.Labels)

            self.notes = ZscalerCollection.form_list(config["notes"] if "notes" in config else [], common.Notes)

            self.incident_groups = ZscalerCollection.form_list(
                config["incidentGroups"] if "incidentGroups" in config else [], common.IncidentGroups
            )

            self.dlp_incident_tickets = ZscalerCollection.form_list(
                config["dlpIncidentTickets"] if "dlpIncidentTickets" in config else [], common.DLPIncidentTickets
            )

            if "matchingPolicies" in config:
                if isinstance(config["matchingPolicies"], common.MatchingPolicies):
                    self.matching_policies = config["matchingPolicies"]
                elif config["matchingPolicies"] is not None:
                    self.matching_policies = common.MatchingPolicies(config["matchingPolicies"])
                else:
                    self.matching_policies = None
            else:
                self.matching_policies = None

            if "userInfo" in config:
                if isinstance(config["userInfo"], common.UserInfo):
                    self.user_info = config["userInfo"]
                elif config["userInfo"] is not None:
                    self.user_info = common.UserInfo(config["userInfo"])
                else:
                    self.user_info = None
            else:
                self.user_info = None

            if "applicationInfo" in config:
                if isinstance(config["applicationInfo"], common.ApplicationInfo):
                    self.application_info = config["applicationInfo"]
                elif config["applicationInfo"] is not None:
                    self.application_info = common.ApplicationInfo(config["applicationInfo"])
                else:
                    self.application_info = None
            else:
                self.application_info = None

            if "contentInfo" in config:
                if isinstance(config["contentInfo"], common.ContentInfo):
                    self.content_info = config["contentInfo"]
                elif config["contentInfo"] is not None:
                    self.content_info = common.ContentInfo(config["contentInfo"])
                else:
                    self.content_info = None
            else:
                self.content_info = None

            if "networkInfo" in config:
                if isinstance(config["networkInfo"], common.NetworkInfo):
                    self.network_info = config["networkInfo"]
                elif config["networkInfo"] is not None:
                    self.network_info = common.NetworkInfo(config["networkInfo"])
                else:
                    self.network_info = None
            else:
                self.network_info = None

            if "lastNotifiedUser" in config:
                if isinstance(config["lastNotifiedUser"], common.LastNotifiedUser):
                    self.last_notified_user = config["lastNotifiedUser"]
                elif config["lastNotifiedUser"] is not None:
                    self.last_notified_user = common.LastNotifiedUser(config["lastNotifiedUser"])
                else:
                    self.last_notified_user = None
            else:
                self.last_notified_user = None

        else:
            self.internal_id = None
            self.integration_type = None
            self.transaction_id = None
            self.source_type = None
            self.source_sub_type = None
            self.source_actions = ZscalerCollection.form_list([], str)
            self.severity = None
            self.priority = None
            self.matching_policies = None
            self.match_count = None
            self.created_at = None
            self.last_updated_at = None
            self.source_first_observed_at = None
            self.source_last_observed_at = None
            self.user_info = None
            self.application_info = None
            self.content_info = None
            self.network_info = None
            self.metadata_file_url = None
            self.status = None
            self.resolution = None
            self.assigned_admin = None
            self.last_notified_user = None
            self.notes = []
            self.closed_code = None
            self.incident_group_ids = ZscalerCollection.form_list([], str)
            self.incident_groups = []
            self.dlp_incident_tickets = []
            self.labels = []

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "internalId": self.internal_id,
            "integrationType": self.integration_type,
            "transactionId": self.transaction_id,
            "sourceType": self.source_type,
            "sourceSubType": self.source_sub_type,
            "sourceActions": self.source_actions,
            "severity": self.severity,
            "priority": self.priority,
            "matchingPolicies": self.matching_policies,
            "matchCount": self.match_count,
            "createdAt": self.created_at,
            "lastUpdatedAt": self.last_updated_at,
            "sourceFirstObservedAt": self.source_first_observed_at,
            "sourceLastObservedAt": self.source_last_observed_at,
            "userInfo": self.user_info,
            "applicationInfo": self.application_info,
            "contentInfo": self.content_info,
            "networkInfo": self.network_info,
            "metadataFileUrl": self.metadata_file_url,
            "status": self.status,
            "resolution": self.resolution,
            "assignedAdmin": self.assigned_admin,
            "lastNotifiedUser": self.last_notified_user,
            "notes": self.notes,
            "closedCode": self.closed_code,
            "incidentGroupIds": self.incident_group_ids,
            "incidentGroups": self.incident_groups,
            "dlpIncidentTickets": self.dlp_incident_tickets,
            "labels": self.labels,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
