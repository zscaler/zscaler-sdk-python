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
from zscaler.zpa.models import application_segment as application_segment


class PrivilegedRemoteAccessApproval(ZscalerObject):
    """
    A class representing the Privileged Remote Access Approval.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.id = config["id"] if "id" in config else None
            self.start_time = config["startTime"] if "startTime" in config else None
            self.end_time = config["endTime"] if "endTime" in config else None
            self.modified_time = config["modifiedTime"] if "modifiedTime" in config else None
            self.creation_time = config["creationTime"] if "creationTime" in config else None
            self.status = config["status"] if "status" in config else None

            self.email_ids = ZscalerCollection.form_list(config["emailIds"] if "emailIds" in config else [], str)

            self.applications = ZscalerCollection.form_list(
                config["applications"] if "applications" in config else [], application_segment.ApplicationSegment
            )

            if "workingHours" in config:
                if isinstance(config["workingHours"], WorkingHours):
                    self.working_hours = config["workingHours"]
                elif config["workingHours"] is not None:
                    self.working_hours = WorkingHours(config["workingHours"])
                else:
                    self.working_hours = None
            else:
                self.working_hours = None

        else:
            self.id = None
            self.start_time = None
            self.end_time = None
            self.modified_time = None
            self.creation_time = None
            self.status = None
            self.email_ids = []
            self.applications = []
            self.working_hours = None

    def request_format(self):
        """
        Prepare the object in a format suitable for sending as a request payload.

        Returns:
            dict: A dictionary representing the PRA approval for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "startTime": self.start_time,
            "endTime": self.end_time,
            "status": self.status,
            "emailIds": self.email_ids,
            "applications": self.applications,
            "workingHours": self.working_hours,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class WorkingHours(ZscalerObject):
    """
    A class for WorkingHours objects.
    """

    def __init__(self, config=None):
        """
        Initialize the WorkingHours model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.end_time = config["endTime"] if "endTime" in config else None

            self.end_time_cron = config["endTimeCron"] if "endTimeCron" in config else None

            self.start_time = config["startTime"] if "startTime" in config else None

            self.start_time_cron = config["startTimeCron"] if "startTimeCron" in config else None

            self.time_zone = config["timeZone"] if "timeZone" in config else None

            self.days = ZscalerCollection.form_list(config["days"] if "days" in config else [], str)

        else:
            self.end_time = None
            self.end_time_cron = None
            self.start_time = None
            self.start_time_cron = None
            self.time_zone = None
            self.days = []

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "endTime": self.end_time,
            "endTimeCron": self.end_time_cron,
            "startTime": self.start_time,
            "startTimeCron": self.start_time_cron,
            "timeZone": self.time_zone,
            "days": self.days,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
