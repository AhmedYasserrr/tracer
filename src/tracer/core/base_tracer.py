from tracer.store import LogWriter
from tracer import LogDomain
from tracer.db.crud import get_crud_class


# Abstract base class for tracers
class BaseTracer:
    def __init__(self, domain: LogDomain):
        self.writer = LogWriter(domain)
        self.crud = get_crud_class(domain)

    def start(self):
        raise NotImplementedError

    def stop(self):
        raise NotImplementedError
