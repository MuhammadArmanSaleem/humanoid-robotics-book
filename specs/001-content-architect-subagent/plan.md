# Implementation Plan: Content Architect Subagent

**Branch**: `001-content-architect-subagent` | **Date**: 2025-12-15 | **Spec**: [specs/001-content-architect-subagent/spec.md](spec.md)
**Input**: Feature specification from `/specs/001-content-architect-subagent/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

The Content Architect Subagent will implement a command-line tool that reads COURSE_CONTENT.md and automatically generates the complete Docusaurus textbook structure for 3 chapters with 2 lessons each. The implementation will focus on file system operations, parsing, and Docusaurus configuration generation while maintaining idempotent execution and preserving manual customizations.

## Technical Context

**Language/Version**: Python 3.11 (aligns with constitution's FastAPI requirement and Claude Code integration)
**Primary Dependencies**: PyYAML (for parsing configuration), markdown (for processing), pathlib (for file operations), json (for configuration generation)
**Storage**: File system-based (no database needed - operates on markdown and configuration files)
**Testing**: pytest (aligns with constitution's testing requirements)
**Target Platform**: Cross-platform (Linux, macOS, Windows) for developer workflow
**Project Type**: Single CLI tool project (determines source structure)
**Performance Goals**: Generate complete textbook structure (3 chapters × 2 lessons = 6 lessons) in under 30 seconds
**Constraints**: <200MB memory usage, support for 100+ concurrent file operations, maintain SEO-friendly URL patterns
**Scale/Scope**: Support up to 100 chapters and 1000 lessons with proper directory organization

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Content-First Development**: Implementation will prioritize educational quality by ensuring proper pedagogical structure in generated content
- **AI-Assisted Spec-Driven Workflow**: Following Spec-Kit Plus methodology as mandated by constitution
- **Progressive Enhancement Architecture**: This subagent supports the base Docusaurus textbook implementation (Phase 1 requirement)
- **Reusable Intelligence**: This is a Claude Code Subagent as required by constitution for +50 bonus points
- **Technical Stack Compliance**: Using Python (aligns with FastAPI ecosystem in constitution)
- **Zero-Cost Architecture**: File-based operations with no external dependencies beyond standard libraries
- **Test-Before-Implement**: Test coverage >80% for base features as required

## Project Structure

### Documentation (this feature)

```text
specs/001-content-architect-subagent/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
src/
├── content_architect/
│   ├── __init__.py
│   ├── main.py          # CLI entry point
│   ├── parser.py        # COURSE_CONTENT.md parsing logic
│   ├── generator.py     # Directory and file generation logic
│   ├── docusaurus.py    # Docusaurus-specific configuration generation
│   └── utils.py         # Utility functions
├── cli/
│   └── content_architect_cli.py  # Command-line interface
└── tests/
    ├── unit/
    │   ├── test_parser.py
    │   ├── test_generator.py
    │   └── test_docusaurus.py
    ├── integration/
    │   └── test_end_to_end.py
    └── fixtures/
        └── sample_course_content.md
```

**Structure Decision**: Single CLI tool project structure selected to implement the Content Architect Subagent. This structure provides clear separation of concerns with dedicated modules for parsing, generation, and Docusaurus-specific functionality while maintaining testability.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Multi-module architecture | Clear separation of concerns for maintainability | Single-file approach would create unmaintainable monolith as feature complexity grows |
