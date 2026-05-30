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

from typing import List, Optional
from zscaler.api_client import APIClient
from zscaler.request_executor import RequestExecutor
from zscaler.types import APIResult
from zscaler.utils import format_url
from zscaler.zia.models.email_profiles import EmailProfiles


class EmailProfilesAPI(APIClient):
    """
    A Client object for the Email profiles resource.
    """

    _zia_base_endpoint = "/zia/api/v1"

    def __init__(self, request_executor: "RequestExecutor") -> None:
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def list_email_profiles(self, query_params: Optional[dict] = None) -> APIResult[List[EmailProfiles]]:
        """
        Lists email profiles in your organization with pagination.
        A subset of email profiles can be returned that match a supported
        filter expression or query.

        Args:
            query_params {dict}: Map of query parameters for the request.
                ``[query_params.page]`` {int}: Specifies the page offset.

                ``[query_params.page_size]`` {int}: Page size for pagination.

                ``[query_params.search]`` {str}: Search string for filtering results.

        Returns:
            tuple: A tuple containing (list of Email Profiles instances, Response, error)

        Examples:
            List Email Profiles using default settings:

            >>> profile_list, _, error = client.zia.email_profiles.list_email_profiles(
                query_params={'search': updated_profile.name})
            >>> if error:
            ...     print(f"Error listing email profiles: {error}")
            ...     return
            ... print(f"Total email profiles found: {len(profile_list)}")
            ... for profile in profile_list:
            ...     print(profile.as_dict())

            Client-side filtering with JMESPath:

            The response object supports client-side filtering and
            projection via ``resp.search(expression)``.  See the
            `JMESPath documentation <https://jmespath.org/>`_ for
            expression syntax.

        """
        http_method = "get".upper()
        api_url = format_url(f"""
            {self._zia_base_endpoint}
            /emailRecipientProfile
        """)

        query_params = query_params or {}

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers, params=query_params)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)

        if error:
            return (None, response, error)

        try:
            result = []
            for item in response.get_results():
                result.append(EmailProfiles(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_email_profile(self, profile_id: int) -> APIResult[dict]:
        """
        Fetches a specific email profile by ID.

        Args:
            profile_id (int): The unique identifier for the email profile.

        Returns:
            tuple: A tuple containing (Email Profile instance, Response, error).

        Examples:
            Print a specific Email Profile

            >>> fetched_profile, _, error = client.zia.email_profiles.get_email_profile(
                '1254654')
            >>> if error:
            ...     print(f"Error fetching Email Profile by ID: {error}")
            ...     return
            ... print(f"Fetched Email Profile by ID: {fetched_profile.as_dict()}")
        """
        http_method = "get".upper()
        api_url = format_url(f"""
            {self._zia_base_endpoint}
            /emailRecipientProfile/{profile_id}
        """)

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, EmailProfiles)
        if error:
            return (None, response, error)

        try:
            result = EmailProfiles(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def add_email_profile(self, **kwargs) -> APIResult[dict]:
        """
        Creates a new ZIA Email Profile.

        Args:
            name (str): The name of the email profile.
            **kwargs: Optional keyword args.

        Keyword Args:
            description (str): Additional notes or information

        Returns:
            tuple: A tuple containing the newly added Email Profile, response, and error.

        Examples:
            Add a new Email Profile :

            >>> added_profile, _, error = client.zia.email_profiles.add_email_profile(
            ...     name=f"NewProfile_{random.randint(1000, 10000)}",
            ...     description=f"NewProfile_{random.randint(1000, 10000)}",
            ...     emails=['john.doe@example.com', 'mary.jane@example.com']
            ... )
            >>> if error:
            ...     print(f"Error adding email profile: {error}")
            ...     return
            ... print(f"Email Profile added successfully: {added_profile.as_dict()}")
        """
        http_method = "post".upper()
        api_url = format_url(f"""
            {self._zia_base_endpoint}
            /emailRecipientProfile
        """)

        body = kwargs

        request, error = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
            body=body,
        )

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, EmailProfiles)
        if error:
            return (None, response, error)

        try:
            result = EmailProfiles(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_email_profile(self, profile_id: int, **kwargs) -> APIResult[dict]:
        """
        Updates information for the specified ZIA Email Profile.

        Args:
            profile_id (int): The unique ID for the Email Profile.

        Returns:
            tuple: A tuple containing the updated Email Profile, response, and error.

        Examples:
            Update an existing Email Profile :

            >>> updated_profile, _, error = client.zia.email_profiles.update_email_profile(
                profile_id='1524566'
            ... name=f"UpdatedEmailProfile_{random.randint(1000, 10000)}",
            ... description=f"UpdatedEmailProfile_{random.randint(1000, 10000)}",
            ... )
            >>> if error:
            ...     print(f"Error updating Email Profile: {error}")
            ...     return
            ... print(f"Email Profile updated successfully: {updated_profile.as_dict()}")
        """
        http_method = "put".upper()
        api_url = format_url(f"""
            {self._zia_base_endpoint}
            /emailRecipientProfile/{profile_id}
        """)
        body = kwargs

        request, error = self._request_executor.create_request(http_method, api_url, body, {}, {})
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, EmailProfiles)
        if error:
            return (None, response, error)

        try:
            result = EmailProfiles(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def delete_email_profile(self, profile_id: int) -> APIResult[dict]:
        """
        Deletes the specified Email Profile.

        Args:
            profile_id (str): The unique identifier of the Email Profile.

        Returns:
            tuple: A tuple containing the response object and error (if any).

        Examples:
            Delete an Email Profile:

            >>> _, _, error = client.zia.email_profiles.delete_email_profile('73459')
            >>> if error:
            ...     print(f"Error deleting Email Profile: {error}")
            ...     return
            ... print(f"Email Profile with ID {'73459'} deleted successfully.")
        """
        http_method = "delete".upper()
        api_url = format_url(f"""
            {self._zia_base_endpoint}
            /emailRecipientProfile/{profile_id}
        """)

        params = {}

        request, error = self._request_executor.create_request(http_method, api_url, params=params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)
        return (None, response, None)
