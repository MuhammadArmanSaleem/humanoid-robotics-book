# Data Model: Workflow Integration

**Feature**: Workflow Integration  
**Date**: 2025-12-23  
**Phase**: 1 - Design & Contracts

## Overview

This document defines the data models and entities for the Workflow Integration feature, including request/response models, job status tracking, and validation results.

## Core Entities

### ContentGenerationRequest

Represents a request to generate textbook content with specifications.

**Fields**:
- `chapters`: List[str] - Chapter identifiers to generate (e.g., ["1", "2", "3"] or ["1-3"])
- `lessons`: Optional[List[str]] - Lesson identifiers per chapter (e.g., ["1", "2"] or ["1-2"])
- `research_guidance`: Optional[Dict[str, str]] - Research guidance per lesson (lesson_id → guidance text)
- `target_word_count`: Optional[int] - Target words per lesson (default: 800)
- `user_id`: Optional[str] - User ID making the request (for authentication/authorization)
- `priority`: Optional[str] - Job priority ("low", "normal", "high") (default: "normal")

**Validation Rules**:
- `chapters` must be non-empty
- `chapters` format: "1", "1-3", or ["1", "2", "3"]
- `lessons` format: "1", "1-2", or ["1", "2"]
- `target_word_count` must be between 500 and 1000 (inclusive)

**Example**:
```json
{
  "chapters": ["1", "2", "3"],
  "lessons": ["1", "2"],
  "research_guidance": {
    "1.1": "Focus on embodied intelligence definition and sensor-motor integration",
    "1.2": "Cover history from Brooks 1991 to modern robots"
  },
  "target_word_count": 800,
  "priority": "normal"
}
```

### ContentGenerationJob

Represents an active or completed content generation workflow with status, progress, and results.

**Fields**:
- `job_id`: str - Unique job identifier (UUID)
- `status`: str - Job status enum: "pending", "in_progress", "validating", "indexing", "syncing", "completed", "failed", "cancelled"
- `progress`: float - Progress percentage (0.0 to 100.0)
- `current_step`: Optional[str] - Current workflow step description
- `created_at`: datetime - Job creation timestamp
- `started_at`: Optional[datetime] - Workflow start timestamp
- `completed_at`: Optional[datetime] - Workflow completion timestamp
- `request`: ContentGenerationRequest - Original request
- `results`: Optional[ContentGenerationResults] - Generation results (when completed)
- `error`: Optional[ErrorDetails] - Error information (when failed)
- `component_statuses`: Dict[str, str] - Status of each component ("pending", "in_progress", "completed", "failed")
- `validation_results`: Optional[ValidationResult] - Validation results
- `indexing_status`: Optional[str] - RAG indexing status ("pending", "in_progress", "completed", "failed")
- `sync_status`: Optional[str] - Frontend sync status ("pending", "in_progress", "completed", "failed")

**State Transitions**:
```
pending → in_progress → validating → indexing → syncing → completed
                                    ↓
                                 failed (at any step)
```

**Validation Rules**:
- `progress` must be between 0.0 and 100.0
- `status` must be valid enum value
- `completed_at` must be after `started_at` (if both present)

### ContentGenerationResults

Represents the results of a completed content generation job.

**Fields**:
- `lessons_generated`: List[LessonResult] - Results for each generated lesson
- `total_lessons`: int - Total number of lessons generated
- `successful_lessons`: int - Number of successfully generated lessons
- `failed_lessons`: int - Number of failed lessons
- `content_locations`: List[str] - File paths to generated content
- `generation_time`: float - Total generation time in seconds
- `warnings`: List[str] - Non-fatal warnings during generation

