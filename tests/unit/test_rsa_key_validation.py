"""
Testing RSA Key Validation for CWE-326 Mitigation
Tests to ensure weak RSA keys are rejected
"""

import pytest
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from zscaler.oneapi_oauth_client import validate_rsa_key_strength, MIN_RSA_KEY_SIZE


def test_validate_strong_rsa_key_2048():
    """Test that 2048-bit RSA keys pass validation (minimum requirement)."""
    # Generate a 2048-bit RSA key
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    
    # Should not raise an exception
    key_size = validate_rsa_key_strength(private_key)
    assert key_size == 2048


def test_validate_strong_rsa_key_4096():
    """Test that 4096-bit RSA keys pass validation."""
    # Generate a 4096-bit RSA key
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=4096,
        backend=default_backend()
    )
    
    # Should not raise an exception
    key_size = validate_rsa_key_strength(private_key)
    assert key_size == 4096


def test_reject_weak_rsa_key_1024():
    """Test that 1024-bit RSA keys are rejected (insufficient strength)."""
    # Generate a weak 1024-bit RSA key
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=1024,
        backend=default_backend()
    )
    
    # Should raise ValueError for weak key
    with pytest.raises(ValueError) as exc_info:
        validate_rsa_key_strength(private_key)
    
    # Verify error message contains key information
    error_message = str(exc_info.value)
    assert "1024 bits" in error_message
    assert str(MIN_RSA_KEY_SIZE) in error_message
    assert "Insufficient RSA key strength" in error_message


def test_reject_weak_rsa_key_512():
    """Test that the cryptography library itself prevents very weak keys (<1024 bits)."""
    # The cryptography library won't even allow generating keys < 1024 bits
    # This is an additional security layer beyond our validation
    with pytest.raises(ValueError) as exc_info:
        rsa.generate_private_key(
            public_exponent=65537,
            key_size=512,
            backend=default_backend()
        )
    
    # Verify the cryptography library rejects it
    error_message = str(exc_info.value)
    assert "1024" in error_message or "512" in error_message


def test_validate_key_boundary_exactly_2048():
    """Test the exact boundary case of 2048 bits."""
    # Generate exactly 2048-bit key (minimum acceptable)
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    
    # Should pass validation
    key_size = validate_rsa_key_strength(private_key)
    assert key_size == 2048


def test_validate_non_rsa_key():
    """Test that non-RSA key types are handled gracefully."""
    # Use a non-RSA key object (like a string)
    non_rsa_key = "not_an_rsa_key"
    
    # Should return None for unsupported key types without raising exception
    result = validate_rsa_key_strength(non_rsa_key)
    assert result is None


def test_min_rsa_key_size_constant():
    """Test that MIN_RSA_KEY_SIZE constant is set to NIST recommendation."""
    assert MIN_RSA_KEY_SIZE == 2048, "MIN_RSA_KEY_SIZE should be 2048 per NIST guidelines"


def test_error_message_contains_mitigation_guidance():
    """Test that error messages provide actionable guidance to users."""
    # Generate a weak key
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=1024,
        backend=default_backend()
    )
    
    # Capture the error message
    with pytest.raises(ValueError) as exc_info:
        validate_rsa_key_strength(private_key)
    
    error_message = str(exc_info.value).lower()
    
    # Verify the error message provides guidance
    assert "stronger rsa key" in error_message
    assert "secure authentication" in error_message
    assert "nist" in error_message

