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


class GeneratedTickets(ZscalerObject):
    """
    A class for GeneratedTickets objects.
    """

    def __init__(self, config=None):
        """
        Initialize the GeneratedTickets model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:

            if "cursor" in config:
                if isinstance(config["cursor"], common.Common):
                    self.cursor = config["cursor"]
                elif config["cursor"] is not None:
                    self.cursor = common.Common(config["cursor"])
                else:
                    self.cursor = None
            else:
                self.cursor = None

            self.tickets = ZscalerCollection.form_list(config["tickets"] if "tickets" in config else [], Tickets)

        else:
            self.cursor = None
            self.tickets = []

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {"cursor": self.cursor, "tickets": self.tickets}
        parent_req_format.update(current_obj_format)
        return parent_req_format


class Tickets(ZscalerObject):
    """
    A class for Tickets objects.
    """

    def __init__(self, config=None):
        """
        Initialize the Tickets model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.ticket_type = config["ticketType"] if "ticketType" in config else None
            self.ticketing_system_name = config["ticketingSystemName"] if "ticketingSystemName" in config else None
            self.project_id = config["projectId"] if "projectId" in config else None
            self.project_name = config["projectName"] if "projectName" in config else None

            if "ticketInfo" in config:
                if isinstance(config["ticketInfo"], TicketInfo):
                    self.ticket_info = config["ticketInfo"]
                elif config["ticketInfo"] is not None:
                    self.ticket_info = TicketInfo(config["ticketInfo"])
                else:
                    self.ticket_info = None
            else:
                self.ticket_info = None

        else:
            self.cursor = None
            self.ticketing_system_name = None
            self.project_id = None
            self.project_name = None
            self.ticket_info = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "ticketType": self.ticket_type,
            "ticketingSystemName": self.ticketing_system_name,
            "projectId": self.project_id,
            "projectName": self.project_name,
            "ticketInfo": self.ticket_info,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class TicketInfo(ZscalerObject):
    """
    A class for TicketInfo objects.
    """

    def __init__(self, config=None):
        """
        Initialize the TicketInfo model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.ticket_id = config["ticketId"] if "ticketId" in config else None
            self.ticket_url = config["ticketUrl"] if "ticketUrl" in config else None
            self.state = config["state"] if "state" in config else None

        else:
            self.ticket_id = None
            self.ticket_url = None
            self.state = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "ticketId": self.ticket_id,
            "ticketUrl": self.ticket_url,
            "state": self.state,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
