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
