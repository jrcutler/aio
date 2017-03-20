from time import monotonic as time

from .traps import Suspend

__all__ = (
    'sleep',
    'suspend',
    'time', # alias for time.monotonic
)


async def sleep(delay):
    """Sleep for (at least) delay seconds, returning actual elapsed time"""
    start = time()
    until = start + delay
    actual = await Suspend(until)
    return actual - start


async def suspend(until):
    """Suspend until specified time, return actual resume time"""
    return await Suspend(until)
