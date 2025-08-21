"""
Unit tests for pre_deployment.py module
"""

import os
import sys
import pytest
import logging
from unittest.mock import patch, MagicMock

# Add the pre_deployment module to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'pre_deployment'))

from pre_deployment import load_env_vars, pre_deployment

# Fixtures for common test data
@pytest.fixture
def valid_env_vars():
    """Fixture providing valid environment variables"""
    return {
        'DB_PASSWORD': 'test_password',
        'DB_HOST': 'test_host',
        'DB_PORT': '1433',
        'DB_NAME': 'test_db',
        'DB_USER': 'test_user'
    }


@pytest.fixture
def minimal_env_vars():
    """Fixture providing minimal valid environment variables"""
    return {
        'DB_PASSWORD': 'test_password'
    }

class TestLoadEnvVars:
    """Test cases for the load_env_vars function"""
    
    def test_load_env_vars_with_all_defaults(self):
        """Test loading environment variables with all default values"""
        with patch.dict(os.environ, {'DB_PASSWORD': 'test_password'}, clear=True):
            result = load_env_vars()
            
            expected = {
                "DB_PASSWORD": "test_password",
                "DB_HOST": "localhost",
                "DB_PORT": 1433,
                "DB_NAME": "wordle",
                "DB_USER": "sa",
            }
            assert result == expected
    
    def test_load_env_vars_with_custom_values(self):
        """Test loading environment variables with custom values"""
        test_env = {
            'DB_PASSWORD': 'custom_password',
            'DB_HOST': 'custom_host',
            'DB_PORT': '5432',
            'DB_NAME': 'custom_db',
            'DB_USER': 'custom_user'
        }
        
        with patch.dict(os.environ, test_env, clear=True):
            result = load_env_vars()
            
            # the DB_PORT is a string from test_env, so it should be a string in the result
            expected = {
                "DB_PASSWORD": "custom_password",
                "DB_HOST": "custom_host", 
                "DB_PORT": "5432", 
                "DB_NAME": "custom_db",
                "DB_USER": "custom_user",
            }
            assert result == expected
    
    def test_load_env_vars_missing_required_password(self):
        """Test that missing DB_PASSWORD causes sys.exit"""
        with patch.dict(os.environ, {}, clear=True):
            with patch('sys.exit') as mock_exit:
                with patch('pre_deployment.logger') as mock_logger:
                    load_env_vars()
                    
                    mock_logger.error.assert_called_with(
                        "Missing required environment variable: DB_PASSWORD"
                    )
                    mock_exit.assert_called_with(1)
                    
    
    def test_load_env_vars_partial_custom_values(self):
        """Test loading with some custom and some default values"""
        test_env = {
            'DB_PASSWORD': 'test_password',
            'DB_HOST': 'production_host',
            'DB_PORT': '3306'
            # DB_NAME and DB_USER should use defaults
        }
        
        with patch.dict(os.environ, test_env, clear=True):
            result = load_env_vars()
            
            expected = {
                "DB_PASSWORD": "test_password",
                "DB_HOST": "production_host",
                "DB_PORT": "3306",
                "DB_NAME": "wordle",  # default
                "DB_USER": "sa",      # default
            }
            assert result == expected

