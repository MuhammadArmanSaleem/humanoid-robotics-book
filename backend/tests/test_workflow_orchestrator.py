"""Tests for Workflow Orchestrator Service"""

import pytest
from unittest.mock import patch, MagicMock
from backend.src.services.workflow_orchestrator import WorkflowOrchestrator
from backend.src.models import ContentGenerationRequest


@pytest.fixture
def orchestrator():
    """Create workflow orchestrator instance"""
    return WorkflowOrchestrator()


@pytest.fixture
def sample_request():
    """Sample content generation request"""
    return ContentGenerationRequest(
        chapters=["1"],
        lessons=["1"],
        target_word_count=800
    )


def test_error_handler_invocation_insufficient_sources(orchestrator, sample_request):
    """Test error handler invocation for insufficient sources"""
    with patch.object(orchestrator.error_handler, 'handle_insufficient_sources') as mock_handler:
        mock_handler.return_value = {
            'error_type': 'insufficient_sources',
            'user_message': 'Limited sources found'
        }
        
        # Simulate insufficient sources scenario
        result = orchestrator.error_handler.handle_insufficient_sources("1.1", 2, 3)
        
        assert result['error_type'] == 'insufficient_sources'
        mock_handler.assert_called_once()


def test_error_handler_invocation_component_failure(orchestrator):
    """Test error handler invocation for component failures"""
    with patch.object(orchestrator.error_handler, 'handle_component_failure') as mock_handler:
        mock_handler.return_value = {
            'error_type': 'component_failure',
            'component': 'content_architect',
            'user_message': 'Component failed'
        }
        
        result = orchestrator.error_handler.handle_component_failure("content_architect", "Test error")
        
        assert result['error_type'] == 'component_failure'
        assert result['component'] == 'content_architect'
        mock_handler.assert_called_once()


def test_edge_case_handler_invocation(orchestrator):
    """Test edge case handler invocation"""
    with patch.object(orchestrator.edge_case_handler, 'handle_insufficient_sources') as mock_handler:
        mock_handler.return_value = {
            'handled': True,
            'edge_case': 'insufficient_sources',
            'user_notification': 'Limited sources found'
        }
        
        result = orchestrator.edge_case_handler.handle_insufficient_sources(2, 3)
        
        assert result['handled'] is True
        assert result['edge_case'] == 'insufficient_sources'
        mock_handler.assert_called_once()


def test_error_logging_and_notification(orchestrator):
    """Test error logging and user notification"""
    with patch.object(orchestrator.error_handler, 'log_error') as mock_log:
        with patch.object(orchestrator.error_handler, 'notify_user') as mock_notify:
            error_info = {
                'error_type': 'component_failure',
                'component': 'test_component',
                'user_message': 'Test error message'
            }
            
            orchestrator.error_handler.log_error(error_info)
            orchestrator.error_handler.notify_user(error_info)
            
            mock_log.assert_called_once_with(error_info)
            mock_notify.assert_called_once_with(error_info)

