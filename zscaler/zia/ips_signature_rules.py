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

import textwrap
from datetime import datetime
from typing import List, Optional

from zscaler.api_client import APIClient
from zscaler.request_executor import RequestExecutor
from zscaler.types import APIResult
from zscaler.utils import format_url
from zscaler.zia.models.ips_signature_rules import IPSSignatureRules, ValidateIPSRuleText


class IPSSignatureRulesAPI(APIClient):
    """
    A Client object for the IPS Signture Rules resource.
    """

    _zia_base_endpoint = "/zia/api/v1"

    def __init__(self, request_executor: "RequestExecutor") -> None:
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def list_ips_signature_rules(self, query_params: Optional[dict] = None) -> APIResult[List[IPSSignatureRules]]:
        """
        Lists custom IPS signature rules.

        See the `List ZIA Custom IPS Signature Rules API reference
        <https://help.zscaler.com/legacy-apis/ips-control-policy#/ipsSignatureRules-get>`__
        for further detail on optional keyword parameter structures.

        Args:
            query_params {dict}: Map of query parameters for the request.
                ``[query_params.page]`` {int}: Specifies the page offset.

                ``[query_params.page_size]`` {int}: Page size for pagination.

        Returns:
            tuple: A tuple containing (list of IPS Signture Rules instances, Response, error)

        Examples:
            List IPS Signture Rules using default settings:

            >>> rules_list, _, error = client.zia.ips_signature_rules.list_ips_signature_rules(
                query_params={'page': '1', 'page_size': '250'})
            >>> if error:
            ...     print(f"Error listing IPS Signature Rules: {error}")
            ...     return
            ... print(f"Total IPS Signature Rules found: {len(rules_list)}")
            ... for rule in rules_list:
            ...     print(rule.as_dict())

            Client-side filtering with JMESPath:

            The response object supports client-side filtering and
            projection via ``resp.search(expression)``.  See the
            `JMESPath documentation <https://jmespath.org/>`_ for
            expression syntax.

        """
        http_method = "get".upper()
        api_url = format_url(f"""
            {self._zia_base_endpoint}
            /ipsSignatureRules
        """)

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
                result.append(IPSSignatureRules(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_ips_signature_rule(self, rule_id: int) -> APIResult[dict]:
        """
        Fetches the custom IPS signature rules based on the specified ID

        See the `Get ZIA Custom IPS Signature Rule API reference
        <https://help.zscaler.com/legacy-apis/ips-control-policy#/ipsSignatureRules-post>`__
        for further detail on optional keyword parameter structures.

        Args:
            rule_id (int): The unique identifier for the IPS Signature Rule.

        Returns:
            tuple: A tuple containing (IPS Signature Rule instance, Response, error).

        Examples:
            Print a specific IPS Signature Rule

            >>> fetched_rule, _, error = client.zia.ips_signature_rules.get_ips_signature_rule(
                '1254654')
            >>> if error:
            ...     print(f"Error fetching IPS Signature Rule by ID: {error}")
            ...     return
            ... print(f"Fetched IPS Signature Rule by ID: {fetched_rule.as_dict()}")
        """
        http_method = "get".upper()
        api_url = format_url(f"""
            {self._zia_base_endpoint}
            /ipsSignatureRules/{rule_id}
        """)

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, IPSSignatureRules)
        if error:
            return (None, response, error)

        try:
            result = IPSSignatureRules(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def _preflight_validate_rule_text(self, kwargs: dict) -> Optional[Exception]:
        """
        Internal pre-flight hook used by :meth:`add_ips_signature_rule` and
        :meth:`update_ips_signature_rule`.

        If ``kwargs`` carries a ``rule_text``, this calls
        :meth:`validate_ips_signature_rule` and surfaces any syntactic / semantic
        issue *before* the SDK issues the create or update request. Returns
        ``None`` when there is nothing to validate or the rule is valid, and an
        ``Exception`` describing the failure otherwise.

        Update calls that don't change ``rule_text`` simply skip validation.
        """
        rule_text = kwargs.get("rule_text")
        if not rule_text:
            return None

        result, _, error = self.validate_ips_signature_rule(rule_text=rule_text)
        if error:
            return error
        if result is None:
            return None
        if result.status == 0 and not result.err_msg:
            return None

        return ValueError(
            "IPS signature rule validation failed "
            f"(status={result.status}, errPosition={result.err_position}): "
            f"{result.err_msg or 'unknown error'}"
        )

    def add_ips_signature_rule(self, **kwargs) -> APIResult[dict]:
        """
        Creates a new custom IPS signature rule.

        The supplied ``rule_text`` is validated against the ZIA dynamic-validation
        endpoint (``validate_ips_signature_rule``) *before* the create request is
        issued. If the rule is syntactically or semantically invalid, the method
        returns ``(None, None, ValueError(...))`` and no create call is made.

        See the `Add ZIA Custom IPS Signature Rule API reference
        <https://help.zscaler.com/legacy-apis/ips-control-policy#/ipsSignatureRules-post>`__
        for further detail on optional keyword parameter structures.

        Args:
            name (str): The name of the IPS Signature Rule.
            **kwargs: Optional keyword args.

        Keyword Args:
            description (str): Additional notes or information.
            rule_text (str): The custom signature rule text. Validated before submit.

        Returns:
            tuple: A tuple containing the newly added IPS Signature Rule, response, and error.

        Examples:
            Add a new IPS Signature Rule :

            >>> added_rule, _, error = client.zia.ips_signature_rules.add_ips_signature_rule(
            ...     name=f"NewIPS_Signature_Rule_{random.randint(1000, 10000)}",
            ...     description=f"NewIPS_Signature_Rule_{random.randint(1000, 10000)}",
            ...     rule_text='alert http any any -> any any (msg:"HTTP /admin"; '
            ...               'content:"/admin"; http_uri; nocase; sid:1000010; rev:1;)',
            ... )
            >>> if error:
            ...     print(f"Error adding IPS Signature Rule: {error}")
            ...     return
            ... print(f"IPS Signature Rule added successfully: {added_rule.as_dict()}")
        """
        validation_error = self._preflight_validate_rule_text(kwargs)
        if validation_error:
            return (None, None, validation_error)

        http_method = "post".upper()
        api_url = format_url(f"""
            {self._zia_base_endpoint}
            /ipsSignatureRules
        """)

        body = kwargs

        request, error = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
            body=body,
        )

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, IPSSignatureRules)
        if error:
            return (None, response, error)

        try:
            result = IPSSignatureRules(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_ips_signature_rule(self, rule_id: int, **kwargs) -> APIResult[dict]:
        """
        Updates information for the specified IPS Signature Rule.

        .. note::
            Unlike :meth:`add_ips_signature_rule`, this method does **not** call
            :meth:`validate_ips_signature_rule` before issuing the update. The
            dynamic-validation endpoint flags any signature carrying a ``sid``
            (or other unique identifiers) that already exists on the tenant as
            a duplicate — which on an update is the rule being modified
            itself, so a pre-flight check would reject every legitimate update.
            If you want to validate ``rule_text`` before updating, call
            :meth:`validate_ips_signature_rule` explicitly from your code.

        See the `Update ZIA Custom IPS Signature Rule API reference
        <https://help.zscaler.com/legacy-apis/ips-control-policy#/ipsSignatureRules/{id}-put>`__
        for further detail on optional keyword parameter structures.

        Args:
            rule_id (int): The unique ID for the IPS Signature Rule.

        Keyword Args:
            name (str): The name of the IPS Signature Rule.
            description (str): Additional notes or information.
            rule_text (str): The custom signature rule text.

        Returns:
            tuple: A tuple containing the updated IPS Signature Rule, response, and error.

        Examples:
            Update an existing IPS Signature Rule :

            >>> updated_rule, _, error = client.zia.ips_signature_rules.update_ips_signature_rule(
            ...     rule_id='1524566',
            ...     name=f"UpdatedIPS_Signature_Rule_{random.randint(1000, 10000)}",
            ...     description=f"UpdatedIPS_Signature_Rule_{random.randint(1000, 10000)}",
            ...     rule_text='alert http any any -> any any (msg:"HTTP /admin"; '
            ...               'content:"/admin"; http_uri; nocase; sid:1000010; rev:1;)',
            ... )
            >>> if error:
            ...     print(f"Error updating IPS Signature Rule: {error}")
            ...     return
            ... print(f"IPS Signature Rule updated successfully: {updated_rule.as_dict()}")
        """
        http_method = "put".upper()
        api_url = format_url(f"""
            {self._zia_base_endpoint}
            /ipsSignatureRules/{rule_id}
        """)
        body = kwargs

        request, error = self._request_executor.create_request(http_method, api_url, body, {}, {})
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, IPSSignatureRules)
        if error:
            return (None, response, error)

        try:
            result = IPSSignatureRules(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def delete_ips_signature_rule(self, rule_id: int) -> APIResult[dict]:
        """
        Deletes the specified IPS Signature Rule.

        See the `Delete ZIA Custom IPS Signature Rule API reference
        <https://help.zscaler.com/legacy-apis/ips-control-policy#/ipsSignatureRules/{id}-delete>`__
        for further detail on optional keyword parameter structures.

        Args:
            rule_id (int): The unique identifier of the IPS Signature Rule.

        Returns:
            tuple: A tuple containing the response object and error (if any).

        Examples:
            Delete a IPS Signature Rule:

            >>> _, _, error = client.zia.ips_signature_rules.delete_ips_signature_rule('73459')
            >>> if error:
            ...     print(f"Error deleting IPS Signature Rule: {error}")
            ...     return
            ... print(f"IPS Signature Rule with ID {'73459' deleted successfully.")
        """
        http_method = "delete".upper()
        api_url = format_url(f"""
            {self._zia_base_endpoint}
            /ipsSignatureRules/{rule_id}
        """)

        params = {}

        request, error = self._request_executor.create_request(http_method, api_url, params=params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)
        return (None, response, None)

    def validate_ips_signature_rule(self, rule_text: str) -> APIResult[dict]:
        """
        Validates a new custom signature rule based on specific predefined conditions,
        such as syntax errors, duplicate signatures, and more.

        See the `Validate ZIA Custom IPS Signature Rule API reference
        <https://help.zscaler.com/legacy-apis/ips-control-policy#/ipsSignatureRules/validateRuleText-post>`__
        for further detail on optional keyword parameter structures.

        Args:
            rule_text (str): The custom signature rule text to be validated. Sent on the
                wire as ``{"ruleText": "<rule_text>"}`` to match the API contract.

        Returns:
            tuple: A tuple containing (:class:`ValidateIPSRuleText`, Response, error).

        Example:
            To validate a custom signature rule text:

            >>> rule_text = '''
            ... alert http any any -> any any (msg:"HTTP /admin"; content:"/admin"; \
            ... http_uri; nocase; sid:1000010; rev:1;)
            ... '''
            >>> result, _, error = client.zia.ips_signature_rules.validate_ips_signature_rule(
            ...     rule_text=rule_text,
            ... )
            >>> if error:
            ...     print(f"Validation failed: {error}")
            ... elif result.status == 0 and not result.err_msg:
            ...     print("IPS signature rule is valid.")
            ... else:
            ...     print(f"Invalid rule: {result.err_msg} (position {result.err_position})")
        """
        http_method = "post".upper()
        api_url = format_url(f"""
            {self._zia_base_endpoint}
            /ipsSignatureRules/validateRuleText
        """)

        # Normalize so validator sees the rule at line 1 (matches the position
        # reported back by the API in `errPosition`).
        signature_rule_text = textwrap.dedent(rule_text).lstrip("\r\n")

        # The API expects a JSON object with `ruleText`, not a bare JSON string.
        body = {"ruleText": signature_rule_text}

        request, error = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
            body=body,
        )
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        try:
            result = ValidateIPSRuleText(self.form_response_body(response.get_body()))
        except Exception as parse_error:
            return (None, response, parse_error)

        return (result, response, None)

    def export_custom_ips_signatures(self, filename: str = None):
        """
        Exports the custom IPS signature rules to a CSV file.

        See the `Export ZIA Custom IPS Signature Rules API reference
        <https://help.zscaler.com/legacy-apis/ips-control-policy#/ipsSignatureRules/export-get>`__
        for further detail on optional keyword parameter structures.

        Args:

            filename (str, optional): Custom filename for the CSV file. Defaults to timestamped name.

        Returns:
            str: Path to the downloaded CSV file.

        Examples:
            Export custom IPS signature rules to a CSV:

            >>> try:
            ...     filename = client.zia.ips_signature_rules.export_custom_ips_signatures(
            ...         filename="custom_ips_signature_rules.csv",
            ...     )
            ...     print(f"Custom IPS signature rules exported successfully: {filename}")
            ... except Exception as e:
            ...     print(f"Error during export: {e}")
        """
        if not filename:
            filename = f"custom-ips-signatures-{datetime.now().strftime('%Y%m%d-%H_%M_%S')}.csv"

        http_method = "get".upper()
        api_url = format_url(f"{self._zia_base_endpoint}/ipsSignatureRules/export")

        request, error = self._request_executor.create_request(http_method, api_url, headers={"Accept": "*/*"})

        if error:
            raise Exception("Error creating request for exporting custom IPS signature rules.")

        response, error = self._request_executor.execute(request, return_raw_response=True)
        if error:
            raise error
        if response is None:
            raise Exception("No response received when exporting custom IPS signature rules.")

        content_type = response.headers.get("Content-Type", "").lower()
        csv_header = '"Name","Signature Rule","Threat Category","Description","Status"'
        if not content_type.startswith("application/octet-stream") and not response.text.startswith(csv_header):
            raise Exception("Invalid response content type or unexpected response format.")

        with open(filename, "wb") as f:
            f.write(response.content)

        return filename
