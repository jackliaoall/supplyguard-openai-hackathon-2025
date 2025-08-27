"""
AI Agent Base Class
Provides common functionality and interface for all AI agents
"""
import json
import logging
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, List, Any, Optional
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.services.ai_service import AIService

class BaseAgent(ABC):
    """AI Agent Base Class"""

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.logger = logging.getLogger(f"agent.{name}")

        # Initialize AI service
        self.ai_service = AIService()
        
    @abstractmethod
    def analyze(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        執行分析
        
        Args:
            data: 輸入數據
            
        Returns:
            分析結果
        """
        pass
    
    def log_thinking(self, message: str):
        """Log agent thinking process"""
        self.logger.info(f"[{self.name}] {message}")

    def analyze_with_ai(self, query: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Perform AI-powered analysis using OpenRouter

        Args:
            query: Analysis query or request
            context: Additional context data

        Returns:
            AI analysis results
        """
        # Determine analysis type based on agent name
        analysis_type = self.name.lower().replace('_agent', '')

        # Use AI service for analysis
        return self.ai_service.analyze_with_ai(analysis_type, query, context)
        
    def format_response(self, 
                       analysis_type: str,
                       risk_level: str, 
                       risk_score: float,
                       summary: str,
                       details: Dict[str, Any],
                       recommendations: List[str],
                       **kwargs) -> Dict[str, Any]:
        """
        格式化回應
        
        Args:
            analysis_type: 分析類型
            risk_level: 風險等級
            risk_score: 風險分數
            summary: 摘要
            details: 詳細資訊
            recommendations: 建議
            **kwargs: 其他額外資訊
            
        Returns:
            格式化的回應
        """
        response = {
            'analysis_type': analysis_type,
            'agent_name': self.name,
            'risk_level': risk_level,
            'risk_score': round(risk_score, 2),
            'summary': summary,
            'details': details,
            'recommendations': recommendations,
            'timestamp': datetime.now().isoformat()
        }
        
        # 添加額外資訊
        response.update(kwargs)
        
        return response
    
    def calculate_risk_level(self, risk_score: float) -> str:
        """
        根據風險分數計算風險等級
        
        Args:
            risk_score: 風險分數 (0-100)
            
        Returns:
            風險等級
        """
        if risk_score >= 80:
            return 'critical'
        elif risk_score >= 60:
            return 'high'
        elif risk_score >= 40:
            return 'medium'
        else:
            return 'low'
    
    def extract_keywords(self, text: str) -> List[str]:
        """
        從文本中提取關鍵字
        
        Args:
            text: 輸入文本
            
        Returns:
            關鍵字列表
        """
        # 簡單的關鍵字提取邏輯
        keywords = []
        text_lower = text.lower()
        
        # 風險相關關鍵字
        risk_keywords = [
            'delay', 'disruption', 'shortage', 'conflict', 'strike', 'embargo',
            'tariff', 'sanction', 'earthquake', 'flood', 'hurricane', 'pandemic',
            '延遲', '中斷', '短缺', '衝突', '罷工', '禁運', '關稅', '制裁', 
            '地震', '洪水', '颶風', '疫情'
        ]
        
        for keyword in risk_keywords:
            if keyword in text_lower:
                keywords.append(keyword)
                
        return keywords
    
    def validate_input(self, data: Dict[str, Any], required_fields: List[str]) -> bool:
        """
        驗證輸入數據
        
        Args:
            data: 輸入數據
            required_fields: 必需欄位列表
            
        Returns:
            驗證結果
        """
        for field in required_fields:
            if field not in data:
                self.logger.error(f"Missing required field: {field}")
                return False
        return True

