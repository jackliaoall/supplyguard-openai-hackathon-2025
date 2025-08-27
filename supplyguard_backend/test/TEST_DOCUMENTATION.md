# SupplyGuard Testing Documentation

## Overview

This document provides comprehensive documentation for the SupplyGuard testing framework, covering both traditional analysis strategies and AI-powered analysis methods.

## Test Structure

```
test/
├── __init__.py                          # Test package initialization
├── test_config.py                       # Test configuration and settings
├── TEST_DOCUMENTATION.md               # This documentation file
├── traditional_analysis/               # Traditional analysis tests
│   ├── test_statistical_analysis.py    # Statistical analysis tests
│   ├── test_threshold_analysis.py      # Threshold-based analysis tests
│   ├── test_keyword_matching.py        # Keyword matching tests
│   ├── test_trade_route_analysis.py    # Trade route analysis tests
│   └── test_time_window_analysis.py    # Time window analysis tests
├── ai_analysis/                        # AI analysis tests
│   └── test_ai_strategies.py           # AI strategy tests and comparisons
├── utils/                              # Test utilities
│   └── test_data_generator.py          # Test data generation utilities
├── data/                               # Test data files (if needed)
├── reports/                            # Test reports and results
└── run_all_tests.py                   # Main test runner
```

## Traditional Analysis Strategies

### 1. Statistical Analysis (`test_statistical_analysis.py`)

**Purpose**: Test statistical methods for risk assessment

**Key Features**:
- **Event Statistics**: Count and categorize news events by impact level
- **Delay Statistics**: Calculate delay percentages and average delay days
- **Risk Score Calculation**: Combine multiple statistical metrics
- **Empty Data Handling**: Graceful handling of missing data

**Test Methods**:
- `test_delay_statistics_calculation()`: Verify delay metric calculations
- `test_event_statistics_calculation()`: Verify event metric calculations
- `test_risk_score_calculation()`: Test risk score derivation from statistics
- `test_empty_data_handling()`: Test edge cases with no data

**Example Output**:
```
✓ Delay Statistics: 6/20 delayed (30.0%)
✓ Event Statistics: 8/30 high-impact (26.67%)
✓ Medium Risk Scenario: Score=45.5, Level=medium
```

### 2. Threshold Analysis (`test_threshold_analysis.py`)

**Purpose**: Test threshold-based risk classification

**Key Features**:
- **Configurable Thresholds**: Define risk levels based on predefined thresholds
- **Multi-Metric Assessment**: Combine delay and event thresholds
- **Boundary Testing**: Test exact threshold values
- **Risk Level Combination**: Merge multiple risk assessments

**Threshold Configuration**:
```python
thresholds = {
    'delay_percentage': {'low': 10, 'medium': 25, 'high': 50, 'critical': 75},
    'high_impact_events': {'low': 2, 'medium': 5, 'high': 10, 'critical': 15},
    'average_delay_days': {'low': 3, 'medium': 7, 'high': 14, 'critical': 30}
}
```

**Test Methods**:
- `test_delay_threshold_analysis()`: Test delay-based thresholds
- `test_event_threshold_analysis()`: Test event-based thresholds
- `test_threshold_boundary_conditions()`: Test exact boundary values
- `test_empty_data_threshold_analysis()`: Test with no data

### 3. Keyword Matching (`test_keyword_matching.py`)

**Purpose**: Test keyword-based risk detection

**Key Features**:
- **Weighted Keywords**: Different risk weights for keyword categories
- **Multi-Category Analysis**: Political, logistics, tariff, and schedule keywords
- **Case-Insensitive Matching**: Robust text processing
- **Risk Aggregation**: Combine keyword matches into risk scores

**Keyword Categories**:
- **Political**: war, conflict, sanctions, election, government
- **Logistics**: blockade, strike, congestion, delay, port
- **Tariff**: trade war, embargo, tariff, duty, customs
- **Schedule**: cancelled, delayed, postponed, schedule

**Test Methods**:
- `test_single_text_keyword_analysis()`: Test individual text analysis
- `test_news_events_keyword_analysis()`: Test multiple event analysis
- `test_keyword_extraction()`: Test keyword extraction functionality
- `test_keyword_case_sensitivity()`: Test case-insensitive matching

### 4. Trade Route Analysis (`test_trade_route_analysis.py`)

**Purpose**: Test trade route risk assessment

**Key Features**:
- **Country Risk Scores**: Predefined risk scores for different countries
- **Route Complexity**: Factor in transit countries and route complexity
- **Alternative Route Identification**: Suggest lower-risk alternatives
- **Equipment-Route Mapping**: Analyze risks for specific equipment routes

**Country Risk Examples**:
- Low Risk: United States (20), Germany (15), Japan (18)
- Medium Risk: China (45), India (50)
- High Risk: Russia (70), Iran (85), North Korea (95)

**Test Methods**:
- `test_country_pair_risk_analysis()`: Test bilateral route risks
- `test_equipment_trade_route_analysis()`: Test equipment-specific routes
- `test_alternative_route_identification()`: Test route alternatives
- `test_unknown_countries_handling()`: Test error handling

### 5. Time Window Analysis (`test_time_window_analysis.py`)

**Purpose**: Test time-based risk analysis

**Key Features**:
- **Multiple Time Windows**: Immediate (1 day), short-term (7 days), medium-term (30 days), long-term (90 days)
- **Risk Decay Factors**: Reduce impact of older events
- **Trend Analysis**: Identify increasing/decreasing risk trends
- **Schedule Timeline Analysis**: Analyze upcoming deliveries

