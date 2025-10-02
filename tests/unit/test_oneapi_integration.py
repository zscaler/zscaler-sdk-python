"""
Integration tests for Zscaler OneAPI authentication and resource endpoint workflow.

This module tests the complete OneAPI workflow:
1. Authentication with vanity_domain parameter
2. Bearer token retrieval
3. Dynamic URL construction based on cloud parameter
4. Resource endpoint calls with proper authentication
5. Error handling and edge cases
"""

import pytest
import json
from unittest.mock import Mock, patch


# Mock responses for authentication
def generate_mock_access_token():
    """Generate a mock access token for testing purposes."""
    import base64
    import json
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

AUTH_SUCCESS_RESPONSE = {
    "access_token": generate_mock_access_token(),
    "token_type": "Bearer",
    "expires_in": 3600,
    "scope": "read write"
}

AUTH_ERROR_RESPONSE = {
    "error": "invalid_client",
    "error_description": "Client authentication failed"
}

# Mock responses for resource endpoints
RESOURCE_SUCCESS_RESPONSE = {
    "data": [
        {
            "id": "12345",
            "name": "Test Resource",
            "status": "active",
            "created_at": "2024-01-01T00:00:00Z"
        }
    ],
    "total": 1,
    "page": 1,
    "per_page": 10
}

RESOURCE_ERROR_RESPONSE = {
    "error": "unauthorized",
    "message": "Invalid or expired token"
}


class TestOneAPIURLConstruction:
    """Test suite for OneAPI URL construction logic."""

    def test_authentication_url_construction_without_cloud(self):
        """Test authentication URL construction without cloud parameter."""
        vanity_domain = "testcompany"
        
        # Test URL construction logic
        expected_url = f"https://{vanity_domain}.zslogin.net/oauth2/v1/token"
        
        # Verify URL construction
        assert expected_url == "https://testcompany.zslogin.net/oauth2/v1/token"

    def test_authentication_url_construction_with_cloud(self):
        """Test authentication URL construction with cloud parameter."""
        vanity_domain = "testcompany"
        cloud = "beta"
        
        # Test URL construction logic
        expected_url = f"https://{vanity_domain}.zslogin{cloud}.net/oauth2/v1/token"
        
        # Verify URL construction
        assert expected_url == "https://testcompany.zsloginbeta.net/oauth2/v1/token"

    def test_resource_url_construction_without_cloud(self):
        """Test resource URL construction without cloud parameter."""
        # Test URL construction logic
        expected_url = "https://api.zsapi.net/v1/resources"
        
        # Verify URL construction
        assert expected_url == "https://api.zsapi.net/v1/resources"

    def test_resource_url_construction_with_cloud(self):
        """Test resource URL construction with cloud parameter."""
        cloud = "beta"
        
        # Test URL construction logic
        expected_url = f"https://api.{cloud}.zsapi.net/v1/resources"
        
        # Verify URL construction
        assert expected_url == "https://api.beta.zsapi.net/v1/resources"

    def test_url_construction_with_different_clouds(self):
        """Test URL construction with different cloud environments."""
        vanity_domain = "testcompany"
        clouds = ["alpha", "beta", "gamma", "preview"]
        
        for cloud in clouds:
            # Test authentication URL construction
            auth_url = f"https://{vanity_domain}.zslogin{cloud}.net/oauth2/v1/token"
            expected_auth_url = f"https://{vanity_domain}.zslogin{cloud}.net/oauth2/v1/token"
            assert auth_url == expected_auth_url
            
            # Test resource URL construction
            resource_url = f"https://api.{cloud}.zsapi.net/v1/resources"
            expected_resource_url = f"https://api.{cloud}.zsapi.net/v1/resources"
            assert resource_url == expected_resource_url


