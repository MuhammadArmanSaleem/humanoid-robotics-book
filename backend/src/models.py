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