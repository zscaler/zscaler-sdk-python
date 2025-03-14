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
            **filter (int, optional):
                Retrieves the list of PAC files without the PAC file content in the response
            **search (str, optional):
                Returns PAC files with the names that match the search criteria

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
        pac_version_status: str,
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
            pac_version_action (str): Specifies the action to be performed on the PAC file version.

                                    Supported values:

                                    - `DEPLOY`: ❌ **Cannot transition to any other status**.

                                    - `STAGE`: ✅ **Can transition to** `DEPLOY`, `UNSTAGE`.

                                    - `LKG`: ✅ **Can be set if no status is assigned (`NULL`)**.

                                    - `UNSTAGE`: ✅ **Can transition to** `STAGE`.

                                    - `REMOVE_LKG`: ✅ **Can be set if no status is assigned (`NULL`)**.

                                    **Transition Rules:**

                                    - If the PAC version is `DEPLOYED`, it **cannot** be changed to `STAGE`, `UNSTAGE`, `LKG`, or `REMOVE_LKG`.

                                    - If the PAC version is `STAGE`, it **can** transition to `DEPLOY` or `UNSTAGE`.

                                    - If no PAC version status is assigned (`NULL`), **any** action is allowed.

            name (str): The name of the PAC file.
            description (str): Description of the PAC file.
            domain (str): The domain associated with the PAC file.
            pac_commit_message (str): Commit message for the PAC file.
            pac_verification_status (str): Verification status of the PAC file.
                                        Supported values: `VERIFY_NOERR`, `VERIFY_ERR`, `NOVERIFY`
            pac_version_status (str): Version status of the PAC file.
                                    Supported values: `DEPLOYED`, `STAGE`, `LKG`
            pac_content (str): The actual PAC file content to be updated.
            new_lkg_ver (int, optional): Specifies a different version to be marked as the last known good version
                                        **only if** `pac_version_action` is `REMOVE_LKG`.

        Keyword Args:
            Additional optional parameters as key-value pairs.

        Returns:
            Box: The updated PAC file resource record.

        Raises:
            ValueError: If the requested `pac_version_action` is not a valid transition for the current PAC version status.

        Example:
            >>> pac_file = zia.update_pac_file(
                    pac_id="12345",
                    pac_version="1",
                    pac_version_action="DEPLOY",
                    name="Updated_Pac_File_01",
                    description="Updated_Pac_File_01",
                    domain="acme.com",
                    pac_commit_message="Update_Pac_File_01",
                    pac_verification_status="VERIFY_NOERR",
                    pac_version_status="DEPLOYED",
                    pac_content="function FindProxyForURL(url, host) { return 'PROXY gateway.example.com:80'; }",
                    new_lkg_ver=5
                )
        """
        # Step 1: Retrieve PAC file version details using get_pac_file_version
        pac_file_version_details = self.get_pac_file(pac_id, )
        if not pac_file_version_details:
            raise Exception(f"Failed to retrieve PAC file version details for pac_id {pac_id} and version {pac_version}.")

        # Step 2: Extract the current pacVersionStatus
        current_pac_version_status = pac_file_version_details.get("pacVersionStatus")

        # Step 3: Define valid transition rules
        status_transitions = {
            "DEPLOYED": [],  # Cannot transition to any other status
            "STAGE": ["DEPLOY", "UNSTAGE"],  # Can transition to DEPLOY or UNSTAGE
            None: ["DEPLOY", "STAGE", "UNSTAGE", "LKG", "REMOVE_LKG"],  # Any action is allowed if status is NULL
        }

        # Step 4: Validate Action Transition
        if current_pac_version_status not in status_transitions:
            raise ValueError(f"Unsupported current PAC version status: {current_pac_version_status}.")

        allowed_actions = status_transitions[current_pac_version_status]
        if pac_version_action not in allowed_actions:
            raise ValueError(
                f"Invalid transition: PAC version with status '{current_pac_version_status}' cannot be transitioned to '{pac_version_action}'. "
                f"Allowed actions: {allowed_actions}."
            )

        # Step 5: Validate PAC content
        validation_result = self.validate_pac_file(pac_content)
        if not validation_result.success:
            raise Exception("PAC content validation failed: {}".format(validation_result))

        # Step 6: Construct the URL with required parameters
        url = f"/pacFiles/{pac_id}/version/{pac_version}/action/{pac_version_action}"

        # Step 7: Include newLKGVer only if explicitly provided
        if new_lkg_ver is not None:
            url += f"?newLKGVer={new_lkg_ver}"

        # Step 8: Construct the payload with required fields
        payload = {
            "name": name,
            "description": description,
            "domain": domain,
            "pacCommitMessage": pac_commit_message,
            "pacVerificationStatus": pac_verification_status,
            "pacVersionStatus": pac_version_status,
            "pacContent": pac_content,
            "pacVersion": pac_version,
        }

        # Add any additional optional parameters
        for key, value in kwargs.items():
            payload[snake_to_camel(key)] = value

        # Step 9: Make the request to update the PAC file
        response = self.rest.put(url, json=payload)
        if isinstance(response, Response):
            if response.status_code != 200:
                raise Exception(f"API call failed with status {response.status_code}: {response.json()}")
            return Box(response.json())
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
                                      Supported Values: `DEPLOYED`
            pac_content (str): The actual PAC file content to be validated and cloned.

        Keyword Args:
            Additional optional parameters as key-value pairs.

        Returns:
            Box: The newly added PAC file resource record.

        Example:
            >>> pac_file = zia.add_pac_file(
                    name="Test_Pac_File_01",
                    description="Test_Pac_File_01",
                    domain="acme.com",
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
        delete_version: int = None,  # Must be explicitly provided by the user
        **kwargs,
    ) -> Box:
        """
        Clones an existing PAC file by creating a new PAC file based on the specified PAC ID and version.

        Args:
            pac_id (str): The unique identifier of the PAC file to be cloned.
            pac_version (str): The specific version of the PAC file to be cloned.
            name (str): The name of the new PAC file.
            description (str): Description of the new PAC file.
            domain (str): The domain associated with the new PAC file.
            pac_commit_message (str): Commit message for the new PAC file.
            pac_verification_status (str): Verification status of the new PAC file.
            pac_version_status (str): Version status of the new PAC file.
                                    Supported Values: `DEPLOYED`
            pac_content (str): The actual PAC file content to be validated and cloned.
            delete_version (int, optional): Specifies the PAC file version to replace if the version limit of 10 is reached.
                                            - Only included if explicitly provided **AND** the PAC version count is **= 10**.

        Keyword Args:
            Additional optional parameters as key-value pairs.

        Returns:
            Box: The newly cloned PAC file resource record.

        Raises:
            ValueError: If the number of PAC versions is exactly `10` and `delete_version` is not provided.

        Example:
            >>> pac_file = zia.clone_pac_file(
                    pac_id="12345",
                    pac_version="1",
                    name="Cloned_Pac_File_01",
                    description="Cloned_Pac_File_01",
                    domain="acme.com",
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
            raise Exception(f"PAC content validation failed: {validation_result}")

        # Step 2: Fetch existing PAC file versions for the given pac_id with pac_content filter
        pac_file_details = self.get_pac_file(pac_id, filter="pac_content")

        # Ensure we have a valid response
        if not pac_file_details or not isinstance(pac_file_details, list):
            raise Exception(f"Failed to retrieve PAC file versions for pac_id {pac_id}")

        # Extract PAC versions from details
        total_versions = sum(1 for entry in pac_file_details if "id" in entry)

        # Step 3: Check if the PAC file count has reached the limit
        if total_versions == 10 and delete_version is None:
            raise ValueError(
                f"The PAC file version limit of 10 has been reached. You must specify `delete_version` to indicate which version to remove."
            )

        # Step 4: Construct the URL (Includes deleteVersion only if explicitly set and needed)
        delete_version_param = f"?deleteVersion={delete_version}" if delete_version is not None and total_versions == 10 else ""
        url = f"/pacFiles/{pac_id}/version/{pac_version}{delete_version_param}"

        # Step 5: Construct the payload with mandatory fields
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

        # Step 6: Make the request to clone the PAC file
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
        pac_version_status: str,
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
            pac_version_action (str): Specifies the action to be performed on the PAC file version.

                                    Supported values:

                                    - `DEPLOY`: ❌ **Cannot transition to any other status**.

                                    - `STAGE`: ✅ **Can transition to** `DEPLOY`, `UNSTAGE`.

                                    - `LKG`: ✅ **Can be set if no status is assigned (`NULL`)**.

                                    - `UNSTAGE`: ✅ **Can transition to** `STAGE`.

                                    - `REMOVE_LKG`: ✅ **Can be set if no status is assigned (`NULL`)**.

                                    **Transition Rules:**

                                    - If the PAC version is `DEPLOYED`, it **cannot** be changed to `STAGE`, `UNSTAGE`, `LKG`, or `REMOVE_LKG`.

                                    - If the PAC version is `STAGE`, it **can** transition to `DEPLOY` or `UNSTAGE`.

                                    - If no PAC version status is assigned (`NULL`), **any** action is allowed.

            name (str): The name of the PAC file.
            description (str): Description of the PAC file.
            domain (str): The domain associated with the PAC file.
            pac_commit_message (str): Commit message for the PAC file.
            pac_verification_status (str): Verification status of the PAC file.
                                        Supported values: `VERIFY_NOERR`, `VERIFY_ERR`, `NOVERIFY`
            pac_version_status (str): Version status of the PAC file.
                                    Supported values: `DEPLOYED`, `STAGE`, `LKG`
            pac_content (str): The actual PAC file content to be updated.
            new_lkg_ver (int, optional): Specifies a different version to be marked as the last known good version
                                        **only if** `pac_version_action` is `REMOVE_LKG`.

        Keyword Args:
            Additional optional parameters as key-value pairs.

        Returns:
            Box: The updated PAC file resource record.

        Raises:
            ValueError: If the requested `pac_version_action` is not a valid transition for the current PAC version status.

        Example:
            >>> pac_file = zia.update_pac_file(
                    pac_id="12345",
                    pac_version="1",
                    pac_version_action="DEPLOY",
                    name="Updated_Pac_File_01",
                    description="Updated_Pac_File_01",
                    domain="acme.com",
                    pac_commit_message="Update_Pac_File_01",
                    pac_verification_status="VERIFY_NOERR",
                    pac_version_status="DEPLOYED",
                    pac_content="function FindProxyForURL(url, host) { return 'PROXY example.com:80'; }",
                    new_lkg_ver=5
                )
        """

        # Step 1: Retrieve PAC file version details before making an update request
        pac_file_version = self.get_pac_file_version(pac_id, pac_version)

        if not pac_file_version or not isinstance(pac_file_version, dict):
            raise Exception(f"Failed to retrieve PAC file version details for pac_id {pac_id}, version {pac_version}")

        # Extract the current PAC version status from API response
        current_pac_version_status = pac_file_version.get("pacVersionStatus")

        # Define valid transition rules
        status_transitions = {
            "DEPLOYED": [],
            "STAGE": ["DEPLOY", "UNSTAGE"],
            None: ["DEPLOY", "STAGE", "UNSTAGE", "LKG", "REMOVE_LKG"],
        }

        # Step 2: Validate Action Transition Before Making an API Call
        if current_pac_version_status not in status_transitions:
            raise ValueError(
                f"Unknown PAC version status: '{current_pac_version_status}'. Please check API documentation."
            )

        allowed_actions = status_transitions[current_pac_version_status]
        if allowed_actions and pac_version_action not in allowed_actions:
            raise ValueError(
                f"Invalid transition: PAC version with status '{current_pac_version_status}' cannot be transitioned to '{pac_version_action}'. "
                f"Allowed actions: {allowed_actions}.\nPlease check the transition rules in the function docstring."
            )

        # Step 3: Validate PAC content
        validation_result = self.validate_pac_file(pac_content)
        if not validation_result.success:
            raise Exception("PAC content validation failed: {}".format(validation_result))

        # Step 4: Construct the URL with required parameters
        url = f"/pacFiles/{pac_id}/version/{pac_version}/action/{pac_version_action}"

        # Step 5: Include newLKGVer only if explicitly provided
        if new_lkg_ver is not None:
            url += f"?newLKGVer={new_lkg_ver}"

        # Step 6: Construct the payload with required fields
        payload = {
            "name": name,
            "description": description,
            "domain": domain,
            "pacCommitMessage": pac_commit_message,
            "pacVerificationStatus": pac_verification_status,
            "pacVersionStatus": pac_version_status,
            "pacContent": pac_content,
            "pacVersion": pac_version,
        }

        # Add any additional optional parameters
        for key, value in kwargs.items():
            payload[snake_to_camel(key)] = value

        # Step 7: Make the request to update the PAC file
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
