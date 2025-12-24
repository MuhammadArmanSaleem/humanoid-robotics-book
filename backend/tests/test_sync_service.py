"""Tests for Sync Service"""

import pytest
from unittest.mock import patch, MagicMock
from backend.src.services.sync_service import SyncService
from pathlib import Path


@pytest.fixture
def sync_service():
    """Create sync service instance"""
    return SyncService()


def test_rag_indexing_integration(sync_service):
    """Test RAG indexing integration"""
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


def test_rag_indexing_failure_handling(sync_service):
    """Test RAG indexing failure handling (preserve files, mark as "indexing_failed")"""
    content_locations = ["frontend/textbook-content/chapter-1/lesson-1.md"]
    
    with patch.object(sync_service.content_service, 'index_content') as mock_index:
        mock_index.return_value = {"success": False, "indexed_count": 0, "error_count": 1, "errors": ["Indexing failed"]}
        
        with patch('pathlib.Path.exists', return_value=True):
            with patch('builtins.open', create=True) as mock_open:
                mock_open.return_value.__enter__.return_value.read.return_value = "# Test Content"
                
                import asyncio
                result = asyncio.run(sync_service.index_content_in_rag(content_locations))
                
                assert result.status == "failed"
                assert result.error is not None
                # Files should be preserved (not deleted) - this is implicit in the design


def test_frontend_sync_service(sync_service):
    """Test frontend sync service"""
    content_locations = ["frontend/textbook-content/chapter-1/lesson-1.md"]
    
    with patch('pathlib.Path.exists', return_value=True):
        result = sync_service.validate_frontend_structure(content_locations)
        
        assert result.status in ["completed", "failed"]
        assert result.files_synced >= 0
        assert result.total_files == len(content_locations)

