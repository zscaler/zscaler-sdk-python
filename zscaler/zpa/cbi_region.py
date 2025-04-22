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
from zscaler.zpa.models.cbi_region import CBIRegion
from zscaler.utils import format_url


class CBIRegionAPI(APIClient):
    """
    A Client object for the Cloud Browser Isolation Banners resource.
    """

    def __init__(self, request_executor, config):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor
        customer_id = config["client"].get("customerId")
        self._cbi_base_endpoint = f"/zpa/cbiconfig/cbi/api/customers/{customer_id}"

    def list_cbi_regions(self) -> list:
        """
        Returns a list of all cloud browser isolation regions.

        Returns:
            tuple: A tuple containing a list of `CBIRegion` instances, response object, and error if any.

        Examples:
            >>> region_list, _, err = client.zpa.cbi_region.list_cbi_regions()
            ... if err:
            ...     print(f"Error listing regions: {err}")
            ...     return
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._cbi_base_endpoint}
            /regions
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
                result.append(CBIRegion(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)
