# Smart Ambulance Route & Hospital Allocation System

## 1. Project Overview

The Smart Ambulance Route & Hospital Allocation System is a Python-based system designed to support emergency ambulance management.

The system helps to:

- Prioritize emergency cases.
- Find suitable available ambulances.
- Find suitable hospitals.
- Calculate shortest ambulance routes.
- Allocate ambulances using a greedy approach.
- Optimize emergency resources using Dynamic Programming.
- Explore possible routes using Backtracking.
- Find suitable routes using Branch and Bound.
- Check hospital availability concurrently.
- Test the system using automated unit tests.

---

## 2. Problem Statement

During emergency situations, ambulance services need to make quick decisions.

The system must consider:

- Emergency priority.
- Ambulance availability.
- Ambulance location.
- Hospital availability.
- Available hospital beds.
- Emergency capacity.
- Road distances.

The goal is to provide an algorithmic solution that helps select ambulances, hospitals, and routes efficiently.

---

## 3. Technologies Used

- Python
- FastAPI
- Pytest
- Hypothesis
- MyPy
- Ruff
- JSON
- Git
- GitHub Actions
- Docker

---

## 4. Project Structure

```text
Smart_Ambulance_System/
│
├── .github/
│   └── workflows/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   ├── data_manager.py
│   ├── graph.py
│   ├── algorithms.py
│   ├── allocation.py
│   └── untils.py
│
├── data/
│   ├── patients.json
│   ├── ambulances.json
│   └── hospitals.json
│
├── docs/
│
├── tests/
│
├── venv/
│
├── .gitignore
├── requirements.txt
├── README.md
└── Dockerfile