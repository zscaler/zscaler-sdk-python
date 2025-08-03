#!/usr/bin/env python3
"""
Test script to verify the authentication payload format for ZDX Legacy Client
"""

import os
import time
import hashlib
import requests
from zscaler.user_agent import UserAgent

def test_auth_payload():
    """Test the authentication payload format"""
    print("=== Testing ZDX Legacy Authentication Payload ===")
    
    # Get credentials from environment
    client_id = os.getenv("ZDX_CLIENT_ID")
    client_secret = os.getenv("ZDX_CLIENT_SECRET")
    cloud = os.getenv("ZDX_CLOUD", "zdxcloud")
    
    if not client_id or not client_secret:
        print("❌ Missing environment variables!")
        return False
    
    # Create the payload exactly as the legacy client does
    epoch_time = int(time.time())
    api_secret_format = f"{client_secret}:{epoch_time}"
    api_secret_hash = hashlib.sha256(api_secret_format.encode("utf-8")).hexdigest()
    
    payload = {
        "key_id": client_id,
        "key_secret": api_secret_hash,
        "timestamp": epoch_time,
    }
    
    print(f"Client ID: {client_id}")
    print(f"Epoch Time: {epoch_time}")
    print(f"API Secret Format: {api_secret_format}")
    print(f"API Secret Hash: {api_secret_hash}")
    print(f"Payload: {payload}")
    
    # Test the request
    url = f"https://api.{cloud}.net/v1/oauth/token"
    user_agent = UserAgent().get_user_agent_string()
    
    headers = {
        "Content-Type": "application/json",
        "User-Agent": user_agent,
    }
    
    print(f"\nMaking request to: {url}")
    print(f"Headers: {headers}")
    
    try:
        response = requests.post(
            url,
            json=payload,
            headers=headers,
            timeout=30
        )
        
        print(f"\nResponse Status: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            print("✅ Authentication successful!")
            response_data = response.json()
            print(f"Response data keys: {list(response_data.keys())}")
            return True
        else:
            print(f"❌ Authentication failed with status {response.status_code}")
            print(f"Response body: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Request failed: {e}")
        return False

def main():
    """Main function"""
    print("ZDX Legacy Client Authentication Payload Test")
    print("=" * 60)
    
    success = test_auth_payload()
    
    if success:
        print("\n✅ Authentication payload test passed!")
    else:
        print("\n❌ Authentication payload test failed!")
        print("\nPossible issues:")
        print("1. Incorrect client_id or client_secret")
        print("2. Wrong cloud configuration")
        print("3. API endpoint not accessible")
        print("4. Network connectivity issues")

if __name__ == "__main__":
    main() 