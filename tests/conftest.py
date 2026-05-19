"""Pytest configuration and shared fixtures for FastAPI tests."""
import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    """Provide a TestClient for making HTTP requests to the FastAPI app."""
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset activities to a known state before each test."""
    # Store original activities
    original_activities = {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        },
        "Basketball Team": {
            "description": "Team basketball practice and intramural games",
            "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 18,
            "participants": ["david@mergington.edu", "sarah@mergington.edu"]
        },
        "Swimming Club": {
            "description": "Learn swim techniques and participate in local meets",
            "schedule": "Mondays and Wednesdays, 3:00 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["nina@mergington.edu", "jack@mergington.edu"]
        },
        "Art Studio": {
            "description": "Explore drawing, painting, and mixed media art",
            "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 15,
            "participants": ["lily@mergington.edu", "jason@mergington.edu"]
        },
        "Drama Club": {
            "description": "Acting workshops and stage productions for students",
            "schedule": "Fridays, 4:00 PM - 6:00 PM",
            "max_participants": 25,
            "participants": ["emma@mergington.edu", "alex@mergington.edu"]
        },
        "Math League": {
            "description": "Competitive math problem solving and team contests",
            "schedule": "Tuesdays, 3:30 PM - 5:00 PM",
            "max_participants": 16,
            "participants": ["lucas@mergington.edu", "mia@mergington.edu"]
        },
        "Science Club": {
            "description": "Hands-on science experiments and research projects",
            "schedule": "Thursdays, 3:30 PM - 5:00 PM",
            "max_participants": 18,
            "participants": ["sophia@mergington.edu", "ethan@mergington.edu"]
        }
    }
    
    # Clear and reset activities
    activities.clear()
    activities.update(original_activities)
    
    yield
    
    # Cleanup after test
    activities.clear()
    activities.update(original_activities)
