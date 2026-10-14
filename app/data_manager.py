import json
from pathlib import Path
from typing import Any


class DataManager:
    """Handles reading project data from JSON files."""

    def __init__(self, data_directory: str = "data") -> None:
        self.data_directory = Path(data_directory)

    def load_json(self, filename: str) -> list[dict[str, Any]]:
        """Load a JSON file from the data directory."""

        file_path = self.data_directory / filename

        with file_path.open("r", encoding="utf-8") as file:
            return json.load(file)

    def get_patients(self) -> list[dict[str, Any]]:
        """Return all patients."""
        return self.load_json("patients.json")

    def get_ambulances(self) -> list[dict[str, Any]]:
        """Return all ambulances."""
        return self.load_json("ambulances.json")

    def get_hospitals(self) -> list[dict[str, Any]]:
        """Return all hospitals."""
        return self.load_json("hospitals.json")
