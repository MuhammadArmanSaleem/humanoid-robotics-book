#!/usr/bin/env python3
"""
Error Handler Module
Implements error handling for workflow components (T104-T116)
"""

import logging
import sys
from enum import Enum
from typing import Optional, Dict, Any
from datetime import datetime


class ErrorType(Enum):
    """Error types for workflow components"""
    INSUFFICIENT_SOURCES = "insufficient_sources"
    COMPONENT_FAILURE = "component_failure"
    VALIDATION_ERROR = "validation_error"
    WORKFLOW_ERROR = "workflow_error"
    TIMEOUT_ERROR = "timeout_error"


class ErrorHandler:
    """Error handler for textbook content generation workflow"""
    
    def __init__(self, log_file: Optional[str] = None):
        """Initialize error handler with logging"""
        self.logger = logging.getLogger('workflow_error_handler')
        self.logger.setLevel(logging.INFO)
        
        if log_file:
            handler = logging.FileHandler(log_file)
            handler.setFormatter(
                logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            )
            self.logger.addHandler(handler)
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(
            logging.Formatter('%(levelname)s: %(message)s')
        )
        self.logger.addHandler(console_handler)
    
    def handle_insufficient_sources(self, 
                                   lesson_id: str,
                                   sources_found: int,
                                   min_required: int = 3) -> Dict[str, Any]:
        """
        Handle insufficient research sources error (FR-008)
        
        Args:
            lesson_id: Identifier for the lesson
            sources_found: Number of sources found
            min_required: Minimum required sources
        
        Returns:
            Dict with error details and recovery suggestions
        """
        error_info = {
            'error_type': ErrorType.INSUFFICIENT_SOURCES.value,
            'lesson_id': lesson_id,
            'sources_found': sources_found,
            'min_required': min_required,
            'timestamp': datetime.now().isoformat(),
            'recovery_strategy': 'fallback_to_available_sources',
            'user_message': (
                f"Limited research sources found for {lesson_id}. "
                f"Found {sources_found} sources (minimum: {min_required}). "
                "Proceeding with available sources. Consider adding more authoritative sources."
            )
        }
        
        self.logger.warning(
            f"Insufficient sources for {lesson_id}: {sources_found}/{min_required}"
        )
        
        return error_info
    
    def handle_component_failure(self,
                                component: str,
                                error_message: str,
                                context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Handle component failure error
        
        Args:
            component: Name of the failed component
            error_message: Error message from component
            context: Additional context about the failure
        
        Returns:
            Dict with error details and recovery suggestions
        """
        error_info = {
            'error_type': ErrorType.COMPONENT_FAILURE.value,
            'component': component,
            'error_message': error_message,
            'context': context or {},
            'timestamp': datetime.now().isoformat(),
            'recovery_strategy': 'retry_with_backoff',
            'user_message': (
                f"Content generation component '{component}' failed. "
                "Please check logs and retry. Error details logged."
            )
        }
        
        self.logger.error(
            f"Component failure: {component} - {error_message}",
            extra={'context': context}
        )
        
        return error_info
    
    def handle_validation_error(self,
                               validation_type: str,
                               error_details: str,
                               lesson_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Handle content validation error
        
        Args:
            validation_type: Type of validation that failed
            error_details: Details about the validation failure
            lesson_id: Identifier for the lesson (if applicable)
        
        Returns:
            Dict with error details and recovery suggestions
        """
        error_info = {
            'error_type': ErrorType.VALIDATION_ERROR.value,
            'validation_type': validation_type,
            'error_details': error_details,
            'lesson_id': lesson_id,
            'timestamp': datetime.now().isoformat(),
            'recovery_strategy': 'regenerate_with_adjustments',
            'user_message': (
                f"Content validation failed: {validation_type}. "
                f"Regenerating with adjusted parameters. Details: {error_details}"
            )
        }
        
        self.logger.warning(
            f"Validation error: {validation_type} - {error_details}",
            extra={'lesson_id': lesson_id}
        )
        
        return error_info
    
    def notify_user(self, error_info: Dict[str, Any]) -> None:
        """Notify user of error (T108)"""
        user_message = error_info.get('user_message', 'An error occurred during content generation.')
        print(f"\n⚠️  {user_message}\n")
    
    def log_error(self, error_info: Dict[str, Any]) -> None:
        """Log error for debugging (T109)"""
        self.logger.error(
            f"Error logged: {error_info['error_type']}",
            extra=error_info
        )


def create_fallback_strategy(error_type: ErrorType) -> str:
    """Create fallback strategy based on error type (T110)"""
    strategies = {
        ErrorType.INSUFFICIENT_SOURCES: (
            "1. Expand search terms\n"
            "2. Use related concepts\n"
            "3. Proceed with available sources (minimum 1)\n"
            "4. Flag lesson for manual review"
        ),
        ErrorType.COMPONENT_FAILURE: (
            "1. Retry component invocation (max 3 attempts)\n"
            "2. Use alternative component if available\n"
            "3. Skip failed component if non-critical\n"
            "4. Report failure for manual intervention"
        ),
        ErrorType.VALIDATION_ERROR: (
            "1. Adjust generation parameters\n"
            "2. Regenerate content with corrections\n"
            "3. Apply post-processing adjustments\n"
            "4. Flag for manual review if auto-correction fails"
        )
    }
    return strategies.get(error_type, "Manual intervention required")


if __name__ == '__main__':
    # Example usage
    handler = ErrorHandler('workflow_errors.log')
    
    # Test insufficient sources handling
    error = handler.handle_insufficient_sources('lesson-1.1', sources_found=2)
    handler.notify_user(error)
    print(f"Fallback strategy:\n{create_fallback_strategy(ErrorType.INSUFFICIENT_SOURCES)}")
    
    # Test component failure handling
    error = handler.handle_component_failure(
        'Technical Writer',
        'Content generation failed',
        {'lesson_id': 'lesson-1.1', 'attempt': 1}
    )
    handler.notify_user(error)

