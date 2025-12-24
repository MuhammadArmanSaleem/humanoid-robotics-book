"""Tests for Validation Service"""

import pytest
from unittest.mock import patch, MagicMock
from backend.src.services.validation_service import ValidationService
from pathlib import Path


@pytest.fixture
def validation_service():
    """Create validation service instance"""
    return ValidationService()


def test_word_count_validation_execution(validation_service):
    """Test word count validation execution"""
    test_file = Path("test_lesson.md")
    
    # Create a test file
    test_file.write_text("# Test Lesson\n" + "word " * 800)
    
    try:
        with patch('subprocess.run') as mock_run:
            mock_result = MagicMock()
            mock_result.returncode = 0
            mock_result.stdout = '{"status": "passed", "target_word_count": 800, "actual_word_count": 800, "variance": 0.0}'
            mock_result.stderr = ""
            mock_run.return_value = mock_result
            
            result = validation_service._validate_word_count(str(test_file), 800)
            
            assert "status" in result
            assert "target_word_count" in result
    finally:
        if test_file.exists():
            test_file.unlink()


def test_source_validation_execution(validation_service):
    """Test source validation execution"""
    test_file = Path("test_lesson.md")
    
    # Create a test file with sources
    content = "# Test Lesson\n## Further Reading\n- https://example.edu/article\n- https://example.org/paper"
    test_file.write_text(content)
    
    try:
        with patch('subprocess.run') as mock_run:
            mock_result = MagicMock()
            mock_result.returncode = 0
            mock_result.stdout = '{"status": "passed", "sources_checked": 2, "authoritative_sources": 2, "non_authoritative_sources": 0, "min_required": 3}'
            mock_result.stderr = ""
            mock_run.return_value = mock_result
            
            result = validation_service._validate_sources(str(test_file))
            
            assert "status" in result
            assert "authoritative_sources" in result
    finally:
        if test_file.exists():
            test_file.unlink()


def test_validation_failure_handling(validation_service):
    """Test validation failure handling (block RAG indexing)"""
    content_locations = ["test1.md", "test2.md"]
    
    # Mock validation to return failed status
    with patch.object(validation_service, '_validate_word_count', return_value={"status": "failed", "message": "Word count too low"}):
        with patch.object(validation_service, '_validate_sources', return_value={"status": "passed"}):
            result = validation_service.validate_content(content_locations, 800)
            
            assert result.overall_status == "failed"
            assert len(result.errors) > 0


def test_validation_results_in_job_status():
    """Test validation results in job status response"""
    # This test would verify that validation results are included in job status
    # Integration test - would be tested in test_content_generation_api.py
    pass

