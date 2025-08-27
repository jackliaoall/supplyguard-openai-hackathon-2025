"""
Trade Route Analysis Tests
Tests for traditional trade route risk analysis
"""
import sys
import os
import unittest
from typing import List, Dict, Any, Tuple

# Add parent directories to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from test.utils.test_data_generator import TestDataGenerator
from test.test_config import TestConfig

class TradeRouteAnalyzer:
    """Traditional trade route analysis methods"""
    
    def __init__(self):
        self.config = TestConfig()
        
        # Define trade route risk factors
        self.country_risk_scores = {
            'United States': 20, 'Germany': 15, 'Japan': 18, 'United Kingdom': 22,
            'France': 25, 'Canada': 18, 'South Korea': 30, 'Italy': 35,
            'China': 45, 'India': 50, 'Russia': 70, 'Iran': 85,
            'North Korea': 95, 'Venezuela': 80, 'Syria': 90
        }
        
        # Regional risk multipliers
        self.regional_risks = {
            'North America': 1.0,
            'Western Europe': 1.1,
            'East Asia': 1.3,
            'Middle East': 1.8,
            'Eastern Europe': 1.5,
            'South America': 1.4,
            'Africa': 1.6,
            'Southeast Asia': 1.3
        }
        
        # Trade route complexity factors
        self.route_complexity_factors = {
            'direct': 1.0,          # Direct country-to-country
            'single_transit': 1.2,  # One transit country
            'multi_transit': 1.5,   # Multiple transit countries
            'high_risk_transit': 2.0 # Transit through high-risk areas
        }
    
    def analyze_country_pair_risk(self, origin_country: str, destination_country: str) -> Dict[str, Any]:
        """Analyze risk for a specific country pair"""
        origin_risk = self.country_risk_scores.get(origin_country, 40)  # Default medium risk
        destination_risk = self.country_risk_scores.get(destination_country, 40)
        
        # Calculate combined risk (weighted average)
        combined_risk = (origin_risk + destination_risk) / 2
        
        # Determine risk level
        if combined_risk >= 70:
            risk_level = 'critical'
        elif combined_risk >= 50:
            risk_level = 'high'
        elif combined_risk >= 30:
            risk_level = 'medium'
        else:
            risk_level = 'low'
        
        return {
            'origin_country': origin_country,
            'destination_country': destination_country,
            'origin_risk_score': origin_risk,
            'destination_risk_score': destination_risk,
            'combined_risk_score': round(combined_risk, 2),
            'risk_level': risk_level,
            'methodology': 'country_pair_analysis'
        }
    
    def analyze_equipment_trade_routes(self, equipment_list: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze trade route risks for equipment list"""
        if not equipment_list:
            return {
                'total_equipment': 0,
                'route_analysis': {},
                'risk_distribution': {},
                'high_risk_routes': [],
                'methodology': 'trade_route_analysis'
            }
        
        route_risks = {}
        risk_distribution = {'low': 0, 'medium': 0, 'high': 0, 'critical': 0}
        high_risk_routes = []
        total_risk_score = 0
        
        for equipment in equipment_list:
            origin = equipment.get('manufacturing_country', 'Unknown')
            destination = equipment.get('destination_country', 'Unknown')
            
            if origin == 'Unknown' or destination == 'Unknown':
                continue
            
            route_key = f"{origin} → {destination}"
            
            if route_key not in route_risks:
                # Analyze this route
                route_analysis = self.analyze_country_pair_risk(origin, destination)
                route_risks[route_key] = {
                    'analysis': route_analysis,
                    'equipment_count': 0,
                    'equipment_ids': [],
                    'total_value': 0
                }
            
            # Add equipment to route
            route_risks[route_key]['equipment_count'] += 1
            route_risks[route_key]['equipment_ids'].append(equipment.get('id'))
            route_risks[route_key]['total_value'] += equipment.get('cost', 0)
            
            # Update risk distribution
            risk_level = route_risks[route_key]['analysis']['risk_level']
            risk_distribution[risk_level] += 1
            total_risk_score += route_risks[route_key]['analysis']['combined_risk_score']
            
            # Track high-risk routes
            if risk_level in ['high', 'critical']:
                route_info = {
                    'route': route_key,
                    'risk_level': risk_level,
                    'risk_score': route_risks[route_key]['analysis']['combined_risk_score'],
                    'equipment_count': route_risks[route_key]['equipment_count'],
                    'total_value': route_risks[route_key]['total_value']
                }
                
                # Update existing entry or add new one
                existing = next((r for r in high_risk_routes if r['route'] == route_key), None)
                if existing:
                    existing.update(route_info)
                else:
                    high_risk_routes.append(route_info)
        
        # Calculate overall metrics
        total_equipment = len(equipment_list)
        average_risk_score = total_risk_score / total_equipment if total_equipment > 0 else 0
        
        # Determine overall risk level
        if average_risk_score >= 70:
            overall_risk = 'critical'
        elif average_risk_score >= 50:
            overall_risk = 'high'
        elif average_risk_score >= 30:
            overall_risk = 'medium'
        else:
            overall_risk = 'low'
        
        return {
            'total_equipment': total_equipment,
            'total_routes': len(route_risks),
            'average_risk_score': round(average_risk_score, 2),
            'overall_risk_level': overall_risk,
            'route_analysis': route_risks,
            'risk_distribution': risk_distribution,
            'high_risk_routes': sorted(high_risk_routes, key=lambda x: x['risk_score'], reverse=True),
            'high_risk_route_count': len(high_risk_routes),
            'methodology': 'trade_route_analysis'
        }
    
    def identify_alternative_routes(self, origin_country: str, destination_country: str, 
                                  max_alternatives: int = 3) -> List[Dict[str, Any]]:
        """Identify alternative trade routes with lower risk"""
        # This is a simplified implementation
        # In reality, this would use geographic and trade data
        
        # Get direct route risk
        direct_route = self.analyze_country_pair_risk(origin_country, destination_country)
        
        # Generate some alternative routes through transit countries
        potential_transit_countries = [
            'Germany', 'United States', 'Singapore', 'United Kingdom', 'Netherlands'
        ]
        
        alternatives = []
        
        for transit in potential_transit_countries:
            if transit == origin_country or transit == destination_country:
                continue
            
            # Calculate route through transit country
            leg1 = self.analyze_country_pair_risk(origin_country, transit)
            leg2 = self.analyze_country_pair_risk(transit, destination_country)
            
            # Combined risk with complexity factor
            combined_risk = (leg1['combined_risk_score'] + leg2['combined_risk_score']) / 2
            combined_risk *= self.route_complexity_factors['single_transit']
            
            if combined_risk >= 70:
                risk_level = 'critical'
            elif combined_risk >= 50:
                risk_level = 'high'
            elif combined_risk >= 30:
                risk_level = 'medium'
            else:
                risk_level = 'low'
            
            alternatives.append({
                'route': f"{origin_country} → {transit} → {destination_country}",
                'transit_country': transit,
                'combined_risk_score': round(combined_risk, 2),
                'risk_level': risk_level,
                'risk_improvement': round(direct_route['combined_risk_score'] - combined_risk, 2)
            })
        
        # Sort by risk score and return top alternatives
        alternatives.sort(key=lambda x: x['combined_risk_score'])
        
        return {
            'direct_route': direct_route,
            'alternatives': alternatives[:max_alternatives],
            'best_alternative': alternatives[0] if alternatives else None
        }

class TestTradeRouteAnalysis(unittest.TestCase):
    """Test cases for trade route analysis"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.generator = TestDataGenerator()
        self.analyzer = TradeRouteAnalyzer()
        self.config = TestConfig()
    
    def test_country_pair_risk_analysis(self):
        """Test risk analysis for country pairs"""
        test_pairs = [
            ('United States', 'Germany'),      # Low risk
            ('China', 'United States'),        # Medium risk
            ('Iran', 'North Korea'),          # High risk
        ]
        
        for origin, destination in test_pairs:
            with self.subTest(origin=origin, destination=destination):
                result = self.analyzer.analyze_country_pair_risk(origin, destination)
                
                # Verify structure
                self.assertIsInstance(result, dict)
                self.assertEqual(result['origin_country'], origin)
                self.assertEqual(result['destination_country'], destination)
                self.assertIn('combined_risk_score', result)
                self.assertIn('risk_level', result)
                
                # Verify risk level is valid
                self.assertIn(result['risk_level'], ['low', 'medium', 'high', 'critical'])
                
                print(f"✓ {origin} → {destination}: {result['risk_level']} risk (score: {result['combined_risk_score']})")
    
    def test_equipment_trade_route_analysis(self):
        """Test trade route analysis for equipment"""
        # Generate equipment with specific countries
        equipment_data = self.generator.generate_equipment_data(count=15)
        
        result = self.analyzer.analyze_equipment_trade_routes(equipment_data)
        
        # Verify results
        self.assertIsInstance(result, dict)
        self.assertEqual(result['total_equipment'], 15)
        self.assertIn('route_analysis', result)
        self.assertIn('risk_distribution', result)
        self.assertIn('high_risk_routes', result)
        
        print(f"✓ Equipment Route Analysis: {result['total_equipment']} equipment across {result['total_routes']} routes")
        print(f"  Overall risk: {result['overall_risk_level']} (score: {result['average_risk_score']})")
        print(f"  High-risk routes: {result['high_risk_route_count']}")
        
        # Print risk distribution
        risk_dist = result['risk_distribution']
        print(f"  Risk distribution: Low={risk_dist['low']}, Medium={risk_dist['medium']}, High={risk_dist['high']}, Critical={risk_dist['critical']}")
    
    def test_alternative_route_identification(self):
        """Test identification of alternative routes"""
        test_routes = [
            ('China', 'United States'),
            ('Iran', 'Germany'),
            ('Russia', 'Japan')
        ]
        
        for origin, destination in test_routes:
            with self.subTest(origin=origin, destination=destination):
                result = self.analyzer.identify_alternative_routes(origin, destination)
                
                # Verify structure
                self.assertIsInstance(result, dict)
                self.assertIn('direct_route', result)
                self.assertIn('alternatives', result)
                
                direct_risk = result['direct_route']['combined_risk_score']
                
                print(f"✓ Alternative Routes for {origin} → {destination}:")
                print(f"  Direct route risk: {direct_risk}")
                
                if result['alternatives']:
                    best_alt = result['alternatives'][0]
                    print(f"  Best alternative: {best_alt['route']} (risk: {best_alt['combined_risk_score']})")
                    print(f"  Risk improvement: {best_alt['risk_improvement']}")
    
    def test_scenario_based_route_analysis(self):
        """Test route analysis on different scenarios"""
        for scenario_name in ['low_risk', 'medium_risk', 'high_risk']:
            with self.subTest(scenario=scenario_name):
                data = self.generator.generate_scenario_data(scenario_name)
                
                result = self.analyzer.analyze_equipment_trade_routes(data['equipment'])
                
                # Verify results
                self.assertIsInstance(result, dict)
                self.assertGreater(result['total_equipment'], 0)
                self.assertIn('overall_risk_level', result)
                
                print(f"✓ {scenario_name.title()} Scenario Routes: {result['total_equipment']} equipment, "
                      f"risk: {result['overall_risk_level']} (score: {result['average_risk_score']})")
    
    def test_empty_equipment_list(self):
        """Test route analysis with empty equipment list"""
        result = self.analyzer.analyze_equipment_trade_routes([])
        
        self.assertEqual(result['total_equipment'], 0)
        self.assertEqual(result['total_routes'], 0)
        self.assertEqual(len(result['high_risk_routes']), 0)
        
        print("✓ Empty equipment list handling works correctly")
    
    def test_unknown_countries_handling(self):
        """Test handling of unknown countries"""
        equipment_with_unknown = [
            {
                'id': 1,
                'manufacturing_country': 'Unknown',
                'destination_country': 'Germany',
                'cost': 10000
            },
            {
                'id': 2,
                'manufacturing_country': 'China',
                'destination_country': 'Unknown',
                'cost': 20000
            }
        ]
        
        result = self.analyzer.analyze_equipment_trade_routes(equipment_with_unknown)
        
        # Should handle unknown countries gracefully
        self.assertEqual(result['total_equipment'], 2)
        self.assertEqual(result['total_routes'], 0)  # No valid routes
        
        print("✓ Unknown countries handling works correctly")

if __name__ == '__main__':
    unittest.main(verbosity=2)
