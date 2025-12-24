from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum


class RoleEnum(str, Enum):
    user = "user"
    assistant = "assistant"
    system = "system"


class Source(BaseModel):
    url: str
    title: str
    chapter: str
    lesson: str
    relevance: float


class ContentChunk(BaseModel):
    id: str
    content: str
    chapter: str
    lesson: str
    section: Optional[str] = None
    url: str
    embedding: Optional[List[float]] = None  # 384-dimensional vector


class ChatMessage(BaseModel):
    id: str
    role: RoleEnum
    content: str
    sources: Optional[List[Source]] = []
    timestamp: datetime


class ChatSession(BaseModel):
    session_id: str
    messages: List[ChatMessage] = []
    created_at: datetime
    current_page: Optional[str] = None
    expires_at: datetime


class ChatRequest(BaseModel):
    message: str
    context: Optional[Dict[str, Any]] = {}


class ChatResponse(BaseModel):
    type: str  # text, sources, navigation, session_update
    content: Optional[str] = None
    sources: Optional[List[Source]] = []
    navigation: Optional[List[Dict[str, str]]] = []  # {url: str, title: str}
    session_id: Optional[str] = None


class IndexContentRequest(BaseModel):
    content_chunks: List[ContentChunk]


class IndexContentResponse(BaseModel):
    success: bool
    indexed_count: int
    error_count: int
    errors: List[str] = []


# Authentication Models
class SignupRequest(BaseModel):
    email: str
    password: str
    software_experience: str  # beginner, intermediate, advanced
    hardware_experience: str  # beginner, intermediate, advanced
    programming_languages: List[str]  # e.g., ["Python", "C++", "JavaScript"]
    robotics_background: Optional[str] = None
    learning_goals: Optional[str] = None


class SigninRequest(BaseModel):
    email: str
    password: str


class UserResponse(BaseModel):
    id: str
    email: str
    is_active: bool
    created_at: datetime


class AuthResponse(BaseModel):
    user: UserResponse
    access_token: str
    token_type: str = "bearer"


class BackgroundData(BaseModel):
    software_experience: str  # beginner, intermediate, advanced
    hardware_experience: str  # beginner, intermediate, advanced
    programming_languages: List[str]
    robotics_background: Optional[str] = None
    learning_goals: Optional[str] = None


class UpdateBackgroundRequest(BaseModel):
    background: BackgroundData


class TokenData(BaseModel):
    user_id: str
    email: str


# Content Generation Models
class ContentGenerationRequest(BaseModel):
    chapters: List[str]
    lessons: Optional[List[str]] = None
    research_guidance: Optional[Dict[str, str]] = None
    target_word_count: Optional[int] = 800
    user_id: Optional[str] = None
    priority: Optional[str] = "normal"


class LessonResult(BaseModel):
    lesson_id: str
    status: str  # "completed", "failed", "skipped"
    file_path: Optional[str] = None
    word_count: Optional[int] = None
    sources_used: Optional[int] = None
    error: Optional[str] = None
    edge_cases_handled: Optional[List[str]] = None


class ContentGenerationResults(BaseModel):
    lessons_generated: List[LessonResult]
    total_lessons: int
    successful_lessons: int
    failed_lessons: int
    content_locations: List[str]
    generation_time: float
    warnings: List[str] = []


class WordCountValidation(BaseModel):
    status: str  # "passed", "failed", "warning"
    target_word_count: int
    actual_word_count: int
    variance: float
    message: Optional[str] = None


class SourceValidation(BaseModel):
    status: str  # "passed", "failed", "warning"
    sources_checked: int
    authoritative_sources: int
    non_authoritative_sources: int
    min_required: int = 3
    message: Optional[str] = None


class QualityCheck(BaseModel):
    check_name: str
    status: str  # "passed", "failed", "warning"
    message: Optional[str] = None


class ValidationResult(BaseModel):
    overall_status: str  # "passed", "failed", "warning"
    word_count_validation: WordCountValidation
    source_validation: SourceValidation
    quality_checks: List[QualityCheck] = []
    errors: List[str] = []
    warnings: List[str] = []


class RAGIndexingStatus(BaseModel):
    status: str  # "pending", "in_progress", "completed", "failed"
    chunks_indexed: int
    total_chunks: int
    error: Optional[str] = None
    indexed_at: Optional[datetime] = None


class FrontendSyncStatus(BaseModel):
    status: str  # "pending", "in_progress", "completed", "failed"
    files_synced: int
    total_files: int
    error: Optional[str] = None
    synced_at: Optional[datetime] = None
    requires_rebuild: bool = False


class ErrorDetails(BaseModel):
    error_type: str  # "insufficient_sources", "component_failure", "validation_error", "workflow_error", "timeout_error"
    component: Optional[str] = None
    message: str
    recovery_suggestions: List[str] = []
    retryable: bool = False
    occurred_at: datetime


class ContentGenerationJob(BaseModel):
    job_id: str
    status: str  # "pending", "in_progress", "validating", "indexing", "syncing", "completed", "failed", "cancelled"
    progress: float  # 0.0 to 100.0
    current_step: Optional[str] = None
    created_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    request: ContentGenerationRequest
    results: Optional[ContentGenerationResults] = None
    error: Optional[ErrorDetails] = None
    component_statuses: Dict[str, str] = {}  # component -> status
    validation_results: Optional[ValidationResult] = None
    indexing_status: Optional[str] = None  # "pending", "in_progress", "completed", "failed"
    sync_status: Optional[str] = None  # "pending", "in_progress", "completed", "failed"


class JobCreatedResponse(BaseModel):
    job_id: str
    status: str
    message: str
    estimated_completion_time: Optional[int] = None


class JobStatusResponse(BaseModel):
    job_id: str
    status: str
    progress: float
    current_step: Optional[str] = None
    created_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    request: ContentGenerationRequest
    results: Optional[ContentGenerationResults] = None
    error: Optional[ErrorDetails] = None
    component_statuses: Dict[str, str] = {}
    validation_results: Optional[ValidationResult] = None
    indexing_status: Optional[str] = None
    sync_status: Optional[str] = None


class JobCancelledResponse(BaseModel):
    job_id: str
    status: str
    message: str