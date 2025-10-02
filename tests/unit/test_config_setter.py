"""
Testing Config Setter for Zscaler SDK
"""

import pytest
import os
from unittest.mock import patch
from zscaler.config.config_setter import ConfigSetter


def test_config_setter_default_values():
    """Test that ConfigSetter applies default values correctly."""
    config_setter = ConfigSetter()
    config_setter._apply_default_values()
    
    # Test default configuration values
    assert config_setter._config["client"]["connectionTimeout"] == 30
    assert config_setter._config["client"]["requestTimeout"] == 0
    assert config_setter._config["client"]["cache"]["enabled"] is False
    assert config_setter._config["client"]["logging"]["enabled"] is False
    assert config_setter._config["client"]["logging"]["logLevel"] == 20  # logging.INFO
    assert config_setter._config["client"]["rateLimit"]["maxRetries"] == 2


def test_config_setter_apply_config():
    """Test that ConfigSetter applies user configuration correctly."""
    config_setter = ConfigSetter()
    
    user_config = {
        "client": {
            "clientId": "test_client_id",
            "clientSecret": "test_client_secret",
            "vanityDomain": "testcompany",
            "cloud": "beta",
            "connectionTimeout": 60,
            "cache": {
                "enabled": True,
                "defaultTtl": 3600,
                "defaultTti": 1800
            }
        }
    }
    
    config_setter._apply_config(user_config)
    
    # Test that user config is applied
    assert config_setter._config["client"]["clientId"] == "test_client_id"
    assert config_setter._config["client"]["clientSecret"] == "test_client_secret"
    assert config_setter._config["client"]["vanityDomain"] == "testcompany"
    assert config_setter._config["client"]["cloud"] == "beta"
    assert config_setter._config["client"]["connectionTimeout"] == 60
    assert config_setter._config["client"]["cache"]["enabled"] is True
    assert config_setter._config["client"]["cache"]["defaultTtl"] == 3600
    assert config_setter._config["client"]["cache"]["defaultTti"] == 1800


def test_config_setter_environment_variables():
    """Test that ConfigSetter reads environment variables correctly."""
    config_setter = ConfigSetter()
    
    with patch.dict('os.environ', {
        'ZSCALER_CLIENT_ID': 'env_client_id',
        'ZSCALER_CLIENT_SECRET': 'env_client_secret',
        'ZSCALER_VANITY_DOMAIN': 'env_company',
        'ZSCALER_CLOUD': 'env_cloud'
    }):
        config_setter._apply_env_config("client")
        
        # Test that environment variables are applied
        assert config_setter._config["client"]["clientId"] == "env_client_id"
        assert config_setter._config["client"]["clientSecret"] == "env_client_secret"
        assert config_setter._config["client"]["vanityDomain"] == "env_company"
        assert config_setter._config["client"]["cloud"] == "env_cloud"


def test_config_setter_merge_config():
    """Test that ConfigSetter merges configurations correctly."""
    config_setter = ConfigSetter()
    
    # Set up base config
    base_config = {
        "client": {
            "clientId": "base_client_id",
            "connectionTimeout": 30,
            "cache": {
                "enabled": False,
                "defaultTtl": 1800
            }
        },
        "testing": {
            "disableHttpsCheck": False
        }
    }
    
    # Set up override config
    override_config = {
        "client": {
            "clientId": "override_client_id",
            "requestTimeout": 60,
            "cache": {
                "enabled": True,
                "defaultTti": 900
            }
        }
    }
    
    config_setter._config = base_config
    config_setter._apply_config(override_config)
    
    # Test that override values take precedence
    assert config_setter._config["client"]["clientId"] == "override_client_id"
    assert config_setter._config["client"]["connectionTimeout"] == 30  # Should remain from base
    assert config_setter._config["client"]["requestTimeout"] == 60  # Should be added from override
    assert config_setter._config["client"]["cache"]["enabled"] is True  # Should be overridden
    assert config_setter._config["client"]["cache"]["defaultTtl"] == 1800  # Should remain from base
    assert config_setter._config["client"]["cache"]["defaultTti"] == 900  # Should be added from override


