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
from zscaler.utils import format_url

class PolicyExportAPI(APIClient):
    """
    A Client object for exporting ZIA policy rules to JSON files.
    """
    _zia_base_endpoint = "/zia/api/v1"

    def __init__(self, request_executor):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def policy_export(self, policy_types=None, output_file=None) -> tuple:
        """
        Exports the rules for the specified policy types to JSON (or ZIP) files, 
        depending on the API response. One file is created per policy type.

        Args:
            policy_types (list[str]): A list of policy types to export. For example:
                ["BA", "URL_FILTERING", "CUSTOM_CAPP", ...].
                If omitted or None, you may get a default set (check your API doc).
            output_file (str): Optional. If provided, the raw response is saved 
                to a file with this name.

        Returns:
            tuple: A tuple of (export_content, error).
                - export_content (bytes or dict or str): The raw response body,
                  or None if error.
                - error (str): Any error message. If None, the operation succeeded.

        Examples:
            >>> export_content, err = client.zia.policy_export.policy_export(
            ...     policy_types=["BA","URL_FILTERING"],
            ...     output_file="policy_export.zip"
            ... )
            >>> if err:
            ...     print(f"Error exporting policies: {err}")
            ... else:
            ...     print("Policies exported successfully.")
        """
        http_method = "POST"
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /exportPolicies
            """
        )

        # The API definition says: "body param is an array of strings"
        # e.g. ["BA", "URL_FILTERING"]
        # So we build the JSON body as that list.
        # Or if no policy_types provided, pass empty list or omit if your API allows.
        body = policy_types if policy_types else []

        # Depending on your API doc, the Accept might be "application/octet-stream"
        # or maybe "application/zip" if it returns multiple policy files zipped up.
        # Some endpoints may also respond with "application/json" if only one type is requested.
        headers = {
            "Accept": "application/octet-stream",
            "Content-Type": "application/json",
        }

        # We want raw bytes if it's a file, so we might do `return_raw_response=True`
        # in the request_executor call.
        request, error = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
            body=body,
            headers=headers,
            use_raw_data_for_body=False,  # Because we pass a Python list as JSON
        )
        if error:
            return (None, error)

        response, error = self._request_executor.execute(
            request, return_raw_response=True
        )
        if error:
            # If request failed, return the error and possibly the response body
            return (None, f"Request failed: {error}")

        # The raw response might contain binary data (e.g. a .zip file)
        # or possibly JSON. We'll store it in `content`.
        content = response.content

        # If the user specified an output_file, write it to disk.
        if output_file:
            with open(output_file, "wb") as f:
                f.write(content)

        # Return the raw content as well.
        return (content, None)
