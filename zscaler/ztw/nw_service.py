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
from zscaler.ztw.models.nw_service import NetworkServices
from zscaler.utils import format_url


class NWServiceAPI(APIClient):

    _ztw_base_endpoint = "/ztw/api/v1"

    def __init__(self, request_executor):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def list_network_services(self, query_params=None) -> tuple:
        """
        Lists network services in your organization with pagination.
        A subset of network services  can be returned that match a supported
        filter expression or query.

        Args:
            query_params {dict}: Map of query parameters for the request.
                ``[query_params.protocol]`` {str}: Filter based on the network service protocol.
                Supported Values: `ICMP`, `TCP`, `UDP`, `GRE`, `ESP`, `OTHER`,

                ``[query_params.search]`` {str}: The search string used to match against a service's name or description attributes.

                ``[query_params.locale]`` (str): When set to one of the supported locales (e.g., ``en-US``, ``de-DE``,
                    ``es-ES``, ``fr-FR``, ``ja-JP``, ``zh-CN``), the network application
                    description is localized into the requested language.
        Returns:
            tuple: A tuple containing (list of network services instances, Response, error)

        Examples:
            Gets a list of all network services.

            >>> service_list, response, error = ztw.nw_service.list_network_services():
            ... if error:
            ...     print(f"Error listing network services: {error}")
            ...     return
            ... print(f"Total network services found: {len(service_list)}")
            ... for service in service_list:
            ...     print(service.as_dict())

            Gets a list of all network services.

            >>> service_list, response, error = ztw.nw_service.list_network_services(query_params={"search": 'FTP'}):
            ... if error:
            ...     print(f"Error listing network services: {error}")
            ...     return
            ... print(f"Total services found: {len(service_list)}")
            ... for service in service_list:
            ...     print(service.as_dict())

        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._ztw_base_endpoint}
            /networkServices
        """
        )
        query_params = query_params or {}

        # Prepare request body and headers
        body = {}
        headers = {}

        # Create the request
        request, error = self._request_executor.create_request(http_method, api_url, body, headers, params=query_params)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)

        if error:
            return (None, response, error)

        try:
            result = []
            for item in response.get_results():
                result.append(NetworkServices(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def add_network_service(self, ports: list = None, **kwargs) -> tuple:
        """
        Adds a new Network Service.

        Args:
            name: The name of the Network Service
            ports (list):
                A list of port protocol tuples. Tuples must follow the convention `src/dest`, `protocol`,
                `start port`, `end port`. If this is a single port and not a port range then `end port` can be omitted.
                E.g.

                .. code-block:: python

                    ('src', 'tcp', '49152', '65535'),
                    ('dest', 'tcp', '22),
                    ('dest', 'tcp', '9010', '9012'),
                    ('dest', 'udp', '9010', '9012')

            **kwargs: Optional keyword args.

        Keyword Args:
            description (str): Additional information on the Network Service.

        Returns:
            :obj:`Tuple`: The newly created Network Service resource record.

        Examples:
            Add Network Service for Microsoft Exchange:

            >>> ztw.nw_service.add_network_service('MS LDAP',
            ...    description='Covers all ports used by MS LDAP',
            ...    ports=[
            ...        ('dest', 'tcp', '389'),
            ...        ('dest', 'udp', '389'),
            ...        ('dest', 'tcp', '636'),
            ...        ('dest', 'tcp', '3268', '3269')])

            Add Network Service designed to match inbound SSH traffic:

            >>> ztw.nw_service.add_network_service('Inbound SSH',
            ...    description='Inbound SSH',
            ...    ports=[
            ...        ('src', 'tcp', '22'),
            ...        ('dest', 'tcp', '1024', '65535')])

        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._ztw_base_endpoint}
            /networkServices
        """
        )

        body = kwargs

        if ports is not None:
            for items in ports:
                port_dict = {"start": int(items[2])}
                if len(items) == 4:
                    port_dict["end"] = int(items[3])
                body.setdefault(f"{items[0]}{items[1].title()}Ports", []).append(port_dict)

        request, error = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
            body=body,
        )

        if error:
            return (None, None, error)

        # Execute the request
        response, error = self._request_executor.execute(request, NetworkServices)

        if error:
            return (None, response, error)

        try:
            result = NetworkServices(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_network_service(self, service_id: str, ports: list = None, **kwargs) -> tuple:
        """
        Updates the specified Network Service.

        If ports aren't provided then no changes will be made to the ports already defined. If ports are provided then
        the existing ports will be overwritten.

        Args:
            service_id (str): The unique ID for the Network Service.
            ports (list):
                A list of port protocol tuples. Tuples must follow the convention `src/dest`, `protocol`, `start port`,
                `end port`. If this is a single port and not a port range then `end port` can be omitted. E.g.

                .. code-block:: python

                    ('src', 'tcp', '49152', '65535'),
                    ('dest', 'tcp', '22),
                    ('dest', 'tcp', '9010', '9012'),
                    ('dest', 'udp', '9010', '9012')

            **kwargs: Optional keyword args.

        Keyword Args:
            description (str): Additional information on the Network Service.

        Returns:
            :obj:`dict`: The updated Network Service resource record.

        Examples:
            Update the name and description for a Network Service:

            >>> ztw.nw_service.update_network_service('959093',
            ...    name='MS Exchange',
            ...    description='All ports related to the MS Exchange service.')

            Updates the ports for a Network Service, leaving other fields intact:

            >>> ztw.nw_service.update_network_service('959093',
            ...    ports=[
            ...        ('dest', 'tcp', '500', '510')])

        """
        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._ztw_base_endpoint}
            /networkServices/{service_id}
        """
        )

        body = {}

        body.update(kwargs)

        if ports is not None:
            for items in ports:
                port_dict = {"start": int(items[2])}
                if len(items) == 4:
                    port_dict["end"] = int(items[3])
                body.setdefault(f"{items[0]}{items[1].title()}Ports", []).append(port_dict)

        request, error = self._request_executor.create_request(http_method, api_url, body, {}, {})

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, NetworkServices)

        if error:
            return (None, response, error)

        try:
            result = NetworkServices(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def delete_network_service(self, service_id: int) -> tuple:
        """
        Deletes the specified Network Service.

        Args:
            service_id (str): The unique ID for the Network Service.

        Returns:
            :obj:`int`: The status code for the operation.

        Examples:
            >>> _, response, error = client.ztw.nw_service.delete_network_service(updated_group.id)
            ... if error:
            ...     print(f"Error deleting group: {error}")
            ... return

        """
        http_method = "delete".upper()
        api_url = format_url(
            f"""
            {self._ztw_base_endpoint}
            /networkServices/{service_id}
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
