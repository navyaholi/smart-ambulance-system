from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_home():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["message"] == "Smart Ambulance System is running"


def test_get_patients():
    response = client.get("/patients")

    assert response.status_code == 200
    assert len(response.json()) == 3


def test_get_ambulances():
    response = client.get("/ambulances")

    assert response.status_code == 200
    assert len(response.json()) == 3


def test_get_hospitals():
    response = client.get("/hospitals")

    assert response.status_code == 200
    assert len(response.json()) == 3


def test_nearest_ambulance():
    response = client.get(
        "/ambulances/nearest",
        params={
            "latitude": 17.386,
            "longitude": 78.487,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "ambulance_id" in data
    assert "driver_name" in data
    assert "distance" in data


def test_suitable_hospital():
    response = client.get(
        "/hospitals/suitable",
        params={
            "latitude": 17.386,
            "longitude": 78.487,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "hospital_id" in data
    assert "hospital_name" in data
    assert "available_beds" in data


def test_allocate_ambulances():
    response = client.post("/allocate")

    assert response.status_code == 200

    data = response.json()

    assert "assignments" in data
    assert len(data["assignments"]) > 0


def test_shortest_route():
    response = client.get(
        "/route",
        params={
            "start": "Area A",
            "destination": "Hospital A",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["start"] == "Area A"
    assert data["destination"] == "Hospital A"
    assert data["distance"] >= 0
    assert len(data["route"]) > 0


def test_route_not_found():
    response = client.get(
        "/route",
        params={
            "start": "Unknown",
            "destination": "Hospital A",
        },
    )

    assert response.status_code == 404