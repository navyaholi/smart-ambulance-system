import time

from app.algorithms import (
    check_hospitals_concurrently,
    find_all_routes,
    optimize_emergency_resources,
)
from app.graph import RoadGraph


def benchmark_dijkstra() -> None:
    graph = RoadGraph()

    for i in range(100):
        graph.add_road(
            f"Location{i}",
            f"Location{i + 1}",
            1,
        )

    start_time = time.perf_counter()

    graph.shortest_path(
        "Location0",
        "Location100",
    )

    end_time = time.perf_counter()

    print(
        f"Dijkstra: {(end_time - start_time) * 1000:.4f} ms"
    )


def benchmark_dynamic_programming() -> None:
    emergencies = [
        (f"E{i}", i % 10 + 1, i % 20 + 1)
        for i in range(50)
    ]

    start_time = time.perf_counter()

    optimize_emergency_resources(
        emergencies,
        100,
    )

    end_time = time.perf_counter()

    print(
        f"Dynamic Programming: "
        f"{(end_time - start_time) * 1000:.4f} ms"
    )


def benchmark_backtracking() -> None:
    graph = {
        "A": ["B", "C"],
        "B": ["A", "D", "E"],
        "C": ["A", "D"],
        "D": ["B", "C", "E"],
        "E": ["B", "D"],
    }

    start_time = time.perf_counter()

    find_all_routes(
        graph,
        "A",
        "E",
    )

    end_time = time.perf_counter()

    print(
        f"Backtracking: "
        f"{(end_time - start_time) * 1000:.4f} ms"
    )


def benchmark_concurrency() -> None:
    hospitals = [
        (f"H{i}", 10, 5)
        for i in range(10)
    ]

    start_time = time.perf_counter()

    check_hospitals_concurrently(hospitals)

    end_time = time.perf_counter()

    print(
        f"Concurrent Hospital Check: "
        f"{(end_time - start_time) * 1000:.4f} ms"
    )


if __name__ == "__main__":
    print("Smart Ambulance System - Performance Benchmark")
    print("-" * 55)

    benchmark_dijkstra()
    benchmark_dynamic_programming()
    benchmark_backtracking()
    benchmark_concurrency()

    print("-" * 55)
    print("Benchmark completed.")