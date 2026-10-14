import heapq

from app.models import Ambulance, Emergency, Hospital, Location

# ============================================================
# 1. EMERGENCY PRIORITY QUEUE
# ============================================================


class EmergencyQueue:
    """Priority queue for emergency cases."""

    def __init__(self) -> None:
        self._queue: list[tuple[int, int, Emergency]] = []
        self._counter = 0

    def add_emergency(self, emergency: Emergency) -> None:
        """Add an emergency to the priority queue."""

        # Higher emergency level gets higher priority.
        # heapq is a min-heap, so we use negative values.
        priority = -emergency.patient.emergency_level

        heapq.heappush(self._queue, (priority, self._counter, emergency))

        self._counter += 1

    def get_next_emergency(self) -> Emergency | None:
        """Return the highest-priority emergency."""

        if not self._queue:
            return None

        _, _, emergency = heapq.heappop(self._queue)

        return emergency

    def is_empty(self) -> bool:
        """Check whether the queue is empty."""

        return len(self._queue) == 0

    def size(self) -> int:
        """Return the number of emergencies."""

        return len(self._queue)


# ============================================================
# 2. DISTANCE CALCULATION
# ============================================================


def calculate_distance(location1: Location, location2: Location) -> float:
    """Calculate simple mathematical distance between two locations."""

    latitude_difference = location1.latitude - location2.latitude

    longitude_difference = location1.longitude - location2.longitude

    distance = (latitude_difference**2 + longitude_difference**2) ** 0.5

    return distance


# ============================================================
# 3. FIND NEAREST AVAILABLE AMBULANCE
# ============================================================


def find_nearest_ambulance(
    ambulances: list[Ambulance], emergency_location: Location
) -> Ambulance | None:
    """Find the nearest available ambulance."""

    available_ambulances = [
        ambulance for ambulance in ambulances if ambulance.available
    ]

    if not available_ambulances:
        return None

    nearest = min(
        available_ambulances,
        key=lambda ambulance: calculate_distance(
            ambulance.location, emergency_location
        ),
    )

    return nearest


# ============================================================
# 4. FIND SUITABLE HOSPITAL
# ============================================================


def find_suitable_hospital(
    hospitals: list[Hospital], emergency_location: Location
) -> Hospital | None:
    """
    Find the nearest hospital that has:
    - Available beds
    - Emergency capacity
    """

    suitable_hospitals = [
        hospital
        for hospital in hospitals
        if hospital.available_beds > 0 and hospital.emergency_capacity > 0
    ]

    if not suitable_hospitals:
        return None

    nearest = min(
        suitable_hospitals,
        key=lambda hospital: calculate_distance(hospital.location, emergency_location),
    )

    return nearest


# ============================================================
# 5. GREEDY AMBULANCE ASSIGNMENT
# ============================================================


def greedy_ambulance_assignment(
    ambulances: list[Ambulance], emergency_locations: list[Location]
) -> list[tuple[str, str]]:
    """
    Greedy ambulance assignment.

    For each emergency location:
    1. Look at currently available ambulances.
    2. Find the nearest ambulance.
    3. Assign that ambulance.
    4. Remove it from the available list.

    Returns:
        List of tuples containing:
        (ambulance_id, emergency_location)
    """

    available_ambulances = [
        ambulance for ambulance in ambulances if ambulance.available
    ]

    assignments: list[tuple[str, str]] = []

    for emergency_location in emergency_locations:
        # Stop if there are no ambulances left.
        if not available_ambulances:
            break

        # Greedy choice:
        # Select the nearest available ambulance.
        nearest = min(
            available_ambulances,
            key=lambda ambulance: calculate_distance(
                ambulance.location, emergency_location
            ),
        )

        assignments.append((nearest.ambulance_id, emergency_location.name))

        # Ambulance is now assigned,
        # so remove it from available ambulances.
        available_ambulances.remove(nearest)

    return assignments
