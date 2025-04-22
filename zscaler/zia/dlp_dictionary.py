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
from zscaler.zia.models.dlp_dictionary import DLPDictionary, DLPPatternValidation
from zscaler.utils import format_url


class DLPDictionaryAPI(APIClient):
    """
    A Client object for the DLP Dictionary resource.
    """

    _zia_base_endpoint = "/zia/api/v1"

    def __init__(self, request_executor):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def list_dicts(
        self,
        query_params=None,
    ) -> tuple:
        """
        Returns a list of all custom and predefined ZIA DLP Dictionaries.

        Args:
            query_params {dict}: Map of query parameters for the request.
                ``[query_params.search]`` {str}: Search string to match a DLP dictionary's name or description attributes

        Returns:
            tuple: A tuple containing (list of DLPDictionaries instances, Response, error)

        Example:
            List all dlp dictionaries:

            >>> dict_list, response, error = client.zia.dlp_dictionary.list_dicts()
            ... if error:
            ...    print(f"Error listing dlp dictionaries: {error}")
            ...    return
            ... print(f"Total dictionaries found: {len(dict_list)}")
            ... for dict in dict_list:
            ...    print(dict.as_dict())

            filtering dlp dictionaries by name :

            >>> dict_list, response, error = client.zia.dlp_dictionary.list_dicts(
                query_params={"search": 'GDPR'}
            )
            ... if error:
            ...    print(f"Error listing dlp dictionaries: {error}")
            ...    return
            ... print(f"Total dictionaries found: {len(dict_list)}")
            ... for dict in dict_list:
            ...    print(dict.as_dict())

        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /dlpDictionaries
        """
        )

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
                result.append(DLPDictionary(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def list_dicts_lite(
        self,
        query_params=None,
    ) -> tuple:
        """
        Lists name and ID dictionary of all custom and predefined DLP dictionaries.
        If the `search` parameter is provided, the function filters the rules client-side.

        Args:
            query_params {dict}: Map of query parameters for the request.
                ``[query_params.search]`` {str}: The search string used to match against a dictionary name.

        Returns:
            tuple: List of DLP Dictionary resource records.

        Examples:
            Gets a list of all DLP Dictionary.

            >>> fetched_dicts, response, error = client.zia.dlp_dictionary.list_dicts()
            ... if error:
            ...     print(f"Error listing DLP Dictionaries: {error}")
            ...     return
            ... print(f"Fetched dictionaries: {[dictionary.as_dict() for dictionary in fetched_dicts]}")

            Gets a list of all DLP Dictionary name and ID.

            >>> dict, response, error = = client.zia.dlp_dictionary.list_dicts(query_params={"search": 'EUIBAN_LEAKAGE'})
            ... if error:
            ...     print(f"Error listing DLP Dictionary: {error}")
            ...     return
            ... print(f"Fetched dictionary: {[dictionary.as_dict() for dictionary in dict]}")

        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /dlpDictionaries/lite
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
                results.append(DLPDictionary(self.form_response_body(item)))
        except Exception as exc:
            return (None, response, exc)

        if local_search:
            lower_search = local_search.lower()
            results = [r for r in results if lower_search in (r.name.lower() if r.name else "")]

        return (results, response, None)

    def get_dict(self, dict_id: int) -> tuple:
        """
        Returns the DLP Dictionary that matches the specified DLP Dictionary id.

        Args:
            dict_id (str): The unique id for the DLP Dictionary.

        Returns:
            :obj:`Tuple`: The ZIA DLP Dictionary resource record.

        Examples:
            >>> pprint(zia.dlp_dictionary.get_dict('3'))

        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /dlpDictionaries/{dict_id}
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
            result = DLPDictionary(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def add_dict(self, name: str, custom_phrase_match_type: str, dictionary_type: str, **kwargs) -> tuple:
        """
        Add a new Patterns and Phrases DLP Dictionary to ZIA.

        Args:
            name (str): The name of the DLP Dictionary.
            match_type (str): The DLP custom phrase/pattern match type. Accepted values are ``all`` or ``any``.

        Keyword Args:
            description (str): Additional information about the DLP Dictionary.
            phrases (list):
                A list of DLP phrases, with each phrase provided by a tuple following the convention
                (`action`, `pattern`). Accepted actions are ``all`` or ``unique``. E.g.

                .. code-block:: python

                    ('all', 'TOP SECRET')
                    ('unique', 'COMMERCIAL-IN-CONFIDENCE')

            patterns (list):
                A list of DLP patterns, with each pattern provided by a tuple following the convention
                (`action`, `pattern`). Accepted actions are ``all`` or ``unique``. E.g.

                .. code-block:: python

                    ('all', '\d{2} \d{3} \d{3} \d{3}')
                    ('unique', '[A-Z]{6}[A-Z0-9]{2,5}')

        Returns:
            :obj:`Tuple`: The newly created DLP Dictionary resource record.

        Examples:
            Match text found that contains an IPv4 address using patterns:

            >>> zia.dlp_dictionary.add_dict(name='IPv4 Addresses',
            ...                description='Matches IPv4 address pattern.',
            ...                match_type='all',
            ...                patterns=[
            ...                    ('all', '\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}(/(\d|[1-2]\d|3[0-2]))?')
            ...                ]))

            Match text found that contains government document caveats using phrases.

            >>> zia.dlp_dictionary.add_dict(name='Gov Document Caveats',
            ...                description='Matches government classification caveats.',
            ...                match_type='any',
            ...                phrases=[
            ...                    ('all', 'TOP SECRET'),
            ...                    ('all', 'SECRET'),
            ...                    ('all', 'CONFIDENTIAL')
            ...                ]))

            Match text found that meets the criteria for a Secret Project's document markings using phrases and
            patterns:

            >>> zia.dlp_dictionary.add_dict(name='Secret Project Documents',
            ...                description='Matches documents created for the Secret Project.',
            ...                match_type='any',
            ...                phrases=[
            ...                    ('all', 'Project Umbrella'),
            ...                    ('all', 'UMBRELLA')
            ...                ],
            ...                patterns=[
            ...                    ('unique', '\d{1,2}-\d{1,2}-[A-Z]{5}')
            ...                ]))

        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}/dlpDictionaries
        """
        )

        payload = {
            "name": name,
            "customPhraseMatchType": custom_phrase_match_type,
            "dictionaryType": dictionary_type,
        }

        payload.update(kwargs)

        if "phrases" in payload:
            payload["phrases"] = [{"action": action, "phrase": phrase} for action, phrase in payload["phrases"]]

        if "patterns" in payload:
            payload["patterns"] = [{"action": action, "pattern": pattern} for action, pattern in payload["patterns"]]

        request, error = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
            body=payload,
        )

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, DLPDictionary)

        if error:
            return (None, response, error)

        try:
            result = DLPDictionary(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)

        return (result, response, None)

    def update_dict(self, dict_id: int, **kwargs) -> tuple:
        """
        Updates the specified DLP Dictionary.

        Args:
            dict_id (str): The unique id of the DLP Dictionary.
            **kwargs: Optional keyword args.

        Keyword Args:
            description (str): Additional information about the DLP Dictionary.
            match_type (str): The DLP custom phrase/pattern match type. Accepted values are ``all`` or ``any``.
            name (str): The name of the DLP Dictionary.
            phrases (list):
                A list of DLP phrases, with each phrase provided by a tuple following the convention
                (`action`, `pattern`). Accepted actions are ``all`` or ``unique``. E.g.

                .. code-block:: python

                    ('all', 'TOP SECRET')
                    ('unique', 'COMMERCIAL-IN-CONFIDENCE')

            patterns (list):
                A list of DLP pattersn, with each pattern provided by a tuple following the convention
                (`action`, `pattern`). Accepted actions are ``all`` or ``unique``. E.g.

                .. code-block:: python

                    ('all', '\d{2} \d{3} \d{3} \d{3}')
                    ('unique', '[A-Z]{6}[A-Z0-9]{2,5}')

        Returns:
            tuple: The updated DLP Dictionary resource record.

        Examples:
            Update the name of a DLP Dictionary:

            >>> zia.dlp_dictionary.update_dict('3',
            ...                name='IPv4 and IPv6 Addresses')

            Update the description and phrases for a DLP Dictionary.

            >>> zia.dlp_dictionary.update_dict('4',
            ...        description='Updated government caveats.'
            ...        phrases=[
            ...                    ('all', 'TOP SECRET'),
            ...                    ('all', 'SECRET'),
            ...                    ('all', 'PROTECTED')
            ...                ])

        """
        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /dlpDictionaries/{dict_id}
        """
        )

        payload = kwargs.copy()

        if "phrases" in payload:
            payload["phrases"] = [{"action": action, "phrase": phrase} for action, phrase in payload["phrases"]]

        if "patterns" in payload:
            payload["patterns"] = [{"action": action, "pattern": pattern} for action, pattern in payload["patterns"]]

        request, error = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
            body=payload,
        )

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, DLPDictionary)
        if error:
            return (None, response, error)

        try:
            result = DLPDictionary(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def delete_dict(self, dict_id: str) -> tuple:
        """
        Deletes the DLP Dictionary that matches the specified DLP Dictionary id.

        Args:
            dict_id (str): The unique id for the DLP Dictionary.

        Returns:
            :obj:`int`: The status code for the operation.

        Examples:
            >>> zia.dlp_dictionary.delete_dict('8')

        """
        http_method = "delete".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}/dlpDictionaries/{dict_id}
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

    def validate_dict(self, pattern: str) -> tuple:
        """
        Validates the provided pattern for usage in a DLP Dictionary.

        Note: The ZIA API documentation doesn't provide information on how to structure a request for this API endpoint.
        This endpoint is returning a valid response but validation isn't failing for obvious wrong patterns. Use at
        own risk.

        Args:
            pattern (str): DLP Pattern for evaluation.

        Returns:
            tuple: A tuple containing the validation result (DLPPatternValidation instance), response, and error.
        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /dlpDictionaries/validateDlpPattern
        """
        )

        payload = {"data": pattern}

        request, error = self._request_executor.create_request(http_method, api_url, payload, {}, {})
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, DLPPatternValidation)
        if error:
            return (None, response, error)

        try:
            result = DLPPatternValidation(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)

        return (result, response, None)

    def list_dict_predefined_identifiers(self, dict_name: str) -> tuple:
        """
        Returns a list of predefined identifiers for a specific DLP dictionary by its name.

        Args:
            dict_name (str): The name of the predefined DLP dictionary. Supported Predefined Identifiers are:
                `ASPP_LEAKAGE`, `CRED_LEAKAGE`, `EUIBAN_LEAKAGE`, `PPEU_LEAKAGE`, `USDL_LEAKAGE`

        Returns:
            tuple: A tuple containing (list of predefined identifiers, Response, error)
        Examples:
            List predefined identifiers for the 'USDL_LEAKAGE' dictionary

            >>> pprint(zia.dlp_dictionary.list_dict_predefined_identifiers('USDL_LEAKAGE'))

        """
        dictionaries, response, error = self.list_dicts()
        if error:
            return (None, response, error)

        dictionary = next((d for d in dictionaries if d.name == dict_name), None)
        if not dictionary:
            return (None, response, ValueError(f"No dictionary found with the name: {dict_name}"))

        dict_id = dictionary.id

        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /dlpDictionaries/{dict_id}/predefinedIdentifiers
        """
        )

        request, error = self._request_executor.create_request(http_method, api_url, {}, {}, {})
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, DLPDictionary)
        if error:
            return (None, response, error)

        try:
            result = response.get_body()
        except Exception as error:
            return (None, response, error)

        return (result, response, None)
