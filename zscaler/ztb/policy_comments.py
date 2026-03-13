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

from typing import Optional

from zscaler.api_client import APIClient
from zscaler.request_executor import RequestExecutor
from zscaler.utils import format_url
from zscaler.types import APIResult
from zscaler.ztb.models.policy_comments import PolicyComment


class PolicyCommentsAPI(APIClient):
    """
    Client for the ZTB Policy Comments resource.

    Provides CRUD operations for policy comments in the Zero Trust Branch API.
    Endpoints under ``/api/v3/policy-comments/comment/``.
    """

    _ztb_base_endpoint = "/ztb/api/v3"

    def __init__(self, request_executor: "RequestExecutor") -> None:
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def list_comments(
        self,
        policy_id: str,
        policy_type: str = "application",
        query_params: Optional[dict] = None,
    ) -> APIResult:
        """
        Get all comments for a policy.

        Args:
            policy_id (str): The policy ID.
            policy_type (str): Policy type. Available values:
                application, endpoint, killswitch, network. Default: application.
            query_params (dict, optional): Additional query parameters.

        Returns:
            tuple: (list of PolicyComment instances, Response, error).

        Examples:
            >>> comments, _, err = client.ztb.policy_comments.list_comments(
            ...     "policy-123", policy_type="application"
            ... )
        """
        http_method = "GET"
        api_url = format_url(
            f"""
            {self._ztb_base_endpoint}
            /policy-comments/comment/{policy_id}
        """
        )
        params = dict(query_params) if query_params else {}
        params["policyType"] = policy_type
        request, error = self._request_executor.create_request(http_method, api_url, {}, {}, params=params)
        if error:
            return (None, None, error)
        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)
        try:
            result = []
            for item in response.get_results():
                result.append(PolicyComment(self.form_response_body(item)))
        except Exception as err:
            return (None, response, err)
        return (result, response, None)

    def create_comment(
        self,
        policy_id: str,
        comment: str,
        policy_type: str = "application",
        query_params: Optional[dict] = None,
    ) -> APIResult:
        """
        Create a comment for a policy.

        Args:
            policy_id (str): The policy ID.
            comment (str): Comment text.
            policy_type (str): Policy type. Available values:
                application, endpoint, killswitch, network. Default: application.
            query_params (dict, optional): Additional query parameters.

        Returns:
            tuple: (PolicyCommentResponse or None, Response, error).

        Examples:
            >>> resp_data, _, err = client.ztb.policy_comments.create_comment(
            ...     "policy-123", "My comment", policy_type="application"
            ... )
        """
        http_method = "POST"
        api_url = format_url(
            f"""
            {self._ztb_base_endpoint}
            /policy-comments/comment/{policy_id}
        """
        )
        body = {"comment": comment}
        params = dict(query_params) if query_params else {}
        params["policyType"] = policy_type
        request, error = self._request_executor.create_request(
            http_method, api_url, body, {"Content-Type": "application/json"}, params=params
        )
        if error:
            return (None, None, error)
        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)
        try:
            from zscaler.ztb.models.policy_comments import PolicyCommentResponse

            payload = response.get_body()
            result = PolicyCommentResponse(self.form_response_body(payload)) if payload else None
        except Exception:
            result = None
        return (result, response, None)

    def update_comment(
        self,
        comment_id: str,
        comment: str,
    ) -> APIResult:
        """
        Update a policy comment.

        Args:
            comment_id (str): The comment ID.
            comment (str): Updated comment text.

        Returns:
            tuple: (None, Response, error).

        Examples:
            >>> _, _, err = client.ztb.policy_comments.update_comment(
            ...     "comment-456", "Updated comment text"
            ... )
        """
        http_method = "PUT"
        api_url = format_url(
            f"""
            {self._ztb_base_endpoint}
            /policy-comments/comment/{comment_id}
        """
        )
        body = {"comment": comment}
        request, error = self._request_executor.create_request(
            http_method, api_url, body, {"Content-Type": "application/json"}
        )
        if error:
            return (None, None, error)
        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)
        return (None, response, None)

    def delete_comment(self, comment_id: str) -> APIResult:
        """
        Delete a policy comment.

        Args:
            comment_id (str): The comment ID.

        Returns:
            tuple: (PolicyCommentResponse or None, Response, error).

        Examples:
            >>> resp_data, _, err = client.ztb.policy_comments.delete_comment(
            ...     "comment-456"
            ... )
        """
        http_method = "DELETE"
        api_url = format_url(
            f"""
            {self._ztb_base_endpoint}
            /policy-comments/comment/{comment_id}
        """
        )
        request, error = self._request_executor.create_request(http_method, api_url, {}, {})
        if error:
            return (None, None, error)
        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)
        try:
            from zscaler.ztb.models.policy_comments import PolicyCommentResponse

            payload = response.get_body()
            result = PolicyCommentResponse(self.form_response_body(payload)) if payload else None
        except Exception:
            result = None
        return (result, response, None)
