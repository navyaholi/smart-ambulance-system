from app.allocation import (
    EmergencyQueue,
    calculate_distance,
    find_nearest_ambulance,
    find_suitable_hospital,
    greedy_ambulance_assignment,
)
from app.models import Ambulance, Emergency, Hospital, Location, Patient

# =========================================================
# HELPER
# =========================================================


def create_emergency(emergency_id: str, level: int) -> Emergency:

    location = Location(name="Area A", latitude=17.385, longitude=78.486)

    patient = Patient(
        patient_id=f"P{emergency_id}",
        name="Test Patient",
        age=30,
        emergency_level=level,
        location=location,
    )

    return Emergency(
        emergency_id=emergency_id, patient=patient, required_ambulance=True
    )


# =========================================================
# EMERGENCY QUEUE
# =========================================================


def test_emergency_priority():

    queue = EmergencyQueue()

    queue.add_emergency(create_emergency("001", 2))

    queue.add_emergency(create_emergency("002", 5))

    queue.add_emergency(create_emergency("003", 3))

    assert queue.size() == 3
    assert queue.is_empty() is False

    first = queue.get_next_emergency()
    second = queue.get_next_emergency()
    third = queue.get_next_emergency()

    assert first.patient.emergency_level == 5
    assert second.patient.emergency_level == 3
    assert third.patient.emergency_level == 2

    assert queue.is_empty() is True


def test_empty_emergency_queue():

    queue = EmergencyQueue()

    assert queue.is_empty() is True
    assert queue.size() == 0
    assert queue.get_next_emergency() is None


# =========================================================
# DISTANCE
# =========================================================


def test_calculate_distance():

    location1 = Location(name="Area A", latitude=17.385, longitude=78.486)

    location2 = Location(name="Area B", latitude=17.400, longitude=78.500)

    distance = calculate_distance(location1, location2)

    assert distance > 0


def test_same_location_distance():

    location = Location(name="Area A", latitude=17.385, longitude=78.486)

    assert calculate_distance(location, location) == 0


# =========================================================
# NEAREST AMBULANCE
# =========================================================


def test_find_nearest_ambulance():

    ambulance1 = Ambulance(
        ambulance_id="AMB001",
        driver_name="Ravi",
        location=Location(name="Area A", latitude=17.385, longitude=78.486),
        available=True,
    )

    ambulance2 = Ambulance(
        ambulance_id="AMB002",
        driver_name="Kiran",
        location=Location(name="Area B", latitude=17.400, longitude=78.500),
        available=True,
    )

    emergency_location = Location(name="Emergency", latitude=17.386, longitude=78.487)

    nearest = find_nearest_ambulance([ambulance1, ambulance2], emergency_location)

    assert nearest is not None
    assert nearest.ambulance_id == "AMB001"


def test_ignore_unavailable_ambulance():

    ambulance1 = Ambulance(
        ambulance_id="AMB001",
        driver_name="Ravi",
        location=Location(name="Area A", latitude=17.385, longitude=78.486),
        available=False,
    )

    ambulance2 = Ambulance(
        ambulance_id="AMB002",
        driver_name="Kiran",
        location=Location(name="Area B", latitude=17.400, longitude=78.500),
        available=True,
    )

    emergency_location = Location(name="Emergency", latitude=17.386, longitude=78.487)

    nearest = find_nearest_ambulance([ambulance1, ambulance2], emergency_location)

    assert nearest is not None
    assert nearest.ambulance_id == "AMB002"


def test_no_available_ambulance():

    ambulance = Ambulance(
        ambulance_id="AMB001",
        driver_name="Ravi",
        location=Location(name="Area A", latitude=17.385, longitude=78.486),
        available=False,
    )

    emergency_location = Location(name="Emergency", latitude=17.386, longitude=78.487)

    assert find_nearest_ambulance([ambulance], emergency_location) is None


# =========================================================
# HOSPITAL
# =========================================================


def test_find_suitable_hospital():

    hospital1 = Hospital(
        hospital_id="H001",
        name="City General Hospital",
        location=Location(name="Hospital A", latitude=17.385, longitude=78.486),
        available_beds=20,
        emergency_capacity=10,
    )

    hospital2 = Hospital(
        hospital_id="H002",
        name="Apollo Emergency Center",
        location=Location(name="Hospital B", latitude=17.400, longitude=78.500),
        available_beds=15,
        emergency_capacity=8,
    )

    emergency_location = Location(name="Emergency", latitude=17.386, longitude=78.487)

    selected = find_suitable_hospital([hospital1, hospital2], emergency_location)

    assert selected is not None
    assert selected.hospital_id == "H001"


def test_ignore_full_hospital():

    full_hospital = Hospital(
        hospital_id="H001",
        name="City General Hospital",
        location=Location(name="Hospital A", latitude=17.385, longitude=78.486),
        available_beds=0,
        emergency_capacity=0,
    )

    available_hospital = Hospital(
        hospital_id="H002",
        name="Apollo Emergency Center",
        location=Location(name="Hospital B", latitude=17.400, longitude=78.500),
        available_beds=15,
        emergency_capacity=8,
    )

    emergency_location = Location(name="Emergency", latitude=17.386, longitude=78.487)

    selected = find_suitable_hospital(
        [full_hospital, available_hospital], emergency_location
    )

    assert selected is not None
    assert selected.hospital_id == "H002"


def test_no_hospital_available():

    hospital = Hospital(
        hospital_id="H001",
        name="City General Hospital",
        location=Location(name="Hospital A", latitude=17.385, longitude=78.486),
        available_beds=0,
        emergency_capacity=0,
    )

    emergency_location = Location(name="Emergency", latitude=17.386, longitude=78.487)

    assert find_suitable_hospital([hospital], emergency_location) is None


# =========================================================
# GREEDY AMBULANCE ASSIGNMENT
# =========================================================


def test_greedy_ambulance_assignment():

    ambulance1 = Ambulance(
        ambulance_id="AMB001",
        driver_name="Ravi",
        location=Location(name="Area A", latitude=17.385, longitude=78.486),
        available=True,
    )

    ambulance2 = Ambulance(
        ambulance_id="AMB002",
        driver_name="Kiran",
        location=Location(name="Area B", latitude=17.400, longitude=78.500),
        available=True,
    )

    emergencies = [
        Location(name="Emergency A", latitude=17.386, longitude=78.487),
        Location(name="Emergency B", latitude=17.401, longitude=78.501),
    ]

    assignments = greedy_ambulance_assignment([ambulance1, ambulance2], emergencies)

    assert len(assignments) == 2

    assert assignments[0] == ("AMB001", "Emergency A")

    assert assignments[1] == ("AMB002", "Emergency B")


def test_greedy_assignment_no_ambulances():

    emergency = Location(name="Emergency A", latitude=17.386, longitude=78.487)

    assignments = greedy_ambulance_assignment([], [emergency])

    assert assignments == []


def test_more_emergencies_than_ambulances():

    ambulance = Ambulance(
        ambulance_id="AMB001",
        driver_name="Ravi",
        location=Location(name="Area A", latitude=17.385, longitude=78.486),
        available=True,
    )

    emergencies = [
        Location(name="Emergency A", latitude=17.386, longitude=78.487),
        Location(name="Emergency B", latitude=17.400, longitude=78.500),
    ]

    assignments = greedy_ambulance_assignment([ambulance], emergencies)

    assert len(assignments) == 1
    assert assignments[0][0] == "AMB001"
