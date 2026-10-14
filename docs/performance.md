# Performance Evaluation

## Benchmark Results

The Smart Ambulance System was tested using a performance benchmark for the main computational techniques.

| Algorithm / Technique | Execution Time |
|---|---:|
| Dijkstra | 0.1571 ms |
| Dynamic Programming | 1.1980 ms |
| Backtracking | 0.0346 ms |
| Concurrent Hospital Check | 106.9052 ms |

## Observations

- Dijkstra completed the tested shortest-path calculation in approximately 0.1571 ms.
- Dynamic programming completed the tested resource optimisation in approximately 1.1980 ms.
- Backtracking completed the tested route exploration in approximately 0.0346 ms.
- Concurrent hospital checking took approximately 106.9052 ms because the benchmark intentionally simulates 0.1 seconds of waiting for each hospital check.

## Complexity

### Dijkstra

With a binary heap:

O((V + E) log V)

### Dynamic Programming

For `n` emergencies and capacity `C`:

O(n × C)

### Backtracking

Worst-case complexity is exponential because multiple possible routes may be explored.

### Branch and Bound

Worst-case complexity can also be exponential, but pruning can reduce the number of explored branches.

## Benchmark Command

The benchmark can be executed from the project root using:

```powershell
python -m performance.benchmark