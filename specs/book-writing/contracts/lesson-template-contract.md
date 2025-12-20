# Lesson Template Generator Contract

**Component**: Lesson Template Generator Skill
**Version**: 1.0.0
**Date**: 2025-12-15
**Integration**: Textbook Content Generation Workflow

## Overview

The Lesson Template Generator skill creates standardized 7-section lesson templates that serve as the foundation for technical content generation. Each template follows a consistent structure to ensure educational quality and pedagogical effectiveness.

## Interface Contract

### Input Specification
```
Input Format: Template parameters with lesson metadata
Example: { "lesson_title": "Introduction to Embodied Intelligence", "chapter_title": "Physical AI Fundamentals", "target_words": 800 }
```

**Required Input Parameters**:
- `lesson_title`: String - Title of the lesson
- `chapter_title`: String - Title of the parent chapter
- `target_words`: Integer - Expected word count (~800)

### Output Guarantees

#### Template Structure
**Given**: Valid lesson metadata
**When**: Lesson Template Generator executes successfully
**Then**: Creates lesson file with exactly 7 sections:
1. Introduction
2. Learning Objectives (3 action-oriented bullets)
3. Key Concepts (3 subsections with ### headers)
4. Hands-on Exercise (Prerequisites, Steps 1-3, Expected Outcome)
5. Quiz (3 multiple-choice questions with answers)
6. Key Takeaways (3 bullet points)
7. Further Reading (3 resources + Next Lesson link)

#### Frontmatter Generation
**Given**: Lesson template is created
**When**: Template Generator completes
**Then**: Includes proper Docusaurus frontmatter with:
- `title`: Lesson title
- `description`: Brief lesson description
- `sidebar_position`: Appropriate position in chapter
- Additional metadata as needed

### Performance Contract
- **Execution Time**: < 2 minutes per lesson template
- **Resource Usage**: < 50MB memory during execution
- **Reliability**: 100% success rate with valid input

### Error Handling Contract
- `Missing lesson_title`: Returns error requesting required parameter
- `Invalid target_words`: Returns error with valid range (e.g., 700-900)
- `Template generation failure`: Returns descriptive error with troubleshooting steps

### Integration Contract with Workflow
**Given**: Content Architect creates lesson file
**When**: Lesson Template Generator is invoked
**Then**:
- 7-section template is written to lesson file
- File is ready for Technical Writer agent
- Proper frontmatter is included for Docusaurus

## Functional Guarantees

### Standardization Guarantee
**Given**: Lesson template is generated
**When**: Template Generator executes
**Then**: All 7 required sections are present in correct order with appropriate headers

### Educational Quality Guarantee
**Given**: Template generation request
**When**: Lesson Template Generator processes request
**Then**: Learning objectives are action-oriented and measurable

### Content Readiness Guarantee
**Given**: Template is completed
**When**: Template Generator finishes
**Then**: File structure is ready for technical content insertion

## Section-Specific Requirements

### Learning Objectives Section
- Must contain exactly 3 bullet points
- Each objective must start with an action verb (understand, apply, analyze, etc.)
- Objectives must be measurable and specific

### Key Concepts Section
- Must contain exactly 3 subsections
- Each subsection uses ### header format
- Content areas must be technically relevant to lesson topic

### Hands-on Exercise Section
- Must include Prerequisites subsection
- Must include Steps 1-3 with clear instructions
- Must include Expected Outcome subsection

### Quiz Section
- Must contain exactly 3 multiple-choice questions
- Each question must have 4 options (A-D)
- Must include answer key or explanation

## Backward Compatibility
- Template structure compatible with Docusaurus markdown requirements
- Section headers follow standard markdown formatting
- Frontmatter format follows Docusaurus standards
- File structure allows for easy content updates

## Validation Requirements
- Generated templates must render properly in Docusaurus
- All 7 sections must be present and properly formatted
- Frontmatter must follow Docusaurus schema
- Section headers must use correct markdown syntax