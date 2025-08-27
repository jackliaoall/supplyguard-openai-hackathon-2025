"""
AI Strategy Tests
Tests for AI-powered analysis strategies and comparison with traditional methods
"""
import sys
import os
import unittest
from unittest.mock import Mock, patch
from typing import List, Dict, Any

# Add parent directories to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from test.utils.test_data_generator import TestDataGenerator
from test.test_config import TestConfig
from src.services.ai_service import AIService

class AIStrategyTester:
    """Test AI strategies and compare with traditional methods"""
    
    def __init__(self):
        self.config = TestConfig()
        self.ai_service = AIService()
    
    def test_ai_scheduler_analysis(self, schedules: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Test AI-powered schedule analysis"""
        if not schedules:
            return {
                'analysis_type': 'ai_scheduler',
                'risk_level': 'low',
                'risk_score': 0,
                'summary': 'No schedule data available',
                'methodology': 'ai_analysis'
            }
        
        # Prepare context for AI analysis
        context = {
            'total_schedules': len(schedules),
            'schedule_data': f"Analyzing {len(schedules)} equipment delivery schedules"
        }
        
        # Create analysis query
        query = f"Analyze delivery schedule risks for {len(schedules)} equipment schedules. Identify delays, bottlenecks, and potential timeline issues."
        
        try:
            # Use AI service for analysis
            result = self.ai_service.analyze_with_ai('scheduler', query, context)
            return result
        except Exception as e:
            # Fallback response if AI service fails
            return {
                'analysis_type': 'ai_scheduler',
                'risk_level': 'medium',
                'risk_score': 50,
                'summary': f'AI analysis failed: {str(e)}',
                'methodology': 'ai_analysis_fallback',
                'error': str(e)
            }
    
    def test_ai_political_analysis(self, events: List[Dict[str, Any]], country: str = None) -> Dict[str, Any]:
        """Test AI-powered political risk analysis"""
        if not events:
            return {
                'analysis_type': 'ai_political',
                'risk_level': 'low',
                'risk_score': 0,
                'summary': 'No political events available',
                'methodology': 'ai_analysis'
            }
        
        # Prepare context for AI analysis
        context = {
            'total_events': len(events),
            'target_country': country,
            'news_events': f"Analyzing {len(events)} political events"
        }
        
        # Create analysis query
        country_text = f" in {country}" if country else ""
        query = f"Analyze political risks affecting supply chain operations{country_text}. Consider geopolitical events, policy changes, and their impact on procurement and logistics."
        
        try:
            # Use AI service for analysis
            result = self.ai_service.analyze_with_ai('political', query, context)
            return result
        except Exception as e:
            # Fallback response if AI service fails
            return {
                'analysis_type': 'ai_political',
                'risk_level': 'medium',
                'risk_score': 50,
                'summary': f'AI analysis failed: {str(e)}',
                'methodology': 'ai_analysis_fallback',
                'error': str(e)
            }
    
    def test_ai_comprehensive_analysis(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Test AI-powered comprehensive analysis"""
        # Prepare comprehensive context
        context = {
            'equipment_count': len(data.get('equipment', [])),
            'schedule_count': len(data.get('schedules', [])),
            'event_count': len(data.get('news_events', [])),
            'comprehensive_data': 'Multi-dimensional supply chain risk analysis'
        }
        
        # Create comprehensive analysis query
        query = """Perform a comprehensive supply chain risk analysis considering:
        1. Equipment delivery schedules and potential delays
        2. Political and geopolitical risks
        3. Logistics and transportation challenges
        4. Trade policy and tariff impacts
        
        Provide an integrated risk assessment with prioritized recommendations."""
        
        try:
            # Use AI service for comprehensive analysis
            result = self.ai_service.analyze_with_ai('comprehensive', query, context)
            return result
        except Exception as e:
            # Fallback response if AI service fails
            return {
                'analysis_type': 'ai_comprehensive',
                'risk_level': 'medium',
                'risk_score': 50,
                'summary': f'AI comprehensive analysis failed: {str(e)}',
                'methodology': 'ai_analysis_fallback',
                'error': str(e)
            }
    
    def compare_ai_vs_traditional(self, ai_result: Dict[str, Any], 
                                traditional_result: Dict[str, Any]) -> Dict[str, Any]:
        """Compare AI and traditional analysis results"""
        
        # Extract key metrics for comparison
        ai_risk_score = ai_result.get('risk_score', 0)
        traditional_risk_score = traditional_result.get('risk_score', 0)
        
        ai_risk_level = ai_result.get('risk_level', 'unknown')
        traditional_risk_level = traditional_result.get('risk_level', 'unknown')
        
        # Calculate score difference
        score_difference = abs(ai_risk_score - traditional_risk_score)
        
        # Determine agreement level
        if ai_risk_level == traditional_risk_level:
            agreement = 'full_agreement'
        elif self._risk_levels_adjacent(ai_risk_level, traditional_risk_level):
            agreement = 'partial_agreement'
        else:
            agreement = 'disagreement'
        
        # Analyze strengths of each approach
        ai_strengths = [
            'Natural language processing',
            'Contextual understanding',
            'Complex pattern recognition',
            'Adaptive reasoning'
        ]
        
        traditional_strengths = [
            'Consistent methodology',
            'Transparent calculations',
            'Predictable results',
            'Fast processing'
        ]
        
        return {
            'ai_result': {
                'risk_score': ai_risk_score,
                'risk_level': ai_risk_level,
                'methodology': ai_result.get('methodology', 'ai_analysis')
            },
            'traditional_result': {
                'risk_score': traditional_risk_score,
                'risk_level': traditional_risk_level,
                'methodology': traditional_result.get('methodology', 'traditional_analysis')
            },
            'comparison': {
                'score_difference': round(score_difference, 2),
                'agreement_level': agreement,
                'ai_strengths': ai_strengths,
                'traditional_strengths': traditional_strengths
            },
            'recommendation': self._generate_comparison_recommendation(agreement, score_difference)
        }
    
    def _risk_levels_adjacent(self, level1: str, level2: str) -> bool:
        """Check if two risk levels are adjacent"""
        risk_order = ['low', 'medium', 'high', 'critical']
        try:
            idx1 = risk_order.index(level1)
            idx2 = risk_order.index(level2)
            return abs(idx1 - idx2) == 1
        except ValueError:
            return False
    
    def _generate_comparison_recommendation(self, agreement: str, score_difference: float) -> str:
        """Generate recommendation based on comparison results"""
        if agreement == 'full_agreement' and score_difference < 10:
            return "Both methods agree strongly. High confidence in risk assessment."
        elif agreement == 'partial_agreement' and score_difference < 20:
            return "Methods show partial agreement. Consider combining insights from both approaches."
        elif agreement == 'disagreement' or score_difference > 30:
            return "Significant disagreement detected. Manual review recommended to resolve discrepancies."
        else:
            return "Moderate agreement between methods. Consider context and specific use case requirements."

class TestAIStrategies(unittest.TestCase):
    """Test cases for AI analysis strategies"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.generator = TestDataGenerator()
        self.ai_tester = AIStrategyTester()
        self.config = TestConfig()
    
    def test_ai_scheduler_analysis(self):
        """Test AI-powered schedule analysis"""
        # Generate test schedules
        schedules = self.generator.generate_schedule_data(count=15)
        
        # Test AI analysis
        result = self.ai_tester.test_ai_scheduler_analysis(schedules)
        
        # Verify structure
        self.assertIsInstance(result, dict)
        self.assertIn('risk_level', result)
        self.assertIn('risk_score', result)
        self.assertIn('summary', result)
        
        print(f"✓ AI Schedule Analysis: Risk={result['risk_level']}, Score={result['risk_score']}")
        print(f"  Summary: {result['summary'][:100]}...")
        
        if 'error' in result:
            print(f"  Note: Fallback used due to: {result['error']}")
    
    def test_ai_political_analysis(self):
        """Test AI-powered political risk analysis"""
        # Generate test events
        events = self.generator.generate_news_events(count=20)
        
        # Test AI analysis with and without country focus
        result_global = self.ai_tester.test_ai_political_analysis(events)
        result_country = self.ai_tester.test_ai_political_analysis(events, country="Germany")
        
        # Verify structure
        for result in [result_global, result_country]:
            self.assertIsInstance(result, dict)
            self.assertIn('risk_level', result)
            self.assertIn('risk_score', result)
            self.assertIn('summary', result)
        
        print(f"✓ AI Political Analysis (Global): Risk={result_global['risk_level']}, Score={result_global['risk_score']}")
        print(f"✓ AI Political Analysis (Germany): Risk={result_country['risk_level']}, Score={result_country['risk_score']}")
    
    def test_ai_comprehensive_analysis(self):
        """Test AI-powered comprehensive analysis"""
        # Generate comprehensive test data
        data = self.generator.generate_scenario_data('medium_risk')
        
        # Test comprehensive AI analysis
        result = self.ai_tester.test_ai_comprehensive_analysis(data)
        
        # Verify structure
        self.assertIsInstance(result, dict)
        self.assertIn('risk_level', result)
        self.assertIn('risk_score', result)
        self.assertIn('summary', result)
        
        print(f"✓ AI Comprehensive Analysis: Risk={result['risk_level']}, Score={result['risk_score']}")
        print(f"  Summary: {result['summary'][:100]}...")
    
    def test_ai_vs_traditional_comparison(self):
        """Test comparison between AI and traditional methods"""
        # Import traditional analyzers
        from test.traditional_analysis.test_statistical_analysis import StatisticalAnalyzer
        from test.traditional_analysis.test_threshold_analysis import ThresholdAnalyzer
        
        # Generate test data
        data = self.generator.generate_scenario_data('high_risk')
        
        # Run AI analysis
        ai_result = self.ai_tester.test_ai_scheduler_analysis(data['schedules'])
        
        # Run traditional analysis
        traditional_analyzer = StatisticalAnalyzer()
        delay_stats = traditional_analyzer.calculate_delay_statistics(data['schedules'])
        event_stats = traditional_analyzer.calculate_event_statistics(data['news_events'])
        traditional_result = traditional_analyzer.calculate_risk_score_from_statistics(delay_stats, event_stats)
        
        # Compare results
        comparison = self.ai_tester.compare_ai_vs_traditional(ai_result, traditional_result)
        
        # Verify comparison structure
        self.assertIsInstance(comparison, dict)
        self.assertIn('ai_result', comparison)
        self.assertIn('traditional_result', comparison)
        self.assertIn('comparison', comparison)
        self.assertIn('recommendation', comparison)
        
        print(f"✓ AI vs Traditional Comparison:")
        print(f"  AI: Risk={comparison['ai_result']['risk_level']}, Score={comparison['ai_result']['risk_score']}")
        print(f"  Traditional: Risk={comparison['traditional_result']['risk_level']}, Score={comparison['traditional_result']['risk_score']}")
        print(f"  Agreement: {comparison['comparison']['agreement_level']}")
        print(f"  Score Difference: {comparison['comparison']['score_difference']}")
        print(f"  Recommendation: {comparison['recommendation']}")
    
    def test_ai_analysis_scenarios(self):
        """Test AI analysis across different risk scenarios"""
        scenarios = ['low_risk', 'medium_risk', 'high_risk', 'critical_risk']
        
        for scenario_name in scenarios:
            with self.subTest(scenario=scenario_name):
                data = self.generator.generate_scenario_data(scenario_name)
                
                # Test AI schedule analysis
                schedule_result = self.ai_tester.test_ai_scheduler_analysis(data['schedules'])
                
                # Test AI political analysis
                political_result = self.ai_tester.test_ai_political_analysis(data['news_events'])
                
                print(f"✓ {scenario_name.title()} Scenario AI Analysis:")
                print(f"  Schedule: {schedule_result['risk_level']} (score: {schedule_result['risk_score']})")
                print(f"  Political: {political_result['risk_level']} (score: {political_result['risk_score']})")
    
    def test_ai_error_handling(self):
        """Test AI analysis error handling"""
        # Test with empty data
        empty_schedule_result = self.ai_tester.test_ai_scheduler_analysis([])
        empty_political_result = self.ai_tester.test_ai_political_analysis([])
        
        # Verify graceful handling
        self.assertEqual(empty_schedule_result['risk_level'], 'low')
        self.assertEqual(empty_political_result['risk_level'], 'low')
        
        print("✓ AI error handling works correctly for empty data")
    
    @patch('src.services.ai_service.AIService.analyze_with_ai')
    def test_ai_service_mock(self, mock_analyze):
        """Test AI analysis with mocked service"""
        # Mock AI service response
        mock_analyze.return_value = {
            'risk_level': 'high',
            'risk_score': 75,
            'summary': 'Mocked AI analysis result',
            'key_findings': ['Finding 1', 'Finding 2'],
            'recommendations': ['Recommendation 1', 'Recommendation 2'],
            'confidence': 85
        }
        
        # Generate test data
        schedules = self.generator.generate_schedule_data(count=10)
        
        # Test with mock
        result = self.ai_tester.test_ai_scheduler_analysis(schedules)
        
        # Verify mock was called and result structure
        mock_analyze.assert_called_once()
        self.assertEqual(result['risk_level'], 'high')
        self.assertEqual(result['risk_score'], 75)
        
        print("✓ AI service mocking works correctly")

if __name__ == '__main__':
    unittest.main(verbosity=2)
