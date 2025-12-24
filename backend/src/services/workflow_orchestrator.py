"""Workflow Orchestrator Service

Orchestrates the content generation workflow:
Content Architect → Template Generator → Technical Writer → Validation → RAG Indexing → Frontend Sync
"""

import logging
import subprocess
import json
import os
import importlib.util
from typing import Dict, Optional, List
from uuid import uuid4
from datetime import datetime
from pathlib import Path

# Initialize logger first
logger = logging.getLogger(__name__)

# Import error and edge case handlers
import sys
# Calculate path: backend/src/services/workflow_orchestrator.py -> repo root
handler_scripts_path = Path(__file__).parent.parent.parent.parent / "specs" / "book-writing" / "scripts"
sys.path.insert(0, str(handler_scripts_path))

# Try to import handlers (files use hyphens, so we need importlib)
HANDLERS_AVAILABLE = False
ErrorHandler = None
ErrorType = None
EdgeCaseHandler = None
EdgeCaseType = None

try:
    # Import error-handler.py (with hyphen)
    error_handler_path = handler_scripts_path / "error-handler.py"
    if error_handler_path.exists():
        spec = importlib.util.spec_from_file_location("error_handler", error_handler_path)
        error_handler_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(error_handler_module)
        ErrorHandler = error_handler_module.ErrorHandler
        ErrorType = error_handler_module.ErrorType
    
    # Import edge-case-handler.py (with hyphen)
    edge_case_handler_path = handler_scripts_path / "edge-case-handler.py"
    if edge_case_handler_path.exists():
        spec = importlib.util.spec_from_file_location("edge_case_handler", edge_case_handler_path)
        edge_case_handler_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(edge_case_handler_module)
        EdgeCaseHandler = edge_case_handler_module.EdgeCaseHandler
        EdgeCaseType = edge_case_handler_module.EdgeCaseType
    
    if ErrorHandler and EdgeCaseHandler:
        HANDLERS_AVAILABLE = True
except Exception as e:
    HANDLERS_AVAILABLE = False
    logger.warning(f"Error and edge case handlers not available: {e}")

from ..models import (
    ContentGenerationRequest, ContentGenerationJob, ContentGenerationResults,
    LessonResult, ErrorDetails
)
from ..utils.workflow_utils import update_job, get_job
from .validation_service import ValidationService
from .sync_service import SyncService


