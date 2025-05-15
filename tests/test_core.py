"""
Test module for torero API core functionality

This module contains tests for the torero_api core modules, particularly
the torero_executor.py module which interfaces with the torero CLI.
"""

import pytest
from unittest.mock import patch, MagicMock
import subprocess
import json

from torero_api.core.torero_executor import (
    check_torero_available,
    check_torero_version,
    get_services,
    get_service_by_name
)
from torero_api.models.service import Service

# Sample test data
SAMPLE_SERVICES = [
    Service(
        name="test-service-1",
        description="Test service 1",
        type="ansible-playbook",
        tags=["test", "ansible", "network"],
        registries={"file": {"path": "/etc/torero/services/test-service-1"}}
    ),
    Service(
        name="test-service-2",
        description="Test service 2",
        type="opentofu-plan",
        tags=["test", "opentofu", "cloud"],
        registries={"file": {"path": "/etc/torero/services/test-service-2"}}
    )
]

@patch("subprocess.run")
def test_check_torero_available_success(mock_run):
    """Test check_torero_available when torero is available."""

    # Set up the mock
    process_mock = MagicMock()
    process_mock.returncode = 0
    process_mock.stdout = "torero version 1.3.0"
    mock_run.return_value = process_mock
    
    # Call the function
    available, message = check_torero_available()
    
    # Assertions
    assert available is True
    assert message == "torero is available"
    mock_run.assert_called_once_with(
        ["torero", "version"],
        capture_output=True,
        text=True,
        check=False,
        timeout=5
    )

@patch("subprocess.run")
def test_check_torero_available_failure(mock_run):
    """Test check_torero_available when torero is not available."""

    # Set up the mock
    process_mock = MagicMock()
    process_mock.returncode = 1
    process_mock.stderr = "command not found: torero"
    mock_run.return_value = process_mock
    
    # Call the function
    available, message = check_torero_available()
    
    # Assertions
    assert available is False
    assert "torero command failed" in message
    mock_run.assert_called_once()

@patch("subprocess.run")
def test_check_torero_available_timeout(mock_run):
    """Test check_torero_available when torero command times out."""

    # Set up the mock
    mock_run.side_effect = subprocess.TimeoutExpired(cmd="torero version", timeout=5)
    
    # Call the function
    available, message = check_torero_available()
    
    # Assertions
    assert available is False
    assert message == "torero command timed out"
    mock_run.assert_called_once()

@patch("subprocess.run")
def test_check_torero_version(mock_run):
    """Test check_torero_version function."""

    # Set up the mock
    process_mock = MagicMock()
    process_mock.returncode = 0
    process_mock.stdout = "torero version 1.3.0\nSome other info\n"
    mock_run.return_value = process_mock
    
    # Call the function
    version = check_torero_version()
    
    # Assertions
    assert version == "1.3.0"
    mock_run.assert_called_once()

@patch("subprocess.run")
def test_check_torero_version_error(mock_run):
    """Test check_torero_version when an error occurs."""

    # Set up the mock
    process_mock = MagicMock()
    process_mock.returncode = 1
    process_mock.stderr = "Error: torero command not found"
    mock_run.return_value = process_mock
    
    # Call the function
    version = check_torero_version()
    
    # Assertions
    assert version == "unknown"
    mock_run.assert_called_once()

@patch("subprocess.run")
def test_get_services(mock_run):
    """Test get_services function."""

    # Set up the mock
    process_mock = MagicMock()
    process_mock.returncode = 0
    process_mock.stdout = json.dumps([
        {
            "name": "test-service-1",
            "description": "Test service 1",
            "type": "ansible-playbook",
            "tags": ["test", "ansible", "network"],
            "registries": {"file": {"path": "/etc/torero/services/test-service-1"}}
        },
        {
            "name": "test-service-2",
            "description": "Test service 2",
            "type": "opentofu-plan",
            "tags": ["test", "opentofu", "cloud"],
            "registries": {"file": {"path": "/etc/torero/services/test-service-2"}}
        }
    ])
    mock_run.return_value = process_mock
    
    # Call the function
    services = get_services()
    
    # Assertions
    assert len(services) == 2
    assert services[0].name == "test-service-1"
    assert services[0].type == "ansible-playbook"
    assert "ansible" in services[0].tags
    assert services[1].name == "test-service-2"
    assert services[1].type == "opentofu-plan"
    assert "cloud" in services[1].tags
    mock_run.assert_called_once_with(
        ["torero", "get", "services", "--raw"],
        capture_output=True,
        text=True,
        check=False,
        timeout=30
    )

@patch("subprocess.run")
def test_get_services_error(mock_run):
    """Test get_services function when an error occurs."""

    # Set up the mock
    process_mock = MagicMock()
    process_mock.returncode = 1
    process_mock.stderr = "Error: torero command failed"
    mock_run.return_value = process_mock
    
    # Call the function and expect an exception
    with pytest.raises(RuntimeError) as excinfo:
        get_services()
    
    # Assertions
    assert "torero error" in str(excinfo.value)
    mock_run.assert_called_once()

@patch("subprocess.run")
def test_get_services_invalid_json(mock_run):
    """Test get_services function with invalid JSON response."""

    # Set up the mock
    process_mock = MagicMock()
    process_mock.returncode = 0
    process_mock.stdout = "Not a valid JSON"
    mock_run.return_value = process_mock
    
    # Call the function and expect an exception
    with pytest.raises(RuntimeError) as excinfo:
        get_services()
    
    # Assertions
    assert "Invalid JSON" in str(excinfo.value)
    mock_run.assert_called_once()

@patch("torero_api.core.torero_executor.get_services")
def test_get_service_by_name_found(mock_get_services):
    """Test get_service_by_name when service is found."""

    # Set up the mock
    mock_get_services.return_value = SAMPLE_SERVICES
    
    # Call the function
    service = get_service_by_name("test-service-1")
    
    # Assertions
    assert service is not None
    assert service.name == "test-service-1"
    assert service.type == "ansible-playbook"
    mock_get_services.assert_called_once()

@patch("torero_api.core.torero_executor.get_services")
def test_get_service_by_name_not_found(mock_get_services):
    """Test get_service_by_name when service is not found."""

    # Set up the mock
    mock_get_services.return_value = SAMPLE_SERVICES
    
    # Call the function
    service = get_service_by_name("non-existent-service")
    
    # Assertions
    assert service is None
    mock_get_services.assert_called_once()