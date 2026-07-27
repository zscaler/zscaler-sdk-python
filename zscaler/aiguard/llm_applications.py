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

from zscaler.aiguard.models.llm_applications import LlmApplications
from zscaler.api_client import APIClient
from zscaler.request_executor import RequestExecutor
from zscaler.types import APIResult
from zscaler.utils import format_url


class LLMApplicationsAPI(APIClient):
    """
    A Client object for the AI Guard LLM Applications resource.
    """

    _aiguard_base_endpoint = "/aiguard/v1"

    def __init__(self, request_executor: "RequestExecutor") -> None:
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def list_applications(self, query_params: Optional[dict] = None) -> APIResult[List[LlmApplications]]:
        """
        Lists the LLM applications configured in your organization.

        Args:
            query_params {dict}: Map of query parameters for the request.

        Returns:
            tuple: A tuple containing (list of LlmApplications instances, Response, error)

        Examples:
            List LLM applications:

            >>> application_list, _, error = client.aiguard.llm_applications.list_applications()
            >>> if error:
            ...     print(f"Error listing LLM applications: {error}")
            ...     return
            ... print(f"Total LLM applications found: {len(application_list)}")
            ... for application in application_list:
            ...     print(application.as_dict())

            Client-side filtering with JMESPath:

            The response object supports client-side filtering and
            projection via ``resp.search(expression)``.  See the
            `JMESPath documentation <https://jmespath.org/>`_ for
            expression syntax.
        """
        http_method = "get".upper()
        api_url = format_url(f"""
            {self._aiguard_base_endpoint}
            /llm-applications
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
                result.append(LlmApplications(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_application(self, application_id: int) -> APIResult[LlmApplications]:
        """
        Fetches a specific LLM application by ID.

        Args:
            application_id (int): The unique identifier for the LLM application.

        Returns:
            tuple: A tuple containing (LlmApplications instance, Response, error).

        Examples:
            Print a specific LLM application:

            >>> fetched_application, _, error = client.aiguard.llm_applications.get_application(1013)
            >>> if error:
            ...     print(f"Error fetching LLM application by ID: {error}")
            ...     return
            ... print(f"Fetched LLM application by ID: {fetched_application.as_dict()}")
        """
        http_method = "get".upper()
        api_url = format_url(f"""
            {self._aiguard_base_endpoint}
            /llm-applications/{application_id}
        """)

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, LlmApplications)
        if error:
            return (None, response, error)

        try:
            result = LlmApplications(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_application_by_name(self, name: str) -> APIResult[LlmApplications]:
        """
        Fetches a specific LLM application by name.

        Args:
            name (str): The name of the LLM application.

        Returns:
            tuple: A tuple containing (LlmApplications instance, Response, error).

        Examples:
            Print a specific LLM application by name:

            >>> fetched_application, _, error = client.aiguard.llm_applications.get_application_by_name('Application01')
            >>> if error:
            ...     print(f"Error fetching LLM application by name: {error}")
            ...     return
            ... print(f"Fetched LLM application by name: {fetched_application.as_dict()}")
        """
        http_method = "get".upper()
        api_url = format_url(f"""
            {self._aiguard_base_endpoint}
            /llm-applications/name/{name}
        """)

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, LlmApplications)
        if error:
            return (None, response, error)

        try:
            result = LlmApplications(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    # NOTE: The referential-check endpoint is currently returning HTTP 404 for every
    # resource type, including via Postman with a known-good id. The method is
    # commented out until the API supports it; re-enable once the endpoint is live.
    # def referential_check(self, application_id: int) -> APIResult[dict]:
    #     """
    #     Performs a referential check for the specified LLM application, returning the resources that reference it.
    #
    #     Args:
    #         application_id (int): The unique identifier for the LLM application.
    #
    #     Returns:
    #         tuple: A tuple containing (the raw response value, Response, error).
    #
    #     Examples:
    #         >>> result, _, error = client.aiguard.llm_applications.referential_check(1013)
    #         >>> if error:
    #         ...     print(f"Error calling referential_check: {error}")
    #         ...     return
    #         ... print(f"Result: {result}")
    #     """
    #     http_method = "get".upper()
    #     api_url = format_url(f"""
    #         {self._aiguard_base_endpoint}
    #         /llm-applications/{application_id}/referential-check
    #     """)
    #
    #     body = {}
    #     headers = {}
    #
    #     request, error = self._request_executor.create_request(http_method, api_url, body, headers)
    #
    #     if error:
    #         return (None, None, error)
    #
    #     response, error = self._request_executor.execute(request)
    #     if error:
    #         return (None, response, error)
    #
    #     try:
    #         result = self.form_response_body(response.get_body())
    #     except Exception as error:
    #         return (None, response, error)
    #     return (result, response, None)

    def add_application(self, **kwargs) -> APIResult[LlmApplications]:
        """
        Creates a new LLM application.

        Args:
            name (str): The name of the LLM application.
            **kwargs: Optional keyword args.

        Keyword Args:
            owner_email (str): The owner email for this LLM application.
            application_settings (str): The application settings for this LLM application.

        Returns:
            tuple: A tuple containing the newly added LlmApplications instance, response, and error.

        Examples:
            Add a new LLM application:

            >>> added_application, _, error = client.aiguard.llm_applications.add_application(
            ...     name="App10",
            ...     ownerEmail="jdoe@acme.com",
            ...     applicationSettings={
            ...         "includeEventContents": True,
            ...         "encryptEventContents": False,
            ...     },
            ... )
            >>> if error:
            ...     print(f"Error adding LLM application: {error}")
            ...     return
            ... print(f"LLM application added successfully: {added_application.as_dict()}")

            Note:
                Setting ``encryptEventContents`` to ``True`` requires a customer-managed key
                (CMK) configured in the tenant settings; the API rejects the request
                otherwise.
        """
        http_method = "post".upper()
        api_url = format_url(f"""
            {self._aiguard_base_endpoint}
            /llm-applications
        """)

        body = kwargs

        request, error = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
            body=body,
        )

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, LlmApplications)
        if error:
            return (None, response, error)

        try:
            result = LlmApplications(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_application(self, application_id: int, **kwargs) -> APIResult[LlmApplications]:
        """
        Updates information for the specified LLM application.

        Args:
            application_id (int): The unique identifier for the LLM application.

        Keyword Args:
            name (str): The name of the LLM application.
            owner_email (str): The owner email for this LLM application.
            application_settings (str): The application settings for this LLM application.

        Returns:
            tuple: A tuple containing the updated LlmApplications instance, response, and error.

        Examples:
            Update an existing LLM application:

            >>> updated_application, _, error = client.aiguard.llm_applications.update_application(
            ...     application_id=1575,
            ...     name="App10_Updated",
            ...     ownerEmail="jdoe@acme.com",
            ...     applicationSettings={
            ...         "includeEventContents": True,
            ...         "encryptEventContents": False,
            ...     },
            ... )
            >>> if error:
            ...     print(f"Error updating LLM application: {error}")
            ...     return
            ... print(f"LLM application updated successfully: {updated_application.as_dict()}")
        """
        http_method = "put".upper()
        api_url = format_url(f"""
            {self._aiguard_base_endpoint}
            /llm-applications/{application_id}
        """)
        body = kwargs

        request, error = self._request_executor.create_request(http_method, api_url, body, {}, {})
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, LlmApplications)
        if error:
            return (None, response, error)

        try:
            result = LlmApplications(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def delete_application(self, application_id: int) -> APIResult[None]:
        """
        Deletes the specified LLM application.

        Args:
            application_id (int): The unique identifier for the LLM application.

        Returns:
            tuple: A tuple containing the response object and error (if any).

        Examples:
            Delete a LLM application:

            >>> _, _, error = client.aiguard.llm_applications.delete_application(1013)
            >>> if error:
            ...     print(f"Error deleting LLM application: {error}")
            ...     return
            ... print(f"Llm application deleted successfully.")
        """
        http_method = "delete".upper()
        api_url = format_url(f"""
            {self._aiguard_base_endpoint}
            /llm-applications/{application_id}
        """)

        params = {}

        request, error = self._request_executor.create_request(http_method, api_url, params=params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)
        return (None, response, None)
