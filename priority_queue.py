import heapq
from node import Node  # Assuming Node class is in node.py, import it

# Define the priority queue class
class PriorityQueue:
    def __init__(self):
        self._queue = []
        self._index = 0  # To maintain the insertion order in case of ties

    def push(self, time, node):
        """Add a new object with time and node to the priority queue."""
        # We store the time and node as a tuple, and use a counter (_index) to ensure proper ordering in case of tie times.
        heapq.heappush(self._queue, (time, self._index, node))
        self._index += 1  # Increment index to maintain uniqueness

    def pop(self):
        """Pop the object with the minimum time (earliest event) and return both time and node."""
        if self._queue:
            # Return both the time and node (object)
            time, _, node = heapq.heappop(self._queue)
            return time, node
        else:
            return None  # If the queue is empty

    def is_empty(self):
        """Check if the priority queue is empty."""
        return len(self._queue) == 0


# Example usage:

# Assuming we have a Node class with some attributes like node_id

