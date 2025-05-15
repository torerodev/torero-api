"""
API package for torero-api

This package contains the API endpoints and routing configuration
for the torero-api service. It organizes endpoints by version and
resource type, following RESTful API best practices to ensure
a consistent and intuitive interface for clients.

The API is designed to be compatible with the Model Context Protocol (MCP),
providing detailed type information and following OpenAPI standards.
"""

# Version re-export for easier imports
from torero_api import __version__