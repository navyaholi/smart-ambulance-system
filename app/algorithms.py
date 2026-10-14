import time
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor
from functools import reduce

# =========================================================
# 1. DYNAMIC PROGRAMMING
# =========================================================


def optimize_emergency_resources(
    emergencies: list[tuple[str, int, int]], capacity: int
) -> tuple[int, list[str]]:

    n = len(emergencies)

    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        emergency_id, resource, priority = emergencies[i - 1]

        for current_capacity in range(capacity + 1):
            dp[i][current_capacity] = dp[i - 1][current_capacity]

            if resource <= current_capacity:
                selected_value = dp[i - 1][current_capacity - resource] + priority

                dp[i][current_capacity] = max(dp[i][current_capacity], selected_value)

    maximum_priority = dp[n][capacity]

    selected_emergencies: list[str] = []

    current_capacity = capacity

    for i in range(n, 0, -1):
        if dp[i][current_capacity] != dp[i - 1][current_capacity]:
            emergency_id, resource, priority = emergencies[i - 1]

            selected_emergencies.append(emergency_id)

            current_capacity -= resource

    selected_emergencies.reverse()

    return maximum_priority, selected_emergencies


# =========================================================
# 2. BACKTRACKING
# =========================================================


def find_all_routes(
    graph: dict[str, list[str]], start: str, destination: str
) -> list[list[str]]:

    all_routes: list[list[str]] = []

    def backtrack(current: str, current_path: list[str]) -> None:

        if current == destination:
            all_routes.append(current_path.copy())

            return

        for neighbour in graph.get(current, []):
            if neighbour not in current_path:
                current_path.append(neighbour)

                backtrack(neighbour, current_path)

                current_path.pop()

    backtrack(start, [start])

    return all_routes


# =========================================================
# 3. BRANCH AND BOUND
# =========================================================


def find_best_emergency_route(
    graph: dict[str, list[tuple[str, float]]], start: str, destination: str
) -> tuple[float, list[str]]:

    best_distance = float("inf")
    best_route: list[str] = []

    def branch_and_bound(
        current: str, current_distance: float, current_route: list[str]
    ) -> None:

        nonlocal best_distance
        nonlocal best_route

        if current == destination:
            if current_distance < best_distance:
                best_distance = current_distance

                best_route = current_route.copy()

            return

        for neighbour, distance in graph.get(current, []):
            if neighbour not in current_route:
                new_distance = current_distance + distance

                if new_distance < best_distance:
                    current_route.append(neighbour)

                    branch_and_bound(neighbour, new_distance, current_route)

                    current_route.pop()

    branch_and_bound(start, 0, [start])

    return best_distance, best_route


# =========================================================
# 4. FUNCTIONAL PROGRAMMING
# =========================================================


def get_emergency_priorities(emergencies: list[tuple[str, int, int]]) -> list[int]:

    priorities = [emergency[2] for emergency in emergencies]

    return priorities


def filter_high_priority_emergencies(
    emergencies: list[tuple[str, int, int]], minimum_priority: int
) -> list[tuple[str, int, int]]:

    high_priority = list(
        filter(lambda emergency: emergency[2] >= minimum_priority, emergencies)
    )

    return high_priority


def calculate_total_priority(emergencies: list[tuple[str, int, int]]) -> int:

    total_priority = reduce(
        lambda total, emergency: total + emergency[2], emergencies, 0
    )

    return total_priority


def create_priority_calculator(multiplier: int) -> Callable[[int], int]:

    def calculate(priority: int) -> int:

        return priority * multiplier

    return calculate


def calculate_average_priority(emergencies: list[tuple[str, int, int]]) -> float:

    if not emergencies:
        return 0.0

    total = calculate_total_priority(emergencies)

    return total / len(emergencies)


# =========================================================
# 5. CONCURRENCY
# =========================================================


def check_hospital_availability(hospital: tuple[str, int, int]) -> tuple[str, bool]:
    """
    Simulate checking hospital availability.

    hospital:
        (hospital_id, available_beds, emergency_capacity)

    Returns:
        (hospital_id, available)
    """

    hospital_id, available_beds, emergency_capacity = hospital

    time.sleep(0.1)

    available = available_beds > 0 and emergency_capacity > 0

    return hospital_id, available


def check_hospitals_concurrently(
    hospitals: list[tuple[str, int, int]],
) -> list[tuple[str, bool]]:
    """
    Check multiple hospitals concurrently using threads.

    Threading is suitable here because the task represents
    I/O-style waiting rather than CPU-heavy computation.
    """

    if not hospitals:
        return []

    with ThreadPoolExecutor(max_workers=len(hospitals)) as executor:
        results = list(executor.map(check_hospital_availability, hospitals))

    return results
