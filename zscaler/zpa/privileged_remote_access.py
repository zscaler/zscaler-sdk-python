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


from typing import Any, Dict, List, Optional

from box import Box, BoxList
from requests import Response

from zscaler.utils import is_valid_ssh_key, snake_to_camel, validate_and_convert_times
from zscaler.zpa.client import ZPAClient


class PrivilegedRemoteAccessAPI:
    def __init__(self, client: ZPAClient):
        self.rest = client

    def list_portals(self, **kwargs) -> BoxList:
        """
        Returns a list of all privileged remote access portals.

        Keyword Args:
            **max_items (int):
                The maximum number of items to request before stopping iteration.
            **max_pages (int):
                The maximum number of pages to request before stopping iteration.
            **pagesize (int):
                Specifies the page size. The default size is 20, but the maximum size is 500.
            **search (str, optional):
                The search string used to match against features and fields.

        Returns:
            :obj:`BoxList`: A list of all configured privileged remote access portals.

        Examples:
            >>> for pra_portal in zpa.privileged_remote_access.list_portals():
            ...    pprint(pra_portal)

        """
        list, _ = self.rest.get_paginated_data(path="/praPortal", **kwargs, api_version="v1")
        return list

    def get_portal(self, portal_id: str) -> Box:
        """
        Returns information on the specified pra portal.

        Args:
            portal_id (str):
                The unique identifier for the pra portal.

        Returns:
            :obj:`Box`: The resource record for the pra portal.

        Examples:
            >>> pprint(zpa.privileged_remote_access.get_portal('99999'))

        """
        return self.rest.get(f"praPortal/{portal_id}")

    def add_portal(
        self,
        name: str,
        certificate_id: str,
        domain: str,
        enabled: bool = True,
        user_notification_enabled: bool = True,
        **kwargs,
    ) -> Box:
        """
        Add a privileged remote access portal.

        Args:
            name (str):
                The name of the privileged portal.
            enabled (bool):
                Whether or not the privileged portal is enabled. Default is True.
            certificate_id (bool):
                The unique identifier of the certificate.
            domain (str):
                The domain of the privileged portal.
            **kwargs:
                Optional keyword args.

        Keyword Args:
            description (str):
                The description of the privileged portal.
            user_notification (str):
                The notification message displayed in the banner of the privileged portallink, if enabled.
            user_notification_enabled (bool):
                Indicates if the Notification Banner is enabled (true) or disabled (false)

        Returns:
            :obj:`Box`: The resource record for the newly created portal.

        Examples:
            Create a pra portal with the minimum required parameters:

            >>> zpa.privileged_remote_access.add_portal(
            ...   name='PRA Portal Example',
            ...   certificate_id='123456789',
            ...   user_notification_enabled=True)
        """
        payload = {
            "name": name,
            "enabled": enabled,
            "domain": domain,
            "userNotificationEnabled": user_notification_enabled,
            "certificateId": certificate_id,
        }

        # Add optional parameters to payload
        for key, value in kwargs.items():
            payload[snake_to_camel(key)] = value

        response = self.rest.post("/praPortal", json=payload)
        if isinstance(response, Response):
            status_code = response.status_code
            if status_code > 299:
                return None
        return self.get_portal(response.get("id"))

    def update_portal(self, portal_id: str, **kwargs) -> Box:
        """
        Updates the specified pra portal.

        Args:
            portal_id (str):
                The unique identifier for the portal being updated.
            **kwargs:
                Optional keyword args.

        Keyword Args:
            name (str):
                The name of the privileged portal.
            description (str):
                The description of the privileged portal.
            enabled (bool):
                Whether or not the privileged portal is enabled. Default is True
            certificate_id (bool):
                Whether or not The unique identifier of the certificate.
            domain (str):
                The domain of the privileged portal.
            user_notification (str):
                The notification message displayed in the banner of the privileged portallink, if enabled.
            user_notification_enabled (bool):
                Indicates if the Notification Banner is enabled (true) or disabled (false)

        Returns:
            :obj:`Box`: The resource record for the updated portal.

        Examples:
            Update the name of a portal:

            >>> zpa.privileged_remote_access.update_portal(
            ...   '99999',
            ...   name='Updated PRA Portal')

            Update the pra portal:

            >>> zpa.privileged_remote_access.update_portal(
            ...    '99999',
            ...    name='Updated PRA Portal')

        """
        # Set payload to value of existing record
        payload = {snake_to_camel(k): v for k, v in self.get_portal(portal_id).items()}

        # Add optional parameters to payload
        for key, value in kwargs.items():
            payload[snake_to_camel(key)] = value

        resp = self.rest.put(f"praPortal/{portal_id}", json=payload).status_code

        if resp == 204:
            return self.get_portal(portal_id)

    def delete_portal(self, portal_id: str) -> int:
        """
        Delete the specified pra portal.

        Args:
            portal_id (str): The unique identifier for the portal to be deleted.

        Returns:
            :obj:`int`: The response code for the operation.

        Examples:
            >>> zpa.privileged_remote_access.delete_portal('99999')

        """
        return self.rest.delete(f"praPortal/{portal_id}").status_code

    def list_consoles(self, **kwargs) -> BoxList:
        """
        Returns a list of all privileged remote access consoles.

        Keyword Args:
            **max_items (int):
                The maximum number of items to request before stopping iteration.
            **max_pages (int):
                The maximum number of pages to request before stopping iteration.
            **pagesize (int):
                Specifies the page size. The default size is 20, but the maximum size is 500.
            **search (str, optional):
                The search string used to match against features and fields.

        Returns:
            :obj:`BoxList`: A list of all configured privileged remote access consoles.

        Examples:
            >>> for pra_console in zpa.privileged_remote_access.list_consoles():
            ...    pprint(pra_console)

        """
        list, _ = self.rest.get_paginated_data(path="/praConsole", **kwargs, api_version="v1")
        return list

    def get_console(self, console_id: str) -> Box:
        """
        Returns information on the specified pra console.

        Args:
            console_id (str):
                The unique identifier for the pra console.

        Returns:
            :obj:`Box`: The resource record for the pra console.

        Examples:
            >>> pprint(zpa.privileged_remote_access.get_console('99999'))

        """
        return self.rest.get(f"praConsole/{console_id}")

    def get_console_portal(self, portal_id: str) -> Box:
        """
        Returns information on the specified pra console of the privileged portal.

        Args:
            portal_id (str):
                The unique identifier of the privileged portal.

        Returns:
            :obj:`Box`: The resource record for the privileged portal.

        Examples:
            >>> pprint(zpa.privileged_remote_access.get_console_portal('99999'))

        """
        return self.rest.get(f"praConsole/praPortal/{portal_id}")

    def add_console(
        self,
        name: str,
        pra_application_id: str,
        pra_portal_ids: list,
        enabled: bool = True,
        **kwargs,
    ) -> Box:
        """
        Adds a new Privileged Remote Access (PRA) console.

        Args:
            name (str): The name of the PRA console.
            pra_application_id (str): The unique identifier of the associated PRA application.
            pra_portal_ids (list of str): A list of unique identifiers for the associated PRA portals.
            enabled (bool, optional): Indicates whether the console is enabled. Defaults to True.

        Keyword Args:
            description (str, optional): A description for the PRA console.

        Returns:
            Box: A Box object containing the details of the newly created console.

        Examples:
            >>> zpa.privileged_remote_access.add_console(
            ...     name='PRA Console Example',
            ...     pra_application_id='999999999',
            ...     pra_portal_ids=['999999999'],
            ...     description='PRA Console Description',
            ...     enabled=True
            ... )
        """
        payload = {
            "name": name,
            "enabled": enabled,
            "praApplication": {"id": pra_application_id},
            "praPortals": [{"id": portal_id} for portal_id in pra_portal_ids],
        }

        # Add optional parameters to payload
        for key, value in kwargs.items():
            payload[snake_to_camel(key)] = value

        response = self.rest.post("praConsole", json=payload)
        if isinstance(response, Response):
            # this is only true when the creation failed (status code is not 2xx)
            status_code = response.status_code
            # Handle error response
            raise Exception(f"API call failed with status {status_code}: {response.json()}")
        return response

    def update_console(
        self,
        console_id: str,
        pra_application_id: str = None,
        pra_portal_ids: list = None,
        **kwargs,
    ) -> Box:
        """
        Updates the specified PRA console. All the attributes are required by the API.

        Args:
            console_id (str): The unique identifier of the console being updated.

        Keyword Args:
            name (str): The new name of the PRA console.
            description (str): The new description of the PRA console.
            enabled (bool): Indicates whether the console should be enabled.
            pra_application_id (str): The unique identifier of the associated PRA application to be linked with the console.
            pra_portal_ids (list of str): List of unique IDs for the associated PRA portals to be linked with the console.

        Returns:
            Box: A Box object containing the details of the updated console.

        Examples:
            >>> zpa.privileged_remote_access.update_console(
            ...     console_id='99999',
            ...     name='Updated PRA Console',
            ...     description='Updated Description',
            ...     enabled=True,
            ...     pra_application_id='999999999',
            ...     pra_portal_ids=['999999999']
            ... )
        """
        # Fetch existing console details first if necessary
        existing_console = self.get_console(console_id)

        # Set payload to value of existing record if needed
        payload = {snake_to_camel(k): v for k, v in existing_console.items()}

        if pra_application_id:
            payload["praApplication"] = {"id": pra_application_id}
        if pra_portal_ids:
            payload["praPortals"] = [{"id": id} for id in pra_portal_ids]

        # Add/Update optional parameters in payload
        for key, value in kwargs.items():
            payload[snake_to_camel(key)] = value

        resp = self.rest.put(f"praConsole/{console_id}", json=payload).status_code
        if not isinstance(resp, Response):
            return self.get_console(console_id)

    def delete_console(self, console_id: str) -> int:
        """
        Delete the specified pra console.

        Args:
            console_id (str): The unique identifier for the console to be deleted.

        Returns:
            :obj:`int`: The response code for the operation.

        Examples:
            >>> zpa.privileged_remote_access.delete_console('99999')

        """
        response = self.rest.delete(f"/praConsole/{console_id}")
        if response.status_code != 204:
            raise Exception(f"Failed to delete console: {response.text}")
        return response.status_code

    def add_bulk_console(self, consoles: List[Dict[str, Any]]) -> Box:
        """
        Adds a list of Privileged Remote Access (PRA) consoles in bulk.

        Args:
            consoles (List[Dict[str, Any]]): A list of dictionaries where each dictionary
                contains details of a PRA console to be added. Required keys in each dictionary include
                'name', 'pra_application_id', and 'pra_portal_ids'. Optionally, 'enabled' and 'description'
                can also be included.

        Returns:
            Box: A Box object containing the details of the newly created consoles.

        Examples:
            >>> zpa.privileged_remote_access.add_bulk_console([
            ...     {
            ...         'name': 'PRA Console Example 1',
            ...         'pra_application_id': '999999999',
            ...         'pra_portal_ids': ['999999998'],
            ...         'description': 'PRA Console Description 1',
            ...         'enabled': True
            ...     },
            ...     {
            ...         'name': 'PRA Console Example 2',
            ...         'pra_application_id': '999999999',
            ...         'pra_portal_ids': ['999999997'],
            ...         'description': 'PRA Console Description 2',
            ...         'enabled': True
            ...     }
            ... ])
        """
        # Transform the input list of console dictionaries to the expected JSON payload format
        payload = [
            {
                "name": console.get("name"),
                "description": console.get("description", ""),
                "enabled": console.get("enabled", True),
                "praApplication": {"id": console.get("pra_application_id")},
                "praPortals": [{"id": id} for id in console.get("pra_portal_ids", [])],
            }
            for console in consoles
        ]

        response = self.rest.post("praConsole/bulk", json=payload)
        if isinstance(response, Response):
            status_code = response.status_code
            # Handle error response
            raise Exception(f"API call failed with status {status_code}: {response.json()}")
        return response

    def list_credentials(self, **kwargs) -> BoxList:
        """
        Returns a list of all privileged remote access credentials.

        Keyword Args:
            **max_items (int):
                The maximum number of items to request before stopping iteration.
            **max_pages (int):
                The maximum number of pages to request before stopping iteration.
            **pagesize (int):
                Specifies the page size. The default size is 20, but the maximum size is 500.
            **search (str, optional):
                The search string used to match against features and fields.

        Returns:
            :obj:`BoxList`: A list of all configured privileged remote access credentials.

        Examples:
            >>> for pra_credential in zpa.privileged_remote_access.list_credentials():
            ...    pprint(pra_credential)

        """
        list, _ = self.rest.get_paginated_data(path="/credential", **kwargs, api_version="v1")
        return list

    def get_credential(self, credential_id: str) -> Box:
        """
        Returns information on the specified pra credential.

        Args:
            credential_id (str):
                The unique identifier for the pra credential.

        Returns:
            :obj:`Box`: The resource record for the pra credential.

        Examples:
            >>> pprint(zpa.privileged_remote_access.get_credential('99999'))

        """
        return self.rest.get(f"credential/{credential_id}")
        # response = self.rest.get("/credential/%s" % (credential_id))
        # if isinstance(response, Response):
        #     status_code = response.status_code
        #     if status_code != 200:
        #         return None
        # return response

    def add_credential(
        self,
        name: str,
        credential_type: str,
        username: Optional[str] = None,
        password: Optional[str] = None,
        private_key: Optional[str] = None,
        **kwargs,
    ) -> Box:
        """
        Validates input based on credential_type and adds a new credential.
        """
        payload = {"name": name, "credentialType": credential_type}

        if credential_type == "USERNAME_PASSWORD":
            if not username or not password:
                raise ValueError("Username and password must be provided for USERNAME_PASSWORD type.")
            payload.update({"userName": username, "password": password})

        elif credential_type == "SSH_KEY":
            if not username or not private_key:
                raise ValueError("Username and private_key must be provided for SSH_KEY type.")
            if not is_valid_ssh_key(private_key):
                raise ValueError("Invalid SSH key format.")
            payload.update({"userName": username, "privateKey": private_key})

        elif credential_type == "PASSWORD":
            if not password:
                raise ValueError("Password must be provided for PASSWORD type.")
            payload["password"] = password

        else:
            raise ValueError(f"Unsupported credential_type: {credential_type}")

        # Add optional parameters to payload
        for key, value in kwargs.items():
            if key in ["description", "user_domain", "passphrase"]:
                payload[snake_to_camel(key)] = value

        response = self.rest.post("credential", json=payload)
        if isinstance(response, Response):
            # this is only true when the creation failed (status code is not 2xx)
            status_code = response.status_code
            # Handle error response
            raise Exception(f"API call failed with status {status_code}: {response.json()}")
        return response

    def update_credential(self, credential_id: str, **kwargs) -> Box:
        """
        Updates a specified credential based on provided keyword arguments.

        Args:
            credential_id (str): The unique identifier for the credential being updated.

        Keyword Args:
            All attributes of the credential that can be updated including but not limited to:
            - username (str): Username for 'USERNAME_PASSWORD' and 'SSH_KEY' types.
            - password (str): Password for 'USERNAME_PASSWORD' and 'PASSWORD' types.
            - private_key (str): SSH private key for 'SSH_KEY' type.
            - description (str): Description of the credential.
            - user_domain (str): Domain associated with the username.
            - passphrase (str): Passphrase for the SSH private key, applicable only for 'SSH_KEY'.

        Returns:
            Box: The resource record for the updated credential.

        Raises:
            Exception: If fetching the credential fails or the required parameters are missing based on the credential type.

        Examples:
            Update a USERNAME_PASSWORD credential:
            >>> zpa.privileged_remote_access.update_credential(
            ...     credential_id='2223',
            ...     username='jdoe',
            ...     name='John Doe',
            ...     credential_type='USERNAME_PASSWORD',
            ...     password='**********',
            ...     description='Updated credential description'
            ... )
        """
        # Fetch the existing credential to determine the credential type
        existing_credential = self.get_credential(credential_id)
        if not existing_credential:
            raise Exception(f"Failed to fetch credential {credential_id}")

        # Validate and enforce required fields based on the credential type
        credential_type = existing_credential.credential_type
        required_fields = ["username", "password"] if credential_type in ["USERNAME_PASSWORD", "SSH_KEY"] else ["password"]
        missing_fields = [field for field in required_fields if field not in kwargs]
        if missing_fields:
            raise ValueError(f"Missing required fields for '{credential_type}': {', '.join(missing_fields)}")

        # Prepare the payload with the existing details and updates from kwargs
        payload = {
            **existing_credential.to_dict(),
            **{snake_to_camel(key): value for key, value in kwargs.items()},
        }

        # Execute the update operation
        response = self.rest.put(f"credential/{credential_id}", json=payload)
        if not response.ok:
            raise Exception(f"Failed to update credential {credential_id}: {response.text}")

        # Fetch and return the updated credential details
        return self.get_credential(credential_id)

    def delete_credential(self, credential_id: str) -> int:
        """
        Delete the specified pra credential.

        Args:
            credential_id (str): The unique identifier for the credential to be deleted.

        Returns:
            :obj:`int`: The response code for the operation.

        Examples:
            >>> zpa.privileged_remote_access.delete_credential('99999')

        """
        return self.rest.delete(f"credential/{credential_id}").status_code

    def list_approval(self, **kwargs) -> BoxList:
        """
        Returns a list of all privileged remote access approvals.

        Keyword Args:
            max_items (int):
                The maximum number of items to request before stopping iteration.
            max_pages (int):
                The maximum number of pages to request before stopping iteration.
            pagesize (int):
                Specifies the page size. Default is 20, maximum is 500.
            search (str, optional):
                The search string used to match against features and fields.
            search_field (str, optional):
                The field to search against. Defaults to 'name'. Commonly used fields
                include 'name' and 'email_ids'.

        Returns:
            :obj:`BoxList`: A list of all configured privileged remote access approvals.

        Examples:
            Search by default field 'name':

            >>> for pra_approval in zpa.privileged_remote_access.list_approval(
            ...     search='Example_Name'):
            ...     pprint(pra_approval)

            Search by 'email_ids':

            >>> for approval in zpa.privileged_remote_access.list_approval(
            ...     search='jdoe@example.com', search_field='email_ids'):
            ...     pprint(approval)

            Specify maximum items and use an explicit search field:

            >>> approvals = zpa.privileged_remote_access.list_approval(
            ...     search='Example_Name', search_field='name', max_items=10)
            ... for approval in approvals:
            ...     pprint(approval)

        """
        list, _ = self.rest.get_paginated_data(path="/approval", **kwargs, api_version="v1")
        return list

    def get_approval(self, approval_id: str) -> Box:
        """
        Returns information on the specified pra approval.

        Args:
            approval_id (str):
                The unique identifier for the pra approval.

        Returns:
            :obj:`Box`: The resource record for the pra approval.

        Examples:
            >>> pprint(zpa.privileged_remote_access.get_approval('99999'))

        """
        return self.rest.get(f"approval/{approval_id}")

    def add_approval(
        self,
        email_ids: list,
        application_ids: list,
        start_time: str,
        end_time: str,
        status: str,
        working_hours: dict,
        **kwargs,
    ) -> Box:
        """
        Add a privileged remote access approval.

        Args:
            email_ids (list): The email addresses of the users that you are assigning the privileged approval to.
            application_ids (list of str): A list of unique identifiers for the associated application segment ids.
            start_time (str): The start timestamp in UNIX format for when the approval begins.
            end_time (str): The end timestamp in UNIX format for when the approval ends.
            status (str): The status of the privileged approval. Supported values are: INVALID, ACTIVE, FUTURE, EXPIRED.
            working_hours (dict): Dictionary containing details of working hours.

        Keyword Args:
            Any additional optional parameters that can be included in the payload.

        Returns:
            Box: The resource record for the newly created approval.

        Examples:
            Create a PRA approval with the minimum required parameters and working hours:

            >>> zpa.privileged_remote_access.add_approval(
            ...   email_ids=['jdoe@example.com'],
            ...   application_ids=['999999999'],
            ...   start_time='1712856502',
            ...   end_time='1714498102',
            ...   status='ACTIVE',
            ...   working_hours={
            ...       "start_time_cron": "0 0 16 ? * SUN,MON,TUE,WED,THU,FRI,SAT",
            ...       "end_time_cron": "0 0 0 ? * MON,TUE,WED,THU,FRI,SAT,SUN",
            ...       "start_time": "09:00",
            ...       "end_time": "17:00",
            ...       "days": ["SUN", "MON", "TUE", "WED", "THU", "FRI", "SAT"],
            ...       "time_zone": "America/Vancouver"
            ...   }
            ... )
        """
        start_epoch, end_epoch = validate_and_convert_times(start_time, end_time, working_hours["time_zone"])

        payload = {
            "emailIds": email_ids,
            "applications": [{"id": application_id} for application_id in application_ids],
            "startTime": start_epoch,
            "endTime": end_epoch,
            "status": status,
            "workingHours": {
                "startTimeCron": working_hours["start_time_cron"],
                "endTimeCron": working_hours["end_time_cron"],
                "startTime": working_hours["start_time"],
                "endTime": working_hours["end_time"],
                "days": working_hours["days"],
                "timeZone": working_hours["time_zone"],
            },
        }
        # Incorporate optional parameters
        for key, value in kwargs.items():
            payload[snake_to_camel(key)] = value

        response = self.rest.post("approval", json=payload)
        if isinstance(response, Response):
            # this is only true when the creation failed (status code is not 2xx)
            status_code = response.status_code
            # Handle error response
            raise Exception(f"API call failed with status {status_code}: {response.json()}")
        return response

    def update_approval(self, approval_id: str, **kwargs) -> Box:
        """
        Updates a specified approval based on provided keyword arguments.
        ...
        """
        # Fetch existing approval details to get the current state
        existing_approval = self.get_approval(approval_id)
        if not existing_approval:
            raise Exception(f"Failed to fetch approval {approval_id}")

        # Pre-process and validate start_time and end_time if provided
        if "start_time" in kwargs and "end_time" in kwargs:
            start_time = kwargs["start_time"]
            end_time = kwargs["end_time"]
            # Assuming working_hours contains the time zone
            time_zone = kwargs.get("working_hours", {}).get("time_zone", existing_approval.working_hours.time_zone)
            start_epoch, end_epoch = validate_and_convert_times(start_time, end_time, time_zone)
            kwargs["start_time"] = start_epoch
            kwargs["end_time"] = end_epoch

        # Construct payload dynamically based on existing details and updates from kwargs
        payload = {
            "emailIds": kwargs.get("email_ids", existing_approval.email_ids),
            "applications": [
                {"id": app_id}
                for app_id in kwargs.get(
                    "application_ids",
                    [app["id"] for app in existing_approval.applications],
                )
            ],
            "status": kwargs.get("status", existing_approval.status),
        }

        # Special handling for working_hours to preserve existing details if not fully specified in kwargs
        working_hours = kwargs.get("working_hours", {})
        existing_wh = existing_approval.working_hours
        payload["workingHours"] = {
            "startTimeCron": working_hours.get("start_time_cron", existing_wh.start_time_cron),
            "endTimeCron": working_hours.get("end_time_cron", existing_wh.end_time_cron),
            "startTime": working_hours.get("start_time", existing_wh.start_time),
            "endTime": working_hours.get("end_time", existing_wh.end_time),
            "days": working_hours.get("days", existing_wh.days),
            "timeZone": working_hours.get("time_zone", existing_wh.time_zone),
        }

        # Add any additional provided parameters to payload
        for key, value in kwargs.items():
            if key not in ["email_ids", "application_ids", "working_hours"]:
                payload[snake_to_camel(key)] = value

        # Execute the update operation
        response = self.rest.put(f"approval/{approval_id}", json=payload)
        if response.status_code == 204:
            return self.get_approval(approval_id)
        else:
            raise Exception(f"Failed to update approval {approval_id}: {response.text}")

    def delete_approval(self, approval_id: str) -> int:
        """
        Delete the specified pra approval.

        Args:
            approval_id (str): The unique identifier for the approval to be deleted.

        Returns:
            :obj:`int`: The response code for the operation.

        Examples:
            >>> zpa.privileged_remote_access.delete_approval('99999')

        """
        return self.rest.delete(f"approval/{approval_id}").status_code

    def expired_approval(self) -> int:
        """
        Deletes all expired privileged approvals.

        Returns:
            :obj:`int`: The response code for the operation.

        Examples:
            >>> zpa.privileged_remote_access.expired_approval('99999')

        """
        return self.rest.delete("approval/expired").status_code
