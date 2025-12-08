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
from zscaler.zpa.models.pra_credential import PrivilegedRemoteAccessCredential
from zscaler.utils import format_url, is_valid_ssh_key


class PRACredentialAPI(APIClient):
    """
    A Client object for the Privileged Remote Access Credential resource.
    """

    def __init__(self, request_executor, config):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor
        customer_id = config["client"].get("customerId")
        self._zpa_base_endpoint = f"/zpa/mgmtconfig/v1/admin/customers/{customer_id}"

    def list_credentials(self, query_params: Optional[dict] = None) -> List[PrivilegedRemoteAccessCredential]:
        """
        Returns a list of all privileged remote access credentials.

        Args:
            query_params (dict): Map of query parameters for the request.

        Returns:
            List[PrivilegedRemoteAccessCredential]: A list of credential instances.

        Raises:
            ZscalerAPIException: If the API request fails.

        Examples:
            >>> try:
            ...     credentials = client.zpa.pra_credential.list_credentials()
            ...     for cred in credentials:
            ...         print(cred.as_dict())
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
        """
        http_method = "GET"
        api_url = format_url(f"{self._zpa_base_endpoint}/credential")

        query_params = query_params or {}
        if microtenant_id := query_params.get("microtenant_id"):
            query_params["microtenantId"] = microtenant_id

        request = self._request_executor.create_request(http_method, api_url, params=query_params)
        response = self._request_executor.execute(request, PrivilegedRemoteAccessCredential)

        return [PrivilegedRemoteAccessCredential(self.form_response_body(item)) for item in response.get_results()]

    def get_credential(self, credential_id: str, query_params: Optional[dict] = None) -> PrivilegedRemoteAccessCredential:
        """
        Returns information on the specified credential.

        Args:
            credential_id (str): The unique identifier of the credential.
            query_params (dict, optional): Map of query parameters.

        Returns:
            PrivilegedRemoteAccessCredential: The credential object.

        Raises:
            ZscalerAPIException: If the API request fails.

        Examples:
            >>> try:
            ...     cred = client.zpa.pra_credential.get_credential('999999')
            ...     print(cred.as_dict())
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
        """
        http_method = "GET"
        api_url = format_url(f"{self._zpa_base_endpoint}/credential/{credential_id}")

        query_params = query_params or {}
        if microtenant_id := query_params.get("microtenant_id"):
            query_params["microtenantId"] = microtenant_id

        request = self._request_executor.create_request(http_method, api_url, params=query_params)
        response = self._request_executor.execute(request, PrivilegedRemoteAccessCredential)

        return PrivilegedRemoteAccessCredential(self.form_response_body(response.get_body()))

    def add_credential(self, **kwargs) -> PrivilegedRemoteAccessCredential:
        """
        Adds a new privileged remote access credential.

        Args:
            name (str): The name of the credential.
            credential_type (str): The type ('USERNAME_PASSWORD', 'SSH_KEY', 'PASSWORD').
            username (str, optional): The username.
            password (str, optional): The password.
            private_key (str, optional): The private key for SSH_KEY type.

        Returns:
            PrivilegedRemoteAccessCredential: The newly created credential.

        Raises:
            ZscalerAPIException: If the API request fails.
            ValueError: If required fields are missing for the credential type.

        Examples:
            >>> try:
            ...     cred = client.zpa.pra_credential.add_credential(
            ...         name="John Doe",
            ...         credential_type="PASSWORD",
            ...         password="secret"
            ...     )
            ...     print(cred.as_dict())
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
        """
        http_method = "POST"
        api_url = format_url(f"{self._zpa_base_endpoint}/credential")

        body = kwargs
        credential_type = body.get("credential_type")
        username = body.get("user_name")
        password = body.get("password")
        private_key = body.get("private_key")

        if credential_type == "USERNAME_PASSWORD":
            if not username or not password:
                raise ValueError("Username and password must be provided for USERNAME_PASSWORD type.")
            body.update({"user_name": username, "password": password})
        elif credential_type == "SSH_KEY":
            if not username or not private_key:
                raise ValueError("Username and private_key must be provided for SSH_KEY type.")
            if not is_valid_ssh_key(private_key):
                raise ValueError("Invalid SSH key format.")
            body.update({"user_name": username, "private_key": private_key})
        elif credential_type == "PASSWORD":
            if not password:
                raise ValueError("Password must be provided for PASSWORD type.")
            body["password"] = password
        else:
            raise ValueError(f"Unsupported credential_type: {credential_type}")

        microtenant_id = body.get("microtenant_id")
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        request = self._request_executor.create_request(http_method, api_url, body=body, params=params)
        response = self._request_executor.execute(request, PrivilegedRemoteAccessCredential)

        return PrivilegedRemoteAccessCredential(self.form_response_body(response.get_body()))

    def update_credential(self, credential_id: str, **kwargs) -> PrivilegedRemoteAccessCredential:
        """
        Updates a specified credential.

        Args:
            credential_id (str): The unique identifier for the credential.
            **kwargs: Fields to update.

        Returns:
            PrivilegedRemoteAccessCredential: The updated credential.

        Raises:
            ZscalerAPIException: If the API request fails.
            ValueError: If required fields are missing for the credential type.

        Examples:
            >>> try:
            ...     cred = client.zpa.pra_credential.update_credential(
            ...         '999999',
            ...         name="Updated Credential"
            ...     )
            ...     print(cred.as_dict())
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
        """
        http_method = "PUT"
        api_url = format_url(f"{self._zpa_base_endpoint}/credential/{credential_id}")

        body = dict(kwargs)
        credential_type = body.get("credential_type")
        username = body.get("user_name")
        password = body.get("password")
        private_key = body.get("private_key")

        if credential_type == "USERNAME_PASSWORD":
            if not username or not password:
                raise ValueError("Username and password must be provided for USERNAME_PASSWORD type.")
            body.update({"user_name": username, "password": password})
        elif credential_type == "SSH_KEY":
            if not username or not private_key:
                raise ValueError("Username and private_key must be provided for SSH_KEY type.")
            if not is_valid_ssh_key(private_key):
                raise ValueError("Invalid SSH key format.")
            body.update({"user_name": username, "private_key": private_key})
        elif credential_type == "PASSWORD":
            if not password:
                raise ValueError("Password must be provided for PASSWORD type.")
            body["password"] = password
        else:
            raise ValueError(f"Unsupported credential_type: {credential_type}")

        microtenant_id = body.get("microtenant_id")
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        request = self._request_executor.create_request(http_method, api_url, body, {}, params)
        response = self._request_executor.execute(request, PrivilegedRemoteAccessCredential)

        if response is None:
            return PrivilegedRemoteAccessCredential({"id": credential_id})

        return PrivilegedRemoteAccessCredential(self.form_response_body(response.get_body()))

    def delete_credential(self, credential_id: str, microtenant_id: str = None) -> None:
        """
        Deletes the specified credential.

        Args:
            credential_id (str): The unique identifier of the credential.
            microtenant_id (str, optional): The microtenant ID.

        Returns:
            None

        Raises:
            ZscalerAPIException: If the API request fails.

        Examples:
            >>> try:
            ...     client.zpa.pra_credential.delete_credential('999999')
            ...     print("Credential deleted successfully")
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
        """
        http_method = "DELETE"
        api_url = format_url(f"{self._zpa_base_endpoint}/credential/{credential_id}")

        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        request = self._request_executor.create_request(http_method, api_url, params=params)
        self._request_executor.execute(request)

    def credential_move(self, credential_id: str, query_params: Optional[dict] = None) -> None:
        """
        Moves credential between parent tenant and microtenants.

        Args:
            credential_id (str): The unique identifier of the credential.
            query_params (dict): Must include target_microtenant_id.

        Returns:
            None

        Raises:
            ZscalerAPIException: If the API request fails.
            ValueError: If target_microtenant_id is not provided.

        Examples:
            >>> try:
            ...     client.zpa.pra_credential.credential_move(
            ...         'cred_id',
            ...         query_params={"target_microtenant_id": "target_id"}
            ...     )
            ...     print("Credential moved successfully")
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
        """
        http_method = "POST"
        api_url = format_url(f"{self._zpa_base_endpoint}/credential/{credential_id}/move")

        query_params = query_params or {}

        target_microtenant_id = query_params.get("target_microtenant_id")
        if not target_microtenant_id:
            raise ValueError("target_microtenant_id must be provided in query_params.")

        if "microtenant_id" in query_params:
            query_params["microtenantId"] = query_params.pop("microtenant_id")

        request = self._request_executor.create_request(http_method, api_url, params=query_params)
        self._request_executor.execute(request)
