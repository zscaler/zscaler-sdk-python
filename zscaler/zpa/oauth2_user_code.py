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

from typing import Dict, List, Optional, Any, Union
from zscaler.api_client import APIClient
from zscaler.request_executor import RequestExecutor
from zscaler.zpa.models.oauth2_user_code import OAuth2UserCode
from zscaler.utils import format_url
from zscaler.types import APIResult


def simplify_key_type(key_type):
    """
    Simplifies the key type for the user. Accepted values are 'connector' and 'service_edge'.

    Args:
        key_type (str): The key type provided by the user.

    Returns:
        str: The simplified key type.
    """
    if key_type == "connector":
        return "CONNECTOR_GRP"
    elif key_type == "service_edge":
        return "SERVICE_EDGE_GRP"
    elif key_type == "assistant_group":
        return "NP_ASSISTANT_GRP"
    elif key_type == "site_controller_group":
        return "SITE_CONTROLLER_GRP"
    else:
        raise ValueError("Unexpected key type.")


class OAuth2UserCodeAPI(APIClient):
    """
    A Client object for the OAuth2 User Code resource.
    """

    def __init__(self, request_executor, config):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor
        customer_id = config["client"].get("customerId")
        self._zpa_base_endpoint = f"/zpa/mgmtconfig/v1/admin/customers/{customer_id}"

    def verify_oauth2_user_code(self, key_type: str, **kwargs) -> APIResult[OAuth2UserCode]:
        """
        Verifies the provided list of user codes for a given component provisioning.

        Args:
            key_type (str): The type of provisioning key, accepted values are:
                ``connector``, ``service_edge``, ``assistant_group``, and ``site_controller_group``.

        Keyword Args:
            user_codes (list[str]): List of user codes to verify.
            component_group_id (int, optional): The unique identifier of the component group.
            config_cloud_name (str, optional): The cloud name for the configuration.
            enrollment_server (str, optional): The enrollment server URL.
            nonce_association_type (str, optional): The nonce association type (e.g., ``ASSISTANT_GRP``).
            tenant_id (int, optional): The unique identifier of the tenant.
            zcomponent_id (int, optional): The unique identifier of the Zscaler component.
            microtenant_id (str, optional): The microtenant ID if applicable.

        Returns:
            :obj:`Tuple`: A tuple containing (OAuth2UserCode instance, Response, error).

        Examples:
            >>> verified_codes, _, err = client.zpa.oauth2_user_code.verify_oauth2_user_code(
            ...     key_type='connector',
            ...     user_codes=['code1', 'code2', 'code3']
            ... )
            ... if err:
            ...     print(f"Error verifying user codes: {err}")
            ...     return
            ... print(f"User codes verified successfully: {verified_codes.as_dict()}")
        """
        if not key_type:
            raise ValueError("key_type must be provided.")

        http_method = "post".upper()
        api_url = format_url(
            f"""{
            self._zpa_base_endpoint}
            /associationType/{simplify_key_type(key_type)}/usercodes
        """
        )

        body = kwargs

        microtenant_id = body.get("microtenant_id", None)
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        request, error = self._request_executor.create_request(http_method, api_url, body=body, params=params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, OAuth2UserCode)
        if error:
            return (None, response, error)

        try:
            result = OAuth2UserCode(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def add_provisioning_key(self, key_type: str, **kwargs) -> APIResult[OAuth2UserCode]:
        """
        Adds a new Provisioning Key for the specified customer.

        Args:
            key_type (str): The type of provisioning key, accepted values are:
                ``connector``, ``service_edge``, ``assistant_group``, and ``site_controller_group``.

        Keyword Args:
            user_codes (list[str]): List of user codes associated with the provisioning key.
            component_group_id (int, optional): The unique identifier of the component group.
            config_cloud_name (str, optional): The cloud name for the configuration.
            enrollment_server (str, optional): The enrollment server URL.
            nonce_association_type (str, optional): The nonce association type (e.g., ``ASSISTANT_GRP``).
            tenant_id (int, optional): The unique identifier of the tenant.
            zcomponent_id (int, optional): The unique identifier of the Zscaler component.
            microtenant_id (str, optional): The microtenant ID if applicable.

        Returns:
            :obj:`Tuple`: A tuple containing (OAuth2UserCode instance, Response, error).

        Examples:
            >>> new_prov_key, _, err = client.zpa.oauth2_user_code.add_provisioning_key(
            ...     key_type='connector',
            ...     user_codes=['code1', 'code2']
            ... )
            ... if err:
            ...     print(f"Error adding provisioning key: {err}")
            ...     return
            ... print(f"Provisioning key added successfully: {new_prov_key.as_dict()}")
        """
        if not key_type:
            raise ValueError("key_type must be provided.")

        http_method = "post".upper()
        api_url = format_url(
            f"""{
            self._zpa_base_endpoint}
            /associationType/{simplify_key_type(key_type)}/usercodes/status
        """
        )

        body = kwargs

        microtenant_id = body.get("microtenant_id", None)
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        request, error = self._request_executor.create_request(http_method, api_url, body=body, params=params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, OAuth2UserCode)
        if error:
            return (None, response, error)

        try:
            result = OAuth2UserCode(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)
