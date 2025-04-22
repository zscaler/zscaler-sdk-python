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
            :obj:`Tuple`: A tuple containing a list of `CBIBanner` instances, response object, and error if any.

        Examples:
            >>> banner_list, _, err = client.zpa.cbi_banner.list_cbi_banners()
            ... if err:
            ...     print(f"Error listing banners: {err}")
            ...     return
            ... print(f"Total banners found: {len(banner_list)}")
            ... for banner in banner_list:
            ...     print(banner.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._cbi_base_endpoint}
            /banners
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
                result.append(CBIBanner(self.form_response_body(item)))
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

        Examples:
            >>> fetched_banner, _, err = client.zpa.cbi_banner.get_cbi_banner(
            ... banner_id='ab73fa29-667a-4057-83c5-6a8dccf84930')
            ... if err:
            ...     print(f"Error fetching banner by ID: {err}")
            ...     return
            ... print(f"Fetched banner by ID: {fetched_banner.as_dict()}")
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._cbi_base_endpoint}
            /banners/{banner_id}
        """
        )

        request, error = self._request_executor.create_request(http_method, api_url)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, CBIBanner)
        if error:
            return (None, response, error)

        try:
            result = CBIBanner(self.form_response_body(response.get_body()))
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

        Examples:
            >>> added_banner, _, err = client.zpa.cbi_banner.add_cbi_banner(
            ...     name=f"Create_CBI_Banner_{random.randint(1000, 10000)}",
            ...     logo= "data:image/png;base64,iVBORw0KGgoAAAANS",
            ...     primary_color= "#0076BE",
            ...     text_color= "#FFFFFF",
            ...     banner=True,
            ...     notification_title= "Heads up, you've been redirected to Browser Isolation!",
            ...     notification_text= "The website you were trying to access",
            ... )
            ... if err:
            ...     print(f"Error adding cbi banner: {err}")
            ...     return
            ... print(f"CBI Banner added successfully: {added_banner.as_dict()}")
        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._cbi_base_endpoint}
            /banner
        """
        )

        body = kwargs

        request, error = self._request_executor.create_request(http_method, api_url, body=body)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, CBIBanner)
        if error:
            return (None, response, error)

        try:
            result = CBIBanner(self.form_response_body(response.get_body()))
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

        Examples:
            >>> updated_banner, _, err = client.zpa.cbi_banner.update_cbi_banner(
            ...     banner_id='ab73fa29-667a-4057-83c5-6a8dccf84930'
            ...     name=f"Update_CBI_Banner_{random.randint(1000, 10000)}",
            ...     logo= "data:image/png;base64,iVBORw0KGgoAAAANS",
            ...     primary_color= "#0076BE",
            ...     text_color= "#FFFFFF",
            ...     banner=True,
            ...     notification_title= "Heads up, you've been redirected to Browser Isolation!",
            ...     notification_text= "The website you were trying to access",
            ... )
            ... if err:
            ...     print(f"Error updating cbi banner: {err}")
            ...     return
            ... print(f"CBI Banner updated successfully: {updated_banner.as_dict()}")
        """
        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._cbi_base_endpoint}
            /banners/{banner_id}
        """
        )

        body = {}

        body.update(kwargs)

        request, error = self._request_executor.create_request(http_method, api_url, body, {})
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, CBIBanner)
        if error:
            return (None, response, error)

        # Handle case where no content is returned (204 No Content)
        if response is None:
            # Return a meaningful result to indicate success
            return (CBIBanner({"id": banner_id}), None, None)

        try:
            result = CBIBanner(self.form_response_body(response.get_body()))
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

        Examples:
            >>> _, _, err = client.zpa.cbi_banner.delete_cbi_banner(
            ...     banner_id='ab73fa29-667a-4057-83c5-6a8dccf84930'
            ... )
            ... if err:
            ...     print(f"Error deleting cbi banner: {err}")
            ...     return
            ... print(f"CBI Banner with ID {ab73fa29-667a-4057-83c5-6a8dccf84930} deleted successfully.")
        """
        http_method = "delete".upper()
        api_url = format_url(
            f"""
            {self._cbi_base_endpoint}
            /banners/{banner_id}
        """
        )

        request, error = self._request_executor.create_request(http_method, api_url)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        return (None, response, None)
