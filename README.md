# tracer

A Python CLI tool and library for tracing filesystem and network activity. The project is designed to provide a modular and extensible tracer module. It includes tools for logging, tracing, and analyzing device behavior.

## Project Structure

```
tracer/
  ├── pyproject.toml
  ├── .gitignore
  ├── README.md
  ├── src/tracer/
    ├── __init__.py
    ├── core/
    │   ├── __init__.py
    │   ├── base_tracer.py          # Abstract base class for tracers
    │   ├── file_tracer.py          # File system tracing logic
    │   ├── net_tracer.py           # Network tracing logic
    │
    ├── mcp/   
    │   ├── __init__.py
    │   ├── server.py
    │   ├── tools.py
    │   └── resources.py
    |
    ├── db/
    │   ├── __init__.py
    │   ├── connection.py    # Engine setup, SessionLocal, and DB initialization
    │   ├── models.py        # SQLAlchemy Declarative Models (your tables)
    |
    ├── store/
    │   ├── __init__.py
    │   ├── log_writer.py           # Appending logs, maybe with rotation
    │   └── log_reader.py           # Reverse iterator, filtering by timestamp
    │
    ├── utils/
    │   ├── __init__.py
    │   └── timestamp.py            # Formatters, converters, etc.
    │
    ├── logs/
    ├── config.py                   # Central config (e.g., paths, domains, etc.)
    ├── command_parser.py
    ├── tracer_core.py              
    ├── __init__.py
    └── __main__.py                 # entry point     
```

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

### Start Tracing
Start tracing for a specific domain (e.g., `file_system` for filesystem or `network` for network):
```bash
tracer start file_system --dir path/to/watch
```

### Show Logs
Show logs for a specific domain, optionally filtering by time range:
```bash
tracer show file_system --start "yesterday" --end "now"
```

### Clear Logs
Clear all logs for a specific domain:
```bash
tracer clear file_system
```