from typing import Dict, Any, List, Union

from zscaler.helpers import to_lower_camel_case


def _to_camel(key: Any) -> Any:
    """
    Normalize a dict key to camelCase using the project's own ``to_lower_camel_case``
    helper instead of ``pydash.strings.camel_case``.

    ``pydash.camel_case`` tokenizes strings on every digit/letter boundary and
    re-cases the tokens, which silently corrupts already-camelCase keys that
    contain a digit-followed-by-lowercase-letter pattern. For example,
    ``camel_case("isNameL10nTag")`` returns ``"isNameL10NTag"`` (capital ``N``),
    so a downstream model lookup for ``config["isNameL10nTag"]`` fails and
    the field comes back as ``None``.

    ``to_lower_camel_case`` (from ``zscaler.helpers``) returns the string
    unchanged when it contains no underscore, and consults a curated
    ``FIELD_EXCEPTIONS`` map for snake_case keys that don't round-trip
    cleanly (e.g. ``is_name_l10n_tag`` → ``isNameL10nTag``). Non-string
    keys (rare, but possible) are returned untouched.
    """
    if not isinstance(key, str):
        return key
    return to_lower_camel_case(key)


class APIClient:
    """
    Base class for handling responses and converting keys between camelCase and snake_case.
    """

    def __init__(self):
        """
        Automatically set the base URL from the request executor (inherited by each API class).
        """
        pass

    @staticmethod
    def form_response_body(body: Union[Dict[str, Any], List[Any], Any]) -> Union[Dict[str, Any], List[Any], Any]:
        # If body is a dictionary, process its items
        if isinstance(body, dict):
            result = {}
            for key, val in body.items():
                if val is None:
                    continue
                # If val is a dict, process recursively
                if isinstance(val, dict):
                    result[_to_camel(key)] = APIClient.form_response_body(val)
                # If val is a list, process each item inside it
                elif isinstance(val, list):
                    processed_list = []
                    for item in val:
                        if isinstance(item, dict):
                            processed_list.append(APIClient.form_response_body(item))
                        else:
                            # Simple type inside the list, just append as is
                            processed_list.append(item)
                    result[_to_camel(key)] = processed_list
                else:
                    # Simple type (string, int, etc.)
                    result[_to_camel(key)] = val
            return result

        # If body is a list (which can happen if we ever pass a list directly),
        # process each element in the list and return a list
        elif isinstance(body, list):
            processed_list = []
            for item in body:
                if isinstance(item, dict):
                    processed_list.append(APIClient.form_response_body(item))
                else:
                    processed_list.append(item)
            return processed_list

        # If it's neither dict nor list (e.g., a string, int), just return it
        return body

    @staticmethod
    def format_request_body(body: Dict[str, Any]) -> Dict[str, Any]:
        """
        Method to format the request body from snake_case to camelCase.
        Args:
            body (dict): API request body
        """
        result = {}
        for key, val in body.items():
            if val is None:
                continue
            if not isinstance(val, dict):
                result[_to_camel(key)] = val
            else:
                result[_to_camel(key)] = APIClient.format_request_body(val)
        return result
