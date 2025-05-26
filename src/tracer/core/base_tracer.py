from tracer.store import LogWriter
from tracer import LogDomain

# Abstract base class for tracers
class BaseTracer:
    def __init__(self, domain: LogDomain):
        self.writer = LogWriter(domain)

    def start(self):
        raise NotImplementedError
    
    def stop(self):
        raise NotImplementedError