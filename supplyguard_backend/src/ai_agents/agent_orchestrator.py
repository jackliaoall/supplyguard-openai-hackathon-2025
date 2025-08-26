"""
AI代理協調器
負責協調和管理多個AI代理，處理自然語言查詢並路由到適當的代理
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

import re
import logging
from typing import Dict, List, Any, Optional
from src.ai_agents.scheduler_agent import SchedulerAgent
from src.ai_agents.political_risk_agent import PoliticalRiskAgent
from src.ai_agents.logistics_agent import LogisticsAgent
from src.ai_agents.tariff_agent import TariffAgent

class AgentOrchestrator:
    """AI代理協調器"""
    
    def __init__(self):
        self.logger = logging.getLogger("orchestrator")
        
        # 初始化所有代理
        self.agents = {
            'scheduler': SchedulerAgent(),
            'political': PoliticalRiskAgent(),
            'logistics': LogisticsAgent(),
            'tariff': TariffAgent()
        }
        
        # 查詢路由規則
        self.routing_rules = {
            'scheduler': {
                'keywords': [
                    'schedule', 'delivery', 'timeline', 'delay', 'deadline',
                    '排程', '交付', '時間表', '延遲', '截止日期', '進度'
                ],
                'patterns': [
                    r'schedule.*risk',
                    r'delivery.*delay',
                    r'排程.*風險',
                    r'交付.*延遲'
                ]
            },
            'political': {
                'keywords': [
                    'political', 'government', 'policy', 'election', 'sanction',
                    '政治', '政府', '政策', '選舉', '制裁', '外交'
                ],
                'patterns': [
                    r'political.*risk',
                    r'government.*change',
                    r'政治.*風險',
                    r'政府.*變化'
                ]
            },
            'logistics': {
                'keywords': [
                    'logistics', 'transport', 'shipping', 'port', 'cargo',
                    '物流', '運輸', '航運', '港口', '貨物', '運送'
                ],
                'patterns': [
                    r'logistics.*risk',
                    r'transport.*delay',
                    r'物流.*風險',
                    r'運輸.*延遲'
                ]
            },
            'tariff': {
                'keywords': [
                    'tariff', 'trade', 'customs', 'duty', 'import', 'export',
                    '關稅', '貿易', '海關', '稅收', '進口', '出口'
                ],
                'patterns': [
                    r'tariff.*risk',
                    r'trade.*war',
                    r'關稅.*風險',
                    r'貿易.*戰'
                ]
            }
        }
    
    def process_query(self, query: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        處理自然語言查詢
        
        Args:
            query: 用戶查詢
            context: 額外上下文資訊
            
        Returns:
            分析結果
        """
        self.logger.info(f"Processing query: {query}")
        
        # 分析查詢意圖
        intent = self._analyze_intent(query)
        
        # 路由到適當的代理
        if intent['agent_type']:
            agent = self.agents.get(intent['agent_type'])
            if agent:
                try:
                    # 準備代理輸入數據
                    agent_data = self._prepare_agent_data(query, intent, context)
                    
                    # 執行分析
                    result = agent.analyze(agent_data)
                    
                    # 添加查詢資訊
                    result['original_query'] = query
                    result['detected_intent'] = intent
                    
                    return result
                    
                except Exception as e:
                    self.logger.error(f"Error in agent {intent['agent_type']}: {str(e)}")
                    return self._create_error_response(query, str(e))
        
        # 如果無法確定意圖，執行綜合分析
        return self._perform_comprehensive_analysis(query, context)
    
    def _analyze_intent(self, query: str) -> Dict[str, Any]:
        """分析查詢意圖"""
        query_lower = query.lower()
        
        # 計算每個代理的匹配分數
        agent_scores = {}
        
        for agent_type, rules in self.routing_rules.items():
            score = 0
            
            # 關鍵字匹配
            for keyword in rules['keywords']:
                if keyword in query_lower:
                    score += 2
            
            # 模式匹配
            for pattern in rules['patterns']:
                if re.search(pattern, query_lower):
                    score += 3
            
            agent_scores[agent_type] = score
        
        # 找到最高分的代理
        best_agent = max(agent_scores.items(), key=lambda x: x[1])
        
        # 提取實體
        entities = self._extract_entities(query)
        
        return {
            'agent_type': best_agent[0] if best_agent[1] > 0 else None,
            'confidence': best_agent[1],
            'entities': entities,
            'all_scores': agent_scores
        }
    
    def _extract_entities(self, query: str) -> Dict[str, List[str]]:
        """從查詢中提取實體"""
        entities = {
            'countries': [],
            'equipment_types': [],
            'time_periods': []
        }
        
        # 國家實體
        countries = [
            '中國', '美國', '日本', '德國', '韓國', '台灣', '荷蘭', '英國',
            'china', 'usa', 'japan', 'germany', 'korea', 'taiwan', 'netherlands', 'uk'
        ]
        
        for country in countries:
            if country in query.lower():
                entities['countries'].append(country)
        
        # 設備類型實體
        equipment_types = [
            '機器人', '設備', '機械', '電子', '醫療', '化工',
            'robot', 'equipment', 'machinery', 'electronic', 'medical', 'chemical'
        ]
        
        for eq_type in equipment_types:
            if eq_type in query.lower():
                entities['equipment_types'].append(eq_type)
        
        # 時間實體
        time_patterns = [
            r'最近.*天', r'過去.*週', r'未來.*月',
            r'recent.*days?', r'past.*weeks?', r'next.*months?'
        ]
        
        for pattern in time_patterns:
            matches = re.findall(pattern, query.lower())
            entities['time_periods'].extend(matches)
        
        return entities
    
    def _prepare_agent_data(self, query: str, intent: Dict[str, Any], context: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """準備代理輸入數據"""
        data = {
            'query': query,
            'intent': intent,
            'entities': intent.get('entities', {}),
            'context': context or {}
        }
        
        # 根據代理類型添加特定數據
        agent_type = intent.get('agent_type')
        
        if agent_type == 'political':
            # 為政治風險代理添加國家資訊
            countries = intent.get('entities', {}).get('countries', [])
            if countries:
                data['target_countries'] = countries
        
        elif agent_type == 'logistics':
            # 為物流代理添加路線資訊
            countries = intent.get('entities', {}).get('countries', [])
            if len(countries) >= 2:
                data['origin_country'] = countries[0]
                data['destination_country'] = countries[1]
        
        elif agent_type == 'tariff':
            # 為關稅代理添加貿易關係資訊
            countries = intent.get('entities', {}).get('countries', [])
            if len(countries) >= 2:
                data['country1'] = countries[0]
                data['country2'] = countries[1]
        
        return data
    
    def _perform_comprehensive_analysis(self, query: str, context: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """執行綜合分析"""
        self.logger.info("Performing comprehensive analysis")
        
        results = {}
        
        # 執行所有代理的分析
        for agent_name, agent in self.agents.items():
            try:
                agent_data = {'query': query, 'context': context or {}}
                result = agent.analyze(agent_data)
                results[agent_name] = result
            except Exception as e:
                self.logger.error(f"Error in comprehensive analysis for {agent_name}: {str(e)}")
                results[agent_name] = {
                    'error': str(e),
                    'agent_name': agent_name
                }
        
        # 計算綜合風險分數
        overall_risk = self._calculate_overall_risk(results)
        
        # 生成綜合摘要
        summary = self._generate_comprehensive_summary(results)
        
        # 生成綜合建議
        recommendations = self._generate_comprehensive_recommendations(results)
        
        return {
            'analysis_type': 'comprehensive',
            'agent_name': 'ORCHESTRATOR',
            'risk_level': overall_risk['level'],
            'risk_score': overall_risk['score'],
            'summary': summary,
            'details': results,
            'recommendations': recommendations,
            'original_query': query,
            'timestamp': results.get('scheduler', {}).get('timestamp', '')
        }
    
    def _calculate_overall_risk(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """計算綜合風險分數"""
        total_score = 0
        valid_agents = 0
        
        for agent_name, result in results.items():
            if 'risk_score' in result and not result.get('error'):
                total_score += result['risk_score']
                valid_agents += 1
        
        if valid_agents == 0:
            return {'score': 0, 'level': 'low'}
        
        avg_score = total_score / valid_agents
        
        # 確定風險等級
        if avg_score >= 80:
            level = 'critical'
        elif avg_score >= 60:
            level = 'high'
        elif avg_score >= 40:
            level = 'medium'
        else:
            level = 'low'
        
        return {'score': round(avg_score, 2), 'level': level}
    
    def _generate_comprehensive_summary(self, results: Dict[str, Any]) -> str:
        """生成綜合摘要"""
        summaries = []
        
        for agent_name, result in results.items():
            if 'summary' in result and not result.get('error'):
                risk_level = result.get('risk_level', 'unknown')
                summary = result.get('summary', '')
                summaries.append(f"{agent_name.upper()}風險({risk_level}): {summary}")
        
        if not summaries:
            return "無法生成綜合分析摘要，所有代理都遇到錯誤。"
        
        return " | ".join(summaries)
    
    def _generate_comprehensive_recommendations(self, results: Dict[str, Any]) -> List[str]:
        """生成綜合建議"""
        all_recommendations = []
        
        for agent_name, result in results.items():
            if 'recommendations' in result and not result.get('error'):
                recommendations = result.get('recommendations', [])
                # 為每個建議添加來源標識
                tagged_recommendations = [f"[{agent_name.upper()}] {rec}" for rec in recommendations[:2]]
                all_recommendations.extend(tagged_recommendations)
        
        # 添加綜合建議
        all_recommendations.extend([
            "建立跨領域風險監控機制",
            "定期更新風險評估模型",
            "加強供應鏈韌性建設"
        ])
        
        return all_recommendations[:8]  # 限制建議數量
    
    def _create_error_response(self, query: str, error_message: str) -> Dict[str, Any]:
        """創建錯誤回應"""
        return {
            'analysis_type': 'error',
            'agent_name': 'ORCHESTRATOR',
            'risk_level': 'unknown',
            'risk_score': 0,
            'summary': f'處理查詢時發生錯誤: {error_message}',
            'details': {'error': error_message},
            'recommendations': ['請檢查查詢格式並重試', '聯繫系統管理員獲取支援'],
            'original_query': query,
            'error': True
        }
    
    def get_agent_capabilities(self) -> Dict[str, Dict[str, Any]]:
        """獲取所有代理的能力描述"""
        capabilities = {}
        
        for agent_name, agent in self.agents.items():
            capabilities[agent_name] = {
                'name': agent.name,
                'description': agent.description,
                'keywords': self.routing_rules[agent_name]['keywords'],
                'example_queries': self._get_example_queries(agent_name)
            }
        
        return capabilities
    
    def _get_example_queries(self, agent_type: str) -> List[str]:
        """獲取代理的示例查詢"""
        examples = {
            'scheduler': [
                "What are the schedule risks?",
                "分析設備交付排程的風險",
                "檢查延遲的項目"
            ],
            'political': [
                "What are the political risks?",
                "分析德國的政治風險",
                "評估地緣政治影響"
            ],
            'logistics': [
                "What are the logistics risks?",
                "分析物流運輸風險",
                "檢查港口擁堵情況"
            ],
            'tariff': [
                "What are the tariff risks?",
                "分析貿易關稅風險",
                "評估貿易戰影響"
            ]
        }
        
        return examples.get(agent_type, [])
    
    def health_check(self) -> Dict[str, Any]:
        """健康檢查"""
        status = {
            'orchestrator': 'healthy',
            'agents': {},
            'total_agents': len(self.agents),
            'healthy_agents': 0
        }
        
        for agent_name, agent in self.agents.items():
            try:
                # 簡單的健康檢查
                test_data = {'query': 'health check', 'context': {}}
                agent.validate_input(test_data, ['query'])
                status['agents'][agent_name] = 'healthy'
                status['healthy_agents'] += 1
            except Exception as e:
                status['agents'][agent_name] = f'error: {str(e)}'
        
        status['overall_health'] = 'healthy' if status['healthy_agents'] == status['total_agents'] else 'degraded'
        
        return status

