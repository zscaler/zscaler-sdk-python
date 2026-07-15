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

from datetime import datetime
from typing import List

from zscaler.api_client import APIClient
from zscaler.request_executor import RequestExecutor
from zscaler.types import APIResult
from zscaler.utils import format_url
from zscaler.zpa.models.business_continuity import BusinessContinuity


class BusinessContinuityAPI(APIClient):

    def __init__(self, request_executor, config):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor
        customer_id = config["client"].get("customerId")
        self._zpa_base_endpoint = f"/zpa/mgmtconfig/v1/admin/customers/{customer_id}"

    def list_business_continuity_settings(self) -> APIResult[List[BusinessContinuity]]:
        """
        Returns the configured business continuity settings.

        This endpoint takes no parameters.

        Returns:
            tuple: (list of BusinessContinuity instances, Response, error)

        Examples:
            List the business continuity settings::

                >>> settings, _, err = client.zpa.business_continuity.list_business_continuity_settings()
                >>> if err:
                ...     print(f"Error listing business continuity settings: {err}")
                ...     return
                >>> for setting in settings:
                ...     print(setting.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(f"""
            {self._zpa_base_endpoint}
            /businessContinuitySettings
        """)

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)
        try:
            result = []
            for item in response.get_results():
                result.append(BusinessContinuity(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_business_continuity_setting_certificate(self, filename: str = None) -> str:
        """
        Downloads the SAML SP certificate for the business continuity settings.

        This endpoint takes no parameters. The certificate is streamed as a file
        attachment (``sp_cert.crt``) and written to disk, similar to the ZCC
        ``download_devices`` helper.

        Args:
            filename (str, optional): Custom filename for the certificate.
                Defaults to a timestamped ``.crt`` name.

        Returns:
            str: Path to the downloaded certificate file.

        Examples:
            Download the business continuity SP certificate::

                >>> try:
                ...     path = client.zpa.business_continuity.get_business_continuity_setting_certificate()
                ...     print(f"Certificate downloaded successfully: {path}")
                ... except Exception as e:
                ...     print(f"Error during download: {e}")
        """
        if not filename:
            filename = f"bc-sp-certificate-{datetime.now().strftime('%Y%m%d-%H_%M_%S')}.crt"

        http_method = "get".upper()
        api_url = format_url(f"""
            {self._zpa_base_endpoint}
            /businessContinuitySettings/certificate
        """)

        request, error = self._request_executor.create_request(http_method, api_url, headers={"Accept": "*/*"})
        if error:
            raise Exception("Error creating request for downloading the business continuity certificate.")

        response, error = self._request_executor.execute(request, return_raw_response=True)
        if error:
            raise error
        if response is None:
            raise Exception("No response received when downloading the business continuity certificate.")

        with open(filename, "wb") as f:
            f.write(response.content)

        return filename

    def get_business_continuity_setting_metadata(self, filename: str = None) -> str:
        """
        Downloads the SAML metadata for the business continuity settings.

        This endpoint takes no parameters. The metadata is streamed as a file
        attachment (``metadata.xml``) and written to disk, similar to the ZCC
        ``download_devices`` helper.

        Args:
            filename (str, optional): Custom filename for the metadata.
                Defaults to a timestamped ``.xml`` name.

        Returns:
            str: Path to the downloaded metadata file.

        Examples:
            Download the business continuity SAML metadata::

                >>> try:
                ...     path = client.zpa.business_continuity.get_business_continuity_setting_metadata()
                ...     print(f"Metadata downloaded successfully: {path}")
                ... except Exception as e:
                ...     print(f"Error during download: {e}")
        """
        if not filename:
            filename = f"bc-metadata-{datetime.now().strftime('%Y%m%d-%H_%M_%S')}.xml"

        http_method = "get".upper()
        api_url = format_url(f"""
            {self._zpa_base_endpoint}
            /businessContinuitySettings/metadata
        """)

        request, error = self._request_executor.create_request(http_method, api_url, headers={"Accept": "*/*"})
        if error:
            raise Exception("Error creating request for downloading the business continuity metadata.")

        response, error = self._request_executor.execute(request, return_raw_response=True)
        if error:
            raise error
        if response is None:
            raise Exception("No response received when downloading the business continuity metadata.")

        with open(filename, "wb") as f:
            f.write(response.content)

        return filename

    def get_business_continuity_setting(self, business_continuity_setting_id: str) -> APIResult[BusinessContinuity]:
        """
        Returns information for the specified business_continuity_setting.

        Args:
            business_continuity_setting_id (str): The unique identifier for the business_continuity_setting.

        Returns:
            tuple: The resource record for the business_continuity_setting.
        """
        http_method = "get".upper()
        api_url = format_url(f"""
            {self._zpa_base_endpoint}
            /businessContinuitySettings/{business_continuity_setting_id}
        """)
        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, BusinessContinuity)
        if error:
            return (None, response, error)
        try:
            result = BusinessContinuity(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def add_business_continuity_setting(self, **kwargs) -> APIResult[BusinessContinuity]:
        """
        Adds a new business_continuity_setting.

        Returns:
            tuple: The newly created business_continuity_setting resource record.
        """
        http_method = "post".upper()
        api_url = format_url(f"""
            {self._zpa_base_endpoint}
            /businessContinuitySettings
        """)

        body = kwargs

        request, error = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
            body=body,
        )
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, BusinessContinuity)
        if error:
            return (None, response, error)
        try:
            result = BusinessContinuity(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_business_continuity_setting(
        self, business_continuity_setting_id: str, **kwargs
    ) -> APIResult[BusinessContinuity]:
        """
        Updates an existing business_continuity_setting.

        Args:
            business_continuity_setting_id (str): The unique ID for the business_continuity_setting being updated.
            **kwargs: Optional keyword args.

        Returns:
            tuple: The updated business_continuity_setting resource record.
        """
        http_method = "put".upper()
        api_url = format_url(f"""
            {self._zpa_base_endpoint}
            /businessContinuitySettings/{business_continuity_setting_id}
        """)

        body = kwargs

        request, error = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
            body=body,
        )
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, BusinessContinuity)
        if error:
            return (None, response, error)
        try:
            result = BusinessContinuity(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def delete_business_continuity_setting(self, business_continuity_setting_id: str) -> APIResult[None]:
        """
        Deletes the specified business_continuity_setting.

        Args:
            business_continuity_setting_id (str): The unique identifier for the business_continuity_setting.

        Returns:
            tuple: A tuple containing the response object and error (if any).
        """
        http_method = "delete".upper()
        api_url = format_url(f"""
            {self._zpa_base_endpoint}
            /businessContinuitySettings/{business_continuity_setting_id}
        """)

        params = {}

        request, error = self._request_executor.create_request(http_method, api_url, params=params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)
        return (None, response, None)
