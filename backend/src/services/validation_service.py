"""Validation Service

Wraps validation scripts (word count, source validation) for content quality verification.
"""

import logging
import subprocess
import json
from typing import Dict, Optional, List
from pathlib import Path
from datetime import datetime

from ..models import (
    ValidationResult, WordCountValidation, SourceValidation, QualityCheck
)

logger = logging.getLogger(__name__)

# Path to validation scripts
VALIDATION_SCRIPTS_PATH = Path(__file__).parent.parent.parent / "specs" / "book-writing" / "scripts"


class ValidationService:
    """Service for validating generated content"""
    
    def __init__(self):
        self.word_count_script = VALIDATION_SCRIPTS_PATH / "validate-word-count.py"
        self.sources_script = VALIDATION_SCRIPTS_PATH / "validate-sources.py"
    
    def validate_content(self, content_locations: List[str], target_word_count: int = 800) -> ValidationResult:
        """
        Validate all generated content files
        
        Args:
            content_locations: List of file paths to validate
            target_word_count: Target word count per lesson
            
        Returns:
            ValidationResult with overall status and detailed validation results
        """
        word_count_results = []
        source_results = []
        quality_checks = []
        errors = []
        warnings = []
        
        for file_path in content_locations:
            # Validate word count
            word_count_result = self._validate_word_count(file_path, target_word_count)
            word_count_results.append(word_count_result)
            
            if word_count_result["status"] == "failed":
                errors.append(f"Word count validation failed for {file_path}: {word_count_result.get('message', 'Unknown error')}")
            elif word_count_result["status"] == "warning":
                warnings.append(f"Word count warning for {file_path}: {word_count_result.get('message', '')}")
            
            # Validate sources
            source_result = self._validate_sources(file_path)
            source_results.append(source_result)
            
            if source_result["status"] == "failed":
                errors.append(f"Source validation failed for {file_path}: {source_result.get('message', 'Unknown error')}")
            elif source_result["status"] == "warning":
                warnings.append(f"Source validation warning for {file_path}: {source_result.get('message', '')}")
        
        # Aggregate results
        overall_word_count = self._aggregate_word_count_validation(word_count_results, target_word_count)
        overall_source = self._aggregate_source_validation(source_results)
        
        # Determine overall status
        if any(r["status"] == "failed" for r in word_count_results + source_results):
            overall_status = "failed"
        elif any(r["status"] == "warning" for r in word_count_results + source_results):
            overall_status = "warning"
        else:
            overall_status = "passed"
        
        return ValidationResult(
            overall_status=overall_status,
            word_count_validation=overall_word_count,
            source_validation=overall_source,
            quality_checks=quality_checks,
            errors=errors,
            warnings=warnings
        )
    
    def _validate_word_count(self, file_path: str, target_word_count: int) -> Dict:
        """Execute word count validation script"""
        try:
            file_path_obj = Path(file_path)
            if not file_path_obj.exists():
                return {
                    "status": "failed",
                    "message": f"File not found: {file_path}",
                    "target_word_count": target_word_count,
                    "actual_word_count": 0,
                    "variance": 100.0
                }
            
            # Execute validation script
            result = subprocess.run(
                ["python", str(self.word_count_script), str(file_path), str(target_word_count)],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode != 0:
                return {
                    "status": "failed",
                    "message": f"Validation script error: {result.stderr}",
                    "target_word_count": target_word_count,
                    "actual_word_count": 0,
                    "variance": 100.0
                }
            
            # Parse JSON output
            try:
                output = json.loads(result.stdout)
                return output
            except json.JSONDecodeError:
                # Fallback: parse text output
                return self._parse_word_count_output(result.stdout, target_word_count)
                
        except subprocess.TimeoutExpired:
            return {
                "status": "failed",
                "message": "Word count validation timed out",
                "target_word_count": target_word_count,
                "actual_word_count": 0,
                "variance": 100.0
            }
        except Exception as e:
            logger.error(f"Word count validation error for {file_path}: {str(e)}")
            return {
                "status": "failed",
                "message": f"Validation error: {str(e)}",
                "target_word_count": target_word_count,
                "actual_word_count": 0,
                "variance": 100.0
            }
    
    def _validate_sources(self, file_path: str) -> Dict:
        """Execute source validation script"""
        try:
            file_path_obj = Path(file_path)
            if not file_path_obj.exists():
                return {
                    "status": "failed",
                    "message": f"File not found: {file_path}",
                    "sources_checked": 0,
                    "authoritative_sources": 0,
                    "non_authoritative_sources": 0,
                    "min_required": 3
                }
            
            # Execute validation script
            result = subprocess.run(
                ["python", str(self.sources_script), str(file_path)],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode != 0:
                return {
                    "status": "failed",
                    "message": f"Validation script error: {result.stderr}",
                    "sources_checked": 0,
                    "authoritative_sources": 0,
                    "non_authoritative_sources": 0,
                    "min_required": 3
                }
            
            # Parse JSON output
            try:
                output = json.loads(result.stdout)
                return output
            except json.JSONDecodeError:
                # Fallback: parse text output
                return self._parse_source_output(result.stdout)
                
        except subprocess.TimeoutExpired:
            return {
                "status": "failed",
                "message": "Source validation timed out",
                "sources_checked": 0,
                "authoritative_sources": 0,
                "non_authoritative_sources": 0,
                "min_required": 3
            }
        except Exception as e:
            logger.error(f"Source validation error for {file_path}: {str(e)}")
            return {
                "status": "failed",
                "message": f"Validation error: {str(e)}",
                "sources_checked": 0,
                "authoritative_sources": 0,
                "non_authoritative_sources": 0,
                "min_required": 3
            }
    
    def _parse_word_count_output(self, output: str, target_word_count: int) -> Dict:
        """Parse word count validation output (fallback)"""
        # Simple parsing - in production, scripts should return JSON
        lines = output.strip().split('\n')
        actual_count = 0
        
        for line in lines:
            if 'word count' in line.lower() or 'words' in line.lower():
                try:
                    actual_count = int(''.join(filter(str.isdigit, line)))
                    break
                except:
                    pass
        
        if actual_count == 0:
            return {
                "status": "failed",
                "message": "Could not parse word count",
                "target_word_count": target_word_count,
                "actual_word_count": 0,
                "variance": 100.0
            }
        
        variance = abs(actual_count - target_word_count) / target_word_count * 100
        
        if variance < 10:
            status = "passed"
        elif variance < 20:
            status = "warning"
        else:
            status = "failed"
        
        return {
            "status": status,
            "target_word_count": target_word_count,
            "actual_word_count": actual_count,
            "variance": variance,
            "message": f"Word count: {actual_count} (target: {target_word_count}, variance: {variance:.1f}%)"
        }
    
    def _parse_source_output(self, output: str) -> Dict:
        """Parse source validation output (fallback)"""
        # Simple parsing - in production, scripts should return JSON
        lines = output.strip().split('\n')
        authoritative = 0
        non_authoritative = 0
        
        for line in lines:
            if 'authoritative' in line.lower():
                try:
                    authoritative = int(''.join(filter(str.isdigit, line)))
                except:
                    pass
            if 'non-authoritative' in line.lower() or 'non_authoritative' in line.lower():
                try:
                    non_authoritative = int(''.join(filter(str.isdigit, line)))
                except:
                    pass
        
        total = authoritative + non_authoritative
        min_required = 3
        
        if authoritative >= min_required:
            status = "passed"
        elif authoritative > 0:
            status = "warning"
        else:
            status = "failed"
        
        return {
            "status": status,
            "sources_checked": total,
            "authoritative_sources": authoritative,
            "non_authoritative_sources": non_authoritative,
            "min_required": min_required,
            "message": f"Sources: {authoritative} authoritative, {non_authoritative} non-authoritative (min required: {min_required})"
        }
    
    def _aggregate_word_count_validation(self, results: List[Dict], target_word_count: int) -> WordCountValidation:
        """Aggregate word count validation results"""
        if not results:
            return WordCountValidation(
                status="failed",
                target_word_count=target_word_count,
                actual_word_count=0,
                variance=100.0,
                message="No content files to validate"
            )
        
        total_actual = sum(r.get("actual_word_count", 0) for r in results)
        avg_actual = total_actual / len(results) if results else 0
        variance = abs(avg_actual - target_word_count) / target_word_count * 100 if target_word_count > 0 else 100.0
        
        # Determine overall status
        if any(r.get("status") == "failed" for r in results):
            status = "failed"
        elif any(r.get("status") == "warning" for r in results):
            status = "warning"
        else:
            status = "passed"
        
        return WordCountValidation(
            status=status,
            target_word_count=target_word_count,
            actual_word_count=int(avg_actual),
            variance=variance,
            message=f"Average word count: {int(avg_actual)} (target: {target_word_count}, variance: {variance:.1f}%)"
        )
    
    def _aggregate_source_validation(self, results: List[Dict]) -> SourceValidation:
        """Aggregate source validation results"""
        if not results:
            return SourceValidation(
                status="failed",
                sources_checked=0,
                authoritative_sources=0,
                non_authoritative_sources=0,
                min_required=3,
                message="No content files to validate"
            )
        
        total_checked = sum(r.get("sources_checked", 0) for r in results)
        total_authoritative = sum(r.get("authoritative_sources", 0) for r in results)
        total_non_authoritative = sum(r.get("non_authoritative_sources", 0) for r in results)
        min_required = 3
        
        # Determine overall status
        if any(r.get("status") == "failed" for r in results):
            status = "failed"
        elif any(r.get("status") == "warning" for r in results):
            status = "warning"
        else:
            status = "passed"
        
        return SourceValidation(
            status=status,
            sources_checked=total_checked,
            authoritative_sources=total_authoritative,
            non_authoritative_sources=total_non_authoritative,
            min_required=min_required,
            message=f"Total sources: {total_authoritative} authoritative, {total_non_authoritative} non-authoritative"
        )

