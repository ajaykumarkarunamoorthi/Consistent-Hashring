import hashlib
import bisect
import statistics

class ConsistentHashRing:
    def __init__(self, physical_nodes=None, virtual_nodes=100):
        """
        Initialize the Consistent Hash Ring.
        :param physical_nodes: List of initial physical node names (e.g., ['Node1', 'Node2'])
        :param virtual_nodes: Number of vnodes per physical node (default 100 as per requirements)
        """
        self.virtual_nodes = virtual_nodes
        self.ring = {}  # Maps hash_value -> physical_node_name
        self.sorted_keys = []  # Sorted list of hash values for binary search
        
        if physical_nodes:
            for node in physical_nodes:
                self.add_node(node)

    def _hash(self, key):
        """
        Generates a hash for a given key.
        Using MD5 as it is fast and provides good distribution for this simulation.
        Returns an integer.
        """
        return int(hashlib.md5(key.encode('utf-8')).hexdigest(), 16)

    def add_node(self, node):
        """Adds a physical node and its virtual nodes to the ring."""
        for i in range(self.virtual_nodes):
            vnode_key = f"{node}#{i}"
            hash_val = self._hash(vnode_key)
            self.ring[hash_val] = node
            bisect.insort(self.sorted_keys, hash_val)

    def remove_node(self, node):
        """Removes a physical node and its virtual nodes from the ring."""
        for i in range(self.virtual_nodes):
            vnode_key = f"{node}#{i}"
            hash_val = self._hash(vnode_key)
            if hash_val in self.ring:
                del self.ring[hash_val]
                # Note: removing from list is O(N), but acceptable for this simulation scale
                self.sorted_keys.remove(hash_val)

    def get_node(self, key):
        """
        Maps an arbitrary string key (e.g., UserID) to a specific physical node.
        Uses binary search (bisect) to find the next node on the ring.
        """
        if not self.ring:
            return None
        
        hash_val = self._hash(key)
        
        # Find the first hash in the ring >= the key's hash
        idx = bisect.bisect_right(self.sorted_keys, hash_val)
        
        # If we reach the end of the list, wrap around to the first node (Circle structure)
        if idx == len(self.sorted_keys):
            idx = 0
            
        return self.ring[self.sorted_keys[idx]]

# --- SIMULATION DRIVER ---

def run_simulation():
    print("--- STARTING CONSISTENT HASHING SIMULATION ---\n")
    
    # 1. Setup
    nodes = ["Node_A", "Node_B", "Node_C"]
    ch = ConsistentHashRing(nodes, virtual_nodes=100)
    total_keys = 10000
    
    # Generate random keys
    import uuid
    keys = [str(uuid.uuid4()) for _ in range(total_keys)]
    
    # Helper to calculate distribution
    def get_distribution(ring_instance, key_list):
        dist = {node: 0 for node in set(ring_instance.ring.values())}
        assignments = {}
        for k in key_list:
            node = ring_instance.get_node(k)
            dist[node] += 1
            assignments[k] = node
        return dist, assignments

    # 2. Initial Distribution
    print(f"Step 1: Distributing {total_keys} keys across {len(nodes)} nodes...")
    dist_initial, assignments_initial = get_distribution(ch, keys)
    
    for node, count in dist_initial.items():
        print(f"  {node}: {count} keys ({count/total_keys*100:.2f}%)")
    
    counts = list(dist_initial.values())
    print(f"  Standard Deviation: {statistics.stdev(counts):.2f}")
    print("-" * 30)

    # 3. Add a Node (Node_D)
    print("\nStep 2: Adding 'Node_D'...")
    ch.add_node("Node_D")
    dist_after_add, assignments_after_add = get_distribution(ch, keys)
    
    moved_keys = 0
    for k in keys:
        if assignments_initial[k] != assignments_after_add[k]:
            moved_keys += 1
            
    print(f"  Keys moved: {moved_keys}")
    print(f"  Data Movement: {(moved_keys/total_keys)*100:.2f}% (Ideal is ~25% for 4 nodes)")
    print("-" * 30)

    # 4. Remove a Node (Node_A)
    print("\nStep 3: Removing 'Node_A'...")
    ch.remove_node("Node_A")
    dist_after_remove, assignments_after_remove = get_distribution(ch, keys)
    
    moved_keys_remove = 0
    for k in keys:
        if assignments_after_add[k] != assignments_after_remove[k]:
            moved_keys_remove += 1

    print(f"  Keys moved: {moved_keys_remove}")
    print(f"  Data Movement: {(moved_keys_remove/total_keys)*100:.2f}% (Ideal is ~33% for 3 nodes)")
    print("-" * 30)
    print("\nSimulation Complete.")

if __name__ == "__main__":
    run_simulation()