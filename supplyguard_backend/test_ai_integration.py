#!/usr/bin/env python3
"""
Test script for AI integration with OpenRouter
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from src.services.ai_service import AIService

def test_ai_service():
    """Test basic AI service functionality"""
    print("🧪 Testing AI Service...")
    
    try:
        ai_service = AIService()
        
        # Test health check
        print("  ✓ Testing health check...")
        health = ai_service.health_check()
        print(f"    Status: {health.get('status', 'unknown')}")
        
        # Test basic analysis
        print("  ✓ Testing basic analysis...")
        result = ai_service.analyze_with_ai(
            'scheduler',
            'Analyze delivery schedule risks for equipment procurement',
            {'total_schedules': 5, 'delayed_schedules': 2}
        )
        
        print(f"    Risk Level: {result.get('risk_level', 'unknown')}")
        print(f"    Risk Score: {result.get('risk_score', 'unknown')}")
        print(f"    Summary: {result.get('summary', 'No summary')[:100]}...")
        
        return True
        
    except Exception as e:
        print(f"  ❌ AI Service test failed: {str(e)}")
        return False

def test_ai_direct_analysis():
    """Test AI service direct analysis without database dependencies"""
    print("\n🤖 Testing AI Direct Analysis...")

    try:
        ai_service = AIService()

        # Test scheduler analysis
        scheduler_result = ai_service.analyze_with_ai(
            'scheduler',
            'Analyze delivery schedule risks for 5 equipment items with 2 delayed deliveries',
            {
                'total_schedules': 5,
                'delayed_schedules': 2,
                'schedule_data': 'Total: 5, Delayed: 2, Upcoming: 1, Critical: 1'
            }
        )

        print(f"  ✓ Scheduler Analysis:")
        print(f"    Risk Level: {scheduler_result.get('risk_level', 'unknown')}")
        print(f"    Risk Score: {scheduler_result.get('risk_score', 'unknown')}")
        print(f"    Summary: {scheduler_result.get('summary', 'No summary')[:80]}...")

        # Test political analysis
        political_result = ai_service.analyze_with_ai(
            'political',
            'Analyze political risks affecting supply chain in Germany',
            {
                'target_country': 'Germany',
                'total_events': 10,
                'high_impact_events': 3,
                'news_events': 'Analyzing 10 political events, 3 high-impact, 2 recent'
            }
        )

        print(f"  ✓ Political Analysis:")
        print(f"    Risk Level: {political_result.get('risk_level', 'unknown')}")
        print(f"    Risk Score: {political_result.get('risk_score', 'unknown')}")
        print(f"    Summary: {political_result.get('summary', 'No summary')[:80]}...")

        return True

    except Exception as e:
        print(f"  ❌ AI Direct Analysis test failed: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("🚀 Starting AI Integration Tests")
    print("=" * 50)
    
    # Check if API key is configured
    api_key = os.getenv('OPENROUTER_API_KEY', 'sk-or-v1-demo-key-placeholder')
    if api_key == 'sk-or-v1-demo-key-placeholder':
        print("⚠️  Warning: Using placeholder API key. Set OPENROUTER_API_KEY environment variable for real testing.")
        print("   For testing purposes, the system will use fallback responses.")
    else:
        print("✓ API key configured")
    
    print()
    
    # Run tests
    tests = [
        test_ai_service,
        test_ai_direct_analysis
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"🎯 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("✅ All tests passed! AI integration is working correctly.")
    else:
        print("❌ Some tests failed. Check the error messages above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
