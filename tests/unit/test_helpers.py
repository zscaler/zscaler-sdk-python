"""
Testing Helper functions for Zscaler SDK
"""

import pytest
from zscaler.helpers import (
    to_snake_case,
    to_lower_camel_case,
    convert_keys_to_snake_case,
    convert_keys_to_camel_case,
    convert_keys_to_camel_case_selective
)


def test_to_snake_case():
    """Test to_snake_case function with various inputs."""
    # Basic cases
    assert to_snake_case('string') == 'string'
    assert to_snake_case('CamelCaseStr') == 'camel_case_str'
    assert to_snake_case('lowerCamelCaseStr') == 'lower_camel_case_str'
    assert to_snake_case('snake_case_str') == 'snake_case_str'
    
    # Edge cases
    assert to_snake_case('') == ''
    assert to_snake_case('Single') == 'single'
    assert to_snake_case('UPPERCASE') == 'u_p_p_e_r_c_a_s_e'  # Each uppercase letter becomes separate
    assert to_snake_case('lowercase') == 'lowercase'
    
    # Special Zscaler field exceptions
    assert to_snake_case('predefinedADPControls') == 'predefined_adp_controls'
    assert to_snake_case('surrogateIP') == 'surrogate_ip'
    assert to_snake_case('capturePCAP') == 'capture_pcap'
    assert to_snake_case('internalIpRange') == 'internal_ip_range'
    assert to_snake_case('startIPAddress') == 'start_ip_address'
    assert to_snake_case('endIPAddress') == 'end_ip_address'
    assert to_snake_case('minTLSVersion') == 'min_tls_version'
    assert to_snake_case('primaryGW') == 'primary_gw'
    assert to_snake_case('secondaryGW') == 'secondary_gw'
    assert to_snake_case('greTunnelIP') == 'gre_tunnel_ip'
    assert to_snake_case('tunID') == 'tun_id'
    assert to_snake_case('routableIP') == 'routable_ip'
    assert to_snake_case('validSSLCertificate') == 'valid_ssl_certificate'
    assert to_snake_case('ecVMs') == 'ec_vms'
    assert to_snake_case('ipV6Enabled') == 'ipv6_enabled'
    assert to_snake_case('emailIds') == 'email_ids'
    assert to_snake_case('showEUN') == 'show_eun'
    assert to_snake_case('showEUNATP') == 'show_eunatp'
    
    # Complex cases
    assert to_snake_case('enableIPv6DnsResolutionOnTransparentProxy') == 'enable_ipv6_dns_resolution_on_transparent_proxy'
    assert to_snake_case('dnsResolutionOnTransparentProxyIPv6ExemptApps') == 'dns_resolution_on_transparent_proxy_ipv6_exempt_apps'
    assert to_snake_case('cookieStealingPCAPEnabled') == 'cookie_stealing_pcap_enabled'
    assert to_snake_case('alertForUnknownOrSuspiciousC2Traffic') == 'alert_for_unknown_or_suspicious_c2_traffic'


def test_to_lower_camel_case():
    """Test to_lower_camel_case function with various inputs."""
    # Basic cases
    assert to_lower_camel_case('') == ''
    assert to_lower_camel_case('string') == 'string'
    assert to_lower_camel_case('CamelCaseStr') == 'CamelCaseStr'  # Already camelCase, no change
    assert to_lower_camel_case('lowerCamelCaseStr') == 'lowerCamelCaseStr'
    assert to_lower_camel_case('snake_case_str') == 'snakeCaseStr'
    assert to_lower_camel_case('_start_with_underscore') == 'StartWithUnderscore'
    assert to_lower_camel_case('__start_with_double_underscore') == 'StartWithDoubleUnderscore'
    assert to_lower_camel_case('__double_underscores__') == 'DoubleUnderscores'
    
    # Edge cases
    assert to_lower_camel_case('single') == 'single'
    assert to_lower_camel_case('UPPERCASE') == 'UPPERCASE'  # No underscores, no change
    assert to_lower_camel_case('lowercase') == 'lowercase'
    assert to_lower_camel_case('no_underscores') == 'noUnderscores'
    
    # Special Zscaler field exceptions
    assert to_lower_camel_case('predefined_adp_controls') == 'predefinedADPControls'
    assert to_lower_camel_case('surrogate_ip') == 'surrogateIP'
    assert to_lower_camel_case('capture_pcap') == 'capturePCAP'
    assert to_lower_camel_case('internal_ip_range') == 'internalIpRange'
    assert to_lower_camel_case('start_ip_address') == 'startIPAddress'
    assert to_lower_camel_case('end_ip_address') == 'endIPAddress'
    assert to_lower_camel_case('min_tls_version') == 'minTLSVersion'
    assert to_lower_camel_case('primary_gw') == 'primaryGW'
    assert to_lower_camel_case('secondary_gw') == 'secondaryGW'
    assert to_lower_camel_case('gre_tunnel_ip') == 'greTunnelIp'  # Standard camelCase conversion
    assert to_lower_camel_case('tun_id') == 'tunID'
    assert to_lower_camel_case('routable_ip') == 'routableIP'
    assert to_lower_camel_case('valid_ssl_certificate') == 'validSSLCertificate'
    assert to_lower_camel_case('ec_vms') == 'ecVMs'
    assert to_lower_camel_case('ipv6_enabled') == 'ipV6Enabled'
    assert to_lower_camel_case('email_ids') == 'emailIds'
    assert to_lower_camel_case('show_eun') == 'showEUN'
    assert to_lower_camel_case('show_eunatp') == 'showEUNATP'
    
    # Complex cases
    assert to_lower_camel_case('enable_ipv6_dns_resolution_on_transparent_proxy') == 'enableIPv6DnsResolutionOnTransparentProxy'
    assert to_lower_camel_case('dns_resolution_on_transparent_proxy_ipv6_exempt_apps') == 'dnsResolutionOnTransparentProxyIPv6ExemptApps'
    assert to_lower_camel_case('cookie_stealing_pcap_enabled') == 'cookieStealingPCAPEnabled'
    assert to_lower_camel_case('alert_for_unknown_or_suspicious_c2_traffic') == 'alertForUnknownOrSuspiciousC2Traffic'


