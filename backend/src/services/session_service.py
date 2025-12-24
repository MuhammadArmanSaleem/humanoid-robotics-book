import logging
from typing import Dict, Optional
from datetime import datetime, timedelta
from uuid import uuid4
import asyncio

from ..models import ChatMessage, ChatSession
from ..config import settings


logger = logging.getLogger(__name__)


class SessionService:
    def __init__(self):
        # In-memory storage for sessions (would use Redis in production)
        self.sessions: Dict[str, ChatSession] = {}
        # Start cleanup task
        self._start_cleanup_task()

    def _start_cleanup_task(self):
        """
        Start background task to clean up expired sessions
        """
        # Note: In a real application, you'd run this as a background task
        # For now, we'll rely on manual cleanup checks
        pass

    def create_session(self, current_page: Optional[str] = None) -> ChatSession:
        """
        Create a new chat session
        """
        session_id = str(uuid4())
        now = datetime.now()
        expires_at = now + timedelta(hours=settings.session_timeout_hours)

        session = ChatSession(
            session_id=session_id,
            messages=[],
            created_at=now,
            current_page=current_page,
            expires_at=expires_at
        )

        self.sessions[session_id] = session
        logger.info(f"Created new session: {session_id}")
        return session

    def get_session(self, session_id: str) -> Optional[ChatSession]:
        """
        Get a session by ID, cleaning up if expired
        """
        if session_id not in self.sessions:
            return None

        session = self.sessions[session_id]

        # Check if session is expired
        if datetime.now() > session.expires_at:
            self.delete_session(session_id)
            logger.info(f"Session {session_id} expired and deleted")
            return None

        # Refresh expiration time
        session.expires_at = datetime.now() + timedelta(hours=settings.session_timeout_hours)
        return session

    def update_session(self, session: ChatSession) -> ChatSession:
        """
        Update an existing session
        """
        if session.session_id in self.sessions:
            # Refresh expiration time
            session.expires_at = datetime.now() + timedelta(hours=settings.session_timeout_hours)
            self.sessions[session.session_id] = session
            logger.debug(f"Updated session: {session.session_id}")
        return session

    def delete_session(self, session_id: str):
        """
        Delete a session
        """
        if session_id in self.sessions:
            del self.sessions[session_id]
            logger.info(f"Deleted session: {session_id}")

    def add_message_to_session(self, session_id: str, message: ChatMessage) -> Optional[ChatSession]:
        """
        Add a message to a session
        """
        session = self.get_session(session_id)
        if not session:
            logger.warning(f"Cannot add message to non-existent session: {session_id}")
            return None

        session.messages.append(message)

        # Limit messages to prevent memory issues (keep last 50)
        if len(session.messages) > 50:
            session.messages = session.messages[-50:]

        self.update_session(session)
        return session

    def cleanup_expired_sessions(self):
        """
        Remove all expired sessions
        """
        now = datetime.now()
        expired_sessions = [
            sid for sid, session in self.sessions.items()
            if now > session.expires_at
        ]

        for session_id in expired_sessions:
            del self.sessions[session_id]
            logger.info(f"Cleaned up expired session: {session_id}")

        return len(expired_sessions)

    def get_all_active_sessions(self) -> Dict[str, ChatSession]:
        """
        Get all non-expired sessions
        """
        active_sessions = {}
        now = datetime.now()

        for session_id, session in self.sessions.items():
            if now <= session.expires_at:
                active_sessions[session_id] = session
            else:
                # Clean up expired session
                del self.sessions[session_id]

        return active_sessions