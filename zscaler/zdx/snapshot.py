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
from zscaler.zdx.models.snapshot import Snapshot
from zscaler.utils import format_url, zdx_params


class SnapshotAPI(APIClient):
    def __init__(self, request_executor):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor
        self._zdx_base_endpoint = "/zdx/v1"

    @zdx_params
    def share_snapshot(self, **kwargs) -> tuple:
        """
        Share a ZDX Snapshot of alert details for a given alert ID.

        Args:
            name (str): The name of the ZDX Snapshot.
            alert_id (str): The alert ID to create a ZDX Snapshot for.

        Keyword Args:
            expiry (int): The expiry time in hours (will be converted to Unix epoch)
                         The default is set to 2 hours. To configure, the expiration
                         must be between 2 hours and 90 days
            obfuscation (list): Specifies the fields to obfuscate in ZDX snapshot
                               The possible values are: "USER_NAME", "LOCATION",
                               "DEVICE_NAME", "IP_ADDRESS", "WIFI_NAME"

        Returns:
            :obj:`Tuple`: The snapshot resource record containing the following attributes:
                - id (str): The unique identifier for the snapshot.
                - name (str): The name of the snapshot.
                - alert_id (str): The unique ID for the alert associated with the snapshot.
                - expiry (int): The expiry time in Unix epoch format.
                - obfuscation (list): List of obfuscation settings applied to the snapshot.
                - url (str): The URL where the snapshot can be accessed.
                - status (str): The current status of the snapshot.

        Examples:
            Share a ZDX Snapshot of alert

            >>> share_snapshot, _, error = client.zdx.snapshot.share_snapshot(
            ...     name="ZDX-Test-Alert-Snapshot",
            ...     alert_id='7473160764821179371',
            ...     expiry=2
            ... )
            ... if error:
            ...     print(f"Error sharing snapshot: {error}")
            ...     return
            ... print(f"Snapshot shared successfully: {share_snapshot.as_dict()}")

            Share a ZDX Snapshot with obfuscation settings

            >>> share_snapshot, _, error = client.zdx.snapshot.share_snapshot(
            ...     name="ZDX-Test-Alert-Snapshot",
            ...     alert_id='7473160764821179371',
            ...     expiry=24,
            ...     obfuscation=["USER_NAME", "IP_ADDRESS"]
            ... )
            ... if error:
            ...     print(f"Error sharing snapshot: {error}")
            ...     return
            ... print(f"Snapshot shared successfully: {share_snapshot.as_dict()}")
        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._zdx_base_endpoint}
            /snapshot/alert
        """
        )

        # Handle expiry conversion from hours to Unix epoch
        query_params = kwargs.get('query_params', {})
        body = {}

        # Extract the main parameters for the body
        if 'name' in kwargs:
            body['name'] = kwargs['name']
        if 'alert_id' in kwargs:
            body['alert_id'] = kwargs['alert_id']

        # Check if expiry is in query_params (from decorator) and convert it
        if 'expiry' in query_params:
            import time
            # Convert hours to Unix epoch (current time + hours * 3600 seconds)
            expiry_hours = query_params.pop('expiry')  # Remove from query_params
            expiry_epoch = int(time.time()) + (expiry_hours * 3600)
            body['expiry'] = expiry_epoch

        request, error = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
            body=body,
            params=query_params or {}
        )

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, Snapshot)
        if error:
            return (None, response, error)

        try:
            result = Snapshot(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)