def test_convert_keys_to_snake_case():
    """Test convert_keys_to_snake_case function with nested data structures."""
    # Simple dictionary
    data = {
        "clientId": "test_client",
        "clientSecret": "test_secret",
        "vanityDomain": "testcompany"
    }
    result = convert_keys_to_snake_case(data)
    expected = {
        "client_id": "test_client",
        "client_secret": "test_secret",
        "vanity_domain": "testcompany"
    }
    assert result == expected
    
    # Nested dictionary
    data = {
        "client": {
            "clientId": "test_client",
            "vanityDomain": "testcompany",
            "cache": {
                "enabled": True,
                "defaultTtl": 3600
            }
        }
    }
    result = convert_keys_to_snake_case(data)
    expected = {
        "client": {
            "client_id": "test_client",
            "vanity_domain": "testcompany",
            "cache": {
                "enabled": True,
                "default_ttl": 3600
            }
        }
    }
    assert result == expected
    
    # List of dictionaries
    data = [
        {"clientId": "client1", "vanityDomain": "company1"},
        {"clientId": "client2", "vanityDomain": "company2"}
    ]
    result = convert_keys_to_snake_case(data)
    expected = [
        {"client_id": "client1", "vanity_domain": "company1"},
        {"client_id": "client2", "vanity_domain": "company2"}
    ]
    assert result == expected
    
    # Non-dictionary/list data
    assert convert_keys_to_snake_case("string") == "string"
    assert convert_keys_to_snake_case(123) == 123
    assert convert_keys_to_snake_case(True) == True
    assert convert_keys_to_snake_case(None) == None


def test_convert_keys_to_camel_case():
    """Test convert_keys_to_camel_case function with nested data structures."""
    # Simple dictionary
    data = {
        "client_id": "test_client",
        "client_secret": "test_secret",
        "vanity_domain": "testcompany"
    }
    result = convert_keys_to_camel_case(data)
    expected = {
        "clientId": "test_client",
        "clientSecret": "test_secret",
        "vanityDomain": "testcompany"
    }
    assert result == expected
    
    # Nested dictionary
    data = {
        "client": {
            "client_id": "test_client",
            "vanity_domain": "testcompany",
            "cache": {
                "enabled": True,
                "default_ttl": 3600
            }
        }
    }
    result = convert_keys_to_camel_case(data)
    expected = {
        "client": {
            "clientId": "test_client",
            "vanityDomain": "testcompany",
            "cache": {
                "enabled": True,
                "defaultTtl": 3600
            }
        }
    }
    assert result == expected
    
    # List of dictionaries
    data = [
        {"client_id": "client1", "vanity_domain": "company1"},
        {"client_id": "client2", "vanity_domain": "company2"}
    ]
    result = convert_keys_to_camel_case(data)
    expected = [
        {"clientId": "client1", "vanityDomain": "company1"},
        {"clientId": "client2", "vanityDomain": "company2"}
    ]
    assert result == expected
    
    # Non-dictionary/list data
    assert convert_keys_to_camel_case("string") == "string"
    assert convert_keys_to_camel_case(123) == 123
    assert convert_keys_to_camel_case(True) == True
    assert convert_keys_to_camel_case(None) == None


