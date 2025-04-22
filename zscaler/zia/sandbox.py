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

import mimetypes
import time
from zscaler.request_executor import RequestExecutor
from zscaler.utils import format_url


class CloudSandboxAPI:
    """
    A Client object for the Cloud Sandbox resource.
    """

    _sandbox_base_endpoint = "/zscsb"
    _zia_base_endpoint = "/zia/api/v1"

    def __init__(self, request_executor):
        self._request_executor: RequestExecutor = request_executor

    def submit_file(self, file_path: str, force: bool = False) -> tuple:
        """
        Submits a file to the ZIA Advanced Cloud Sandbox for analysis.

        Args:
            file_path (str): The filename that will be submitted for sandbox analysis.
            force (bool): Force ZIA to analyse the file even if it has been submitted previously.

        Returns:
            :obj:`Tuple`: The Cloud Sandbox submission response information.

        Examples:
            Submit a file in the current directory called malware.exe to the cloud sandbox, forcing analysis.

            >>> script_dir = os.path.dirname(os.path.abspath(__file__))
            ... file_path = os.path.join(script_dir, "test-pe-file.exe")
            ... force_analysis = True
            ...     submit, _, err = client.zia.sandbox.submit_file(
                file_path=file_path, force=force_analysis)
            >>>     if err:
            ...         print(f"Error submitting file: {err}")
            ...     else:
            ...         print("File submitted successfully!")
            ...         print(f"Response: {submit}")
        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._sandbox_base_endpoint}
            /submit
            """
        )

        with open(file_path, "rb") as file:
            file_content = file.read()

        params = {
            "force": int(force),
        }

        request, error = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
            body=file_content,
            params=params,
            headers={"Content-Type": "application/octet-stream"},
            use_raw_data_for_body=True,
        )

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)

        if error:
            return (None, response, error)

        try:
            result = response.get_body()
        except Exception as error:
            return (None, response, error)

        return (result, response, None)

    def submit_file_for_inspection(self, file_path: str) -> tuple:
        """
        Submits a file for inspection.

        Args:
            file_path (str): The path to the file to be inspected.

        Returns:
            tuple: A tuple containing the result, response, and error.

        Examples:
            Submit a file in the current directory called malware.exe to the cloud sandbox, forcing analysis.

            >>> script_dir = os.path.dirname(os.path.abspath(__file__))
            ... file_path = os.path.join(script_dir, "test-pe-file.exe")
            ... force_analysis = True
            ...     submit, _, err = client.zia.sandbox.submit_file_for_inspection(
                file_path=file_path, force=force_analysis)
            >>>     if err:
            ...         print(f"Error submitting file: {err}")
            ...     else:
            ...         print("File submitted successfully!")
            ...         print(f"Response: {submit}")
        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._sandbox_base_endpoint}
            /discan
            """
        )

        with open(file_path, "rb") as file:
            file_content = file.read()
        content_type, _ = mimetypes.guess_type(file_path)
        if not content_type:
            content_type = "application/octet-stream"

        params = {}

        request, error = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
            body=file_content,
            params=params,
            headers={"Content-Type": content_type},
            use_raw_data_for_body=True,
        )

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)

        if error:
            return (None, response, error)

        try:
            result = response.get_body()
        except Exception as error:
            return (None, response, error)

        return (result, response, None)

    def get_quota(self) -> tuple:
        """
        Returns the Cloud Sandbox API quota information for the organisation.

        Returns:
            tuple: A tuple containing the result, response, and error.
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /sandbox/report/quota
            """
        )

        request, error = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
        )

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)

        if error:
            return (None, response, error)

        try:
            result = response.get_body()
        except Exception as error:
            return (None, response, error)

        return (result, response, None)

    def get_report(self, md5_hash: str, report_details: str = "summary") -> tuple:
        """
        Returns the Cloud Sandbox Report for the provided hash.

        Args:
            md5_hash (str):
                The MD5 hash of the file that was analysed by Cloud Sandbox.
            report_details (str):
                The type of report. Accepted values are 'full' or 'summary'. Defaults to 'summary'.

        Returns:
            tuple: A tuple containing the result, response, and error.
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /sandbox/report/{md5_hash}?details={report_details}
            """
        )

        # Create the request
        request, error = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
        )

        if error:
            return (None, None, error)

        # Execute the request
        response, error = self._request_executor.execute(request)

        if error:
            return (None, response, error)

        try:
            result = response.get_body()
        except Exception as error:
            return (None, response, error)

        return (result, response, None)

    def get_behavioral_analysis(self) -> tuple:
        """
        Returns the custom list of MD5 file hashes that are blocked by Sandbox.

        Returns:
            tuple: A tuple containing the result, response, and error.
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /behavioralAnalysisAdvancedSettings
            """
        )

        request, error = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
        )

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)

        if error:
            return (None, response, error)

        try:
            result = response.get_body()
        except Exception as error:
            return (None, response, error)

        return (result, response, None)

    def get_file_hash_count(self) -> tuple:
        """
        Retrieves the Cloud Sandbox used and unused quota for blocking MD5 file hashes.

        This method fetches the count of MD5 hashes currently blocked by the Sandbox and the remaining
        quota available for blocking additional hashes.

        Returns:
            tuple: A tuple containing the result, response, and error.
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /behavioralAnalysisAdvancedSettings/fileHashCount
            """
        )

        # Create the request
        request, error = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
        )

        if error:
            return (None, None, error)

        # Execute the request
        response, error = self._request_executor.execute(request)

        if error:
            return (None, response, error)

        try:
            result = response.get_body()
        except Exception as error:
            return (None, response, error)

        return (result, response, None)

    def add_hash_to_custom_list(self, file_hashes_to_be_blocked: list) -> tuple:
        """
        Updates the custom list of MD5 file hashes that are blocked by Sandbox.

        Args:
            file_hashes_to_be_blocked (:obj:`list` of :obj:`str`):
                The list of MD5 Hashes to be added. Pass an empty list to clear the blocklist.

        Returns:
            tuple: A tuple containing the result, response, and error.
        """
        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /behavioralAnalysisAdvancedSettings
            """
        )

        payload = {"fileHashesToBeBlocked": file_hashes_to_be_blocked}

        request, error = self._request_executor.create_request(method=http_method, endpoint=api_url, body=payload)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)

        if error:
            return (None, response, error)
        time.sleep(2)
        return self.get_behavioral_analysis()
