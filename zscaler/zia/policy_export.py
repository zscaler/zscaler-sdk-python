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
        Exports the rules for the specified policy types. The server typically returns
        a ZIP file containing one JSON file per policy type.

        Args:
            policy_types (list[str]): A list of policy types, e.g. ["BA", "URL_FILTERING", ...].
            output_file (str): Optional. If provided, the ZIP is saved to disk at this file path.

        Returns:
            tuple:
                (export_content, error)

                - export_content (bytes): The raw ZIP file bytes from the server (or raw JSON if only one type).
                - error (str): Any error message, or None on success.

        Example:
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
        api_url = format_url(f"{self._zia_base_endpoint}/exportPolicies")

        # Body must be an array of policy type strings
        body = policy_types if policy_types else []

        headers = {
            "Accept": "application/octet-stream",
            "Content-Type": "application/json",
        }

        request, error = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
            body=body,
            headers=headers,
            use_raw_data_for_body=False,  # We'll let JSON be formed from the Python list
        )
        if error:
            return (None, error)

        # We want raw bytes so we can save them if it's a ZIP
        response, error = self._request_executor.execute(request, return_raw_response=True)
        if error:
            return (None, f"Request failed: {error}")

        content = response.content  # raw bytes (likely a .zip)

        # If user asked for a file, write it
        if output_file:
            with open(output_file, "wb") as f:
                f.write(content)

        return (content, None)
