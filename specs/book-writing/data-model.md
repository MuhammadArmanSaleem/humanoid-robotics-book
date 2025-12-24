# Data Model: Textbook Content Generation

**Feature**: Textbook Content Generation
**Date**: 2025-12-15
**Entities**: Chapter, Lesson, Section, Subsection, ResearchOutline, ConceptSummary, Example, Source

## Entity: Chapter

**Definition**: Represents a major section of the textbook containing multiple lessons

**Attributes**:
- `number`: Integer (1-100) - Sequential chapter identifier
- `title`: String (max 100 chars) - Human-readable chapter name
- `description`: String (max 500 chars) - Brief chapter overview
- `lessons`: Array[Lesson] - Collection of lessons within this chapter
- `slug`: String (auto-generated) - URL-friendly identifier
- `status`: Enum - "scaffolding", "templated", "content-generated", "reviewed"

**Validation Rules**:
- Number must be positive integer
- Title must not be empty
- Title must be unique within course
- Number must be sequential (no gaps)
- Status transitions must follow proper sequence

**State Transitions**:
- `scaffolding` → `templated` (when templates applied)
- `templated` → `content-generated` (when content added)
- `content-generated` → `reviewed` (when reviewed)

## Entity: Lesson

**Definition**: Represents a subsection within a chapter containing ~800 words of technical content

**Attributes**:
- `number`: Integer (1-50) - Sequential lesson identifier within chapter
- `title`: String (max 100 chars) - Human-readable lesson name
- `description`: String (max 300 chars) - Brief lesson overview
- `content`: String (800±50 words) - Main lesson content with technical depth
- `sections`: Array[Section] - Required sections (Introduction, Learning Objectives, etc.)
- `slug`: String (auto-generated) - URL-friendly identifier
- `frontmatter`: Object - Docusaurus frontmatter properties
- `status`: Enum - "template", "researched", "full_content", "reviewed"
- `research_sources`: Array[Source] - Authoritative sources used

**Validation Rules**:
- Number must be positive integer within chapter
- Title must not be empty
- Title must be unique within chapter
- Content must be between 750-850 words
- All required sections must be present
- Number must be sequential (no gaps)
- Research sources must be from authoritative domains

**State Transitions**:
- `template` → `researched` (when research applied)
- `researched` → `full_content` (when content generated)
- `full_content` → `reviewed` (when reviewed)

## Entity: Section

**Definition**: Represents a structured part of a lesson (Introduction, Learning Objectives, etc.)

**Attributes**:
- `type`: Enum - "introduction", "learning_objectives", "key_concepts", "hands_on", "quiz", "takeaways", "further_reading"
- `title`: String - Section title
- `content`: String - Section content
- `order`: Integer - Position in lesson sequence
- `subsection`: Array[Subsection] - Optional detailed subsections

**Validation Rules**:
- Type must be one of defined enum values
- Title must not be empty
- Order must be sequential within lesson
- Content must be appropriate for section type

**State Transitions**: N/A (immutable after creation)

## Entity: Subsection

**Definition**: Represents a detailed subsection within a section (for complex technical topics)

**Attributes**:
- `title`: String - Subsection title
- `content`: String - Subsection content
- `order`: Integer - Position in section sequence
- `parent_section`: Section - Reference to parent section

**Validation Rules**:
- Title must not be empty
- Order must be sequential within parent section
- Must have valid parent section reference

**State Transitions**: N/A (immutable after creation)

## Entity: ResearchOutline

**Definition**: Structured plan for research topics to be covered in a lesson

**Attributes**:
- `lesson_id`: String - Reference to associated lesson
- `key_concepts`: Array[String] - Technical concepts to cover
- `examples`: Array[Example] - Technical examples to include
- `sources`: Array[Source] - Authoritative sources to use
- `research_notes`: String - Additional research guidance

**Validation Rules**:
- Must have valid lesson reference
- Key concepts must be technically relevant
- Sources must be from authoritative domains
- Examples must be current and relevant

**State Transitions**: N/A (generated once per lesson)

## Entity: ConceptSummary

**Definition**: Brief explanation of a technical concept for educational clarity

**Attributes**:
- `concept_name`: String - Name of the concept
- `definition`: String - Clear definition
- `importance`: Enum - "foundational", "important", "advanced"
- `related_concepts`: Array[String] - Related concepts
- `examples`: Array[String] - Practical examples

**Validation Rules**:
- Concept name must be unique within lesson
- Definition must be clear and concise
- Importance level must be appropriate
- Related concepts must exist

**State Transitions**: N/A (immutable after creation)

## Entity: Example

**Definition**: Technical example demonstrating a concept or principle

**Attributes**:
- `name`: String - Example identifier
- `description`: String - What the example demonstrates
- `code`: String - Optional code snippet (if applicable)
- `application`: String - How it applies to the lesson topic
- `source`: Source - Where the example originates from

**Validation Rules**:
- Name must be unique within lesson
- Description must be clear
- Code must be syntactically valid if present
- Source must be verifiable

**State Transitions**: N/A (immutable after creation)

## Entity: Source

**Definition**: Authoritative source used for research and content generation

**Attributes**:
- `url`: String - HTTPS URL to the source
- `title`: String - Title of the source
- `author`: String - Author or organization
- `date`: Date - Publication or last updated date
- `relevance`: Enum - "high", "medium", "low" for current lesson
- `verification_status`: Enum - "verified", "pending", "unverified"

**Validation Rules**:
- URL must be valid HTTPS
- Title must not be empty
- Verification status must be current
- Domain must be authoritative (edu, org, official company sites)

**State Transitions**:
- `pending` → `verified` (when source verified)
- `pending` → `unverified` (when source invalid)

## Relationships

### Chapter → Lesson
- One-to-Many: One chapter contains many lessons
- Mandatory: Each lesson belongs to exactly one chapter
- Cascade: When chapter status updates, lessons follow appropriately

### Lesson → Section
- One-to-Many: One lesson contains many sections
- Mandatory: Each section belongs to exactly one lesson
- Validation: All required sections must be present

### Section → Subsection
- One-to-Many: One section contains many subsections (optional)
- Optional: Sections may not have subsections
- Validation: Subsections follow proper ordering

### Lesson → ResearchOutline
- One-to-One: One lesson has one research outline
- Mandatory: Each lesson must have research outline
- Synchronization: Research outline guides content generation

### Lesson → Source
- One-to-Many: One lesson references many sources
- Validation: All sources must be authoritative
- Quality: Sources must have "high" or "medium" relevance

### ResearchOutline → Example
- One-to-Many: One research outline includes many examples
- Validation: Examples must be current and relevant
- Technical: Examples must demonstrate key concepts

## Constraints

### Content Constraints
- Lesson content: 750-850 words range
- Section count: Minimum 5 required sections per lesson
- Source count: Minimum 3 authoritative sources per lesson
- Example count: Minimum 2 technical examples per lesson

### Quality Constraints
- All sources must be from authoritative domains (.edu, .org, official company sites)
- Content must maintain technical accuracy while being educationally accessible
- Examples must be current (from last 5 years) for robotics technology
- Research must include both foundational concepts and recent developments

### Workflow Constraints
- State transitions must follow proper sequence (template → researched → full_content → reviewed)
- Content generation must complete within time budget (45 minutes for 6 lessons)
- All validation rules must pass before status transition
- Manual review required before "reviewed" status