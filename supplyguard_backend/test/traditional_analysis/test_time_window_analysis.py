"""
Time Window Analysis Tests
Tests for traditional time-based risk analysis
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

class TimeWindowAnalyzer:
    """Traditional time window analysis methods"""
    
    def __init__(self):
        self.config = TestConfig()
        
        # Define time windows for analysis
        self.time_windows = {
            'immediate': 1,    # 1 day
            'short_term': 7,   # 1 week
            'medium_term': 30, # 1 month
            'long_term': 90    # 3 months
        }
        
        # Risk decay factors (how risk decreases over time)
        self.risk_decay_factors = {
            'immediate': 1.0,    # Full impact
            'short_term': 0.8,   # 80% impact
            'medium_term': 0.5,  # 50% impact
            'long_term': 0.2     # 20% impact
        }
    
    def analyze_events_by_time_window(self, events: List[Dict[str, Any]], 
                                    reference_date: datetime = None) -> Dict[str, Any]:
        """Analyze events within different time windows"""
        if reference_date is None:
            reference_date = datetime.now()
        
        if not events:
            return {
                'reference_date': reference_date.isoformat(),
                'total_events': 0,
                'time_window_analysis': {},
                'risk_score': 0,
                'risk_level': 'low',
                'methodology': 'time_window_events'
            }
        
        window_analysis = {}
        total_weighted_score = 0
        
        for window_name, days in self.time_windows.items():
            window_start = reference_date - timedelta(days=days)
            
            # Filter events in this time window
            window_events = []
            for event in events:
                event_date = event.get('published_date')
                if isinstance(event_date, str):
                    event_date = datetime.fromisoformat(event_date.replace('Z', '+00:00'))
                
                if event_date >= window_start:
                    window_events.append(event)
            
            # Analyze events in this window
            window_stats = self._analyze_window_events(window_events, window_name)
            window_analysis[window_name] = window_stats
            
            # Add to weighted score
            decay_factor = self.risk_decay_factors[window_name]
            total_weighted_score += window_stats['window_score'] * decay_factor
        
        # Determine overall risk level
        if total_weighted_score >= 70:
            risk_level = 'critical'
        elif total_weighted_score >= 50:
            risk_level = 'high'
        elif total_weighted_score >= 25:
            risk_level = 'medium'
        else:
            risk_level = 'low'
        
        return {
            'reference_date': reference_date.isoformat(),
            'total_events': len(events),
            'time_window_analysis': window_analysis,
            'weighted_risk_score': round(total_weighted_score, 2),
            'risk_level': risk_level,
            'methodology': 'time_window_events'
        }
    
    def analyze_schedules_by_time_window(self, schedules: List[Dict[str, Any]], 
                                       reference_date: datetime = None) -> Dict[str, Any]:
        """Analyze schedules within different time windows"""
        if reference_date is None:
            reference_date = datetime.now()
        
        if not schedules:
            return {
                'reference_date': reference_date.isoformat(),
                'total_schedules': 0,
                'time_window_analysis': {},
                'risk_score': 0,
                'risk_level': 'low',
                'methodology': 'time_window_schedules'
            }
        
        window_analysis = {}
        total_weighted_score = 0
        
        for window_name, days in self.time_windows.items():
            window_end = reference_date + timedelta(days=days)
            
            # Filter schedules in this time window
            window_schedules = []
            overdue_schedules = []
            
            for schedule in schedules:
                delivery_date = schedule.get('delivery_date')
                if isinstance(delivery_date, str):
                    delivery_date = datetime.fromisoformat(delivery_date.replace('Z', '+00:00'))
                
                # Check if delivery is within this window
                if reference_date <= delivery_date <= window_end:
                    window_schedules.append(schedule)
                
                # Check if already overdue
                if delivery_date < reference_date and schedule.get('status') in ['delayed', 'at_risk']:
                    overdue_schedules.append(schedule)
            
            # Analyze schedules in this window
            window_stats = self._analyze_window_schedules(window_schedules, overdue_schedules, window_name)
            window_analysis[window_name] = window_stats
            
            # Add to weighted score
            decay_factor = self.risk_decay_factors[window_name]
            total_weighted_score += window_stats['window_score'] * decay_factor
        
        # Determine overall risk level
        if total_weighted_score >= 70:
            risk_level = 'critical'
        elif total_weighted_score >= 50:
            risk_level = 'high'
        elif total_weighted_score >= 25:
            risk_level = 'medium'
        else:
            risk_level = 'low'
        
        return {
            'reference_date': reference_date.isoformat(),
            'total_schedules': len(schedules),
            'time_window_analysis': window_analysis,
            'weighted_risk_score': round(total_weighted_score, 2),
            'risk_level': risk_level,
            'methodology': 'time_window_schedules'
        }
    
    def _analyze_window_events(self, events: List[Dict[str, Any]], window_name: str) -> Dict[str, Any]:
        """Analyze events within a specific time window"""
        total_events = len(events)
        
        if total_events == 0:
            return {
                'window_name': window_name,
                'total_events': 0,
                'high_impact_events': 0,
                'window_score': 0,
                'impact_distribution': {'low': 0, 'medium': 0, 'high': 0}
            }
        
        # Count by impact level
        impact_counts = {'low': 0, 'medium': 0, 'high': 0}
        for event in events:
            impact_level = event.get('impact_level', 'medium')
            impact_counts[impact_level] += 1
        
        # Calculate window score
        window_score = (
            impact_counts['low'] * 1 +
            impact_counts['medium'] * 3 +
            impact_counts['high'] * 5
        )
        
        return {
            'window_name': window_name,
            'total_events': total_events,
            'high_impact_events': impact_counts['high'],
            'window_score': window_score,
            'impact_distribution': impact_counts
        }
    
    def _analyze_window_schedules(self, window_schedules: List[Dict[str, Any]], 
                                overdue_schedules: List[Dict[str, Any]], 
                                window_name: str) -> Dict[str, Any]:
        """Analyze schedules within a specific time window"""
        total_window_schedules = len(window_schedules)
        total_overdue = len(overdue_schedules)
        
        # Count at-risk schedules in window
        at_risk_count = sum(1 for s in window_schedules if s.get('status') == 'at_risk')
        high_priority_count = sum(1 for s in window_schedules if s.get('priority') == 'high')
        
        # Calculate window score
        window_score = (
            total_overdue * 5 +      # Overdue schedules have high impact
            at_risk_count * 3 +      # At-risk schedules have medium impact
            high_priority_count * 2   # High priority schedules have some impact
        )
        
        return {
            'window_name': window_name,
            'window_schedules': total_window_schedules,
            'overdue_schedules': total_overdue,
            'at_risk_schedules': at_risk_count,
            'high_priority_schedules': high_priority_count,
            'window_score': window_score
        }
    
    def analyze_trend_over_time(self, events: List[Dict[str, Any]], 
                              days_back: int = 30) -> Dict[str, Any]:
        """Analyze trends over time periods"""
        if not events:
            return {
                'trend_analysis': 'insufficient_data',
                'daily_counts': [],
                'trend_direction': 'stable',
                'methodology': 'trend_analysis'
            }
        
        reference_date = datetime.now()
        daily_counts = []
        
        # Count events per day for the specified period
        for i in range(days_back):
            day_start = reference_date - timedelta(days=i+1)
            day_end = day_start + timedelta(days=1)
            
            day_events = []
            for event in events:
                event_date = event.get('published_date')
                if isinstance(event_date, str):
                    event_date = datetime.fromisoformat(event_date.replace('Z', '+00:00'))
                
                if day_start <= event_date < day_end:
                    day_events.append(event)
            
            daily_counts.append({
                'date': day_start.strftime('%Y-%m-%d'),
                'event_count': len(day_events),
                'high_impact_count': sum(1 for e in day_events if e.get('impact_level') == 'high')
            })
        
        # Analyze trend
        if len(daily_counts) >= 7:
            recent_avg = sum(d['event_count'] for d in daily_counts[:7]) / 7
            older_avg = sum(d['event_count'] for d in daily_counts[-7:]) / 7
            
            if recent_avg > older_avg * 1.2:
                trend_direction = 'increasing'
            elif recent_avg < older_avg * 0.8:
                trend_direction = 'decreasing'
            else:
                trend_direction = 'stable'
        else:
            trend_direction = 'insufficient_data'
        
        return {
            'trend_analysis': 'completed',
            'daily_counts': daily_counts,
            'trend_direction': trend_direction,
            'recent_average': round(recent_avg, 2) if len(daily_counts) >= 7 else 0,
            'older_average': round(older_avg, 2) if len(daily_counts) >= 7 else 0,
            'methodology': 'trend_analysis'
        }

class TestTimeWindowAnalysis(unittest.TestCase):
    """Test cases for time window analysis"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.generator = TestDataGenerator()
        self.analyzer = TimeWindowAnalyzer()
        self.config = TestConfig()
    
    def test_events_time_window_analysis(self):
        """Test time window analysis for events"""
        # Generate events with different dates
        events = self.generator.generate_news_events(count=20)
        
        result = self.analyzer.analyze_events_by_time_window(events)
        
        # Verify structure
        self.assertIsInstance(result, dict)
        self.assertEqual(result['total_events'], 20)
        self.assertIn('time_window_analysis', result)
        self.assertIn('weighted_risk_score', result)
        self.assertIn('risk_level', result)
        
        # Check all time windows are analyzed
        for window_name in self.analyzer.time_windows.keys():
            self.assertIn(window_name, result['time_window_analysis'])
        
        print(f"✓ Events Time Window Analysis: {result['total_events']} events")
        print(f"  Weighted risk score: {result['weighted_risk_score']}, Risk level: {result['risk_level']}")
        
        # Print window breakdown
        for window_name, window_data in result['time_window_analysis'].items():
            print(f"  {window_name}: {window_data['total_events']} events, score: {window_data['window_score']}")
    
    def test_schedules_time_window_analysis(self):
        """Test time window analysis for schedules"""
        # Generate schedules with different delivery dates
        schedules = self.generator.generate_schedule_data(count=25)
        
        result = self.analyzer.analyze_schedules_by_time_window(schedules)
        
        # Verify structure
        self.assertIsInstance(result, dict)
        self.assertEqual(result['total_schedules'], 25)
        self.assertIn('time_window_analysis', result)
        self.assertIn('weighted_risk_score', result)
        self.assertIn('risk_level', result)
        
        print(f"✓ Schedules Time Window Analysis: {result['total_schedules']} schedules")
        print(f"  Weighted risk score: {result['weighted_risk_score']}, Risk level: {result['risk_level']}")
        
        # Print window breakdown
        for window_name, window_data in result['time_window_analysis'].items():
            print(f"  {window_name}: {window_data['window_schedules']} schedules, "
                  f"{window_data['overdue_schedules']} overdue, score: {window_data['window_score']}")
    
    def test_trend_analysis(self):
        """Test trend analysis over time"""
        # Generate events with dates spread over time
        events = self.generator.generate_news_events(count=30)
        
        result = self.analyzer.analyze_trend_over_time(events, days_back=14)
        
        # Verify structure
        self.assertIsInstance(result, dict)
        self.assertIn('trend_direction', result)
        self.assertIn('daily_counts', result)
        
        # Verify daily counts
        self.assertEqual(len(result['daily_counts']), 14)
        
        print(f"✓ Trend Analysis: Direction = {result['trend_direction']}")
        if result['trend_analysis'] == 'completed':
            print(f"  Recent average: {result['recent_average']}, Older average: {result['older_average']}")
    
    def test_scenario_based_time_analysis(self):
        """Test time window analysis on different scenarios"""
        for scenario_name in ['low_risk', 'medium_risk', 'high_risk']:
            with self.subTest(scenario=scenario_name):
                data = self.generator.generate_scenario_data(scenario_name)
                
                # Analyze events
                events_result = self.analyzer.analyze_events_by_time_window(data['news_events'])
                
                # Analyze schedules
                schedules_result = self.analyzer.analyze_schedules_by_time_window(data['schedules'])
                
                print(f"✓ {scenario_name.title()} Scenario Time Analysis:")
                print(f"  Events: {events_result['risk_level']} risk (score: {events_result['weighted_risk_score']})")
                print(f"  Schedules: {schedules_result['risk_level']} risk (score: {schedules_result['weighted_risk_score']})")
    
    def test_empty_data_time_analysis(self):
        """Test time window analysis with empty data"""
        # Test empty events
        events_result = self.analyzer.analyze_events_by_time_window([])
        self.assertEqual(events_result['total_events'], 0)
        self.assertEqual(events_result['risk_level'], 'low')
        
        # Test empty schedules
        schedules_result = self.analyzer.analyze_schedules_by_time_window([])
        self.assertEqual(schedules_result['total_schedules'], 0)
        self.assertEqual(schedules_result['risk_level'], 'low')
        
        print("✓ Empty data time window analysis works correctly")
    
    def test_custom_reference_date(self):
        """Test time window analysis with custom reference date"""
        events = self.generator.generate_news_events(count=10)
        custom_date = datetime.now() - timedelta(days=5)
        
        result = self.analyzer.analyze_events_by_time_window(events, reference_date=custom_date)
        
        # Verify custom reference date is used
        self.assertEqual(result['reference_date'], custom_date.isoformat())
        
        print(f"✓ Custom reference date analysis works correctly")

if __name__ == '__main__':
    unittest.main(verbosity=2)
