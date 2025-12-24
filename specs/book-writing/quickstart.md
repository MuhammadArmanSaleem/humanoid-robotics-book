# Quickstart: Textbook Content Generation

**Feature**: Textbook Content Generation
**Version**: 1.0.0
**Date**: 2025-12-15

## Overview

The Textbook Content Generation workflow orchestrates existing components (Content Architect subagent, Lesson Template Generator skill, Technical Writer agent) to generate high-quality textbook content with proper technical research. This workflow focuses on generating content for Physical AI & Humanoid Robotics course with ~800 words per lesson.

## Prerequisites

- Claude Code environment with agent/skill support
- Existing components installed:
  - Content Architect subagent (.claude/agents/content-architect.md)
  - Lesson Template Generator skill (.claude/skills/lesson-template-generator/SKILL.md)
  - Technical Writer agent (.claude/agents/technical-writer.md)
- COURSE_CONTENT.md file describing the curriculum structure
- Basic understanding of the target audience (Physical AI & Robotics students)

## Installation & Setup

### 1. Verify Component Availability
```bash
# Check that required components exist
ls .claude/agents/content-architect.md
ls .claude/agents/technical-writer.md
ls .claude/skills/lesson-template-generator/SKILL.md
```

### 2. Prepare Course Content Specification
Create a COURSE_CONTENT.md file with your curriculum structure:

```markdown
# Physical AI & Humanoid Robotics Course

## Chapter 1: Introduction to Physical AI
### Lesson 1: What is Physical AI?
### Lesson 2: History and Evolution

## Chapter 2: Fundamentals of Humanoid Robotics
### Lesson 1: Kinematics and Motion
### Lesson 2: Control Systems

## Chapter 3: Advanced Topics
### Lesson 1: AI Integration
### Lesson 2: Future Directions
```

### 3. Set up Directory Structure
```bash
mkdir -p docs/docs
touch docs/sidebars.ts
```

## Basic Usage

### 1. Run Content Scaffolding
```bash
# Generate basic structure using Content Architect
claude agent content-architect << EOF
chapters 1-3, lessons 1-2
EOF
```

### 2. Generate Lesson Templates
The Content Architect will automatically invoke the Lesson Template Generator to create standardized 7-section templates for each lesson.

### 3. Generate Technical Content
For each lesson that needs content generation, use the Technical Writer agent with research guidance:

```bash
# Example for Lesson 1.1: Introduction to Embodied Intelligence
claude agent technical-writer << EOF
Generate ~800 words of technical content about embodied intelligence.
Key concepts: embodied intelligence definition, sensor-motor integration, physical constraints.
Examples: Tesla Optimus, Figure 01, 1X Neo, Boston Dynamics Atlas.
Sources: Pfeifer & Bongard book, Brooks 1991 paper, official robot documentation.
Target: Educational content for Physical AI students.
EOF
```

## Workflow Orchestration

### Complete Generation Workflow
```bash
# Step 1: Generate scaffolding (10 minutes)
claude agent content-architect << EOF
chapters 1-3, lessons 1-2
EOF

# Step 2: Templates are automatically generated (5 minutes)

# Step 3: Generate content for priority lessons (21 minutes)
# For each lesson, run Technical Writer with specific research guidance
claude agent technical-writer << EOF
Generate ~800 words about ROS 2 architecture for lesson 2.1.
Key concepts: ROS 2 middleware, publish-subscribe, services/actions.
Examples: Unitree H1, NASA Valkyrie, Agility Robotics Digit.
Sources: ROS 2 docs, Navigation2 docs, Quigley paper.
EOF

# Step 4: Review and validate content
# Manually review generated content for technical accuracy
```

### Research-Guided Content Generation
For each lesson, provide specific research guidance to the Technical Writer:

```bash
# Example for Gazebo simulation lesson
claude agent technical-writer << EOF
Generate ~800 words about Gazebo simulation setup for lesson 3.1.
Key concepts: Physics simulation, SDF/URDF, sensor simulation.
Examples: NASA workflows, Unitree development, RoboCup standards.
Sources: Gazebo docs, academic papers, source code documentation.
Target: Practical setup guide with technical depth.
EOF
```

## Verification Checklist

### Content Quality Verification
- [ ] Each lesson contains 750-850 words of technical content
- [ ] Content includes specific technical examples (Tesla Optimus, etc.)
- [ ] At least 3 authoritative sources referenced per lesson
- [ ] Technical accuracy verified (concepts properly explained)
- [ ] Educational accessibility maintained (complex topics explained clearly)

### Structure Verification
- [ ] All 6 lessons (3 chapters × 2 lessons) generated
- [ ] Each lesson has 7 required sections (Introduction, Learning Objectives, etc.)
- [ ] Proper frontmatter included in each lesson file
- [ ] Category.json files created for each chapter
- [ ] Sidebars.ts updated with new content structure

### Research Verification
- [ ] Content includes current examples (from 2023-2025)
- [ ] Authoritative sources properly cited (edu, org, official sites)
- [ ] Technical concepts explained with practical applications
- [ ] Both foundational and advanced concepts covered appropriately

## Troubleshooting

### Common Issues

1. **Missing Components**: If agents/skills not found
   - Verify .claude/ directory structure
   - Check component file paths exist

2. **Content Generation Issues**: If Technical Writer fails
   - Verify research guidance is specific enough
   - Check that sources are accessible and authoritative

3. **Template Generation Issues**: If templates not created
   - Ensure Content Architect properly invokes Lesson Template Generator
   - Check skill configuration

### Error Messages
- `Component not found`: Check that all required agents/skills exist
- `Content too short/long`: Adjust Technical Writer prompts for word count
- `Invalid sources`: Ensure all research sources are from authoritative domains
- `Template missing sections`: Verify Lesson Template Generator configuration

## Performance Guidelines

### Time Estimates
- Content Architect scaffolding: ~10 minutes
- Template generation: ~5 minutes (6 lessons)
- Technical content generation: ~7 minutes per lesson
- Manual review: ~5 minutes per lesson
- **Total estimated time**: ~41 minutes for complete workflow

### Optimization Tips
- Focus on priority lessons first (1.1, 2.1, 3.1)
- Use parallel processing where possible for content generation
- Prepare research guidance in advance to speed up Technical Writer
- Review content incrementally rather than waiting for complete generation

## Advanced Usage

### Custom Research Guidance
For specialized content needs, provide detailed research guidance:

```bash
claude agent technical-writer << EOF
Generate technical content for [specific lesson].
Key concepts: [list specific concepts]
Examples: [list specific, current examples]
Sources: [list authoritative sources with URLs]
Technical depth: [educational vs. implementation focus]
Target audience: [student level: beginner/intermediate/advanced]
Word count: [specific range if different from 800]
EOF
```

### Quality Assurance Process
1. Generate content with Technical Writer
2. Verify against authoritative sources
3. Check technical accuracy with domain knowledge
4. Ensure educational accessibility
5. Validate structure and formatting

## Next Steps

1. **Begin Generation**: Start with priority lessons (1.1, 2.1, 3.1)
2. **Review Content**: Validate technical accuracy and educational value
3. **Expand Coverage**: Generate content for remaining lessons
4. **Quality Assurance**: Conduct SME review of all content
5. **Deployment**: Integrate into Docusaurus textbook structure

## Support

For issues or questions:
- Check the [troubleshooting](#troubleshooting) section
- Review the [full specification](spec.md)
- Verify all components are properly installed
- Ensure research guidance is specific and authoritative