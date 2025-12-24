"""Workflow Utility Functions

Utility functions for workflow execution, job tracking, and concurrent request management.
"""

import logging
from typing import Dict, Optional
from uuid import uuid4
from datetime import datetime, timedelta
import threading

logger = logging.getLogger(__name__)

# In-memory job storage
_jobs: Dict[str, Dict] = {}
_job_lock = threading.Lock()
_active_job_lock = threading.Lock()
_active_job_id: Optional[str] = None

# Job expiration: 24 hours
JOB_EXPIRATION_HOURS = 24
MAX_JOBS = 100

# Background task for cleanup
import threading
import time

def start_cleanup_task():
    """Start background task to clean up expired jobs"""
    def cleanup_loop():
        while True:
            try:
                cleanup_expired_jobs()
                time.sleep(3600)  # Run every hour
            except Exception as e:
                logger.error(f"Cleanup task error: {str(e)}")
    
    cleanup_thread = threading.Thread(target=cleanup_loop, daemon=True)
    cleanup_thread.start()
    logger.info("Started job cleanup background task")


def generate_job_id() -> str:
    """Generate a unique job ID using UUID"""
    return str(uuid4())


def create_job(job_id: str, job_data: Dict) -> None:
    """Create a new job in in-memory storage"""
    with _job_lock:
        # Clean up expired jobs if we're approaching the limit
        if len(_jobs) >= MAX_JOBS * 0.9:
            cleanup_expired_jobs()
        
        job_data['created_at'] = datetime.utcnow()
        _jobs[job_id] = job_data
        logger.info(f"Created job {job_id}")


def get_job(job_id: str) -> Optional[Dict]:
    """Get a job by ID"""
    with _job_lock:
        job = _jobs.get(job_id)
        if job:
            # Check if expired
            created_at = job.get('created_at')
            if created_at and isinstance(created_at, datetime):
                if datetime.utcnow() - created_at > timedelta(hours=JOB_EXPIRATION_HOURS):
                    logger.info(f"Job {job_id} has expired")
                    del _jobs[job_id]
                    return None
        return job


def update_job(job_id: str, updates: Dict) -> bool:
    """Update a job with new data"""
    with _job_lock:
        if job_id not in _jobs:
            return False
        _jobs[job_id].update(updates)
        logger.debug(f"Updated job {job_id}")
        return True


def delete_job(job_id: str) -> bool:
    """Delete a job"""
    with _job_lock:
        if job_id in _jobs:
            del _jobs[job_id]
            logger.info(f"Deleted job {job_id}")
            return True
        return False


def cleanup_expired_jobs() -> None:
    """Remove expired jobs from storage"""
    now = datetime.utcnow()
    expired_jobs = []
    
    for job_id, job_data in _jobs.items():
        created_at = job_data.get('created_at')
        if created_at and isinstance(created_at, datetime):
            if now - created_at > timedelta(hours=JOB_EXPIRATION_HOURS):
                expired_jobs.append(job_id)
    
    for job_id in expired_jobs:
        del _jobs[job_id]
        logger.info(f"Cleaned up expired job {job_id}")
    
    if expired_jobs:
        logger.info(f"Cleaned up {len(expired_jobs)} expired jobs")


def is_job_active() -> bool:
    """Check if there is an active job"""
    with _active_job_lock:
        if _active_job_id is None:
            return False
        # Verify the job still exists and is active
        job = get_job(_active_job_id)
        if job and job.get('status') in ['pending', 'in_progress', 'validating', 'indexing', 'syncing']:
            return True
        else:
            # Job completed or doesn't exist, clear active job
            _active_job_id = None
            return False


def set_active_job(job_id: str) -> bool:
    """Set the active job (only one job can be active at a time)"""
    with _active_job_lock:
        if _active_job_id is not None:
            # Check if the current active job is still running
            if is_job_active():
                return False
            # Current job is done, clear it
            _active_job_id = None
        
        _active_job_id = job_id
        logger.info(f"Set active job: {job_id}")
        return True


def clear_active_job(job_id: Optional[str] = None) -> None:
    """Clear the active job"""
    with _active_job_lock:
        if job_id is None or _active_job_id == job_id:
            _active_job_id = None
            logger.info(f"Cleared active job: {job_id}")


def get_active_job_id() -> Optional[str]:
    """Get the current active job ID"""
    with _active_job_lock:
        return _active_job_id


# Initialize cleanup task on module import
try:
    start_cleanup_task()
except Exception as e:
    logger.warning(f"Failed to start cleanup task: {e}")

