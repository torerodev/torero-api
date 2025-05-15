"""
Data models for the torero API

This package contains Pydantic models that define the data structures
used throughout the torero API. These models provide type validation,
serialization/deserialization, and documentation through OpenAPI schemas.

The models are designed to be MCP-compatible, providing rich type
information and examples to assist AI systems in understanding the API.

Models:
- Service: Represents a torero service with its metadata
- ErrorResponse: Standard error response format
- APIInfo: Information about the API and available endpoints
"""

# Re-export models for easier imports
from torero_api.models.service import Service, ServiceType
from torero_api.models.common import ErrorResponse, APIInfo