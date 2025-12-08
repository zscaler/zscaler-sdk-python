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

    def list_cbi_regions(self) -> List[CBIRegion]:
        """
        Returns a list of all cloud browser isolation regions.

        Returns:

        Examples:
            >>> try:
            ...     region_list = client.zpa.cbi_region.list_cbi_regions()
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._cbi_base_endpoint}
            /regions
        """
        )

        request = self._request_executor.create_request(http_method, api_url)
        response = self._request_executor.execute(request)
        result = []
        for item in response.get_results():
            result.append(CBIRegion(self.form_response_body(item)))
        return result
