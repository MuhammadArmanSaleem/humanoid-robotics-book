#!/usr/bin/env python3
"""
Source Validation Script
Validates that sources are from authoritative domains (T088)
"""

import re
import sys
from pathlib import Path
from urllib.parse import urlparse


AUTHORITATIVE_DOMAINS = [
    '.edu',
    '.org',
    '.gov',
    'tesla.com',
    'figure.ai',
    'bostondynamics.com',
    'nasa.gov',
    'ros.org',
    'gazebosim.org',
    'mitpress.mit.edu',
    'arxiv.org',
    'github.com/osrf',
    'github.com/ros2',
]


def extract_sources(text):
    """Extract URLs and source references from text"""
    # Find URLs
    url_pattern = r'https?://[^\s\)]+'
    urls = re.findall(url_pattern, text)
    
    # Find source references in "Further Reading" section
    further_reading_pattern = r'## Further Reading.*?(?=##|\Z)'
    further_reading = re.search(further_reading_pattern, text, re.DOTALL | re.IGNORECASE)
    
    sources = []
    if further_reading:
        # Extract lines that look like sources
        lines = further_reading.group(0).split('\n')
        for line in lines:
            if 'http' in line or any(domain in line.lower() for domain in ['edu', 'org', 'gov', '.com']):
                sources.append(line.strip())
    
    # Combine URLs and source references
    all_sources = list(set(urls + sources))
    return all_sources


def is_authoritative(url_or_text):
    """Check if source is from authoritative domain"""
    # Extract URL if present
    url_match = re.search(r'https?://([^\s\)/]+)', url_or_text)
    if url_match:
        domain = url_match.group(1).lower()
    else:
        domain = url_or_text.lower()
    
    # Check against authoritative domains
    for auth_domain in AUTHORITATIVE_DOMAINS:
        if auth_domain in domain:
            return True
    
    return False


def validate_sources(lesson_path, min_sources=3):
    """Validate sources in a lesson file"""
    try:
        with open(lesson_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        sources = extract_sources(content)
        authoritative_sources = [s for s in sources if is_authoritative(s)]
        
        if len(sources) < min_sources:
            return {
                'status': 'FAIL',
                'total_sources': len(sources),
                'authoritative_sources': len(authoritative_sources),
                'message': f'Insufficient sources: {len(sources)} found (minimum: {min_sources})'
            }
        elif len(authoritative_sources) < min_sources:
            return {
                'status': 'WARN',
                'total_sources': len(sources),
                'authoritative_sources': len(authoritative_sources),
                'message': f'Insufficient authoritative sources: {len(authoritative_sources)} found (minimum: {min_sources})'
            }
        else:
            return {
                'status': 'PASS',
                'total_sources': len(sources),
                'authoritative_sources': len(authoritative_sources),
                'message': f'Source validation passed: {len(authoritative_sources)} authoritative sources found'
            }
    except Exception as e:
        return {
            'status': 'ERROR',
            'total_sources': 0,
            'authoritative_sources': 0,
            'message': f'Error reading file: {str(e)}'
        }


def main():
    """Main validation function"""
    if len(sys.argv) < 2:
        print("Usage: validate-sources.py <lesson-file>")
        sys.exit(1)
    
    lesson_path = Path(sys.argv[1])
    
    if not lesson_path.exists():
        print(f"Error: File not found: {lesson_path}")
        sys.exit(1)
    
    result = validate_sources(lesson_path)
    
    print(f"File: {lesson_path}")
    print(f"Status: {result['status']}")
    print(f"Total Sources: {result['total_sources']}")
    print(f"Authoritative Sources: {result['authoritative_sources']}")
    print(f"Message: {result['message']}")
    
    if result['status'] == 'FAIL':
        sys.exit(1)
    elif result['status'] == 'ERROR':
        sys.exit(2)
    else:
        sys.exit(0)


if __name__ == '__main__':
    main()

