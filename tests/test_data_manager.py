from app.data_manager import DataManager


def test_load_patients():
    manager = DataManager()

    patients = manager.get_patients()

    assert len(patients) == 3
    assert patients[0]["patient_id"] == "P001"


def test_load_ambulances():
    manager = DataManager()

    ambulances = manager.get_ambulances()

    assert len(ambulances) == 3
    assert ambulances[0]["ambulance_id"] == "AMB001"


def test_load_hospitals():
    manager = DataManager()

    hospitals = manager.get_hospitals()

    assert len(hospitals) == 3
    assert hospitals[0]["hospital_id"] == "H001"
