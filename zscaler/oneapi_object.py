from zscaler.helpers import to_snake_case
from zscaler.helpers import convert_keys_to_snake_case


class ZscalerObject:
    """
    Base object for all Zscaler datatypes.
    """

    def __init__(self, config=None):
        pass

    def __repr__(self):
        return str(vars(self))

    def __getitem__(self, key):
        if hasattr(self, key):
            return getattr(self, key)
        raise KeyError(f"{key} not found in {self.__class__.__name__}")

    def __contains__(self, key):
        return hasattr(self, key)

    def as_dict(self):
        result = {}
        for key, val in self.request_format().items():
            if val is None:
                continue

            # If it's a list, convert each item
            if isinstance(val, list):
                formatted_list = []
                for item in val:
                    if isinstance(item, ZscalerObject):
                        formatted_list.append(item.as_dict())
                    else:
                        # If item is itself a dict, also recursively convert it
                        if isinstance(item, dict):
                            formatted_list.append(convert_keys_to_snake_case(item))
                        else:
                            formatted_list.append(item)
                result[to_snake_case(key)] = formatted_list

            # If it's a ZscalerObject, just recurse the same way
            elif isinstance(val, ZscalerObject):
                result[to_snake_case(key)] = val.as_dict()

            # If it's a dict, recursively snake_case its contents
            elif isinstance(val, dict):
                result[to_snake_case(key)] = convert_keys_to_snake_case(val)

            # Otherwise it's a simple type (string, int, etc.)
            else:
                result[to_snake_case(key)] = val

        return result

    def request_format(self):
        """
        Return the object in a format suitable for API requests.
        The keys are in camelCase as expected by the API.
        """
        return {}
