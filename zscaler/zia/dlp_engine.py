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
from zscaler.zia.models.dlp_engine import DLPEngine, DLPVAlidateExpression
from zscaler.utils import format_url


class DLPEngineAPI(APIClient):
    """
    A Client object for the DLP Engine resource.
    """

    _zia_base_endpoint = "/zia/api/v1"

    def __init__(self, request_executor):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def list_dlp_engines(self, query_params=None) -> tuple:
        """
        Returns a list of all DLP Engines.

        Args:
            query_params {dict}: Map of query parameters for the request.
                ``[query_params.search]`` {str}: Search string to match against a DLP Engine name or description attributes.

        Returns:
            tuple: A tuple containing (list of DLP Engines instances, Response, error)

        Examples:
            Gets a list of all DLP Engine.

            >>> fetched_engines, response, error = client.zia.dlp_engine.list_dlp_engines()
            ... if error:
            ...     print(f"Error listing DLP Engines: {error}")
            ...     return
            ... print(f"Fetched engines: {[engine.as_dict() for engine in fetched_engines]}")

            Gets a list of all DLP Engine by name.

            >>> engine, response, error = = client.zia.dlp_engine.list_dlp_engines(
                query_params={"search": 'EUIBAN_LEAKAGE'})
            ... if error:
            ...     print(f"Error listing DLP Engine: {error}")
            ...     return
            ... print(f"Fetched engine: {[engine.as_dict() for engine in dict]}")

        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /dlpEngines
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
                results.append(DLPEngine(self.form_response_body(item)))
        except Exception as exc:
            return (None, response, exc)

        if local_search:
            lower_search = local_search.lower()
            results = [r for r in results if lower_search in (r.name.lower() if r.name else "")]

        return (results, response, None)

    def list_dlp_engines_lite(
        self,
        query_params=None,
    ) -> tuple:
        """
        Lists name and ID Engine of all custom and predefined DLP dictionaries.
        If the `search` parameter is provided, the function filters the rules client-side.

        Args:
            query_params {dict}: Map of query parameters for the request.
                ``[query_params.search]`` {str}: The search string used to match against a dictionary name.

        Returns:
            tuple: List of DLP Engine resource records.

        Examples:
            Gets a list of all DLP Engine.

            >>> fetched_engines, response, error = client.zia.dlp_engine.list_dlp_engines_lite()
            ... if error:
            ...     print(f"Error listing DLP Engines: {error}")
            ...     return
            ... print(f"Fetched engines: {[engine.as_dict() for engine in fetched_engines]}")

            Gets a list of all DLP Engine name and ID.

            >>> engine, response, error = = client.zia.dlp_engine.list_dlp_engines_lite(
                query_params={"search": 'EUIBAN_LEAKAGE'})
            ... if error:
            ...     print(f"Error listing DLP Engine: {error}")
            ...     return
            ... print(f"Fetched engine: {[engine.as_dict() for engine in dict]}")

        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /dlpEngines/lite
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
                results.append(DLPEngine(self.form_response_body(item)))
        except Exception as exc:
            return (None, response, exc)

        if local_search:
            lower_search = local_search.lower()
            results = [r for r in results if lower_search in (r.name.lower() if r.name else "")]

        return (results, response, None)

    def get_dlp_engines(self, engine_id: int) -> tuple:
        """
        Returns the dlp engine details for a given DLP Engine.

        Args:
            engine_id (str): The unique identifier for the DLP Engine.

        Returns:
            :obj:`Tuple`: The DLP Engine resource record.

        Examples:
            >>> engine = zia.dlp.get_dlp_engines('99999')

        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /dlpEngines/{engine_id}
        """
        )

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, DLPEngine)

        if error:
            return (None, response, error)

        try:
            result = DLPEngine(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def add_dlp_engine(self, **kwargs) -> tuple:
        """
        Adds a new dlp engine.

        Args:
            name (str): The order of the rule, defaults to adding rule to bottom of list.

            **kwargs: Optional keyword args.

        Keyword Args:

            engine_expression (str, optional): The logical expression defining a DLP engine by
                combining DLP dictionaries using logical operators: All (AND), Any (OR), Exclude (NOT),
                and Sum (total number of content matches).
            custom_dlp_engine (bool, optional): If true, indicates a custom DLP engine.
            description (str, optional): The DLP engine description.

        Returns:
            :obj:`Tuple`: The updated dlp engine resource record.

        Examples:
            Update the dlp engine:

            >>> zia.dlp.update_dlp_engine(name='new_dlp_engine',
            ...    description='TT#1965432122',
            ...    engine_expression="((D63.S > 1))",
            ...    custom_dlp_engine=False)

            Update a rule to enable custom dlp engine:

            >>> zia.dlp.update_dlp_engine('976597',
            ...    custom_dlp_engine=True,
            ...    engine_expression="((D63.S > 1))",
            ...    description="TT#1965232866")

        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /dlpEngines
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

        response, error = self._request_executor.execute(request, DLPEngine)
        if error:
            return (None, response, error)

        try:
            result = DLPEngine(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_dlp_engine(self, engine_id: int, **kwargs) -> tuple:
        """
        Updates an existing dlp engine.

        Args:
            engine_id (str): The unique ID for the dlp engine that is being updated.

        Keyword Args:
            name (str): The order of the rule, defaults to adding rule to bottom of list.
            description (str, optional): The DLP engine description.
            engine_expression (str, optional): The logical expression defining a DLP engine by
                combining DLP dictionaries using logical operators: All (AND), Any (OR), Exclude (NOT),
                and Sum (total number of content matches).
            custom_dlp_engine (bool, optional): If true, indicates a custom DLP engine.

        Returns:
            tuple: The updated dlp engine resource record.

        Examples:
            Update the dlp engine:

            >>> zia.dlp.update_dlp_engine(name='new_dlp_engine',
            ...    description='TT#1965432122',
            ...    engine_expression="((D63.S > 1))",
            ...    custom_dlp_engine=False)

            Update a rule to enable custom dlp engine:

            >>> zia.dlp.update_dlp_engine('976597',
            ...    custom_dlp_engine=True,
            ...    engine_expression="((D63.S > 1))",
            ...    description="TT#1965232866")

        """
        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /dlpEngines/{engine_id}
        """
        )

        body = {}

        body.update(kwargs)

        request, error = self._request_executor.create_request(http_method, api_url, body, {}, {})
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, DLPEngine)
        if error:
            return (None, response, error)

        try:
            result = DLPEngine(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def delete_dlp_engine(self, engine_id: int) -> tuple:
        """
        Deletes the specified dlp engine.

        Args:
            engine_id (str): The unique identifier for the dlp engine.

        Returns:
            :obj:`int`: The status code for the operation.

        Examples:
            >>> zia.dlp.delete_dlp_engine('278454')

        """
        http_method = "delete".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}/dlpEngines/{engine_id}
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

    def validate_dlp_expression(self, expression: str) -> tuple:
        """
        Validates a DLP engine expression.

        Args:
            expression (str): The logical expression to validate.

        Returns:
            dict: The response from the API, containing the validation status and any errors.

        Examples:
            >>> zia.dlp.validate_dlp_expression("((D63.S > 1) AND (D38.S > 0))")
        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /dlpEngines/validateDlpExpr
        """
        )

        payload = {"data": expression}

        request, error = self._request_executor.create_request(http_method, api_url, payload, {}, {})
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, DLPVAlidateExpression)
        if error:
            return (None, response, error)

        try:
            result = DLPVAlidateExpression(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)

        return (result, response, None)