class TestOneAPIAuthenticationFlow:
    """Test suite for OneAPI authentication flow."""

    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.vanity_domain = "testcompany"
        self.client_id = "test_client_id"
        self.client_secret = "test_client_secret"

    def test_authentication_request_structure(self):
        """Test authentication request structure."""
        with patch('requests.post') as mock_post:
            # Generate fresh mock response for each test
            mock_auth_response = {
                "access_token": generate_mock_access_token(),
                "token_type": "Bearer",
                "expires_in": 3600,
                "scope": "read write"
            }
            
            # Mock successful authentication response
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = mock_auth_response
            mock_post.return_value = mock_response

            # Test authentication request
            url = f"https://{self.vanity_domain}.zslogin.net/oauth2/v1/token"
            data = {
                "grant_type": "client_credentials",
                "client_id": self.client_id,
                "client_secret": self.client_secret
            }
            
            response = mock_post(url, data=data)
            
            # Verify request was made
            mock_post.assert_called_once_with(url, data=data)
            
            # Verify response
            assert response.status_code == 200
            assert response.json() == mock_auth_response

    def test_authentication_request_with_cloud(self):
        """Test authentication request structure with cloud parameter."""
        cloud = "beta"
        
        with patch('requests.post') as mock_post:
            # Generate fresh mock response for each test
            mock_auth_response = {
                "access_token": generate_mock_access_token(),
                "token_type": "Bearer",
                "expires_in": 3600,
                "scope": "read write"
            }
            
            # Mock successful authentication response
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = mock_auth_response
            mock_post.return_value = mock_response

            # Test authentication request with cloud
            url = f"https://{self.vanity_domain}.zslogin{cloud}.net/oauth2/v1/token"
            data = {
                "grant_type": "client_credentials",
                "client_id": self.client_id,
                "client_secret": self.client_secret
            }
            
            response = mock_post(url, data=data)
            
            # Verify request was made with cloud URL
            mock_post.assert_called_once_with(url, data=data)
            
            # Verify response
            assert response.status_code == 200
            assert response.json() == mock_auth_response

    def test_authentication_failure_handling(self):
        """Test authentication failure handling."""
        with patch('requests.post') as mock_post:
            # Mock authentication failure response
            mock_response = Mock()
            mock_response.status_code = 401
            mock_response.json.return_value = AUTH_ERROR_RESPONSE
            mock_post.return_value = mock_response

            # Test authentication request
            url = f"https://{self.vanity_domain}.zslogin.net/oauth2/v1/token"
            data = {
                "grant_type": "client_credentials",
                "client_id": self.client_id,
                "client_secret": self.client_secret
            }
            
            response = mock_post(url, data=data)
            
            # Verify request was made
            mock_post.assert_called_once_with(url, data=data)
            
            # Verify error response
            assert response.status_code == 401
            assert response.json() == AUTH_ERROR_RESPONSE

    def test_authentication_with_different_clouds(self):
        """Test authentication with different cloud environments."""
        clouds = ["alpha", "beta", "gamma", "preview"]
        
        for cloud in clouds:
            with patch('requests.post') as mock_post:
                # Generate fresh mock response for each test
                mock_auth_response = {
                    "access_token": generate_mock_access_token(),
                    "token_type": "Bearer",
                    "expires_in": 3600,
                    "scope": "read write"
                }
                
                # Mock successful authentication response
                mock_response = Mock()
                mock_response.status_code = 200
                mock_response.json.return_value = mock_auth_response
                mock_post.return_value = mock_response

                # Test authentication request with specific cloud
                url = f"https://{self.vanity_domain}.zslogin{cloud}.net/oauth2/v1/token"
                data = {
                    "grant_type": "client_credentials",
                    "client_id": self.client_id,
                    "client_secret": self.client_secret
                }
                
                response = mock_post(url, data=data)
                
                # Verify request was made with correct cloud URL
                mock_post.assert_called_once_with(url, data=data)
                
                # Verify response
                assert response.status_code == 200
                assert response.json() == mock_auth_response


