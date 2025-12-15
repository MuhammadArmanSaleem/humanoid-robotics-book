# Data Model: Content Architect Subagent

**Feature**: Content Architect Subagent
**Date**: 2025-12-15
**Entities**: Chapter, Lesson, CourseContent, CategoryConfig, SidebarConfig

## Entity: Chapter

**Definition**: Represents a major section of the textbook containing multiple lessons

**Attributes**:
- `number`: Integer (1-100) - Sequential chapter identifier
- `title`: String (max 100 chars) - Human-readable chapter name
- `description`: String (max 500 chars) - Brief chapter overview
- `lessons`: Array[Lesson] - Collection of lessons within this chapter
- `slug`: String (auto-generated) - URL-friendly identifier

**Validation Rules**:
- Number must be positive integer
- Title must not be empty
- Title must be unique within course
- Number must be sequential (no gaps)

**State Transitions**: N/A (immutable after creation)

## Entity: Lesson

**Definition**: Represents a subsection within a chapter containing educational content

**Attributes**:
- `number`: Integer (1-50) - Sequential lesson identifier within chapter
- `title`: String (max 100 chars) - Human-readable lesson name
- `description`: String (max 300 chars) - Brief lesson overview
- `sections`: Array[String] - Required sections (Learning Objectives, Introduction, Content, Summary, Exercises)
- `slug`: String (auto-generated) - URL-friendly identifier
- `frontmatter`: Object - Docusaurus frontmatter properties

**Validation Rules**:
- Number must be positive integer within chapter
- Title must not be empty
- Title must be unique within chapter
- All required sections must be present in content
- Number must be sequential (no gaps)

**State Transitions**: N/A (immutable after creation)

## Entity: CourseContent

**Definition**: The input specification document that defines the textbook structure

**Attributes**:
- `source_file`: String - Path to COURSE_CONTENT.md
- `chapters`: Array[Chapter] - Parsed chapter specifications
- `metadata`: Object - Course-level metadata and configuration
- `validation_status`: Enum - Valid, Invalid, ParsingError

**Validation Rules**:
- Must contain at least one valid chapter specification
- Must follow expected structure format
- Chapter numbers must be sequential
- All required fields must be present

**State Transitions**:
- `Parsing` → `Valid` (when parsing succeeds)
- `Parsing` → `Invalid` (when validation fails)
- `Invalid` → `Valid` (when corrected and re-parsed)

## Entity: CategoryConfig

**Definition**: JSON configuration file that defines chapter-level settings for Docusaurus documentation

**Attributes**:
- `label`: String - Display name for the chapter
- `position`: Integer - Order in navigation
- `collapsible`: Boolean - Whether chapter can be collapsed in sidebar
- `collapsed`: Boolean - Default collapsed state
- `link`: Object - Optional link to external resource
- `className`: String - CSS class for styling

**Validation Rules**:
- Label must not be empty
- Position must be positive integer
- Must generate valid JSON format
- Must be compatible with Docusaurus v3

**State Transitions**: N/A (generated from Chapter entity)

## Entity: SidebarConfig

**Definition**: TypeScript configuration that defines the navigation structure for the Docusaurus site

**Attributes**:
- `items`: Array[Object] - Navigation items (chapters and lessons)
- `type`: String - Configuration type (always "category" for chapters)
- `label`: String - Display name
- `items`: Array[String|Object] - Child navigation items
- `collapsed`: Boolean - Default collapsed state

**Validation Rules**:
- Must maintain valid TypeScript syntax
- Must preserve existing manual customizations
- Must reference actual generated files
- Must follow Docusaurus v3 schema

**State Transitions**: N/A (updated from CourseContent and generated structure)

## Relationships

### Chapter → Lesson
- One-to-Many: One chapter contains many lessons
- Mandatory: Each lesson belongs to exactly one chapter
- Cascade: When chapter is removed, all lessons are removed

### CourseContent → Chapter
- One-to-Many: One course content specification contains many chapters
- Mandatory: Each chapter belongs to exactly one course content
- Validation: CourseContent validates all chapters

### Chapter → CategoryConfig
- One-to-One: One chapter generates one category configuration
- Derived: CategoryConfig is generated from Chapter data
- Synchronization: Changes to Chapter affect CategoryConfig

### CourseContent → SidebarConfig
- One-to-One: One course content updates one sidebar configuration
- Aggregation: SidebarConfig aggregates all chapters and lessons
- Preservation: Manual sidebar customizations are preserved

## Constraints

### Structural Constraints
- Maximum 100 chapters per course
- Maximum 50 lessons per chapter
- Maximum 1000 total lessons per course
- Unique slugs across all entities

### Validation Constraints
- All generated files must pass Docusaurus validation
- Configuration files must maintain backward compatibility
- Manual customizations must be preserved during updates
- Generated content must follow SEO best practices

### Performance Constraints
- Parsing must complete in under 10 seconds for typical content
- Generation must complete in under 30 seconds for 100 chapters
- Memory usage must remain under 200MB during operations