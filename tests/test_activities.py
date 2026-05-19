"""Tests for FastAPI activity management endpoints."""
import pytest


class TestGetActivities:
    """Tests for GET /activities endpoint."""

    def test_get_activities_returns_all_activities(self, client):
        """Test that GET /activities returns all available activities."""
        response = client.get("/activities")
        assert response.status_code == 200
        activities = response.json()
        assert len(activities) == 9
        assert "Chess Club" in activities
        assert "Programming Class" in activities
        assert "Gym Class" in activities

    def test_get_activities_returns_correct_structure(self, client):
        """Test that GET /activities returns activities with correct data structure."""
        response = client.get("/activities")
        assert response.status_code == 200
        activities = response.json()
        
        # Check Chess Club structure
        chess_club = activities["Chess Club"]
        assert "description" in chess_club
        assert "schedule" in chess_club
        assert "max_participants" in chess_club
        assert "participants" in chess_club
        assert isinstance(chess_club["participants"], list)
        assert "michael@mergington.edu" in chess_club["participants"]


class TestSignupForActivity:
    """Tests for POST /activities/{activity_name}/signup endpoint."""

    def test_signup_success(self, client):
        """Test successful signup for an activity."""
        response = client.post(
            "/activities/Chess%20Club/signup?email=newstudent@mergington.edu",
            json={}
        )
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "newstudent@mergington.edu" in data["message"]
        
        # Verify participant was added
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert "newstudent@mergington.edu" in activities["Chess Club"]["participants"]

    def test_signup_already_registered(self, client):
        """Test that signup fails if student is already registered."""
        response = client.post(
            "/activities/Chess%20Club/signup?email=michael@mergington.edu",
            json={}
        )
        assert response.status_code == 400
        data = response.json()
        assert "already signed up" in data["detail"]

    def test_signup_activity_not_found(self, client):
        """Test that signup returns 404 for non-existent activity."""
        response = client.post(
            "/activities/Nonexistent%20Activity/signup?email=student@mergington.edu",
            json={}
        )
        assert response.status_code == 404
        data = response.json()
        assert "not found" in data["detail"]

    def test_signup_multiple_students(self, client):
        """Test that multiple different students can sign up for the same activity."""
        # Sign up first student
        response1 = client.post(
            "/activities/Programming%20Class/signup?email=student1@mergington.edu",
            json={}
        )
        assert response1.status_code == 200
        
        # Sign up second student
        response2 = client.post(
            "/activities/Programming%20Class/signup?email=student2@mergington.edu",
            json={}
        )
        assert response2.status_code == 200
        
        # Verify both are in participants
        activities_response = client.get("/activities")
        activities = activities_response.json()
        participants = activities["Programming Class"]["participants"]
        assert "student1@mergington.edu" in participants
        assert "student2@mergington.edu" in participants


class TestUnregisterFromActivity:
    """Tests for DELETE /activities/{activity_name}/unregister endpoint."""

    def test_unregister_success(self, client):
        """Test successful unregister from an activity."""
        response = client.delete(
            "/activities/Chess%20Club/unregister?email=michael@mergington.edu"
        )
        assert response.status_code == 200
        data = response.json()
        assert "Unregistered" in data["message"]
        
        # Verify participant was removed
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert "michael@mergington.edu" not in activities["Chess Club"]["participants"]

    def test_unregister_not_registered(self, client):
        """Test that unregister fails if student is not registered."""
        response = client.delete(
            "/activities/Chess%20Club/unregister?email=notregistered@mergington.edu"
        )
        assert response.status_code == 400
        data = response.json()
        assert "not signed up" in data["detail"]

    def test_unregister_activity_not_found(self, client):
        """Test that unregister returns 404 for non-existent activity."""
        response = client.delete(
            "/activities/Nonexistent%20Activity/unregister?email=student@mergington.edu"
        )
        assert response.status_code == 404
        data = response.json()
        assert "not found" in data["detail"]

    def test_unregister_all_participants(self, client):
        """Test unregistering all participants from an activity."""
        # Get initial participants
        activities_response = client.get("/activities")
        initial_participants = activities_response.json()["Chess Club"]["participants"].copy()
        
        # Unregister each participant
        for participant in initial_participants:
            response = client.delete(
                f"/activities/Chess%20Club/unregister?email={participant}"
            )
            assert response.status_code == 200
        
        # Verify all removed
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert len(activities["Chess Club"]["participants"]) == 0


class TestWorkflows:
    """Integration tests for multi-step workflows."""

    def test_signup_then_unregister_workflow(self, client):
        """Test end-to-end workflow: signup then unregister."""
        email = "workflow@mergington.edu"
        activity = "Basketball%20Team"
        
        # Initial check: student not registered
        response = client.get("/activities")
        activities = response.json()
        assert email not in activities["Basketball Team"]["participants"]
        
        # Step 1: Sign up
        signup_response = client.post(
            f"/activities/{activity}/signup?email={email}",
            json={}
        )
        assert signup_response.status_code == 200
        
        # Verify signup succeeded
        response = client.get("/activities")
        activities = response.json()
        assert email in activities["Basketball Team"]["participants"]
        
        # Step 2: Unregister
        unregister_response = client.delete(
            f"/activities/{activity}/unregister?email={email}"
        )
        assert unregister_response.status_code == 200
        
        # Verify unregister succeeded
        response = client.get("/activities")
        activities = response.json()
        assert email not in activities["Basketball Team"]["participants"]
