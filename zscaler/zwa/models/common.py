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


class Common(ZscalerObject):
    """
    A class for Common objects.
    """

    def __init__(self, config=None):
        """
        Initialize the Common model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.cursor = config["cursor"] if "cursor" in config else None
        else:
            self.cursor = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "cursor": self.cursor,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class Pagination(ZscalerObject):
    """
    A class for Pagination objects.
    """

    def __init__(self, config=None):
        """
        Initialize the Pagination model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.total_pages = config["totalPages"] if "totalPages" in config else None
            self.current_page_number = config["currentPageNumber"] if "currentPageNumber" in config else None
            self.current_page_size = config["currentPageSize"] if "currentPageSize" in config else None
            self.page_id = config["pageId"] if "pageId" in config else None
            self.total_elements = config["totalElements"] if "totalElements" in config else None
        else:
            self.total_pages = None
            self.current_page_number = None
            self.current_page_size = None
            self.page_id = None
            self.total_elements = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "totalPages": self.total_pages,
            "currentPageNumber": self.current_page_number,
            "currentPageSize": self.current_page_size,
            "pageId": self.page_id,
            "totalElements": self.total_elements,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class MatchingPolicies(ZscalerObject):
    def __init__(self, config=None):
        super().__init__(config)

        if config:
            self.engines = ZscalerCollection.form_list(config["engines"] if "engines" in config else [], Engines)
            self.rules = ZscalerCollection.form_list(config["rules"] if "rules" in config else [], Rules)
            self.dictionaries = ZscalerCollection.form_list(
                config["dictionaries"] if "dictionaries" in config else [], Dictionaries
            )
        else:
            self.engines = []
            self.rules = []
            self.dictionaries = []

    def request_format(self):
        return {
            "engines": self.engines,
            "rules": self.rules,
            "dictionaries": self.dictionaries,
        }


