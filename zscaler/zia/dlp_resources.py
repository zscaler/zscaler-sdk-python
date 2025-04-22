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
from zscaler.zia.models.dlp_resources import DLPICAPServer
from zscaler.zia.models.dlp_resources import DLPIDMProfile
from zscaler.zia.models.dlp_resources import DLPEDMSchema
from zscaler.utils import format_url


class DLPResourcesAPI(APIClient):
    """
    A Client object for other DLP resources.
    """

    _zia_base_endpoint = "/zia/api/v1"

    def __init__(self, request_executor):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def list_dlp_icap_servers(
        self,
        query_params=None,
    ) -> tuple:
        """
        Returns the list of ZIA DLP ICAP Servers.

        Args:
            query_params {dict}: Map of query parameters for the request.
                ``[query_params.search]`` {str}: The search string used to match against a Icap server name attributes.

        Returns:
            tuple: A tuple containing (list of DLP ICAP Server instances, Response, error)

        Example:
            List all dlp icap servers:

            >>> icap_list, response, error = client.zia.dlp_resources.list_dlp_icap_servers()
            ... if error:
            ...    print(f"Error listing dlp icaps: {error}")
            ...    return
            ... print(f"Total icaps found: {len(icap_list)}")
            ... for icap in icap_list:
            ...    print(icap.as_dict())

            filtering dlp icap by name :

            >>> icap_list, response, error = client.dlp_resources.list_dlp_icap_servers(
                query_params={"search": 'ICAP_SERVER01'}
            )
            ... if error:
            ...    print(f"Error listing dlp icaps: {error}")
            ...    return
            ... print(f"Total icaps found: {len(icap_list)}")
            ... for icap in icap_list:
            ...    print(icap.as_dict())

        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /icapServers
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
                results.append(DLPICAPServer(self.form_response_body(item)))
        except Exception as exc:
            return (None, response, exc)

        if local_search:
            lower_search = local_search.lower()
            results = [r for r in results if lower_search in (r.name.lower() if r.name else "")]

        return (results, response, None)

    def list_dlp_icap_servers_lite(
        self,
        query_params=None,
    ) -> tuple:
        """
        Lists name and ID of all ICAP servers.
        If the `search` parameter is provided, the function filters the rules client-side.

        Args:
            query_params {dict}: Map of query parameters for the request.
                ``[query_params.search]`` {str}: The search string used to match against a ICAP servers name.

        Returns:
            tuple: List of ICAP servers resource records.

        Example:
            List all dlp icap servers:

            >>> icap_list, response, error = client.zia.dlp_resources.list_dlp_icap_servers_lite()
            ... if error:
            ...    print(f"Error listing dlp icaps: {error}")
            ...    return
            ... print(f"Total icaps found: {len(icap_list)}")
            ... for icap in icap_list:
            ...    print(icap.as_dict())

            filtering dlp icap by name :

            >>> icap_list, response, error = client.dlp_resources.list_dlp_icap_servers_lite(
                query_params={"search": 'ICAP_SERVER01'}
            )
            ... if error:
            ...    print(f"Error listing dlp icaps: {error}")
            ...    return
            ... print(f"Total icaps found: {len(icap_list)}")
            ... for icap in icap_list:
            ...    print(icap.as_dict())

        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /icapServers/lite
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
                results.append(DLPICAPServer(self.form_response_body(item)))
        except Exception as exc:
            return (None, response, exc)

        if local_search:
            lower_search = local_search.lower()
            results = [r for r in results if lower_search in (r.name.lower() if r.name else "")]

        return (results, response, None)

    def get_dlp_icap_servers(
        self,
        icap_server_id: int,
    ) -> tuple:
        """
        Returns the dlp icap server details for a given DLP ICAP Server.

        Args:
            icap_server_id (str): The unique identifier for the DLP ICAP Server.

        Returns:
            tuple: A tuple containing (DLP Resources instance, Response, error).

        Examples:
            >>> icap = zia.dlp_resources.get_dlp_icap_servers('99999')

        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /icapServers/{icap_server_id}
        """
        )

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)

        if error:
            return (None, response, error)

        try:
            result = DLPICAPServer(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def list_dlp_incident_receiver(
        self,
        query_params=None,
    ) -> tuple:
        """
        Returns the list of ZIA DLP Incident Receiver.

        Args:
            query_params {dict}: Map of query parameters for the request.
                ``[query_params.search]`` {str}: The search string used to match against a Icap server name attributes.

        Returns:
            tuple: A tuple containing (list of DLP Incident Receivers instances, Response, error)

        Example:
            List all incident receivers

            >>> receiver_list, response, error = client.zia.dlp_resources.list_dlp_incident_receiver()
            ... if error:
            ...    print(f"Error listing dlp incident receivers: {error}")
            ...    return
            ... print(f"Total incident receivers found: {len(receiver_list)}")
            ... for receiver in receiver_list:
            ...    print(receiver.as_dict())

            filtering incident receivers by name :

            >>> receiver_list, response, error = client.dlp_resources.list_dlp_incident_receiver(
                query_params={"search": 'ZS_INC_RECEIVER_01'}
            )
            ... if error:
            ...    print(f"Error listing dlp incident receivers: {error}")
            ...    return
            ... print(f"Total incident receivers found: {len(receiver_list)}")
            ... for receiver in receiver_list:
            ...    print(receiver.as_dict())

        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /incidentReceiverServers
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
                results.append(DLPICAPServer(self.form_response_body(item)))
        except Exception as exc:
            return (None, response, exc)

        if local_search:
            lower_search = local_search.lower()
            results = [r for r in results if lower_search in (r.name.lower() if r.name else "")]

        return (results, response, None)

    def list_dlp_incident_receiver_lite(
        self,
        query_params=None,
    ) -> tuple:
        """
        Lists name and ID DLP Incident Receiver.

        Args:
            query_params {dict}: Map of query parameters for the request.
                ``[query_params.search]`` {str}: The search string used to match against a Incident Receiver name attributes.

        Returns:
            tuple: A tuple containing (list of DLP Incident Receivers instances, Response, error)

        Example:
            List all incident receivers

            >>> receiver_list, response, error = client.zia.dlp_resources.list_dlp_incident_receiver_lite()
            ... if error:
            ...    print(f"Error listing dlp incident receivers: {error}")
            ...    return
            ... print(f"Total incident receivers found: {len(receiver_list)}")
            ... for receiver in receiver_list:
            ...    print(receiver.as_dict())

            filtering incident receivers by name :

            >>> receiver_list, response, error = client.dlp_resources.list_dlp_incident_receiver_lite(
                query_params={"search": 'ZS_INC_RECEIVER_01'}
            )
            ... if error:
            ...    print(f"Error listing dlp incident receivers: {error}")
            ...    return
            ... print(f"Total incident receivers found: {len(receiver_list)}")
            ... for receiver in receiver_list:
            ...    print(receiver.as_dict())

        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /incidentReceiverServers/lite
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
                results.append(DLPICAPServer(self.form_response_body(item)))
        except Exception as exc:
            return (None, response, exc)

        if local_search:
            lower_search = local_search.lower()
            results = [r for r in results if lower_search in (r.name.lower() if r.name else "")]

        return (results, response, None)

    def get_dlp_incident_receiver(self, receiver_id: int) -> tuple:
        """
        Returns the dlp incident receiver details for a given DLP Incident Receiver.

        Args:
            receiver_id (str): The unique identifier for the DLP Incident Receiver.

        Returns:
            tuple: A tuple containing (IncidentReceiver instance, Response, error).

        Examples:
            >>> incident_receiver = zia.dlp_resources.get_dlp_incident_receiver('99999')

        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /incidentReceiverServers/{receiver_id}
        """
        )

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)

        if error:
            return (None, response, error)

        try:
            result = DLPICAPServer(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def list_dlp_idm_profiles(
        self,
        query_params=None,
    ) -> tuple:
        """
        Returns the list of ZIA DLP IDM Profiles.

        Args:
            query_params {dict}: Map of query parameters for the request.

                ``[query_params.search]`` {str}: Search string for filtering results.

        Returns:
            tuple: A tuple containing (list of DLP IDM Profile instances, Response, error)

        Examples:
            Print all idm profiles

            >>> for dlp idm in zia.dlp_resources.list_dlp_idm_profiles():
            ...    pprint(idm)

            Print IDM profiles that match the name or description 'IDM_PROFILE_TEMPLATE'

            >>> pprint(zia.dlp_resources.list_dlp_idm_profiles('IDM_PROFILE_TEMPLATE'))

        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /idmprofile
        """
        )

        query_params = query_params or {}

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers, params=query_params)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)

        if error:
            return (None, response, error)

        try:
            result = []
            for item in response.get_results():
                result.append(DLPIDMProfile(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_dlp_idm_profiles(self, profile_id: int) -> tuple:
        """
        Returns the dlp idmp profile details for a given DLP IDM Profile.

        Args:
            icap_server_id (str): The unique identifier for the DLP IDM Profile.

        Returns:
            tuple: A tuple containing (IDM Profiles instance, Response, error).

        Examples:
            >>> idm = zia.dlp_resources.get_dlp_idm_profiles('99999')

        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /idmprofile/{profile_id}
        """
        )

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)

        if error:
            return (None, response, error)

        try:
            result = DLPIDMProfile(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def list_edm_schemas(
        self,
        query_params=None,
    ) -> tuple:
        """
        Returns the list of ZIA DLP Exact Data Match Schemas.

        Args:
            query_params {dict}: Map of query parameters for the request.
                ``[query_params.page]`` {int}: Specifies the page offset.

                ``[query_params.page_size]`` {int}: Specifies the page size.
                    The default size is 100, but the maximum size is 1000.

                ``[query_params.search]`` {str}: Search string for filtering results.

        Returns:
            tuple: A tuple containing (list of DLP EDM Schema instances, Response, error)

        Examples:
            Print all dlp edms

            >>> pprint(zia.dlp_resources.list_edm_schemas())
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /dlpExactDataMatchSchemas
        """
        )

        query_params = query_params or {}

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers, params=query_params)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)

        if error:
            return (None, response, error)

        try:
            result = []
            for item in response.get_results():
                result.append(DLPEDMSchema(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def list_edm_schema_lite(
        self,
        schema_name: str = None,
        active_only: bool = None,
        fetch_tokens: bool = None,
        query_params=None,
    ) -> tuple:
        """
        Returns the list of active EDM templates (or EDM schemas) and their criteria (or token details), only.

        Args:
            schema_name (str): The EDM schema name.
            active_only (bool): If set to true, only active EDM templates (or schemas) are returned in the response.
            fetch_tokens (bool): If set to true, the criteria for the active templates are returned in the response.

        Returns:
            tuple: A tuple containing (list of EDM Schema instances, Response, error)

        Examples:

                Print engines that match the name or description 'ZS_DLP_IDX01'
                >>> pprint(zia.dlp_resources.list_edm_schema_lite(schema_name='ZS_DLP_IDX01'))

                List active EDM schemas with their token details
                >>> pprint(zia.dlp_resources.list_edm_schema_lite(active_only=True, fetch_tokens=True))
        """
        params = {}
        if schema_name is not None:
            params["schemaName"] = schema_name
        if active_only is not None:
            params["activeOnly"] = active_only
        if fetch_tokens is not None:
            params["fetchTokens"] = fetch_tokens

        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /dlpExactDataMatchSchemas/lite
        """
        )

        query_params = query_params or {}

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers, params=query_params)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)

        if error:
            return (None, response, error)

        try:
            result = []
            for item in response.get_results():
                result.append(DLPEDMSchema(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)

        return (result, response, None)
