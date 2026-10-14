from app.algorithms import (
    calculate_average_priority,
    calculate_total_priority,
    check_hospital_availability,
    check_hospitals_concurrently,
    create_priority_calculator,
    filter_high_priority_emergencies,
    find_all_routes,
    find_best_emergency_route,
    get_emergency_priorities,
    optimize_emergency_resources,
)

# =========================================================
# 1. DYNAMIC PROGRAMMING
# =========================================================


def test_optimize_emergency_resources():
    emergencies = [
        ("E1", 2, 10),
        ("E2", 3, 15),
        ("E3", 4, 20),
    ]

    maximum_priority, selected = optimize_emergency_resources(emergencies, 5)

    assert maximum_priority == 25
    assert selected == ["E1", "E2"]


def test_optimize_emergency_resources_empty():
    maximum_priority, selected = optimize_emergency_resources([], 5)

    assert maximum_priority == 0
    assert selected == []


def test_optimize_emergency_resources_zero_capacity():
    emergencies = [
        ("E1", 2, 10),
        ("E2", 3, 15),
    ]

    maximum_priority, selected = optimize_emergency_resources(emergencies, 0)

    assert maximum_priority == 0
    assert selected == []


def test_optimize_emergency_resources_single_emergency():
    emergencies = [
        ("E1", 2, 10),
    ]

    maximum_priority, selected = optimize_emergency_resources(emergencies, 2)

    assert maximum_priority == 10
    assert selected == ["E1"]


def test_optimize_emergency_resources_capacity_too_small():
    emergencies = [
        ("E1", 5, 10),
        ("E2", 6, 20),
    ]

    maximum_priority, selected = optimize_emergency_resources(emergencies, 2)

    assert maximum_priority == 0
    assert selected == []


# =========================================================
# 2. BACKTRACKING
# =========================================================


def test_find_all_routes():
    graph = {"A": ["B", "C"], "B": ["D"], "C": ["D"], "D": []}

    routes = find_all_routes(graph, "A", "D")

    assert routes == [["A", "B", "D"], ["A", "C", "D"]]


def test_find_all_routes_start_equals_destination():
    graph = {"A": ["B"], "B": []}

    routes = find_all_routes(graph, "A", "A")

    assert routes == [["A"]]


def test_find_all_routes_no_route():
    graph = {"A": ["B"], "B": [], "C": []}

    routes = find_all_routes(graph, "A", "C")

    assert routes == []


def test_find_all_routes_cycle():
    graph = {"A": ["B"], "B": ["A", "C"], "C": []}

    routes = find_all_routes(graph, "A", "C")

    assert routes == [["A", "B", "C"]]


# =========================================================
# 3. BRANCH AND BOUND
# =========================================================


def test_find_best_emergency_route():
    graph = {"A": [("B", 2), ("C", 5)], "B": [("D", 3)], "C": [("D", 1)], "D": []}

    distance, route = find_best_emergency_route(graph, "A", "D")

    assert distance == 5
    assert route == ["A", "B", "D"]


def test_branch_and_bound_start_equals_destination():
    graph = {"A": [("B", 2)], "B": []}

    distance, route = find_best_emergency_route(graph, "A", "A")

    assert distance == 0
    assert route == ["A"]


def test_branch_and_bound_no_route():
    graph = {"A": [("B", 2)], "B": [], "C": []}

    distance, route = find_best_emergency_route(graph, "A", "C")

    assert distance == float("inf")
    assert route == []


def test_branch_and_bound_unknown_start():
    graph = {"A": [("B", 2)], "B": []}

    distance, route = find_best_emergency_route(graph, "X", "B")

    assert distance == float("inf")
    assert route == []


def test_branch_and_bound_unknown_destination():
    graph = {"A": [("B", 2)], "B": []}

    distance, route = find_best_emergency_route(graph, "A", "X")

    assert distance == float("inf")
    assert route == []


def test_branch_and_bound_prunes_expensive_route():
    graph = {"A": [("B", 1), ("C", 10)], "B": [("D", 1)], "C": [("D", 1)], "D": []}

    distance, route = find_best_emergency_route(graph, "A", "D")

    assert distance == 2
    assert route == ["A", "B", "D"]


def test_branch_and_bound_pruning_condition():
    graph = {"A": [("D", 1), ("B", 1)], "B": [("D", 1)], "D": []}

    distance, route = find_best_emergency_route(graph, "A", "D")

    assert distance == 1
    assert route == ["A", "D"]


# =========================================================
# 4. FUNCTIONAL PROGRAMMING
# =========================================================


def test_get_emergency_priorities():
    emergencies = [
        ("E1", 2, 10),
        ("E2", 3, 20),
        ("E3", 4, 15),
    ]

    result = get_emergency_priorities(emergencies)

    assert result == [10, 20, 15]


def test_filter_high_priority_emergencies():
    emergencies = [
        ("E1", 2, 10),
        ("E2", 3, 20),
        ("E3", 4, 15),
    ]

    result = filter_high_priority_emergencies(emergencies, 15)

    assert result == [("E2", 3, 20), ("E3", 4, 15)]


def test_calculate_total_priority():
    emergencies = [
        ("E1", 2, 10),
        ("E2", 3, 20),
        ("E3", 4, 15),
    ]

    result = calculate_total_priority(emergencies)

    assert result == 45


def test_create_priority_calculator():
    calculator = create_priority_calculator(2)

    assert calculator(10) == 20
    assert calculator(5) == 10


def test_calculate_average_priority():
    emergencies = [
        ("E1", 2, 10),
        ("E2", 3, 20),
        ("E3", 4, 15),
    ]

    result = calculate_average_priority(emergencies)

    assert result == 15


def test_calculate_average_priority_empty():
    result = calculate_average_priority([])

    assert result == 0.0


# =========================================================
# 5. CONCURRENCY
# =========================================================


def test_check_hospital_availability_available():
    hospital = ("H001", 10, 5)

    result = check_hospital_availability(hospital)

    assert result == ("H001", True)


def test_check_hospital_availability_unavailable():
    hospital = ("H002", 0, 5)

    result = check_hospital_availability(hospital)

    assert result == ("H002", False)


def test_check_hospitals_concurrently():
    hospitals = [("H001", 10, 5), ("H002", 0, 5), ("H003", 5, 2)]

    results = check_hospitals_concurrently(hospitals)

    assert results == [("H001", True), ("H002", False), ("H003", True)]
