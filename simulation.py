import uuid
from collections import defaultdict
import statistics
from consistent_hash_ring import ConsistentHashRing

def run_scenario(v_nodes):
    print(f"Running Simulation with {v_nodes} virtual nodes per server...")
    ring = ConsistentHashRing(num_replicas=v_nodes)

    # 1. Add 5 Initial Nodes
    servers = ["Server_A", "Server_B", "Server_C", "Server_D", "Server_E"]
    for s in servers:
        ring.add_node(s)

    # 2. Distribute 10,000 Unique Keys
    total_keys = 10000
    keys = [str(uuid.uuid4()) for _ in range(total_keys)]
    initial_mapping = {}
    
    # Calculate load distribution
    node_counts = defaultdict(int)

    for k in keys:
        node = ring.get_node(k)
        initial_mapping[k] = node
        node_counts[node] += 1
    
    print("  Initial Distribution:")
    for s in servers:
        print(f"    {s}: {node_counts[s]}")
    
    # Calculate Standard Deviation to show load balance quality
    counts = list(node_counts.values())
    if len(counts) > 1:
        print(f"  Standard Deviation: {statistics.stdev(counts):.2f}")

    # 3. Remove one node (Server_C)
    print("\n  -> Removing 'Server_C'...")
    ring.remove_node("Server_C")

    # 4. Calculate Remapping Stats
    remapped_keys = 0
    
    for k in keys:
        new_node = ring.get_node(k)
        if new_node != initial_mapping[k]:
            remapped_keys += 1
            
    percentage = (remapped_keys / total_keys) * 100
    print(f"  Keys Remapped: {remapped_keys} / {total_keys} ({percentage:.2f}%)")
    print(f"  Note: Ideal remapping for 5 nodes -> 4 nodes is 20%.\n")
    print("-" * 40 + "\n")

if __name__ == "__main__":
    print("=== Consistent Hashing Simulation (Python) ===\n")
    
    # Scenario 1: 10 Virtual Nodes (High Variance)
    run_scenario(10)
    
    # Scenario 2: 100 Virtual Nodes (Low Variance)
    run_scenario(100)