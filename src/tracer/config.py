# Central config (e.g., paths, domains, etc.)
from pathlib import Path
from enum import Enum

# Root folder where logs are stored (relative to tracer module)
BASE_DIR = Path(__file__).resolve().parent
LOG_DIR = BASE_DIR / "logs"

# Ensure the directory exists
LOG_DIR.mkdir(parents=True, exist_ok=True)

# Enum for log domains
class LogDomain(Enum):
    FS = "file_system"
    NET = "networking"
    
    def __str__(self):
        return self.value

# Function to get log file path for a specific domain
def get_log_file(domain: LogDomain) -> Path:
    log_file = LOG_DIR / f"{domain.value}.jsonl"
    if not log_file.exists():
        log_file.touch()  # Create if it doesn't exist
    return log_file

# Example usage
FS_LOG_FILE = get_log_file(LogDomain.FS)
NET_LOG_FILE = get_log_file(LogDomain.NET)