**Example**:
```json
{
  "lessons_generated": [
    {
      "lesson_id": "1.1",
      "status": "completed",
      "file_path": "frontend/textbook-content/chapter-1-introduction/lesson-1-what-is-physical-ai.md",
      "word_count": 812,
      "sources_used": 4
    }
  ],
  "total_lessons": 6,
  "successful_lessons": 6,
  "failed_lessons": 0,
  "content_locations": [
    "frontend/textbook-content/chapter-1-introduction/lesson-1-what-is-physical-ai.md",
    "frontend/textbook-content/chapter-1-introduction/lesson-2-history-and-evolution.md"
  ],
  "generation_time": 245.3,
  "warnings": []
}
```

### LessonResult

Represents the result for a single lesson generation.

**Fields**:
- `lesson_id`: str - Lesson identifier (e.g., "1.1")
- `status`: str - Generation status ("completed", "failed", "skipped")
- `file_path`: Optional[str] - Path to generated markdown file
- `word_count`: Optional[int] - Actual word count of generated content
- `sources_used`: Optional[int] - Number of research sources used
- `error`: Optional[str] - Error message if failed
- `edge_cases_handled`: Optional[List[str]] - Edge cases that were handled

### ValidationResult

Represents the outcome of content validation (word count, sources, quality checks).

**Fields**:
- `overall_status`: str - Validation status ("passed", "failed", "warning")
- `word_count_validation`: WordCountValidation - Word count validation results
- `source_validation`: SourceValidation - Source validation results
- `quality_checks`: List[QualityCheck] - Additional quality check results
- `errors`: List[str] - Validation errors
- `warnings`: List[str] - Validation warnings

**Validation Rules**:
- `overall_status` is "failed" if any critical validation fails
- `overall_status` is "warning" if non-critical issues found
- `overall_status` is "passed" if all validations pass

### WordCountValidation

Word count validation results.

**Fields**:
- `status`: str - Validation status ("passed", "failed", "warning")
- `target_word_count`: int - Target word count
- `actual_word_count`: int - Actual word count
- `variance`: float - Percentage variance from target
- `message`: Optional[str] - Validation message

**Validation Rules**:
- `status` is "passed" if variance < 10%
- `status` is "warning" if 10% <= variance < 20%
- `status` is "failed" if variance >= 20%

### SourceValidation

Source validation results.

**Fields**:
- `status`: str - Validation status ("passed", "failed", "warning")
- `sources_checked`: int - Number of sources validated
- `authoritative_sources`: int - Number of authoritative sources
- `non_authoritative_sources`: int - Number of non-authoritative sources
- `min_required`: int - Minimum required authoritative sources (default: 3)
- `message`: Optional[str] - Validation message

**Validation Rules**:
- `status` is "passed" if authoritative_sources >= min_required
- `status` is "warning" if 1 <= authoritative_sources < min_required
- `status` is "failed" if authoritative_sources == 0

### QualityCheck

Additional quality check result.

**Fields**:
- `check_name`: str - Name of the quality check
- `status`: str - Check status ("passed", "failed", "warning")
- `message`: Optional[str] - Check result message

### IntegrationStatus

Represents the status of content integration (RAG indexing, frontend sync, validation).

**Fields**:
- `rag_indexing`: RAGIndexingStatus - RAG indexing status
- `frontend_sync`: FrontendSyncStatus - Frontend synchronization status
- `validation`: ValidationStatus - Validation status
- `overall_status`: str - Overall integration status ("pending", "in_progress", "completed", "failed")

### RAGIndexingStatus

RAG indexing status information.

**Fields**:
- `status`: str - Indexing status ("pending", "in_progress", "completed", "failed")
- `chunks_indexed`: int - Number of content chunks indexed
- `total_chunks`: int - Total number of chunks to index
- `error`: Optional[str] - Error message if failed
- `indexed_at`: Optional[datetime] - Indexing completion timestamp

### FrontendSyncStatus

Frontend synchronization status information.

**Fields**:
- `status`: str - Sync status ("pending", "in_progress", "completed", "failed")
- `files_synced`: int - Number of files synchronized
- `total_files`: int - Total number of files to sync
- `error`: Optional[str] - Error message if failed
- `synced_at`: Optional[datetime] - Sync completion timestamp
- `requires_rebuild`: bool - Whether Docusaurus rebuild is required

