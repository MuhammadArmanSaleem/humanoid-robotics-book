"""Sync Service

Handles frontend-backend content synchronization and RAG indexing.
"""

import logging
from typing import Dict, Optional, List
from pathlib import Path
from datetime import datetime

from ..services.content_service import ContentIndexingService
from ..models import ContentChunk, RAGIndexingStatus, FrontendSyncStatus, IndexContentRequest

logger = logging.getLogger(__name__)


class SyncService:
    """Service for synchronizing content between frontend and backend"""
    
    def __init__(self):
        self.content_service = ContentIndexingService()
        self.content_dir = Path(__file__).parent.parent.parent.parent / "frontend" / "textbook-content"
    
    async def index_content_in_rag(self, content_locations: List[str]) -> RAGIndexingStatus:
        """
        Index generated content in RAG system
        
        Args:
            content_locations: List of file paths to index
            
        Returns:
            RAGIndexingStatus with indexing results
        """
        try:
            chunks_to_index = []
            total_chunks = 0
            
            for file_path in content_locations:
                file_path_obj = Path(file_path)
                if not file_path_obj.exists():
                    logger.warning(f"Content file not found: {file_path}")
                    continue
                
                # Read content
                with open(file_path_obj, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Extract chapter and lesson from path
                # Path format: frontend/textbook-content/chapter-{N}/lesson-{M}.md
                parts = file_path_obj.parts
                chapter = "unknown"
                lesson = "unknown"
                
                for part in parts:
                    if part.startswith("chapter-"):
                        chapter = part.replace("chapter-", "")
                    elif part.startswith("lesson-") or (part.endswith(".md") and "lesson" in part):
                        lesson = part.replace("lesson-", "").replace(".md", "")
                
                # Chunk content
                content_chunks = self.content_service.chunk_text(content, chunk_size=500, overlap_size=50)
                
                # Create ContentChunk objects
                for idx, chunk_text in enumerate(content_chunks):
                    chunk = ContentChunk(
                        id=f"{file_path}_{idx}",
                        content=chunk_text,
                        chapter=chapter,
                        lesson=lesson,
                        url=f"/docs/{chapter}/{lesson}",
                        section=None
                    )
                    chunks_to_index.append(chunk)
                    total_chunks += 1
            
            if not chunks_to_index:
                return RAGIndexingStatus(
                    status="failed",
                    chunks_indexed=0,
                    total_chunks=0,
                    error="No content chunks to index",
                    indexed_at=None
                )
            
            # Index in RAG system
            index_request = IndexContentRequest(content_chunks=chunks_to_index)
            index_response = self.content_service.index_content(index_request.content_chunks)
            
            if index_response.get("success", False):
                indexed_count = index_response.get("indexed_count", 0)
                return RAGIndexingStatus(
                    status="completed",
                    chunks_indexed=indexed_count,
                    total_chunks=total_chunks,
                    error=None,
                    indexed_at=datetime.utcnow()
                )
            else:
                errors = index_response.get("errors", [])
                error_msg = "; ".join(errors) if errors else "Unknown indexing error"
                return RAGIndexingStatus(
                    status="failed",
                    chunks_indexed=index_response.get("indexed_count", 0),
                    total_chunks=total_chunks,
                    error=error_msg,
                    indexed_at=None
                )
                
        except Exception as e:
            logger.error(f"RAG indexing error: {str(e)}", exc_info=True)
            return RAGIndexingStatus(
                status="failed",
                chunks_indexed=0,
                total_chunks=total_chunks if 'total_chunks' in locals() else 0,
                error=f"Indexing error: {str(e)}",
                indexed_at=None
            )
    
    def validate_frontend_structure(self, content_locations: List[str]) -> FrontendSyncStatus:
        """
        Validate that generated content matches frontend structure expectations
        
        Args:
            content_locations: List of file paths to validate
            
        Returns:
            FrontendSyncStatus with validation results
        """
        try:
            files_synced = 0
            total_files = len(content_locations)
            errors = []
            
            for file_path in content_locations:
                file_path_obj = Path(file_path)
                
                # Check if file exists
                if not file_path_obj.exists():
                    errors.append(f"File not found: {file_path}")
                    continue
                
                # Check if file is in correct directory structure
                if "textbook-content" not in str(file_path_obj):
                    errors.append(f"File not in textbook-content directory: {file_path}")
                    continue
                
                # Check if file has valid markdown extension
                if not file_path_obj.suffix == ".md":
                    errors.append(f"File is not markdown: {file_path}")
                    continue
                
                files_synced += 1
            
            status = "completed" if files_synced == total_files and not errors else "failed"
            
            return FrontendSyncStatus(
                status=status,
                files_synced=files_synced,
                total_files=total_files,
                error="; ".join(errors) if errors else None,
                synced_at=datetime.utcnow() if status == "completed" else None,
                requires_rebuild=False  # Docusaurus auto-detects new files in dev mode
            )
            
        except Exception as e:
            logger.error(f"Frontend structure validation error: {str(e)}", exc_info=True)
            return FrontendSyncStatus(
                status="failed",
                files_synced=0,
                total_files=len(content_locations),
                error=f"Validation error: {str(e)}",
                synced_at=None,
                requires_rebuild=False
            )

