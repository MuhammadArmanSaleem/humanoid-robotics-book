# Implementation Plan: Workflow Integration

**Branch**: `006-workflow-integration` | **Date**: 2025-12-23 | **Spec**: [specs/006-workflow-integration/spec.md](spec.md)
**Input**: Feature specification from `/specs/006-workflow-integration/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

The Workflow Integration feature will integrate the existing textbook content generation workflow (Content Architect, Lesson Template Generator, Technical Writer) with the backend API, enabling programmatic content generation, automatic validation, error handling, RAG indexing, and frontend synchronization. The implementation focuses on creating a unified API endpoint that orchestrates all workflow components, integrates error and edge case handling modules, executes validation scripts, indexes content in RAG, and ensures frontend-backend content synchronization.

## Technical Context

**Language/Version**: Python 3.11+ (FastAPI backend), existing workflow components (Claude Code agents/skills)  
**Primary Dependencies**: FastAPI, existing workflow components (Content Architect subagent, Lesson Template Generator skill, Technical Writer agent), error-handler.py, edge-case-handler.py, validate-word-count.py, validate-sources.py, ContentIndexingService (RAG), Qdrant client  
**Storage**: File system (Markdown files in `frontend/textbook-content/`), Qdrant vector database (for RAG indexing), in-memory job status tracking (with optional PostgreSQL persistence for future enhancement)  
**Testing**: pytest for backend API, manual verification for workflow integration, existing test scenarios from `specs/book-writing/tests/test-scenarios.md`  
**Target Platform**: Cross-platform (Linux, macOS, Windows) backend API server  
**Project Type**: Web application (backend API integration)  
**Performance Goals**: API endpoint responds within 2 seconds for request validation (SC-001), workflow completes and indexes content within 5 minutes (SC-002), 95% success rate without manual intervention (SC-003), content searchable in RAG within 1 minute (SC-004), frontend displays new content within 30 seconds (SC-005)  
**Constraints**: Handle concurrent requests gracefully (FR-007), provide status updates every 30 seconds for long-running jobs (SC-008), maintain <850 words per lesson, ensure frontend-backend content synchronization (FR-013)  
**Scale/Scope**: Support multiple concurrent content generation jobs, handle partial failures (some lessons succeed, others fail), integrate with existing RAG chatbot and Docusaurus frontend

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Core Principles Compliance

- **Content-First Development**: ✅ Integration prioritizes educational quality by ensuring generated content is validated before indexing and display
- **AI-Assisted Spec-Driven Workflow**: ✅ Following Spec-Kit Plus methodology with formal specification
- **Progressive Enhancement Architecture**: ✅ Building on existing stable components (Content Architect, Template Generator, Technical Writer)
- **Test-Before-Implement Discipline**: ✅ API endpoint tests will be written before implementation; existing test scenarios provide acceptance criteria
- **Documentation as Code**: ✅ PHR created for this planning phase

### Technical Stack Mandates

- **Backend API**: ✅ FastAPI (Python 3.11+) - already in use
- **Vector Database**: ✅ Qdrant Cloud - already integrated via ContentIndexingService
- **Testing**: ✅ pytest - standard for FastAPI projects; API tests before implementation
- **CI/CD**: ✅ Workflow integration tests will be added to GitHub Actions CI pipeline

### Quality Gates

- **Code Quality**: ✅ Follow existing backend code quality standards (type hints, Pydantic models, Black formatter, mypy if configured)
- **Performance Benchmarks**: ✅ Success criteria defined (SC-001 to SC-008)
- **Security Requirements**: ✅ Content generation API requires authentication (JWT) and rate limiting (using existing middleware)

### Gate Evaluation

**Status**: ✅ **PASS** - All clarifications resolved, no blocking violations
**Post-Design Re-evaluation**: ✅ **PASS** - Design phase completed with all requirements addressed

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── models.py                    # Existing models (add ContentGenerationRequest, ContentGenerationJob, ValidationResult, IntegrationStatus)
│   ├── routes/
│   │   └── content_generation.py    # NEW: Content generation API endpoint
│   ├── services/
│   │   ├── content_service.py        # Existing: RAG indexing service
│   │   ├── workflow_orchestrator.py  # NEW: Orchestrates workflow components
│   │   ├── validation_service.py     # NEW: Wraps validation scripts
│   │   └── sync_service.py           # NEW: Frontend-backend content sync
│   └── utils/
│       └── workflow_utils.py         # NEW: Utility functions for workflow execution
└── tests/
    ├── test_content_generation_api.py  # NEW: API endpoint tests
    ├── test_workflow_orchestrator.py   # NEW: Orchestrator tests
    └── test_integration.py             # NEW: End-to-end integration tests

frontend/
├── src/
│   └── [No changes - Docusaurus auto-detects new content]
└── textbook-content/                 # Existing: Generated content location
    └── [Content generated by workflow]

specs/book-writing/scripts/
├── error-handler.py                  # Existing: Error handling module
├── edge-case-handler.py             # Existing: Edge case handling module
├── validate-word-count.py           # Existing: Word count validation
└── validate-sources.py              # Existing: Source validation
```

**Structure Decision**: Web application structure (Option 2) - backend API integration with existing frontend. The workflow integration adds new backend services and routes while leveraging existing error handling, edge case handling, and validation scripts from `specs/book-writing/scripts/`. The frontend requires no changes as Docusaurus automatically detects new content files.

## Phase 0: Research Complete ✅

**Status**: All technical unknowns resolved  
**Output**: `research.md` - See [specs/006-workflow-integration/research.md](research.md)

**Resolved Clarifications**:
1. ✅ Job status storage: In-memory with optional DB persistence
2. ✅ Test-Before-Implement: API tests written before implementation
3. ✅ CI/CD integration: Tests added to GitHub Actions
4. ✅ Code quality standards: Follow existing backend standards
5. ✅ Authentication: Required with rate limiting
6. ✅ Component invocation: Subprocess wrapper for Claude Code agents
7. ✅ Frontend sync: File system-based, auto-detected by Docusaurus

## Phase 1: Design & Contracts Complete ✅

**Status**: Data model, API contracts, and quickstart documentation created  
**Outputs**:
- `data-model.md` - Entity definitions and relationships
- `contracts/openapi.yaml` - OpenAPI 3.0 specification
- `quickstart.md` - Integration examples and usage guide

**Key Design Decisions**:
- In-memory job status tracking (initial implementation)
- Asynchronous workflow execution with job polling
- Subprocess-based component invocation
- File system-based frontend sync (Docusaurus auto-detection)
- Integration with existing error/edge case handlers and validation scripts

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

No violations - all design decisions align with constitution requirements.
