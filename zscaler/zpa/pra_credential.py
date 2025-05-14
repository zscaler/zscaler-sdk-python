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

    def list_credentials(self, query_params=None) -> tuple:
        """
        Returns a list of all privileged remote access credentials.

        Args:
            query_params {dict}: Map of query parameters for the request.
                ``[query_params.page]`` {str}: Specifies the page number.
                ``[query_params.page_size]`` {int}: Page size for pagination.
                ``[query_params.search]`` {str}: Search string for filtering results.
                ``[query_params.microtenant_id]`` {str}: ID of the microtenant, if applicable.

        Returns:
            tuple: A tuple containing (list of PrivilegedRemoteAccessCredential instances, Response, error)

        Examples:
            >>> credential_list, _, err = client.zpa.pra_credential.list_credentials(
            ... query_params={'search': 'pra_console01', 'page': '1', 'page_size': '100'})
            ... if err:
            ...     print(f"Error listing pra credentials: {err}")
            ...     return
            ... print(f"Total pra credentials found: {len(credential_list)}")
            ... for pra in credential_list:
            ...     print(pra.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /credential
        """
        )

        query_params = query_params or {}
        microtenant_id = query_params.get("microtenant_id", None)
        if microtenant_id:
            query_params["microtenantId"] = microtenant_id

        request, error = self._request_executor.create_request(http_method, api_url, params=query_params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, PrivilegedRemoteAccessCredential)
        if error:
            return (None, response, error)

        try:
            result = []
            for item in response.get_results():
                result.append(PrivilegedRemoteAccessCredential(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_credential(self, credential_id: str, query_params=None) -> tuple:
        """
        Returns information on the specified privileged remote access credential.

        Args:
            credential_id (str): The unique identifier of the credential.
            query_params (dict, optional): Map of query parameters for the request.
                ``[query_params.microtenant_id]`` {str}: The microtenant ID, if applicable.

        Returns:
            :obj:`Tuple`: PrivilegedRemoteAccessCredential: The resource record for the credential.

        Examples:
            >>> fetched_credential, _, err = client.zpa.pra_credential.get_credential('999999')
            ... if err:
            ...     print(f"Error fetching credential by ID: {err}")
            ...     return
            ... print(f"Fetched credential by ID: {fetched_credential.as_dict()}")
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""{
            self._zpa_base_endpoint}
            /credential/{credential_id}
        """
        )

        query_params = query_params or {}
        microtenant_id = query_params.get("microtenant_id", None)
        if microtenant_id:
            query_params["microtenantId"] = microtenant_id

        request, error = self._request_executor.create_request(http_method, api_url, params=query_params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, PrivilegedRemoteAccessCredential)
        if error:
            return (None, response, error)

        try:
            result = PrivilegedRemoteAccessCredential(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def add_credential(self, **kwargs) -> tuple:
        """
        Adds a new privileged remote access credential.

        Args:
            name (str): The name of the credential.
            credential_type (str): The type of credential ('USERNAME_PASSWORD', 'SSH_KEY', 'PASSWORD').
            username (str, optional): The username for 'USERNAME_PASSWORD' or 'SSH_KEY' types.
            password (str, optional): The password for 'USERNAME_PASSWORD' or 'PASSWORD' types.
            private_key (str, optional): The private key for 'SSH_KEY' type.

        Returns:
            :obj:`Tuple`: PrivilegedRemoteAccessCredential: The newly created credential resource.

        Examples:
            >>> added_credential, _, err = client.zpa.pra_credential.update_credential(
            ...     credential_id='999999',
            ...     name="John Doe",
            ...     description="Created PRA Credential",
            ...     credential_type="PASSWORD",
            ...     user_domain="acme.com",
            ...     password="",
            ... )
            ... if err:
            ...     print(f"Error adding credential: {err}")
            ...     return
            ... print(f"credential added successfully: {added_credential.as_dict()}")
        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /credential
        """
        )

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

        microtenant_id = body.get("microtenant_id", None)
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        request, error = self._request_executor.create_request(http_method, api_url, body=body, params=params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, PrivilegedRemoteAccessCredential)
        if error:
            return (None, response, error)

        try:
            result = PrivilegedRemoteAccessCredential(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_credential(self, credential_id: str, **kwargs) -> tuple:
        """
        Updates a specified credential based on provided keyword arguments.

        Args:
            credential_id (str): The unique identifier for the credential being updated.

        Returns:
            :obj:`Tuple`: PrivilegedRemoteAccessCredential: The updated credential resource.

        Examples:
            >>> updated_console, _, err = client.zpa.pra_credential.update_credential(
            ...     credential_id='999999',
            ...     name="John Doe",
            ...     description="Created PRA Credential",
            ...     credential_type="PASSWORD",
            ...     user_domain="acme.com",
            ...     password="",
            ... )
            ... if err:
            ...     print(f"Error updating credential: {err}")
            ...     return
            ... print(f"credential updated successfully: {updated_console.as_dict()}")
        """
        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /credential/{credential_id}
        """
        )

        body = {}

        body.update(kwargs)

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

        microtenant_id = body.get("microtenant_id", None)
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        request, error = self._request_executor.create_request(http_method, api_url, body, {}, params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, PrivilegedRemoteAccessCredential)
        if error:
            return (None, response, error)

        if response is None:
            return (PrivilegedRemoteAccessCredential({"id": credential_id}), None, None)

        try:
            result = PrivilegedRemoteAccessCredential(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def delete_credential(self, credential_id: str, microtenant_id: str = None) -> tuple:
        """
        Deletes the specified privileged remote access credential.

        Args:
            credential_id (str): The unique identifier of the credential to delete.
            microtenant_id (str, optional): The optional ID of the microtenant if applicable.

        Returns:
            int: The status code of the delete operation.

        Examples:
            >>> _, _, err = client.zpa.pra_credential.delete_credential(
            ...     credential_id='999999'
            ... )
            ... if err:
            ...     print(f"Error deleting pra credential: {err}")
            ...     return
            ... print(f"PRA Credential with ID {'999999'} deleted successfully.")
        """
        http_method = "delete".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /credential/{credential_id}
        """
        )

        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        request, error = self._request_executor.create_request(http_method, api_url, params=params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)
        return (None, response, None)

    def credential_move(self, credential_id: str, query_params=None) -> tuple:
        """
        Moves privileged remote access credentials between parent tenant and microtenants.

        Args:
            credential_id (str): The unique identifier of the credential.
            move_data (dict or object): Dictionary or object that contains the move-related data.
            target_microtenant_id (str): The unique identifier of the target microtenant.
                                        For Default microtenant, 0 should be passed.

        Returns:
            dict: Empty dictionary if the move operation is successful.

        Examples:
            >>> _, _, err = client.zpa.pra_credential.credential_move(
            ...     credential_id=updated_credential.id,
            ...     query_params={
            ...         "microtenant_id": microtenant_id,
            ...         "target_microtenant_id": target_microtenant_id
            ...     }
            ... )
            ... if err:
            ...     print(f"Error moving credential: {err}")
            ...     return
            ... print(f"Credential with ID {updated_credential.id} moved successfully.")
        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /credential/{credential_id}/move
        """
        )

        query_params = query_params or {}

        target_microtenant_id = query_params.get("target_microtenant_id")
        if not target_microtenant_id:
            raise ValueError("target_microtenant_id must be provided in query_params.")

        if "microtenant_id" in query_params:
            query_params["microtenantId"] = query_params.pop("microtenant_id")

        request, error = self._request_executor.create_request(http_method, api_url, params=query_params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, str)
        if error:
            return (None, response, error)

        return (None, None, None)
