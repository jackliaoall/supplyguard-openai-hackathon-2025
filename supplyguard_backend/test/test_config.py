"""
Test Configuration
Centralized configuration for all tests
"""
import os
from datetime import datetime, timedelta

class TestConfig:
    """Test configuration settings"""
    
    # Test database settings
    TEST_DATABASE_URI = "sqlite:///:memory:"
    
    # Test data settings
    SAMPLE_EQUIPMENT_COUNT = 20
    SAMPLE_SCHEDULE_COUNT = 30
    SAMPLE_NEWS_EVENT_COUNT = 50
    SAMPLE_RISK_ASSESSMENT_COUNT = 25
    
    # Risk analysis thresholds for testing
    RISK_THRESHOLDS = {
        'low': 30,
        'medium': 60,
        'high': 80,
        'critical': 90
    }
    
    # Time windows for analysis
    TIME_WINDOWS = {
        'recent': 7,      # days
        'short_term': 30, # days
        'medium_term': 90, # days
        'long_term': 365   # days
    }
    
    # Keywords for different risk categories
    RISK_KEYWORDS = {
        'political': [
            'election', 'government', 'policy', 'regulation', 'sanction', 
            'embargo', 'trade war', 'diplomatic', 'political', 'conflict', 
            'protest', 'coup', 'instability'
        ],
        'logistics': [
            'port', 'shipping', 'transport', 'logistics', 'delay', 
            'congestion', 'strike', 'blockade', 'route', 'infrastructure'
        ],
        'tariff': [
            'tariff', 'trade', 'customs', 'duty', 'import', 'export',
            'trade war', 'wto', 'agreement', 'quota'
        ],
        'schedule': [
            'delay', 'postpone', 'schedule', 'timeline', 'deadline',
            'delivery', 'shipment', 'production', 'manufacturing'
        ]
    }
    
    # Countries for testing trade route analysis
    TEST_COUNTRIES = [
        'United States', 'China', 'Germany', 'Japan', 'United Kingdom',
        'France', 'Italy', 'Canada', 'South Korea', 'India'
    ]
    
    # Equipment types for testing
    EQUIPMENT_TYPES = [
        'Manufacturing Equipment', 'IT Hardware', 'Medical Devices',
        'Automotive Parts', 'Electronics', 'Machinery', 'Tools',
        'Industrial Components', 'Software Systems', 'Laboratory Equipment'
    ]
    
    # Test scenarios for comprehensive testing
    TEST_SCENARIOS = {
        'low_risk': {
            'delayed_schedules_ratio': 0.1,
            'high_impact_events_ratio': 0.1,
            'political_events_ratio': 0.2
        },
        'medium_risk': {
            'delayed_schedules_ratio': 0.3,
            'high_impact_events_ratio': 0.3,
            'political_events_ratio': 0.4
        },
        'high_risk': {
            'delayed_schedules_ratio': 0.6,
            'high_impact_events_ratio': 0.5,
            'political_events_ratio': 0.7
        },
        'critical_risk': {
            'delayed_schedules_ratio': 0.8,
            'high_impact_events_ratio': 0.8,
            'political_events_ratio': 0.9
        }
    }
    
    @classmethod
    def get_test_date_range(cls, days_back=30):
        """Get date range for testing"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days_back)
        return start_date, end_date
    
    @classmethod
    def get_risk_level_from_score(cls, score):
        """Convert risk score to risk level"""
        if score >= cls.RISK_THRESHOLDS['critical']:
            return 'critical'
        elif score >= cls.RISK_THRESHOLDS['high']:
            return 'high'
        elif score >= cls.RISK_THRESHOLDS['medium']:
            return 'medium'
        else:
            return 'low'
