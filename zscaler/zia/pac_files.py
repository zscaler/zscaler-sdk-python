# -*- coding: utf-8 -*-

# Copyright (c) 2023, Zscaler Inc.
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.


from box import Box, BoxList
from requests import Response

from zscaler.utils import snake_to_camel
from zscaler.zia import ZIAClient


class PacFilesAPI:
    def __init__(self, client: ZIAClient):
        self.rest = client

    def list_pac_files(self, **kwargs) -> BoxList:
        """
        Returns the list of ZIA Pac Files.

        Keyword Args:
            **max_items (int, optional):
                The maximum number of items to request before stopping iteration.
            **max_pages (int, optional):
                The maximum number of pages to request before stopping iteration.
            **page_size (int, optional):
                Specifies the page size. The default size is 100, but the maximum size is 1000.

        Returns:
            :obj:`BoxList`: The list of PAC Files configured in ZIA.

        Examples:
            List PAC Files using default settings:

            >>> for pac_files in zia.pac_files.list_pac_files():
            ...   print(pac_files)

        """
        list, _ = self.rest.get_paginated_data(path="/pacFiles", **kwargs)
        return list

    def get_pac_file(self, pac_id: str, filter: str = None) -> Box:
        """
        Returns the PAC file details for a given PAC ID.

        Args:
            pac_id (str): The unique identifier for the PAC file.
            filter (str, optional): Excludes specific information about the PAC file from
                                    the response such as the PAC file content.
                                    Accepts only the value 'pac_content'.

        Returns:
            :obj:`Box`: The PAC file resource record.

        Example:
            >>> pac_file = zia.get_pac_file('12345', filter='pac_content')
        """
        # Construct URL with optional filter
        url = f"/pacFiles/{pac_id}/version"
        if filter == "pac_content":
            url += f"?filter={filter}"

        response = self.rest.get(url)
        if isinstance(response, Response):
            if response.status_code != 200:
                return None
        return response

    def get_pac_file_version(self, pac_id: str, pac_version: str, filter: str = None) -> Box:
        """
        Returns the PAC file version details for a given PAC ID and version.

        Args:
            pac_id (str): The unique identifier for the PAC file.
            pac_version (str): The specific version of the PAC file.
            filter (str, optional): Excludes specific information about the PAC file from
                                    the response such as the PAC file content.
                                    Accepts only the value 'pac_content'.

        Returns:
            :obj:`Box`: The PAC file version resource record.

        Example:
            >>> pac_file_version = zia.get_pac_file_version('12345', '1', filter='pac_content')
        """
        # Construct URL with optional filter
        url = f"/pacFiles/{pac_id}/version/{pac_version}"
        if filter == "pac_content":
            url += f"?filter={filter}"

        response = self.rest.get(url)
        if isinstance(response, Response):
            if response.status_code != 200:
                return None
        return response

    def validate_pac_file(self, pac_file_content: str) -> Box:
        """
        Sends the PAC file content for validation and returns the validation result.

        Args:
            pac_file_content (str): The PAC file content to be validated.

        Returns:
            Box: The API response containing the validation result.

        Raises:
            Exception: If the API call fails with a non-2xx status code.

        Example:
            To validate PAC file content:

            .. code-block:: python

                pac_file_content = '''
                function FindProxyForURL(url, host) {
                    return "PROXY gateway.example.com:80";
                }
                '''
                
                response = client.validate_pac_file(pac_file_content=pac_file_content)
                if response["success"]:
                    print("PAC file is valid.")
                else:
                    print("PAC file validation failed.")
        """
        # Send only the PAC content as the raw body
        response = self.rest.post("pacFiles/validate", data=pac_file_content)

        # Check if the response is successful and already in Box format
        if isinstance(response, Box):
            return response
        elif isinstance(response, Response):
            if response.status_code != 200:
                raise Exception(f"API call failed with status {response.status_code}: {response.json()}")
            # Convert to Box if needed
            return Box(response.json())

    def add_pac_file(
        self,
        name: str,
        description: str,
        domain: str,
        pac_commit_message: str,
        pac_verification_status: str,
        pac_version_status: str,
        pac_content: str,
        **kwargs,
    ) -> Box:
        """
        Adds a new custom PAC file after validating the PAC content.

        Args:
            name (str): The name of the new PAC file.
            description (str): The description of the new PAC file.
            domain (str): The domain of your organization to which the PAC file applies.
            pac_commit_message (str): The commit message entered while saving the PAC file version as indicated by the pacVersion field.
            pac_verification_status (str): Indicates the verification status of the PAC file and if any errors are identified in the syntax.
                                           Supported Values: `VERIFY_NOERR`, `VERIFY_ERR`, `NOVERIFY`
            pac_version_status (str): Version status of the new PAC file.
                                      Supported Values: `DEPLOYED`, `STAGE`, `LKG`
            pac_content (str): The actual PAC file content to be validated and cloned.

        Keyword Args:
            Additional optional parameters as key-value pairs.

        Returns:
            Box: The newly added PAC file resource record.

        Example:
            >>> pac_file = zia.add_pac_file(
                    name="Test_Pac_File_01",
                    description="Test_Pac_File_01",
                    domain="bd-hashicorp.com",
                    pacCommitMessage="Test_Pac_File_01",
                    pacVerificationStatus="VERIFY_NOERR",
                    pacVersionStatus="DEPLOYED",
                    pacContent="function FindProxyForURL(url, host) { return 'PROXY gateway.example.com:80'; }"
                )
        """
        validation_result = self.validate_pac_file(pac_content)
        if not validation_result.success:
            raise Exception("PAC content validation failed: {}".format(validation_result))

        payload = {
            "name": name,
            "description": description,
            "domain": domain,
            "pacCommitMessage": pac_commit_message,
            "pacVerificationStatus": pac_verification_status,
            "pacVersionStatus": pac_version_status,
            "pacContent": pac_content,
        }

        for key, value in kwargs.items():
            payload[snake_to_camel(key)] = value

        response = self.rest.post("pacFiles", json=payload)
        if isinstance(response, Response):
            if response.status_code != 200:
                raise Exception(f"API call failed with status {response.status_code}: {response.json()}")
            return Box(response.json())
        return response

    def clone_pac_file(
        self,
        pac_id: str,
        pac_version: str,
        name: str,
        description: str,
        domain: str,
        pac_commit_message: str,
        pac_verification_status: str,
        pac_version_status: str,
        pac_content: str,
        delete_version: int = None,
        **kwargs,
    ) -> Box:
        """
        Clones an existing PAC file by creating a new PAC file based on the specified PAC ID and version.

        Args:
            pac_id (str): The unique identifier of the PAC file to be cloned.
            pac_version (str): The specific version of the PAC file to be cloned.
            name (str): The name of the new PAC file.
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
            Box: The newly cloned PAC file resource record.

        Example:
            >>> pac_file = zia.clone_pac_file(
                    pac_id="12345",
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
        validation_result = self.validate_pac_file(pac_content)
        if not validation_result.success:
            raise Exception("PAC content validation failed: {}".format(validation_result))

        # Step 2: Check the number of PAC file versions
        pac_file_details = self.get_pac_file(pac_id)
        if isinstance(pac_file_details, Box):
            pac_file_details = pac_file_details.to_list()  # Convert Box to a list of dictionaries if needed

        # Extract pac versions from details
        pac_versions = [entry.get("pacVersion") for entry in pac_file_details] if pac_file_details else []
        total_versions = len(pac_versions)

        # Step 3: Decide on including delete_version in the URL
        if total_versions >= 10:
            if delete_version is None:
                # If delete_version was not provided, default to the oldest version (smallest number)
                delete_version = min(pac_versions)
            url = f"/pacFiles/{pac_id}/version/{pac_version}?deleteVersion={delete_version}"
        else:
            url = f"/pacFiles/{pac_id}/version/{pac_version}"

        # Step 4: Construct the payload with mandatory fields
        payload = {
            "name": name,
            "description": description,
            "domain": domain,
            "pacCommitMessage": pac_commit_message,
            "pacVerificationStatus": pac_verification_status,
            "pacVersionStatus": pac_version_status,
            "pacContent": pac_content,
        }

        # Add any additional optional parameters
        for key, value in kwargs.items():
            payload[snake_to_camel(key)] = value

        # Step 5: Make the request to clone the PAC file
        response = self.rest.post(url, json=payload)
        if isinstance(response, Response):
            if response.status_code != 200:
                raise Exception(f"API call failed with status {response.status_code}: {response.json()}")
            return Box(response.json())
        return response

    def update_pac_file(
        self,
        pac_id: str,
        pac_version: str,
        pac_version_action: str,
        name: str,
        description: str,
        domain: str,
        pac_commit_message: str,
        pac_verification_status: str,
        # pac_version_status: str,
        pac_content: str,
        new_lkg_ver: int = None,
        **kwargs,
    ) -> Box:
        """
        Performs the specified action on the PAC file version and updates the file status.
        Supported actions include deploying, staging, unstaging, and marking or unmarking
        the file as last known good version.

        Args:
            pac_id (str): The unique identifier of the PAC file to be updated.
            pac_version (str): The specific version of the PAC file to be updated.
            pac_version_action (str): Action to perform on the PAC version.
                                    Supported Values: `DEPLOY`, `STAGE`, `LKG`, `UNSTAGE`, `REMOVE_LKG`
            name (str): The name of the PAC file.
            description (str): Description of the PAC file.
            domain (str): The domain associated with the PAC file.
            pac_commit_message (str): Commit message for the PAC file.
            pac_verification_status (str): Verification status of the PAC file.
                                        Supported Values: `VERIFY_NOERR`, `VERIFY_ERR`, `NOVERIFY`
            pac_version_status (str): Version status of the PAC file.
                                    Supported Values: `DEPLOYED`, `STAGE`, `LKG`
            pac_content (str): The actual PAC file content to be updated.
            new_lkg_ver (int, optional): Specifies a different version to be marked as the last known good version
                                        if the action is removing the current last known good version.

        Keyword Args:
            Additional optional parameters as key-value pairs.

        Returns:
            Box: The updated PAC file resource record.

        Example:
            >>> pac_file = zia.update_pac_file(
                    pac_id="12345",
                    pac_version="1",
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
        # Step 1: Validate the PAC content
        validation_result = self.validate_pac_file(pac_content)
        if not validation_result.success:
            raise Exception("PAC content validation failed: {}".format(validation_result))

        # Step 2: Construct the URL with mandatory parameters and optional newLKGVer
        url = f"/pacFiles/{pac_id}/version/{pac_version}/action/{pac_version_action}"
        if new_lkg_ver is not None:
            url += f"?newLKGVer={new_lkg_ver}"

        # Step 3: Construct the payload with required fields
        payload = {
            "name": name,
            "description": description,
            "domain": domain,
            "pacCommitMessage": pac_commit_message,
            "pacVerificationStatus": pac_verification_status,
            # "pacVersionStatus": pac_version_status,
            "pacContent": pac_content,
        }

        # Add any additional optional parameters
        for key, value in kwargs.items():
            payload[snake_to_camel(key)] = value

        # Step 4: Make the request to update the PAC file
        response = self.rest.put(url, json=payload)
        if isinstance(response, Response):
            if response.status_code != 200:
                raise Exception(f"API call failed with status {response.status_code}: {response.json()}")
            return Box(response.json())
        return response

    def delete_pac_file(self, pac_id):
        """
        Deletes the specified Pac File.

        Args:
            pac_id (str): The unique identifier of the Pac File that will be deleted.

        Returns:
            :obj:`int`: The response code for the request.

        Examples
            >>> user = zia.pac_files.delete_pac_file('99999')

        """
        return self.rest.delete(f"pacFiles/{pac_id}").status_code

