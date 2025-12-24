#!/usr/bin/env python3
"""
Edge Case Handler Module
Implements edge case handling for content generation (T094-T103)
"""

import re
import logging
from typing import Dict, List, Optional, Tuple
from enum import Enum


class EdgeCaseType(Enum):
    """Edge case types from specification"""
    INSUFFICIENT_SOURCES = "insufficient_sources"
    CONFLICTING_INFORMATION = "conflicting_information"
    WORD_COUNT_EXCEEDS = "word_count_exceeds"
    WORD_COUNT_SHORT = "word_count_short"
    VISUAL_AIDS_REQUIRED = "visual_aids_required"


class EdgeCaseHandler:
    """Handler for edge cases in content generation"""
    
    def __init__(self):
        """Initialize edge case handler"""
        self.logger = logging.getLogger('edge_case_handler')
        self.logger.setLevel(logging.INFO)
    
    def handle_insufficient_sources(self,
                                   sources_found: int,
                                   min_required: int = 3) -> Dict:
        """
        Handle insufficient research sources (T094, T099)
        
        Strategy:
        - Expand search terms
        - Use related concepts
        - Proceed with available sources (minimum 1)
        - Flag for manual review
        """
        if sources_found >= min_required:
            return {'handled': False, 'message': 'Sufficient sources available'}
        
        strategy = {
            'handled': True,
            'edge_case': EdgeCaseType.INSUFFICIENT_SOURCES.value,
            'sources_found': sources_found,
            'min_required': min_required,
            'fallback_actions': [
                'Expand search terms to related concepts',
                'Use broader topic categories',
                'Include foundational sources even if older',
                f'Proceed with {sources_found} available source(s)',
                'Flag lesson for manual source review'
            ],
            'user_notification': (
                f"Limited research sources found ({sources_found}/{min_required}). "
                "Proceeding with available sources. Lesson flagged for review."
            )
        }
        
        self.logger.warning(f"Insufficient sources: {sources_found}/{min_required}")
        return strategy
    
    def handle_conflicting_information(self,
                                     conflicts: List[Dict]) -> Dict:
        """
        Handle conflicting information from different sources (T095, T100)
        
        Strategy:
        - Prioritize more authoritative sources (.edu, .org over .com)
        - Use most recent sources (prefer 2023-2025)
        - Present multiple perspectives when appropriate
        - Flag conflicts for manual review
        """
        if not conflicts:
            return {'handled': False, 'message': 'No conflicts detected'}
        
        # Prioritize sources by authority
        prioritized_conflicts = sorted(
            conflicts,
            key=lambda x: (
                1 if '.edu' in x.get('source', '') or '.org' in x.get('source', '') else 2,
                -int(x.get('year', 0))  # Most recent first
            )
        )
        
        strategy = {
            'handled': True,
            'edge_case': EdgeCaseType.CONFLICTING_INFORMATION.value,
            'conflicts_detected': len(conflicts),
            'resolution_strategy': 'prioritize_authoritative_recent',
            'actions': [
                'Prioritize .edu and .org sources over .com',
                'Prefer sources from 2023-2025 timeframe',
                'Present multiple perspectives when appropriate',
                'Document conflict resolution decisions',
                'Flag for manual review if high-stakes conflict'
            ],
            'resolved_conflicts': prioritized_conflicts,
            'user_notification': (
                f"Conflicting information detected in {len(conflicts)} source(s). "
                "Resolved using authoritative source prioritization. "
                "Conflicts documented for review."
            )
        }
        
        self.logger.warning(f"Conflicting information: {len(conflicts)} conflicts resolved")
        return strategy
    
    def handle_word_count_exceeds(self,
                                 word_count: int,
                                 max_words: int = 850) -> Dict:
        """
        Handle content exceeding word limit (T096, T101)
        
        Strategy:
        - Summarize verbose sections
        - Remove redundant content
        - Focus on key concepts
        """
        if word_count <= max_words:
            return {'handled': False, 'message': 'Word count within limit'}
        
        excess = word_count - max_words
        strategy = {
            'handled': True,
            'edge_case': EdgeCaseType.WORD_COUNT_EXCEEDS.value,
            'word_count': word_count,
            'max_words': max_words,
            'excess': excess,
            'adjustment_strategy': 'summarize_and_trim',
            'actions': [
                f'Summarize verbose sections (reduce by ~{excess} words)',
                'Remove redundant explanations',
                'Consolidate similar examples',
                'Focus on key concepts',
                'Maintain technical accuracy'
            ],
            'user_notification': (
                f"Content exceeds word limit ({word_count}/{max_words}). "
                f"Summarizing to reduce by ~{excess} words."
            )
        }
        
        self.logger.warning(f"Word count exceeds limit: {word_count}/{max_words}")
        return strategy
    
    def handle_word_count_short(self,
                               word_count: int,
                               min_words: int = 750) -> Dict:
        """
        Handle content falling short of word limit (T097, T101)
        
        Strategy:
        - Expand explanations
        - Add more examples
        - Include additional concepts
        - Add practical applications
        """
        if word_count >= min_words:
            return {'handled': False, 'message': 'Word count sufficient'}
        
        deficit = min_words - word_count
        strategy = {
            'handled': True,
            'edge_case': EdgeCaseType.WORD_COUNT_SHORT.value,
            'word_count': word_count,
            'min_words': min_words,
            'deficit': deficit,
            'expansion_strategy': 'expand_and_enrich',
            'actions': [
                f'Expand explanations (add ~{deficit} words)',
                'Add more technical examples',
                'Include additional related concepts',
                'Add practical applications',
                'Enhance hands-on exercise descriptions'
            ],
            'user_notification': (
                f"Content falls short of word limit ({word_count}/{min_words}). "
                f"Expanding content by ~{deficit} words."
            )
        }
        
        self.logger.warning(f"Word count short: {word_count}/{min_words}")
        return strategy
    
    def handle_visual_aids_required(self,
                                   concepts: List[str]) -> Dict:
        """
        Handle complex technical concepts requiring visual aids (T098, T102)
        
        Strategy:
        - Insert placeholder markers
        - Include descriptions of required visuals
        - Suggest visual aid types
        """
        if not concepts:
            return {'handled': False, 'message': 'No visual aids required'}
        
        strategy = {
            'handled': True,
            'edge_case': EdgeCaseType.VISUAL_AIDS_REQUIRED.value,
            'concepts_requiring_visuals': concepts,
            'placeholder_strategy': 'mark_and_describe',
            'actions': [
                'Insert placeholder markers for each concept',
                'Include descriptions of required visuals',
                'Suggest visual aid types (diagram, chart, code example)',
                'Flag lesson for visual aid creation',
                'Document visual aid requirements'
            ],
            'placeholders': [
                {
                    'concept': concept,
                    'placeholder': f'[VISUAL_AID: {concept}]',
                    'description': f'Diagram or illustration showing {concept}',
                    'suggested_type': 'diagram'
                }
                for concept in concepts
            ],
            'user_notification': (
                f"Visual aids required for {len(concepts)} concept(s). "
                "Placeholders inserted. Lesson flagged for visual aid creation."
            )
        }
        
        self.logger.info(f"Visual aids required: {len(concepts)} concepts")
        return strategy


