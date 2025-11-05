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

from zscaler.request_executor import RequestExecutor
from typing import List, Optional

from zscaler.api_client import APIClient
from zscaler.ztw.models.public_cloud_info import PublicCloudInfo
from zscaler.ztw.models.common import CommonPublicCloudInfo
from zscaler.ztw.models.public_cloud_info import AccountDetails
from zscaler.utils import format_url, transform_common_id_fields, reformat_params
from zscaler.types import APIResult


class PublicCloudInfoAPI(APIClient):

    _ztw_base_endpoint = "/ztw/api/v1"

    def __init__(self, request_executor):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def list_public_cloud_info(self, query_params: Optional[dict] = None) -> APIResult[List[PublicCloudInfo]]:
        """
        Retrieves the list of AWS accounts with metadata.

        See the
        `Partner Integrations API reference (publicCloudInfo-list):
        <https://help.zscaler.com/cloud-branch-connector/partner-integrations#/publicCloudInfo-get>`_
        for further detail on payload structure.

        Keyword Args:
            query_params {dict}: Optional query parameters.

                ``[query_params.page]`` {int}: Specifies the page offset.

                ``[query_params.page_size]`` {int}: Specifies the page size. The default
                    size is 100, but the maximum size is 1000.

        Returns:
            tuple: A tuple containing (list of PublicCloudInfo instances, Response, error)

        Examples:
            Gets a list of all public cloud info.

            >>> public_cloud_info_list, response, error = ztw.public_cloud_info.list_public_cloud_info()
            ... if error:
            ...     print(f"Error listing public cloud info: {error}")
            ...     return
            ... print(f"Total public cloud info found: {len(public_cloud_info_list)}")
            ... for public_cloud_info in public_cloud_info_list:
            ...     print(public_cloud_info.as_dict())

            Gets a list of all public cloud info with search filter.

            >>> public_cloud_info_list, response, error = ztw.public_cloud_info.list_public_cloud_info(
            ...     query_params={"search": "FTP"}
            ... )
            ... if error:
            ...     print(f"Error listing public cloud info: {error}")
            ...     return
            ... print(f"Total public cloud info found: {len(public_cloud_info_list)}")
            ... for public_cloud_info in public_cloud_info_list:
            ...     print(public_cloud_info.as_dict())

        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._ztw_base_endpoint}
            /publicCloudInfo
        """
        )
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
                result.append(PublicCloudInfo(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def list_public_cloud_info_lite(self, query_params: Optional[dict] = None) -> APIResult[List[PublicCloudInfo]]:
        """
        Retrieves basic information about the public cloud accounts.

        Keyword Args:
            query_params {dict}: Optional query parameters.

                ``[query_params.page]`` {int}: Specifies the page offset.

                ``[query_params.page_size]`` {int}: Specifies the page size.
                    The default size is 250, but the maximum size is 1000.

                ``[query_params.search]`` {str}: Search string for filtering results.

                ``[query_params.cloud_type]`` {str}: The cloud type. The default and mandatory value is AWS.
                    Supported values: `AWS`, `AZURE`, `GCP`

        Returns:
            :obj:`Tuple`: A list of configured public accounts.

        Examples:
            List public accounts with default settings:

            >>> public_accounts_list, _, err = client.ztw.public_cloud_info.list_public_cloud_info_lite()
            >>> if err:
            ...     print(f"Error listing public accounts: {err}")
            ...     return
            ... print(f"Total public accounts found: {len(public_accounts_list)}")
            ... for public_account in public_accounts_list:
            ...     print(public_account.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._ztw_base_endpoint}
            /publicCloudInfo/lite
        """
        )

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
                result.append(PublicCloudInfo(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_public_cloud_info(self, cloud_id: int) -> APIResult[PublicCloudInfo]:
        """
        Retrieves the existing AWS account details based on the provided ID.

        Args:
            cloud_id (int): The unique ID of the AWS account.

        Returns:
            tuple: A tuple containing (PublicCloudInfo instance, Response, error)

        Examples:
            >>> fetched_public_cloud_info, response, error = (
            ...     client.ztw.public_cloud_info.get_public_cloud_info(18382907)
            ... )
            ... if error:
            ...     print(f"Error fetching public cloud info by ID: {error}")
            ...     return
            ... print(f"Fetched public cloud info by ID: {fetched_public_cloud_info.as_dict()}")

        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._ztw_base_endpoint}
            /publicCloudInfo/{cloud_id}
        """
        )

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, PublicCloudInfo)

        if error:
            return (None, response, error)

        try:
            result = PublicCloudInfo(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def add_public_cloud_info(self, **kwargs) -> APIResult[PublicCloudInfo]:
        """
        Creates a new AWS account with the provided account and region details.
        You can create a maximum of 512 accounts in each organization.

        Keyword Args:
            name (str): The name of the public cloud account.
            cloud_type (str): The cloud provider type (e.g., "AWS").
            external_id (str, optional): External identifier for the account.
            account_details (dict): Account details object containing:
                - awsAccountId (str): AWS account ID.
                - awsRoleName (str): AWS IAM role name.
                - cloudWatchGroupArn (str): CloudWatch log group ARN. Use "DISABLED" to disable.
                - eventBusName (str): EventBridge event bus name.
                - externalId (str, optional): External identifier.
                - logInfoType (str, optional): Log information type (e.g., "INFO").
                - troubleShootingLogging (bool): Enable troubleshooting logging.
                - trustedAccountId (str): Trusted AWS account ID.
                - trustedRole (str): Trusted IAM role ARN or name.
            account_groups (list, optional): List of account group IDs.
            permission_status (str, optional): Permission status (e.g., "TBD").
            region_status (list, optional): List of region status objects.
            supported_region_ids (list): List of IDs for supported region objects.

        See the
        `Partner Integrations API reference (publicCloudInfo-post):
        <https://help.zscaler.com/cloud-branch-connector/partner-integrations#/publicCloudInfo-post>`_
        for further detail on payload structure.

        Returns:
            tuple: A tuple containing (PublicCloudInfo instance, Response, error)

        Examples:
            Add a new Public Cloud Info:

            >>> new_cloud_info, response, error = ztw.public_cloud_info.add_public_cloud_info(
            ...     name="AWSAccount01",
            ...     cloud_type="AWS",
            ...     account_details={
            ...         "awsAccountId": "202719523534",
            ...         "awsRoleName": "bedrock-core-zscaler-role",
            ...         "cloudWatchGroupArn": "DISABLED",
            ...         "eventBusName": "zscaler-bus-24326813-zscalerthree.net",
            ...         "troubleShootingLogging": True,
            ...         "trustedAccountId": "175726779870",
            ...         "trustedRole": "arn:aws:iam::175726779870:role/ZscalerTagDiscoveryRole"
            ...     },
            ...     supported_region_ids=[12345]
            ... )
            ... if error:
            ...     print(f"Error adding public cloud info: {error}")
            ...     return
            ... print(f"Created public cloud info: {new_cloud_info.as_dict()}")

        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._ztw_base_endpoint}
            /publicCloudInfo
        """
        )

        body = kwargs

        transform_common_id_fields(reformat_params, body, body)

        request, error = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
            body=body,
        )

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, PublicCloudInfo)
        if error:
            return (None, response, error)

        try:
            result = PublicCloudInfo(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_public_cloud_info(self, cloud_id: int, **kwargs) -> APIResult[PublicCloudInfo]:
        """
        Updates the existing AWS account details based on the provided ID.

        Args:
            cloud_id (int): The unique ID of the AWS account.

        Keyword Args:
            name (str, optional): The name of the public cloud account.
            cloud_type (str, optional): The cloud provider type (e.g., "AWS").
            external_id (str, optional): External identifier for the account.
            account_details (dict, optional): Account details object containing:
                - awsAccountId (str): AWS account ID.
                - awsRoleName (str): AWS IAM role name.
                - cloudWatchGroupArn (str): CloudWatch log group ARN. Use "DISABLED" to disable.
                - eventBusName (str): EventBridge event bus name.
                - externalId (str, optional): External identifier.
                - logInfoType (str, optional): Log information type (e.g., "INFO").
                - troubleShootingLogging (bool): Enable troubleshooting logging.
                - trustedAccountId (str): Trusted AWS account ID.
                - trustedRole (str): Trusted IAM role ARN or name.
            account_groups (list, optional): List of account group IDs.
            permission_status (str, optional): Permission status (e.g., "TBD").
            region_status (list, optional): List of region status objects.
            supported_region_ids (list, optional): List of supported region IDs.

        Returns:
            tuple: A tuple containing (PublicCloudInfo instance, Response, error)

        Examples:
            Update public cloud info:

            >>> updated_cloud_info, _, error = client.ztw.public_cloud_info.update_public_cloud_info(
            ...     cloud_id=452125,
            ...     name="Updated AWS Account",
            ...     account_details={
            ...         "awsAccountId": "202719523534",
            ...         "awsRoleName": "updated-zscaler-role",
            ...         "cloudWatchGroupArn": "DISABLED",
            ...         "eventBusName": "zscaler-bus-24326813-zscalerthree.net",
            ...         "troubleShootingLogging": True,
            ...         "trustedAccountId": "175726779870",
            ...         "trustedRole": "arn:aws:iam::175726779870:role/ZscalerTagDiscoveryRole"
            ...     },
            ...     supported_region_ids=[12345]
            ... )
            ... if error:
            ...     print(f"Error updating public cloud info: {error}")
            ...     return
            ... print(f"Public cloud info updated: {updated_cloud_info.as_dict()}")

        """
        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._ztw_base_endpoint}
            /publicCloudInfo/{cloud_id}
        """
        )

        body = {}

        body.update(kwargs)

        transform_common_id_fields(reformat_params, body, body)

        request, error = self._request_executor.create_request(http_method, api_url, body, {}, {})
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, PublicCloudInfo)
        if error:
            return (None, response, error)

        try:
            result = PublicCloudInfo(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def delete_public_cloud_info(self, cloud_id: int) -> APIResult[None]:
        """
        Removes a specific AWS account based on the provided ID.

        Args:
            cloud_id (int): The unique ID of the AWS account.

        Returns:
            tuple: A tuple containing (None, Response, error). The API returns 204 No Content on success.

        Examples:
            >>> _, _, error = client.ztw.public_cloud_info.delete_public_cloud_info(545845)
            ... if error:
            ...     print(f"Error deleting public cloud info: {error}")
            ...     return
            ... print("Public cloud info deleted successfully")

        """
        http_method = "delete".upper()
        api_url = format_url(
            f"""
            {self._ztw_base_endpoint}
            /publicCloudInfo/{cloud_id}
        """
        )

        params = {}

        request, error = self._request_executor.create_request(http_method, api_url, params=params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)
        return (None, response, None)

    def get_cloud_formation_template(self, aws_account_id: Optional[str] = None) -> APIResult[str]:
        """
        Retrieves the CloudFormation template URL.

        This endpoint returns a URL string pointing to a CloudFormation template YAML file.
        The URL can be customized with an AWS account ID if provided.

        Args:
            aws_account_id (str, optional): The AWS account ID to customize the
                CloudFormation template URL. If provided, the URL is customized with
                account-specific values. If not provided, a generic template URL is returned.

        Returns:
            tuple: A tuple containing (URL string, Response, error)

        Examples:
            Get generic CloudFormation template URL:

            >>> template_url, _, error = client.ztw.public_cloud_info.get_cloud_formation_template()
            ... if error:
            ...     print(f"Error getting CloudFormation template: {error}")
            ...     return
            ... print(f"CloudFormation template URL: {template_url}")

            Get customized CloudFormation template URL for specific AWS account:

            >>> template_url, _, error = client.ztw.public_cloud_info.get_cloud_formation_template(
            ...     aws_account_id="202719523534"
            ... )
            ... if error:
            ...     print(f"Error getting CloudFormation template: {error}")
            ...     return
            ... print(f"CloudFormation template URL: {template_url}")
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._ztw_base_endpoint}
            /publicCloudInfo/cloudFormationTemplate
        """
        )

        query_params = {}
        if aws_account_id:
            query_params["awsAccountId"] = aws_account_id

        headers = {}

        request, error = self._request_executor.create_request(
            http_method, api_url, body={}, headers=headers, params=query_params
        )
        if error:
            return (None, None, error)

        # Get raw response - this endpoint returns plain text URL even though Content-Type is application/json
        raw_response, error = self._request_executor.execute(request, return_raw_response=True)

        # Check the actual HTTP status code, not the error object
        # The executor may return an "error" for non-JSON responses even on HTTP 200
        # When return_raw_response=True, we need to check the actual response status
        if raw_response is None:
            # True network/request error
            return (None, None, error)

        try:
            # Ensure we have a valid response object with status_code attribute
            if not hasattr(raw_response, 'status_code'):
                return (None, raw_response, error if error else "Invalid response object")

            status_code = raw_response.status_code
            body_text = raw_response.text.strip() if hasattr(raw_response, 'text') else ""

            # HTTP 200 = successful response with URL string
            if status_code == 200:
                # Return the URL string from the response body
                return (body_text, raw_response, None)

            # Any other response = error
            else:
                return (None, raw_response, error if error else f"Unexpected response: {status_code}")

        except Exception as ex:
            return (None, raw_response, ex)

    def get_public_cloud_info_count(self) -> APIResult[List[dict]]:
        """
        Returns the count of configured public cloud accounts for the provided customer.

        This endpoint returns a list of dictionaries, each containing the number of
        public cloud accounts configured and the date when the configuration was set.

        Returns:
            :obj:`Tuple`: A tuple containing a list of dictionaries with configuration
            count information, the response object, and error if any.

        Examples:
            >>> counts, _, error = client.ztw.public_cloud_info.get_public_cloud_info_count()
            ... if error:
            ...     print(f"Error getting public cloud info count: {error}")
            ...     return
            ... print(f"Found {len(counts)} count records:")
            ... for count in counts:
            ...     print(count)
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._ztw_base_endpoint}
            /publicCloudInfo/count
        """
        )

        request, error = self._request_executor.create_request(http_method, api_url)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        try:
            result = []
            for item in response.get_results():
                result.append(self.form_response_body(item))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def generate_external_id(self, **kwargs) -> APIResult[AccountDetails]:
        """
        Generates an external ID for an AWS account.

        This endpoint creates a unique external ID that can be used when configuring
        AWS IAM roles for cross-account access. The external ID is required for secure
        cross-account access scenarios.

        Keyword Args:
            aws_account_id (str): The AWS account ID for which to generate the external ID.
            aws_role_name (str): The AWS IAM role name associated with the account.

        See the
        `Partner Integrations API reference (publicCloudInfo-generateExternalId):
        <https://help.zscaler.com/cloud-branch-connector/partner-integrations#/publicCloudInfo-generateExternalId-post>`_
        for further detail on payload structure.

        Returns:
            tuple: A tuple containing (AccountDetails instance with the generated external_id,
            Response, error)

        Examples:
            Generate an external ID for an AWS account:

            >>> account_details, response, error = client.ztw.public_cloud_info.generate_external_id(
            ...     aws_account_id="202719523534",
            ...     aws_role_name="bedrock-core-zscaler-role"
            ... )
            ... if error:
            ...     print(f"Error generating external ID: {error}")
            ...     return
            ... print(f"Generated external ID: {account_details.external_id}")
            ... print(f"Account details: {account_details.as_dict()}")

        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._ztw_base_endpoint}
            /publicCloudInfo/generateExternalId
        """
        )

        body = kwargs

        request, error = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
            body=body,
        )

        if error:
            return (None, None, error)

        # Use raw response to avoid JSON parsing error for plain text response
        raw_response, error = self._request_executor.execute(request, return_raw_response=True)
        if error:
            return (None, None, error)

        if not raw_response:
            return (None, None, "No response received")

        # API returns plain text external ID string
        external_id = raw_response.text.strip()
        account_details_config = {
            "externalId": external_id,
            "awsAccountId": kwargs.get("aws_account_id"),
            "awsRoleName": kwargs.get("aws_role_name"),
        }
        result = AccountDetails(account_details_config)
        return (result, raw_response, None)

    def change_state_public_cloud_info(self, cloud_id: int, **kwargs) -> APIResult[PublicCloudInfo]:
        """
        Enables or disables a specific AWS account in all regions based on the provided ID.

        Args:
            cloud_id (int): The unique ID of the AWS account.

        Keyword Args:
            query_params {dict}: Optional query parameters.

                ``[query_params.enable]`` {bool}: Set true to enable the AWS account, and false to disable it.

        Returns:
            tuple: A tuple containing (PublicCloudInfo instance, Response, error)

        Examples:
            Update public cloud info:

            >>> change_state, _, error = client.ztw.public_cloud_info.change_state_public_cloud_info(
            ...     cloud_id=452125,
            ...     },
            ... )
            ... if error:
            ...     print(f"Error changing state of public cloud info: {error}")
            ...     return
            ... print(f"Public cloud info updated: {change_state.as_dict()}")

        """
        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._ztw_base_endpoint}
            /publicCloudInfo/{cloud_id}/changeState
        """
        )

        body = {}

        body.update(kwargs)

        request, error = self._request_executor.create_request(http_method, api_url, body, {}, {})
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, PublicCloudInfo)
        if error:
            return (None, response, error)

        try:
            result = PublicCloudInfo(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)
