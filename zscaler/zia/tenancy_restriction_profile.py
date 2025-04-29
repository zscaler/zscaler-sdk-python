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

                ``[query_params.search]`` {str}: Search string for filtering results.

        Returns:
            tuple: A tuple containing (list of Tenancy Restiction Profiles, Response, error)

        Examples:
            Print all Tenancy Restiction Profiles

            >>> profile_list, _, error = client.zia.tenancy_restriction_profile.list_restriction_profile()
            >>> if error:
            ...     print(f"Error listing Tenancy Restiction Profiles: {error}")
            ...     return
            ... print(f"Total Tenancy Restiction Profiles found: {len(profile_list)}")
            ... for profile in profile_list:
            ...     print(profile.as_dict())
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

        request, error = self._request_executor.create_request(http_method, api_url, body, headers, params=query_params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        try:
            results = []
            for item in response.get_results():
                results.append(TenancyRestrictionProfile(self.form_response_body(item)))
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

        Examples:
            Print a specific Tenancy Restriction Profile

            >>> fetched_profile, _, error = client.zia.tenancy_restriction_profile.get_restriction_profile(
                '1254654')
            >>> if error:
            ...     print(f"Error fetching Tenancy Restriction Profile by ID: {error}")
            ...     return
            ... print(f"Fetched Tenancy Restriction Profile by ID: {fetched_profile.as_dict()}")
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

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, TenancyRestrictionProfile)
        if error:
            return (None, response, error)

        try:
            result = TenancyRestrictionProfile(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def add_restriction_profile(self, **kwargs) -> tuple:
        """
        Creates restricted tenant profiles.

        Args:
            id (str): Restricted tenant profile ID.
            name (str): Tenant profile name.
            description (str): Additional information about the profile.
            app_type (str): Application type.
                Supported values: `YOUTUBE`, `GOOGLE`, `MSLOGINSERVICES`, `SLACK`, `BOX`,
                `FACEBOOK`, `AWS`, `DROPBOX`, `WEBEX_LOGIN_SERVICES`, `AMAZON_S3`,
                `ZOHO_LOGIN_SERVICES`, `GOOGLE_CLOUD_PLATFORM`, `ZOOM`, `IBMSMARTCLOUD`,
                `GITHUB`, `CHATGPT_AI`.
            item_type_primary (str): Primary item type for the profile.
                Supported values: `TENANT_RESTRICTION_TEAM_ID`, `TENANT_RESTRICTION_ALLOWED_WORKSPACE_ID`,
                `TENANT_RESTRICTION_DOMAIN`, `TENANT_RESTRICTION_TENANT_NAME`,
                `TENANT_RESTRICTION_TENANT_DIRECTORY`, `TENANT_RESTRICTION_CHANNEL_ID`,
                `TENANT_RESTRICTION_CATEGORY_ID`, `TENANT_RESTRICTION_SCHOOL_ID`,
                `TENANT_RESTRICTION_REQUEST_WORKSPACE_ID`, `TENANT_RESTRICTION_EXP_BUCKET_OWNERID`,
                `TENANT_RESTRICTION_EXP_BUCKET_SRC_OWNERID`, `TENANT_RESTRICTION_RESTRICT_MSA`,
                `TENANT_RESTRICTION_TENANT_POLICY_ID`, `TENANT_RESTRICTION_ACCOUNT_ID`,
                `TENANT_RESTRICTION_TENANT_ORG_ID`, `TENANT_RESTRICTION_POLICY_LABEL`,
                `TENANT_RESTRICTION_ENTERPRISE_SLUG`, `TENANT_RESTRICTION_WORKSPACE_ID`.
            item_data_primary (list): Primary item data.
            item_type_secondary (str): Secondary item type for the profile.
                Supported values: Same as item_type_primary.
            item_data_secondary (list): Secondary item data.
            item_value (list): Tenant profile item value for YouTube categories.
                Supported values: `TENANT_RESTRICTION_FILM_AND_ANIMATION`, `TENANT_RESTRICTION_AUTOS_AND_VEHICLES`,
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
                `TENANT_RESTRICTION_SHOWS`, `TENANT_RESTRICTION_TRAILERS`,
                `TENANT_RESTRICTION_NONPROFITS_AND_ACTIVISM`.
            restrict_personal_o365_domains (bool): Flag to restrict personal domains for Office 365.
            allow_google_consumers (bool): Flag to allow Google consumers.
            ms_login_services_trv2 (bool): Flag to choose between v1 and v2 for MS Login services.
            allow_google_visitors (bool): Flag to allow Google visitors.
            allow_gcp_cloud_storage_read (bool): Flag to allow or disallow GCP cloud storage reads.

        Returns:
            tuple: A tuple containing:
                - The newly added restricted tenant profile.
                - The HTTP response.
                - Any error message encountered.

        Examples:
            Add a new restricted tenant profile

            >>> added_tenancy, _, error = client.zia.tenancy_restriction_profile.add_restriction_profile(
            ...     name=f"UpdateMSProfile01_{random.randint(1000, 10000)}",
            ...     description=f"UpdateMSProfile01_{random.randint(1000, 10000)}",
            ...     restrict_personal_o365_domains=False,
            ...     app_type='MSLOGINSERVICES',
            ...     item_type_primary='TENANT_RESTRICTION_TENANT_DIRECTORY',
            ...     item_data_primary=["76b66e9c-201a-49dc-bb7e-e9d77604a4c2"],
            ...     item_type_secondary="TENANT_RESTRICTION_TENANT_NAME",
            ...     item_data_secondary=[ "securitygeek.dev", "securitygeekio.ca"]
            ... )
            >>> if error:
            ...     print(f"Error adding tenancy restriction profile: {error}")
            ...     return
            ... print(f"tenancy restriction profile added successfully: {added_tenancy.as_dict()}")
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

        response, error = self._request_executor.execute(request, TenancyRestrictionProfile)
        if error:
            return (None, response, error)

        try:
            result = TenancyRestrictionProfile(self.form_response_body(response.get_body()))
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

        Examples:
            Update a restricted tenant profile

            >>> updated_tenancy, _, error = client.zia.tenancy_restriction_profile.update_restriction_profile(
            ...     profile_id=added_tenancy.id,
            ...     name=f"UpdateMSProfile01_{random.randint(1000, 10000)}",
            ...     description=f"UpdateMSProfile01_{random.randint(1000, 10000)}",
            ...     restrict_personal_o365_domains=False,
            ...     app_type='MSLOGINSERVICES',
            ...     item_type_primary='TENANT_RESTRICTION_TENANT_DIRECTORY',
            ...     item_data_primary=["76b66e9c-201a-49dc-bb7e-e9d77604a4c2"],
            ...     item_type_secondary="TENANT_RESTRICTION_TENANT_NAME",
            ...     item_data_secondary=[ "securitygeek.dev", "securitygeekio.ca"]
            ... )
            >>> if error:
            ...     print(f"Error updating tenancy restriction profile: {error}")
            ...     return
            ... print(f"tenancy restriction profile updated successfully: {updated_tenancy.as_dict()}")
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

        request, error = self._request_executor.create_request(http_method, api_url, body, {}, {})
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, TenancyRestrictionProfile)
        if error:
            return (None, response, error)

        try:
            result = TenancyRestrictionProfile(self.form_response_body(response.get_body()))
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

        Examples:
            Delete a specific Tenant Restriction Profile

            >>> _, _, error = client.zia.tenancy_restriction_profile.delete_restriction_profile(
                '1254654')
            >>> if error:
            ...     print(f"Error deleting Tenant Restriction Profile: {error}")
            ...     return
            ... print(f"Tenant Restriction Profile with ID {'1254654'} deleted successfully.")
        """
        http_method = "delete".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /tenancyRestrictionProfile/{profile_id}
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

    def list_app_item_count(
        self,
        app_type: str,
        item_type: str,
    ) -> tuple:
        """
        Retrieves the item count of the specified item type for a given application, excluding any specified profile.

        Args:
            app_type (str): The type of application for which item count is retrieved.
                Supported values: YOUTUBE, GOOGLE, MSLOGINSERVICES, SLACK,
                BOX, FACEBOOK, AWS, DROPBOX, WEBEX_LOGIN_SERVICES,
                AMAZON_S3, ZOHO_LOGIN_SERVICES, GOOGLE_CLOUD_PLATFORM,
                ZOOM, IBMSMARTCLOUD, GITHUB, CHATGPT_AI.
            item_type (str): The item type to retrieve the count for.
                Supported values: TENANT_RESTRICTION_TEAM_ID, TENANT_RESTRICTION_ALLOWED_WORKSPACE_ID,
                TENANT_RESTRICTION_DOMAIN, TENANT_RESTRICTION_TENANT_NAME,
                TENANT_RESTRICTION_TENANT_DIRECTORY, TENANT_RESTRICTION_CHANNEL_ID,
                TENANT_RESTRICTION_CATEGORY_ID, TENANT_RESTRICTION_SCHOOL_ID,
                TENANT_RESTRICTION_REQUEST_WORKSPACE_ID, TENANT_RESTRICTION_EXP_BUCKET_OWNERID,
                TENANT_RESTRICTION_EXP_BUCKET_SRC_OWNERID, TENANT_RESTRICTION_RESTRICT_MSA,
                TENANT_RESTRICTION_TENANT_POLICY_ID, TENANT_RESTRICTION_ACCOUNT_ID,
                TENANT_RESTRICTION_TENANT_ORG_ID, TENANT_RESTRICTION_POLICY_LABEL,
                TENANT_RESTRICTION_ENTERPRISE_SLUG, TENANT_RESTRICTION_WORKSPACE_ID.
            exclude_profile (int, optional): Profile ID to exclude from the item count calculation.

        Returns:
            tuple: A tuple containing:
                - list: List of item counts matching the application and item type.
                - Response: The full API response object.
                - error: Any error encountered during the request.

        Examples:
            Retrieve item counts for a specific app type:

            >>> items, response, error = zia.tenancy_restriction_profile.list_app_item_count(
            ...     app_type="GOOGLE",
            ...     item_type="TENANT_RESTRICTION_DOMAIN"
            ... )
            >>> if items:
            ...     for item in items:
            ...         print(item)
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /tenancyRestrictionProfile/app-item-count/{app_type}/{item_type}
            """
        )

        # body = {"cloudApps": cloud_apps}

        request, error = self._request_executor.create_request(http_method, api_url, {}, {})

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
