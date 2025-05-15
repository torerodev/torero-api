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