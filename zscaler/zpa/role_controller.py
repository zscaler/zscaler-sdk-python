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

# from zscaler.api_client import APIClient
# from zscaler.request_executor import RequestExecutor
# from zscaler.zpa.models.role_controller import RoleController
# from zscaler.utils import format_url


# class RoleControllerAPI(APIClient):
#     """
#     A client object for the Role Controller resource.
#     """

#     def __init__(self, request_executor, config):
#         super().__init__()
#         self._request_executor: RequestExecutor = request_executor
#         customer_id = config["client"].get("customerId")
#         self._zpa_base_endpoint = f"/zpa/mgmtconfig/v1/admin/customers/{customer_id}"

#     def list_roles(self, query_params=None) -> tuple:
#         """
#         Get All configured roles.

#         Args:
#             query_params {dict}: Map of query parameters for the request.
#                 ``[query_params.microtenant_id]`` {str}: ID of the microtenant, if applicable.

#         Returns:
#             :obj:`Tuple`: A tuple containing (list of RoleController instances, Response, error)

#         Example:
#             Fetch all roles without filtering

#             >>> role_list, _, err = client.zpa.role_controller.list_roles()
#             ... if err:
#             ...     print(f"Error listing roles: {err}")
#             ...     return
#             ... print(f"Total roles found: {len(role_list)}")
#             ... for role in role_list:
#             ...     print(role.as_dict())
#         """
#         http_method = "get".upper()
#         api_url = format_url(
#             f"""
#             {self._zpa_base_endpoint}
#             /roles
#         """
#         )

#         query_params = query_params or {}
#         microtenant_id = query_params.get("microtenant_id", None)
#         if microtenant_id:
#             query_params["microtenantId"] = microtenant_id

#         request, error = self._request_executor.create_request(http_method, api_url, params=query_params)
#         if error:
#             return (None, None, error)

#         response, error = self._request_executor.execute(request)
#         if error:
#             return (None, response, error)

#         try:
#             result = []
#             for item in response.get_results():
#                 result.append(RoleController(self.form_response_body(item)))
#         except Exception as error:
#             return (None, response, error)
#         return (result, response, None)

#     def get_role(self, role_id: str, query_params=None) -> tuple:
#         """
#         Gets information on the specified role by ID.

#         Args:
#             role_id (str): The unique identifier of the role.
#             query_params (dict, optional): Map of query parameters for the request.
#                 ``[query_params.microtenant_id]`` {str}: The microtenant ID, if applicable.

#         Returns:
#             :obj:`Tuple`: RoleController: The corresponding role object.

#         Example:
#             Retrieve details of a specific role

#             >>> fetched_role, _, err = client.zpa.role_controller.get_role('999999')
#             ... if err:
#             ...     print(f"Error fetching role by ID: {err}")
#             ...     return
#             ... print(f"Fetched role by ID: {fetched_role.as_dict()}")
#         """
#         http_method = "get".upper()
#         api_url = format_url(
#             f"""
#             {self._zpa_base_endpoint}
#             /roles/{role_id}
#         """
#         )

#         query_params = query_params or {}
#         microtenant_id = query_params.get("microtenant_id", None)
#         if microtenant_id:
#             query_params["microtenantId"] = microtenant_id

#         request, error = self._request_executor.create_request(http_method, api_url, params=query_params)
#         if error:
#             return (None, None, error)

#         response, error = self._request_executor.execute(request, RoleController)
#         if error:
#             return (None, response, error)

#         try:
#             result = RoleController(self.form_response_body(response.get_body()))
#         except Exception as error:
#             return (None, response, error)
#         return (result, response, None)

#     def add_role(self, **kwargs) -> tuple:
#         """
#         Adds a new role.

#         Args:
#             name (str): The name of the role.
#             description (str): The description of the role.

#         Returns:
#             :obj:`Tuple`: RoleController: The created role object.

