# Abstract base class for tracers
class BaseTracer:
    def __init__(self, writer):
        self.writer = writer

    def start(self):
        raise NotImplementedError
