#!/usr/bin/env python3
"""
SupplyGuard Comprehensive Test Runner
Runs all traditional and AI analysis tests with detailed reporting
"""
import sys
import os
import time
import argparse
from datetime import datetime
from typing import Dict, List, Any

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# Import test modules
from test.traditional_analysis.test_statistical_analysis import TestStatisticalAnalysis
from test.traditional_analysis.test_threshold_analysis import TestThresholdAnalysis
from test.traditional_analysis.test_keyword_matching import TestKeywordMatching
from test.traditional_analysis.test_trade_route_analysis import TestTradeRouteAnalysis
from test.traditional_analysis.test_time_window_analysis import TestTimeWindowAnalysis
from test.ai_analysis.test_ai_strategies import TestAIStrategies
from test.utils.test_data_generator import TestDataGenerator
from test.test_config import TestConfig

class ComprehensiveTestRunner:
    """Comprehensive test runner for all SupplyGuard analysis strategies"""
    
    def __init__(self, debug: bool = False):
        self.debug = debug
        self.config = TestConfig()
        self.generator = TestDataGenerator()
        self.results = {
            'traditional_tests': {},
            'ai_tests': {},
            'comparison_results': {},
            'summary': {}
        }
        self.start_time = None
        self.end_time = None
    
    def run_all_tests(self) -> Dict[str, Any]:
        """Run all tests and generate comprehensive report"""
        print("🚀 Starting SupplyGuard Comprehensive Test Suite")
        print("=" * 60)
        
        self.start_time = time.time()
        
        try:
            # Run traditional analysis tests
            print("\n📊 Running Traditional Analysis Tests...")
            self._run_traditional_tests()
            
            # Run AI analysis tests
            print("\n🤖 Running AI Analysis Tests...")
            self._run_ai_tests()
            
            # Run comparison tests
            print("\n⚖️  Running Comparison Tests...")
            self._run_comparison_tests()
            
            # Generate summary
            self._generate_summary()
            
        except Exception as e:
            print(f"❌ Test suite failed with error: {str(e)}")
            if self.debug:
                import traceback
                traceback.print_exc()
        
        self.end_time = time.time()
        
        # Print final report
        self._print_final_report()
        
        return self.results
    
    def _run_traditional_tests(self):
        """Run all traditional analysis tests"""
        traditional_tests = [
            ('Statistical Analysis', TestStatisticalAnalysis),
            ('Threshold Analysis', TestThresholdAnalysis),
            ('Keyword Matching', TestKeywordMatching),
            ('Trade Route Analysis', TestTradeRouteAnalysis),
            ('Time Window Analysis', TestTimeWindowAnalysis)
        ]
        
        for test_name, test_class in traditional_tests:
            print(f"\n  🔍 Testing {test_name}...")
            
            try:
                # Create test instance
                test_instance = test_class()
                test_instance.setUp()
                
                # Run key test methods
                test_results = self._run_test_methods(test_instance, test_name)
                self.results['traditional_tests'][test_name] = test_results
                
                print(f"    ✅ {test_name}: {test_results['passed']}/{test_results['total']} tests passed")
                
            except Exception as e:
                print(f"    ❌ {test_name}: Failed with error: {str(e)}")
                self.results['traditional_tests'][test_name] = {
                    'status': 'failed',
                    'error': str(e),
                    'passed': 0,
                    'total': 0
                }
    
    def _run_ai_tests(self):
        """Run all AI analysis tests"""
        print(f"\n  🧠 Testing AI Strategies...")
        
        try:
            # Create test instance
            test_instance = TestAIStrategies()
            test_instance.setUp()
            
            # Run AI test methods
            test_results = self._run_test_methods(test_instance, 'AI Strategies')
            self.results['ai_tests']['AI Strategies'] = test_results
            
            print(f"    ✅ AI Strategies: {test_results['passed']}/{test_results['total']} tests passed")
            
        except Exception as e:
            print(f"    ❌ AI Strategies: Failed with error: {str(e)}")
            self.results['ai_tests']['AI Strategies'] = {
                'status': 'failed',
                'error': str(e),
                'passed': 0,
                'total': 0
            }
    
    def _run_comparison_tests(self):
        """Run comparison tests between traditional and AI methods"""
        print(f"\n  📈 Running Method Comparisons...")
        
        try:
            # Generate test scenarios
            scenarios = ['low_risk', 'medium_risk', 'high_risk']
            comparison_results = []
            
            for scenario in scenarios:
                print(f"    🎯 Testing {scenario} scenario...")
                
                # Generate scenario data
                data = self.generator.generate_scenario_data(scenario)
                
                # Run traditional analysis
                from test.traditional_analysis.test_statistical_analysis import StatisticalAnalyzer
                traditional_analyzer = StatisticalAnalyzer()
                delay_stats = traditional_analyzer.calculate_delay_statistics(data['schedules'])
                event_stats = traditional_analyzer.calculate_event_statistics(data['news_events'])
                traditional_result = traditional_analyzer.calculate_risk_score_from_statistics(delay_stats, event_stats)
                
                # Run AI analysis
                from test.ai_analysis.test_ai_strategies import AIStrategyTester
                ai_tester = AIStrategyTester()
                ai_result = ai_tester.test_ai_scheduler_analysis(data['schedules'])
                
                # Compare results
                comparison = ai_tester.compare_ai_vs_traditional(ai_result, traditional_result)
                comparison['scenario'] = scenario
                comparison_results.append(comparison)
                
                print(f"      Agreement: {comparison['comparison']['agreement_level']}")
            
            self.results['comparison_results'] = comparison_results
            print(f"    ✅ Completed {len(comparison_results)} scenario comparisons")
            
        except Exception as e:
            print(f"    ❌ Comparison tests failed: {str(e)}")
            self.results['comparison_results'] = {'error': str(e)}
    
    def _run_test_methods(self, test_instance, test_name: str) -> Dict[str, Any]:
        """Run test methods for a test instance"""
        test_methods = [method for method in dir(test_instance) if method.startswith('test_')]
        
        passed = 0
        total = len(test_methods)
        errors = []
        
        for method_name in test_methods:
            try:
                method = getattr(test_instance, method_name)
                method()
                passed += 1
                if self.debug:
                    print(f"      ✓ {method_name}")
            except Exception as e:
                errors.append(f"{method_name}: {str(e)}")
                if self.debug:
                    print(f"      ✗ {method_name}: {str(e)}")
        
        return {
            'status': 'passed' if passed == total else 'partial',
            'passed': passed,
            'total': total,
            'errors': errors
        }
    
    def _generate_summary(self):
        """Generate test summary statistics"""
        # Count traditional test results
        traditional_passed = 0
        traditional_total = 0
        
        for test_name, results in self.results['traditional_tests'].items():
            traditional_passed += results.get('passed', 0)
            traditional_total += results.get('total', 0)
        
        # Count AI test results
        ai_passed = 0
        ai_total = 0
        
        for test_name, results in self.results['ai_tests'].items():
            ai_passed += results.get('passed', 0)
            ai_total += results.get('total', 0)
        
        # Count comparison results
        comparison_count = len(self.results.get('comparison_results', []))
        
        # Calculate execution time
        execution_time = self.end_time - self.start_time if self.end_time and self.start_time else 0
        
        self.results['summary'] = {
            'traditional_tests': {
                'passed': traditional_passed,
                'total': traditional_total,
                'success_rate': round((traditional_passed / traditional_total * 100) if traditional_total > 0 else 0, 2)
            },
            'ai_tests': {
                'passed': ai_passed,
                'total': ai_total,
                'success_rate': round((ai_passed / ai_total * 100) if ai_total > 0 else 0, 2)
            },
            'comparison_tests': {
                'completed': comparison_count,
                'scenarios_tested': comparison_count
            },
            'execution_time': round(execution_time, 2),
            'timestamp': datetime.now().isoformat()
        }
    
    def _print_final_report(self):
        """Print comprehensive final report"""
        print("\n" + "=" * 60)
        print("📋 COMPREHENSIVE TEST REPORT")
        print("=" * 60)
        
        summary = self.results['summary']
        
        # Traditional tests summary
        trad = summary['traditional_tests']
        print(f"\n📊 Traditional Analysis Tests:")
        print(f"   Passed: {trad['passed']}/{trad['total']} ({trad['success_rate']}%)")
        
        # AI tests summary
        ai = summary['ai_tests']
        print(f"\n🤖 AI Analysis Tests:")
        print(f"   Passed: {ai['passed']}/{ai['total']} ({ai['success_rate']}%)")
        
        # Comparison tests summary
        comp = summary['comparison_tests']
        print(f"\n⚖️  Comparison Tests:")
        print(f"   Scenarios: {comp['completed']} completed")
        
        # Overall summary
        total_passed = trad['passed'] + ai['passed']
        total_tests = trad['total'] + ai['total']
        overall_success = round((total_passed / total_tests * 100) if total_tests > 0 else 0, 2)
        
        print(f"\n🎯 Overall Results:")
        print(f"   Total Tests: {total_passed}/{total_tests} ({overall_success}%)")
        print(f"   Execution Time: {summary['execution_time']} seconds")
        print(f"   Timestamp: {summary['timestamp']}")
        
        # Status indicator
        if overall_success >= 90:
            print(f"\n✅ Test Suite: EXCELLENT ({overall_success}%)")
        elif overall_success >= 75:
            print(f"\n✅ Test Suite: GOOD ({overall_success}%)")
        elif overall_success >= 50:
            print(f"\n⚠️  Test Suite: NEEDS ATTENTION ({overall_success}%)")
        else:
            print(f"\n❌ Test Suite: CRITICAL ISSUES ({overall_success}%)")
        
        print("=" * 60)
    
    def save_report(self, filename: str = None):
        """Save test report to file"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"test/reports/test_report_{timestamp}.json"
        
        # Ensure reports directory exists
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        import json
        with open(filename, 'w') as f:
            json.dump(self.results, f, indent=2, default=str)
        
        print(f"📄 Test report saved to: {filename}")

def main():
    """Main function to run tests"""
    parser = argparse.ArgumentParser(description='Run SupplyGuard comprehensive tests')
    parser.add_argument('--debug', action='store_true', help='Enable debug output')
    parser.add_argument('--save-report', action='store_true', help='Save test report to file')
    
    args = parser.parse_args()
    
    # Run tests
    runner = ComprehensiveTestRunner(debug=args.debug)
    results = runner.run_all_tests()
    
    # Save report if requested
    if args.save_report:
        runner.save_report()
    
    # Exit with appropriate code
    summary = results.get('summary', {})
    traditional_success = summary.get('traditional_tests', {}).get('success_rate', 0)
    ai_success = summary.get('ai_tests', {}).get('success_rate', 0)
    overall_success = (traditional_success + ai_success) / 2
    
    sys.exit(0 if overall_success >= 75 else 1)

if __name__ == '__main__':
    main()
