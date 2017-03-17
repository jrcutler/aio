from heapq import heappop, heappush
from itertools import count

__all__ = (
    'PriorityQueue',
)


class PriorityQueue:
    """Stable key, value priority queue, where value need not be comparable"""
    __slots__ = (
        'heap',
        'sequence',
    )
    def __init__(self):
        self.heap = []
        self.sequence = count()
    def __len__(self):
        return len(self.heap)
    def push(self, key, value):
        """push (key, value) tuple into queue"""
        entry = (key, next(self.sequence), value)
        heappush(self.heap, entry)
    def pop(self):
        """pop the first value with minimal key from queue"""
        if not self:
            raise KeyError('empty')
        return heappop(self.heap)[2]
    def peek(self):
        """peek at the minimal key from queue"""
        return self.heap[0][0]
