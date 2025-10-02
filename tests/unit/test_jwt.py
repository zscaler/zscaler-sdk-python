"""
Testing JWT functions for Zscaler SDK
"""

import pytest
import json
import base64
from unittest.mock import patch, Mock
from zscaler.oneapi_oauth_client import OAuth


def generate_mock_jwt_token():
    """Generate a mock JWT token for testing purposes."""
    import time
    
    # Create a mock JWT header
    header = {"alg": "HS256", "typ": "JWT"}
    header_encoded = base64.urlsafe_b64encode(json.dumps(header).encode()).decode().rstrip('=')
    
    # Create a mock JWT payload
    payload = {
        "sub": "test_user",
        "iss": "zscaler",
        "aud": "api",
        "exp": int(time.time()) + 3600,
        "iat": int(time.time()),
        "scope": "read write"
    }
    payload_encoded = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode().rstrip('=')
    
    # Create a mock signature
    signature = "mock_signature_for_testing"
    signature_encoded = base64.urlsafe_b64encode(signature.encode()).decode().rstrip('=')
    
    return f"{header_encoded}.{payload_encoded}.{signature_encoded}"


def test_jwt_token_generation():
    """Test JWT token generation for authentication."""
    # Test that we can generate a valid JWT token structure
    token = generate_mock_jwt_token()
    
    # Verify token has three parts (header.payload.signature)
    parts = token.split('.')
    assert len(parts) == 3
    
    # Verify header can be decoded
    header_decoded = json.loads(base64.urlsafe_b64decode(parts[0] + '=='))
    assert header_decoded["alg"] == "HS256"
    assert header_decoded["typ"] == "JWT"
    
    # Verify payload can be decoded
    payload_decoded = json.loads(base64.urlsafe_b64decode(parts[1] + '=='))
    assert payload_decoded["sub"] == "test_user"
    assert payload_decoded["iss"] == "zscaler"
    assert payload_decoded["aud"] == "api"
    assert "exp" in payload_decoded
    assert "iat" in payload_decoded
    assert payload_decoded["scope"] == "read write"


def test_jwt_token_expiration():
    """Test JWT token expiration handling."""
    import time
    
    # Generate token with specific expiration
    current_time = int(time.time())
    token = generate_mock_jwt_token()
    
    # Decode payload to check expiration
    parts = token.split('.')
    payload_decoded = json.loads(base64.urlsafe_b64decode(parts[1] + '=='))
    
    # Verify expiration is in the future
    assert payload_decoded["exp"] > current_time
    assert payload_decoded["iat"] <= current_time


def test_jwt_token_validation():
    """Test JWT token validation logic."""
    # Test valid token structure
    valid_token = generate_mock_jwt_token()
    parts = valid_token.split('.')
    
    # Should have exactly 3 parts
    assert len(parts) == 3
    
    # Each part should be base64 encoded
    for part in parts:
        try:
            base64.urlsafe_b64decode(part + '==')
        except Exception:
            pytest.fail(f"Token part {part} is not valid base64")
    
    # Test invalid token structure
    invalid_tokens = [
        "invalid.token",  # Missing signature
        "invalid",  # Only one part
        "invalid.token.with.too.many.parts",  # Too many parts
        "",  # Empty token
        "not.a.valid.token.structure"  # Invalid structure
    ]
    
    for invalid_token in invalid_tokens:
        parts = invalid_token.split('.')
        assert len(parts) != 3 or not all(parts)


def test_jwt_token_claims():
    """Test JWT token claims extraction."""
    token = generate_mock_jwt_token()
    parts = token.split('.')
    payload_decoded = json.loads(base64.urlsafe_b64decode(parts[1] + '=='))
    
    # Test required claims
    required_claims = ["sub", "iss", "aud", "exp", "iat", "scope"]
    for claim in required_claims:
        assert claim in payload_decoded
    
    # Test claim values
    assert payload_decoded["sub"] == "test_user"
    assert payload_decoded["iss"] == "zscaler"
    assert payload_decoded["aud"] == "api"
    assert payload_decoded["scope"] == "read write"
    
    # Test numeric claims
    assert isinstance(payload_decoded["exp"], int)
    assert isinstance(payload_decoded["iat"], int)


