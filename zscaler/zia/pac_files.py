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
from zscaler.zia.models.pac_files import PacFiles
from zscaler.utils import format_url


class PacFilesAPI(APIClient):
    """
    A Client object for the Rule labels resource.
    """

    _zia_base_endpoint = "/zia/api/v1"

    def __init__(self, request_executor):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def list_pac_files(self, query_params=None) -> tuple:
        """
        Lists pac files in your organization with pagination.
        A subset of pac files can be returned that match a supported
        filter expression or query.

        Args:
            query_params {dict}: Map of query parameters for the request.
                ``[query_params.search]`` {str}: Search string for filtering results.

        Returns:
            tuple: A tuple containing (list of Pac Files instances, Response, error)

        Examples:
            List all Pac Files using default settings:
            >>> pac_files, response, err = zia.pac_files.list_pac_files()

        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /pacFiles
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

        # Execute the request
        response, error = self._request_executor.execute(request)

        if error:
            return (None, response, error)

        try:
            result = []
            for item in response.get_results():
                result.append(PacFiles(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_pac_file(self, pac_id: int, query_params=None) -> tuple:
        """
        Retrieves all versions of a PAC file based on the specified ID

        Args:
            pac_id (int): The unique identifier for the Pac File.

        Returns:
            tuple: A tuple containing (Pac File instance, Response, error).
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /pacFiles/{pac_id}/version
        """
        )

        query_params = query_params or {}

        request, error = self._request_executor.create_request(method=http_method, endpoint=api_url, params=query_params)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, PacFiles)
        if error:
            return (None, response, error)

        try:
            result = PacFiles(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)

        return (result, response, None)

    def get_pac_file_version(self, pac_id: int, pac_version: int, query_params=None) -> tuple:
        """
        Returns the PAC file version details for a given PAC ID and version.

        Args:
            pac_id (str): The unique identifier for the PAC file.
            pac_version (str): The specific version of the PAC file.
            filter (str, optional): Excludes specific information about the PAC file from
                                    the response such as the PAC file content.
                                    Accepts only the value 'pac_content'.

        Returns:
            :obj:`Tuple`: The PAC file version resource record.

        Example:
            >>> pac_file_version = zia.get_pac_file_version('12345', '1', filter='pac_content')
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /pacFiles/{pac_id}/version
        """
        )

        query_params = query_params or {}

        request, error = self._request_executor.create_request(method=http_method, endpoint=api_url, params=query_params)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, PacFiles)
        if error:
            return (None, response, error)

        try:
            result = PacFiles(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)

        return (result, response, None)

    def add_pac_file(self, **kwargs) -> tuple:
        """
        Adds a new custom PAC file after validating the PAC content.

        Args:
            name (str): The name of the new PAC file.
            description (str): The description of the new PAC file.
            domain (str): The domain of your organization to which the PAC file applies.
            pac_commit_message (str): Commit msg entered when saving the PAC file version as indicated by the pacVersion field.
            pac_verification_status (str): Verification status of the PAC file and if any errors are identified in the syntax.
                                           Supported Values: `VERIFY_NOERR`, `VERIFY_ERR`, `NOVERIFY`
            pac_version_status (str): Version status of the new PAC file.
                                      Supported Values: `DEPLOYED`, `STAGE`, `LKG`
            pac_content (str): The actual PAC file content to be validated and cloned.

        Keyword Args:
            Additional optional parameters as key-value pairs.

        Returns:
            Tuple: The newly added PAC file resource record.

        Example:
            >>> pac_file = zia.add_pac_file(
                    name="Test_Pac_File_01",
                    description="Test_Pac_File_01",
                    domain="bd-hashicorp.com",
                    pac_commit_message="Test_Pac_File_01",
                    pac_verification_status="VERIFY_NOERR",
                    pac_version_status="DEPLOYED",
                    pac_content="function FindProxyForURL(url, host) { return 'PROXY gateway.example.com:80'; }"
                )
        """
        # Validate the PAC file content before proceeding
        pac_content = kwargs.get("pac_content")
        if not pac_content:
            raise ValueError("Missing required parameter: pac_content")

        validation_result, _, validation_error = self.validate_pac_file(body=pac_content)
        if validation_error or not validation_result.get("success", False):
            raise Exception(f"PAC content validation failed: {validation_result}")

        # Preserve the existing logic for payload and request
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /pacFiles
        """
        )

        body = kwargs

        # Create the request with no empty param handling logic
        request, error = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
            body=body,
        )

        if error:
            return (None, None, error)

        # Execute the request
        response, error = self._request_executor.execute(request, PacFiles)
        if error:
            return (None, response, error)

        try:
            result = PacFiles(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)

        return (result, response, None)

    def clone_pac_file(self, pac_id: int, pac_version: str, **kwargs) -> tuple:
        """
        Clones an existing PAC file by creating a new PAC file based on the specified PAC ID and version.

        Args:
            pac_id (int): The unique identifier of the PAC file to be cloned.
            pac_version (str): The specific version of the PAC file to be cloned.
            name (str): The name of the new PAC file.
            description (str): The description of the new PAC file.
            domain (str): The domain associated with the new PAC file.
            pac_commit_message (str): Commit message for the new PAC file.
            pac_verification_status (str): Verification status of the new PAC file.
                                           Supported Values: `VERIFY_NOERR`, `VERIFY_ERR`, `NOVERIFY`
            pac_version_status (str): Version status of the new PAC file.
                                       Supported Values: `DEPLOYED`, `STAGE`, `LKG`
            pac_content (str): The actual PAC file content to be validated and cloned.
            delete_version (int, optional): Specifies the PAC file version to replace if the version limit of 10 is reached.

        Keyword Args:
            Additional optional parameters as key-value pairs.

        Returns:
            Tuple: The newly cloned PAC file resource record.

        Example:
            >>> pac_file = zia.clone_pac_file(
                    pac_id=12345,
                    pac_version="1",
                    name="Cloned_Pac_File_01",
                    description="Cloned_Pac_File_01",
                    domain="bd-hashicorp.com",
                    pac_commit_message="Clone of Test_Pac_File_01",
                    pac_verification_status="VERIFY_NOERR",
                    pac_version_status="DEPLOYED",
                    pac_content="function FindProxyForURL(url, host) { return 'PROXY gateway.example.com:80'; }",
                    delete_version=5
                )
        """
        # Step 1: Validate the PAC content
        pac_content = kwargs.get("pac_content")
        if not pac_content:
            raise ValueError("Missing required parameter: pac_content")

        validation_result, _, validation_error = self.validate_pac_file(body=pac_content)
        if validation_error or not validation_result.get("success", False):
            raise Exception(f"PAC content validation failed: {validation_result}")

        # Step 2: Retrieve PAC file details to handle versioning logic
        pac_file_details, _, fetch_error = self.get_pac_file(pac_id)
        if fetch_error:
            raise Exception(f"Failed to retrieve PAC file details: {fetch_error}")

        # Extract pac versions from details
        pac_versions = [entry.get("pacVersion") for entry in pac_file_details] if pac_file_details else []
        total_versions = len(pac_versions)

        # Step 3: Construct the URL with optional delete_version
        if total_versions >= 10:
            delete_version = kwargs.pop("delete_version", None)
            if not delete_version:
                delete_version = min(pac_versions)  # Default to the oldest version if delete_version is not provided
            api_url = format_url(
                f"""
                {self._zia_base_endpoint}
                /pacFiles/{pac_id}/version/{pac_version}?deleteVersion={delete_version}
            """
            )
        else:
            api_url = format_url(
                f"""
                {self._zia_base_endpoint}
                /pacFiles/{pac_id}/version/{pac_version}
            """
            )

        # Step 4: Use the constructor logic to create the request and execute it
        body = kwargs

        request, error = self._request_executor.create_request(
            method="post".upper(),
            endpoint=api_url,
            body=body,
        )

        if error:
            return (None, None, error)

        # Execute the request
        response, error = self._request_executor.execute(request, PacFiles)
        if error:
            return (None, response, error)

        try:
            result = PacFiles(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def validate_pac_file(self, pac_file_content: str) -> tuple:
        """
        Sends the PAC file content for validation and returns the validation result.

        Args:
            pac_file_content (str): The PAC file content to be validated.

        Returns:
            tuple: A tuple containing (validation result, Response, error).

        Example:
            To validate PAC file content:

            >>> pac_file_content = '''
            >>> function FindProxyForURL(url, host) {
            >>>     return "PROXY gateway.example.com:80";
            >>> }
            >>> '''
            >>> validation_result, response, error = client.zia.validate_pac_file(pac_file_content)
            >>> if error:
            >>>     print(f"Validation failed: {error}")
            >>> elif validation_result.get("success", False):
            >>>     print("PAC file is valid.")
            >>> else:
            >>>     print("PAC file validation failed.")
        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /pacFiles/validate
        """
        )

        # Use the PAC file content as the raw body for the request
        body = pac_file_content

        # Create the request
        request, error = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
            body=body,
            headers={"Content-Type": "text/plain"},  # Content-Type should match the API requirements
        )
        if error:
            return (None, None, error)

        # Execute the request
        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        try:
            result = self.form_response_body(response.get_body())
        except Exception as parse_error:
            return (None, response, parse_error)

        return (result, response, None)

    def update_pac_file(
        self, pac_id: int, pac_version: int, pac_version_action: str, new_lkg_ver: int = None, **kwargs
    ) -> tuple:
        """
        Performs the specified action on the PAC file version and updates the file status.
        Supported actions include deploying, staging, unstaging, and marking or unmarking
        the file as last known good version.

        Args:
            pac_id (int): The unique identifier of the PAC file to be updated.
            pac_version (int): The specific version of the PAC file to be updated.
            pac_version_action (str): Action to perform on the PAC version.
                                      Supported Values: `DEPLOY`, `STAGE`, `LKG`, `UNSTAGE`, `REMOVE_LKG`
            new_lkg_ver (int, optional): Specifies a different version to be marked as the last known good version
                                         if the action is removing the current last known good version.

        Keyword Args:
            Additional optional parameters as key-value pairs, including:
                - name (str): The name of the PAC file.
                - description (str): Description of the PAC file.
                - domain (str): The domain associated with the PAC file.
                - pac_commit_message (str): Commit message for the PAC file.
                - pac_verification_status (str): Verification status of the PAC file.
                                                Supported Values: `VERIFY_NOERR`, `VERIFY_ERR`, `NOVERIFY`
                - pac_version_status (str): Version status of the PAC file.
                                            Supported Values: `DEPLOYED`, `STAGE`, `LKG`
                - pac_content (str): The actual PAC file content to be updated.

        Returns:
            tuple: A tuple containing (updated PAC file resource record, Response, error).

        Example:
            >>> pac_file = zia.update_pac_file(
                    pac_id=12345,
                    pac_version=1,
                    pac_version_action="DEPLOY",
                    name="Update_Pac_File_01",
                    description="Update_Pac_File_01",
                    domain="bd-hashicorp.com",
                    pac_commit_message="Update_Pac_File_01",
                    pac_verification_status="VERIFY_NOERR",
                    pac_version_status="DEPLOYED",
                    pac_content="function FindProxyForURL(url, host) { return 'PROXY gateway.example.com:80'; }",
                    new_lkg_ver=5
                )
        """
        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /pacFiles/{pac_id}/version/{pac_version}/action/{pac_version_action}
        """
        )

        # Append optional newLKGVer parameter to the URL if provided
        if new_lkg_ver is not None:
            api_url += f"?newLKGVer={new_lkg_ver}"

        # Construct the body from kwargs
        body = {}
        body.update(kwargs)

        # Create the request
        request, error = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
            body=body,
        )
        if error:
            return (None, None, error)

        # Execute the request
        response, error = self._request_executor.execute(request, PacFiles)
        if error:
            return (None, response, error)

        # Parse the response into a PacFiles instance
        try:
            result = PacFiles(self.form_response_body(response.get_body()))
        except Exception as parse_error:
            return (None, response, parse_error)

        return (result, response, None)

    def delete_pac_file(self, pac_id: int) -> tuple:
        """
        Deletes an existing PAC file including all of its versions based on the specified ID

        Args:
            pac_id (str): Specifies the ID of the PAC file

        Returns:
            tuple: A tuple containing the response object and error (if any).
        """
        http_method = "delete".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /pacFiles/{pac_id}
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
