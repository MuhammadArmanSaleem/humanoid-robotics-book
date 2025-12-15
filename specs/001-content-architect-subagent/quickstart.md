# Quickstart: Content Architect Subagent

**Feature**: Content Architect Subagent
**Version**: 1.0.0
**Date**: 2025-12-15

## Overview

The Content Architect Subagent is a command-line tool that automatically generates Docusaurus textbook structure from a COURSE_CONTENT.md specification. It creates chapters, lessons, configuration files, and standardized templates with a single command.

## Prerequisites

- Python 3.11 or higher
- pip package manager
- Access to the project directory with Docusaurus setup
- A valid COURSE_CONTENT.md file describing the textbook structure

## Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd <repository-name>
```

### 2. Set up Python Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install PyYAML pytest
```

### 3. Install the Content Architect Subagent
```bash
# Navigate to the project root
cd <project-root>

# Install in development mode
pip install -e .
```

## Basic Usage

### 1. Prepare COURSE_CONTENT.md
Create a COURSE_CONTENT.md file in the project root with your textbook structure:

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

### 2. Run the Content Architect Subagent
```bash
# Generate the textbook structure
python -m src.cli.content_architect_cli --input COURSE_CONTENT.md --output docs

# Or use the convenience script if available
./scripts/generate-textbook.sh
```

### 3. Verify the Generated Structure
After running the command, you should see:
```
docs/
├── chapter-1/
│   ├── lesson-1.md
│   ├── lesson-2.md
│   └── category.json
├── chapter-2/
│   ├── lesson-1.md
│   ├── lesson-2.md
│   └── category.json
├── chapter-3/
│   ├── lesson-1.md
│   ├── lesson-2.md
│   └── category.json
└── sidebars.ts (updated with new chapters/lessons)
```

## Configuration Options

### Command Line Arguments
```bash
python -m src.cli.content_architect_cli [OPTIONS]

Options:
  --input, -i TEXT        Input COURSE_CONTENT.md file (default: COURSE_CONTENT.md)
  --output, -o TEXT       Output directory (default: docs)
  --force, -f            Overwrite existing content (default: false)
  --preserve, -p         Preserve existing manual customizations (default: true)
  --validate, -v         Validate generated structure (default: true)
  --help, -h             Show help message
```

### Example with Options
```bash
# Generate with custom output directory
python -m src.cli.content_architect_cli --input my-course.md --output docs/textbook

# Force overwrite existing content
python -m src.cli.content_architect_cli --force

# Validate without generating
python -m src.cli.content_architect_cli --validate
```

## Generated Content Structure

### Lesson Template
Each generated lesson file includes standardized sections:
```markdown
---
title: "Lesson Title"
description: "Brief description of the lesson"
---

# Learning Objectives
- Understand [key concept 1]
- Apply [key concept 2]
- Analyze [key concept 3]

# Introduction
[Lesson introduction content]

# Content
[Main lesson content]

# Summary
[Lesson summary]

# Exercises
1. [Exercise 1]
2. [Exercise 2]
```

### Category Configuration
Each chapter directory includes a `category.json` file:
```json
{
  "label": "Chapter X: Chapter Title",
  "position": X,
  "collapsible": true,
  "collapsed": false
}
```

### Sidebar Configuration
The `sidebars.ts` file is updated with new navigation entries while preserving existing customizations.

## Advanced Usage

### Adding New Chapters
To add new chapters to an existing structure, simply update your COURSE_CONTENT.md and run the subagent again. It will add new chapters without modifying existing ones.

### Custom Templates
The subagent supports custom lesson templates. Place custom templates in `templates/lesson-custom.md` to override the default template.

### Validation
The subagent validates generated content against Docusaurus requirements:
```bash
# Run validation separately
python -m src.cli.content_architect_cli --validate
```

## Troubleshooting

### Common Issues

1. **Permission Error**: Ensure you have write permissions to the output directory
2. **Invalid Input**: Verify your COURSE_CONTENT.md follows the expected format
3. **Missing Dependencies**: Run `pip install PyYAML` if you encounter import errors

### Error Messages
- `File not found`: Check that COURSE_CONTENT.md exists in the specified location
- `Invalid structure`: Verify the markdown structure follows the expected format
- `Permission denied`: Check write permissions for the output directory

## Development

### Running Tests
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/unit/test_generator.py

# Run with coverage
pytest --cov=src
```

### Building Documentation
```bash
# Generate all documentation
./scripts/generate-docs.sh
```

## Next Steps

1. **Customize Content**: Fill in the generated lesson templates with actual course content
2. **Add Assets**: Include images, diagrams, and other resources in appropriate directories
3. **Configure Docusaurus**: Customize the Docusaurus theme and styling
4. **Deploy**: Build and deploy your textbook website

## Support

For issues or questions:
- Check the [troubleshooting](#troubleshooting) section
- Review the [full documentation](spec.md)
- Create an issue in the repository