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
from zscaler.api_client import APIClient
from zscaler.zia.models.tenancy_restriction_profile import TenancyRestrictionProfile
from zscaler.utils import format_url

class TenancyRestrictionProfileAPI(APIClient):

    _zia_base_endpoint = "/zia/api/v1"

    def __init__(self, request_executor):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def list_restriction_profile(
        self,
        query_params=None,
    ) -> tuple:
        """
        Retrieves all the restricted tenant profiles.

        Args:
            query_params {dict}: Map of query parameters for the request.

                ``[query_params.instance_name]`` {str}: The restricted tenant profile name

                ``[query_params.instance_type]`` {bool}: The restricted tenant profile type
                    Supported values: `SHAREPOINTONLINE`, `ONEDRIVE`, `BOXNET`, `OKTA`, `APPSPACE`,
                        `BITBUCKET`, `GITHUB`, `SLACK`, `QUICK_BASE`, `ZEPLIN`, `SOURCEFORGE`, `ZOOM`,
                        `WORKDAY`, `GDRIVE`, `GOOGLE_WEBMAIL`, `WINDOWS_LIVE_HOTMAIL`, `MSTEAM"

                ``[query_params.page]`` (int): Specifies the page offset.

                ``[query_params.page_size]`` (int): Specifies the page size. The default size is 255.

        Returns:
            tuple: A tuple containing (list of Device Group instances, Response, error)

        Examples:
            Print all device groups

            >>> for device group in zia.device_management.list_device_groups():
            ...    pprint(device)

            Print Device Groups that match the name or description 'Windows'

            >>> pprint(zia.device_management.list_device_groups('Windows'))

        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /tenancyRestrictionProfile
        """
        )

        query_params = query_params or {}

        local_search = query_params.pop("search", None)

        body = {}
        headers = {}

        request, error = self._request_executor.\
            create_request(http_method, api_url, body, headers, params=query_params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        try:
            results = []
            for item in response.get_results():
                results.append(TenancyRestrictionProfile(
                    self.form_response_body(item))
                )
        except Exception as exc:
            return (None, response, exc)

        if local_search:
            lower_search = local_search.lower()
            results = [r for r in results if lower_search in (r.name.lower() if r.name else "")]

        return (results, response, None)
    
    def get_restriction_profile(self, profile_id: int) -> tuple:
        """
        Retrieves the restricted tenant profile based on the specified ID

        Args:
            profile_id (int): The unique identifier for the restricted tenant profile.

        Returns:
            tuple: A tuple containing (restricted tenant profile, Response, error).
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /tenancyRestrictionProfile/{profile_id}
        """
        )

        body = {}
        headers = {}

        request, error = self._request_executor.\
            create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor.\
            execute(request, TenancyRestrictionProfile)
        if error:
            return (None, response, error)

        try:
            result = TenancyRestrictionProfile(
                self.form_response_body(response.get_body())
            )
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def add_restriction_profile(self, **kwargs) -> tuple:
        """
        Creates restricted tenant profiles.

        Args:
            id(str): restricted tenant profile ID
            name (str): Tenant profile name
            description (str): Additional information about the profile

            app_type (str): Restricted tenant profile application type
                Supported Values: `YOUTUBE`, `GOOGLE`, `MSLOGINSERVICES`, `SLACK`, `BOX`,
                    `FACEBOOK`, `AWS`, `DROPBOX`, `WEBEX_LOGIN_SERVICES`, 
                    `AMAZON_S3`, `ZOHO_LOGIN_SERVICES`, `GOOGLE_CLOUD_PLATFORM`,
                    `ZOOM`, `IBMSMARTCLOUD`, `GITHUB`, `CHATGPT_AI`

            item_type_primary (str): Tenant profile primary item type
                Supported Values: `TENANT_RESTRICTION_TEAM_ID`, `TENANT_RESTRICTION_ALLOWED_WORKSPACE_ID`,
                    `TENANT_RESTRICTION_DOMAIN`, `TENANT_RESTRICTION_TENANT_NAME`,
                    `TENANT_RESTRICTION_TENANT_DIRECTORY`, `TENANT_RESTRICTION_CHANNEL_ID`,
                    `TENANT_RESTRICTION_CATEGORY_ID`, `TENANT_RESTRICTION_SCHOOL_ID`,
                    `TENANT_RESTRICTION_REQUEST_WORKSPACE_ID`, `TENANT_RESTRICTION_EXP_BUCKET_OWNERID`,
                    `TENANT_RESTRICTION_EXP_BUCKET_SRC_OWNERID`, `TENANT_RESTRICTION_RESTRICT_MSA`,
                    `TENANT_RESTRICTION_TENANT_POLICY_ID`, `TENANT_RESTRICTION_ACCOUNT_ID`,
                    `TENANT_RESTRICTION_TENANT_ORG_ID`, `TENANT_RESTRICTION_POLICY_LABEL`,
                    `TENANT_RESTRICTION_ENTERPRISE_SLUG`, `TENANT_RESTRICTION_WORKSPACE_ID`

            item_data_primary (list): Tenant profile primary item data

            item_type_secondary (str): Tenant profile secondary item type
                Supported Values: `TENANT_RESTRICTION_TEAM_ID`, `TENANT_RESTRICTION_ALLOWED_WORKSPACE_ID`,
                    `TENANT_RESTRICTION_DOMAIN`, `TENANT_RESTRICTION_TENANT_NAME`,
                    `TENANT_RESTRICTION_TENANT_DIRECTORY`, `TENANT_RESTRICTION_CHANNEL_ID`,
                    `TENANT_RESTRICTION_CATEGORY_ID`, `TENANT_RESTRICTION_SCHOOL_ID`,
                    `TENANT_RESTRICTION_REQUEST_WORKSPACE_ID`, `TENANT_RESTRICTION_EXP_BUCKET_OWNERID`,
                    `TENANT_RESTRICTION_EXP_BUCKET_SRC_OWNERID`, `TENANT_RESTRICTION_RESTRICT_MSA`,
                    `TENANT_RESTRICTION_TENANT_POLICY_ID`, `TENANT_RESTRICTION_ACCOUNT_ID`,
                    `TENANT_RESTRICTION_TENANT_ORG_ID`, `TENANT_RESTRICTION_POLICY_LABEL`,
                    `TENANT_RESTRICTION_ENTERPRISE_SLUG`, `TENANT_RESTRICTION_WORKSPACE_ID`

            item_data_secondary (list): Tenant profile secondary item data
            item_value (list): Tenant profile item value for YouTube category
                Supported Values: `TENANT_RESTRICTION_FILM_AND_ANIMATION`, `TENANT_RESTRICTION_AUTOS_AND_VEHICLES`,
                    `TENANT_RESTRICTION_MUSIC`, `TENANT_RESTRICTION_PETS_AND_ANIMALS`,
                    `TENANT_RESTRICTION_SPORTS`, `TENANT_RESTRICTION_SHORT_MOVIES`,
                    `TENANT_RESTRICTION_TRAVEL_AND_EVENTS`, `TENANT_RESTRICTION_GAMING`,
                    `TENANT_RESTRICTION_VIDEOBLOGGING`, `TENANT_RESTRICTION_PEOPLE_AND_BLOGS`,
                    `TENANT_RESTRICTION_COMEDY`, `TENANT_RESTRICTION_ENTERTAINMENT`,
                    `TENANT_RESTRICTION_NEWS_AND_POLITICS`, `TENANT_RESTRICTION_HOWTO_AND_STYLE`,
                    `TENANT_RESTRICTION_EDUCATION`, `TENANT_RESTRICTION_SCIENCE_AND_TECHNOLOGY`,
                    `TENANT_RESTRICTION_MOVIES`, `TENANT_RESTRICTION_ANIME_OR_ANIMATION`,
                    `TENANT_RESTRICTION_ACTION_OR_ADVENTURE`, `TENANT_RESTRICTION_CLASSICS`,
                    `TENANT_RESTRICTION_DOCUMENTARY`, `TENANT_RESTRICTION_DRAMA`,
                    `TENANT_RESTRICTION_FAMILY`, `TENANT_RESTRICTION_FOREIGN`,
                    `TENANT_RESTRICTION_HORROR`, `TENANT_RESTRICTION_SCIFI_OR_FANTASY`,
                    `TENANT_RESTRICTION_THRILLER`, `TENANT_RESTRICTION_SHORTS`,
                    `TENANT_RESTRICTION_SHOWS`,`TENANT_RESTRICTION_TRAILERS`,
                    `TENANT_RESTRICTION_NONPROFITS_AND_ACTIVISM`
            restrict_personal_o365_domains: (bool): Flag to restrict personal domains for Office 365
            allow_google_consumers: (bool): Flag to allow Google consumers
            ms_login_services_trv2: (bool): Flag to decide between v1 and v2 for tenant restriction on MSLOGINSERVICES
            allow_google_visitors: (bool): Flag to allow Google visitors
            allow_gcp_cloud_storage_read: (bool): Flag to allow or disallow cloud storage resources for GCP
                     
        Returns:
            tuple: A tuple containing the newly added restricted tenant profile, response, and error.
        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /tenancyRestrictionProfile
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

        response, error = self._request_executor.\
            execute(request, TenancyRestrictionProfile)
        if error:
            return (None, response, error)

        try:
            result = TenancyRestrictionProfile(
                self.form_response_body(response.get_body())
            )
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_restriction_profile(self, profile_id: int, **kwargs) -> tuple:
        """
        Updates the restricted tenant profile based on the specified ID

        Args:
            profile_id (int): The unique ID for the restricted tenant profile

        Returns:
            tuple: A tuple containing the updated restricted tenant profile, response, and error.
        """
        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /tenancyRestrictionProfile/{profile_id}
        """
        )
        body = {}

        body.update(kwargs)

        request, error = self._request_executor.\
            create_request(http_method, api_url, body, {}, {})
        if error:
            return (None, None, error)

        response, error = self._request_executor.\
            execute(request, TenancyRestrictionProfile)
        if error:
            return (None, response, error)

        try:
            result = TenancyRestrictionProfile(
                self.form_response_body(response.get_body())
            )
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def delete_restriction_profile(self, profile_id: int) -> tuple:
        """
        Deletes a restricted tenant profile based on the specified ID

        Args:
            instance_id (str): The unique identifier of the restricted tenant profile.

        Returns:
            tuple: A tuple containing the response object and error (if any).
        """
        http_method = "delete".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /tenancyRestrictionProfile/{profile_id}
        """
        )

        params = {}

        request, error = self._request_executor.\
            create_request(http_method, api_url, params=params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)
        return (None, response, None)

    def list_app_item_count(
        self,
        app_type: str,
        item_type: str,
    ) -> tuple:
        """
        Retrieves the item count of the specified item type for a given application, excluding any specified profile

        Args:
            **app_type (str): The type of rule for which actions should be retrieved.
                Supported Values: `YOUTUBE`, `GOOGLE`, `MSLOGINSERVICES`, `SLACK`,
                    `BOX`, `FACEBOOK`, `AWS`, `DROPBOX`, `WEBEX_LOGIN_SERVICES`,
                    `AMAZON_S3`,`ZOHO_LOGIN_SERVICES`, `GOOGLE_CLOUD_PLATFORM`,
                    `ZOOM`, `IBMSMARTCLOUD`, `GITHUB`,`CHATGPT_AI`
            **item_type (str): Item type
                Supported Values: `TENANT_RESTRICTION_TEAM_ID`, `TENANT_RESTRICTION_ALLOWED_WORKSPACE_ID`,
                    `TENANT_RESTRICTION_DOMAIN`, `TENANT_RESTRICTION_TENANT_NAME`,
                    `TENANT_RESTRICTION_TENANT_DIRECTORY`, `TENANT_RESTRICTION_CHANNEL_ID`,
                    `TENANT_RESTRICTION_CATEGORY_ID`, `TENANT_RESTRICTION_SCHOOL_ID`,
                    `TENANT_RESTRICTION_REQUEST_WORKSPACE_ID`, `TENANT_RESTRICTION_EXP_BUCKET_OWNERID`,
                    `TENANT_RESTRICTION_EXP_BUCKET_SRC_OWNERID`, `TENANT_RESTRICTION_RESTRICT_MSA`,
                    `TENANT_RESTRICTION_TENANT_POLICY_ID`, `TENANT_RESTRICTION_ACCOUNT_ID`,
                    `TENANT_RESTRICTION_TENANT_ORG_ID`, `TENANT_RESTRICTION_POLICY_LABEL`,
                    `TENANT_RESTRICTION_ENTERPRISE_SLUG`, `TENANT_RESTRICTION_WORKSPACE_ID`
            **exclude_profile (int): Specifies the profile ID that is excluded from the item count calculation

        Returns:
            tuple: A tuple containing:
                - result (list): A list of actions supported for the given rule type.
                - response (object): The full API response object.
                - error (object): Any error encountered during the request.

        Examples:
            Retrieve available actions for a specific rule type:
                >>> actions, response, error = zia.tenancy_restriction_profile.list_app_item_count(
                    query_params=
                ... )
                >>> if actions:
                ...     for action in actions:
                ...         print(action)
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /tenancyRestrictionProfile/app-item-count/{app_type}/{item_type}
            """
        )

        # body = {"cloudApps": cloud_apps}

        request, error = self._request_executor.\
            create_request(http_method, api_url, {}, {})

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)

        if error:
            return (None, response, error)

        try:
            result = response.get_body()
            if not isinstance(result, list):
                raise ValueError("Unexpected response format: Expected a list.")
        except Exception as error:
            return (None, response, error)

        return (result, response, None)