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
from zscaler.zpa.models.cbi_profile import CBIProfile
from zscaler.utils import format_url


class CBIProfileAPI(APIClient):
    """
    A Client object for the Cloud Browser Isolation Profile resource.
    """

    def __init__(self, request_executor, config):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor
        customer_id = config["client"].get("customerId")
        self._cbi_base_endpoint = f"/zpa/cbiconfig/cbi/api/customers/{customer_id}"

    def list_cbi_profiles(self) -> List[CBIProfile]:
        """
        Returns a list of all cloud browser isolation profile.

        Args:
            scope_id (str, optional): The unique identifier of the scope of the tenant to filter the profiles.

        Returns:
            :obj:`Tuple`: A tuple containing a list of `CBIProfile` instances, response object, and error if any.

        Examples:
            >>> try:
            ...     profile_list = client.zpa.cbi_profile.list_cbi_profiles()
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
            ... print(f"Total profiles found: {len(profile_list)}")
            ... for profile in profile_list:
            ...     print(profile.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._cbi_base_endpoint}
            /profiles
        """
        )

        request = self._request_executor.create_request(http_method, api_url)
        response = self._request_executor.execute(request)
        result = []
        for item in response.get_results():
            result.append(CBIProfile(self.form_response_body(item)))
        return result

    def get_cbi_profile(self, profile_id: str) -> CBIProfile:
        """
        Returns information on the specified cloud browser isolation profile.

        Args:
            profile_id (str): The unique identifier for the cloud browser isolation profile.

        Returns:
            :obj:`Tuple`: A tuple containing the `CBIProfile` instance, response object, and error if any.

        Examples:
            >>> try:
            ...     fetched_profile = client.zpa.cbi_profile.get_cbi_profile(
            ... profile_id='ab73fa29-667a-4057-83c5-6a8dccf84930')
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
            ... print(f"Fetched profile by ID: {fetched_profile.as_dict()}")
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._cbi_base_endpoint}
            /profiles/{profile_id}
        """
        )

        request = self._request_executor.create_request(http_method, api_url)
        response = self._request_executor.execute(request, CBIProfile)
        result = CBIProfile(self.form_response_body(response.get_body()))
        return result

    def add_cbi_profile(self, **kwargs) -> CBIProfile:
        """
        Adds a new cloud browser isolation profile to the Zscaler platform.

        Args:
            name (str): The name of the new cloud browser isolation profile.
            region_ids (list): List of region IDs. Requires at least 2 region IDs.
            certificate_ids (list): List of certificate IDs associated with the profile.

        Keyword Args:
            description (str, optional): A brief description of the security profile.
            is_default (bool, optional): Indicates if this profile should be set as the default for new users.
            banner_id (str, optional): The unique identifier for a custom banner displayed in the isolation session.
            security_controls (dict, optional): Specifies the cloud browser isolation security settings.

                - document_viewer (bool): Enable or disable document viewing capabilities
                - allow_printing (bool): Allow or restrict printing of documents
                - watermark (dict): Configuration for watermarking documents displayed in the browser:
                    - enabled (bool): Enable or disable watermarking
                    - show_user_id (bool): Display user ID on the watermark.
                    - show_timestamp (bool): Include a timestamp in the watermark.
                    - show_message (bool): Include a custom message in the watermark.
                    - message (str): The custom message to display if 'show_message' is True.

                - flattened_pdf (bool): Specify whether PDFs should be flattened.
                - upload_download (str): Control upload and download capabilities ('all', 'none', or other configurations).
                - restrict_keystrokes (bool): Restrict the use of keystrokes within the isolation session.
                - copy_paste (str): Control copy and paste capabilities ('all', 'none', or specific configurations).
                - local_render (bool): Enable or disable local rendering of web content.

            debug_mode (dict, optional): Debug mode settings that may include logging and error tracking configurations.

                - allowed (bool, optional): Allow debug mode
                - file_password (str, Optional): Optional password to debug files when this mode is enabled.

            user_experience (dict, optional): Settings that affect how end-users interact with the isolated browser.

                - forward_to_zia (dict): Configuration for forwarding traffic to ZIA:
                    - enabled (bool): Enable or disable forwarding.
                    - organization_id (str): Organization ID to use for forwarding.
                    - cloud_name (str): Name of the Zscaler cloud.
                    - pac_file_url (str): URL to the PAC file.
                - browser_in_browser (bool): Enable or disable the use of a browser within the isolated browser.
                - persist_isolation_bar (bool): Specify whether the isolation bar should remain visible.
                - session_persistence (bool): Enable or disable session persistence across browser restarts.

        Returns:
            :obj:`Tuple`: A tuple containing the `CBIProfile` instance, response object, and error if any.
        Examples:
            Creating a security profile with required and optional parameters:

            >>> added_profile, _, err = zpa.cbi_profile.add_cbi_profile(
            ...   name='Add_CBI_Profile',
            ...   region_ids=["dc75dc8d-a713-49aa-821e-eb35da523cc2", "1a2cd1bc-b8e0-466b-96ad-fbe44832e1c7"],
            ...   certificate_ids=["87122222-457f-11ed-b878-0242ac120002"],
            ...   description='Description of Add_CBI_Profile',
            ...   security_controls={
            ...       "document_viewer": True,
            ...       "allow_printing": True,
            ...       "watermark": {
            ...           "enabled": True,
            ...           "show_user_id": True,
            ...           "show_timestamp": True,
            ...           "show_message": True,
            ...           "message": "Confidential"
            ...       },
            ...       "flattened_pdf": False,
            ...       "upload_download": "all",
            ...       "restrict_keystrokes": True,
            ...       "copy_paste": "all",
            ...       "local_render": True
            ...   },
            ...   debug_mode={
            ...       "allowed": True,
            ...       "file_password": ""
            ...   },
            ...   user_experience={
            ...       "forward_to_zia": {
            ...           "enabled": True,
            ...           "organization_id": "44772833",
            ...           "cloud_name": "example_cloud",
            ...           "pac_file_url": "https://pac.example_cloud/proxy.pac"
            ...       },
            ...       "browser_in_browser": True,
            ...       "persist_isolation_bar": True,
            ...       "session_persistence": True
            ...   },
            ...   banner_id="97f339f6-9f85-40fb-8b76-f62cdf8f795c"
            ... )
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
            ... print(f"CBI profile added successfully: {added_profile.as_dict()}")
        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._cbi_base_endpoint}
            /profiles
        """
        )

        body = kwargs

        # Validation for required fields: region_ids and certificate_ids
        if not body.get("region_ids") or not isinstance(body.get("region_ids"), list) or len(body.get("region_ids")) < 2:
            raise ValueError("'region_ids' is required and must contain at least 2 region IDs.")

        if not body.get("certificate_ids") or not isinstance(body.get("certificate_ids"), list):
            raise ValueError("'certificate_ids' is required and must be a list.")

        # Proceed with request creation and execution
        request = self._request_executor.create_request(http_method, api_url, body=body)
        response = self._request_executor.execute(request, CBIProfile)
        result = CBIProfile(self.form_response_body(response.get_body()))
        return result

    def update_cbi_profile(self, profile_id: str, **kwargs) -> CBIProfile:
        """
        Updates an existing cloud browser isolation profile.

        Args:
            profile_id (str):
                The unique identifier for the cloud browser isolation profile to be updated.
            **kwargs: Optional keyword args.

        Keyword Args:
            description (str, optional): A brief description of the security profile.
            is_default (bool, optional): Indicates if this profile should be set as the default for new users.
            banner_id (str, optional): The unique identifier for a custom banner displayed in the isolation session.
            security_controls (dict, optional): Specifies the cloud browser isolation security settings.

                - document_viewer (bool): Enable or disable document viewing capabilities
                - allow_printing (bool): Allow or restrict printing of documents
                - watermark (dict): Configuration for watermarking documents displayed in the browser:
                    - enabled (bool): Enable or disable watermarking
                    - show_user_id (bool): Display user ID on the watermark.
                    - show_timestamp (bool): Include a timestamp in the watermark.
                    - show_message (bool): Include a custom message in the watermark.
                    - message (str): The custom message to display if 'show_message' is True.

                - flattened_pdf (bool): Specify whether PDFs should be flattened.
                - upload_download (str): Control upload and download capabilities ('all', 'none', or other configurations).
                - restrict_keystrokes (bool): Restrict the use of keystrokes within the isolation session.
                - copy_paste (str): Control copy and paste capabilities ('all', 'none', or specific configurations).
                - local_render (bool): Enable or disable local rendering of web content.

            debug_mode (dict, optional): Debug mode settings that may include logging and error tracking configurations.

                - allowed (bool, optional): Allow debug mode
                - file_password (str, Optional): Optional password to debug files when this mode is enabled.

            user_experience (dict, optional): Settings that affect how end-users interact with the isolated browser.

                - forward_to_zia (dict): Configuration for forwarding traffic to ZIA:
                    - enabled (bool): Enable or disable forwarding.
                    - organization_id (str): Organization ID to use for forwarding.
                    - cloud_name (str): Name of the Zscaler cloud.
                    - pac_file_url (str): URL to the PAC file.

                - browser_in_browser (bool): Enable or disable the use of a browser within the isolated browser.
                - persist_isolation_bar (bool): Specify whether the isolation bar should remain visible.
                - session_persistence (bool): Enable or disable session persistence across browser restarts.

        Returns:
            :obj:`Tuple`: A tuple containing the `CBIProfile` instance, response object, and error if any.

        Examples:
            Updating the name and description of a cloud browser isolation profile:

            >>> updated_profile, _, err = zpa.cbi_profile.update_cbi_profile(
            ...   profile_id='1beed6be-eb22-4328-92f2-fbe73fd6e5c7',
            ...   name='CBI_Profile_Update'
            ...   description='CBI_Profile_Update'
            )
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
            ... print(f"CBI profile added successfully: {updated_profile.as_dict()}")
        """
        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._cbi_base_endpoint}
            /profiles/{profile_id}
        """
        )

        body = {}

        body.update(kwargs)

        # Validation for required fields: regions, certificates, and banner
        if not body.get("regions") or not isinstance(body.get("regions"), list) or len(body.get("regions")) < 2:
            raise ValueError("'regions' is required and must contain at least 2 region objects.")

        if not body.get("certificates") or not isinstance(body.get("certificates"), list):
            raise ValueError("'certificates' is required and must be a list of certificate objects.")

        if not body.get("banner") or not isinstance(body.get("banner"), dict) or not body["banner"].get("id"):
            raise ValueError("'banner' is required and must contain a valid 'id'.")

        # Proceed with request creation and execution
        request = self._request_executor.create_request(http_method, api_url, body, {})
        response = self._request_executor.execute(request, CBIProfile)
        # Handle case where no content is returned (204 No Content)
        if response is None:
            return CBIProfile({"id": profile_id})

        result = CBIProfile(self.form_response_body(response.get_body()))
        return result

    def delete_cbi_profile(self, profile_id: str) -> None:
        """
        Deletes the specified cloud browser isolation profile.

        Args:
            profile_id (str): The unique identifier of the cloud browser isolation profile.

        Returns:
            :obj:`Tuple`: A tuple containing the response object and error if any.

        Examples:
            >>> try:
            ...     _ = client.zpa.cbi_profile.delete_cbi_profile(
            ...     profile_id='ab73fa29-667a-4057-83c5-6a8dccf84930'
            ... )
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
            ... print(f"CBI Profile with ID {ab73fa29-667a-4057-83c5-6a8dccf84930} deleted successfully.")
        """
        http_method = "delete".upper()
        api_url = format_url(
            f"""
            {self._cbi_base_endpoint}
            /profiles/{profile_id}
        """
        )

        request = self._request_executor.create_request(http_method, api_url)
        response = self._request_executor.execute(request)
        return None
