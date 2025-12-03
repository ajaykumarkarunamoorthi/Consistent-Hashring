# Consistent Hashing with Virtual Nodes (Python)

## Project Overview
This project implements a **Consistent Hashing Ring** in Python. It solves the problem of distributing data across distributed servers while minimizing data migration when servers are added or removed.

It focuses specifically on the concept of **Virtual Nodes (vnodes)**,  showing how increasing the number of vnodes leads to a more uniform load distribution.

## 1. Implementation Details

### Data Structure: `bisect` + `dict`
Python's standard library does not include a Red-Black tree (like Java's `TreeMap`). To achieve efficient **O(log N)** lookups, we used:
1.  **`self.ring` (dict):** Maps a hash value to a physical server name.
2.  **`self.sorted_keys` (list):** Keeps all hash values in sorted order.
3.  **`bisect` module:** Uses binary search to find the correct position on the ring.

### How Lookup Works
1.  Compute `MD5(key)`.
2.  Use `bisect_right` on `sorted_keys` to find the first hash greater than the key.
3.  If the index is out of bounds, wrap around to index 0.
4.  Retrieve the server name from `self.ring`.

---

## 2. Complexity Analysis

Let $V$ be the number of virtual nodes per server and $N$ be the number of servers. Total entries on the ring $T = V \times N$.

| Operation | Complexity | Explanation |
| :--- | :--- | :--- |
| **Add Node** | $O(V \cdot N)$ | `insort` is $O(T)$ in Python (list insertion is linear). A strict tree structure would be $O(\log T)$. |
| **Get Node** | $O(\log T)$ | Binary search (`bisect`) is logarithmic. |
| **Space** | $O(T)$ | Stores all virtual node hashes. |

*Note: For a pure $O(\log N)$ write performance in Python, one would need an external library like `sortedcontainers`, but this implementation prefers standard libraries for portability.*

---

## 3. Simulation Results

We simulated distributing **10,000 keys** across **5 servers**, and then removing **1 server**.

### Findings
1.  **10 Virtual Nodes:** - The load distribution was uneven (High Standard Deviation).
    - Remapping percentage fluctuates significantly from the ideal 20%.
    
2.  **100 Virtual Nodes:**
    - The load distribution was smooth (Low Standard Deviation).
    - Remapping percentage was consistently close to **20-21%**, which is mathematically ideal (only keys from the failed node moved).

## How to Run
1. Ensure you have Python installed.
2. Run the simulation script:
   ```bash
   python simulation.py
