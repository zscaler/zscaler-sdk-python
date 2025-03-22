"""
Module contains different helper functions.
Module is independent from any zscaler modules.
"""

import re

def to_snake_case(string):
    """
    Converts string to snake case.

    Args:
        string (str): input string in any case

    Returns:
        str: string converted to snake case

    Example:
        >>> to_snake_case('lowerCamelCaseString')
        'lower_camel_case_string'
    """
    return re.sub(r"(?<!^)(?=[A-Z])", "_", string).lower()

def to_lower_camel_case(string):
    """
    Converts string to lower camel case with exceptions for specific substrings
    (e.g., TLS remains TLS instead of Tls).

    Args:
        string (str): input string in any case

    Returns:
        str: string converted to lower camel case

    Example:
        >>> to_lower_camel_case('min_tls_version')
        'minTLSVersion'
        >>> to_lower_camel_case('min_client_tls_version')
        'minClientTLSVersion'
    """
    components = string.split("_")
    
    # Define exceptions where components should remain in uppercase
    special_cases = {
                    "tls": "TLS",
                    "dns": "DNS", 
                    "dlp": "DLP",
                }
    
    # Lowercase first letter of the first component
    if components[0]:
        components[0] = components[0][0].lower() + components[0][1:]

    # Join other components, applying special casing where necessary
    return components[0] + "".join(
        special_cases.get(x.lower(), x.title()) for x in components[1:]
    )

def convert_keys_to_snake_case(data):
    """
    Convert all keys in a dictionary or list to snake_case.
    """
    if isinstance(data, dict):
        return {to_snake_case(k): convert_keys_to_snake_case(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [convert_keys_to_snake_case(item) for item in data]
    else:
        return data
    
def convert_keys_to_camel_case(data):
    """
    Recursively convert all keys in a dictionary or list to camelCase.
    Handles nested lists and dictionaries.
    """
    if isinstance(data, dict):
        return {to_lower_camel_case(k): convert_keys_to_camel_case(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [convert_keys_to_camel_case(item) for item in data]
    else:
        return data
