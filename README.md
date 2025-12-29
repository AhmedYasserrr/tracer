# tracer

A Python CLI tool and library for tracing filesystem and network activity with MCP (Model Context Protocol) server architecture. The project provides a modular and extensible tracer system that runs as a centralized daemon service, allowing CLI tools and LLMs to interact with tracers through a standardized interface.

## Project Structure

```
tracer/
  ├── pyproject.toml
  ├── .gitignore
  ├── README.md
  ├── src/tracer/
    ├── __init__.py
    ├── cli/                        # CLI interface and MCP client
    │   ├── __init__.py
    │   ├── client.py              # MCP HTTP client for communication
    │   ├── command_parser.py      # Argument parsing for all commands
    │   └── interface.py           # Command interface wrapping MCP calls
    │
    ├── core/
    │   ├── __init__.py
    │   ├── base_tracer.py          # Abstract base class for tracers
    │   ├── fs_tracer.py           # File system tracing logic (threaded)
    │   └── net_tracer.py          # Network tracing logic (threaded)
    │
    ├── server/                     # MCP Server implementation
    │   ├── __init__.py
    │   ├── mcp_server.py          # Main MCP server with HTTP transport
    │   ├── tools.py               # MCP tools for tracing operations
    │   └── resources.py           # MCP resources for database access
    │
    ├── db/
    │   ├── __init__.py
    │   ├── connection.py          # Engine setup, SessionLocal, and DB initialization
    │   ├── models.py              # SQLAlchemy Declarative Models (tables)
    │   └── crud/                  # Database CRUD operations
    │       ├── __init__.py
    │       ├── base_crud.py
    │       ├── fs_crud.py
    │       └── net_crud.py
    │
    ├── store/
    │   ├── __init__.py
    │   ├── log_writer.py          # Appending logs with rotation
    │   └── log_reader.py          # Reverse iterator, timestamp filtering
    │
    ├── utils/
    │   ├── __init__.py
    │   └── timestamp.py           # Formatters, converters, etc.
    │
    ├── logs/                      # Log files and database
    │   ├── file_system.jsonl
    │   ├── network.jsonl
    │   └── tracer.db
    │
    ├── config.py                  # Central config (paths, domains, etc.)
    ├── tracer_core.py            # Core tracer management (threaded)
    ├── __init__.py
    └── __main__.py               # CLI entry point (MCP client)
```

---

## Architecture

The tracer uses a **centralized daemon architecture** with MCP (Model Context Protocol) for communication:

- **`tracerd`** - Background daemon service that manages all tracers
- **CLI Client** - Communicates with daemon via MCP HTTP calls
- **Threaded Tracers** - Each tracer runs in its own thread for non-blocking operation
- **Database Storage** - SQLite database for persistent log storage
- **LLM Integration** - External LLMs can interact with the same MCP interface

---

## Installation

### Prerequisites
- Python 3.10 or higher
- `pip` (Python package manager)


1. **Clone the repository**:

   ```bash
   git clone https://github.com/AhmedYasserrr/tracer.git
   cd tracer
   ```

2. **Build the package**:

   ```bash
   python -m build
   ```

   This will create a distributable package in the `dist/` directory.

3. **Install the package**:

   ```bash
   pip install dist/tracer-0.1.0-py3-none-any.whl
   ```

This ensures a clean and reliable installation.

---

### Development Installation

For development purposes, install the package in **editable mode**:

```bash
pip install -e .
```

This allows you to freely edit the code and have changes take effect immediately without needing to reinstall.

---

---

## Usage

### Starting the MCP Server

First, start the tracer daemon (MCP server):
```bash
# Start the MCP server on default port 9999
server
```

### CLI Commands

All CLI commands communicate with the running daemon via MCP calls:

### Start Tracing
Start tracing for a specific domain:
```bash
# Filesystem tracing (requires directory)
tracer start file_system --dir /path/to/watch

# Network tracing
tracer start network
```

### Stop Tracing
Stop tracing for a specific domain:
```bash
# Stop filesystem tracing for specific directory
tracer stop file_system --dir /path/to/watch

# Stop network tracing
tracer stop network
```

### Show Recent Logs
Display recent logs for a domain (last 10 entries):
```bash
tracer show file_system
tracer show network
```

### Execute SQL Queries
Run custom SQL queries against the database:
```bash
tracer query "SELECT * FROM file_system WHERE action='created' LIMIT 5"
tracer query "SELECT COUNT(*) FROM network WHERE timestamp > '2024-01-01'"
```

### List Commands
Get information about available domains and active tracers:
```bash
# List all available tracing domains
tracer list-domains

# List currently active tracers with thread status
tracer list-tracers
```

### Database Operations
Manage the database and logs:
```bash
# Clear logs for a specific domain
tracer clear file_system
tracer clear network

# Reset entire database (drops and recreates all tables)
tracer reset
```

### Schema Inspection
View database table structure and contents:
```bash
# Read table schema/contents for a domain
tracer schema file_system
tracer schema network
```
