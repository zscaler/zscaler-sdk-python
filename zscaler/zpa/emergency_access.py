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


from box import Box
from requests import Response

from zscaler.utils import snake_to_camel
from zscaler.zpa.client import ZPAClient


class EmergencyAccessAPI:
    def __init__(self, client: ZPAClient):
        self.rest = client

    def get_user(self, user_id: str) -> Box:
        """
        Returns information on the specified emergency access user.

        Args:
            portal_id (str):
                The unique identifier for the emergency access user.

        Returns:
            :obj:`Box`: The resource record for the emergency access user.

        Examples:
            >>> pprint(zpa.emergency_access.get_user('99999'))

        """
        return self.rest.get(f"emergencyAccess/user/{user_id}")

    def add_user(
        self,
        email_id: str,
        first_name: str,
        last_name: str,
        user_id: str,
        activate_now: bool = True,
        **kwargs,
    ) -> Box:
        """
        Add an emergency access user.

        Args:
            email_id (str): The email address of the emergency access user, as provided by the admin.
            first_name (str): The first name of the emergency access user.
            last_name (str): The last name of the emergency access user, as provided by the admin.
            user_id (str): The unique identifier of the emergency access user.
            activate_now (bool, optional): Indicates if the emergency access user is activated upon creation. Defaults to True.

            **kwargs: Optional keyword args for additional attributes.

        Returns:
            :obj:`Box`: The resource record for the newly created user or an error message.

        Examples:
            >>> zpa.emergency_access.add_user(
            ...   email_id='user1Access@acme.com',
            ...   first_name='User1',
            ...   last_name='Access',
            ...   user_id='user1',
            ...   activate_now=True,
            )
        """
        payload = {
            "emailId": email_id,
            "userId": user_id,
            "firstName": first_name,
            "lastName": last_name,
        }

        # Include any additional attributes passed via kwargs
        for key, value in kwargs.items():
            payload[snake_to_camel(key)] = value

        # Append 'activateNow=true' to the URL query parameters if activate_now is True
        query_params = {"activateNow": "true"} if activate_now else {}

        response = self.rest.post("emergencyAccess/user", params=query_params, json=payload)
        if isinstance(response, Response):
            # this is only true when the creation failed (status code is not 2xx)
            status_code = response.status_code
            # Handle error response
            raise Exception(f"API call failed with status {status_code}: {response.json()}")
        return response

    def update_user(self, user_id: str, **kwargs) -> Box:
        """
        Updates the specified emergency access user.

        Args:
            user_id (str): The unique identifier of the emergency access user.

        Keyword Args:
            email_id (str): The email address of the emergency access user, as provided by the admin.
            first_name (str): The first name of the emergency access user.
            last_name (str): The last name of the emergency access user, as provided by the admin.
            user_id (str): The unique identifier of the emergency access user.

        Returns:
            Box: A Box object containing the details of the emergency access user.

        Examples:
            >>> zpa.emergency_access.update_user(
            ...     user_id='99999',
            ...     first_name='User1',
            ...     last_name='Access')
        """
        # Set payload to value of existing record
        payload = {snake_to_camel(k): v for k, v in self.get_user(user_id).items()}

        # Add optional parameters to payload
        for key, value in kwargs.items():
            payload[snake_to_camel(key)] = value

        resp = self.rest.put(f"emergencyAccess/user/{user_id}", json=payload)
        if not isinstance(resp, Response):
            return self.get_user(user_id)

    def activate_user(self, user_id: str, send_email: bool = False) -> Box:
        """
        Activates the emergency access user.

        Args:
            user_id (str): The unique identifier of the emergency access user to be activated.

        Returns:

        Examples:
            >>> zpa.emergency_access.activate_user('99999', send_email=True)

        """
        query_params = {"sendEmail": "true"} if send_email else {}

        response = self.rest.put(f"emergencyAccess/user/{user_id}/activate", params=query_params)
        if response.status_code == 200:
            return self.get_user(user_id)
        else:
            raise Exception(f"API call failed with status {response.status_code}: {response.text}")

    def deactivate_user(self, user_id: str) -> Box:
        """
        Deactivates the emergency access user.

        Args:
            user_id (str): The unique identifier of the emergency access user to be deactivated.

        Returns:

        Examples:
            >>> zpa.emergency_access.deactivate_user('99999')

        """
        resp = self.rest.put(f"emergencyAccess/user/{user_id}/deactivate").status_code
        if not isinstance(resp, Response):
            return self.get_user(user_id)