**Time Windows**:
- **Immediate**: 1.0 impact factor (full impact)
- **Short-term**: 0.8 impact factor
- **Medium-term**: 0.5 impact factor
- **Long-term**: 0.2 impact factor

**Test Methods**:
- `test_events_time_window_analysis()`: Test event time windows
- `test_schedules_time_window_analysis()`: Test schedule time windows
- `test_trend_analysis()`: Test trend identification
- `test_custom_reference_date()`: Test with custom dates

## AI Analysis Strategies

### AI Strategy Testing (`test_ai_strategies.py`)

**Purpose**: Test AI-powered analysis and compare with traditional methods

**Key Features**:
- **AI Service Integration**: Test OpenRouter API integration
- **Multiple Analysis Types**: Schedule, political, and comprehensive analysis
- **AI vs Traditional Comparison**: Direct comparison of methodologies
- **Error Handling**: Graceful fallback when AI service fails
- **Mock Testing**: Test with mocked AI responses

**AI Analysis Types**:
1. **Scheduler Analysis**: AI-powered schedule risk assessment
2. **Political Analysis**: AI-powered geopolitical risk analysis
3. **Comprehensive Analysis**: Multi-dimensional AI analysis

**Test Methods**:
- `test_ai_scheduler_analysis()`: Test AI schedule analysis
- `test_ai_political_analysis()`: Test AI political analysis
- `test_ai_comprehensive_analysis()`: Test comprehensive AI analysis
- `test_ai_vs_traditional_comparison()`: Compare AI and traditional results
- `test_ai_service_mock()`: Test with mocked AI service

## Test Data Generation

### Test Data Generator (`test_data_generator.py`)

**Purpose**: Generate realistic test data for comprehensive testing

**Generated Data Types**:
- **Equipment Data**: Manufacturing equipment with countries, costs, priorities
- **Schedule Data**: Delivery schedules with dates, statuses, priorities
- **News Events**: Political, economic, logistics, and trade events
- **Risk Assessments**: Historical risk assessments with scores and levels

**Scenario Generation**:
- **Low Risk**: 10% delays, 10% high-impact events
- **Medium Risk**: 30% delays, 30% high-impact events
- **High Risk**: 60% delays, 50% high-impact events
- **Critical Risk**: 80% delays, 80% high-impact events

## Running Tests

### Individual Test Files
```bash
# Run specific test file
python -m pytest test/traditional_analysis/test_statistical_analysis.py -v

# Run with detailed output
python test/traditional_analysis/test_statistical_analysis.py
```

### All Traditional Tests
```bash
# Run all traditional analysis tests
python -m pytest test/traditional_analysis/ -v
```

### All AI Tests
```bash
# Run all AI analysis tests
python -m pytest test/ai_analysis/ -v
```

### Complete Test Suite
```bash
# Run all tests
python test/run_all_tests.py
```

## Test Configuration

### Key Configuration Parameters (`test_config.py`)

```python
# Sample data sizes
SAMPLE_EQUIPMENT_COUNT = 20
SAMPLE_SCHEDULE_COUNT = 30
SAMPLE_NEWS_EVENT_COUNT = 50

# Risk thresholds
RISK_THRESHOLDS = {
    'low': 30, 'medium': 60, 'high': 80, 'critical': 90
}

# Time windows
TIME_WINDOWS = {
    'recent': 7, 'short_term': 30, 'medium_term': 90, 'long_term': 365
}
```

## Expected Test Results

### Traditional Analysis Results
- **Statistical Analysis**: Quantitative metrics with clear calculations
- **Threshold Analysis**: Consistent risk level classification
- **Keyword Matching**: Accurate keyword detection and scoring
- **Trade Route Analysis**: Country-based risk assessment
- **Time Window Analysis**: Time-sensitive risk evaluation

### AI Analysis Results
- **Contextual Understanding**: More nuanced risk interpretation
- **Natural Language Processing**: Better handling of complex scenarios
- **Adaptive Reasoning**: Dynamic risk assessment based on context
- **Comprehensive Integration**: Multi-factor analysis synthesis

### Comparison Results
- **Agreement Analysis**: How often AI and traditional methods agree
- **Score Differences**: Quantitative comparison of risk scores
- **Methodology Strengths**: Identification of each approach's advantages
- **Recommendations**: Guidance on when to use each method

## Troubleshooting

### Common Issues

1. **AI Service Unavailable**
   - Tests use fallback responses when OpenRouter API is unavailable
   - Check API key configuration in `.env` file

2. **Import Errors**
   - Ensure all parent directories are in Python path
   - Check that all required dependencies are installed

3. **Data Generation Issues**
   - Verify test configuration parameters
   - Check date/time handling for different time zones

### Debug Mode
```bash
# Run tests with debug output
python test/run_all_tests.py --debug

# Run specific test with verbose output
python -m pytest test/traditional_analysis/test_statistical_analysis.py -v -s
```

## Performance Benchmarks

### Expected Performance
- **Traditional Analysis**: < 1 second per test
- **AI Analysis**: 2-10 seconds per test (depending on API response)
- **Data Generation**: < 0.5 seconds for standard datasets
- **Complete Test Suite**: < 2 minutes total

### Optimization Tips
- Use smaller datasets for development testing
- Mock AI services for faster iteration
- Run tests in parallel when possible
- Cache generated test data when appropriate
