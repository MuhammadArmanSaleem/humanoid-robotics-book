# Research: Workflow Integration

**Feature**: Workflow Integration  
**Date**: 2025-12-23  
**Phase**: 0 - Research & Clarification

## Overview

This document resolves all "NEEDS CLARIFICATION" items identified in the Technical Context and Constitution Check sections of the implementation plan.

## Technical Unknowns Resolved

### 1. Persistent Job Status Storage

**Unknown**: Do we need persistent job status storage for content generation jobs?

**Research Findings**:
- Content generation jobs can take 5+ minutes (SC-002)
- Users need status updates every 30 seconds (SC-008)
- Concurrent requests must be handled gracefully (FR-007)
- Partial failures need tracking (FR-011)

**Decision**: Use in-memory job status tracking with optional persistence for long-running jobs
**Rationale**: 
- FastAPI can maintain job status in memory for active jobs
- For production, consider Redis or PostgreSQL for job persistence
- Initial implementation: in-memory dict with job_id → status mapping
- Future enhancement: Add database persistence for job history

**Alternatives considered**:
- Database-only: Adds complexity and latency for simple status checks
- File-based: Not suitable for concurrent access
- External job queue (Celery): Overkill for initial implementation

### 2. Test-Before-Implement for API Integration

**Unknown**: Should we write tests before implementing the API integration?

**Research Findings**:
- Constitution mandates Test-Before-Implement discipline
- Existing test scenarios exist in `specs/book-writing/tests/test-scenarios.md`
- FastAPI supports pytest with TestClient for API testing

**Decision**: Write API endpoint tests before implementation
**Rationale**:
- Aligns with constitution's Test-Before-Implement principle
- FastAPI TestClient allows testing endpoints without full server startup
- Existing test scenarios provide acceptance criteria
- Integration tests can be written after API implementation

**Test Strategy**:
1. Unit tests for workflow orchestrator (before orchestrator implementation)
2. API endpoint contract tests (before route implementation)
3. Integration tests (after implementation, using existing test scenarios)

### 3. CI/CD Integration

**Unknown**: Should workflow integration tests be added to GitHub Actions?

**Research Findings**:
- Constitution requires CI/CD via GitHub Actions
- Existing backend has test infrastructure
- Workflow integration is a critical feature requiring automated testing

**Decision**: Add workflow integration tests to GitHub Actions CI pipeline
**Rationale**:
- Ensures workflow integration doesn't break with future changes
- Validates API endpoints and workflow orchestration
- Can use mocked workflow components for faster CI execution

**Implementation**:
- Add `test_workflow_integration.py` to CI test suite
- Mock external dependencies (Claude Code agents) for CI
- Run full integration tests in staging environment

### 4. Code Quality Standards

**Unknown**: What linting/type checking standards should be applied?

**Research Findings**:
- Backend uses Python 3.11+ with FastAPI
- Existing codebase may have established standards
- Constitution requires code quality gates

**Decision**: Follow existing backend code quality standards
**Rationale**:
- Consistency with existing codebase
- FastAPI best practices recommend type hints and Pydantic models
- Use existing linting configuration if available

**Standards to Apply**:
- Type hints for all functions (Python 3.11+ syntax)
- Pydantic models for request/response validation
- Black or similar formatter for code style
- mypy for type checking (if configured)
- Follow existing backend code structure patterns

### 5. Authentication and Rate Limiting

**Unknown**: Should content generation API require authentication? Rate limiting?

**Research Findings**:
- Content generation is resource-intensive (5+ minutes per job)
- Constitution requires API rate limiting and abuse prevention
- Existing backend has auth_service and rate_limiter middleware
- Content generation should be restricted to authorized users

**Decision**: Require authentication and apply rate limiting
**Rationale**:
- Prevents abuse of resource-intensive content generation
- Aligns with security requirements in constitution
- Existing infrastructure (auth_service, rate_limiter) can be reused

**Implementation**:
- Use existing `@rate_limiter` middleware for rate limiting
- Require authentication token for content generation endpoint
- Consider different rate limits for content generation vs. chat API
- Log all content generation requests for monitoring

### 6. Workflow Component Invocation

**Unknown**: How to invoke Claude Code agents/skills from FastAPI backend?

**Research Findings**:
- Content Architect, Template Generator, Technical Writer are Claude Code components
- These are typically invoked via CLI or agent interface
- Backend needs to orchestrate these components programmatically

**Decision**: Use subprocess or Python subprocess wrapper to invoke Claude Code components
**Rationale**:
- Claude Code agents can be invoked via command-line interface
- Subprocess allows backend to execute and monitor component execution
- Can capture stdout/stderr for error handling and logging
- Alternative: If Claude Code provides Python SDK, use that instead

**Implementation Approach**:
- Create `WorkflowOrchestrator` service that manages subprocess execution
- Parse component outputs (stdout/stderr) for status and results
- Handle subprocess timeouts and errors gracefully
- Use existing error-handler.py for error processing

**Alternatives considered**:
- Direct Python API: Not available for Claude Code agents
- HTTP API wrapper: Would require additional service layer
- Queue-based: Adds complexity, may be future enhancement

### 7. Frontend Content Synchronization

**Unknown**: How does Docusaurus detect new content? How to ensure frontend-backend sync?

