# -*- coding: utf-8 -*-

# Copyright (c) 2023, Zscaler Inc.
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.


from box import Box, BoxList
from requests import Response

from zscaler.utils import snake_to_camel, recursive_snake_to_camel

from zscaler.zpa.client import ZPAClient


class IsolationAPI:
    def __init__(self, client: ZPAClient):
        self.rest = client

    def list_banners(self: str) -> Box:
        """
        Returns information a list of all cloud browser isolation banners.

        Args:

        Returns:
            :obj:`Box`: The resource record for the cloud browser isolation.

        Examples:
            >>> pprint(zpa.isolation.list_banners())

        """
        return self.rest.get("banners", api_version="cbiconfig_v1")

    def get_banner(self, banner_id: str) -> Box:
        """
        Returns information on the specified cloud browser isolation banner.

        Args:
            profile_id (str):
                The unique identifier for the cloud browser isolation banner.

        Returns:
            :obj:`Box`: The resource record for the cloud browser isolation banner.

        Examples:
            >>> pprint(zpa.isolation.get_banner('99999'))

        """
        return self.rest.get(f"banners/{banner_id}", api_version="cbiconfig_v1")

    def add_banner(self, name: str, banner: bool, **kwargs) -> Box:
        """
        Adds a new cloud browser isolation banner.

        Args:
            name (str):
                The name of the new cloud browser isolation banner.
            logo (str):
                Base64 Logo Image (.jpeg or .png; Maximum file size is 100KB.)

            **kwargs:

        Keyword Args:
            primary_color (str):
                Cloud browser isolation Banner Primary Color
            text_color (str):
                Cloud browser isolation Banner Text Color
            banner (bool):
                Enable Cloud browser isolation banner
            notification_title (str):
                Cloud browser isolation Banner Notification Title
            notification_text (str):
                Cloud browser isolation Banner Notification Text

        Returns:
            :obj:`Box`: The resource record for the newly created Cloud browser isolation.

        Examples:
            Creating a Cloud browser isolation with the minimum required parameters:

            >>> zpa.isolation.add_banner(
            ...     name='new_banner',
            ...     logo= 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAYQAAABQCAMAAAAuu',
            ...     primary_color='#0076BE',
            ...     text_color='#FFFFFF',
            ...     banner=True,
            ...     notification_title='Heads up, you have been redirected to Browser Isolation!',
            ...     notification_text='ZscalerCloud Browser Isolation',
            ...     )
        """

        payload = {
            "name": name,
            "banner": banner,
        }

        # Add optional parameters to payload
        for key, value in kwargs.items():
            payload[snake_to_camel(key)] = value

        response = self.rest.post("banner", json=payload, api_version="cbiconfig_v1")
        if isinstance(response, Response):
            # this is only true when the creation failed (status code is not 2xx)
            status_code = response.status_code
            # Handle error response
            raise Exception(f"API call failed with status {status_code}: {response.json()}")
        return response

    def update_banner(self, banner_id: str, **kwargs) -> Box:
        """
        Updates an existing Cloud browser isolation.

        Args:
            banner_id (str):
                The unique identifier for the Cloud browser isolation to be updated.
            **kwargs: Optional keyword args.

        Keyword Args:
            name (str):
                Cloud browser isolation Theme Name
            primary_color (str):
                Cloud browser isolation Banner Primary Color
            text_color (str):
                Cloud browser isolation Banner Text Color
            banner (bool):
                Enable Cloud browser isolation banner
            notification_title (str):
                Cloud browser isolation Banner Notification Title
            notification_text (str):
                Cloud browser isolation Banner Notification Text

        Returns:
            :obj:`Box`: The resource record for the updated Cloud browser isolation.

        Examples:
            Updating the name of a Cloud browser isolation:

            >>> zpa.isolation.update_banner(
                    banner_id='99999',
            ...    name='updated_name')

        """
        # Set payload to value of existing record
        payload = {snake_to_camel(k): v for k, v in self.get_banner(banner_id).items()}

        # Add optional parameters to payload
        for key, value in kwargs.items():
            payload[snake_to_camel(key)] = value

        resp = self.rest.put(f"banners/{banner_id}", json=payload, api_version="cbiconfig_v1")
        # Return the object if it was updated successfully
        if not isinstance(resp, Response):
            return self.get_banner(banner_id)

    def delete_banner(self, banner_id: str) -> int:
        """
        Deletes the specified Cloud browser isolation.

        Args:
            banner_id (str):
                The unique identifier for the Cloud browser isolation to be deleted.

        Returns:
            :obj:`int`: The response code for the operation.

        Examples:
            >>> zpa.isolation.delete_banner('99999')

        """
        return self.rest.delete(f"banners/{banner_id}", api_version="cbiconfig_v1").status_code

    def list_certificates(self: str) -> Box:
        """
        Returns information on the specified Cloud browser isolation.

        Args:

        Returns:
            :obj:`Box`: The resource record for the Cloud browser isolation.

        Examples:
            >>> pprint(zpa.isolation.list_certificates())

        """
        return self.rest.get("certificates", api_version="cbiconfig_v1")

    def get_certificate(self, certificate_id: str) -> Box:
        """
        Returns information on the specified cloud browser certificate.

        Args:
            certificate_id (str):
                The unique identifier for the cloud browser certificate ID.

        Returns:
            :obj:`Box`: The resource record for the cloud browser certificate.

        Examples:
            >>> pprint(zpa.isolation.get_certificate('99999'))

        """
        return self.rest.get(f"certificates/{certificate_id}", api_version="cbiconfig_v1")

    def add_certificate(self, name, pem: str, **kwargs) -> Box:
        """
        Adds a new Cloud browser isolation.

        Args:
            name (str):
                The name of the new Cloud browser isolation.
            pem (str):
                The content of the certificate in PEM format.

        Returns:
            :obj:`Box`: The resource record for the newly created Cloud browser isolation.

        Examples:
            Creating a Cloud browser isolation with the minimum required parameters:

            >>> zpa.isolation.add_certificate(
            ...   name='new_certificate',
            ...   pem=("-----BEGIN CERTIFICATE-----\\n"
            ...              "nMIIF2DCCA8CgAwIBAgIBATANBgkqhkiG==\\n"
            ...              "-----END CERTIFICATE-----"),
            )

        """

        payload = {
            "name": name,
            "pem": pem,
        }

        # Add optional parameters to payload
        for key, value in kwargs.items():
            payload[snake_to_camel(key)] = value

        response = self.rest.post("certificate", json=payload, api_version="cbiconfig_v1")
        if isinstance(response, Response):
            # this is only true when the creation failed (status code is not 2xx)
            status_code = response.status_code
            # Handle error response
            raise Exception(f"API call failed with status {status_code}: {response.json()}")
        return response

    def update_certificate(self, certificate_id: str, **kwargs) -> Box:
        """
        Updates an existing cloud browser isolation certificate.

        Args:
            certificate_id (str):
                The unique identifier for the cloud browser isolation certificate to be updated.
            name (str):
                The name of the new cloud browser isolation certificate.
            pem (str):
                The content of the certificate in PEM format.

        Returns:
            :obj:`Box`: The resource record for the updated Cloud browser isolation.

        Examples:
            Updating the name of a Cloud browser isolation:

            >>> zpa.isolation.update_certificate(
            ...   name='new_certificate',
            ...   pem=("-----BEGIN CERTIFICATE-----\\n"
            ...              "MIIFNzCCBIHNIHIO==\\n"
            ...              "-----END CERTIFICATE-----"),
            )
        """
        # Set payload to value of existing record
        payload = {snake_to_camel(k): v for k, v in self.get_certificate(certificate_id).items()}

        # Add optional parameters to payload
        for key, value in kwargs.items():
            payload[snake_to_camel(key)] = value

        resp = self.rest.put(f"certificates/{certificate_id}", json=payload, api_version="cbiconfig_v1")
        # Return the object if it was updated successfully
        if not isinstance(resp, Response):
            return self.get_certificate(certificate_id)

    def delete_certificate(self, certificate_id: str) -> int:
        """
        Deletes the specified cloud browser isolation certificate.

        Args:
            certificate_id (str):
                The unique identifier for the Cloud browser isolation to be deleted.

        Returns:
            :obj:`int`: The response code for the operation.

        Examples:
            >>> zpa.isolation.delete_certificate('99999')

        """
        return self.rest.delete(f"certificates/{certificate_id}", api_version="cbiconfig_v1").status_code

    def list_profiles(self, **kwargs) -> BoxList:
        """
        Returns a list of all configured isolation profiles.

        Keyword Args:
            max_items (int): The maximum number of items to request before stopping iteration.
            max_pages (int): The maximum number of pages to request before stopping iteration.
            pagesize (int): Specifies the page size. The default size is 20, but the maximum size is 500.
            search (str, optional): The search string used to match against features and fields.

        Returns:
            BoxList: A list of all configured isolation profiles.

        Examples:
            >>> for isolation_profile in zpa.isolation_profiles.list_profiles():
            ...     pprint(isolation_profile)
        """
        list, _ = self.rest.get_paginated_data(path="/isolation/profiles", **kwargs)
        return list

    def get_profile_by_name(self, name: str):
        """
        Retrieves a specific isolation profile by its name.

        Args:
            name (str): The name of the isolation profile to search for.

        Returns:
            dict or None: The isolation profile with the specified name if found, otherwise None.

        Examples:
            >>> profile = zpa.isolation_profiles.get_profile_by_name('DefaultProfile')
            >>> print(profile)
        """
        profiles = self.list_profiles()
        for profile in profiles:
            if profile.get("name") == name:
                return profile
        return None

    def get_profile_by_id(self, profile_id: str):
        """
        Retrieves a specific isolation profile by its unique identifier (ID).

        Args:
            profile_id (str): The ID of the isolation profile to retrieve.

        Returns:
            dict or None: The isolation profile with the specified ID if found, otherwise None.

        Examples:
            >>> profile = zpa.isolation_profiles.get_profile_by_id('12345')
            >>> print(profile)
        """
        profiles = self.list_profiles()
        for profile in profiles:
            if str(profile.get("id")) == str(profile_id):  # Ensuring ID comparison as strings
                return profile
        return None

    def list_cbi_profiles(self) -> Box:
        """
        Returns information on the specified Cloud browser isolation.

        Args:

        Returns:
            :obj:`Box`: The resource record for the Cloud browser isolation.

        Examples:
            >>> pprint(zpa.isolation.list_cbi_profiles())

        """
        return self.rest.get("profiles", api_version="cbiconfig_v1")

    def get_cbi_profile(self, profile_id: str) -> Box:
        """
        Returns information on the specified cloud browser isolation certificate.

        Args:
            profile_id (str):
                The unique identifier for the cloud browser isolation certificate ID.

        Returns:
            :obj:`Box`: The resource record for the cloud browser isolation certificate.

        Examples:
            >>> pprint(zpa.isolation.get_cbi_profile('99999'))

        """
        return self.rest.get(f"profiles/{profile_id}", api_version="cbiconfig_v1")

    def add_cbi_profile(self, name: str, region_ids, certificate_ids: list, **kwargs) -> Box:
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
            :obj:`Box`: The resource record for the newly created Cloud browser isolation profile.

        Examples:
            Creating a security profile with required and optional parameters:

            >>> zpa.isolation.add_cbi_profile(
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
        """
        payload = {
            "name": name,
            "region_ids": region_ids,
            "certificate_ids": certificate_ids,
        }

        # Add optional parameters to payload if provided
        for key, value in kwargs.items():
            if value is not None:
                payload[key] = value  # Keep in snake_case initially

        # Convert the entire payload from snake_case to camelCase
        payload = recursive_snake_to_camel(payload)

        response = self.rest.post("profiles", json=payload, api_version="cbiconfig_v1")
        if isinstance(response, Response) and response.status_code != 200:
            # Assume non-200 responses indicate failure
            raise Exception(f"API call failed with status {response.status_code}: {response.json()}")
        return response

    def update_cbi_profile(self, profile_id: str, **kwargs) -> Box:
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
            :obj:`Box`: The resource record for the updated cloud browser isolation profile.

        Examples:
            Updating the name and description of a cloud browser isolation profile:

            >>> zpa.isolation.update_cbi_profile(
            ...   profile_id='1beed6be-eb22-4328-92f2-fbe73fd6e5c7',
            ...   name='CBI_Profile_Update'
            ...   description='CBI_Profile_Update'
            )
        """
        current_profile_data = self.get_cbi_profile(profile_id)
        if isinstance(current_profile_data, Response):
            raise Exception(f"Failed to retrieve profile with ID {profile_id}: {current_profile_data.json()}")

        for key, value in kwargs.items():
            current_profile_data[key] = value
        updated_payload = recursive_snake_to_camel(current_profile_data)

        response = self.rest.put(f"profiles/{profile_id}", json=updated_payload, api_version="cbiconfig_v1")
        if isinstance(response, Response) and response.status_code != 200:
            raise Exception(f"API call failed with status {response.status_code}: {response.json()}")
        return self.get_cbi_profile(profile_id)

    def delete_cbi_profile(self, profile_id: str) -> int:
        """
        Deletes the specified cloud browser isolation profile.

        Args:
            profile_id (str):
                The unique identifier for the cloud browser isolation profile to be deleted.

        Returns:
            :obj:`int`: The response code for the operation.

        Examples:
            >>> zpa.isolation.delete_cbi_profile('99999')

        """
        return self.rest.delete(f"profiles/{profile_id}", api_version="cbiconfig_v1").status_code

    def list_zpa_profiles(self, show_disabled=None, scope_id=None) -> Box:
        """
        Returns a list of all cloud browser isolation zpa profiles, with options to filter by disabled status and scope.

        Args:
            show_disabled (bool, optional): If set to True, the response includes disabled profiles.
            scope_id (str, optional): The unique identifier of the scope of the tenant to filter the profiles.

        Returns:
            :obj:`Box`: The resource record for the cloud browser isolation zpa profiles.

        Examples:
            >>> pprint(zpa.isolation.list_zpa_profiles())
            >>> pprint(zpa.isolation.list_zpa_profiles(show_disabled=True, scope_id="abc123"))

        """
        params = {}
        if show_disabled is not None:
            params["showDisabled"] = show_disabled
        if scope_id is not None:
            params["scopeId"] = scope_id

        return self.rest.get("zpaprofiles", params=params, api_version="cbiconfig_v1")

    def get_zpa_profile(self, cbi_profile_id: str) -> Box:
        """
        Returns information on the specified cloud browser isolation profile based on the cbi_profile_id.

        Args:
            cbi_profile_id (str):
                The unique identifier for the cloud browser isolation profile.

        Returns:
            :obj:`Box`: The resource record for the cloud browser isolation profile.

        Examples:
            >>> pprint(zpa.isolation.get_zpa_profile('055e0730-cb6b-486f-804d-448024d22d91'))

        """
        profiles = self.list_zpa_profiles()
        for profile in profiles:
            if profile.get("cbi_profile_id") == cbi_profile_id:
                return Box(profile)
        raise ValueError("Profile with ID {} not found".format(cbi_profile_id))

    def list_regions(self: str) -> Box:
        """
        Returns information a list of all cloud browser isolation regions.

        Args:

        Returns:
            :obj:`Box`: The resource record for the cloud browser isolation regions.

        Examples:
            >>> pprint(zpa.isolation.list_regions())

        """
        return self.rest.get("regions", api_version="cbiconfig_v1")

    def get_region(self, region_id: str) -> Box:
        """
        Returns information on the specified cloud browser isolation region by ID.

        Args:
            region_id (str): The unique identifier for the cloud browser isolation region.

        Returns:
            :obj:`Box`: The resource record for the cloud browser isolation region.

        Examples:
            >>> pprint(zpa.isolation.get_region('dc75dc8d-a713-49aa-821e-eb35da523cc2'))

        """
        regions = self.list_regions()
        for region in regions:
            if region["id"] == region_id:
                return Box(region)
        raise ValueError(f"Region with ID {region_id} not found")
