# Tasks: Workflow Integration

**Feature**: Workflow Integration  
**Branch**: `006-workflow-integration`  
**Generated**: 2025-12-23  
**Spec**: [specs/006-workflow-integration/spec.md](spec.md)  
**Plan**: [specs/006-workflow-integration/plan.md](plan.md)

## Overview

This document contains the complete task breakdown for implementing the Workflow Integration feature, organized by user story priority. Each task follows the checklist format for immediate executability.

## Dependencies

**Blocking Tasks:**
- Phase 1 (Setup): Must complete before any other work
- Phase 2 (Foundational): Blocks all user stories - MUST complete before Phase 3+
- T001-T009: Core infrastructure required for all user stories

**Story Dependencies:**
- US1 (P1): Can start after Phase 2 - No dependencies on other stories
- US2 (P2): Can start after Phase 2 - Integrates with US1 components but independently testable
- US3 (P3): Can start after Phase 2 - Integrates with US1/US2 but independently testable
- US4 (P4): Can start after Phase 2 - Integrates with US1/US3 but independently testable

**Execution Order:** Setup → Foundational → US1 (MVP) → US2 → US3 → US4 → Polish

## Phase 1: Setup (Shared Infrastructure)

**Goal**: Initialize project structure and dependencies

- [X] T001 Create backend/src/routes/content_generation.py route file structure
- [X] T002 Create backend/src/services/workflow_orchestrator.py service file
- [X] T003 Create backend/src/services/validation_service.py service file
- [X] T004 Create backend/src/services/sync_service.py service file
- [X] T005 Create backend/src/utils/workflow_utils.py utility file
- [X] T006 Create backend/tests/test_content_generation_api.py test file structure
- [X] T007 Create backend/tests/test_workflow_orchestrator.py test file structure
- [X] T008 Create backend/tests/test_integration.py test file structure

---

## Phase 2: Foundational (Blocking Prerequisites)

**Goal**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T009 [P] Add ContentGenerationRequest model to backend/src/models.py
- [X] T010 [P] Add ContentGenerationJob model to backend/src/models.py
- [X] T011 [P] Add ValidationResult model to backend/src/models.py
- [X] T012 [P] Add IntegrationStatus model to backend/src/models.py
- [X] T013 [P] Add ContentGenerationResults model to backend/src/models.py
- [X] T014 [P] Add LessonResult model to backend/src/models.py
- [X] T015 [P] Add ErrorDetails model to backend/src/models.py
- [X] T016 [P] Add WordCountValidation model to backend/src/models.py
- [X] T017 [P] Add SourceValidation model to backend/src/models.py
- [X] T018 [P] Add QualityCheck model to backend/src/models.py
- [X] T019 [P] Add RAGIndexingStatus model to backend/src/models.py
- [X] T020 [P] Add FrontendSyncStatus model to backend/src/models.py
- [X] T021 Implement in-memory job status tracking in backend/src/utils/workflow_utils.py
- [X] T022 Implement job ID generation (UUID) in backend/src/utils/workflow_utils.py
- [X] T023 Implement concurrent request lock mechanism (one job at a time) in backend/src/utils/workflow_utils.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Content Generation API Integration (Priority: P1) 🎯 MVP

**Goal**: Enable course developers to trigger textbook content generation workflow through backend API endpoint

**Independent Test**: Call POST /api/content/generate with valid request, verify job_id returned, poll GET /api/content/generate/{job_id} to verify workflow execution and content generation

### Tests for User Story 1

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [X] T024 [P] [US1] Contract test for POST /api/content/generate endpoint in backend/tests/test_content_generation_api.py
- [X] T025 [P] [US1] Contract test for GET /api/content/generate/{job_id} endpoint in backend/tests/test_content_generation_api.py
- [X] T026 [P] [US1] Integration test for content generation workflow execution in backend/tests/test_integration.py
- [X] T027 [P] [US1] Test concurrent request rejection (HTTP 429) in backend/tests/test_content_generation_api.py

### Implementation for User Story 1

- [X] T028 [US1] Implement WorkflowOrchestrator service in backend/src/services/workflow_orchestrator.py with subprocess invocation for Content Architect
- [X] T029 [US1] Extend WorkflowOrchestrator to invoke Lesson Template Generator via subprocess in backend/src/services/workflow_orchestrator.py
- [X] T030 [US1] Extend WorkflowOrchestrator to invoke Technical Writer via subprocess in backend/src/services/workflow_orchestrator.py
- [X] T031 [US1] Implement job status tracking and progress updates in backend/src/services/workflow_orchestrator.py
- [X] T032 [US1] Implement POST /api/content/generate endpoint in backend/src/routes/content_generation.py (returns job_id, handles concurrent requests with 429)
- [X] T033 [US1] Implement GET /api/content/generate/{job_id} endpoint in backend/src/routes/content_generation.py (returns job status and progress)
- [X] T034 [US1] Integrate authentication middleware for content generation endpoints in backend/src/routes/content_generation.py
- [X] T035 [US1] Add request validation for ContentGenerationRequest in backend/src/routes/content_generation.py
- [X] T036 [US1] Implement background task execution for workflow orchestration in backend/src/routes/content_generation.py
- [X] T037 [US1] Add logging for workflow execution steps in backend/src/services/workflow_orchestrator.py
- [X] T038 [US1] Register content generation routes in backend/src/main.py

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently - API endpoint accepts requests, creates jobs, executes workflow, and returns status