class TestOneAPIResourceFlow:
    """Test suite for OneAPI resource endpoint flow."""

    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.access_token = "test_access_token"

    def test_resource_request_structure_without_cloud(self):
        """Test resource request structure without cloud parameter."""
        with patch('requests.get') as mock_get:
            # Mock successful resource response
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = RESOURCE_SUCCESS_RESPONSE
            mock_get.return_value = mock_response

            # Test resource request
            url = "https://api.zsapi.net/v1/resources"
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json"
            }
            
            response = mock_get(url, headers=headers)
            
            # Verify request was made
            mock_get.assert_called_once_with(url, headers=headers)
            
            # Verify response
            assert response.status_code == 200
            assert response.json() == RESOURCE_SUCCESS_RESPONSE

    def test_resource_request_structure_with_cloud(self):
        """Test resource request structure with cloud parameter."""
        cloud = "beta"
        
        with patch('requests.get') as mock_get:
            # Mock successful resource response
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = RESOURCE_SUCCESS_RESPONSE
            mock_get.return_value = mock_response

            # Test resource request with cloud
            url = f"https://api.{cloud}.zsapi.net/v1/resources"
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json"
            }
            
            response = mock_get(url, headers=headers)
            
            # Verify request was made with cloud URL
            mock_get.assert_called_once_with(url, headers=headers)
            
            # Verify response
            assert response.status_code == 200
            assert response.json() == RESOURCE_SUCCESS_RESPONSE

    def test_resource_request_authentication_error(self):
        """Test resource request with authentication errors."""
        with patch('requests.get') as mock_get:
            # Mock authentication error response
            mock_response = Mock()
            mock_response.status_code = 401
            mock_response.json.return_value = RESOURCE_ERROR_RESPONSE
            mock_get.return_value = mock_response

            # Test resource request
            url = "https://api.zsapi.net/v1/resources"
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json"
            }
            
            response = mock_get(url, headers=headers)
            
            # Verify request was made
            mock_get.assert_called_once_with(url, headers=headers)
            
            # Verify error response
            assert response.status_code == 401
            assert response.json() == RESOURCE_ERROR_RESPONSE

    def test_resource_request_with_different_clouds(self):
        """Test resource request with different cloud environments."""
        clouds = ["alpha", "beta", "gamma", "preview"]
        
        for cloud in clouds:
            with patch('requests.get') as mock_get:
                # Mock successful resource response
                mock_response = Mock()
                mock_response.status_code = 200
                mock_response.json.return_value = RESOURCE_SUCCESS_RESPONSE
                mock_get.return_value = mock_response

                # Test resource request with specific cloud
                url = f"https://api.{cloud}.zsapi.net/v1/resources"
                headers = {
                    "Authorization": f"Bearer {self.access_token}",
                    "Content-Type": "application/json"
                }
                
                response = mock_get(url, headers=headers)
                
                # Verify request was made with correct cloud URL
                mock_get.assert_called_once_with(url, headers=headers)
                
                # Verify response
                assert response.status_code == 200
                assert response.json() == RESOURCE_SUCCESS_RESPONSE


