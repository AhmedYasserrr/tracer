from tracer.store.log_writer import LogWriter
from tracer.config import LogDomain

# Abstract base class for tracers
class BaseTracer:
    def __init__(self, domain: LogDomain):
        self.writer = LogWriter(domain)

    def start(self):
        raise NotImplementedError
