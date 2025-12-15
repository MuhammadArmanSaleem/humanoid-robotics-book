# Content Architect Subagent API Contract

**Version**: 1.0.0
**Date**: 2025-12-15
**Feature**: Content Architect Subagent

## Overview

This contract defines the interface and behavior of the Content Architect Subagent, a command-line tool that generates Docusaurus textbook structure from COURSE_CONTENT.md specifications.

## Command-Line Interface

### Main Command
```
content-architect [OPTIONS]
```

### Input/Output Specifications

#### Input: COURSE_CONTENT.md
**Format**: Markdown with structured chapter/lesson hierarchy
**Schema**:
```markdown
# Course Title

## Chapter {number}: Chapter Title
### Lesson {number}: Lesson Title
[Optional lesson content or placeholder]
```

**Validation**:
- Must contain at least one chapter
- Chapters must follow "## Chapter X: Title" pattern
- Lessons must follow "### Lesson X: Title" pattern
- Chapter and lesson numbers must be sequential

#### Output: Directory Structure
**Location**: Specified output directory (default: `docs/`)
**Structure**:
```
output/
├── chapter-{number}/
│   ├── lesson-{number}.md
│   └── category.json
└── sidebars.ts
```

### Command Options

#### Input Configuration
```
--input, -i [FILEPATH]
  Path to input COURSE_CONTENT.md file
  Default: "COURSE_CONTENT.md"
  Required: No
```

#### Output Configuration
```
--output, -o [DIRECTORY]
  Output directory for generated content
  Default: "docs"
  Required: No
```

#### Behavior Options
```
--force, -f
  Overwrite existing content without confirmation
  Default: false
  Required: No

--preserve, -p
  Preserve existing manual customizations in configuration files
  Default: true
  Required: No

--validate, -v
  Validate generated structure after creation
  Default: true
  Required: No
```

## Functional Guarantees

### 1. Structure Generation Guarantee
**Given**: Valid COURSE_CONTENT.md with N chapters and M lessons per chapter
**When**: User runs `content-architect --input COURSE_CONTENT.md`
**Then**: Tool creates N chapter directories, each with M lesson files and proper category.json

### 2. Configuration Update Guarantee
**Given**: Existing sidebars.ts file with manual customizations
**When**: User runs content-architect with new content
**Then**: Tool updates sidebars.ts to include new content while preserving manual customizations

### 3. Idempotent Execution Guarantee
**Given**: Generated content structure exists
**When**: User runs content-architect multiple times with same input
**Then**: Tool produces identical output without duplicating entries or breaking existing content

### 4. Validation Guarantee
**Given**: Generated content structure
**When**: User runs with --validate flag
**Then**: Tool verifies all generated files follow Docusaurus v3 requirements

## Error Handling Contract

### Input Validation Errors
- **INVALID_INPUT_FILE**: COURSE_CONTENT.md not found or unreadable
  - Exit code: 1
  - Message: "Input file {path} not found or not readable"

- **INVALID_CONTENT_FORMAT**: COURSE_CONTENT.md format invalid
  - Exit code: 2
  - Message: "Content format invalid: {specific error}"

### Output Validation Errors
- **PERMISSION_DENIED**: Insufficient permissions to write to output directory
  - Exit code: 3
  - Message: "Insufficient permissions to write to {path}"

- **OUTPUT_CONFLICT**: Output directory conflicts with existing files
  - Exit code: 4
  - Message: "Output conflict: {details}"

### Runtime Errors
- **INTERNAL_ERROR**: Unexpected internal error
  - Exit code: 99
  - Message: "Internal error: {details}"

## Performance Contract

### Execution Time
- **Small Course** (≤ 5 chapters, ≤ 3 lessons each): < 10 seconds
- **Medium Course** (≤ 20 chapters, ≤ 5 lessons each): < 30 seconds
- **Large Course** (≤ 100 chapters, ≤ 10 lessons each): < 120 seconds

### Resource Usage
- **Memory**: < 200MB regardless of course size
- **Disk Space**: Output size + temporary files < 2x output size

## Data Format Contracts

### Generated Lesson Format
```markdown
---
title: "Lesson Title"
description: "Brief description"
---

# Learning Objectives
- Objective 1
- Objective 2

# Introduction
[Lesson introduction]

# Content
[Main content]

# Summary
[Lesson summary]

# Exercises
1. Exercise 1
2. Exercise 2
```

### Category Configuration Format
```json
{
  "label": "Chapter X: Title",
  "position": X,
  "collapsible": true,
  "collapsed": false
}
```

### Sidebar Entry Format
```typescript
{
  type: 'category',
  label: 'Chapter X: Title',
  items: ['chapter-X/lesson-1', 'chapter-X/lesson-2'],
  collapsed: false
}
```

## Backward Compatibility

### Versioning
- Minor versions: Add functionality without breaking existing behavior
- Major versions: May include breaking changes with migration path
- Patch versions: Bug fixes and performance improvements

### Migration
- Generated content remains compatible with Docusaurus v3
- Configuration files maintain TypeScript syntax compatibility
- File naming conventions remain stable across minor versions

## Testing Contract

### Required Test Coverage
- **Unit Tests**: 80%+ coverage of all modules
- **Integration Tests**: End-to-end validation of generation process
- **Performance Tests**: Validation of timing and resource constraints
- **Regression Tests**: Idempotent execution verification

### Test Scenarios
1. Valid input with minimal content
2. Valid input with maximum supported content
3. Invalid input formats
4. Edge cases (empty files, special characters, etc.)
5. Idempotent execution verification
6. Configuration preservation validation