#         Example:
#             # Basic example: Add a new role
#             >>> added_role, _, err = zpa.role_controller.add_role(
#             ...     name="Example Group",
#             ...     description="This is an example segment group.",
#             ...     enabled=True
#             ... )

#             # Adding a new role for a specific microtenant
#             >>> added_role, _, err = zpa.role_controller.add_role(
#             ...     name="Example Group",
#             ...     description="Segment group for microtenant",
#             ...     enabled=True,
#             ...     microtenant_id="216196257331380392"
#             ... )
#         """
#         http_method = "post".upper()
#         api_url = format_url(
#             f"""
#             {self._zpa_base_endpoint}
#             /roles
#         """
#         )

#         body = kwargs

#         microtenant_id = body.get("microtenant_id", None)
#         params = {"microtenantId": microtenant_id} if microtenant_id else {}

#         request, error = self._request_executor.create_request(http_method, api_url, body=body, params=params)
#         if error:
#             return (None, None, error)

#         response, error = self._request_executor.execute(request, RoleController)
#         if error:
#             return (None, response, error)

#         try:
#             result = RoleController(self.form_response_body(response.get_body()))
#         except Exception as error:
#             return (None, response, error)
#         return (result, response, None)

#     def update_role(self, role_id: str, **kwargs) -> tuple:
#         """
#         Updates the specified role.

#         Args:
#             role_id (str): The unique identifier for the role being updated.

#         Returns:
#             :obj:`Tuple`: RoleController: The updated role object.

#         Example:
#             # Basic example: Update an existing role
#             >>> role_id = "216196257331370181"
#             >>> updated_group, _, err = zpa.role_controller.update_role(
#             ...     group_id,
#             ...     name="Updated Group Name",
#             ...     description="Updated description for the segment group",
#             ...     enabled=False
#             ... )

#             # Updating a segment group for a specific microtenant
#             >>> group_id = "216196257331370181"
#             >>> updated_group, _, err = zpa.role_controller.update_role(
#             ...     role_id='5254452',
#             ...     name="Tenant-Specific Group Update",
#             ...     description="Updated segment group for microtenant",
#             ...     enabled=True,
#             ...     microtenant_id="216196257331380392"
#             ... )
#         """
#         http_method = "put".upper()
#         api_url = format_url(
#             f"""
#             {self._zpa_base_endpoint}
#             /roles/{role_id}
#         """
#         )

#         body = {}

#         body.update(kwargs)

#         microtenant_id = body.get("microtenant_id", None)
#         params = {"microtenantId": microtenant_id} if microtenant_id else {}

#         request, error = self._request_executor.create_request(http_method, api_url, body, {}, params)
#         if error:
#             return (None, None, error)

#         response, error = self._request_executor.execute(request, RoleController)
#         if error:
#             return (None, response, error)

#         if response is None:
#             return (RoleController({"id": role_id}), None, None)

#         try:
#             result = RoleController(self.form_response_body(response.get_body()))
#         except Exception as error:
#             return (None, response, error)
#         return (result, response, None)

#     def delete_role(self, role_id: str, microtenant_id: str = None) -> tuple:
#         """
#         Deletes the specified role.

#         Args:
#             role_id (str): The unique identifier for the role to be deleted.

#         Returns:
#             int: Status code of the delete operation.

#         Example:
#             # Delete a role by ID
#             >>> _, _, err = client.zpa.role_controller.delete_role('2445851154')
#             ... if err:
#             ...     print(f"Error deleting role: {err}")
#             ...     return
#             ... print(f"Role with ID {'2445851154'} deleted successfully.")
#         """
#         http_method = "delete".upper()
#         api_url = format_url(
#             f"""
#             {self._zpa_base_endpoint}
#             /roles/{role_id}
#         """
#         )

#         params = {"microtenantId": microtenant_id} if microtenant_id else {}

#         request, error = self._request_executor.create_request(http_method, api_url, params=params)
#         if error:
#             return (None, error)

#         response, error = self._request_executor.execute(request)

#         if error:
#             return (None, response, error)
#         return (None, response, error)
