"""
Keyword Matching Tests
Tests for traditional keyword-based risk analysis
"""
import sys
import os
import unittest
import re
from typing import List, Dict, Any, Set

# Add parent directories to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from test.utils.test_data_generator import TestDataGenerator
from test.test_config import TestConfig

class KeywordAnalyzer:
    """Traditional keyword-based analysis methods"""
    
    def __init__(self):
        self.config = TestConfig()
        
        # Enhanced keyword sets with weights
        self.keyword_weights = {
            'political': {
                'high_risk': ['war', 'conflict', 'coup', 'revolution', 'sanctions', 'embargo'],
                'medium_risk': ['election', 'government', 'policy', 'regulation', 'diplomatic'],
                'low_risk': ['political', 'parliament', 'minister', 'official']
            },
            'logistics': {
                'high_risk': ['blockade', 'strike', 'shutdown', 'disaster', 'collapse'],
                'medium_risk': ['congestion', 'delay', 'disruption', 'maintenance'],
                'low_risk': ['port', 'shipping', 'transport', 'logistics', 'route']
            },
            'tariff': {
                'high_risk': ['trade war', 'embargo', 'sanctions', 'ban'],
                'medium_risk': ['tariff', 'duty', 'quota', 'restriction'],
                'low_risk': ['trade', 'customs', 'import', 'export', 'agreement']
            },
            'schedule': {
                'high_risk': ['cancelled', 'suspended', 'failed', 'crisis'],
                'medium_risk': ['delayed', 'postponed', 'rescheduled', 'behind'],
                'low_risk': ['schedule', 'timeline', 'delivery', 'shipment']
            }
        }
        
        # Risk weights for scoring
        self.risk_weights = {
            'high_risk': 10,
            'medium_risk': 5,
            'low_risk': 1
        }
    
    def analyze_text_keywords(self, text: str, category: str = None) -> Dict[str, Any]:
        """Analyze text for risk keywords"""
        text_lower = text.lower()
        
        if category and category in self.keyword_weights:
            categories_to_check = [category]
        else:
            categories_to_check = list(self.keyword_weights.keys())
        
        results = {}
        total_score = 0
        total_matches = 0
        
        for cat in categories_to_check:
            cat_results = {
                'high_risk_matches': [],
                'medium_risk_matches': [],
                'low_risk_matches': [],
                'total_matches': 0,
                'category_score': 0
            }
            
            for risk_level, keywords in self.keyword_weights[cat].items():
                matches = []
                for keyword in keywords:
                    # Use word boundaries to avoid partial matches
                    pattern = r'\b' + re.escape(keyword.lower()) + r'\b'
                    if re.search(pattern, text_lower):
                        matches.append(keyword)
                        cat_results['category_score'] += self.risk_weights[risk_level]
                
                cat_results[f'{risk_level}_matches'] = matches
                cat_results['total_matches'] += len(matches)
            
            results[cat] = cat_results
            total_score += cat_results['category_score']
            total_matches += cat_results['total_matches']
        
        # Determine overall risk level
        if total_score >= 50:
            risk_level = 'critical'
        elif total_score >= 25:
            risk_level = 'high'
        elif total_score >= 10:
            risk_level = 'medium'
        else:
            risk_level = 'low'
        
        return {
            'total_score': total_score,
            'total_matches': total_matches,
            'risk_level': risk_level,
            'category_results': results,
            'methodology': 'keyword_matching'
        }
    
    def analyze_news_events_keywords(self, events: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze multiple news events for keywords"""
        if not events:
            return {
                'total_events': 0,
                'total_score': 0,
                'risk_level': 'low',
                'category_analysis': {},
                'high_risk_events': [],
                'methodology': 'keyword_matching_events'
            }
        
        total_score = 0
        category_scores = {}
        high_risk_events = []
        event_analyses = []
        
        for event in events:
            # Combine title and content for analysis
            text = f"{event.get('title', '')} {event.get('content', '')}"
            
            # Analyze this event
            analysis = self.analyze_text_keywords(text)
            analysis['event_id'] = event.get('id')
            analysis['event_title'] = event.get('title', '')
            
            event_analyses.append(analysis)
            total_score += analysis['total_score']
            
            # Track high-risk events
            if analysis['risk_level'] in ['high', 'critical']:
                high_risk_events.append({
                    'id': event.get('id'),
                    'title': event.get('title', ''),
                    'score': analysis['total_score'],
                    'risk_level': analysis['risk_level'],
                    'matches': analysis['total_matches']
                })
            
            # Aggregate category scores
            for category, cat_result in analysis['category_results'].items():
                if category not in category_scores:
                    category_scores[category] = {
                        'total_score': 0,
                        'event_count': 0,
                        'high_risk_matches': set(),
                        'medium_risk_matches': set(),
                        'low_risk_matches': set()
                    }
                
                category_scores[category]['total_score'] += cat_result['category_score']
                category_scores[category]['event_count'] += 1 if cat_result['total_matches'] > 0 else 0
                category_scores[category]['high_risk_matches'].update(cat_result['high_risk_matches'])
                category_scores[category]['medium_risk_matches'].update(cat_result['medium_risk_matches'])
                category_scores[category]['low_risk_matches'].update(cat_result['low_risk_matches'])
        
        # Convert sets to lists for JSON serialization
        for category in category_scores:
            for match_type in ['high_risk_matches', 'medium_risk_matches', 'low_risk_matches']:
                category_scores[category][match_type] = list(category_scores[category][match_type])
        
        # Calculate average score and determine overall risk
        avg_score = total_score / len(events) if events else 0
        
        if avg_score >= 15:
            overall_risk = 'critical'
        elif avg_score >= 8:
            overall_risk = 'high'
        elif avg_score >= 3:
            overall_risk = 'medium'
        else:
            overall_risk = 'low'
        
        return {
            'total_events': len(events),
            'total_score': total_score,
            'average_score': round(avg_score, 2),
            'risk_level': overall_risk,
            'category_analysis': category_scores,
            'high_risk_events': high_risk_events,
            'high_risk_event_count': len(high_risk_events),
            'event_analyses': event_analyses,
            'methodology': 'keyword_matching_events'
        }
    
    def extract_risk_keywords_from_text(self, text: str) -> Dict[str, List[str]]:
        """Extract all risk keywords found in text"""
        text_lower = text.lower()
        found_keywords = {
            'political': [],
            'logistics': [],
            'tariff': [],
            'schedule': []
        }
        
        for category, risk_levels in self.keyword_weights.items():
            for risk_level, keywords in risk_levels.items():
                for keyword in keywords:
                    pattern = r'\b' + re.escape(keyword.lower()) + r'\b'
                    if re.search(pattern, text_lower):
                        found_keywords[category].append({
                            'keyword': keyword,
                            'risk_level': risk_level,
                            'weight': self.risk_weights[risk_level]
                        })
        
        return found_keywords

class TestKeywordMatching(unittest.TestCase):
    """Test cases for keyword matching analysis"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.generator = TestDataGenerator()
        self.analyzer = KeywordAnalyzer()
        self.config = TestConfig()
    
    def test_single_text_keyword_analysis(self):
        """Test keyword analysis on single text"""
        test_texts = [
            {
                'text': 'Political tensions rise due to trade war and new sanctions',
                'expected_categories': ['political', 'tariff'],
                'expected_risk': 'high'
            },
            {
                'text': 'Port congestion causes shipping delays in major logistics hub',
                'expected_categories': ['logistics'],
                'expected_risk': 'medium'
            },
            {
                'text': 'Regular trade agreement discussion between countries',
                'expected_categories': ['tariff'],
                'expected_risk': 'low'
            }
        ]
        
        for i, test_case in enumerate(test_texts):
            with self.subTest(test_case=i):
                result = self.analyzer.analyze_text_keywords(test_case['text'])
                
                # Verify basic structure
                self.assertIsInstance(result, dict)
                self.assertIn('total_score', result)
                self.assertIn('risk_level', result)
                self.assertIn('category_results', result)
                
                # Check if expected categories have matches
                for category in test_case['expected_categories']:
                    self.assertGreater(
                        result['category_results'][category]['total_matches'], 0,
                        f"Expected matches in {category} category"
                    )
                
                print(f"✓ Text Analysis {i+1}: '{test_case['text'][:50]}...' → {result['risk_level']} risk (score: {result['total_score']})")
    
    def test_news_events_keyword_analysis(self):
        """Test keyword analysis on news events"""
        # Generate test events with specific content
        test_events = [
            {
                'id': 1,
                'title': 'Trade war escalates with new sanctions',
                'content': 'Government imposes embargo on critical supplies',
                'category': 'political'
            },
            {
                'id': 2,
                'title': 'Port strike causes major delays',
                'content': 'Logistics disruption affects shipping schedules',
                'category': 'logistics'
            },
            {
                'id': 3,
                'title': 'New trade agreement signed',
                'content': 'Countries agree on reduced tariffs and customs procedures',
                'category': 'trade'
            }
        ]
        
        result = self.analyzer.analyze_news_events_keywords(test_events)
        
        # Verify results
        self.assertIsInstance(result, dict)
        self.assertEqual(result['total_events'], 3)
        self.assertGreater(result['total_score'], 0)
        self.assertIn('category_analysis', result)
        self.assertIn('high_risk_events', result)
        
        print(f"✓ News Events Analysis: {result['total_events']} events, total score: {result['total_score']}, risk: {result['risk_level']}")
        print(f"  High-risk events: {result['high_risk_event_count']}")
    
    def test_keyword_extraction(self):
        """Test keyword extraction functionality"""
        test_text = "Political crisis leads to trade war with sanctions and port strikes causing logistics disruption"
        
        keywords = self.analyzer.extract_risk_keywords_from_text(test_text)
        
        # Verify structure
        self.assertIsInstance(keywords, dict)
        for category in ['political', 'logistics', 'tariff', 'schedule']:
            self.assertIn(category, keywords)
            self.assertIsInstance(keywords[category], list)
        
        # Check that keywords were found
        total_keywords = sum(len(keywords[cat]) for cat in keywords)
        self.assertGreater(total_keywords, 0)
        
        print(f"✓ Keyword Extraction: Found {total_keywords} keywords across categories")
        for category, kw_list in keywords.items():
            if kw_list:
                print(f"  {category}: {[kw['keyword'] for kw in kw_list]}")
    
    def test_scenario_based_keyword_analysis(self):
        """Test keyword analysis on different risk scenarios"""
        for scenario_name in ['low_risk', 'medium_risk', 'high_risk']:
            with self.subTest(scenario=scenario_name):
                data = self.generator.generate_scenario_data(scenario_name)
                
                # Analyze news events
                result = self.analyzer.analyze_news_events_keywords(data['news_events'])
                
                # Verify results
                self.assertIsInstance(result, dict)
                self.assertGreater(result['total_events'], 0)
                self.assertIn('risk_level', result)
                
                print(f"✓ {scenario_name.title()} Scenario Keywords: {result['total_events']} events, "
                      f"score: {result['total_score']}, risk: {result['risk_level']}")
    
    def test_empty_data_keyword_analysis(self):
        """Test keyword analysis with empty data"""
        # Test empty events list
        result = self.analyzer.analyze_news_events_keywords([])
        
        self.assertEqual(result['total_events'], 0)
        self.assertEqual(result['total_score'], 0)
        self.assertEqual(result['risk_level'], 'low')
        
        # Test empty text
        text_result = self.analyzer.analyze_text_keywords("")
        self.assertEqual(text_result['total_score'], 0)
        self.assertEqual(text_result['risk_level'], 'low')
        
        print("✓ Empty data keyword analysis works correctly")
    
    def test_keyword_case_sensitivity(self):
        """Test that keyword matching is case-insensitive"""
        test_cases = [
            "TRADE WAR escalates",
            "Trade War escalates", 
            "trade war escalates",
            "Trade war Escalates"
        ]
        
        results = []
        for text in test_cases:
            result = self.analyzer.analyze_text_keywords(text)
            results.append(result['total_score'])
        
        # All results should be the same
        self.assertTrue(all(score == results[0] for score in results))
        
        print("✓ Case-insensitive keyword matching works correctly")

if __name__ == '__main__':
    unittest.main(verbosity=2)
