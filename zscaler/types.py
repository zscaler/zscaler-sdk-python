"""
Type definitions for Zscaler SDK autocomplete and type checking.

This module provides reusable type aliases to simplify type hints across the SDK.
All API methods follow the pattern: (result, response, error)

Usage:
    from zscaler.types import APIResult
    from zscaler.zia.models.urlcategory import URLCategory
    from typing import List
    
    # For methods that return a list:
    def list_categories(...) -> APIResult[List[URLCategory]]:
        ...
    
    # For methods that return a single item:
    def get_category(...) -> APIResult[URLCategory]:
        ...
    
    # For methods that return None (like delete):
    def delete_category(...) -> APIResult[None]:
        ...
"""

from typing import TypeVar, Tuple, Optional
from zscaler.oneapi_response import ZscalerAPIResponse

# Type variable for API result types
T = TypeVar('T')

# Standard API method return type: (result, response, error)
# This is a generic type alias that works with any result type.
#
# The type system understands:
#   APIResult[List[URLCategory]] → Tuple[List[URLCategory], ZscalerAPIResponse, Optional[Exception]]
#   APIResult[URLCategory]        → Tuple[URLCategory, ZscalerAPIResponse, Optional[Exception]]
#   APIResult[None]               → Tuple[None, ZscalerAPIResponse, Optional[Exception]]
APIResult = Tuple[T, ZscalerAPIResponse, Optional[Exception]]

