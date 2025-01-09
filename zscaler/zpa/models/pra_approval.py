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
from zscaler.zpa.models.application_segment_pra import ApplicationSegmentPRA

class PrivilegedRemoteAccessApproval(ZscalerObject):
    """
    A class representing the Privileged Remote Access Approval.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.id = config["id"]\
                if "id" in config else None
            self.start_time = config["startTime"]\
                if "startTime" in config else None
            self.end_time = config["endTime"]\
                if "endTime" in config else None
            self.modified_time = config["modifiedTime"]\
                if "modifiedTime" in config else None
            self.creation_time = config["creationTime"]\
                if "creationTime" in config else None
            self.status = config["status"]\
                if "status" in config else None
            self.email_ids = config["emailIds"]\
                if "emailIds" in config else []
                
            self.applications = [
                ApplicationSegmentPRA(app) for app in config.get("applications", [])
            ]

            # Handle working hours with defensive programming for every attribute
            working_hours = config["workingHours"] if "workingHours" in config else {}
            self.working_hours = {
                "startTimeCron": working_hours["startTimeCron"] if "startTimeCron" in working_hours else None,
                "endTimeCron": working_hours["endTimeCron"] if "endTimeCron" in working_hours else None,
                "startTime": working_hours["startTime"] if "startTime" in working_hours else None,
                "endTime": working_hours["endTime"] if "endTime" in working_hours else None,
                "timeZone": working_hours["timeZone"] if "timeZone" in working_hours else None,
                "days": ZscalerCollection.form_list(
                    working_hours["days"] if "days" in working_hours else [], str
                )
            }        
            
        else:
            self.id = None
            self.start_time = None
            self.end_time = None
            self.modified_time = None
            self.creation_time = None
            self.status = None
            self.email_ids = []
            self.applications = []
            self.working_hours = {}


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
            "applications": [app.request_format() for app in self.applications],
            "workingHours": {
                "startTimeCron": self.working_hours["startTimeCron"] if self.working_hours["startTimeCron"] else None,
                "endTimeCron": self.working_hours["endTimeCron"] if self.working_hours["endTimeCron"] else None,
                "startTime": self.working_hours["startTime"] if self.working_hours["startTime"] else None,
                "endTime": self.working_hours["endTime"] if self.working_hours["endTime"] else None,
                "days": self.working_hours["days"] if self.working_hours["days"] else [],
                "timeZone": self.working_hours["timeZone"] if self.working_hours["timeZone"] else None,
            }
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format