"""Tests for Content Generation API endpoints"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from backend.src.main import app
from backend.src.models import ContentGenerationRequest, JobCreatedResponse, JobStatusResponse
from backend.src.utils.workflow_utils import set_active_job, clear_active_job, create_job, get_job

client = TestClient(app)


@pytest.fixture
def auth_token():
    """Create a mock auth token for testing"""
    # In real tests, this would be a valid JWT token
    return "mock_jwt_token"


@pytest.fixture
def sample_request():
    """Sample content generation request"""
    return {
        "chapters": ["1", "2"],
        "lessons": ["1", "2"],
        "target_word_count": 800,
        "priority": "normal"
    }


def test_post_content_generate_endpoint(sample_request, auth_token):
    """Contract test for POST /api/content/generate endpoint"""
    headers = {"Authorization": f"Bearer {auth_token}"}
    
    with patch('backend.src.routes.content_generation.set_active_job', return_value=True):
        with patch('backend.src.routes.content_generation.generate_job_id', return_value="test-job-id"):
            response = client.post(
                "/api/content/generate",
                json=sample_request,
                headers=headers
            )
    
    assert response.status_code == 202
    data = response.json()
    assert "job_id" in data
    assert "status" in data
    assert data["status"] == "pending"
    assert "message" in data


def test_get_content_generate_job_status(auth_token):
    """Contract test for GET /api/content/generate/{job_id} endpoint"""
    job_id = "test-job-id"
    headers = {"Authorization": f"Bearer {auth_token}"}
    
    # Create a mock job
    mock_job = {
        "job_id": job_id,
        "status": "in_progress",
        "progress": 50.0,
        "created_at": "2025-12-23T10:00:00Z"
    }
    
    with patch('backend.src.routes.content_generation.get_job', return_value=mock_job):
        response = client.get(
            f"/api/content/generate/{job_id}",
            headers=headers
        )
    
    assert response.status_code == 200
    data = response.json()
    assert data["job_id"] == job_id
    assert "status" in data
    assert "progress" in data


def test_concurrent_request_rejection(sample_request, auth_token):
    """Test concurrent request rejection (HTTP 429)"""
    headers = {"Authorization": f"Bearer {auth_token}"}
    
    # Set an active job to simulate concurrent request
    set_active_job("active-job-id")
    
    try:
        response = client.post(
            "/api/content/generate",
            json=sample_request,
            headers=headers
        )
        
        assert response.status_code == 429
        data = response.json()
        assert "error" in data or "message" in data
    finally:
        clear_active_job()


def test_post_content_generate_validation_error(auth_token):
    """Test POST /api/content/generate with invalid request"""
    headers = {"Authorization": f"Bearer {auth_token}"}
    
    # Invalid request - missing required chapters
    invalid_request = {
        "lessons": ["1", "2"]
    }
    
    response = client.post(
        "/api/content/generate",
        json=invalid_request,
        headers=headers
    )
    
    assert response.status_code == 422  # Validation error


def test_get_content_generate_job_not_found(auth_token):
    """Test GET /api/content/generate/{job_id} with non-existent job"""
    job_id = "non-existent-job-id"
    headers = {"Authorization": f"Bearer {auth_token}"}
    
    with patch('backend.src.routes.content_generation.get_job', return_value=None):
        response = client.get(
            f"/api/content/generate/{job_id}",
            headers=headers
        )
    
    assert response.status_code == 404


def test_cancel_job_endpoint(sample_request, auth_token):
    """Test job cancellation endpoint"""
    headers = {"Authorization": f"Bearer {auth_token}"}
    job_id = "test-job-id"
    
    # Create a job
    mock_job = {
        "job_id": job_id,
        "status": "in_progress",
        "user_id": "test-user"
    }
    
    with patch('backend.src.routes.content_generation.get_job', return_value=mock_job):
        with patch('backend.src.routes.content_generation.update_job', return_value=True):
            with patch('backend.src.routes.content_generation.clear_active_job'):
                response = client.post(
                    f"/api/content/generate/{job_id}/cancel",
                    headers=headers
                )
                
                assert response.status_code == 200
                data = response.json()
                assert data["status"] == "cancelled"


def test_cancel_completed_job_fails(auth_token):
    """Test that cancelling a completed job fails"""
    headers = {"Authorization": f"Bearer {auth_token}"}
    job_id = "completed-job-id"
    
    mock_job = {
        "job_id": job_id,
        "status": "completed",
        "user_id": "test-user"
    }
    
    with patch('backend.src.routes.content_generation.get_job', return_value=mock_job):
        response = client.post(
            f"/api/content/generate/{job_id}/cancel",
            headers=headers
        )
        
        assert response.status_code == 400

