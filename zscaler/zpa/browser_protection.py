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
from zscaler.zpa.models.browser_protection import BrowserProtectionProfile
from zscaler.utils import format_url
from zscaler.types import APIResult


class BrowserProtectionProfileAPI(APIClient):
    """
    A Client object for the Browser Protection Profile resource.
    """

    def __init__(self, request_executor, config):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor
        customer_id = config["client"].get("customerId")
        self._zpa_base_endpoint = f"/zpa/mgmtconfig/v1/admin/customers/{customer_id}"

    def list_active_browser_protection_profile(self) -> APIResult[List[BrowserProtectionProfile]]:
        """
        Get the active browser protection profile details for the specified customer.

        This endpoint returns the active browser protection profile without requiring any parameters.

        Returns:
            :obj:`Tuple`: A tuple containing (list of BrowserProtectionProfile instances, Response, error)

        Examples:
            >>> profile_list, _, err = client.zpa.browser_protection.list_active_browser_protection_profile()
            ... if err:
            ...     print(f"Error listing browser protection profiles: {err}")
            ...     return
            ... print(f"Total browser protection profiles found: {len(profile_list)}")
            ... for profile in profile_list:
            ...     print(profile.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /activeBrowserProtectionProfile
        """
        )

        request, error = self._request_executor.create_request(http_method, api_url)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, BrowserProtectionProfile)
        if error:
            return (None, response, error)

        try:
            result = []
            for item in response.get_results():
                result.append(BrowserProtectionProfile(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def list_browser_protection_profile(
        self, query_params: Optional[dict] = None
    ) -> APIResult[List[BrowserProtectionProfile]]:
        """
        Gets all configured browser protection profiles for the specified customer.

        Args:
            query_params {dict}: Map of query parameters for the request.

                ``[query_params.page]`` {str}: Specifies the page number.

                ``[query_params.page_size]`` {str}: Specifies the page size.
                    If not provided, the default page size is 20. The max page size is 500.

                ``[query_params.search]`` {str}: Search string for filtering results.
                ``[query_params.sort]`` (str, optional): The sort string used to support
                    sorting on the given field for the API. Default: `sort`.

                ``[query_params.sortdir]`` (str, optional): Specifies the sorting order by
                    ascending (`ASC`) or descending (`DESC`) order.
                    Default: `ASC`.

        Returns:
            :obj:`Tuple`: A tuple containing (list of BrowserProtectionProfile instances, Response, error)

        Examples:
            >>> profile_list, _, err = client.zpa.browser_protection.list_browser_protection_profile(
            ...     query_params={'search': 'Profile01', 'page': '1', 'page_size': '100'})
            ... if err:
            ...     print(f"Error listing browser protection profiles: {err}")
            ...     return
            ... print(f"Total browser protection profiles found: {len(profile_list)}")
            ... for profile in profile_list:
            ...     print(profile.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /browserProtectionProfile
        """
        )

        query_params = query_params or {}

        request, error = self._request_executor.create_request(http_method, api_url, params=query_params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, BrowserProtectionProfile)
        if error:
            return (None, response, error)

        try:
            result = []
            for item in response.get_results():
                result.append(BrowserProtectionProfile(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_browser_protection_profile(self, profile_id: str, **kwargs) -> APIResult[BrowserProtectionProfile]:
        """
        Sets a specified browser protection profile as active for the specified customer.

        Args:
            profile_id (str): The unique identifier of the browser protection profile in ZPA.

        Keyword Args:
            name (str): The name of the browser protection profile.
            description (str): Additional information about the browser protection profile.
            default_csp (bool): Whether to use the default Content Security Policy.
            criteria_flags_mask (int): The criteria flags mask used for browser protection
                matching.
            criteria (dict): The criteria configuration object containing fingerprint
                settings. This should be a dictionary with the following structure:

                - fingerPrintCriteria (dict): Fingerprint criteria configuration
                    - browser (dict): Browser fingerprinting settings
                        - browser_eng (bool): Collect browser engine information
                        - browser_eng_ver (bool): Collect browser engine version
                        - browser_name (bool): Collect browser name
                        - browser_version (bool): Collect browser version
                        - canvas (bool): Collect canvas fingerprinting data
                        - flash_ver (bool): Collect Flash version
                        - fp_usr_agent_str (bool): Collect user agent string
                        - is_cookie (bool): Check for cookie support
                        - is_local_storage (bool): Check for local storage support
                        - is_sess_storage (bool): Check for session storage support
                        - ja3 (bool): Collect JA3 fingerprint
                        - mime (bool): Collect MIME type information
                        - plugin (bool): Collect plugin information
                        - silverlight_ver (bool): Collect Silverlight version
                    - collect_location (bool): Whether to collect location information
                    - fingerprint_timeout (int): Timeout in seconds for fingerprint collection
                    - location (dict): Location collection settings
                        - lat (bool): Collect latitude
                        - lon (bool): Collect longitude
                    - system (dict): System fingerprinting settings
                        - avail_screen_resolution (bool): Collect available screen resolution
                        - cpu_arch (bool): Collect CPU architecture
                        - curr_screen_resolution (bool): Collect current screen resolution
                        - font (bool): Collect font information
                        - java_ver (bool): Collect Java version
                        - mobile_dev_type (bool): Collect mobile device type
                        - monitor_mobile (bool): Monitor mobile devices
                        - os_name (bool): Collect operating system name
                        - os_version (bool): Collect operating system version
                        - sys_lang (bool): Collect system language
                        - tz (bool): Collect timezone information
                        - usr_lang (bool): Collect user language

        Returns:
            :obj:`Tuple`: A tuple containing the updated BrowserProtectionProfile instance, response object, and error if any.

        Examples:
            >>> updated_profile, _, err = client.zpa.browser_protection.update_browser_protection_profile(
            ...     profile_id='999999'
            ... )
            ... if err:
            ...     print(f"Error updating browser protection profile: {err}")
            ...     return
            ... print(f"Browser protection profile updated successfully: {updated_profile.as_dict()}")
        """
        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /browserProtectionProfile/setActive/{profile_id}
        """
        )

        body = kwargs

        request, error = self._request_executor.create_request(http_method, api_url, body=body)
        if error:
            return (None, None, error)

        # Execute the request
        response, error = self._request_executor.execute(request, BrowserProtectionProfile)
        if error:
            return (None, response, error)

        if response is None:
            return (BrowserProtectionProfile({"id": profile_id}), None, None)

        try:
            result = BrowserProtectionProfile(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)