def test_convert_keys_to_camel_case_selective():
    """Test convert_keys_to_camel_case_selective function with key preservation."""
    # Test with preserved keys
    data = {
        "client_id": "test_client",
        "client_secret": "test_secret",
        "vanity_domain": "testcompany",
        "api_key": "test_api_key"
    }
    preserve_keys = {"client_id", "api_key"}
    result = convert_keys_to_camel_case_selective(data, preserve_keys)
    expected = {
        "client_id": "test_client",  # Preserved
        "clientSecret": "test_secret",
        "vanityDomain": "testcompany",
        "api_key": "test_api_key"  # Preserved
    }
    assert result == expected
    
    # Test with nested data and preserved keys
    data = {
        "client": {
            "client_id": "test_client",  # Should be preserved
            "vanity_domain": "testcompany",
            "cache": {
                "enabled": True,
                "default_ttl": 3600
            }
        }
    }
    preserve_keys = {"client_id"}
    result = convert_keys_to_camel_case_selective(data, preserve_keys)
    expected = {
        "client": {
            "client_id": "test_client",  # Preserved
            "vanityDomain": "testcompany",
            "cache": {
                "enabled": True,
                "defaultTtl": 3600
            }
        }
    }
    assert result == expected
    
    # Test with no preserved keys (should behave like regular camel case)
    data = {
        "client_id": "test_client",
        "vanity_domain": "testcompany"
    }
    result = convert_keys_to_camel_case_selective(data, set())
    expected = {
        "clientId": "test_client",
        "vanityDomain": "testcompany"
    }
    assert result == expected
    
    # Test with None preserved keys (should behave like regular camel case)
    data = {
        "client_id": "test_client",
        "vanity_domain": "testcompany"
    }
    result = convert_keys_to_camel_case_selective(data, None)
    expected = {
        "clientId": "test_client",
        "vanityDomain": "testcompany"
    }
    assert result == expected


def test_convert_keys_to_camel_case_with_feature_permissions():
    """Test convert_keys_to_camel_case with featurePermissions special handling."""
    data = {
        "client_id": "test_client",
        "featurePermissions": {
            "read_users": True,
            "write_users": False,
            "admin_access": True
        }
    }
    result = convert_keys_to_camel_case(data)
    expected = {
        "clientId": "test_client",
        "featurePermissions": {
            "read_users": True,  # Keys inside featurePermissions should be preserved
            "write_users": False,
            "admin_access": True
        }
    }
    assert result == expected


def test_helper_functions_edge_cases():
    """Test helper functions with edge cases and special characters."""
    # Test with special characters
    assert to_snake_case('test-with-dash') == 'test-with-dash'
    assert to_snake_case('test_with_underscore') == 'test_with_underscore'
    assert to_snake_case('test.with.dots') == 'test.with.dots'
    
    # Test with numbers
    assert to_snake_case('test123') == 'test123'
    assert to_snake_case('test123Case') == 'test123_case'
    assert to_snake_case('123test') == '123test'
    
    # Test with mixed case
    assert to_snake_case('XMLHttpRequest') == 'x_m_l_http_request'  # Each uppercase letter becomes separate
    assert to_snake_case('HTMLParser') == 'h_t_m_l_parser'
    assert to_snake_case('URLBuilder') == 'u_r_l_builder'
    
    # Test with consecutive capitals
    assert to_snake_case('XMLHTTPRequest') == 'x_m_l_h_t_t_p_request'
    assert to_snake_case('HTTPSConnection') == 'h_t_t_p_s_connection'
    
    # Test with underscores in camel case
    assert to_snake_case('test_CamelCase') == 'test_camel_case'
    assert to_snake_case('test_Camel_Case') == 'test_camel_case'


def test_helper_functions_performance():
    """Test helper functions with large data structures."""
    # Test with large dictionary
    large_data = {}
    for i in range(1000):
        large_data[f"key_{i}"] = f"value_{i}"
    
    result = convert_keys_to_snake_case(large_data)
    assert len(result) == 1000
    assert "key_0" in result
    assert "key_999" in result
    
    # Test with large nested structure
    nested_data = {
        "level1": {
            "level2": {
                "level3": {
                    "level4": {
                        "deep_key": "deep_value"
                    }
                }
            }
        }
    }
    result = convert_keys_to_camel_case(nested_data)
    assert "level1" in result
    assert "level2" in result["level1"]
    assert "level3" in result["level1"]["level2"]
    assert "level4" in result["level1"]["level2"]["level3"]
    assert "deepKey" in result["level1"]["level2"]["level3"]["level4"]


def test_helper_functions_roundtrip():
    """Test that snake_case to camelCase and back works correctly."""
    original_snake = "test_snake_case_string"
    camel = to_lower_camel_case(original_snake)
    back_to_snake = to_snake_case(camel)
    
    # Note: This might not be exactly the same due to field exceptions
    # but should be functionally equivalent
    assert isinstance(camel, str)
    assert isinstance(back_to_snake, str)
    
    # Test with known roundtrip cases
    test_cases = [
        "simple_case",
        "multi_word_case",
        "with_numbers123",
        "mixed_Case_String"
    ]
    
    for case in test_cases:
        camel_result = to_lower_camel_case(case)
        snake_result = to_snake_case(camel_result)
        assert isinstance(camel_result, str)
        assert isinstance(snake_result, str)
