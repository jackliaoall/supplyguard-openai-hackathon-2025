"""
AI Service Module
Integrates with OpenRouter API for AI-powered analysis
"""
import os
import logging
from typing import Dict, List, Any, Optional
from openai import OpenAI

class AIService:
    """AI Service for supply chain risk analysis using OpenRouter API"""
    
    def __init__(self):
        self.logger = logging.getLogger("ai_service")
        
        # Initialize OpenAI client with OpenRouter
        api_key = os.getenv('OPENROUTER_API_KEY', 'sk-or-v1-demo-key-placeholder')
        
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
        )
        
        # Default model configuration
        self.default_model = "openai/gpt-3.5-turbo"
        
        # System prompts for different analysis types
        self.system_prompts = {
            'scheduler': """You are a supply chain scheduling risk analyst. Analyze equipment delivery schedules and identify potential risks, delays, and bottlenecks. Provide risk scores (0-100) and actionable recommendations.""",
            
            'political': """You are a geopolitical risk analyst specializing in supply chain impacts. Analyze political events, policy changes, and their potential effects on supply chain operations. Provide risk assessments and mitigation strategies.""",
            
            'logistics': """You are a logistics and transportation risk analyst. Evaluate shipping routes, port conditions, transportation disruptions, and logistics infrastructure risks. Provide route-specific risk assessments.""",
            
            'tariff': """You are a trade policy and tariff analyst. Analyze trade wars, tariff changes, customs regulations, and their impact on supply chain costs and operations. Provide cost impact assessments.""",
            
            'comprehensive': """You are a comprehensive supply chain risk analyst. Provide holistic risk assessment covering scheduling, political, logistics, and tariff factors. Synthesize multiple risk dimensions into actionable insights."""
        }
    
    def analyze_with_ai(self, analysis_type: str, query: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Perform AI analysis using OpenRouter API
        
        Args:
            analysis_type: Type of analysis (scheduler, political, logistics, tariff, comprehensive)
            query: User query or analysis request
            context: Additional context data
            
        Returns:
            AI analysis results
        """
        try:
            # Get appropriate system prompt
            system_prompt = self.system_prompts.get(analysis_type, self.system_prompts['comprehensive'])
            
            # Prepare context information
            context_str = self._format_context(context) if context else ""
            
            # Construct the full prompt
            full_prompt = f"""
{query}

Context Information:
{context_str}

Please provide your analysis in the following JSON format:
{{
    "risk_level": "low|medium|high|critical",
    "risk_score": 0-100,
    "summary": "Brief summary of the analysis",
    "key_findings": ["finding1", "finding2", "finding3"],
    "recommendations": ["recommendation1", "recommendation2", "recommendation3"],
    "affected_areas": ["area1", "area2"],
    "confidence": 0-100
}}
"""
            
            # Make API call to OpenRouter
            completion = self.client.chat.completions.create(
                extra_body={},
                model=self.default_model,
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user",
                        "content": full_prompt
                    }
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            # Extract response
            response_content = completion.choices[0].message.content
            
            # Try to parse JSON response
            try:
                import json
                ai_result = json.loads(response_content)
            except json.JSONDecodeError:
                # If JSON parsing fails, create structured response from text
                ai_result = self._parse_text_response(response_content, analysis_type)
            
            # Add metadata
            ai_result.update({
                'analysis_type': analysis_type,
                'agent_name': f"{analysis_type.upper()}_AGENT",
                'timestamp': self._get_timestamp(),
                'model_used': self.default_model
            })
            
            return ai_result
            
        except Exception as e:
            self.logger.error(f"Error in AI analysis: {str(e)}")
            return self._create_fallback_response(analysis_type, query, str(e))
    
    def _format_context(self, context: Dict[str, Any]) -> str:
        """Format context information for AI prompt"""
        context_parts = []
        
        if 'equipment_data' in context:
            context_parts.append(f"Equipment Data: {context['equipment_data']}")
        
        if 'schedule_data' in context:
            context_parts.append(f"Schedule Data: {context['schedule_data']}")
        
        if 'news_events' in context:
            context_parts.append(f"Recent Events: {context['news_events']}")
        
        if 'country' in context:
            context_parts.append(f"Country Focus: {context['country']}")
        
        if 'trade_routes' in context:
            context_parts.append(f"Trade Routes: {context['trade_routes']}")
        
        return "\n".join(context_parts)
    
    def _parse_text_response(self, response_text: str, analysis_type: str) -> Dict[str, Any]:
        """Parse text response when JSON parsing fails"""
        # Extract key information from text response
        lines = response_text.split('\n')
        
        # Default values
        result = {
            'risk_level': 'medium',
            'risk_score': 50,
            'summary': response_text[:200] + "..." if len(response_text) > 200 else response_text,
            'key_findings': [],
            'recommendations': [],
            'affected_areas': [],
            'confidence': 75
        }
        
        # Try to extract structured information
        current_section = None
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Look for risk level indicators
            if any(word in line.lower() for word in ['critical', 'high risk', 'severe']):
                result['risk_level'] = 'critical'
                result['risk_score'] = 85
            elif any(word in line.lower() for word in ['high', 'significant']):
                result['risk_level'] = 'high'
                result['risk_score'] = 70
            elif any(word in line.lower() for word in ['low', 'minimal']):
                result['risk_level'] = 'low'
                result['risk_score'] = 25
            
            # Look for recommendations
            if any(word in line.lower() for word in ['recommend', 'suggest', 'should']):
                result['recommendations'].append(line)
            
            # Look for findings
            if any(word in line.lower() for word in ['finding', 'identified', 'observed']):
                result['key_findings'].append(line)
        
        # Limit arrays to reasonable sizes
        result['recommendations'] = result['recommendations'][:5]
        result['key_findings'] = result['key_findings'][:5]
        
        return result
    
    def _create_fallback_response(self, analysis_type: str, query: str, error: str) -> Dict[str, Any]:
        """Create fallback response when AI service fails"""
        return {
            'analysis_type': analysis_type,
            'agent_name': f"{analysis_type.upper()}_AGENT",
            'risk_level': 'medium',
            'risk_score': 50,
            'summary': f"AI analysis temporarily unavailable. Fallback analysis for: {query}",
            'key_findings': [
                "AI service encountered an error",
                "Using fallback analysis method",
                "Manual review recommended"
            ],
            'recommendations': [
                "Review query manually",
                "Check system logs for details",
                "Retry analysis later"
            ],
            'affected_areas': ['system'],
            'confidence': 30,
            'error': error,
            'timestamp': self._get_timestamp(),
            'fallback': True
        }
    
    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def health_check(self) -> Dict[str, Any]:
        """Check AI service health"""
        try:
            # Simple test query
            test_completion = self.client.chat.completions.create(
                model=self.default_model,
                messages=[
                    {
                        "role": "user",
                        "content": "Hello, this is a health check. Please respond with 'OK'."
                    }
                ],
                max_tokens=10
            )
            
            return {
                'status': 'healthy',
                'model': self.default_model,
                'response_received': True,
                'timestamp': self._get_timestamp()
            }
            
        except Exception as e:
            return {
                'status': 'unhealthy',
                'error': str(e),
                'timestamp': self._get_timestamp()
            }