def detect_edge_cases(content: str, sources: List[str]) -> List[EdgeCaseType]:
    """Detect edge cases in generated content"""
    detected = []
    
    # Check word count
    words = len(re.findall(r'\b\w+\b', content))
    if words > 850:
        detected.append(EdgeCaseType.WORD_COUNT_EXCEEDS)
    elif words < 750:
        detected.append(EdgeCaseType.WORD_COUNT_SHORT)
    
    # Check source count
    if len(sources) < 3:
        detected.append(EdgeCaseType.INSUFFICIENT_SOURCES)
    
    # Check for visual aid indicators
    visual_indicators = ['diagram', 'illustration', 'figure', 'chart', 'graph']
    if any(indicator in content.lower() for indicator in visual_indicators):
        detected.append(EdgeCaseType.VISUAL_AIDS_REQUIRED)
    
    return detected


if __name__ == '__main__':
    # Example usage
    handler = EdgeCaseHandler()
    
    # Test insufficient sources
    result = handler.handle_insufficient_sources(sources_found=2)
    print(f"Insufficient sources handling: {result}")
    
    # Test word count exceeds
    result = handler.handle_word_count_exceeds(word_count=950)
    print(f"Word count exceeds handling: {result}")
    
    # Test word count short
    result = handler.handle_word_count_short(word_count=600)
    print(f"Word count short handling: {result}")

