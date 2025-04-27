# tracer

A CLI tool for tracing. The project is designed to provide a modular and extensible tracer module. It includes tools for logging, tracing, and analyzing device behavior.

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
    │   └── future_tracer.py        # Placeholder for new domains
    │
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
    └── cli.py                      # (Optional) CLI interface to run tracers
```

---

## Installation

First, make sure you have **Python 3.10+** installed.

1. **Clone the repository**:

   ```bash
   git clone https://github.com/AhmedYasserrr/tracer.git
   cd tracer
   ```

2. **Install the package** locally:

   ```bash
   pip install .
   ```

This will install `tracer` and make its CLI available.

---

### Development Installation

For development purposes, install the package in **editable mode**:

```bash
pip install -e .
```

This allows you to freely edit the code and have changes take effect immediately without needing to reinstall.

---
