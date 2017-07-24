from collections import deque
from selectors import DefaultSelector

from .priorityqueue import PriorityQueue
from .traps import Suspend, IO, Trap
from .util import time

__all__ = (
    'EventLoop',
)


class EventLoop:
    def __init__(self, *, selector=None):
        if selector is None:
            selector = DefaultSelector()
        self._selector = selector
        self._running = False
        self._closed = False
        self._stopping = False
        self._ready = deque()
        self._scheduled = PriorityQueue()
    def is_running(self):
        return self._running
    def is_closed(self):
        return self._closed
    def close(self):
        if self.is_running():
            raise RuntimeError('cannot close while running')
        if self.is_closed():
            return
        self._selector.close()
        self._closed = True
    def stop(self):
        self._stopping = True
    def run_until_complete(self, *tasks):
        for task in tasks:
            self._add_ready(task)
        self.run()
    def run(self):
        if self.is_running():
            raise RuntimeError('already running')
        self._running = True
        try:
            while not self._stopping and (self._ready or self._scheduled or
                                          self._selector._map):
                self._run_once()
        finally:
            self._running = False
            self._stopping = False
    def _add_ready(self, task, value=None, *, exc=None, last_io=None):
        self._ready.append((task, value, exc, last_io))
    def _add_scheduled(self, task, when):
        self._scheduled.push(when, task)
    def _add_io(self, task, trap):
        self._selector.register(trap.fileobj, trap.events, (task, trap))
    def _remove_io(self, trap):
        self._selector.unregister(trap.fileobj)
    def _run_once(self):
        # determine timeout
        if self._ready:
            timeout = 0
        elif self._scheduled:
            when = self._scheduled.peek()
            now = time()
            timeout = max(0, when - now)
        else:
            # waiting for I/O only
            timeout = None
        # wait for timeout or I/O readiness events
        for key, mask in self._selector.select(timeout):
            # move I/O handlers to ready
            task, last_io = key.data
            self._add_ready(task, mask, last_io=last_io)
        # move expired scheduled tasks to ready
        wakeup = time()
        while self._scheduled and self._scheduled.peek() <= now:
            task = self._scheduled.pop()
            self._add_ready(task, wakeup)
        # handle all tasks that are ready now
        nready = len(self._ready)
        for _ in range(nready):
            task, value, exc, last_io = self._ready.popleft()
            unregister = last_io is not None
            try:
                if exc is None:
                    trap = task.send(value)
                else:
                    trap = task.throw(exc)
                if isinstance(trap, Trap):
                    if isinstance(trap, Suspend):
                        self._add_scheduled(task, trap.until)
                    elif isinstance(trap, IO):
                        if last_io is not None and last_io != trap:
                            unregister = False
                        else:
                            self._add_io(task, trap)
                    else:
                        raise TypeError('{!r} awaited unknown Trap: {!r}'
                            .format(task, trap))
                else:
                    raise TypeError('{!r} awaited non-Trap object: {!r}'
                        .format(task, trap))
            except StopIteration as e:
                # TODO: handle task done (e.value)
                print('{!r} returned {!r}'.format(task, e.value))
                pass
            except Exception:
                # TODO: handle exceptions
                import traceback
                traceback.print_exc()
            if unregister:
                self._remove_io(last_io)
