"""
Command-line interface for torero-api

This module provides the command-line interface for starting and managing the torero API server.
It can be run directly with "python -m torero_api".
"""

import argparse
import logging
import sys
from torero_api.server import start_server
from torero_api.core.torero_executor import check_torero_available, check_torero_version

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
    ]
)
logger = logging.getLogger("torero-api-cli")

def main():
    """
    Main entry point for the torero API CLI.
    
    This function handles command-line arguments and starts the API server.
    """

    # Create argument parser
    parser = argparse.ArgumentParser(
        description="torero API - RESTful API for torero service management",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    # Add command-line arguments
    parser.add_argument("--host", default="0.0.0.0", help="Host to bind the server to")
    parser.add_argument("--port", type=int, default=8000, help="Port to bind the server to")
    parser.add_argument("--log-level", default="info", choices=["debug", "info", "warning", "error", "critical"], 
                        help="Log level to use")
    parser.add_argument("--reload", action="store_true", help="Enable auto-reload (for development)")
    parser.add_argument("--version", action="store_true", help="Show version information and exit")
    parser.add_argument("--check", action="store_true", help="Check torero availability and exit")
    
    # Parse arguments
    args = parser.parse_args()
    
    # Show version information if requested
    if args.version:
        from torero_api import __version__
        print(f"torero-api version: {__version__}")
        
        # Check torero version
        available, message = check_torero_available()
        if available:
            torero_version = check_torero_version()
            print(f"torero version: {torero_version}")
        else:
            print(f"torero: {message}")
        
        sys.exit(0)
    
    # Check torero availability if requested
    if args.check:
        available, message = check_torero_available()
        if available:
            print(f"torero: Available ({check_torero_version()})")
            sys.exit(0)
        else:
            print(f"torero: Not available - {message}")
            sys.exit(1)
    
    # Check if torero is available before starting the server
    available, message = check_torero_available()
    if not available:
        logger.warning(f"torero not available: {message}")
        logger.warning("The API will start, but some functionality may not work correctly.")
    
    # Start the server
    try:
        start_server(
            host=args.host,
            port=args.port,
            log_level=args.log_level,
            reload=args.reload
        )
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Error starting server: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()