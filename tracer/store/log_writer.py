import json
from datetime import datetime
from tracer.config import get_log_file, LogDomain

class LogWriter:
    def __init__(self, domain: LogDomain):
        self.file_path = get_log_file(domain)

    def append(self, event: dict):
        event["timestamp"] = event.get("timestamp") or datetime.utcnow().isoformat()
        with open(self.file_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(event) + "\n")