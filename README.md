# 🚀 torero RESTful API
Fast, and type-safe API that provides programmatic access to [torero](https://torero.dev). Built with [FastAPI](https://fastapi.tiangolo.com/) and created for the purpose of providng a communication interface for MCP _(model context protocol)_.

## ✨ Features
🚀 **High Performance**: Built on FastAPI with async support  
🔍 **Service Discovery**: List, filter, and search torero services  
🎯 **Smart Filtering**: Filter by service type, tags, and metadata  
📊 **Comprehensive Coverage**: Services, decorators, repositories, and registries  
⚡ **Service Execution**: Execute Ansible playbooks, Python scripts, and OpenTofu plans  
🗂️ **Registry Management**: Manage package registries (Ansible Galaxy, PyPI, etc.)  
📖 **Auto Documentation**: Interactive API docs with OpenAPI/Swagger  
🤖 **AI Ready**: MCP (Model Context Protocol) compatible for AI integrations  
⚡ **Developer Friendly**: Type hints, validation, and clear error messages  

## 🚦 Quick Start

### Prerequisites
- Python 3.10 or higher
- torero CLI installed and available in _PATH_

### Installation
```bash
# Install from source
git clone https://github.com/torerodev/torero-api.git
cd torero-api
pip install -e .
```

### Running the API
```bash
# Start the server
torero-api

# Custom host and port
torero-api --host 0.0.0.0 --port 8080

# Development mode with auto-reload
torero-api --reload

# Run as background daemon
torero-api --daemon

# Daemon with custom settings
torero-api --daemon --host 0.0.0.0 --port 8080 --log-file /var/log/torero-api.log
```

### Verify Installation
```bash
# Check if torero is available
torero-api --check

# Show version information
torero-api --version

# Test the API
curl http://localhost:8000/health
```

## 📚 API Documentation
Once running, visit:

- **Interactive docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI schema**: http://localhost:8000/openapi.json

## 🎯 API Endpoints

| Method | Endpoint | Description | Query Parameters |
|--------|----------|-------------|------------------|
| **Services** | | | |
| `GET` | `/v1/services/` | List all services | `type`, `tag`, `skip`, `limit` |
| `GET` | `/v1/services/types` | Get available service types | - |
| `GET` | `/v1/services/tags` | Get all service tags | - |
| `GET` | `/v1/services/{name}` | Get specific service details | - |
| `GET` | `/v1/services/{name}/describe` | Get detailed service description | - |
| **Service Execution** | | | |
| `POST` | `/v1/execution/ansible-playbook/{name}` | Execute Ansible playbook service | - |
| `POST` | `/v1/execution/python-script/{name}` | Execute Python script service | - |
| `POST` | `/v1/execution/opentofu-plan/{name}/apply` | Apply OpenTofu plan service | - |
| `POST` | `/v1/execution/opentofu-plan/{name}/destroy` | Destroy OpenTofu plan resources | - |
| **Decorators** | | | |
| `GET` | `/v1/decorators/` | List all decorators | `type`, `skip`, `limit` |
| `GET` | `/v1/decorators/types` | Get decorator types | - |
| `GET` | `/v1/decorators/{name}` | Get specific decorator details | - |
| **Repositories** | | | |
| `GET` | `/v1/repositories/` | List all repositories | `type`, `skip`, `limit` |
| `GET` | `/v1/repositories/types` | Get repository types | - |
| `GET` | `/v1/repositories/{name}` | Get specific repository details | - |
| **Registries** | | | |
| `GET` | `/v1/registries/` | List all registries | `type` |
| `GET` | `/v1/registries/types` | Get registry types | - |
| `GET` | `/v1/registries/{name}` | Get specific registry details | - |
| **Secrets** | | | |
| `GET` | `/v1/secrets/` | List all secrets (metadata only) | `type`, `skip`, `limit` |
| `GET` | `/v1/secrets/types` | Get secret types | - |
| `GET` | `/v1/secrets/{name}` | Get specific secret metadata | - |
| **System** | | | |
| `GET` | `/` | API information and navigation | - |
| `GET` | `/health` | Health check with torero status | - |

## 💡 Usage Examples
```bash
# Get all services
curl "http://localhost:8000/v1/services/"

# Filter by type
curl "http://localhost:8000/v1/services/?type=ansible-playbook"

# Filter by tag
curl "http://localhost:8000/v1/services/?tag=network"

# Pagination
curl "http://localhost:8000/v1/services/?skip=0&limit=10"

# Get detailed description of a specific service
curl "http://localhost:8000/v1/services/my-service/describe"

# Execute an Ansible playbook service
curl -X POST "http://localhost:8000/v1/execution/ansible-playbook/hello-ansible"

# Execute a Python script service
curl -X POST "http://localhost:8000/v1/execution/python-script/data-processor"

# Apply OpenTofu infrastructure
curl -X POST "http://localhost:8000/v1/execution/opentofu-plan/infrastructure-deploy/apply"

# Destroy OpenTofu infrastructure
curl -X POST "http://localhost:8000/v1/execution/opentofu-plan/infrastructure-deploy/destroy"

# Get all registries
curl "http://localhost:8000/v1/registries/"

# Filter registries by type
curl "http://localhost:8000/v1/registries/?type=ansible-galaxy"
```

### Python Client Example
```python
import httpx

# Initialize client
client = httpx.Client(base_url="http://localhost:8000")

# Get all services
response = client.get("/v1/services/")
services = response.json()

# Filter services by type
response = client.get("/v1/services/", params={"type": "ansible-playbook"})
ansible_services = response.json()

# Get specific service
response = client.get("/v1/services/my-service")
service_details = response.json()

# Execute a service
response = client.post("/v1/execution/ansible-playbook/hello-ansible")
execution_result = response.json()
print(f"Exit code: {execution_result['return_code']}")
print(f"Output: {execution_result['stdout']}")

# Get registries
response = client.get("/v1/registries/")
registries = response.json()
```

## 🏗️ Development

### Setup Environment
```bash
# Clone the repository
git clone https://github.com/torerodev/torero-api.git
cd torero-api

# Install with development dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

### Running Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=torero_api

# Run specific test file
pytest tests/test_services.py

# Verbose output
pytest -v
```

### Generate OpenAPI Schema

```bash
# Generate schema file
generate-openapi -o docs/openapi.json

# Generate YAML version (requires PyYAML)
pip install ".[yaml]"
generate-openapi -o docs/openapi.yaml
```

## ⚙️ Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `TORERO_API_HOST` | `localhost` | API server host |
| `TORERO_API_PORT` | `8000` | API server port |
| `TORERO_API_PID_FILE` | `/tmp/torero-api.pid` | PID file for daemon mode |
| `TORERO_API_LOG_FILE` | `/tmp/torero-api.log` | Log file for daemon mode |

### CLI Options

```bash
torero-api --help

Options:
  --host TEXT          Host to bind the server to [default: 0.0.0.0]
  --port INTEGER       Port to bind the server to [default: 8000]
  --log-level TEXT     Log level [default: info]
  --reload             Enable auto-reload (development)
  --daemon             Run as background daemon
  --pid-file TEXT      PID file for daemon mode [default: /tmp/torero-api.pid]
  --log-file TEXT      Log file for daemon mode [default: /tmp/torero-api.log]
  --version            Show version information
  --check              Check torero availability
```

## 🛠️ Daemon Management

Use the included control script for easier daemon management:

```bash
# Make the control script executable
chmod +x scripts/torero_api_ctl.sh

# Start daemon
./scripts/torero_api_ctl.sh start

# Check status
./scripts/torero_api_ctl.sh status

# View logs
./scripts/torero_api_ctl.sh logs

# Follow logs in real-time
./scripts/torero_api_ctl.sh follow-logs

# Stop daemon
./scripts/torero_api_ctl.sh stop

# Restart daemon
./scripts/torero_api_ctl.sh restart
```