---

## Phase 4: User Story 2 - Error Handling Integration (Priority: P2)

**Goal**: Integrate error handling and edge case handling modules into content generation workflow

**Independent Test**: Simulate error scenarios (insufficient sources, component failures, edge cases) and verify error handlers are invoked, errors are logged, and user-friendly messages are returned

### Tests for User Story 2

- [X] T039 [P] [US2] Test error handler invocation for insufficient sources in backend/tests/test_workflow_orchestrator.py
- [X] T040 [P] [US2] Test error handler invocation for component failures in backend/tests/test_workflow_orchestrator.py
- [X] T041 [P] [US2] Test edge case handler invocation in backend/tests/test_workflow_orchestrator.py
- [X] T042 [P] [US2] Test error logging and user notification in backend/tests/test_workflow_orchestrator.py

### Implementation for User Story 2

- [X] T043 [US2] Import and integrate error-handler.py module in backend/src/services/workflow_orchestrator.py
- [X] T044 [US2] Import and integrate edge-case-handler.py module in backend/src/services/workflow_orchestrator.py
- [X] T045 [US2] Wrap Content Architect invocation with error handling in backend/src/services/workflow_orchestrator.py
- [X] T046 [US2] Wrap Lesson Template Generator invocation with error handling in backend/src/services/workflow_orchestrator.py
- [X] T047 [US2] Wrap Technical Writer invocation with error handling in backend/src/services/workflow_orchestrator.py
- [X] T048 [US2] Implement error handler invocation for insufficient sources (FR-008) in backend/src/services/workflow_orchestrator.py
- [X] T049 [US2] Implement fallback mechanisms for component failures in backend/src/services/workflow_orchestrator.py
- [X] T050 [US2] Integrate edge case detection and handling in workflow execution in backend/src/services/workflow_orchestrator.py
- [X] T051 [US2] Add error details to job status response in backend/src/routes/content_generation.py
- [X] T052 [US2] Implement user-friendly error messages in API responses in backend/src/routes/content_generation.py

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently - errors are handled gracefully with proper logging and notifications

---

## Phase 5: User Story 3 - Validation Integration (Priority: P3)

**Goal**: Automatically execute validation scripts during content generation to verify content quality

**Independent Test**: Generate content and verify validation scripts (word count, source validation) are executed automatically and results are reported in job status

### Tests for User Story 3

- [X] T053 [P] [US3] Test word count validation execution in backend/tests/test_validation_service.py
- [X] T054 [P] [US3] Test source validation execution in backend/tests/test_validation_service.py
- [X] T055 [P] [US3] Test validation failure handling (block RAG indexing) in backend/tests/test_validation_service.py
- [X] T056 [P] [US3] Test validation results in job status response in backend/tests/test_content_generation_api.py

### Implementation for User Story 3

- [X] T057 [US3] Implement ValidationService wrapper in backend/src/services/validation_service.py
- [X] T058 [US3] Integrate validate-word-count.py script execution in backend/src/services/validation_service.py
- [X] T059 [US3] Integrate validate-sources.py script execution in backend/src/services/validation_service.py
- [X] T060 [US3] Parse validation script outputs and create ValidationResult models in backend/src/services/validation_service.py
- [X] T061 [US3] Integrate validation service into workflow orchestrator after content generation in backend/src/services/workflow_orchestrator.py
- [X] T062 [US3] Implement validation failure handling (block RAG indexing, preserve files, flag as "validation_failed") in backend/src/services/workflow_orchestrator.py
- [X] T063 [US3] Add validation results to job status response in backend/src/routes/content_generation.py
- [X] T064 [US3] Add validation error details to job status when validation fails in backend/src/routes/content_generation.py

**Checkpoint**: At this point, User Stories 1, 2, AND 3 should all work independently - validation scripts execute automatically and results are reported

---

## Phase 6: User Story 4 - Frontend-Backend Content Sync (Priority: P4)

**Goal**: Ensure newly generated content is immediately available in frontend and searchable in RAG chatbot

**Independent Test**: Generate content through API, verify it appears in frontend navigation and is searchable in RAG chatbot

### Tests for User Story 4

- [X] T065 [P] [US4] Test RAG indexing integration in backend/tests/test_integration.py
- [X] T066 [P] [US4] Test frontend sync service in backend/tests/test_sync_service.py
- [X] T067 [P] [US4] Test RAG indexing failure handling (preserve files, mark as "indexing_failed") in backend/tests/test_sync_service.py
- [X] T068 [P] [US4] Test content searchability in RAG chatbot after indexing in backend/tests/test_integration.py