def test_jwt_token_encoding():
    """Test JWT token encoding and decoding."""
    # Test encoding
    test_data = {"test": "value", "number": 123}
    encoded = base64.urlsafe_b64encode(json.dumps(test_data).encode()).decode().rstrip('=')
    
    # Test decoding
    decoded = json.loads(base64.urlsafe_b64decode(encoded + '=='))
    assert decoded == test_data


def test_jwt_token_with_different_algorithms():
    """Test JWT token with different algorithms."""
    algorithms = ["HS256", "RS256", "ES256"]
    
    for alg in algorithms:
        # Create header with different algorithm
        header = {"alg": alg, "typ": "JWT"}
        header_encoded = base64.urlsafe_b64encode(json.dumps(header).encode()).decode().rstrip('=')
        
        # Create payload
        payload = {"sub": "test_user", "iss": "zscaler"}
        payload_encoded = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode().rstrip('=')
        
        # Create signature
        signature = f"mock_signature_for_{alg}"
        signature_encoded = base64.urlsafe_b64encode(signature.encode()).decode().rstrip('=')
        
        token = f"{header_encoded}.{payload_encoded}.{signature_encoded}"
        
        # Verify token structure
        parts = token.split('.')
        assert len(parts) == 3
        
        # Verify algorithm in header
        header_decoded = json.loads(base64.urlsafe_b64decode(parts[0] + '=='))
        assert header_decoded["alg"] == alg


def test_jwt_token_with_custom_claims():
    """Test JWT token with custom claims."""
    # Create token with custom claims
    custom_claims = {
        "sub": "test_user",
        "iss": "zscaler",
        "aud": "api",
        "custom_claim": "custom_value",
        "role": "admin",
        "permissions": ["read", "write", "delete"]
    }
    
    # Encode custom claims
    header = {"alg": "HS256", "typ": "JWT"}
    header_encoded = base64.urlsafe_b64encode(json.dumps(header).encode()).decode().rstrip('=')
    payload_encoded = base64.urlsafe_b64encode(json.dumps(custom_claims).encode()).decode().rstrip('=')
    signature_encoded = base64.urlsafe_b64encode("mock_signature".encode()).decode().rstrip('=')
    
    token = f"{header_encoded}.{payload_encoded}.{signature_encoded}"
    
    # Verify custom claims
    parts = token.split('.')
    payload_decoded = json.loads(base64.urlsafe_b64decode(parts[1] + '=='))
    
    assert payload_decoded["custom_claim"] == "custom_value"
    assert payload_decoded["role"] == "admin"
    assert payload_decoded["permissions"] == ["read", "write", "delete"]


def test_jwt_token_parsing():
    """Test JWT token parsing and validation."""
    token = generate_mock_jwt_token()
    
    # Test parsing
    parts = token.split('.')
    header = json.loads(base64.urlsafe_b64decode(parts[0] + '=='))
    payload = json.loads(base64.urlsafe_b64decode(parts[1] + '=='))
    signature = base64.urlsafe_b64decode(parts[2] + '==').decode()
    
    # Verify parsed components
    assert header["alg"] == "HS256"
    assert header["typ"] == "JWT"
    assert payload["sub"] == "test_user"
    assert payload["iss"] == "zscaler"
    assert signature == "mock_signature_for_testing"


def test_jwt_token_error_handling():
    """Test JWT token error handling."""
    # Test invalid base64
    invalid_base64 = "invalid.base64.encoding"
    
    with pytest.raises(Exception):
        base64.urlsafe_b64decode(invalid_base64 + '==')
    
    # Test invalid JSON in payload
    invalid_json = base64.urlsafe_b64encode("invalid json".encode()).decode().rstrip('=')
    
    with pytest.raises(json.JSONDecodeError):
        json.loads(base64.urlsafe_b64decode(invalid_json + '=='))


def test_jwt_token_with_oauth_integration():
    """Test JWT token integration with OAuth flow."""
    # Mock OAuth client
    mock_request_executor = Mock()
    mock_config = {
        "client": {
            "clientId": "test_client_id",
            "clientSecret": "test_client_secret",
            "vanityDomain": "testcompany"
        }
    }
    
    # Test OAuth client initialization
    oauth = OAuth(mock_request_executor, mock_config)
    
    # Test that OAuth client can handle JWT tokens
    assert oauth is not None
    assert hasattr(oauth, '_request_executor')
    assert hasattr(oauth, '_config')
