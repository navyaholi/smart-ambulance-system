from app.models import Ambulance, Emergency, Hospital, Location, Patient


def test_location():

    location = Location(name="Area A", latitude=17.385, longitude=78.486)

    assert location.name == "Area A"
    assert location.latitude == 17.385
    assert location.longitude == 78.486


def test_patient():

    location = Location(name="Area A", latitude=17.385, longitude=78.486)

    patient = Patient(
        patient_id="P001",
        name="Test Patient",
        age=45,
        emergency_level=5,
        location=location,
    )

    assert patient.patient_id == "P001"
    assert patient.name == "Test Patient"
    assert patient.age == 45
    assert patient.emergency_level == 5
    assert patient.location.name == "Area A"


def test_ambulance():

    location = Location(name="Area A", latitude=17.385, longitude=78.486)

    ambulance = Ambulance(ambulance_id="AMB001", driver_name="Ravi", location=location)

    assert ambulance.ambulance_id == "AMB001"
    assert ambulance.driver_name == "Ravi"
    assert ambulance.available is True


def test_hospital():

    location = Location(name="Hospital A", latitude=17.400, longitude=78.500)

    hospital = Hospital(
        hospital_id="H001",
        name="City General Hospital",
        location=location,
        available_beds=20,
        emergency_capacity=10,
    )

    assert hospital.hospital_id == "H001"
    assert hospital.name == "City General Hospital"
    assert hospital.available_beds == 20
    assert hospital.emergency_capacity == 10


def test_emergency():

    location = Location(name="Area A", latitude=17.385, longitude=78.486)

    patient = Patient(
        patient_id="P001",
        name="Test Patient",
        age=45,
        emergency_level=5,
        location=location,
    )

    emergency = Emergency(emergency_id="E001", patient=patient, required_ambulance=True)

    assert emergency.emergency_id == "E001"
    assert emergency.patient.patient_id == "P001"
    assert emergency.required_ambulance is True
    assert emergency.status == "Pending"
