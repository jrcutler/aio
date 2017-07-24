from selectors import EVENT_READ, EVENT_WRITE

__all__ = (
    'Trap',
    'Suspend',
)


class Trap:
    """Base class for aio traps"""
    __slots__ = ()
    def __await__(self):
        value = yield self
        return value


class Suspend(Trap):
    """Trap for suspending execution until a specified time"""
    __slots__ = (
        'until',
    )
    def __init__(self, until):
        self.until = until
    def __repr__(self):
        return '{}({!r})'.format(self.__class__.__name__, self.until)


class IO(Trap):
    """Trap for awaiting I/O readiness"""
    __slots__ = (
        'fileobj',
        'events',
    )
    def __init__(self, fileobj, events):
        self.fileobj = fileobj
        self.events = events
    def __repr__(self):
        return '{}({!r}, {!r})'.format(self.__class__.__name__, self.fileobj,
            self.events)
    @classmethod
    def readable(cls, fileobj):
        return cls(fileobj, EVENT_READ)
    @classmethod
    def writable(cls, fileobj):
        return cls(fileobj, EVENT_WRITE)
