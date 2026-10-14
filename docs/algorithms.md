# Algorithms and Data Structures

## 1. Dijkstra's Algorithm

Dijkstra's algorithm is used to find the shortest path between locations in the road network.

### Input

- Starting location
- Destination location
- Road graph

### Output

- Shortest distance
- Shortest route

## 2. Greedy Algorithm

The greedy approach assigns the nearest available ambulance to an emergency location.

At every step, the currently nearest available ambulance is selected.

## 3. Dynamic Programming

Dynamic Programming is used for emergency resource optimization.

The system evaluates possible combinations of emergency cases under a limited resource capacity.

## 4. Backtracking

Backtracking is used to find possible routes between locations.

The algorithm explores a route and backtracks when the route cannot continue.

## 5. Branch and Bound

Branch and Bound searches for a suitable route while eliminating routes that cannot produce a better solution.

## Data Structures

The project uses:

- Lists
- Dictionaries
- Tuples
- Priority Queues
- Graphs
- Dataclasses

## Complexity

### Dijkstra

Using a priority queue, the shortest-path implementation is approximately:

O((V + E) log V)

where:

- V = number of locations
- E = number of roads

### Dynamic Programming

The resource optimization algorithm uses:

O(n × C)

where:

- n = number of emergencies
- C = resource capacity.