**Research Findings**:
- Docusaurus reads content from `frontend/textbook-content/` directory
- Docusaurus rebuilds on file system changes (in dev mode)
- Production requires build step to include new content
- Sidebars.ts needs updates for new chapters/lessons

**Decision**: 
- Backend generates content in `frontend/textbook-content/` directory
- Content Architect already updates sidebars.ts
- Frontend auto-detects new content on rebuild/refresh
- For production: Trigger Docusaurus rebuild after content generation

**Implementation**:
- Workflow generates content in correct directory structure
- Content Architect handles sidebars.ts updates (already implemented)
- Sync service validates content structure matches frontend expectations
- Optional: Webhook or API call to trigger frontend rebuild (future enhancement)

**Alternatives considered**:
- Separate content repository: Adds complexity
- Database-driven content: Not compatible with Docusaurus static site generation
- Manual sync step: Defeats automation purpose

## Best Practices Researched

### FastAPI Background Tasks
- Use `BackgroundTasks` for long-running operations
- Return job_id immediately, process asynchronously
- Provide status endpoint for job progress
- Use Server-Sent Events (SSE) for real-time status updates (optional enhancement)

### Error Handling Integration
- Import and use existing `error-handler.py` module
- Wrap workflow component invocations with error handling
- Log errors using error handler's logging mechanism
- Return user-friendly error messages via API

### Validation Integration
- Execute validation scripts as subprocess calls
- Parse validation script outputs (JSON or structured text)
- Include validation results in API response
- Block content indexing if validation fails (FR-012)

### RAG Indexing Integration
- Use existing `ContentIndexingService.index_content()` method
- Chunk generated content appropriately
- Index after successful validation
- Handle indexing errors gracefully

### Concurrent Request Handling
- Use job queue or in-memory job tracking
- Prevent duplicate jobs for same content request
- Limit concurrent content generation jobs (resource constraints)
- Return appropriate error if job limit reached

## Integration Patterns

### Workflow Orchestration Pattern
```
API Endpoint → WorkflowOrchestrator → Component Invocation → Error Handling → Validation → RAG Indexing → Sync Service → Response
```

### Status Tracking Pattern
```
Job Created → In Progress → Component Status Updates → Validation Status → Indexing Status → Complete/Failed
```

### Error Recovery Pattern
```
Component Error → Error Handler → Fallback Strategy → Retry (if applicable) → User Notification → Logging
```

## Dependencies and Prerequisites

### Existing Components (Available)
- ✅ Content Architect subagent (`.claude/agents/content-architect.md`)
- ✅ Lesson Template Generator skill (`.claude/skills/lesson-template-generator/SKILL.md`)
- ✅ Technical Writer agent (`.claude/agents/technical-writer.md`)
- ✅ Error handler (`specs/book-writing/scripts/error-handler.py`)
- ✅ Edge case handler (`specs/book-writing/scripts/edge-case-handler.py`)
- ✅ Validation scripts (`specs/book-writing/scripts/validate-*.py`)
- ✅ ContentIndexingService (`backend/src/services/content_service.py`)
- ✅ RAG service (`backend/src/services/rag_service.py`)

### New Components (To Implement)
- WorkflowOrchestrator service
- Content generation API route
- Validation service wrapper
- Sync service for frontend-backend coordination
- Job status tracking mechanism

## Performance Considerations

### Response Time Optimization
- Return job_id immediately (< 2 seconds per SC-001)
- Process workflow asynchronously
- Use background tasks for long-running operations

### Resource Management
- Limit concurrent content generation jobs
- Monitor memory usage during workflow execution
- Implement job timeout (e.g., 10 minutes max)

### Status Update Mechanism
- Poll-based: Client polls status endpoint every 30 seconds
- Future: SSE for real-time updates (optional enhancement)

## Security Considerations

### Authentication
- Require valid auth token for content generation endpoint
- Verify user permissions (if role-based access needed)

### Rate Limiting
- Apply stricter rate limits for content generation (e.g., 5 requests/hour)
- Different limits than chat API (chat is more frequent)

### Input Validation
- Validate content generation request parameters
- Sanitize file paths to prevent directory traversal
- Validate chapter/lesson specifications

## Testing Strategy

### Unit Tests
- WorkflowOrchestrator service methods
- Validation service wrapper
- Sync service utilities
- Error handler integration

### Integration Tests
- End-to-end workflow execution
- Error handling scenarios
- Validation failure handling
- RAG indexing integration
- Frontend sync validation

### Contract Tests
- API endpoint request/response contracts
- Status endpoint contracts
- Error response contracts

## Open Questions Resolved

All "NEEDS CLARIFICATION" items from Technical Context and Constitution Check have been resolved:
1. ✅ Job status storage: In-memory with optional DB persistence
2. ✅ Test-Before-Implement: Yes, write API tests before implementation
3. ✅ CI/CD integration: Add tests to GitHub Actions
4. ✅ Code quality standards: Follow existing backend standards
5. ✅ Authentication: Required with rate limiting
6. ✅ Component invocation: Subprocess wrapper for Claude Code agents
7. ✅ Frontend sync: File system-based, auto-detected by Docusaurus

## Next Steps

Proceed to Phase 1: Design & Contracts
- Generate data-model.md with entities and relationships
- Create API contracts in contracts/ directory
- Generate quickstart.md with integration examples

