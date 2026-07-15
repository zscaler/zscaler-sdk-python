# flake8: noqa
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

from typing import Any, Dict, Optional

from pydash.strings import camel_case

from zscaler.oneapi_object import ZscalerObject


def _get(config: dict, snake_key: str, default=None):
    """Get from config with camelCase or snake_case fallback."""
    if not config:
        return default
    v = config.get(snake_key)
    if v is not None:
        return v
    return config.get(camel_case(snake_key), default)


# ---------------------------------------------------------------------------
# GET /api/v3/policy-comments/comment/{policyId} - comment item
# ---------------------------------------------------------------------------


class PolicyComment(ZscalerObject):
    """Policy comment item from list response."""

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)
        if config:
            self.comment = _get(config, "comment")
            self.created_at = _get(config, "created_at")
            self.id = _get(config, "id")
            self.policy_id = _get(config, "policy_id")
            self.type = _get(config, "type")
            self.updated_at = _get(config, "updated_at")
        else:
            self.comment = None
            self.created_at = None
            self.id = None
            self.policy_id = None
            self.type = None
            self.updated_at = None

    def request_format(self) -> Dict[str, Any]:
        return {
            "comment": self.comment,
            "created_at": self.created_at,
            "id": self.id,
            "policy_id": self.policy_id,
            "type": self.type,
            "updated_at": self.updated_at,
        }


# ---------------------------------------------------------------------------
# POST/PUT body - comment only
# ---------------------------------------------------------------------------


class PolicyCommentBody(ZscalerObject):
    """Request body for create/update comment."""

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)
        if config:
            self.comment = _get(config, "comment")
        else:
            self.comment = None

    def request_format(self) -> Dict[str, Any]:
        return {"comment": self.comment}


# ---------------------------------------------------------------------------
# POST/DELETE response - cluster_token, token
# ---------------------------------------------------------------------------


class PolicyCommentResponse(ZscalerObject):
    """Response for POST (create) and DELETE."""

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)
        if config:
            self.cluster_token = _get(config, "cluster_token")
            self.token = _get(config, "token")
        else:
            self.cluster_token = None
            self.token = None
