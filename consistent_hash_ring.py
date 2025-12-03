import hashlib
import bisect

class ConsistentHashRing:
    def __init__(self, num_replicas=100):
        """
        :param num_replicas: Number of virtual nodes per physical node.
        """
        self.num_replicas = num_replicas
        self.ring = {}  # Map: Hash -> Node Name
        self.sorted_keys = [] # Sorted list of Hash keys for binary search

    def _hash(self, key):
        """
        Generates an MD5 hash for the key.
        Using MD5 ensures better distribution than Python's built-in hash().
        """
        m = hashlib.md5()
        m.update(key.encode('utf-8'))
        # Convert hex digest to a large integer
        return int(m.hexdigest(), 16)

    def add_node(self, node):
        """
        Adds a physical node and its virtual replicas to the ring.
        """
        for i in range(self.num_replicas):
            virtual_node_key = f"{node}-{i}"
            key_hash = self._hash(virtual_node_key)
            
            self.ring[key_hash] = node
            # Insert key in sorted order efficiently
            bisect.insort(self.sorted_keys, key_hash)

    def remove_node(self, node):
        """
        Removes a physical node and its virtual replicas.
        """
        for i in range(self.num_replicas):
            virtual_node_key = f"{node}-{i}"
            key_hash = self._hash(virtual_node_key)
            
            if key_hash in self.ring:
                del self.ring[key_hash]
                # Finding and removing from list is O(N), but necessary here.
                # In production, specialized structures like Red-Black trees are used.
                self.sorted_keys.remove(key_hash)

    def get_node(self, key):
        """
        Returns the physical node responsible for the given key.
        Performs a clockwise lookup (ceil).
        """
        if not self.ring:
            return None

        key_hash = self._hash(key)
        
        # Binary search to find the first index >= key_hash
        index = bisect.bisect_right(self.sorted_keys, key_hash)

        # If index is at the end, wrap around to the first key (Circle structure)
        if index == len(self.sorted_keys):
            index = 0
            
        target_hash = self.sorted_keys[index]
        return self.ring[target_hash]