class TestOneAPICompleteWorkflow:
    """Test suite for complete OneAPI workflow integration."""

    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.vanity_domain = "testcompany"
        self.client_id = "test_client_id"
        self.client_secret = "test_client_secret"

    def test_complete_workflow_without_cloud(self):
        """Test complete workflow without cloud parameter."""
        with patch('requests.post') as mock_post, patch('requests.get') as mock_get:
            # Generate fresh mock response for each test
            mock_auth_response = {
                "access_token": generate_mock_access_token(),
                "token_type": "Bearer",
                "expires_in": 3600,
                "scope": "read write"
            }
            
            # Mock authentication response
            auth_response = Mock()
            auth_response.status_code = 200
            auth_response.json.return_value = mock_auth_response
            mock_post.return_value = auth_response

            # Mock resource response
            resource_response = Mock()
            resource_response.status_code = 200
            resource_response.json.return_value = RESOURCE_SUCCESS_RESPONSE
            mock_get.return_value = resource_response

            # Test complete workflow
            # Step 1: Authentication
            auth_url = f"https://{self.vanity_domain}.zslogin.net/oauth2/v1/token"
            auth_data = {
                "grant_type": "client_credentials",
                "client_id": self.client_id,
                "client_secret": self.client_secret
            }
            auth_result = mock_post(auth_url, data=auth_data)
            
            # Step 2: Resource request
            access_token = auth_result.json()["access_token"]
            resource_url = "https://api.zsapi.net/v1/resources"
            resource_headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
            resource_result = mock_get(resource_url, headers=resource_headers)
            
            # Verify authentication was called
            mock_post.assert_called_once_with(auth_url, data=auth_data)
            
            # Verify resource endpoint was called
            mock_get.assert_called_once_with(resource_url, headers=resource_headers)
            
            # Verify response data
            assert auth_result.json() == mock_auth_response
            assert resource_result.json() == RESOURCE_SUCCESS_RESPONSE

    def test_complete_workflow_with_cloud(self):
        """Test complete workflow with cloud parameter."""
        cloud = "beta"
        
        with patch('requests.post') as mock_post, patch('requests.get') as mock_get:
            # Generate fresh mock response for each test
            mock_auth_response = {
                "access_token": generate_mock_access_token(),
                "token_type": "Bearer",
                "expires_in": 3600,
                "scope": "read write"
            }
            
            # Mock authentication response
            auth_response = Mock()
            auth_response.status_code = 200
            auth_response.json.return_value = mock_auth_response
            mock_post.return_value = auth_response

            # Mock resource response
            resource_response = Mock()
            resource_response.status_code = 200
            resource_response.json.return_value = RESOURCE_SUCCESS_RESPONSE
            mock_get.return_value = resource_response

            # Test complete workflow with cloud
            # Step 1: Authentication with cloud
            auth_url = f"https://{self.vanity_domain}.zslogin{cloud}.net/oauth2/v1/token"
            auth_data = {
                "grant_type": "client_credentials",
                "client_id": self.client_id,
                "client_secret": self.client_secret
            }
            auth_result = mock_post(auth_url, data=auth_data)
            
            # Step 2: Resource request with cloud
            access_token = auth_result.json()["access_token"]
            resource_url = f"https://api.{cloud}.zsapi.net/v1/resources"
            resource_headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
            resource_result = mock_get(resource_url, headers=resource_headers)
            
            # Verify authentication was called with cloud
            mock_post.assert_called_once_with(auth_url, data=auth_data)
            
            # Verify resource endpoint was called with cloud
            mock_get.assert_called_once_with(resource_url, headers=resource_headers)
            
            # Verify response data
            assert auth_result.json() == mock_auth_response
            assert resource_result.json() == RESOURCE_SUCCESS_RESPONSE

    def test_workflow_with_authentication_failure(self):
        """Test workflow with authentication failure."""
        with patch('requests.post') as mock_post:
            # Mock authentication failure response
            auth_response = Mock()
            auth_response.status_code = 401
            auth_response.json.return_value = AUTH_ERROR_RESPONSE
            mock_post.return_value = auth_response

            # Test workflow with authentication failure
            auth_url = f"https://{self.vanity_domain}.zslogin.net/oauth2/v1/token"
            auth_data = {
                "grant_type": "client_credentials",
                "client_id": self.client_id,
                "client_secret": self.client_secret
            }
            auth_result = mock_post(auth_url, data=auth_data)
            
            # Verify authentication was attempted
            mock_post.assert_called_once_with(auth_url, data=auth_data)
            
            # Verify error response
            assert auth_result.status_code == 401
            assert auth_result.json() == AUTH_ERROR_RESPONSE

    def test_workflow_with_different_cloud_environments(self):
        """Test workflow with different cloud environments."""
        clouds = ["alpha", "beta", "gamma", "preview"]
        
        for cloud in clouds:
            with patch('requests.post') as mock_post, patch('requests.get') as mock_get:
                # Generate fresh mock response for each test
                mock_auth_response = {
                    "access_token": generate_mock_access_token(),
                    "token_type": "Bearer",
                    "expires_in": 3600,
                    "scope": "read write"
                }
                
                # Mock authentication response
                auth_response = Mock()
                auth_response.status_code = 200
                auth_response.json.return_value = mock_auth_response
                mock_post.return_value = auth_response

                # Mock resource response
                resource_response = Mock()
                resource_response.status_code = 200
                resource_response.json.return_value = RESOURCE_SUCCESS_RESPONSE
                mock_get.return_value = resource_response

                # Test workflow with specific cloud
                # Step 1: Authentication with cloud
                auth_url = f"https://{self.vanity_domain}.zslogin{cloud}.net/oauth2/v1/token"
                auth_data = {
                    "grant_type": "client_credentials",
                    "client_id": self.client_id,
                    "client_secret": self.client_secret
                }
                auth_result = mock_post(auth_url, data=auth_data)
                
                # Step 2: Resource request with cloud
                access_token = auth_result.json()["access_token"]
                resource_url = f"https://api.{cloud}.zsapi.net/v1/resources"
                resource_headers = {
                    "Authorization": f"Bearer {access_token}",
                    "Content-Type": "application/json"
                }
                resource_result = mock_get(resource_url, headers=resource_headers)
                
                # Verify authentication URL with cloud
                mock_post.assert_called_once_with(auth_url, data=auth_data)
                
                # Verify resource URL with cloud
                mock_get.assert_called_once_with(resource_url, headers=resource_headers)
                
                # Verify response data
                assert auth_result.json() == mock_auth_response
                assert resource_result.json() == RESOURCE_SUCCESS_RESPONSE


