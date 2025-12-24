#!/usr/bin/env python3
"""
Word Count Validation Script
Validates that lesson content is within 750-850 word range (T087)
"""

import re
import sys
from pathlib import Path


def count_words(text):
    """Count words in text, excluding frontmatter and code blocks"""
    # Remove frontmatter (between --- markers)
    text = re.sub(r'^---.*?---\s*', '', text, flags=re.DOTALL | re.MULTILINE)
    
    # Remove code blocks
    text = re.sub(r'```.*?```', '', text, flags=re.DOTALL)
    
    # Remove inline code
    text = re.sub(r'`[^`]+`', '', text)
    
    # Count words
    words = re.findall(r'\b\w+\b', text)
    return len(words)


def validate_lesson(lesson_path, min_words=750, max_words=850):
    """Validate word count for a lesson file"""
    try:
        with open(lesson_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        word_count = count_words(content)
        
        if word_count < min_words:
            return {
                'status': 'FAIL',
                'word_count': word_count,
                'message': f'Content too short: {word_count} words (minimum: {min_words})'
            }
        elif word_count > max_words:
            return {
                'status': 'FAIL',
                'word_count': word_count,
                'message': f'Content too long: {word_count} words (maximum: {max_words})'
            }
        else:
            return {
                'status': 'PASS',
                'word_count': word_count,
                'message': f'Word count valid: {word_count} words'
            }
    except Exception as e:
        return {
            'status': 'ERROR',
            'word_count': 0,
            'message': f'Error reading file: {str(e)}'
        }


def main():
    """Main validation function"""
    if len(sys.argv) < 2:
        print("Usage: validate-word-count.py <lesson-file>")
        sys.exit(1)
    
    lesson_path = Path(sys.argv[1])
    
    if not lesson_path.exists():
        print(f"Error: File not found: {lesson_path}")
        sys.exit(1)
    
    result = validate_lesson(lesson_path)
    
    print(f"File: {lesson_path}")
    print(f"Status: {result['status']}")
    print(f"Word Count: {result['word_count']}")
    print(f"Message: {result['message']}")
    
    if result['status'] == 'FAIL':
        sys.exit(1)
    elif result['status'] == 'ERROR':
        sys.exit(2)
    else:
        sys.exit(0)


if __name__ == '__main__':
    main()

