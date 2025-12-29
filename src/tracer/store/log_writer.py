import json
from datetime import datetime
from tracer import get_log_file, LogDomain
from tracer.db.crud import get_crud_class
from tracer.db.connection import clear_domain_table


class LogWriter:
    def __init__(self, domain: LogDomain):
        self.domain = domain
        self.file_path = get_log_file(domain)
        self.crud = get_crud_class(domain)

    def append(self, event: dict):
        with self.crud() as crud_instance:
            crud_instance.add(event.copy())

        event["timestamp"] = event.get("timestamp") or datetime.utcnow().isoformat()
        with open(self.file_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(event) + "\n")

    def clear(self):
        """Clear all contents from the log file and reset the database."""
        clear_domain_table(self.domain.value)
        with open(self.file_path, "w", encoding="utf-8") as f:
            f.truncate(0)
