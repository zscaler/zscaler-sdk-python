from pydash.strings import camel_case


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
    def form_response_body(body):
        # If body is a dictionary, process its items
        if isinstance(body, dict):
            result = {}
            for key, val in body.items():
                if val is None:
                    continue
                # If val is a dict, process recursively
                if isinstance(val, dict):
                    result[camel_case(key)] = APIClient.form_response_body(val)
                # If val is a list, process each item inside it
                elif isinstance(val, list):
                    processed_list = []
                    for item in val:
                        if isinstance(item, dict):
                            processed_list.append(APIClient.form_response_body(item))
                        else:
                            # Simple type inside the list, just append as is
                            processed_list.append(item)
                    result[camel_case(key)] = processed_list
                else:
                    # Simple type (string, int, etc.)
                    result[camel_case(key)] = val
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
    def format_request_body(body: dict):
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
                result[camel_case(key)] = val
            else:
                result[camel_case(key)] = APIClient.format_request_body(val)
        return result
