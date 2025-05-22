"""
torero executor module

This module provides functions to interact with the torero CLI.
It's responsible for executing torero commands and parsing their output.
"""

import json
import logging
import subprocess
import shutil
from typing import List, Tuple, Optional
from datetime import datetime

from torero_api.models.service import Service

# Configure logging
logger = logging.getLogger(__name__)

def check_torero_available() -> Tuple[bool, str]:
    """
    Check if torero is available in the system PATH.
    
    Returns:
        Tuple[bool, str]: A tuple containing a boolean indicating whether torero is available
                        and a message with more details
    """

    # Check if torero executable is in PATH
    torero_path = shutil.which("torero")
    if not torero_path:
        return False, "torero executable not found in PATH"
    
    # Check if torero can be executed
    try:
        result = subprocess.run(
            ["torero", "version"],
            capture_output=True,
            text=True,
            check=False,
            timeout=5
        )
        
        if result.returncode != 0:
            return False, f"torero command failed: {result.stderr.strip()}"
        
        return True, "torero is available"
    except subprocess.TimeoutExpired:
        return False, "torero command timed out"
    except Exception as e:
        return False, f"Error checking torero: {str(e)}"

def check_torero_version() -> str:
    """
    Get the version of torero installed.
    
    Returns:
        str: The version of torero, or "unknown" if it couldn't be determined
    """
    try:
        result = subprocess.run(
            ["torero", "version"],
            capture_output=True,
            text=True,
            check=False,
            timeout=5
        )
        
        if result.returncode != 0:
            return "unknown"
        
        # Parse the version from the output
        # Example output: "torero version 1.3.1"
        output_lines = result.stdout.strip().split("\n")
        for line in output_lines:
            if line.startswith("torero"):
                parts = line.split()
                if len(parts) >= 3:
                    return parts[2]
        
        return "unknown"
    except Exception:
        return "unknown"

def get_services() -> List[Service]:
    """
    Execute torero CLI command to get all services.
    
    Makes a system call to 'torero get services --raw' to retrieve the raw JSON
    data of all registered services, then parses and validates this data into
    Service objects.
    
    Returns:
        List[Service]: List of Service objects representing all registered torero services.
    
    Raises:
        RuntimeError: If the torero command fails or returns invalid JSON.
    """
    command = ["torero", "get", "services", "--raw"]
    logger.debug(f"Executing command: {' '.join(command)}")
    
    try:
        # Run the torero command
        proc = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False,
            timeout=30
        )

        if proc.returncode != 0:
            error_msg = f"torero error: {proc.stderr.strip()}"
            logger.error(error_msg)
            raise RuntimeError(error_msg)

        try:
            # Parse the output as JSON
            raw_output = json.loads(proc.stdout)
            
            # Create Service objects
            services = [Service(**svc) for svc in raw_output]
            logger.debug(f"Retrieved {len(services)} services from torero")
            return services
        except json.JSONDecodeError as e:
            error_msg = f"Invalid JSON from torero: {e}"
            logger.error(error_msg)
            logger.debug(f"Raw output: {proc.stdout[:1000]}...")  # Log first 1000 chars
            raise RuntimeError(error_msg)
            
    except subprocess.TimeoutExpired:
        error_msg = "torero command timed out"
        logger.error(error_msg)
        raise RuntimeError(error_msg)
    except Exception as e:
        logger.exception(f"Unexpected error executing torero command: {str(e)}")
        raise RuntimeError(f"Failed to execute torero command: {str(e)}")

def get_service_by_name(name: str) -> Optional[Service]:
    """
    Get a specific service by name.
    
    Args:
        name: The name of the service to retrieve
        
    Returns:
        Optional[Service]: The service if found, None otherwise
        
    Raises:
        RuntimeError: If the torero command fails or returns invalid JSON.
    """
    services = get_services()
    
    for service in services:
        if service.name == name:
            return service
    
    return None

def get_decorators() -> List['Decorator']:
    """
    Execute torero CLI command to get all decorators.
    
    Makes a system call to 'torero get decorators --raw' to retrieve the raw JSON
    data of all registered decorators, then parses and validates this data into
    Decorator objects.
    
    Returns:
        List[Decorator]: List of Decorator objects representing all registered torero decorators.
    
    Raises:
        RuntimeError: If the torero command fails or returns invalid JSON.
    """
    command = ["torero", "get", "decorators", "--raw"]
    logger.debug(f"Executing command: {' '.join(command)}")
    
    try:
        # Run the torero command
        proc = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False,
            timeout=30
        )

        if proc.returncode != 0:
            error_msg = f"torero error: {proc.stderr.strip()}"
            logger.error(error_msg)
            raise RuntimeError(error_msg)

        try:
            # Parse the output as JSON
            raw_output = json.loads(proc.stdout)
            
            # Create Decorator objects
            from torero_api.models.decorator import Decorator
            decorators = [Decorator(**dec) for dec in raw_output]
            logger.debug(f"Retrieved {len(decorators)} decorators from torero")
            return decorators
        except json.JSONDecodeError as e:
            error_msg = f"Invalid JSON from torero: {e}"
            logger.error(error_msg)
            logger.debug(f"Raw output: {proc.stdout[:1000]}...")
            raise RuntimeError(error_msg)
            
    except subprocess.TimeoutExpired:
        error_msg = "torero command timed out"
        logger.error(error_msg)
        raise RuntimeError(error_msg)
    except Exception as e:
        logger.exception(f"Unexpected error executing torero command: {str(e)}")
        raise RuntimeError(f"Failed to execute torero command: {str(e)}")