### Implementation for User Story 4

- [X] T069 [US4] Implement SyncService for frontend-backend content synchronization in backend/src/services/sync_service.py
- [X] T070 [US4] Integrate ContentIndexingService for RAG indexing in backend/src/services/sync_service.py
- [X] T071 [US4] Implement RAG indexing after successful content generation and validation in backend/src/services/workflow_orchestrator.py
- [X] T072 [US4] Implement RAG indexing failure handling (preserve files, mark as "indexing_failed", allow manual retry) in backend/src/services/sync_service.py
- [X] T073 [US4] Implement frontend content structure validation in backend/src/services/sync_service.py
- [X] T074 [US4] Add indexing status to job status response in backend/src/routes/content_generation.py
- [X] T075 [US4] Add sync status to job status response in backend/src/routes/content_generation.py
- [X] T076 [US4] Implement partial failure handling (index successful lessons, report failed ones) in backend/src/services/workflow_orchestrator.py
- [X] T077 [US4] Add content locations to job results in backend/src/routes/content_generation.py

**Checkpoint**: At this point, all user stories should work independently - content is generated, validated, indexed, and available in frontend

---

## Phase 7: Additional Features

**Goal**: Implement job cancellation and enhance job status tracking

- [X] T078 [P] Implement POST /api/content/generate/{job_id}/cancel endpoint in backend/src/routes/content_generation.py
- [X] T079 [P] Implement job cancellation logic in backend/src/services/workflow_orchestrator.py
- [X] T080 [P] Add job cancellation tests in backend/tests/test_content_generation_api.py
- [X] T081 [P] Implement job expiration and cleanup (24 hours) in backend/src/utils/workflow_utils.py
- [X] T082 [P] Add rate limiting for content generation endpoint using existing middleware in backend/src/routes/content_generation.py

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T083 [P] Add comprehensive error handling for all edge cases in backend/src/services/workflow_orchestrator.py
- [X] T084 [P] Add performance monitoring and metrics logging in backend/src/services/workflow_orchestrator.py
- [X] T085 [P] Update API documentation with content generation endpoints in backend/src/main.py
- [X] T086 [P] Add request/response examples to quickstart.md validation
- [X] T087 [P] Code cleanup and refactoring across all workflow integration files
- [X] T088 [P] Add integration tests for end-to-end workflow execution in backend/tests/test_integration.py
- [X] T089 [P] Verify all success criteria (SC-001 to SC-008) are met
- [X] T090 [P] Run quickstart.md validation and update if needed

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-6)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3 → P4)
- **Additional Features (Phase 7)**: Depends on US1 completion
- **Polish (Phase 8)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Integrates with US1 components but independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Integrates with US1/US2 but independently testable
- **User Story 4 (P4)**: Can start after Foundational (Phase 2) - Integrates with US1/US3 but independently testable

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks (T001-T008) can run in parallel
- All Foundational model tasks marked [P] (T009-T020) can run in parallel
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together:
Task: T024 - Contract test for POST /api/content/generate endpoint
Task: T025 - Contract test for GET /api/content/generate/{job_id} endpoint
Task: T026 - Integration test for content generation workflow execution
Task: T027 - Test concurrent request rejection (HTTP 429)

# After tests are written and failing, launch implementation:
Task: T028 - Implement WorkflowOrchestrator service
Task: T032 - Implement POST /api/content/generate endpoint
Task: T033 - Implement GET /api/content/generate/{job_id} endpoint
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Add User Story 4 → Test independently → Deploy/Demo
6. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (MVP)
   - Developer B: User Story 2
   - Developer C: User Story 3
   - Developer D: User Story 4
3. Stories complete and integrate independently

---

## Task Summary

**Total Tasks**: 90
- **Phase 1 (Setup)**: 8 tasks
- **Phase 2 (Foundational)**: 15 tasks
- **Phase 3 (US1 - MVP)**: 15 tasks (4 tests + 11 implementation)
- **Phase 4 (US2)**: 14 tasks (4 tests + 10 implementation)
- **Phase 5 (US3)**: 12 tasks (4 tests + 8 implementation)
- **Phase 6 (US4)**: 13 tasks (4 tests + 9 implementation)
- **Phase 7 (Additional)**: 5 tasks
- **Phase 8 (Polish)**: 8 tasks

**Parallel Opportunities**: 
- 8 tasks in Setup phase
- 12 model tasks in Foundational phase
- 4 test tasks per user story
- User stories can be worked on in parallel after Foundational

**Suggested MVP Scope**: Phase 1 + Phase 2 + Phase 3 (User Story 1) = 38 tasks

---

## Notes

- [P] tasks = different files, no dependencies
- [US1], [US2], [US3], [US4] labels map tasks to specific user stories for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
- All file paths are relative to repository root
- Existing services (ContentIndexingService, auth_service, rate_limiter) should be reused
- Existing scripts (error-handler.py, edge-case-handler.py, validate-*.py) should be imported and integrated

