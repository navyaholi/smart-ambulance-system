
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.allocation import (
    calculate_distance,
    find_nearest_ambulance,
    find_suitable_hospital,
    greedy_ambulance_assignment,
)
from app.data_manager import DataManager
from app.graph import RoadGraph
from app.models import Ambulance, Hospital, Location

app = FastAPI(
    title="Smart Ambulance Route & Hospital Allocation System",
    description=(
        "A computational-thinking based system for "
        "ambulance allocation, route planning and hospital selection."
    ),
    version="1.0.0",
)

# Allow the React frontend on ports 5173 and 5174.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

data_manager = DataManager()


def create_location(name: str) -> Location:
    """Create a location using the sample coordinates."""

    locations = {
        "Area A": (17.385, 78.486),
        "Area B": (17.400, 78.500),
        "Area C": (17.420, 78.510),
        "Hospital A": (17.385, 78.486),
        "Hospital B": (17.400, 78.500),
        "Hospital C": (17.420, 78.510),
        "Junction": (17.390, 78.490),
    }

    latitude, longitude = locations.get(
        name, (17.385, 78.486)
    )

    return Location(
        name=name,
        latitude=latitude,
        longitude=longitude,
    )


def load_ambulances() -> list[Ambulance]:
    """Load ambulance records as model objects."""

    return [
        Ambulance(
            ambulance_id=item["ambulance_id"],
            driver_name=item["driver_name"],
            location=create_location(item["location"]),
            available=item["available"],
        )
        for item in data_manager.get_ambulances()
    ]


def load_hospitals() -> list[Hospital]:
    """Load hospital records as model objects."""

    return [
        Hospital(
            hospital_id=item["hospital_id"],
            name=item["name"],
            location=create_location(item["location"]),
            available_beds=item["available_beds"],
            emergency_capacity=item["emergency_capacity"],
        )
        for item in data_manager.get_hospitals()
    ]


@app.get("/")
def home() -> dict[str, str]:
    """Return basic application information."""

    return {
        "message": "Smart Ambulance System is running",
        "version": "1.0.0",
    }


@app.get("/patients")
def get_patients() -> list[dict]:
    """Return all patient records."""

    return data_manager.get_patients()


@app.get("/ambulances")
def get_ambulances() -> list[dict]:
    """Return all ambulance records."""

    return data_manager.get_ambulances()


@app.get("/hospitals")
def get_hospitals() -> list[dict]:
    """Return all hospital records."""

    return data_manager.get_hospitals()


@app.get("/ambulances/nearest")
def nearest_ambulance(
    latitude: float,
    longitude: float,
) -> dict:
    """Find the nearest available ambulance."""

    emergency_location = Location(
        name="Emergency Location",
        latitude=latitude,
        longitude=longitude,
    )

    ambulance = find_nearest_ambulance(
        load_ambulances(),
        emergency_location,
    )

    if ambulance is None:
        raise HTTPException(
            status_code=404,
            detail="No available ambulance found",
        )

    distance = calculate_distance(
        ambulance.location,
        emergency_location,
    )

    return {
        "ambulance_id": ambulance.ambulance_id,
        "driver_name": ambulance.driver_name,
        "distance": distance,
    }


@app.get("/hospitals/suitable")
def suitable_hospital(
    latitude: float,
    longitude: float,
) -> dict:
    """Find the nearest suitable hospital."""

    emergency_location = Location(
        name="Emergency Location",
        latitude=latitude,
        longitude=longitude,
    )

    hospital = find_suitable_hospital(
        load_hospitals(),
        emergency_location,
    )

    if hospital is None:
        raise HTTPException(
            status_code=404,
            detail="No suitable hospital found",
        )

    distance = calculate_distance(
        hospital.location,
        emergency_location,
    )

    return {
        "hospital_id": hospital.hospital_id,
        "hospital_name": hospital.name,
        "available_beds": hospital.available_beds,
        "emergency_capacity": hospital.emergency_capacity,
        "distance": distance,
    }


@app.post("/allocate")
def allocate_ambulances() -> dict:
    """Assign available ambulances to emergency locations."""

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

    return {
        "assignments": [
            {
                "ambulance_id": ambulance_id,
                "emergency_location": location,
            }
            for ambulance_id, location in assignments
        ]
    }


@app.get("/route")
def shortest_route(
    start: str,
    destination: str,
) -> dict:
    """Find the shortest route using Dijkstra's algorithm."""

    road_map = RoadGraph()

    road_map.add_road("Area A", "Junction", 4)
    road_map.add_road("Junction", "Hospital A", 4)
    road_map.add_road("Area A", "Area B", 6)
    road_map.add_road("Area B", "Hospital B", 5)
    road_map.add_road("Area B", "Area C", 3)
    road_map.add_road("Area C", "Hospital C", 4)
    road_map.add_road("Junction", "Area B", 2)

    distance, path = road_map.shortest_path(
        start,
        destination,
    )

    if not path:
        raise HTTPException(
            status_code=404,
            detail="No route found",
        )

    return {
        "start": start,
        "destination": destination,
        "distance": distance,
        "route": path,
    }
