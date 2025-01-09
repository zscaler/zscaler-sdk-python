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
from zscaler.zpa.models.cbi_banner import CBIBanner
from zscaler.utils import format_url


class CBIBannerAPI(APIClient):
    """
    A Client object for the Cloud Browser Isolation Banners resource.
    """

    def __init__(self, request_executor, config):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor
        customer_id = config["client"].get("customerId")
        self._cbi_base_endpoint = f"/zpa/cbiconfig/cbi/api/customers/{customer_id}"

    def list_cbi_banners(self) -> tuple:
        """
        Returns a list of all cloud browser isolation banners.

        Returns:
            tuple: A tuple containing a list of `CBIBanner` instances, response object, and error if any.
        """
        http_method = "get".upper()
        api_url = format_url(f"""
            {self._cbi_base_endpoint}
            /banners
        """)

        request, error = self._request_executor\
            .create_request(http_method, api_url)
        if error:
            return (None, None, error)

        response, error = self._request_executor\
            .execute(request)
        if error:
            return (None, response, error)

        try:
            result = []
            for item in response.get_results():
                result.append(CBIBanner(
                    self.form_response_body(item))
                )
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_cbi_banner(self, banner_id: str) -> tuple:
        """
        Returns information on the specified cloud browser isolation banner.

        Args:
            banner_id (str): The unique identifier for the cloud browser isolation banner.

        Returns:
            tuple: A tuple containing the `CBIBanner` instance, response object, and error if any.
        """
        http_method = "get".upper()
        api_url = format_url(f"""
            {self._cbi_base_endpoint}
            /banners/{banner_id}
        """)

        request, error = self._request_executor\
            .create_request(http_method, api_url)
        if error:
            return (None, None, error)

        response, error = self._request_executor\
            .execute(request, CBIBanner)
        if error:
            return (None, response, error)

        try:
            result = CBIBanner(
                self.form_response_body(response.get_body())
            )
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def add_cbi_banner(self, **kwargs) -> tuple:
        """
        Adds a new cloud browser isolation banner.

        Args:
            name (str): The name of the new cloud browser isolation banner.
            banner (bool): Whether to enable the cloud browser isolation banner.

        Returns:
            tuple: A tuple containing the `CBIBanner` instance, response object, and error if any.
        """
        http_method = "post".upper()
        api_url = format_url(f"""
            {self._cbi_base_endpoint}
            /banner
        """)

        # Construct the body from kwargs (as a dictionary)
        body = kwargs

        request, error = self._request_executor\
            .create_request(http_method, api_url, body=body)
        if error:
            return (None, None, error)

        response, error = self._request_executor\
            .execute(request, CBIBanner)
        if error:
            return (None, response, error)

        try:
            result = CBIBanner(
                self.form_response_body(response.get_body())
            )
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_cbi_banner(self, banner_id: str, **kwargs) -> tuple:
        """
        Updates an existing cloud browser isolation banner.

        Args:
            banner_id (str): The unique identifier of the cloud browser isolation banner.

        Returns:
            tuple: A tuple containing the `CBIBanner` instance, response object, and error if any.
        """
        http_method = "put".upper()
        api_url = format_url(f"""
            {self._cbi_base_endpoint}
            /banners/{banner_id}
        """)

        # Start with an empty body or an existing resource's current data
        body = {}

        # Update the body with the fields passed in kwargs
        body.update(kwargs)

        request, error = self._request_executor\
            .create_request(http_method, api_url, body, {})
        if error:
            return (None, None, error)

        response, error = self._request_executor\
            .execute(request, CBIBanner)
        if error:
            return (None, response, error)

        # Handle case where no content is returned (204 No Content)
        if response is None:
            # Return a meaningful result to indicate success
            return (CBIBanner({"id": banner_id}), None, None)

        try:
            result = CBIBanner(
                self.form_response_body(response.get_body())
            )
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def delete_cbi_banner(self, banner_id: str) -> tuple:
        """
        Deletes the specified cloud browser isolation banner.

        Args:
            banner_id (str): The unique identifier for the cloud browser isolation banner to be deleted.

        Returns:
            tuple: A tuple containing the response object and error if any.
        """
        http_method = "delete".upper()
        api_url = format_url(f"""
            {self._cbi_base_endpoint}
            /banners/{banner_id}
        """)

        request, error = self._request_executor\
            .create_request(http_method, api_url)
        if error:
            return (None, None, error)

        response, error = self._request_executor\
            .execute(request)
        if error:
            return (None, response, error)

        return (None, response, None)
