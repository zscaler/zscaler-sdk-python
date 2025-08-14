#!/usr/bin/env python3
"""
OAuth Client Test Runner

This script runs the enhanced OAuth client tests and provides a summary of the results.
"""

import sys
import subprocess
import os

def run_oauth_tests():
    """Run the OAuth client tests and return results"""
    print("Enhanced OAuth Client Test Suite")
    print("=" * 50)
    
    # Change to the tests directory
    test_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(test_dir)
    
    try:
        # Run the tests
        result = subprocess.run([
            sys.executable, "-m", "pytest", 
            "test_enhanced_oauth_client.py", 
            "-v", "--tb=short"
        ], capture_output=True, text=True)
        
        print("Test Results:")
        print("-" * 20)
        
        if result.returncode == 0:
            print("✅ All OAuth client tests passed!")
            print(f"\nTest Output:\n{result.stdout}")
        else:
            print("❌ Some OAuth client tests failed!")
            print(f"\nTest Output:\n{result.stdout}")
            print(f"\nError Output:\n{result.stderr}")
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"❌ Error running tests: {e}")
        return False

def main():
    """Main function"""
    success = run_oauth_tests()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 OAuth client test suite completed successfully!")
        print("\nTest Coverage:")
        print("- OAuth initialization (with/without cache)")
        print("- Cache key generation")
        print("- Token expiration logic")
        print("- Cache functionality")
        print("- Token information retrieval")
        print("- Token clearing")
        print("- Legacy client handling")
        print("- Singleton pattern")
        print("- Error handling")
        print("- Configuration validation")
    else:
        print("💥 OAuth client test suite failed!")
        sys.exit(1)

if __name__ == "__main__":
    main() 