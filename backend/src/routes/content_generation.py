"""Content Generation API routes"""

from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks, Header, Request
from typing import Optional
from datetime import datetime
import logging

from ..models import (
    ContentGenerationRequest, JobCreatedResponse, JobStatusResponse,
    JobCancelledResponse, ContentGenerationJob
)
from ..services.workflow_orchestrator import WorkflowOrchestrator
from ..utils.auth import get_current_user_id, verify_token
from ..utils.workflow_utils import (
    generate_job_id, create_job, get_job, update_job,
    set_active_job, clear_active_job, is_job_active, delete_job
)
from ..middleware.rate_limit import rate_limiter

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/content", tags=["Content Generation"])

# Initialize orchestrator
orchestrator = WorkflowOrchestrator()


async def get_current_user(authorization: Optional[str] = Header(None)):
    """Dependency to get current user from JWT token"""
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header required")
    
    token = authorization.replace("Bearer ", "")
    payload = verify_token(token)
    
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    return payload.get("sub")  # user_id


@router.post("/generate", response_model=JobCreatedResponse, status_code=202)
async def create_content_generation_job(
    request: ContentGenerationRequest,
    background_tasks: BackgroundTasks,
    http_request: Request,
    user_id: str = Depends(get_current_user)
):
    """
    Create a new content generation job
    
    Returns job_id immediately and processes workflow asynchronously.
    Rejects concurrent requests with HTTP 429.
    """
    # Apply rate limiting (stricter for content generation)
    if not rate_limiter.is_allowed(http_request):
        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded. Please try again later."
        )
    
    # Check for concurrent requests (FR-007)
    if is_job_active():
        raise HTTPException(
            status_code=429,
            detail="Another content generation job is already in progress. Please wait for it to complete."
        )
    
    # Validate request
    if not request.chapters or len(request.chapters) == 0:
        raise HTTPException(
            status_code=400,
            detail="At least one chapter must be specified"
        )
    
    if request.target_word_count and (request.target_word_count < 500 or request.target_word_count > 1000):
        raise HTTPException(
            status_code=400,
            detail="target_word_count must be between 500 and 1000"
        )
    
    # Generate job ID
    job_id = generate_job_id()
    
    # Set user_id from token
    request.user_id = user_id
    
    # Create job
    job_data = {
        "job_id": job_id,
        "status": "pending",
        "progress": 0.0,
        "current_step": "Job created",
        "created_at": datetime.utcnow().isoformat(),
        "request": request.dict(),
        "component_statuses": {},
        "user_id": user_id
    }
    
    create_job(job_id, job_data)
    
    # Set as active job (one at a time)
    if not set_active_job(job_id):
        raise HTTPException(
            status_code=429,
            detail="Failed to start job - another job may be active"
        )
    
    # Execute workflow in background
    background_tasks.add_task(execute_workflow_background, job_id, request)
    
    logger.info(f"Created content generation job {job_id} for user {user_id}")
    
    return JobCreatedResponse(
        job_id=job_id,
        status="pending",
        message="Content generation job created successfully",
        estimated_completion_time=300  # 5 minutes
    )


@router.get("/generate/{job_id}", response_model=JobStatusResponse)
async def get_job_status(
    job_id: str,
    user_id: str = Depends(get_current_user)
):
    """
    Get the status of a content generation job
    
    Clients should poll this endpoint every 30 seconds for status updates.
    Returns error details if job failed, with user-friendly messages.
    """
    job_data = get_job(job_id)
    
    if not job_data:
        raise HTTPException(status_code=404, detail=f"Job {job_id} not found")
    
    # Verify user owns the job (optional security check)
    if job_data.get("user_id") and job_data.get("user_id") != user_id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    # Ensure error details are properly formatted if present
    if job_data.get("error") and isinstance(job_data["error"], dict):
        # Error details already in correct format from ErrorDetails model
        pass
    
    # Convert to response model
    return JobStatusResponse(**job_data)


@router.post("/generate/{job_id}/cancel", response_model=JobCancelledResponse)
async def cancel_job(
    job_id: str,
    user_id: str = Depends(get_current_user)
):
    """
    Cancel a pending or in-progress content generation job
    
    Completed or failed jobs cannot be cancelled.
    """
    job_data = get_job(job_id)
    
    if not job_data:
        raise HTTPException(status_code=404, detail=f"Job {job_id} not found")
    
    # Verify user owns the job
    if job_data.get("user_id") and job_data.get("user_id") != user_id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    current_status = job_data.get("status")
    
    if current_status in ["completed", "failed", "cancelled"]:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot cancel job with status: {current_status}"
        )
    
    # Cancel the job
    update_job(job_id, {
        "status": "cancelled",
        "completed_at": datetime.utcnow().isoformat(),
        "current_step": "Job cancelled by user"
    })
    
    # Clear active job if this was the active one
    clear_active_job(job_id)
    
    logger.info(f"Cancelled job {job_id} by user {user_id}")
    
    return JobCancelledResponse(
        job_id=job_id,
        status="cancelled",
        message="Job cancelled successfully"
    )


async def execute_workflow_background(job_id: str, request: ContentGenerationRequest):
    """Background task to execute the workflow with error handling"""
    try:
        logger.info(f"Starting workflow execution for job {job_id}")
        result = await orchestrator.execute_workflow(job_id, request)
        
        if result.get("success"):
            logger.info(f"Workflow completed successfully for job {job_id}")
        else:
            error = result.get("error", {})
            error_msg = error.get("message", "Unknown error") if isinstance(error, dict) else str(error)
            logger.error(f"Workflow failed for job {job_id}: {error_msg}")
    except Exception as e:
        logger.error(f"Workflow execution error for job {job_id}: {str(e)}", exc_info=True)
        # Create user-friendly error message
        error_details = {
            "error_type": "workflow_error",
            "component": "workflow_orchestrator",
            "message": f"An unexpected error occurred during workflow execution: {str(e)}. Please check logs for details.",
            "recovery_suggestions": [
                "Verify input parameters are correct",
                "Check system logs for detailed error information",
                "Retry the request if the error appears transient",
                "Contact support if the error persists"
            ],
            "retryable": True,
            "occurred_at": datetime.utcnow().isoformat()
        }
        update_job(job_id, {
            "status": "failed",
            "error": error_details,
            "completed_at": datetime.utcnow().isoformat()
        })
    finally:
        # Clear active job when done
        clear_active_job(job_id)

