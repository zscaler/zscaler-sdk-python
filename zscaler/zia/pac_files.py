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

from typing import Dict, List, Optional, Any, Union
from zscaler.api_client import APIClient
from zscaler.request_executor import RequestExecutor
from zscaler.zia.models.pac_files import PacFiles
from zscaler.zia.models.pac_files import PacFileValidationResponse
from zscaler.utils import format_url
from zscaler.types import APIResult
import textwrap


class PacFilesAPI(APIClient):
    """
    A Client object for the Rule labels resource.
    """

    _zia_base_endpoint = "/zia/api/v1"

    def __init__(self, request_executor: "RequestExecutor") -> None:
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def list_pac_files(self, query_params: Optional[dict] = None) -> APIResult[List[PacFiles]]:
        """
        Lists pac files in your organization with pagination.
        A subset of pac files can be returned that match a supported
        filter expression or query.

        Args:
            query_params {dict}: Map of query parameters for the request.
                ``[query_params.search]`` {str}: Search string for filtering results.

                ``[query_params.filter]`` {str}: Excludes specific information about the PAC file
                    from the response such as the PAC file content
                    Available values: pac_content

                ``[query_params.page]`` {str}: Specifies the page offset

                ``[query_params.page_size]`` {str}: Specifies the page size. The default size is 100.

        Returns:
            tuple: A tuple containing (list of Pac Files instances, Response, error)

        Examples:
            Retrieves the list of all PAC files in deployed state

            >>> pac_file_list, _, error = client.zia.pac_files.list_pac_files()
            >>> if error:
            ...     print(f"Error listing all pac files: {error}")
            ...     return
            ... print(f"Total pac files found: {len(pac_file_list)}")

        Examples:
            Retrieves the list of all PAC files in deployed state excluding pac_content

            >>> pac_file_list, _, error = client.zia.pac_files.list_pac_files(query_params={
            ... 'search': 'kerberos.pac', 'filter':'pac_content'})
            >>> if error:
            ...     print(f"Error listing all pac files: {error}")
            ...     return
            ... print(f"Total pac files found: {len(pac_file_list)}")


            Client-side filtering with JMESPath:

            The response object supports client-side filtering and
            projection via ``resp.search(expression)``.  See the
            `JMESPath documentation <https://jmespath.org/>`_ for
            expression syntax.

        """
        http_method = "get".upper()
        api_url = format_url(f"""
            {self._zia_base_endpoint}
            /pacFiles
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
                result.append(PacFiles(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_pac_file(
        self,
        pac_id: int,
        query_params: Optional[dict] = None,
    ) -> APIResult[dict]:
        """
        Retrieves all versions of a PAC file based on the specified ID

        Args:
            query_params {dict}: Map of query parameters for the request.

                ``[query_params.filter]`` {str}: Excludes specific information about the PAC file
                    from the response such as the PAC file content. Available values: `pac_content`

            pac_id (int): The unique identifier for the Pac File.

        Returns:
            tuple: A tuple containing (Pac File instance, Response, error).

        Examples:
            Gets a list of all pac files including the pac content.

            >>> pac_files, _, error = client.zia.pac_files.get_pac_file('18805')
            >>> if error:
            ...     print(f"Error fetching PAC files by ID: {error}")
            ...     return
            ... print(f"Total PAC file versions fetched: {len(pac_files)}")
            ... for version in pac_files:
            ...     print(version.as_dict())

            Gets a list of all pac files excluding the pac content.

            >>> pac_files, _, error = client.zia.pac_files.get_pac_file('18805', query_params={'filter': 'pac_content'})
            >>> if error:
            ...     print(f"Error fetching PAC files by ID: {error}")
            ...     return
            ... print(f"Total PAC file versions fetched: {len(pac_files)}")
            ... for version in pac_files:
            ...     print(version.as_dict())

        """
        http_method = "get".upper()
        api_url = format_url(f"""
            {self._zia_base_endpoint}
            /pacFiles/{pac_id}/version
        """)

        query_params = query_params or {}

        request, error = self._request_executor.create_request(method=http_method, endpoint=api_url, params=query_params)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, PacFiles)
        if error:
            return (None, response, error)

        try:
            result = []
            for item in response.get_results():
                result.append(PacFiles(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_pac_file_version(self, pac_id: int, pac_version: int, query_params: Optional[dict] = None) -> APIResult[dict]:
        """
        Returns the PAC file version details for a given PAC ID and version.

        Args:
            query_params {dict}: Map of query parameters for the request.

                ``[query_params.filter]`` {str, optional}: Excludes specific information about the PAC file
                                    the response such as the PAC file content.
                                    Accepts only the value 'pac_content'

            pac_id (str): The unique identifier for the PAC file.
            pac_version (str): The specific version of the PAC file.

        Returns:
            :obj:`Tuple`: The PAC file version resource record.

            Gets a list of all pac files excluding the pac content.

            >>> pac_files, _, error = client.zia.pac_files.get_pac_file_version(pac_id='18805', pac_version='1',
            ... query_params={'filter': 'pac_content'})
            >>> if error:
            ...     print(f"Error fetching pac_file by ID: {error}")
            ...     return
            ... print(f"Fetched pac_file by ID: {pac_file.as_dict()}")
        """
        http_method = "get".upper()
        api_url = format_url(f"""
            {self._zia_base_endpoint}
            /pacFiles/{pac_id}/version/{pac_version}
        """)

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

    def add_pac_file(self, **kwargs) -> APIResult[dict]:
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
            ...     name="Test_Pac_File_01",
            ...     description="Test_Pac_File_01",
            ...     domain="bd-hashicorp.com",
            ...     pac_commit_message="Test_Pac_File_01",
            ...     pac_verification_status="VERIFY_NOERR",
            ...     pac_version_status="DEPLOYED",
            ...     pac_content="function FindProxyForURL(url, host) { return 'PROXY gateway.example.com:80'; }")
        """
        # Validate the PAC file content before proceeding
        pac_content = kwargs.get("pac_content")
        if not pac_content:
            raise ValueError("Missing required parameter: pac_content")

        validation_result, _, validation_error = self.validate_pac_file(pac_file_content=pac_content)
        if validation_error or not validation_result.get("success", False):
            raise Exception(f"PAC content validation failed: {validation_result}")

        # Preserve the existing logic for payload and request
        http_method = "post".upper()
        api_url = format_url(f"""
            {self._zia_base_endpoint}
            /pacFiles
        """)

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

    def clone_pac_file(
        self,
        pac_id: int,
        pac_version: str,
        pac_content: str,
        pac_version_status: str,
        pac_verification_status: str = "VERIFY_NOERR",
        pac_commit_message: str = "",
        delete_version: Optional[int] = None,
    ) -> APIResult[dict]:
        """
        Branch an existing PAC file by creating a new VERSION inside it
        (``POST /pacFiles/{pacId}/version/{clonedPacVersion}``).

        This endpoint creates a new version inside an existing PAC file
        parent. The parent identity (name, description, domain,
        editable, pacUrlObfuscated) is fixed by the ``pac_id`` in the
        path and CANNOT be supplied here. Only version-level fields go
        in the body:

            pacContent
            pacVerificationStatus
            pacCommitMessage
            pacVersionStatus

        Sending parent-level fields (name/description/domain/...) or
        the path parameter ``pacVersion`` in the body causes the API to
        reject the request with a misleading 400 RESOURCE_NOT_FOUND
        instead of a proper INVALID_INPUT_ARGUMENT, which is why this
        function is a strict signature -- not ``**kwargs`` -- so callers
        can't accidentally trigger that trap.

        The clone POST must be made against COMMITTED state. If you
        created the parent earlier in the same session, call
        ``client.zia.activate.activate()`` BEFORE calling this method,
        otherwise the parent will not yet be visible to the clone
        endpoint and you will get the same 400 RESOURCE_NOT_FOUND.

        Args:
            pac_id (int): The unique identifier of the existing PAC
                file (the parent) to branch FROM.
            pac_version (str): The version number to branch from
                (the source version, NOT the new version number --
                the new version is server-assigned).
            pac_content (str): The PAC file JS body for the new
                version. This is what makes the new version different
                from the source.
            pac_version_status (str): Lifecycle status for the new
                version. Supported values: ``DEPLOYED``, ``STAGE``,
                ``LKG``. Unlike the seed version on
                :meth:`add_pac_file` (which must be ``DEPLOYED``), a
                cloned version may be created in any of these states
                because the parent already has a deployed baseline.
            pac_verification_status (str): Verification status to
                stamp on the new version. Defaults to
                ``VERIFY_NOERR``. Supported values: ``VERIFY_NOERR``,
                ``VERIFY_ERR``, ``NOVERIFY``.
            pac_commit_message (str): Commit message for the new
                version (shown in the policy table next to the
                version number).
            delete_version (int, optional): Only meaningful when the
                parent already has 10 versions (the per-PAC-file
                cap). When supplied, it points at the version to
                evict to make room for this new one. When omitted at
                the cap, the SDK evicts the oldest version
                automatically.

        Returns:
            tuple: A 3-tuple of
            ``(PacFiles | None, Response | None, Exception | None)``.

        Example:
            >>> # Branch v1 of an existing PAC file into a new STAGE
            >>> # version (v2). Note: parent identity (name/domain) is
            >>> # implicit from pac_id and is NOT passed here.
            >>> cloned, _, err = client.zia.pac_files.clone_pac_file(
            ...     pac_id=50883,
            ...     pac_version="1",
            ...     pac_content="function FindProxyForURL(url, host) { return 'PROXY gateway.example.com:9400'; }",
            ...     pac_version_status="STAGE",
            ...     pac_commit_message="branch from v1: switch to port 9400",
            ... )
        """
        if not pac_content:
            raise ValueError("Missing required parameter: pac_content")

        # Step 1: pre-validate the PAC content. We do this client-side
        # first so a broken PAC is rejected before we mutate the parent.
        validation_result, _, validation_error = self.validate_pac_file(pac_file_content=pac_content)
        if validation_error or not validation_result.get("success", False):
            raise Exception(f"PAC content validation failed: {validation_result}")

        # Step 2: count existing versions so we can manage the 10-cap.
        # ``get_pac_file`` returns ``PacFiles`` model instances, so we
        # read the snake_case attribute, not the camelCase API key.
        pac_file_details, _, fetch_error = self.get_pac_file(pac_id)
        if fetch_error:
            raise Exception(f"Failed to retrieve PAC file details: {fetch_error}")

        pac_versions = [entry.pac_version for entry in (pac_file_details or [])]
        pac_versions = [v for v in pac_versions if v is not None]
        total_versions = len(pac_versions)

        # Step 3: construct the URL. ZIA caps each PAC file at 10
        # versions; at the cap we must pin ``deleteVersion`` to free a
        # slot. We honour the caller's choice or default to evicting
        # the oldest version.
        if total_versions >= 10:
            evict = delete_version if delete_version is not None else min(pac_versions)
            api_url = format_url(f"""
                {self._zia_base_endpoint}
                /pacFiles/{pac_id}/version/{pac_version}?deleteVersion={evict}
            """)
        else:
            api_url = format_url(f"""
                {self._zia_base_endpoint}
                /pacFiles/{pac_id}/version/{pac_version}
            """)

        # Step 4: build the body with ONLY the four fields the clone
        # endpoint accepts (this matches the payload the ZIA Admin UI
        # sends from the "Create Branch" dialog). Anything else --
        # parent identity fields like name/description/domain, or the
        # path param pacVersion -- causes a confusing 400
        # RESOURCE_NOT_FOUND from the API.
        body = {
            "pac_content": pac_content,
            "pac_verification_status": pac_verification_status,
            "pac_commit_message": pac_commit_message,
            "pac_version_status": pac_version_status,
        }

        request, error = self._request_executor.create_request(
            method="post".upper(),
            endpoint=api_url,
            body=body,
        )

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

    def validate_pac_file(self, pac_file_content: str) -> APIResult[dict]:
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
            ...     print(f"Validation failed: {error}")
            ... elif validation_result.get("success", False):
            ...     print("PAC file is valid.")
            ... else:
            ...     print("PAC file validation failed.")
        """
        http_method = "post".upper()
        api_url = format_url(f"""
            {self._zia_base_endpoint}
            /pacFiles/validate
        """)

        # Normalize so validator sees the function at line 1
        pac = textwrap.dedent(pac_file_content).lstrip("\r\n")

        # Send the PAC content as raw data
        request, error = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
            body=pac,
        )
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        try:
            result = PacFileValidationResponse(self.form_response_body(response.get_body()))
        except Exception as parse_error:
            return (None, response, parse_error)

        return (result, response, None)

    def update_pac_file(
        self, pac_id: int, pac_version: int, pac_version_action: str, new_lkg_ver: int = None, **kwargs
    ) -> APIResult[dict]:
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
            ...     pac_id=12345,
            ...     pac_version=1,
            ...     pac_version_action="DEPLOY",
            ...     name="Update_Pac_File_01",
            ...     description="Update_Pac_File_01",
            ...     domain="bd-hashicorp.com",
            ...     pac_commit_message="Update_Pac_File_01",
            ...     pac_verification_status="VERIFY_NOERR",
            ...     pac_version_status="DEPLOYED",
            ...     pac_content="function FindProxyForURL(url, host) { return 'PROXY gateway.example.com:80'; }",
            ...     new_lkg_ver=5
            ... )
        """
        http_method = "put".upper()
        api_url = format_url(f"""
            {self._zia_base_endpoint}
            /pacFiles/{pac_id}/version/{pac_version}/action/{pac_version_action}
        """)

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

    def delete_pac_file(self, pac_id: int) -> APIResult[dict]:
        """
        Deletes an existing PAC file including all of its versions based on the specified ID

        Args:
            pac_id (str): Specifies the ID of the PAC file

        Returns:
            tuple: A tuple containing the response object and error (if any).

        Example:
            >>> _, _, error = client.zia.pac_files.delete_pac_file('18805')
            >>> if error:
            ...     print(f"Error deleting pac file: {error}")
            ...     return
            ... print(f"Pac File with ID '18805'} deleted successfully.")
        """
        http_method = "delete".upper()
        api_url = format_url(f"""
            {self._zia_base_endpoint}
            /pacFiles/{pac_id}
        """)

        params = {}

        request, error = self._request_executor.create_request(http_method, api_url, params=params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)
        return (None, response, None)
