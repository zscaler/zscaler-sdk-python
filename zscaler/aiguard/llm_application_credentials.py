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

from zscaler.aiguard.models.llm_application_credentials import LlmApplicationCredentials
from zscaler.api_client import APIClient
from zscaler.request_executor import RequestExecutor
from zscaler.types import APIResult
from zscaler.utils import format_url


class LLMApplicationCredentialsAPI(APIClient):
    """
    A Client object for the AI Guard LLM Application Credentials resource.
    """

    _aiguard_base_endpoint = "/aiguard/v1"

    def __init__(self, request_executor: "RequestExecutor") -> None:
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def list_credentials(self, query_params: Optional[dict] = None) -> APIResult[List[LlmApplicationCredentials]]:
        """
        Lists the LLM application credentials configured in your organization.

        Args:
            query_params {dict}: Map of query parameters for the request.

        Returns:
            tuple: A tuple containing (list of LlmApplicationCredentials instances, Response, error)

        Examples:
            List LLM application credentials:

            >>> credential_list, _, error = client.aiguard.llm_application_credentials.list_credentials()
            >>> if error:
            ...     print(f"Error listing LLM application credentials: {error}")
            ...     return
            ... print(f"Total LLM application credentials found: {len(credential_list)}")
            ... for credential in credential_list:
            ...     print(credential.as_dict())

            Client-side filtering with JMESPath:

            The response object supports client-side filtering and
            projection via ``resp.search(expression)``.  See the
            `JMESPath documentation <https://jmespath.org/>`_ for
            expression syntax.
        """
        http_method = "get".upper()
        api_url = format_url(f"""
            {self._aiguard_base_endpoint}
            /llm-application-credentials
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
                result.append(LlmApplicationCredentials(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_credential(self, credential_id: int) -> APIResult[LlmApplicationCredentials]:
        """
        Fetches a specific LLM application credential by ID.

        Args:
            credential_id (int): The unique identifier for the LLM application credential.

        Returns:
            tuple: A tuple containing (LlmApplicationCredentials instance, Response, error).

        Examples:
            Print a specific LLM application credential:

            >>> fetched_credential, _, error = client.aiguard.llm_application_credentials.get_credential(1013)
            >>> if error:
            ...     print(f"Error fetching LLM application credential by ID: {error}")
            ...     return
            ... print(f"Fetched LLM application credential by ID: {fetched_credential.as_dict()}")
        """
        http_method = "get".upper()
        api_url = format_url(f"""
            {self._aiguard_base_endpoint}
            /llm-application-credentials/{credential_id}
        """)

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, LlmApplicationCredentials)
        if error:
            return (None, response, error)

        try:
            result = LlmApplicationCredentials(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_credential_by_name(self, name: str) -> APIResult[LlmApplicationCredentials]:
        """
        Fetches a specific LLM application credential by name.

        Args:
            name (str): The name of the LLM application credential.

        Returns:
            tuple: A tuple containing (LlmApplicationCredentials instance, Response, error).

        Examples:
            Print a specific LLM application credential by name:

            >>> fetched_credential, _, error = client.aiguard.llm_application_credentials.get_credential_by_name('Credential01')
            >>> if error:
            ...     print(f"Error fetching LLM application credential by name: {error}")
            ...     return
            ... print(f"Fetched LLM application credential by name: {fetched_credential.as_dict()}")
        """
        http_method = "get".upper()
        api_url = format_url(f"""
            {self._aiguard_base_endpoint}
            /llm-application-credentials/name/{name}
        """)

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, LlmApplicationCredentials)
        if error:
            return (None, response, error)

        try:
            result = LlmApplicationCredentials(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    # NOTE: The referential-check endpoint is currently returning HTTP 404 for every
    # resource type, including via Postman with a known-good id. The method is
    # commented out until the API supports it; re-enable once the endpoint is live.
    # def referential_check(self, credential_id: int) -> APIResult[dict]:
    #     """
    #     Performs a referential check for the specified LLM application credential, returning the resources that reference it.
    #
    #     Args:
    #         credential_id (int): The unique identifier for the LLM application credential.
    #
    #     Returns:
    #         tuple: A tuple containing (the raw response value, Response, error).
    #
    #     Examples:
    #         >>> result, _, error = client.aiguard.llm_application_credentials.referential_check(1013)
    #         >>> if error:
    #         ...     print(f"Error calling referential_check: {error}")
    #         ...     return
    #         ... print(f"Result: {result}")
    #     """
    #     http_method = "get".upper()
    #     api_url = format_url(f"""
    #         {self._aiguard_base_endpoint}
    #         /llm-application-credentials/{credential_id}/referential-check
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

    def add_credential(self, **kwargs) -> APIResult[LlmApplicationCredentials]:
        """
        Creates a new LLM application credential.

        Args:
            name (str): The name of the LLM application credential.
            **kwargs: Optional keyword args.

        Keyword Args:
            application_id (str): The application id for this LLM application credential.
            provider_id (str): The provider id for this LLM application credential.
            provider_credentials_id (str): The provider credentials id for this LLM application credential.
            mode (str): The mode for this LLM application credential.

        Returns:
            tuple: A tuple containing the newly added LlmApplicationCredentials instance, response, and error.

        Examples:
            Add a new LLM application credential. ``applicationId``, ``providerId`` and
            ``providerCredentialsId`` must all reference existing resources:

            >>> application, _, error = client.aiguard.llm_applications.get_application_by_name("App01")
            >>> provider, _, error = client.aiguard.llm_providers.get_provider_by_name("Default Anthropic Provider")
            >>> added_credential, _, error = client.aiguard.llm_application_credentials.add_credential(
            ...     applicationId=application.id,
            ...     providerId=provider.id,
            ...     providerCredentialsId=739,
            ...     name="IDB01",
            ...     mode="PROXY",
            ... )
            >>> if error:
            ...     print(f"Error adding LLM application credential: {error}")
            ...     return
            ... print(f"LLM application credential added successfully: {added_credential.as_dict()}")

            Note:
                The create response returns a generated ``key`` -- treat it as a secret and
                do not log it.
        """
        http_method = "post".upper()
        api_url = format_url(f"""
            {self._aiguard_base_endpoint}
            /llm-application-credentials
        """)

        body = kwargs

        request, error = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
            body=body,
        )

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, LlmApplicationCredentials)
        if error:
            return (None, response, error)

        try:
            result = LlmApplicationCredentials(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def regenerate_credential(self, credential_id: int) -> APIResult[LlmApplicationCredentials]:
        """
        Regenerates the key material for the specified LLM application credential.

        Args:
            credential_id (int): The unique identifier for the LLM application credential.

        Returns:
            tuple: A tuple containing the resulting LlmApplicationCredentials instance, response, and error.
            The raw response body is available via ``response.get_body()``.

        Examples:
            >>> result, resp, error = client.aiguard.llm_application_credentials.regenerate_credential(1013)
            >>> if error:
            ...     print(f"Error calling regenerate_credential: {error}")
            ...     return
            ... print(f"Action completed successfully: {result.as_dict()}")
        """
        http_method = "post".upper()
        api_url = format_url(f"""
            {self._aiguard_base_endpoint}
            /llm-application-credentials/{credential_id}/regenerate
        """)

        body = {}

        request, error = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
            body=body,
        )

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, LlmApplicationCredentials)
        if error:
            return (None, response, error)

        try:
            result = LlmApplicationCredentials(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_credential(self, credential_id: int, **kwargs) -> APIResult[LlmApplicationCredentials]:
        """
        Updates information for the specified LLM application credential.

        Args:
            credential_id (int): The unique identifier for the LLM application credential.

        Keyword Args:
            name (str): The name of the LLM application credential.
            application_id (str): The application id for this LLM application credential.
            provider_id (str): The provider id for this LLM application credential.
            provider_credentials_id (str): The provider credentials id for this LLM application credential.
            mode (str): The mode for this LLM application credential.

        Returns:
            tuple: A tuple containing the updated LlmApplicationCredentials instance, response, and error.

        Examples:
            Update an existing LLM application credential:

            >>> updated_credential, _, error = client.aiguard.llm_application_credentials.update_credential(
            ...     credential_id=1075,
            ...     applicationId=647,
            ...     providerId=6099,
            ...     providerCredentialsId=739,
            ...     name="IDB01_Updated",
            ...     mode="PROXY",
            ... )
            >>> if error:
            ...     print(f"Error updating LLM application credential: {error}")
            ...     return
            ... print(f"LLM application credential updated successfully: {updated_credential.as_dict()}")
        """
        http_method = "put".upper()
        api_url = format_url(f"""
            {self._aiguard_base_endpoint}
            /llm-application-credentials/{credential_id}
        """)
        body = kwargs

        request, error = self._request_executor.create_request(http_method, api_url, body, {}, {})
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, LlmApplicationCredentials)
        if error:
            return (None, response, error)

        try:
            result = LlmApplicationCredentials(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def delete_credential(self, credential_id: int) -> APIResult[None]:
        """
        Deletes the specified LLM application credential.

        Args:
            credential_id (int): The unique identifier for the LLM application credential.

        Returns:
            tuple: A tuple containing the response object and error (if any).

        Examples:
            Delete a LLM application credential:

            >>> _, _, error = client.aiguard.llm_application_credentials.delete_credential(1013)
            >>> if error:
            ...     print(f"Error deleting LLM application credential: {error}")
            ...     return
            ... print(f"Llm application credential deleted successfully.")
        """
        http_method = "delete".upper()
        api_url = format_url(f"""
            {self._aiguard_base_endpoint}
            /llm-application-credentials/{credential_id}
        """)

        params = {}

        request, error = self._request_executor.create_request(http_method, api_url, params=params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)
        return (None, response, None)
