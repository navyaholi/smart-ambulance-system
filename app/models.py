from dataclasses import dataclass


@dataclass
class Location:
    name: str
    latitude: float
    longitude: float


@dataclass
class Patient:
    patient_id: str
    name: str
    age: int
    emergency_level: int
    location: Location


@dataclass
class Ambulance:
    ambulance_id: str
    driver_name: str
    location: Location
    available: bool = True


@dataclass
class Hospital:
    hospital_id: str
    name: str
    location: Location
    available_beds: int
    emergency_capacity: int


@dataclass
class Emergency:
    emergency_id: str
    patient: Patient
    required_ambulance: bool
    status: str = "Pending"