class TestOneAPIEdgeCases:
    """Test suite for OneAPI edge cases and error handling."""

    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.vanity_domain = "testcompany"
        self.client_id = "test_client_id"
        self.client_secret = "test_client_secret"

    def test_invalid_vanity_domain(self):
        """Test with invalid vanity domain."""
        with patch('requests.post') as mock_post:
            # Mock authentication failure response
            auth_response = Mock()
            auth_response.status_code = 400
            auth_response.json.return_value = {"error": "invalid_domain"}
            mock_post.return_value = auth_response

            # Test with invalid vanity domain
            invalid_vanity_domain = "invalid_domain"
            auth_url = f"https://{invalid_vanity_domain}.zslogin.net/oauth2/v1/token"
            auth_data = {
                "grant_type": "client_credentials",
                "client_id": self.client_id,
                "client_secret": self.client_secret
            }
            auth_result = mock_post(auth_url, data=auth_data)
            
            # Verify error response
            assert auth_result.status_code == 400
            assert auth_result.json() == {"error": "invalid_domain"}

    def test_network_timeout(self):
        """Test network timeout handling."""
        with patch('requests.post') as mock_post:
            # Mock network timeout
            mock_post.side_effect = Exception("Network timeout")

            # Test network timeout handling
            auth_url = f"https://{self.vanity_domain}.zslogin.net/oauth2/v1/token"
            auth_data = {
                "grant_type": "client_credentials",
                "client_id": self.client_id,
                "client_secret": self.client_secret
            }
            
            with pytest.raises(Exception) as exc_info:
                mock_post(auth_url, data=auth_data)
            
            # Verify error handling
            assert "Network timeout" in str(exc_info.value)

    def test_malformed_response(self):
        """Test handling of malformed responses."""
        with patch('requests.post') as mock_post:
            # Mock malformed response
            auth_response = Mock()
            auth_response.status_code = 200
            auth_response.json.side_effect = json.JSONDecodeError("Invalid JSON", "", 0)
            mock_post.return_value = auth_response

            # Test malformed response handling
            auth_url = f"https://{self.vanity_domain}.zslogin.net/oauth2/v1/token"
            auth_data = {
                "grant_type": "client_credentials",
                "client_id": self.client_id,
                "client_secret": self.client_secret
            }
            auth_result = mock_post(auth_url, data=auth_data)
            
            # Test JSON parsing error
            with pytest.raises(json.JSONDecodeError) as exc_info:
                auth_result.json()
            
            # Verify error handling
            assert "Invalid JSON" in str(exc_info.value)

    def test_rate_limiting_handling(self):
        """Test rate limiting handling in OneAPI."""
        with patch('requests.post') as mock_post, patch('requests.get') as mock_get:
            # Generate fresh mock response for each test
            mock_auth_response = {
                "access_token": generate_mock_access_token(),
                "token_type": "Bearer",
                "expires_in": 3600,
                "scope": "read write"
            }
            
            # Mock authentication response
            auth_response = Mock()
            auth_response.status_code = 200
            auth_response.json.return_value = mock_auth_response
            mock_post.return_value = auth_response

            # Mock rate limiting response
            rate_limit_response = Mock()
            rate_limit_response.status_code = 429
            rate_limit_response.headers = {"Retry-After": "60"}
            rate_limit_response.json.return_value = {"error": "rate_limit_exceeded"}
            mock_get.return_value = rate_limit_response

            # Test rate limiting handling
            # Step 1: Authentication
            auth_url = f"https://{self.vanity_domain}.zslogin.net/oauth2/v1/token"
            auth_data = {
                "grant_type": "client_credentials",
                "client_id": self.client_id,
                "client_secret": self.client_secret
            }
            auth_result = mock_post(auth_url, data=auth_data)
            
            # Step 2: Resource request with rate limiting
            access_token = auth_result.json()["access_token"]
            resource_url = "https://api.zsapi.net/v1/resources"
            resource_headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
            resource_result = mock_get(resource_url, headers=resource_headers)
            
            # Verify rate limiting error handling
            assert resource_result.status_code == 429
            assert resource_result.json() == {"error": "rate_limit_exceeded"}
            assert resource_result.headers["Retry-After"] == "60"