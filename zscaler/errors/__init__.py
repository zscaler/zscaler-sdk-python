"""
Zscaler SDK Error Classes

This module provides error handling for all Zscaler API responses.
"""

from zscaler.errors.error import Error
from zscaler.errors.graphql_error import (
    GraphQLAPIError,
    GraphQLErrorDetail,
    GraphQLErrorLocation,
    is_graphql_error_response,
)
from zscaler.errors.http_error import HTTPError
from zscaler.errors.zscaler_api_error import ZscalerAPIError

__all__ = [
    "Error",
    "HTTPError",
    "ZscalerAPIError",
    "GraphQLAPIError",
    "GraphQLErrorDetail",
    "GraphQLErrorLocation",
    "is_graphql_error_response",
]
