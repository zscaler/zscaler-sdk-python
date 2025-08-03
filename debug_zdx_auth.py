#!/usr/bin/env python3
"""
Debug script for ZDX Legacy Client Authentication
"""

import os
import sys
import logging
from zscaler.zdx.legacy import LegacyZDXClientHelper

# Set up logging to see what's happening
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def debug_environment_variables():
    """Check if environment variables are set correctly"""
    print("=== Environment Variables Check ===")
    
    client_id = os.getenv("ZDX_CLIENT_ID")
    client_secret = os.getenv("ZDX_CLIENT_SECRET")
    cloud = os.getenv("ZDX_CLOUD", "zdxcloud")
    
    print(f"ZDX_CLIENT_ID: {'SET' if client_id else 'NOT SET'}")
    print(f"ZDX_CLIENT_SECRET: {'SET' if client_secret else 'NOT SET'}")
    print(f"ZDX_CLOUD: {cloud}")
    
    if client_id:
        print(f"Client ID length: {len(client_id)}")
        print(f"Client ID starts with: {client_id[:8]}...")
    
    if client_secret:
        print(f"Client Secret length: {len(client_secret)}")
        print(f"Client Secret starts with: {client_secret[:8]}...")
    
    return client_id, client_secret, cloud

def test_legacy_client():
    """Test the legacy client initialization"""
    print("\n=== Testing Legacy Client ===")
    
    try:
        # Initialize the legacy client helper directly
        client = LegacyZDXClientHelper()
        print("✅ Legacy client helper initialized successfully")
        
        # Try to build session
        print("Attempting to build session...")
        session = client._build_session()
        print("✅ Session built successfully")
        
        # Try to validate token
        print("Attempting to validate token...")
        validation_result = client.validate_token()
        print(f"✅ Token validation result: {validation_result}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print(f"Error type: {type(e).__name__}")
        return False

def test_token_creation():
    """Test token creation specifically"""
    print("\n=== Testing Token Creation ===")
    
    try:
        client = LegacyZDXClientHelper()
        
        # Test the create_token method directly
        token_data = client.create_token()
        print(f"✅ Token created successfully")
        print(f"Token data keys: {list(token_data.keys())}")
        
        if 'token' in token_data:
            token = token_data['token']
            print(f"Token length: {len(token)}")
            print(f"Token starts with: {token[:20]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Token creation failed: {e}")
        return False

def main():
    """Main debug function"""
    print("ZDX Legacy Client Authentication Debug")
    print("=" * 50)
    
    # Check environment variables
    client_id, client_secret, cloud = debug_environment_variables()
    
    if not client_id or not client_secret:
        print("\n❌ ERROR: Missing required environment variables!")
        print("Please set ZDX_CLIENT_ID and ZDX_CLIENT_SECRET")
        sys.exit(1)
    
    # Test legacy client
    success = test_legacy_client()
    
    if not success:
        print("\n❌ Legacy client test failed!")
        print("This suggests an authentication issue with the API")
        sys.exit(1)
    
    # Test token creation specifically
    token_success = test_token_creation()
    
    if not token_success:
        print("\n❌ Token creation failed!")
        print("This indicates the API is rejecting the authentication request")
        sys.exit(1)
    
    print("\n✅ All tests passed! Your ZDX legacy client should work correctly.")

if __name__ == "__main__":
    main() 