def get_decorator_by_name(name: str) -> Optional['Decorator']:
    """
    Get a specific decorator by name.
    
    Args:
        name: The name of the decorator to retrieve
        
    Returns:
        Optional[Decorator]: The decorator if found, None otherwise
        
    Raises:
        RuntimeError: If the torero command fails or returns invalid JSON.
    """
    decorators = get_decorators()
    
    for decorator in decorators:
        if decorator.name == name:
            return decorator
    
    return None

def get_repositories() -> List['Repository']:
    """
    Execute torero CLI command to get all repositories.
    
    Makes a system call to 'torero get repositories --raw' to retrieve the raw JSON
    data of all registered repositories, then parses and validates this data into
    Repository objects.
    
    Returns:
        List[Repository]: List of Repository objects representing all registered torero repositories.
    
    Raises:
        RuntimeError: If the torero command fails or returns invalid JSON.
    """
    command = ["torero", "get", "repositories", "--raw"]
    logger.debug(f"Executing command: {' '.join(command)}")
    
    try:
        # Run the torero command
        proc = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False,
            timeout=30
        )

        if proc.returncode != 0:
            error_msg = f"torero error: {proc.stderr.strip()}"
            logger.error(error_msg)
            raise RuntimeError(error_msg)

        try:
            # Parse the output as JSON
            raw_output = json.loads(proc.stdout)
            
            # Create Repository objects
            from torero_api.models.repository import Repository
            repositories = [Repository(**repo) for repo in raw_output]
            logger.debug(f"Retrieved {len(repositories)} repositories from torero")
            return repositories
        except json.JSONDecodeError as e:
            error_msg = f"Invalid JSON from torero: {e}"
            logger.error(error_msg)
            logger.debug(f"Raw output: {proc.stdout[:1000]}...")
            raise RuntimeError(error_msg)
            
    except subprocess.TimeoutExpired:
        error_msg = "torero command timed out"
        logger.error(error_msg)
        raise RuntimeError(error_msg)
    except Exception as e:
        logger.exception(f"Unexpected error executing torero command: {str(e)}")
        raise RuntimeError(f"Failed to execute torero command: {str(e)}")

def get_repository_by_name(name: str) -> Optional['Repository']:
    """
    Get a specific repository by name.
    
    Args:
        name: The name of the repository to retrieve
        
    Returns:
        Optional[Repository]: The repository if found, None otherwise
        
    Raises:
        RuntimeError: If the torero command fails or returns invalid JSON.
    """
    repositories = get_repositories()
    
    for repository in repositories:
        if repository.name == name:
            return repository
    
    return None

def get_secrets() -> List['Secret']:
    """
    Execute torero CLI command to get all secrets.
    
    Makes a system call to 'torero get secrets --raw' to retrieve the raw JSON
    data of all registered secrets, then parses and validates this data into
    Secret objects.
    
    Returns:
        List[Secret]: List of Secret objects representing all registered torero secrets.
    
    Raises:
        RuntimeError: If the torero command fails or returns invalid JSON.
    """
    command = ["torero", "get", "secrets", "--raw"]
    logger.debug(f"Executing command: {' '.join(command)}")
    
    try:
        # Run the torero command
        proc = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False,
            timeout=30
        )

        if proc.returncode != 0:
            error_msg = f"torero error: {proc.stderr.strip()}"
            logger.error(error_msg)
            raise RuntimeError(error_msg)

        try:
            # Parse the output as JSON
            raw_output = json.loads(proc.stdout)
            
            # Create Secret objects
            from torero_api.models.secret import Secret
            secrets = [Secret(**secret) for secret in raw_output]
            logger.debug(f"Retrieved {len(secrets)} secrets from torero")
            return secrets
        except json.JSONDecodeError as e:
            error_msg = f"Invalid JSON from torero: {e}"
            logger.error(error_msg)
            logger.debug(f"Raw output: {proc.stdout[:1000]}...")
            raise RuntimeError(error_msg)
            
    except subprocess.TimeoutExpired:
        error_msg = "torero command timed out"
        logger.error(error_msg)
        raise RuntimeError(error_msg)
    except Exception as e:
        logger.exception(f"Unexpected error executing torero command: {str(e)}")
        raise RuntimeError(f"Failed to execute torero command: {str(e)}")

def get_secret_by_name(name: str) -> Optional['Secret']:
    """
    Get a specific secret by name.
    
    Args:
        name: The name of the secret to retrieve
        
    Returns:
        Optional[Secret]: The secret if found, None otherwise
        
    Raises:
        RuntimeError: If the torero command fails or returns invalid JSON.
    """
    secrets = get_secrets()
    
    for secret in secrets:
        if secret.name == name:
            return secret
    
    return None