#!/usr/bin/env python3
"""
Test Report Generator
Generates detailed HTML and markdown reports from test results
"""
import sys
import os
import json
from datetime import datetime
from typing import Dict, Any, List

# Add parent directories to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

class TestReportGenerator:
    """Generate comprehensive test reports"""
    
    def __init__(self, test_results: Dict[str, Any]):
        self.results = test_results
        self.timestamp = datetime.now()
    
    def generate_markdown_report(self) -> str:
        """Generate markdown format report"""
        report = []
        
        # Header
        report.append("# SupplyGuard Test Report")
        report.append(f"**Generated:** {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        # Executive Summary
        report.append("## Executive Summary")
        summary = self.results.get('summary', {})
        
        if summary:
            trad = summary.get('traditional_tests', {})
            ai = summary.get('ai_tests', {})
            comp = summary.get('comparison_tests', {})
            
            report.append(f"- **Traditional Analysis Tests:** {trad.get('passed', 0)}/{trad.get('total', 0)} passed ({trad.get('success_rate', 0)}%)")
            report.append(f"- **AI Analysis Tests:** {ai.get('passed', 0)}/{ai.get('total', 0)} passed ({ai.get('success_rate', 0)}%)")
            report.append(f"- **Comparison Tests:** {comp.get('completed', 0)} scenarios tested")
            report.append(f"- **Execution Time:** {summary.get('execution_time', 0)} seconds")
        
        report.append("")
        
        # Traditional Analysis Results
        report.append("## Traditional Analysis Test Results")
        traditional_tests = self.results.get('traditional_tests', {})
        
        for test_name, test_result in traditional_tests.items():
            report.append(f"### {test_name}")
            
            if test_result.get('status') == 'failed':
                report.append(f"❌ **Status:** Failed")
                report.append(f"**Error:** {test_result.get('error', 'Unknown error')}")
            else:
                passed = test_result.get('passed', 0)
                total = test_result.get('total', 0)
                success_rate = round((passed / total * 100) if total > 0 else 0, 2)
                
                status_icon = "✅" if passed == total else "⚠️"
                report.append(f"{status_icon} **Status:** {passed}/{total} tests passed ({success_rate}%)")
                
                if test_result.get('errors'):
                    report.append("**Errors:**")
                    for error in test_result['errors']:
                        report.append(f"- {error}")
            
            report.append("")
        
        # AI Analysis Results
        report.append("## AI Analysis Test Results")
        ai_tests = self.results.get('ai_tests', {})
        
        for test_name, test_result in ai_tests.items():
            report.append(f"### {test_name}")
            
            if test_result.get('status') == 'failed':
                report.append(f"❌ **Status:** Failed")
                report.append(f"**Error:** {test_result.get('error', 'Unknown error')}")
            else:
                passed = test_result.get('passed', 0)
                total = test_result.get('total', 0)
                success_rate = round((passed / total * 100) if total > 0 else 0, 2)
                
                status_icon = "✅" if passed == total else "⚠️"
                report.append(f"{status_icon} **Status:** {passed}/{total} tests passed ({success_rate}%)")
                
                if test_result.get('errors'):
                    report.append("**Errors:**")
                    for error in test_result['errors']:
                        report.append(f"- {error}")
            
            report.append("")
        
        # Comparison Results
        report.append("## AI vs Traditional Comparison Results")
        comparison_results = self.results.get('comparison_results', [])
        
        if isinstance(comparison_results, list) and comparison_results:
            report.append("| Scenario | AI Risk Level | Traditional Risk Level | Agreement | Score Difference |")
            report.append("|----------|---------------|------------------------|-----------|------------------|")
            
            for comparison in comparison_results:
                scenario = comparison.get('scenario', 'Unknown')
                ai_level = comparison.get('ai_result', {}).get('risk_level', 'Unknown')
                trad_level = comparison.get('traditional_result', {}).get('risk_level', 'Unknown')
                agreement = comparison.get('comparison', {}).get('agreement_level', 'Unknown')
                score_diff = comparison.get('comparison', {}).get('score_difference', 0)
                
                report.append(f"| {scenario} | {ai_level} | {trad_level} | {agreement} | {score_diff} |")
        
        elif isinstance(comparison_results, dict) and 'error' in comparison_results:
            report.append(f"❌ **Comparison tests failed:** {comparison_results['error']}")
        
        report.append("")
        
        # Methodology Analysis
        report.append("## Methodology Analysis")
        report.append("### Traditional Analysis Strengths")
        report.append("- **Statistical Analysis:** Quantitative metrics with clear calculations")
        report.append("- **Threshold Analysis:** Consistent risk level classification")
        report.append("- **Keyword Matching:** Accurate keyword detection and scoring")
        report.append("- **Trade Route Analysis:** Country-based risk assessment")
        report.append("- **Time Window Analysis:** Time-sensitive risk evaluation")
        report.append("")
        
        report.append("### AI Analysis Strengths")
        report.append("- **Contextual Understanding:** More nuanced risk interpretation")
        report.append("- **Natural Language Processing:** Better handling of complex scenarios")
        report.append("- **Adaptive Reasoning:** Dynamic risk assessment based on context")
        report.append("- **Comprehensive Integration:** Multi-factor analysis synthesis")
        report.append("")
        
        # Recommendations
        report.append("## Recommendations")
        
        if summary:
            overall_success = (summary.get('traditional_tests', {}).get('success_rate', 0) + 
                             summary.get('ai_tests', {}).get('success_rate', 0)) / 2
            
            if overall_success >= 90:
                report.append("✅ **Overall Assessment:** Excellent - Both traditional and AI methods are performing well")
                report.append("- Continue current testing approach")
                report.append("- Consider expanding test scenarios")
            elif overall_success >= 75:
                report.append("✅ **Overall Assessment:** Good - Minor improvements needed")
                report.append("- Review failed test cases")
                report.append("- Optimize underperforming methods")
            elif overall_success >= 50:
                report.append("⚠️ **Overall Assessment:** Needs Attention - Significant issues detected")
                report.append("- Investigate failing tests immediately")
                report.append("- Consider methodology adjustments")
            else:
                report.append("❌ **Overall Assessment:** Critical Issues - Major problems detected")
                report.append("- Immediate investigation required")
                report.append("- Review all methodologies")
        
        return "\n".join(report)
    
    def generate_html_report(self) -> str:
        """Generate HTML format report"""
        html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SupplyGuard Test Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; line-height: 1.6; }}
        .header {{ background: #f4f4f4; padding: 20px; border-radius: 5px; }}
        .summary {{ background: #e8f5e8; padding: 15px; border-radius: 5px; margin: 20px 0; }}
        .test-section {{ margin: 20px 0; }}
        .test-result {{ background: #f9f9f9; padding: 10px; margin: 10px 0; border-left: 4px solid #ddd; }}
        .success {{ border-left-color: #4CAF50; }}
        .warning {{ border-left-color: #FF9800; }}
        .error {{ border-left-color: #F44336; }}
        table {{ width: 100%; border-collapse: collapse; margin: 10px 0; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #f2f2f2; }}
        .metric {{ display: inline-block; margin: 10px; padding: 10px; background: #f0f0f0; border-radius: 5px; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>SupplyGuard Test Report</h1>
        <p><strong>Generated:</strong> {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>
"""
        
        # Add summary section
        summary = self.results.get('summary', {})
        if summary:
            html += '<div class="summary">'
            html += '<h2>Executive Summary</h2>'
            
            trad = summary.get('traditional_tests', {})
            ai = summary.get('ai_tests', {})
            comp = summary.get('comparison_tests', {})
            
            html += f'<div class="metric"><strong>Traditional Tests:</strong> {trad.get("passed", 0)}/{trad.get("total", 0)} ({trad.get("success_rate", 0)}%)</div>'
            html += f'<div class="metric"><strong>AI Tests:</strong> {ai.get("passed", 0)}/{ai.get("total", 0)} ({ai.get("success_rate", 0)}%)</div>'
            html += f'<div class="metric"><strong>Comparisons:</strong> {comp.get("completed", 0)} scenarios</div>'
            html += f'<div class="metric"><strong>Execution Time:</strong> {summary.get("execution_time", 0)}s</div>'
            html += '</div>'
        
        # Add test results sections
        html += self._generate_html_test_section("Traditional Analysis Tests", self.results.get('traditional_tests', {}))
        html += self._generate_html_test_section("AI Analysis Tests", self.results.get('ai_tests', {}))
        
        # Add comparison table
        html += '<div class="test-section">'
        html += '<h2>AI vs Traditional Comparison</h2>'
        
        comparison_results = self.results.get('comparison_results', [])
        if isinstance(comparison_results, list) and comparison_results:
            html += '<table>'
            html += '<tr><th>Scenario</th><th>AI Risk Level</th><th>Traditional Risk Level</th><th>Agreement</th><th>Score Difference</th></tr>'
            
            for comparison in comparison_results:
                scenario = comparison.get('scenario', 'Unknown')
                ai_level = comparison.get('ai_result', {}).get('risk_level', 'Unknown')
                trad_level = comparison.get('traditional_result', {}).get('risk_level', 'Unknown')
                agreement = comparison.get('comparison', {}).get('agreement_level', 'Unknown')
                score_diff = comparison.get('comparison', {}).get('score_difference', 0)
                
                html += f'<tr><td>{scenario}</td><td>{ai_level}</td><td>{trad_level}</td><td>{agreement}</td><td>{score_diff}</td></tr>'
            
            html += '</table>'
        
        html += '</div>'
        
        html += """
</body>
</html>
"""
        return html
    
    def _generate_html_test_section(self, title: str, test_results: Dict[str, Any]) -> str:
        """Generate HTML for a test section"""
        html = f'<div class="test-section"><h2>{title}</h2>'
        
        for test_name, test_result in test_results.items():
            if test_result.get('status') == 'failed':
                css_class = 'test-result error'
                status = f"❌ Failed: {test_result.get('error', 'Unknown error')}"
            else:
                passed = test_result.get('passed', 0)
                total = test_result.get('total', 0)
                success_rate = round((passed / total * 100) if total > 0 else 0, 2)
                
                if passed == total:
                    css_class = 'test-result success'
                    status = f"✅ {passed}/{total} tests passed ({success_rate}%)"
                else:
                    css_class = 'test-result warning'
                    status = f"⚠️ {passed}/{total} tests passed ({success_rate}%)"
            
            html += f'<div class="{css_class}"><h3>{test_name}</h3><p>{status}</p></div>'
        
        html += '</div>'
        return html
    
    def save_reports(self, base_filename: str = None):
        """Save both markdown and HTML reports"""
        if base_filename is None:
            timestamp = self.timestamp.strftime("%Y%m%d_%H%M%S")
            base_filename = f"test_report_{timestamp}"
        
        # Ensure reports directory exists
        reports_dir = os.path.dirname(__file__)
        os.makedirs(reports_dir, exist_ok=True)
        
        # Save markdown report
        md_filename = os.path.join(reports_dir, f"{base_filename}.md")
        with open(md_filename, 'w', encoding='utf-8') as f:
            f.write(self.generate_markdown_report())
        
        # Save HTML report
        html_filename = os.path.join(reports_dir, f"{base_filename}.html")
        with open(html_filename, 'w', encoding='utf-8') as f:
            f.write(self.generate_html_report())
        
        print(f"📄 Reports saved:")
        print(f"   Markdown: {md_filename}")
        print(f"   HTML: {html_filename}")
        
        return md_filename, html_filename

def main():
    """Main function for standalone report generation"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate test reports from JSON results')
    parser.add_argument('input_file', help='JSON file containing test results')
    parser.add_argument('--output', help='Base filename for output reports')
    
    args = parser.parse_args()
    
    # Load test results
    with open(args.input_file, 'r') as f:
        test_results = json.load(f)
    
    # Generate reports
    generator = TestReportGenerator(test_results)
    generator.save_reports(args.output)

if __name__ == '__main__':
    main()
