"""
Statistical Analysis Tests
Tests for traditional statistical analysis methods
"""
import sys
import os
import unittest
from datetime import datetime, timedelta
from typing import List, Dict, Any

# Add parent directories to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from test.utils.test_data_generator import TestDataGenerator
from test.test_config import TestConfig

class StatisticalAnalyzer:
    """Traditional statistical analysis methods"""
    
    def __init__(self):
        self.config = TestConfig()
    
    def calculate_delay_statistics(self, schedules: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate delay-related statistics"""
        now = datetime.now()
        total_schedules = len(schedules)
        
        if total_schedules == 0:
            return {
                'total_schedules': 0,
                'delayed_count': 0,
                'delay_percentage': 0,
                'average_delay_days': 0,
                'max_delay_days': 0,
                'on_time_percentage': 0
            }
        
        delayed_schedules = []
        on_time_schedules = []
        delay_days = []
        
        for schedule in schedules:
            delivery_date = schedule['delivery_date']
            if isinstance(delivery_date, str):
                delivery_date = datetime.fromisoformat(delivery_date.replace('Z', '+00:00'))
            
            if delivery_date < now and schedule['status'] in ['delayed', 'at_risk']:
                delayed_schedules.append(schedule)
                days_delayed = (now - delivery_date).days
                delay_days.append(days_delayed)
            elif schedule['status'] == 'completed':
                on_time_schedules.append(schedule)
        
        delayed_count = len(delayed_schedules)
        delay_percentage = (delayed_count / total_schedules) * 100
        on_time_percentage = (len(on_time_schedules) / total_schedules) * 100
        
        average_delay = sum(delay_days) / len(delay_days) if delay_days else 0
        max_delay = max(delay_days) if delay_days else 0
        
        return {
            'total_schedules': total_schedules,
            'delayed_count': delayed_count,
            'delay_percentage': round(delay_percentage, 2),
            'average_delay_days': round(average_delay, 2),
            'max_delay_days': max_delay,
            'on_time_percentage': round(on_time_percentage, 2),
            'delay_days_list': delay_days
        }
    
    def calculate_event_statistics(self, events: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate news event statistics"""
        total_events = len(events)
        
        if total_events == 0:
            return {
                'total_events': 0,
                'high_impact_count': 0,
                'high_impact_percentage': 0,
                'category_distribution': {},
                'country_distribution': {},
                'recent_events_count': 0
            }
        
        # Count by impact level
        impact_counts = {'low': 0, 'medium': 0, 'high': 0}
        for event in events:
            impact_counts[event['impact_level']] += 1
        
        # Count by category
        category_counts = {}
        for event in events:
            category = event['category']
            category_counts[category] = category_counts.get(category, 0) + 1
        
        # Count by country
        country_counts = {}
        for event in events:
            country = event['country']
            country_counts[country] = country_counts.get(country, 0) + 1
        
        # Count recent events (last 7 days)
        now = datetime.now()
        recent_events = 0
        for event in events:
            pub_date = event['published_date']
            if isinstance(pub_date, str):
                pub_date = datetime.fromisoformat(pub_date.replace('Z', '+00:00'))
            
            if (now - pub_date).days <= 7:
                recent_events += 1
        
        high_impact_percentage = (impact_counts['high'] / total_events) * 100
        
        return {
            'total_events': total_events,
            'high_impact_count': impact_counts['high'],
            'high_impact_percentage': round(high_impact_percentage, 2),
            'impact_distribution': impact_counts,
            'category_distribution': category_counts,
            'country_distribution': country_counts,
            'recent_events_count': recent_events
        }
    
    def calculate_risk_score_from_statistics(self, delay_stats: Dict[str, Any], 
                                           event_stats: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate overall risk score based on statistics"""
        
        # Delay risk component (0-40 points)
        delay_risk = min(40, delay_stats['delay_percentage'] * 0.4)
        
        # Event risk component (0-40 points)
        event_risk = min(40, event_stats['high_impact_percentage'] * 0.4)
        
        # Recent events risk component (0-20 points)
        recent_risk = min(20, event_stats['recent_events_count'] * 2)
        
        total_score = delay_risk + event_risk + recent_risk
        risk_level = self.config.get_risk_level_from_score(total_score)
        
        return {
            'total_score': round(total_score, 2),
            'risk_level': risk_level,
            'components': {
                'delay_risk': round(delay_risk, 2),
                'event_risk': round(event_risk, 2),
                'recent_risk': round(recent_risk, 2)
            },
            'methodology': 'statistical_analysis'
        }

class TestStatisticalAnalysis(unittest.TestCase):
    """Test cases for statistical analysis"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.generator = TestDataGenerator()
        self.analyzer = StatisticalAnalyzer()
        self.config = TestConfig()
    
    def test_delay_statistics_calculation(self):
        """Test delay statistics calculation"""
        # Generate test data
        schedules = self.generator.generate_schedule_data(count=20)
        
        # Calculate statistics
        stats = self.analyzer.calculate_delay_statistics(schedules)
        
        # Verify results
        self.assertIsInstance(stats, dict)
        self.assertEqual(stats['total_schedules'], 20)
        self.assertGreaterEqual(stats['delay_percentage'], 0)
        self.assertLessEqual(stats['delay_percentage'], 100)
        self.assertGreaterEqual(stats['on_time_percentage'], 0)
        self.assertLessEqual(stats['on_time_percentage'], 100)
        
        print(f"✓ Delay Statistics: {stats['delayed_count']}/{stats['total_schedules']} delayed ({stats['delay_percentage']}%)")
    
    def test_event_statistics_calculation(self):
        """Test event statistics calculation"""
        # Generate test data
        events = self.generator.generate_news_events(count=30)
        
        # Calculate statistics
        stats = self.analyzer.calculate_event_statistics(events)
        
        # Verify results
        self.assertIsInstance(stats, dict)
        self.assertEqual(stats['total_events'], 30)
        self.assertGreaterEqual(stats['high_impact_percentage'], 0)
        self.assertLessEqual(stats['high_impact_percentage'], 100)
        self.assertIsInstance(stats['category_distribution'], dict)
        self.assertIsInstance(stats['country_distribution'], dict)
        
        print(f"✓ Event Statistics: {stats['high_impact_count']}/{stats['total_events']} high-impact ({stats['high_impact_percentage']}%)")
    
    def test_risk_score_calculation(self):
        """Test risk score calculation from statistics"""
        # Generate test data for different scenarios
        for scenario_name in ['low_risk', 'medium_risk', 'high_risk']:
            with self.subTest(scenario=scenario_name):
                data = self.generator.generate_scenario_data(scenario_name)
                
                # Calculate statistics
                delay_stats = self.analyzer.calculate_delay_statistics(data['schedules'])
                event_stats = self.analyzer.calculate_event_statistics(data['news_events'])
                
                # Calculate risk score
                risk_result = self.analyzer.calculate_risk_score_from_statistics(delay_stats, event_stats)
                
                # Verify results
                self.assertIsInstance(risk_result, dict)
                self.assertIn('total_score', risk_result)
                self.assertIn('risk_level', risk_result)
                self.assertIn('components', risk_result)
                self.assertGreaterEqual(risk_result['total_score'], 0)
                self.assertLessEqual(risk_result['total_score'], 100)
                
                print(f"✓ {scenario_name.title()} Scenario: Score={risk_result['total_score']}, Level={risk_result['risk_level']}")
    
    def test_empty_data_handling(self):
        """Test handling of empty datasets"""
        # Test with empty schedules
        empty_delay_stats = self.analyzer.calculate_delay_statistics([])
        self.assertEqual(empty_delay_stats['total_schedules'], 0)
        self.assertEqual(empty_delay_stats['delay_percentage'], 0)
        
        # Test with empty events
        empty_event_stats = self.analyzer.calculate_event_statistics([])
        self.assertEqual(empty_event_stats['total_events'], 0)
        self.assertEqual(empty_event_stats['high_impact_percentage'], 0)
        
        print("✓ Empty data handling works correctly")

if __name__ == '__main__':
    unittest.main(verbosity=2)
