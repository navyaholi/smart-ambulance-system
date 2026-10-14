import heapq


class RoadGraph:
    def __init__(self) -> None:
        self.graph: dict[str, list[tuple[str, float]]] = {}

    def add_location(self, location: str) -> None:
        """Add a location to the road network."""
        if location not in self.graph:
            self.graph[location] = []

    def add_road(self, location1: str, location2: str, distance: float) -> None:
        """Add a two-way road between two locations."""
        self.add_location(location1)
        self.add_location(location2)

        self.graph[location1].append((location2, distance))
        self.graph[location2].append((location1, distance))

    def shortest_path(self, start: str, destination: str) -> tuple[float, list[str]]:
        """Find the shortest route using Dijkstra's algorithm."""

        if start not in self.graph or destination not in self.graph:
            return float("inf"), []

        distances: dict[str, float] = {
            location: float("inf") for location in self.graph
        }

        previous: dict[str, str | None] = {location: None for location in self.graph}

        distances[start] = 0

        priority_queue: list[tuple[float, str]] = [(0, start)]

        while priority_queue:
            current_distance, current_location = heapq.heappop(priority_queue)

            if current_distance > distances[current_location]:
                continue

            if current_location == destination:
                break

            for neighbour, road_distance in self.graph[current_location]:
                new_distance = current_distance + road_distance

                if new_distance < distances[neighbour]:
                    distances[neighbour] = new_distance
                    previous[neighbour] = current_location

                    heapq.heappush(priority_queue, (new_distance, neighbour))

        if distances[destination] == float("inf"):
            return float("inf"), []

        path: list[str] = []
        current: str | None = destination

        while current is not None:
            path.append(current)
            current = previous[current]

        path.reverse()

        return distances[destination], path