class WorkflowOrchestrator:
    """Orchestrates the content generation workflow"""
    
    def __init__(self):
        self.error_handler = ErrorHandler() if HANDLERS_AVAILABLE else None
        self.edge_case_handler = EdgeCaseHandler() if HANDLERS_AVAILABLE else None
        self.validation_service = ValidationService()
        self.sync_service = SyncService()
        self.content_dir = Path(__file__).parent.parent.parent.parent / "frontend" / "textbook-content"
        
    async def execute_workflow(self, job_id: str, request: ContentGenerationRequest) -> Dict:
        """Execute the complete content generation workflow"""
        workflow_start_time = datetime.utcnow()
        try:
            # Update job status to in_progress
            update_job(job_id, {
                "status": "in_progress",
                "started_at": datetime.utcnow().isoformat(),
                "progress": 0.0,
                "current_step": "Starting workflow",
                "component_statuses": {
                    "content_architect": "pending",
                    "template_generator": "pending",
                    "technical_writer": "pending"
                }
            })
            
            # Step 1: Content Architect (20% progress)
            update_job(job_id, {"progress": 10.0, "current_step": "Running Content Architect"})
            architect_result = await self._invoke_content_architect(request)
            update_job(job_id, {
                "progress": 20.0,
                "component_statuses": {"content_architect": "completed" if architect_result["success"] else "failed"}
            })
            
            if not architect_result["success"]:
                return self._handle_workflow_error(job_id, "content_architect", architect_result.get("error", "Unknown error"), architect_result.get("error_info"))
            
            # Step 2: Template Generator (40% progress)
            update_job(job_id, {"progress": 30.0, "current_step": "Running Template Generator"})
            template_result = await self._invoke_template_generator(request)
            update_job(job_id, {
                "progress": 40.0,
                "component_statuses": {"template_generator": "completed" if template_result["success"] else "failed"}
            })
            
            if not template_result["success"]:
                return self._handle_workflow_error(job_id, "template_generator", template_result.get("error", "Unknown error"), template_result.get("error_info"))
            
            # Step 3: Technical Writer (70% progress)
            update_job(job_id, {"progress": 50.0, "current_step": "Generating content with Technical Writer"})
            writer_results = await self._invoke_technical_writer(request)
            update_job(job_id, {
                "progress": 70.0,
                "component_statuses": {"technical_writer": "completed" if writer_results["success"] else "failed"}
            })
            
            if not writer_results["success"]:
                return self._handle_workflow_error(job_id, "technical_writer", writer_results.get("error", "Unknown error"))
            
            # Build results
            results = ContentGenerationResults(
                lessons_generated=writer_results.get("lessons", []),
                total_lessons=len(writer_results.get("lessons", [])),
                successful_lessons=len([l for l in writer_results.get("lessons", []) if l.get("status") == "completed"]),
                failed_lessons=len([l for l in writer_results.get("lessons", []) if l.get("status") == "failed"]),
                content_locations=writer_results.get("content_locations", []),
                generation_time=writer_results.get("generation_time", 0.0),
                warnings=writer_results.get("warnings", [])
            )
            
            # Step 4: Validation (80% progress)
            update_job(job_id, {"progress": 75.0, "current_step": "Validating generated content", "status": "validating"})
            validation_result = self.validation_service.validate_content(
                results.content_locations,
                request.target_word_count or 800
            )
            
            # If validation fails, block RAG indexing (FR-012)
            if validation_result.overall_status == "failed":
                update_job(job_id, {
                    "status": "validation_failed",
                    "progress": 80.0,
                    "validation_results": validation_result.dict(),
                    "indexing_status": "blocked",
                    "current_step": "Validation failed - RAG indexing blocked",
                    "completed_at": datetime.utcnow().isoformat(),
                    "results": results.dict()
                })
                logger.warning(f"Validation failed for job {job_id} - RAG indexing blocked")
                return {
                    "success": False,
                    "job_id": job_id,
                    "results": results.dict(),
                    "validation_result": validation_result.dict(),
                    "error": "Validation failed - content preserved but RAG indexing blocked"
                }
            
            update_job(job_id, {
                "progress": 80.0,
                "validation_results": validation_result.dict(),
                "current_step": "Validation passed"
            })
            
            # Step 5: RAG Indexing (90% progress)
            update_job(job_id, {"progress": 85.0, "current_step": "Indexing content in RAG system", "status": "indexing", "indexing_status": "in_progress"})
            indexing_status = await self.sync_service.index_content_in_rag(results.content_locations)
            
            # Handle indexing failure (preserve files, mark as "indexing_failed")
            if indexing_status.status == "failed":
                update_job(job_id, {
                    "status": "indexing_failed",
                    "progress": 90.0,
                    "indexing_status": "failed",
                    "current_step": "RAG indexing failed - content preserved",
                    "completed_at": datetime.utcnow().isoformat(),
                    "results": results.dict(),
                    "validation_results": validation_result.dict()
                })
                logger.warning(f"RAG indexing failed for job {job_id} - content preserved, manual retry available")
                return {
                    "success": False,
                    "job_id": job_id,
                    "results": results.dict(),
                    "validation_result": validation_result.dict(),
                    "indexing_status": indexing_status.dict(),
                    "error": "RAG indexing failed - content preserved, manual retry available"
                }
            
            update_job(job_id, {
                "progress": 90.0,
                "indexing_status": "completed",
                "current_step": "Content indexed in RAG system"
            })
            
            # Step 6: Frontend Sync (95% progress)
            update_job(job_id, {"progress": 92.0, "current_step": "Synchronizing with frontend", "status": "syncing", "sync_status": "in_progress"})
            sync_status = self.sync_service.validate_frontend_structure(results.content_locations)
            
            update_job(job_id, {
                "progress": 95.0,
                "sync_status": sync_status.status,
                "current_step": "Frontend sync completed"
            })
            
            # Handle partial failures (index successful lessons, report failed ones)
            successful_lessons = [l for l in results.lessons_generated if l.get("status") == "completed"]
            failed_lessons = [l for l in results.lessons_generated if l.get("status") == "failed"]
            
            # Index only successful lessons if there are partial failures
            if failed_lessons and successful_lessons:
                logger.info(f"Partial failure: {len(successful_lessons)} successful, {len(failed_lessons)} failed")
                successful_locations = [l.get("file_path") for l in successful_lessons if l.get("file_path")]
                if successful_locations:
                    # Re-index only successful lessons
                    indexing_status = await self.sync_service.index_content_in_rag(successful_locations)
                    update_job(job_id, {"indexing_status": indexing_status.status})
            
            # Mark as completed
            workflow_duration = (datetime.utcnow() - workflow_start_time).total_seconds()
            logger.info(f"Workflow completed for job {job_id} in {workflow_duration:.2f} seconds")
            
            update_job(job_id, {
                "status": "completed",
                "progress": 100.0,
                "completed_at": datetime.utcnow().isoformat(),
                "current_step": "Workflow completed",
                "results": results.dict(),
                "validation_results": validation_result.dict()
            })
            
            # Performance metrics logging
            logger.info(f"Job {job_id} metrics: duration={workflow_duration:.2f}s, lessons={results.total_lessons}, "
                       f"successful={results.successful_lessons}, failed={results.failed_lessons}")
            
            return {
                "success": True,
                "job_id": job_id,
                "results": results.dict(),
                "validation_result": validation_result.dict(),
                "indexing_status": indexing_status.dict(),
                "sync_status": sync_status.dict()
            }
            
        except Exception as e:
            logger.error(f"Workflow execution failed: {str(e)}", exc_info=True)
            return self._handle_workflow_error(job_id, "workflow", str(e))
    
    async def _invoke_content_architect(self, request: ContentGenerationRequest) -> Dict:
        """Invoke Content Architect subagent via subprocess with error handling"""
        try:
            # Build command: claude agent content-architect with input
            chapters_str = ",".join(request.chapters)
            lessons_str = ",".join(request.lessons) if request.lessons else ""
            
            input_text = f"chapters {chapters_str}"
            if lessons_str:
                input_text += f", lessons {lessons_str}"
            
            logger.info(f"Invoking Content Architect with: {input_text}")
            
            # Mock implementation - replace with actual subprocess call
            # result = subprocess.run(
            #     ["claude", "agent", "content-architect"],
            #     input=input_text.encode(),
            #     capture_output=True,
            #     timeout=600,
            #     cwd=str(self.content_dir.parent)
            # )
            
            # For now, return success (actual implementation will call subprocess)
            return {"success": True, "output": "Content structure generated"}
            
        except subprocess.TimeoutExpired:
            error_msg = "Content Architect execution timed out"
            error_info = None
            if self.error_handler:
                error_info = self.error_handler.handle_component_failure("content_architect", error_msg)
                self.error_handler.log_error(error_info)
                self.error_handler.notify_user(error_info)
            return {"success": False, "error": error_msg, "error_info": error_info}
        except Exception as e:
            error_msg = f"Content Architect failed: {str(e)}"
            error_info = None
            if self.error_handler:
                error_info = self.error_handler.handle_component_failure("content_architect", error_msg, {"exception": str(e)})
                self.error_handler.log_error(error_info)
                self.error_handler.notify_user(error_info)
            return {"success": False, "error": error_msg, "error_info": error_info}
    
    async def _invoke_template_generator(self, request: ContentGenerationRequest) -> Dict:
        """Invoke Lesson Template Generator skill via subprocess with error handling"""
        try:
            logger.info("Invoking Lesson Template Generator")
            
            # Mock implementation - replace with actual subprocess call
            # Template generator is typically invoked automatically by Content Architect
            # but can be called separately if needed
            
            return {"success": True, "output": "Templates generated"}
            
        except Exception as e:
            error_msg = f"Template Generator failed: {str(e)}"
            error_info = None
            if self.error_handler:
                error_info = self.error_handler.handle_component_failure("template_generator", error_msg, {"exception": str(e)})
                self.error_handler.log_error(error_info)
                self.error_handler.notify_user(error_info)
            return {"success": False, "error": error_msg, "error_info": error_info}
    
    async def _invoke_technical_writer(self, request: ContentGenerationRequest) -> Dict:
        """Invoke Technical Writer agent via subprocess for each lesson with error and edge case handling"""
        lessons = []
        content_locations = []
        warnings = []
        edge_cases_handled = []
        start_time = datetime.utcnow()
        
        # Generate lessons based on chapters and lessons
        for chapter in request.chapters:
            lesson_list = request.lessons if request.lessons else ["1", "2"]
            for lesson in lesson_list:
                lesson_id = f"{chapter}.{lesson}"
                try:
                    # Build research guidance
                    research_guidance = ""
                    if request.research_guidance and lesson_id in request.research_guidance:
                        research_guidance = request.research_guidance[lesson_id]
                    
                    # Invoke Technical Writer
                    input_text = f"Generate ~{request.target_word_count} words for lesson {lesson_id}."
                    if research_guidance:
                        input_text += f"\n{research_guidance}"
                    
                    logger.info(f"Invoking Technical Writer for lesson {lesson_id}")
                    
                    # Check for insufficient sources (edge case)
                    sources_found = 3  # Mock - in real implementation, check actual sources
                    if self.edge_case_handler and sources_found < 3:
                        edge_case_result = self.edge_case_handler.handle_insufficient_sources(sources_found, 3)
                        if edge_case_result.get("handled"):
                            edge_cases_handled.append(edge_case_result["edge_case"])
                            warnings.append(edge_case_result["user_notification"])
                            logger.warning(f"Edge case handled for {lesson_id}: {edge_case_result['edge_case']}")
                    
                    # Mock implementation - replace with actual subprocess call
                    # result = subprocess.run(
                    #     ["claude", "agent", "technical-writer"],
                    #     input=input_text.encode(),
                    #     capture_output=True,
                    #     timeout=300,
                    #     cwd=str(self.content_dir.parent)
                    # )
                    
                    # Mock lesson result
                    file_path = f"frontend/textbook-content/chapter-{chapter}/lesson-{lesson}.md"
                    lesson_result = {
                        "lesson_id": lesson_id,
                        "status": "completed",
                        "file_path": file_path,
                        "word_count": request.target_word_count,
                        "sources_used": sources_found
                    }
                    if edge_cases_handled:
                        lesson_result["edge_cases_handled"] = edge_cases_handled
                    
                    lessons.append(lesson_result)
                    content_locations.append(file_path)
                    
                except subprocess.TimeoutExpired:
                    error_msg = f"Technical Writer timeout for lesson {lesson_id}"
                    logger.error(error_msg)
                    error_info = None
                    if self.error_handler:
                        error_info = self.error_handler.handle_component_failure("technical_writer", error_msg, {"lesson_id": lesson_id})
                        self.error_handler.log_error(error_info)
                        self.error_handler.notify_user(error_info)
                    lessons.append({
                        "lesson_id": lesson_id,
                        "status": "failed",
                        "error": error_msg,
                        "error_info": error_info
                    })
                except Exception as e:
                    error_msg = f"Technical Writer failed for lesson {lesson_id}: {str(e)}"
                    logger.error(error_msg)
                    error_info = None
                    if self.error_handler:
                        error_info = self.error_handler.handle_component_failure("technical_writer", error_msg, {"lesson_id": lesson_id, "exception": str(e)})
                        self.error_handler.log_error(error_info)
                        self.error_handler.notify_user(error_info)
                    lessons.append({
                        "lesson_id": lesson_id,
                        "status": "failed",
                        "error": error_msg,
                        "error_info": error_info
                    })
        
        generation_time = (datetime.utcnow() - start_time).total_seconds()
        
        # Handle insufficient sources error if needed (FR-008)
        total_sources = sum(l.get("sources_used", 0) for l in lessons if l.get("status") == "completed")
        if total_sources < 3 and self.error_handler:
            error_info = self.error_handler.handle_insufficient_sources("workflow", total_sources, 3)
            warnings.append(error_info.get("user_message", "Insufficient sources detected"))
        
        return {
            "success": len([l for l in lessons if l.get("status") == "completed"]) > 0,
            "lessons": lessons,
            "content_locations": content_locations,
            "generation_time": generation_time,
            "warnings": warnings
        }
    
    def _handle_workflow_error(self, job_id: str, component: str, error_message: str, error_info: Optional[Dict] = None) -> Dict:
        """Handle workflow errors with error handler and user-friendly messages"""
        # Use error_info from handler if available, otherwise create basic error details
        if error_info and self.error_handler:
            recovery_suggestions = error_info.get("recovery_strategy", "").split("\n") if error_info.get("recovery_strategy") else []
            user_message = error_info.get("user_message", error_message)
        else:
            recovery_suggestions = ["Check component logs", "Verify input parameters", "Retry the request"]
            user_message = error_message
            if self.error_handler:
                error_info = self.error_handler.handle_component_failure(component, error_message)
                user_message = error_info.get("user_message", error_message)
                recovery_suggestions = error_info.get("recovery_strategy", "").split("\n") if error_info.get("recovery_strategy") else recovery_suggestions
        
        error_details = ErrorDetails(
            error_type=error_info.get("error_type", "component_failure") if error_info else "component_failure",
            component=component,
            message=user_message,
            recovery_suggestions=recovery_suggestions,
            retryable=error_info.get("retryable", True) if error_info else True,
            occurred_at=datetime.utcnow()
        )
        
        if self.error_handler:
            self.error_handler.log_error(error_info if error_info else {"error_type": "component_failure", "component": component, "message": error_message})
        
        update_job(job_id, {
            "status": "failed",
            "progress": 0.0,
            "error": error_details.dict(),
            "completed_at": datetime.utcnow().isoformat()
        })
        
        return {"success": False, "job_id": job_id, "error": error_details.dict()}