### ErrorDetails

Error information for failed jobs.

**Fields**:
- `error_type`: str - Error type enum: "insufficient_sources", "component_failure", "validation_error", "workflow_error", "timeout_error"
- `component`: Optional[str] - Component that failed (e.g., "content_architect", "technical_writer")
- `message`: str - Error message
- `recovery_suggestions`: List[str] - Suggested recovery actions
- `retryable`: bool - Whether the error is retryable
- `occurred_at`: datetime - Error occurrence timestamp

## Relationships

### ContentGenerationJob Relationships

```
ContentGenerationJob
├── has_one: ContentGenerationRequest (original request)
├── has_one: ContentGenerationResults (when completed)
├── has_one: ValidationResult (validation results)
├── has_one: IntegrationStatus (integration status)
└── has_one: ErrorDetails (when failed)
```

### ContentGenerationResults Relationships

```
ContentGenerationResults
└── has_many: LessonResult (one per generated lesson)
```

### ValidationResult Relationships

```
ValidationResult
├── has_one: WordCountValidation
├── has_one: SourceValidation
└── has_many: QualityCheck
```

### IntegrationStatus Relationships

```
IntegrationStatus
├── has_one: RAGIndexingStatus
└── has_one: FrontendSyncStatus
```

## Data Storage

### In-Memory Storage (Initial Implementation)

- `jobs: Dict[str, ContentGenerationJob]` - Job ID → Job mapping
- Job expiration: Jobs older than 24 hours are removed
- Job limit: Maximum 100 active jobs (configurable)

### Future: Database Storage (Optional Enhancement)

**PostgreSQL Schema** (if persistent storage needed):
```sql
CREATE TABLE content_generation_jobs (
    job_id UUID PRIMARY KEY,
    status VARCHAR(50) NOT NULL,
    progress FLOAT NOT NULL,
    request JSONB NOT NULL,
    results JSONB,
    error JSONB,
    created_at TIMESTAMP NOT NULL,
    started_at TIMESTAMP,
    completed_at TIMESTAMP
);

CREATE INDEX idx_jobs_status ON content_generation_jobs(status);
CREATE INDEX idx_jobs_created_at ON content_generation_jobs(created_at);
```

## Validation Rules Summary

### Request Validation
- Chapters must be non-empty and valid format
- Lessons must be valid format (if provided)
- Target word count must be 500-1000
- Research guidance keys must match lesson IDs

### Job Status Validation
- Status transitions must be valid
- Progress must be 0.0-100.0
- Timestamps must be chronological

### Results Validation
- Successful lessons must have file_path
- Word count must be within target range (±20%)
- Sources must meet minimum requirements

## API Response Models

### POST /api/content/generate Response

**Success Response (202 Accepted)**:
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "pending",
  "message": "Content generation job created",
  "estimated_completion_time": 300
}
```

**Error Response (400 Bad Request)**:
```json
{
  "error": "validation_error",
  "message": "Invalid chapters format",
  "details": {
    "field": "chapters",
    "issue": "Chapters must be non-empty"
  }
}
```

### GET /api/content/generate/{job_id} Response

**Success Response (200 OK)**:
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "completed",
  "progress": 100.0,
  "current_step": "Content generation completed",
  "created_at": "2025-12-23T10:00:00Z",
  "started_at": "2025-12-23T10:00:01Z",
  "completed_at": "2025-12-23T10:05:15Z",
  "results": {
    "total_lessons": 6,
    "successful_lessons": 6,
    "failed_lessons": 0,
    "content_locations": [...]
  }
}
```

**Error Response (404 Not Found)**:
```json
{
  "error": "job_not_found",
  "message": "Job with ID 550e8400-e29b-41d4-a716-446655440000 not found"
}
```