class Engines(ZscalerObject):
    """
    A class for Engines objects.
    """

    def __init__(self, config=None):
        """
        Initialize the Engines model based on API response.

        Args:
            config (dict): A dictionary representing the Rule Labels configuration.
        """
        super().__init__(config)

        if config:
            self.name = config["name"] if "name" in config else None
            self.rule = config["rule"] if "rule" in config else None

        else:
            self.name = None
            self.rule = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "name": self.name,
            "rule": self.rule,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class Rules(ZscalerObject):
    """
    A class for Rules objects.
    """

    def __init__(self, config=None):
        """
        Initialize the Rules model based on API response.

        Args:
            config (dict): A dictionary representing the Rule Labels configuration.
        """
        super().__init__(config)

        if config:
            self.name = config["name"] if "name" in config else None

        else:
            self.name = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "name": self.name,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class Dictionaries(ZscalerObject):
    """
    A class for Dictionaries objects.
    """

    def __init__(self, config=None):
        """
        Initialize the Dictionaries model based on API response.

        Args:
            config (dict): A dictionary representing the Rule Labels configuration.
        """
        super().__init__(config)

        if config:
            self.name = config["name"] if "name" in config else None
            self.match_count = config["matchCount"] if "matchCount" in config else None
            self.name_match_count = config["nameMatchCount"] if "nameMatchCount" in config else None
        else:
            self.name = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "name": self.name,
            "matchCount": self.match_count,
            "nameMatchCount": self.name_match_count,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class UserInfo(ZscalerObject):
    """
    A class for UserInfo objects.
    """

    def __init__(self, config=None):
        """
        Initialize the UserInfo model based on API response.

        Args:
            config (dict): A dictionary representing the Rule Labels configuration.
        """
        super().__init__(config)

        if config:
            self.name = config["name"] if "name" in config else None
            self.email = config["email"] if "email" in config else None
            self.client_ip = config["clientIP"] if "clientIP" in config else None
            self.unique_identifier = config["uniqueIdentifier"] if "uniqueIdentifier" in config else None
            self.user_id = config["userId"] if "userId" in config else None
            self.department = config["department"] if "department" in config else None
            self.home_country = config["homeCountry"] if "homeCountry" in config else None

            if "managerInfo" in config:
                if isinstance(config["managerInfo"], ManagerInfo):
                    self.manager_info = config["managerInfo"]
                elif config["managerInfo"] is not None:
                    self.manager_info = ManagerInfo(config["managerInfo"])
                else:
                    self.manager_info = None
            else:
                self.manager_info = None

        else:
            self.name = None
            self.email = None
            self.client_ip = None
            self.unique_identifier = None
            self.user_id = None
            self.department = None
            self.home_country = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "name": self.name,
            "email": self.email,
            "clientIP": self.client_ip,
            "uniqueIdentifier": self.unique_identifier,
            "userId": self.user_id,
            "department": self.department,
            "homeCountry": self.home_country,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class ManagerInfo(ZscalerObject):
    """
    A class for ManagerInfo objects.
    """

    def __init__(self, config=None):
        """
        Initialize the ManagerInfo model based on API response.

        Args:
            config (dict): A dictionary representing the Rule Labels configuration.
        """
        super().__init__(config)

        if config:
            self.id = config["id"] if "id" in config else None
            self.name = config["name"] if "name" in config else None
            self.email = config["email"] if "email" in config else None
        else:
            self.id = None
            self.name = None
            self.email = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "name": self.name,
            "email": self.email,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class ApplicationInfo(ZscalerObject):
    """
    A class for ApplicationInfo objects.
    """

    def __init__(self, config=None):
        """
        Initialize the ApplicationInfo model based on API response.

        Args:
            config (dict): A dictionary representing the Rule Labels configuration.
        """
        super().__init__(config)

        if config:
            self.url = config["url"] if "url" in config else None
            self.category = config["category"] if "category" in config else None
            self.name = config["name"] if "hostnameOrApplication" in config else None
            self.hostname_or_application = config["name"] if "hostnameOrApplication" in config else None
            self.additional_info = config["additionalInfo"] if "additionalInfo" in config else None
        else:
            self.url = None
            self.category = None
            self.name = None
            self.hostname_or_application = None
            self.additional_info = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "url": self.url,
            "name": self.name,
            "category": self.category,
            "hostnameOrApplication": self.hostname_or_application,
            "additionalInfo": self.additional_info,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class ContentInfo(ZscalerObject):
    """
    A class for ContentInfo objects.
    """

    def __init__(self, config=None):
        """
        Initialize the ContentInfo model based on API response.

        Args:
            config (dict): A dictionary representing the Rule Labels configuration.
        """
        super().__init__(config)

        if config:
            self.file_name = config["fileName"] if "ufileNamerl" in config else None
            self.file_type = config["fileType"] if "fileType" in config else None
            self.additional_info = config["additionalInfo"] if "additionalInfo" in config else None
        else:
            self.file_name = None
            self.file_type = None
            self.additional_info = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "fileName": self.file_name,
            "fileType": self.file_type,
            "additionalInfo": self.additional_info,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class NetworkInfo(ZscalerObject):
    """
    A class for NetworkInfo objects.
    """

    def __init__(self, config=None):
        """
        Initialize the NetworkInfo model based on API response.

        Args:
            config (dict): A dictionary representing the Rule Labels configuration.
        """
        super().__init__(config)

        if config:
            self.source = config["source"] if "source" in config else None
            self.destination = config["destination"] if "destination" in config else None
        else:
            self.source = None
            self.destination = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "source": self.source,
            "destination": self.destination,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class AssignedAdmin(ZscalerObject):
    """
    A class for AssignedAdmin objects.
    """

    def __init__(self, config=None):
        """
        Initialize the AssignedAdmin model based on API response.

        Args:
            config (dict): A dictionary representing the Rule Labels configuration.
        """
        super().__init__(config)

        if config:
            self.email = config["email"] if "email" in config else None
        else:
            self.email = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "email": self.email,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class LastNotifiedUser(ZscalerObject):
    """
    A class for LastNotifiedUser objects.
    """

    def __init__(self, config=None):
        """
        Initialize the LastNotifiedUser model based on API response.

        Args:
            config (dict): A dictionary representing the Rule Labels configuration.
        """
        super().__init__(config)

        if config:
            self.role = config["role"] if "role" in config else None
            self.email = config["email"] if "email" in config else None

        else:
            self.role = None
            self.email = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "role": self.role,
            "email": self.email,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class Notes(ZscalerObject):
    """
    A class for Notes objects.
    """

    def __init__(self, config=None):
        """
        Initialize the Notes model based on API response.

        Args:
            config (dict): A dictionary representing the Rule Labels configuration.
        """
        super().__init__(config)

        if config:
            self.body = config["body"] if "body" in config else None
            self.created_at = config["createdAt"] if "createdAt" in config else None
            self.last_updated_at = config["lastUpdatedAt"] if "lastUpdatedAt" in config else None
            self.created_by = config["createdBy"] if "createdBy" in config else None
            self.last_updated_by = config["lastUpdatedBy"] if "lastUpdatedBy" in config else None
        else:
            self.body = None
            self.created_at = None
            self.last_updated_at = None
            self.created_by = None
            self.last_updated_by = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "body": self.body,
            "createdAt": self.created_at,
            "lastUpdatedAt": self.last_updated_at,
            "createdBy": self.created_by,
            "lastUpdatedBy": self.last_updated_by,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class IncidentGroups(ZscalerObject):
    """
    A class for IncidentGroups objects.
    """

    def __init__(self, config=None):
        """
        Initialize the IncidentGroups model based on API response.

        Args:
            config (dict): A dictionary representing the Rule Labels configuration.
        """
        super().__init__(config)

        if config:
            self.id = config["id"] if "id" in config else None
            self.name = config["name"] if "name" in config else None
            self.description = config["description"] if "description" in config else None
            self.status = config["status"] if "status" in config else None
            self.incident_group_type = config["incidentGroupType"] if "incidentGroupType" in config else None
            # self.is_dlp_incident_group_already_mapped = config["isDLPIncidentGroupAlreadyMapped"]\
            #     if "isDLPIncidentGroupAlreadyMapped" in config else False
            # self.is_dlp_admin_config_already_mapped = config["isDLPAdminConfigAlreadyMapped"]\
            #     if "isDLPAdminConfigAlreadyMapped" in config else False
        else:
            self.id = None
            self.name = None
            self.description = None
            self.status = None
            self.incident_group_type = None
            # self.is_dlp_incident_group_already_mapped = None
            # self.is_dlp_admin_config_already_mapped = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "status": self.status,
            "incidentGroupType": self.incident_group_type,
            # "isDLPIncidentGroupAlreadyMapped": self.is_dlp_incident_group_already_mapped,
            # "isDLPAdminConfigAlreadyMapped": self.is_dlp_admin_config_already_mapped,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class DLPIncidentTickets(ZscalerObject):
    """
    A class for DLPIncidentTickets objects.
    """

    def __init__(self, config=None):
        """
        Initialize the DLPIncidentTickets model based on API response.

        Args:
            config (dict): A dictionary representing the Rule Labels configuration.
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
            self.ticket_type = None
            self.ticketing_system_name = None
            self.project_id = None
            self.project_name = None

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
            config (dict): A dictionary representing the Rule Labels configuration.
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


class Labels(ZscalerObject):
    """
    A class for Labels objects.
    """

    def __init__(self, config=None):
        """
        Initialize the Labels model based on API response.

        Args:
            config (dict): A dictionary representing the Labels configuration.
        """
        super().__init__(config)

        if config:
            self.key = config["key"] if "key" in config else None
            self.value = config["value"] if "value" in config else None

        else:
            self.key = None
            self.value = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "key": self.key,
            "value": self.value,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
