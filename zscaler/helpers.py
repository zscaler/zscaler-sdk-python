"""
Module contains different helper functions.
Module is independent from any zscaler modules.
"""

import re

# Define acronym exceptions to be handled correctly
ACRONYMS = ['Ip', 'IP', 'DNS', 'TLS', 'PCAP', 'DLP']

def to_snake_case(string):
    if not string:
        return string

    # Replace acronyms with a lowercase underscore version (e.g., surrogateIP → surrogate_ip)
    for acronym in ACRONYMS:
        # Only match the acronym when it appears as a suffix or followed by an uppercase
        string = re.sub(
            rf'(?<=[a-z0-9]){acronym}(?=[A-Z]|$)',
            f'_{acronym.lower()}', 
            string
        )

    # Then run standard camelCase to snake_case transformation
    string = re.sub(r'(?<!^)(?=[A-Z])', '_', string).lower()
    return string.replace('__', '_').strip('_')

def to_lower_camel_case(string):
    """
    Converts snake_case to camelCase with special handling for acronyms like IP, DNS, etc.
    """
    if not string or '_' not in string:
        return string

    # Define special uppercase acronyms
    acronyms = {
        "ip": "IP",
        "dns": "DNS",
        "tls": "TLS",
        "dlp": "DLP",
        "pcap": "PCAP",
    }

    components = string.split('_')
    converted = []

    for i, comp in enumerate(components):
        lower = comp.lower()
        if i == 0:
            # First component is always lowerCamel
            converted.append(lower)
        else:
            if lower in acronyms:
                converted.append(acronyms[lower])
            else:
                converted.append(comp.capitalize())

    return ''.join(converted)

# def to_lower_camel_case(string):
#     """
#     Converts string to lower camel case with exceptions for specific acronyms/terms.
#     Handles both standard snake_case and special cases like TLS, DNS, etc.

#     Args:
#         string (str): input string in snake_case format

#     Returns:
#         str: string converted to lower camel case with preserved acronyms

#     Example:
#         >>> to_lower_camel_case('min_tls_version')
#         'minTLSVersion'
#         >>> to_lower_camel_case('tls_enabled')
#         'tlsEnabled'
#         >>> to_lower_camel_case('capture_pcap')
#         'capturePCAP'
#         >>> to_lower_camel_case('dns_sec_enabled')
#         'dnsSecEnabled'
#     """
#     if not string or '_' not in string:
#         return string

#     # Define special cases that should remain in uppercase
#     uppercase_acronyms = {
#         'tls': 'TLS',
#         'dns': 'DNS',
#         'dlp': 'DLP',
#         'pcap': 'PCAP',
#         'ip': 'IP',
#         'ip': 'Ip',
#     }

#     components = string.split('_')
#     converted = []

#     for i, component in enumerate(components):
#         # Handle first component differently (lowercase first letter)
#         if i == 0:
#             if component.lower() in uppercase_acronyms:
#                 # Special case: if first word is an acronym, keep it lowercase
#                 converted.append(component.lower())
#             else:
#                 converted.append(component[0].lower() + component[1:].lower())
#         else:
#             # Handle subsequent components
#             if component.lower() in uppercase_acronyms:
#                 converted.append(uppercase_acronyms[component.lower()])
#             else:
#                 converted.append(component.capitalize())

#     return ''.join(converted)

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
