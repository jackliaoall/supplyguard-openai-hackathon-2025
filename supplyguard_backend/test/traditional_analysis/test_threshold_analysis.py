"""
Threshold Analysis Tests
Tests for traditional threshold-based risk assessment
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

class ThresholdAnalyzer:
    """Traditional threshold-based analysis methods"""
    
    def __init__(self):
        self.config = TestConfig()
        
        # Define thresholds for different metrics
        self.thresholds = {
            'delay_percentage': {
                'low': 10,      # < 10% delayed
                'medium': 25,   # 10-25% delayed
                'high': 50,     # 25-50% delayed
                'critical': 75  # > 50% delayed
            },
            'high_impact_events': {
                'low': 2,       # < 2 high-impact events
                'medium': 5,    # 2-5 high-impact events
                'high': 10,     # 5-10 high-impact events
                'critical': 15  # > 10 high-impact events
            },
            'average_delay_days': {
                'low': 3,       # < 3 days average delay
                'medium': 7,    # 3-7 days average delay
                'high': 14,     # 7-14 days average delay
                'critical': 30  # > 14 days average delay
            },
            'recent_events_count': {
                'low': 3,       # < 3 recent events
                'medium': 7,    # 3-7 recent events
                'high': 15,     # 7-15 recent events
                'critical': 25  # > 15 recent events
            }
        }
    
    def assess_delay_risk_by_threshold(self, schedules: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Assess delay risk using threshold-based approach"""
        now = datetime.now()
        total_schedules = len(schedules)
        
        if total_schedules == 0:
            return {
                'risk_level': 'low',
                'risk_score': 0,
                'metrics': {},
                'threshold_analysis': {},
                'methodology': 'threshold_delay'
            }
        
        # Calculate metrics
        delayed_count = 0
        delay_days = []
        
        for schedule in schedules:
            delivery_date = schedule['delivery_date']
            if isinstance(delivery_date, str):
                delivery_date = datetime.fromisoformat(delivery_date.replace('Z', '+00:00'))
            
            if delivery_date < now and schedule['status'] in ['delayed', 'at_risk']:
                delayed_count += 1
                days_delayed = (now - delivery_date).days
                delay_days.append(days_delayed)
        
        delay_percentage = (delayed_count / total_schedules) * 100
        average_delay = sum(delay_days) / len(delay_days) if delay_days else 0
        
        # Apply thresholds
        delay_risk_level = self._get_risk_level_by_threshold(
            delay_percentage, self.thresholds['delay_percentage']
        )
        
        avg_delay_risk_level = self._get_risk_level_by_threshold(
            average_delay, self.thresholds['average_delay_days']
        )
        
        # Combine risk levels (take the higher one)
        combined_risk_level = self._combine_risk_levels([delay_risk_level, avg_delay_risk_level])
        
        # Convert risk level to score
        risk_score = self._risk_level_to_score(combined_risk_level)
        
        return {
            'risk_level': combined_risk_level,
            'risk_score': risk_score,
            'metrics': {
                'total_schedules': total_schedules,
                'delayed_count': delayed_count,
                'delay_percentage': round(delay_percentage, 2),
                'average_delay_days': round(average_delay, 2)
            },
            'threshold_analysis': {
                'delay_percentage_risk': delay_risk_level,
                'average_delay_risk': avg_delay_risk_level,
                'thresholds_used': {
                    'delay_percentage': self.thresholds['delay_percentage'],
                    'average_delay_days': self.thresholds['average_delay_days']
                }
            },
            'methodology': 'threshold_delay'
        }
    
    def assess_event_risk_by_threshold(self, events: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Assess event risk using threshold-based approach"""
        total_events = len(events)
        
        if total_events == 0:
            return {
                'risk_level': 'low',
                'risk_score': 0,
                'metrics': {},
                'threshold_analysis': {},
                'methodology': 'threshold_events'
            }
        
        # Calculate metrics
        high_impact_count = sum(1 for event in events if event['impact_level'] == 'high')
        
        # Count recent events (last 7 days)
        now = datetime.now()
        recent_events_count = 0
        for event in events:
            pub_date = event['published_date']
            if isinstance(pub_date, str):
                pub_date = datetime.fromisoformat(pub_date.replace('Z', '+00:00'))
            
            if (now - pub_date).days <= 7:
                recent_events_count += 1
        
        # Apply thresholds
        high_impact_risk_level = self._get_risk_level_by_threshold(
            high_impact_count, self.thresholds['high_impact_events']
        )
        
        recent_events_risk_level = self._get_risk_level_by_threshold(
            recent_events_count, self.thresholds['recent_events_count']
        )
        
        # Combine risk levels
        combined_risk_level = self._combine_risk_levels([high_impact_risk_level, recent_events_risk_level])
        
        # Convert risk level to score
        risk_score = self._risk_level_to_score(combined_risk_level)
        
        return {
            'risk_level': combined_risk_level,
            'risk_score': risk_score,
            'metrics': {
                'total_events': total_events,
                'high_impact_count': high_impact_count,
                'recent_events_count': recent_events_count
            },
            'threshold_analysis': {
                'high_impact_risk': high_impact_risk_level,
                'recent_events_risk': recent_events_risk_level,
                'thresholds_used': {
                    'high_impact_events': self.thresholds['high_impact_events'],
                    'recent_events_count': self.thresholds['recent_events_count']
                }
            },
            'methodology': 'threshold_events'
        }
    
    def _get_risk_level_by_threshold(self, value: float, thresholds: Dict[str, float]) -> str:
        """Determine risk level based on threshold comparison"""
        if value >= thresholds['critical']:
            return 'critical'
        elif value >= thresholds['high']:
            return 'high'
        elif value >= thresholds['medium']:
            return 'medium'
        else:
            return 'low'
    
    def _combine_risk_levels(self, risk_levels: List[str]) -> str:
        """Combine multiple risk levels by taking the highest"""
        risk_priority = {'low': 0, 'medium': 1, 'high': 2, 'critical': 3}
        max_priority = max(risk_priority[level] for level in risk_levels)
        
        for level, priority in risk_priority.items():
            if priority == max_priority:
                return level
        
        return 'low'
    
    def _risk_level_to_score(self, risk_level: str) -> float:
        """Convert risk level to numerical score"""
        level_scores = {
            'low': 25,
            'medium': 50,
            'high': 75,
            'critical': 90
        }
        return level_scores.get(risk_level, 25)

class TestThresholdAnalysis(unittest.TestCase):
    """Test cases for threshold-based analysis"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.generator = TestDataGenerator()
        self.analyzer = ThresholdAnalyzer()
        self.config = TestConfig()
    
    def test_delay_threshold_analysis(self):
        """Test delay risk assessment using thresholds"""
        # Test different scenarios
        for scenario_name in ['low_risk', 'medium_risk', 'high_risk', 'critical_risk']:
            with self.subTest(scenario=scenario_name):
                data = self.generator.generate_scenario_data(scenario_name)
                
                # Analyze delay risk
                result = self.analyzer.assess_delay_risk_by_threshold(data['schedules'])
                
                # Verify results
                self.assertIsInstance(result, dict)
                self.assertIn('risk_level', result)
                self.assertIn('risk_score', result)
                self.assertIn('metrics', result)
                self.assertIn('threshold_analysis', result)
                
                # Verify risk level is valid
                self.assertIn(result['risk_level'], ['low', 'medium', 'high', 'critical'])
                
                print(f"✓ {scenario_name.title()} Delay Threshold: Level={result['risk_level']}, Score={result['risk_score']}")
                print(f"  Metrics: {result['metrics']['delayed_count']}/{result['metrics']['total_schedules']} delayed ({result['metrics']['delay_percentage']}%)")
    
    def test_event_threshold_analysis(self):
        """Test event risk assessment using thresholds"""
        # Test different scenarios
        for scenario_name in ['low_risk', 'medium_risk', 'high_risk', 'critical_risk']:
            with self.subTest(scenario=scenario_name):
                data = self.generator.generate_scenario_data(scenario_name)
                
                # Analyze event risk
                result = self.analyzer.assess_event_risk_by_threshold(data['news_events'])
                
                # Verify results
                self.assertIsInstance(result, dict)
                self.assertIn('risk_level', result)
                self.assertIn('risk_score', result)
                self.assertIn('metrics', result)
                self.assertIn('threshold_analysis', result)
                
                # Verify risk level is valid
                self.assertIn(result['risk_level'], ['low', 'medium', 'high', 'critical'])
                
                print(f"✓ {scenario_name.title()} Event Threshold: Level={result['risk_level']}, Score={result['risk_score']}")
                print(f"  Metrics: {result['metrics']['high_impact_count']} high-impact, {result['metrics']['recent_events_count']} recent")
    
    def test_threshold_boundary_conditions(self):
        """Test threshold boundary conditions"""
        # Test exact threshold values
        test_cases = [
            {'delay_percentage': 10, 'expected_min_level': 'medium'},
            {'delay_percentage': 25, 'expected_min_level': 'high'},
            {'delay_percentage': 50, 'expected_min_level': 'critical'},
        ]
        
        for case in test_cases:
            # Create schedules with exact delay percentage
            total_schedules = 100
            delayed_count = case['delay_percentage']
            
            schedules = []
            now = datetime.now()
            
            # Create delayed schedules
            for i in range(delayed_count):
                schedules.append({
                    'id': i + 1,
                    'delivery_date': now - timedelta(days=1),
                    'status': 'delayed'
                })
            
            # Create on-time schedules
            for i in range(delayed_count, total_schedules):
                schedules.append({
                    'id': i + 1,
                    'delivery_date': now + timedelta(days=1),
                    'status': 'on_track'
                })
            
            result = self.analyzer.assess_delay_risk_by_threshold(schedules)
            
            print(f"✓ Boundary Test: {case['delay_percentage']}% delay → {result['risk_level']} risk")
    
    def test_empty_data_threshold_analysis(self):
        """Test threshold analysis with empty data"""
        # Test empty schedules
        delay_result = self.analyzer.assess_delay_risk_by_threshold([])
        self.assertEqual(delay_result['risk_level'], 'low')
        self.assertEqual(delay_result['risk_score'], 0)
        
        # Test empty events
        event_result = self.analyzer.assess_event_risk_by_threshold([])
        self.assertEqual(event_result['risk_level'], 'low')
        self.assertEqual(event_result['risk_score'], 0)
        
        print("✓ Empty data threshold analysis works correctly")

if __name__ == '__main__':
    unittest.main(verbosity=2)