def test_config_setter_prune_config():
    """Test that ConfigSetter prunes unnecessary configuration fields."""
    config_setter = ConfigSetter()
    
    # Set up config with empty fields that should be pruned
    config_with_empty = {
        "client": {
            "clientId": "test_client_id",
            "clientSecret": "test_client_secret",
            "vanityDomain": "testcompany",
            "emptyField1": "",
            "emptyField2": "",
            "cache": {
                "enabled": True,
                "emptyCacheField": ""
            }
        }
    }
    
    pruned_config = config_setter._prune_config(config_with_empty)
    
    # Test that empty fields are removed
    assert "emptyField1" not in pruned_config["client"]
    assert "emptyField2" not in pruned_config["client"]
    assert "emptyCacheField" not in pruned_config["client"]["cache"]
    
    # Test that valid fields remain
    assert pruned_config["client"]["clientId"] == "test_client_id"
    assert pruned_config["client"]["clientSecret"] == "test_client_secret"
    assert pruned_config["client"]["vanityDomain"] == "testcompany"
    assert pruned_config["client"]["cache"]["enabled"] is True


def test_config_setter_get_config():
    """Test that ConfigSetter returns the current configuration."""
    config_setter = ConfigSetter()
    
    # Set up a test configuration
    test_config = {
        "client": {
            "clientId": "test_client_id",
            "vanityDomain": "testcompany"
        }
    }
    
    config_setter._config = test_config
    returned_config = config_setter.get_config()
    
    # Test that the returned config matches the set config
    assert returned_config == test_config
    assert returned_config["client"]["clientId"] == "test_client_id"
    assert returned_config["client"]["vanityDomain"] == "testcompany"


def test_config_setter_setup_logging():
    """Test that ConfigSetter sets up logging correctly."""
    config_setter = ConfigSetter()
    
    # Test with logging enabled
    config_with_logging = {
        "client": {
            "logging": {
                "enabled": True,
                "verbose": True
            }
        }
    }
    
    config_setter._config = config_with_logging
    
    with patch.dict('os.environ', {}, clear=True):
        config_setter._setup_logging()
        assert os.environ["ZSCALER_SDK_LOG"] == "true"
        assert os.environ["ZSCALER_SDK_VERBOSE"] == "true"
    
    # Test with logging disabled
    config_without_logging = {
        "client": {
            "logging": {
                "enabled": False,
                "verbose": False
            }
        }
    }
    
    config_setter._config = config_without_logging
    
    with patch.dict('os.environ', {}, clear=True):
        config_setter._setup_logging()
        assert os.environ["ZSCALER_SDK_LOG"] == "false"


def test_config_setter_apply_config_with_nested_values():
    """Test that ConfigSetter handles nested configuration values correctly."""
    config_setter = ConfigSetter()
    
    user_config = {
        "client": {
            "clientId": "test_client_id",
            "cache": {
                "enabled": True,
                "defaultTtl": 3600,
                "defaultTti": 1800
            },
            "rateLimit": {
                "maxRetries": 5,
                "maxRetrySeconds": 300
            },
            "proxy": {
                "host": "proxy.example.com",
                "port": 8080,
                "username": "proxy_user",
                "password": "proxy_pass"
            }
        }
    }
    
    config_setter._apply_config(user_config)
    
    # Test nested cache configuration
    assert config_setter._config["client"]["cache"]["enabled"] is True
    assert config_setter._config["client"]["cache"]["defaultTtl"] == 3600
    assert config_setter._config["client"]["cache"]["defaultTti"] == 1800
    
    # Test nested rate limit configuration
    assert config_setter._config["client"]["rateLimit"]["maxRetries"] == 5
    assert config_setter._config["client"]["rateLimit"]["maxRetrySeconds"] == 300
    
    # Test nested proxy configuration
    assert config_setter._config["client"]["proxy"]["host"] == "proxy.example.com"
    assert config_setter._config["client"]["proxy"]["port"] == 8080
    assert config_setter._config["client"]["proxy"]["username"] == "proxy_user"
    assert config_setter._config["client"]["proxy"]["password"] == "proxy_pass"
