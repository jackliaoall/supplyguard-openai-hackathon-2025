"""
Political Risk Analysis Agent
Responsible for assessing geopolitical risk impact on supply chain
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from datetime import datetime, timedelta
from typing import Dict, List, Any
from src.ai_agents.base_agent import BaseAgent
from src.models.supply_chain import Equipment, NewsEvent

class PoliticalRiskAgent(BaseAgent):
    """Political Risk Analysis Agent"""

    def __init__(self):
        super().__init__(
            name="POLITICAL_RISK_AGENT",
            description="Assess geopolitical risk impact on supply chain, monitor political events and policy changes"
        )

        # Political risk keywords
        self.political_keywords = [
            'election', 'government', 'policy', 'regulation', 'sanction', 'embargo',
            'trade war', 'diplomatic', 'political', 'conflict', 'protest', 'coup'
        ]
    
    def analyze(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze political risks

        Args:
            data: Data containing country or region information

        Returns:
            Political risk analysis results
        """
        self.log_thinking("Starting political risk analysis...")

        # Get political-related news events
        political_events = NewsEvent.query.filter_by(category='political').order_by(
            NewsEvent.published_date.desc()
        ).limit(20).all()

        # Prepare context for AI analysis
        context = self._prepare_political_context(political_events, data)

        # Create analysis query
        country = data.get('country', 'global regions')
        query = f"Analyze political risks affecting supply chain operations in {country}. Consider geopolitical events, policy changes, and their impact on procurement and logistics."

        # Use AI service for analysis
        ai_result = self.analyze_with_ai(query, context)

        # Combine with traditional analysis
        traditional_analysis = self._analyze_political_events(political_events, data)

        # Merge results
        return self._merge_political_analysis(ai_result, traditional_analysis, political_events)

    def _prepare_political_context(self, events: List[NewsEvent], data: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare context for political risk AI analysis"""

        # Categorize events by impact and recency
        high_impact_events = [e for e in events if e.impact_level == 'high']
        recent_events = [e for e in events if (datetime.now() - e.published_date).days <= 7]

        # Extract country-specific events
        target_country = data.get('country')
        country_events = []
        if target_country:
            country_events = [e for e in events if e.country and target_country.lower() in e.country.lower()]

        # Prepare event summaries
        event_summaries = []
        for event in events[:10]:  # Top 10 recent events
            event_summaries.append({
                'title': event.title,
                'country': event.country,
                'impact_level': event.impact_level,
                'date': event.published_date.strftime('%Y-%m-%d'),
                'category': event.category
            })

        return {
            'total_events': len(events),
            'high_impact_events': len(high_impact_events),
            'recent_events': len(recent_events),
            'country_specific_events': len(country_events),
            'target_country': target_country,
            'news_events': f"Analyzing {len(events)} political events, {len(high_impact_events)} high-impact, {len(recent_events)} recent",
            'event_summaries': event_summaries
        }

    def _merge_political_analysis(self, ai_result: Dict[str, Any], traditional_analysis: Dict[str, Any], events: List[NewsEvent]) -> Dict[str, Any]:
        """Merge AI and traditional political risk analysis"""

        # Use AI assessment with traditional fallback
        risk_level = ai_result.get('risk_level', traditional_analysis.get('risk_level', 'medium'))
        risk_score = ai_result.get('risk_score', traditional_analysis.get('risk_score', 50))

        # Combine insights
        ai_summary = ai_result.get('summary', '')
        traditional_summary = traditional_analysis.get('summary', '')
        combined_summary = f"{ai_summary} {traditional_summary}".strip()

        # Merge recommendations
        ai_recommendations = ai_result.get('recommendations', [])
        traditional_recommendations = traditional_analysis.get('recommendations', [])
        all_recommendations = ai_recommendations + traditional_recommendations
        unique_recommendations = list(dict.fromkeys(all_recommendations))[:5]

        return self.format_response(
            analysis_type='political',
            risk_level=risk_level,
            risk_score=risk_score,
            summary=combined_summary or f"Analyzed {len(events)} political events",
            details={
                **traditional_analysis.get('details', {}),
                'ai_insights': ai_result.get('key_findings', []),
                'ai_confidence': ai_result.get('confidence', 75)
            },
            recommendations=unique_recommendations
        )
        
        # 獲取所有設備以分析受影響的國家
        equipment_list = Equipment.query.all()
        
        # 分析政治風險
        analysis_results = self._analyze_political_risks(political_events, equipment_list)
        
        # 計算整體風險分數
        risk_score = self._calculate_political_risk_score(analysis_results)
        risk_level = self.calculate_risk_level(risk_score)
        
        # 生成摘要
        summary = self._generate_summary(analysis_results)
        
        # 生成建議
        recommendations = self._generate_recommendations(analysis_results)
        
        # 獲取受影響的設備
        affected_equipment = self._get_affected_equipment(equipment_list, analysis_results['affected_countries'])
        
        return self.format_response(
            analysis_type='political',
            risk_level=risk_level,
            risk_score=risk_score,
            summary=summary,
            details=analysis_results,
            recommendations=recommendations,
            recent_events=[event.to_dict() for event in political_events[:5]],
            affected_equipment=affected_equipment
        )
    
    def _analyze_political_risks(self, events: List[NewsEvent], equipment_list: List[Equipment]) -> Dict[str, Any]:
        """分析政治風險"""
        # 統計事件
        total_events = len(events)
        high_impact_events = [e for e in events if e.impact_level == 'high']
        recent_events = [e for e in events if (datetime.now() - e.published_date).days <= 7]
        
        # 分析受影響的國家
        affected_countries = set()
        country_risk_scores = {}
        
        for event in events:
            if event.country:
                affected_countries.add(event.country)
                
                # 計算國家風險分數
                if event.country not in country_risk_scores:
                    country_risk_scores[event.country] = 0
                
                # 根據事件影響等級加分
                if event.impact_level == 'high':
                    country_risk_scores[event.country] += 30
                elif event.impact_level == 'medium':
                    country_risk_scores[event.country] += 15
                else:
                    country_risk_scores[event.country] += 5
                
                # 最近事件加權
                if (datetime.now() - event.published_date).days <= 7:
                    country_risk_scores[event.country] += 10
        
        # 分析關鍵字頻率
        keyword_frequency = {}
        for event in events:
            keywords = self.extract_keywords(event.title + " " + event.content)
            for keyword in keywords:
                if keyword in self.political_keywords:
                    keyword_frequency[keyword] = keyword_frequency.get(keyword, 0) + 1
        
        # 計算供應鏈暴露度
        supply_chain_exposure = self._calculate_supply_chain_exposure(equipment_list, affected_countries)
        
        return {
            'total_events': total_events,
            'high_impact_events': len(high_impact_events),
            'recent_events': len(recent_events),
            'affected_countries': list(affected_countries),
            'country_risk_scores': country_risk_scores,
            'keyword_frequency': keyword_frequency,
            'supply_chain_exposure': supply_chain_exposure,
            'top_risk_countries': self._get_top_risk_countries(country_risk_scores, 5)
        }
    
    def _calculate_supply_chain_exposure(self, equipment_list: List[Equipment], affected_countries: set) -> Dict[str, Any]:
        """計算供應鏈暴露度"""
        total_equipment = len(equipment_list)
        exposed_equipment = []
        
        for equipment in equipment_list:
            if (equipment.manufacturing_country in affected_countries or 
                equipment.destination_country in affected_countries):
                exposed_equipment.append(equipment)
        
        exposure_rate = (len(exposed_equipment) / total_equipment) * 100 if total_equipment > 0 else 0
        
        return {
            'total_equipment': total_equipment,
            'exposed_equipment': len(exposed_equipment),
            'exposure_rate': round(exposure_rate, 2)
        }
    
    def _get_top_risk_countries(self, country_risk_scores: Dict[str, float], top_n: int) -> List[Dict[str, Any]]:
        """獲取風險最高的國家"""
        sorted_countries = sorted(country_risk_scores.items(), key=lambda x: x[1], reverse=True)
        
        top_countries = []
        for country, score in sorted_countries[:top_n]:
            risk_level = self.calculate_risk_level(min(100, score))
            top_countries.append({
                'country': country,
                'risk_score': round(score, 2),
                'risk_level': risk_level
            })
        
        return top_countries
    
    def _calculate_political_risk_score(self, analysis_results: Dict[str, Any]) -> float:
        """計算政治風險分數"""
        high_impact_events = analysis_results.get('high_impact_events', 0)
        recent_events = analysis_results.get('recent_events', 0)
        exposure_rate = analysis_results.get('supply_chain_exposure', {}).get('exposure_rate', 0)
        total_events = analysis_results.get('total_events', 0)
        
        # 基於高影響事件的風險分數 (0-40分)
        high_impact_score = min(40, high_impact_events * 8)
        
        # 基於最近事件的風險分數 (0-30分)
        recent_score = min(30, recent_events * 5)
        
        # 基於供應鏈暴露度的風險分數 (0-30分)
        exposure_score = min(30, exposure_rate * 0.5)
        
        total_score = high_impact_score + recent_score + exposure_score
        
        return min(100, total_score)
    
    def _generate_summary(self, analysis_results: Dict[str, Any]) -> str:
        """生成分析摘要"""
        total_events = analysis_results['total_events']
        high_impact = analysis_results['high_impact_events']
        affected_countries = len(analysis_results['affected_countries'])
        exposed_equipment = analysis_results['supply_chain_exposure']['exposed_equipment']
        
        summary = f"分析了 {total_events} 個政治事件，其中 {high_impact} 個高影響事件，"
        summary += f"涉及 {affected_countries} 個國家，可能影響 {exposed_equipment} 個設備項目。"
        
        return summary
    
    def _generate_recommendations(self, analysis_results: Dict[str, Any]) -> List[str]:
        """生成建議"""
        recommendations = []
        
        high_impact_events = analysis_results.get('high_impact_events', 0)
        exposure_rate = analysis_results.get('supply_chain_exposure', {}).get('exposure_rate', 0)
        top_risk_countries = analysis_results.get('top_risk_countries', [])
        
        if high_impact_events > 3:
            recommendations.append('高影響政治事件頻發，建議加強風險監控')
        
        if exposure_rate > 50:
            recommendations.append('供應鏈暴露度較高，建議考慮多元化策略')
        
        if top_risk_countries:
            high_risk_country = top_risk_countries[0]['country']
            recommendations.append(f'特別關注 {high_risk_country} 的政治局勢發展')
        
        # 通用建議
        recommendations.extend([
            '持續監控政治局勢發展',
            '評估供應鏈多元化選項',
            '與當地合作夥伴保持密切聯繫',
            '準備應急採購計劃'
        ])
        
        return recommendations[:6]
    
    def _get_affected_equipment(self, equipment_list: List[Equipment], affected_countries: List[str]) -> List[Dict[str, Any]]:
        """獲取受影響的設備"""
        affected_equipment = []
        
        for equipment in equipment_list:
            if (equipment.manufacturing_country in affected_countries or 
                equipment.destination_country in affected_countries):
                affected_equipment.append(equipment.to_dict())
        
        return affected_equipment[:5]  # 只返回前5個
    
    def analyze_country_risk(self, country_name: str) -> Dict[str, Any]:
        """
        分析特定國家的政治風險
        
        Args:
            country_name: 國家名稱
            
        Returns:
            國家政治風險分析結果
        """
        self.log_thinking(f"分析 {country_name} 的政治風險...")
        
        # 獲取該國家的政治事件
        country_events = NewsEvent.query.filter_by(
            country=country_name, 
            category='political'
        ).order_by(NewsEvent.published_date.desc()).limit(10).all()
        
        # 獲取該國家相關的設備
        related_equipment = Equipment.query.filter(
            (Equipment.manufacturing_country == country_name) |
            (Equipment.destination_country == country_name)
        ).all()
        
        if not country_events:
            return self.format_response(
                analysis_type='country_political',
                risk_level='low',
                risk_score=20,
                summary=f'{country_name} 暫無政治風險事件記錄',
                details={'total_events': 0, 'related_equipment': len(related_equipment)},
                recommendations=[f'持續監控 {country_name} 的政治局勢']
            )
        
        # 分析國家風險
        analysis_results = self._analyze_country_political_events(country_events, related_equipment)
        risk_score = self._calculate_country_risk_score(analysis_results)
        risk_level = self.calculate_risk_level(risk_score)
        
        summary = f"{country_name} 政治風險分析：發現 {len(country_events)} 個政治事件，可能影響 {len(related_equipment)} 個設備項目"
        
        return self.format_response(
            analysis_type='country_political',
            risk_level=risk_level,
            risk_score=risk_score,
            summary=summary,
            details=analysis_results,
            recommendations=self._generate_country_recommendations(country_name, analysis_results),
            country=country_name,
            recent_events=[event.to_dict() for event in country_events[:5]],
            related_equipment=[eq.to_dict() for eq in related_equipment[:5]]
        )
    
    def _analyze_country_political_events(self, events: List[NewsEvent], equipment: List[Equipment]) -> Dict[str, Any]:
        """分析國家政治事件"""
        high_impact_events = [e for e in events if e.impact_level == 'high']
        recent_events = [e for e in events if (datetime.now() - e.published_date).days <= 30]
        
        # 分析事件類型
        event_types = {}
        for event in events:
            keywords = self.extract_keywords(event.title + " " + event.content)
            for keyword in keywords:
                if keyword in self.political_keywords:
                    event_types[keyword] = event_types.get(keyword, 0) + 1
        
        return {
            'total_events': len(events),
            'high_impact_events': len(high_impact_events),
            'recent_events': len(recent_events),
            'related_equipment': len(equipment),
            'event_types': event_types,
            'latest_event_date': events[0].published_date.isoformat() if events else None
        }
    
    def _calculate_country_risk_score(self, analysis_results: Dict[str, Any]) -> float:
        """計算國家風險分數"""
        high_impact = analysis_results.get('high_impact_events', 0)
        recent_events = analysis_results.get('recent_events', 0)
        total_events = analysis_results.get('total_events', 0)
        
        # 基於高影響事件
        high_impact_score = min(50, high_impact * 15)
        
        # 基於最近事件
        recent_score = min(30, recent_events * 8)
        
        # 基於總事件數
        total_score = min(20, total_events * 2)
        
        return min(100, high_impact_score + recent_score + total_score)
    
    def _generate_country_recommendations(self, country_name: str, analysis_results: Dict[str, Any]) -> List[str]:
        """生成國家特定建議"""
        recommendations = []
        
        high_impact = analysis_results.get('high_impact_events', 0)
        recent_events = analysis_results.get('recent_events', 0)
        
        if high_impact > 2:
            recommendations.append(f'{country_name} 存在多個高影響政治事件，建議重新評估供應鏈風險')
        
        if recent_events > 3:
            recommendations.append(f'{country_name} 最近政治活動頻繁，建議密切監控')
        
        recommendations.extend([
            f'與 {country_name} 當地合作夥伴保持聯繫',
            f'評估 {country_name} 供應鏈的替代方案',
            f'關注 {country_name} 的政策法規變化'
        ])
        
        return recommendations[:5]

