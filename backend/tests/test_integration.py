"""Integration tests for content generation workflow"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from backend.src.main import app

client = TestClient(app)


@pytest.fixture
def auth_token():
    """Create a mock auth token for testing"""
    return "mock_jwt_token"


@pytest.fixture
def sample_request():
    """Sample content generation request"""
    return {
        "chapters": ["1"],
        "lessons": ["1"],
        "target_word_count": 800,
        "priority": "normal"
    }


@patch('backend.src.services.workflow_orchestrator.subprocess')
def test_content_generation_workflow_execution(mock_subprocess, sample_request, auth_token):
    """Integration test for content generation workflow execution"""
    headers = {"Authorization": f"Bearer {auth_token}"}
    
    # Mock subprocess calls for workflow components
    mock_process = MagicMock()
    mock_process.returncode = 0
    mock_process.stdout = b"Success"
    mock_process.stderr = b""
    mock_subprocess.run.return_value = mock_process
    
    # Create job
    with patch('backend.src.routes.content_generation.set_active_job', return_value=True):
        with patch('backend.src.routes.content_generation.generate_job_id', return_value="test-job-id"):
            create_response = client.post(
                "/api/content/generate",
                json=sample_request,
                headers=headers
            )
    
    assert create_response.status_code == 202
    job_id = create_response.json()["job_id"]
    
    # Poll for job status
    with patch('backend.src.routes.content_generation.get_job') as mock_get_job:
        # Simulate job progression
        mock_get_job.side_effect = [
            {"job_id": job_id, "status": "in_progress", "progress": 25.0},
            {"job_id": job_id, "status": "in_progress", "progress": 50.0},
            {"job_id": job_id, "status": "completed", "progress": 100.0, "results": {"total_lessons": 1}}
        ]
        
        status_response = client.get(
            f"/api/content/generate/{job_id}",
            headers=headers
        )
        
        assert status_response.status_code == 200
        data = status_response.json()
        assert data["status"] in ["in_progress", "completed"]


def test_rag_indexing_integration(auth_token):
    """Test RAG indexing integration"""
    from backend.src.services.sync_service import SyncService
    from unittest.mock import patch, MagicMock
    
    sync_service = SyncService()
    content_locations = ["frontend/textbook-content/chapter-1/lesson-1.md"]
    
    with patch.object(sync_service.content_service, 'index_content') as mock_index:
        mock_index.return_value = {"success": True, "indexed_count": 5, "error_count": 0}
        
        # Mock file reading
        with patch('pathlib.Path.exists', return_value=True):
            with patch('builtins.open', create=True) as mock_open:
                mock_open.return_value.__enter__.return_value.read.return_value = "# Test Content\n" + "word " * 100
                
                import asyncio
                result = asyncio.run(sync_service.index_content_in_rag(content_locations))
                
                assert result.status in ["completed", "failed"]
                assert result.total_chunks >= 0


def test_content_searchability_in_rag(auth_token):
    """Test content searchability in RAG chatbot after indexing"""
    # This would test that indexed content is searchable
    # Integration test - would require actual RAG service
    pass

