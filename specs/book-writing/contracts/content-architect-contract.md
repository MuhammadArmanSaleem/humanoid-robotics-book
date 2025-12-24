# Content Architect Contract

**Component**: Content Architect Subagent
**Version**: 1.0.0
**Date**: 2025-12-15
**Integration**: Textbook Content Generation Workflow

## Overview

The Content Architect subagent provides the foundational scaffolding for textbook content generation. It creates the directory structure, lesson templates, and configuration files needed for the Docusaurus textbook.

## Interface Contract

### Input Specification
```
Input Format: Plain text with chapter and lesson specifications
Example: "chapters 1-3, lessons 1-2"
Alternative: "chapters 1,3,5, lessons 1-4"
```

**Required Input Format**:
- `chapters X-Y` or `chapters X,Y,Z` - Specifies which chapters to generate
- `lessons X-Y` or `lessons X,Y,Z` - Specifies which lessons to generate per chapter
- If lessons not specified, defaults to all lessons

### Output Guarantees

#### Directory Structure
**Given**: Valid chapter/lesson specification
**When**: Content Architect executes successfully
**Then**: Creates directory structure at `docs/docs/chapter-{N}-{slug}/` with:
- Chapter directories for each specified chapter
- Lesson files for each specified lesson within chapters
- Category.json files for each chapter
- Updates sidebars.ts with new entries

#### File Generation
**Given**: COURSE_CONTENT.md exists with chapter/lesson structure
**When**: Content Architect processes specification
**Then**: Generates:
- N chapter directories (where N = number of specified chapters)
- M lesson files per chapter (where M = number of specified lessons)
- N category.json files (one per chapter)
- Updated sidebars.ts with all new entries

### Performance Contract
- **Execution Time**: < 10 minutes for 3 chapters × 2 lessons
- **Resource Usage**: < 100MB memory during execution
- **Reliability**: 99% success rate with proper input

### Error Handling Contract
- `COURSE_CONTENT.md not found`: Returns descriptive error message
- `docs/docs/ directory missing`: Creates directory or returns error
- `Permission denied`: Returns clear permission error
- `Invalid input format`: Returns example of correct format

### Integration Contract with Workflow
**Given**: Content Architect completes successfully
**Then**:
- Lesson Template Generator is automatically invoked for each lesson
- Directory structure is ready for Technical Writer agent
- Sidebars.ts is properly updated for navigation

## Functional Guarantees

### Scaffolding Guarantee
**Given**: Valid input specification
**When**: User runs Content Architect
**Then**: Creates complete directory structure with proper Docusaurus formatting

### Template Generation Guarantee
**Given**: Lesson files are created
**When**: Content Architect completes
**Then**: Each lesson file contains 7-section template structure with proper frontmatter

### Configuration Guarantee
**Given**: Chapter directories exist
**When**: Content Architect completes
**Then**: Each chapter has proper category.json and sidebars.ts is updated

## Backward Compatibility
- Generated directory structure compatible with Docusaurus v3
- Frontmatter format follows Docusaurus standards
- Sidebar entries maintain existing customizations
- File naming follows SEO-friendly patterns

## Validation Requirements
- Generated files must pass Docusaurus build validation
- JSON files must have valid syntax
- TypeScript files must have valid syntax
- Directory structure must follow Docusaurus conventions