from app.graph import RoadGraph


def test_shortest_path():

    road_map = RoadGraph()

    road_map.add_road("Hospital", "Junction", 5)
    road_map.add_road("Junction", "Area A", 3)
    road_map.add_road("Junction", "Area B", 4)
    road_map.add_road("Area A", "Area B", 10)

    distance, path = road_map.shortest_path("Hospital", "Area A")

    assert distance == 8

    assert path == ["Hospital", "Junction", "Area A"]


def test_unknown_location():

    road_map = RoadGraph()

    road_map.add_road("Hospital", "Junction", 5)

    distance, path = road_map.shortest_path("Hospital", "Unknown")

    assert distance == float("inf")
    assert path == []


def test_shortest_path_start_equals_destination():

    road_map = RoadGraph()

    road_map.add_location("Hospital")

    distance, path = road_map.shortest_path("Hospital", "Hospital")

    assert distance == 0
    assert path == ["Hospital"]


def test_shortest_path_unreachable():

    road_map = RoadGraph()

    road_map.add_location("Hospital")
    road_map.add_location("Area A")

    distance, path = road_map.shortest_path("Hospital", "Area A")

    assert distance == float("inf")
    assert path == []


def test_shortest_path_with_longer_route():

    road_map = RoadGraph()

    road_map.add_road("Hospital", "A", 2)
    road_map.add_road("A", "B", 3)
    road_map.add_road("Hospital", "B", 10)

    distance, path = road_map.shortest_path("Hospital", "B")

    assert distance == 5

    assert path == ["Hospital", "A", "B"]


def test_dijkstra_skips_outdated_priority_entry():

    road_map = RoadGraph()

    # First, A gets distance 10.
    road_map.add_road("Hospital", "A", 10)

    # Then B gives A a better distance of 4.
    road_map.add_road("Hospital", "B", 2)

    road_map.add_road("B", "A", 2)

    # Make the destination far enough away
    # so the old A=10 queue entry is processed.
    road_map.add_road("A", "Destination", 100)

    distance, path = road_map.shortest_path("Hospital", "Destination")

    assert distance == 104

    assert path == ["Hospital", "B", "A", "Destination"]
