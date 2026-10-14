from app.allocation import (
    calculate_distance,
    find_nearest_ambulance,
    find_suitable_hospital,
    greedy_ambulance_assignment,
)
from app.data_manager import DataManager
from app.graph import RoadGraph
from app.main import create_location, load_ambulances, load_hospitals


def display_header(title: str) -> None:
    """Display a section header."""
    print()
    print("=" * 55)
    print(title)
    print("=" * 55)


def show_patients() -> None:
    """Display all patients."""
    data_manager = DataManager()
    patients = data_manager.get_patients()

    display_header("PATIENT INFORMATION")

    for patient in patients:
        print(
            f"{patient['patient_id']} | "
            f"{patient['name']} | "
            f"Age: {patient['age']} | "
            f"Emergency Level: {patient['emergency_level']}"
        )


def show_ambulances() -> None:
    """Display ambulance information."""
    ambulances = load_ambulances()

    display_header("AMBULANCE INFORMATION")

    for ambulance in ambulances:
        status = "Available" if ambulance.available else "Busy"

        print(
            f"{ambulance.ambulance_id} | "
            f"Driver: {ambulance.driver_name} | "
            f"Location: {ambulance.location.name} | "
            f"Status: {status}"
        )


def show_hospitals() -> None:
    """Display hospital information."""
    hospitals = load_hospitals()

    display_header("HOSPITAL INFORMATION")

    for hospital in hospitals:
        print(
            f"{hospital.hospital_id} | "
            f"{hospital.name} | "
            f"Beds: {hospital.available_beds} | "
            f"Emergency Capacity: {hospital.emergency_capacity}"
        )


def demonstrate_nearest_ambulance() -> None:
    """Demonstrate nearest ambulance selection."""
    emergency_location = create_location("Area A")
    ambulances = load_ambulances()

    ambulance = find_nearest_ambulance(
        ambulances,
        emergency_location,
    )

    display_header("NEAREST AVAILABLE AMBULANCE")

    if ambulance is None:
        print("No available ambulance found.")
        return

    distance = calculate_distance(
        ambulance.location,
        emergency_location,
    )

    print(f"Ambulance : {ambulance.ambulance_id}")
    print(f"Driver    : {ambulance.driver_name}")
    print(f"Distance  : {distance:.4f}")


def demonstrate_hospital_selection() -> None:
    """Demonstrate suitable hospital selection."""
    emergency_location = create_location("Area A")
    hospitals = load_hospitals()

    hospital = find_suitable_hospital(
        hospitals,
        emergency_location,
    )

    display_header("SUITABLE HOSPITAL")

    if hospital is None:
        print("No suitable hospital found.")
        return

    distance = calculate_distance(
        hospital.location,
        emergency_location,
    )

    print(f"Hospital           : {hospital.name}")
    print(f"Available Beds     : {hospital.available_beds}")
    print(f"Emergency Capacity : {hospital.emergency_capacity}")
    print(f"Distance           : {distance:.4f}")


def demonstrate_greedy_allocation() -> None:
    """Demonstrate greedy ambulance allocation."""
    ambulances = load_ambulances()

    emergency_locations = [
        create_location("Area A"),
        create_location("Area B"),
        create_location("Area C"),
    ]

    assignments = greedy_ambulance_assignment(
        ambulances,
        emergency_locations,
    )

    display_header("GREEDY AMBULANCE ALLOCATION")

    if not assignments:
        print("No ambulance assignments available.")
        return

    for ambulance_id, location in assignments:
        print(
            f"Ambulance {ambulance_id} -> {location}"
        )


def demonstrate_shortest_route() -> None:
    """Demonstrate Dijkstra shortest route."""
    road_map = RoadGraph()

    road_map.add_road("Area A", "Junction", 4)
    road_map.add_road("Junction", "Hospital A", 4)
    road_map.add_road("Area A", "Area B", 6)
    road_map.add_road("Area B", "Hospital B", 5)
    road_map.add_road("Area B", "Area C", 3)
    road_map.add_road("Area C", "Hospital C", 4)
    road_map.add_road("Junction", "Area B", 2)

    distance, path = road_map.shortest_path(
        "Area A",
        "Hospital A",
    )

    display_header("SHORTEST ROUTE - DIJKSTRA")

    print(f"Route    : {' -> '.join(path)}")
    print(f"Distance : {distance}")


def main() -> None:
    """Run the complete command-line demonstration."""

    print()
    print("=" * 55)
    print("       SMART AMBULANCE SYSTEM")
    print("=" * 55)

    show_patients()
    show_ambulances()
    show_hospitals()

    demonstrate_nearest_ambulance()
    demonstrate_hospital_selection()
    demonstrate_greedy_allocation()
    demonstrate_shortest_route()

    print()
    print("=" * 55)
    print("       DEMONSTRATION COMPLETED")
    print("=" * 55)


if __name__ == "__main__":
    main()