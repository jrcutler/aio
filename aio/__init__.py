__all__ = (
    'EventLoop',
    'sleep',
    'suspend',
    'time',
)

from .kernel import EventLoop
from .util import sleep, suspend, time
