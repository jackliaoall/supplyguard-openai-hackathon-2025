"""
Test Data Generator
Generates realistic test data for analysis testing
"""
import random
import sys
import os
from datetime import datetime, timedelta
from typing import List, Dict, Any

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from test.test_config import TestConfig

class TestDataGenerator:
    """Generates test data for analysis testing"""
    
    def __init__(self):
        self.config = TestConfig()
    
    def generate_equipment_data(self, count: int = None) -> List[Dict[str, Any]]:
        """Generate sample equipment data"""
        if count is None:
            count = self.config.SAMPLE_EQUIPMENT_COUNT
        
        equipment_list = []
        for i in range(count):
            equipment = {
                'id': i + 1,
                'name': f"{random.choice(self.config.EQUIPMENT_TYPES)} {i+1:03d}",
                'type': random.choice(self.config.EQUIPMENT_TYPES),
                'manufacturing_country': random.choice(self.config.TEST_COUNTRIES),
                'destination_country': random.choice(self.config.TEST_COUNTRIES),
                'cost': random.randint(10000, 1000000),
                'priority': random.choice(['low', 'medium', 'high']),
                'status': random.choice(['ordered', 'in_production', 'shipped', 'delivered']),
                'created_at': datetime.now() - timedelta(days=random.randint(1, 365))
            }
            equipment_list.append(equipment)
        
        return equipment_list
    
    def generate_schedule_data(self, equipment_count: int = None, count: int = None) -> List[Dict[str, Any]]:
        """Generate sample schedule data"""
        if count is None:
            count = self.config.SAMPLE_SCHEDULE_COUNT
        if equipment_count is None:
            equipment_count = self.config.SAMPLE_EQUIPMENT_COUNT
        
        schedules = []
        now = datetime.now()
        
        for i in range(count):
            # Create realistic delivery dates
            days_offset = random.randint(-30, 90)  # Past to future deliveries
            delivery_date = now + timedelta(days=days_offset)
            
            # Determine if schedule is delayed
            is_delayed = delivery_date < now and random.random() < 0.3
            
            schedule = {
                'id': i + 1,
                'equipment_id': random.randint(1, equipment_count),
                'delivery_date': delivery_date,
                'expected_date': delivery_date - timedelta(days=random.randint(0, 10)),
                'status': 'delayed' if is_delayed else random.choice(['on_track', 'at_risk', 'completed']),
                'priority': random.choice(['low', 'medium', 'high']),
                'notes': f"Schedule for equipment delivery {i+1}",
                'created_at': now - timedelta(days=random.randint(1, 60))
            }
            schedules.append(schedule)
        
        return schedules
    
    def generate_news_events(self, count: int = None) -> List[Dict[str, Any]]:
        """Generate sample news events"""
        if count is None:
            count = self.config.SAMPLE_NEWS_EVENT_COUNT
        
        events = []
        now = datetime.now()
        
        for i in range(count):
            category = random.choice(['political', 'economic', 'logistics', 'trade'])
            country = random.choice(self.config.TEST_COUNTRIES)
            
            # Generate realistic event titles based on category
            titles = {
                'political': [
                    f"Political tensions rise in {country}",
                    f"New government policies announced in {country}",
                    f"Election results impact trade in {country}",
                    f"Diplomatic relations strained with {country}"
                ],
                'economic': [
                    f"Economic growth slows in {country}",
                    f"Currency fluctuations affect {country}",
                    f"Inflation concerns in {country}",
                    f"Trade deficit increases in {country}"
                ],
                'logistics': [
                    f"Port congestion reported in {country}",
                    f"Transportation strikes in {country}",
                    f"Infrastructure damage in {country}",
                    f"Shipping delays from {country}"
                ],
                'trade': [
                    f"New tariffs imposed by {country}",
                    f"Trade agreement signed with {country}",
                    f"Export restrictions in {country}",
                    f"Import quotas announced in {country}"
                ]
            }
            
            event = {
                'id': i + 1,
                'title': random.choice(titles[category]),
                'content': f"Detailed analysis of {category} situation in {country}. " +
                          f"This event may impact supply chain operations and risk levels.",
                'category': category,
                'country': country,
                'impact_level': random.choice(['low', 'medium', 'high']),
                'published_date': now - timedelta(days=random.randint(0, 90)),
                'source': f"News Source {random.randint(1, 10)}",
                'created_at': now - timedelta(days=random.randint(0, 90))
            }
            events.append(event)
        
        return events
    
    def generate_risk_assessments(self, equipment_count: int = None, count: int = None) -> List[Dict[str, Any]]:
        """Generate sample risk assessments"""
        if count is None:
            count = self.config.SAMPLE_RISK_ASSESSMENT_COUNT
        if equipment_count is None:
            equipment_count = self.config.SAMPLE_EQUIPMENT_COUNT
        
        assessments = []
        now = datetime.now()
        
        for i in range(count):
            risk_score = random.randint(0, 100)
            risk_level = self.config.get_risk_level_from_score(risk_score)
            
            assessment = {
                'id': i + 1,
                'equipment_id': random.randint(1, equipment_count),
                'risk_type': random.choice(['political', 'logistics', 'tariff', 'schedule']),
                'risk_level': risk_level,
                'risk_score': risk_score,
                'description': f"Risk assessment {i+1} - {risk_level} risk detected",
                'recommendations': [
                    f"Monitor {random.choice(['political', 'economic', 'logistics'])} situation",
                    f"Consider alternative {random.choice(['suppliers', 'routes', 'timelines'])}",
                    f"Implement {random.choice(['contingency', 'mitigation', 'monitoring'])} measures"
                ],
                'created_at': now - timedelta(days=random.randint(0, 30)),
                'updated_at': now - timedelta(days=random.randint(0, 7))
            }
            assessments.append(assessment)
        
        return assessments
    
    def generate_scenario_data(self, scenario_name: str) -> Dict[str, List[Dict[str, Any]]]:
        """Generate data for a specific test scenario"""
        if scenario_name not in self.config.TEST_SCENARIOS:
            raise ValueError(f"Unknown scenario: {scenario_name}")
        
        scenario = self.config.TEST_SCENARIOS[scenario_name]
        
        # Generate equipment data
        equipment_data = self.generate_equipment_data()
        
        # Generate schedules with scenario-specific delay ratio
        schedules = self.generate_schedule_data()
        delayed_count = int(len(schedules) * scenario['delayed_schedules_ratio'])
        for i in range(delayed_count):
            schedules[i]['status'] = 'delayed'
            schedules[i]['delivery_date'] = datetime.now() - timedelta(days=random.randint(1, 30))
        
        # Generate news events with scenario-specific ratios
        news_events = self.generate_news_events()
        high_impact_count = int(len(news_events) * scenario['high_impact_events_ratio'])
        political_count = int(len(news_events) * scenario['political_events_ratio'])
        
        for i in range(high_impact_count):
            news_events[i]['impact_level'] = 'high'
        
        for i in range(political_count):
            news_events[i]['category'] = 'political'
        
        # Generate risk assessments
        risk_assessments = self.generate_risk_assessments()
        
        return {
            'equipment': equipment_data,
            'schedules': schedules,
            'news_events': news_events,
            'risk_assessments': risk_assessments,
            'scenario_info': {
                'name': scenario_name,
                'parameters': scenario
            }
        }
