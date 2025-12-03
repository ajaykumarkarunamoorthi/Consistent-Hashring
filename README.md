# Consistent-Hashring
**3. Simulation Results & Analysis**

* **Initial Distribution:**
    * Simulation run with 10,000 keys and 3 Physical Nodes (100 vnodes each).
    * Resulting distribution: Node C (38.10%), Node B (33.24%), Node A (28.66%).
    * Standard Deviation: 472.07.
    * *Observation:* The distribution is reasonably balanced, avoiding hotspots where one server takes all traffic.

* **Node Addition (Scaling Up):**
    * Added 'Node_D' to the ring.
    * **Data Movement:** 23.36%.
    * *Analysis:* This aligns closely with the theoretical ideal of 25% (1/N) for a 4-node cluster. This confirms that the algorithm successfully minimized data migration; in a naive hashing approach, nearly 75% of data would have shifted.

* **Node Removal (Scaling Down):**
    * Removed 'Node_A'.
    * **Data Movement:** 21.29%.
    * *Analysis:* The percentage of moved data corresponds almost exactly to the load previously held by Node A. This proves that surviving nodes (B, C, D) were unaffected, and only the orphaned keys were redistributed.
