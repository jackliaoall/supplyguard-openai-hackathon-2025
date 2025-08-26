"""
關稅風險分析代理
負責分析貿易政策和關稅變化對供應鏈的影響
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from datetime import datetime, timedelta
from typing import Dict, List, Any
from src.ai_agents.base_agent import BaseAgent
from src.models.supply_chain import Equipment, NewsEvent

class TariffAgent(BaseAgent):
    """關稅風險分析代理"""
    
    def __init__(self):
        super().__init__(
            name="TARIFF_AGENT",
            description="分析貿易政策和關稅變化對供應鏈的影響，監控貿易戰和關稅調整"
        )
        
        # 關稅風險關鍵字
        self.tariff_keywords = [
            'tariff', 'trade war', 'customs', 'duty', 'import', 'export',
            'trade policy', 'trade agreement', 'wto', 'quota', 'embargo',
            '關稅', '貿易戰', '海關', '稅收', '進口', '出口', '貿易政策', 
            '貿易協定', '配額', '禁運'
        ]
        
        # 主要貿易關係
        self.trade_relationships = {
            '美中貿易': ['美國', '中國'],
            '歐美貿易': ['德國', '法國', '荷蘭', '美國'],
            '亞洲貿易': ['中國', '日本', '韓國', '台灣'],
            '跨太平洋貿易': ['美國', '日本', '韓國', '台灣', '澳洲']
        }
    
    def analyze(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        分析關稅風險
        
        Args:
            data: 包含貿易相關資訊的數據
            
        Returns:
            關稅風險分析結果
        """
        self.log_thinking("開始分析關稅風險...")
        
        # 獲取關稅相關新聞事件
        tariff_events = NewsEvent.query.filter_by(category='tariff').order_by(
            NewsEvent.published_date.desc()
        ).limit(20).all()
        
        # 獲取所有設備以分析貿易影響
        equipment_list = Equipment.query.all()
        
        # 分析關稅風險
        analysis_results = self._analyze_tariff_risks(tariff_events, equipment_list)
        
        # 計算整體風險分數
        risk_score = self._calculate_tariff_risk_score(analysis_results)
        risk_level = self.calculate_risk_level(risk_score)
        
        # 生成摘要
        summary = self._generate_summary(analysis_results)
        
        # 生成建議
        recommendations = self._generate_recommendations(analysis_results)
        
        # 獲取受影響的設備
        affected_equipment = self._get_affected_equipment(equipment_list, analysis_results['affected_trade_routes'])
        
        return self.format_response(
            analysis_type='tariff',
            risk_level=risk_level,
            risk_score=risk_score,
            summary=summary,
            details=analysis_results,
            recommendations=recommendations,
            recent_events=[event.to_dict() for event in tariff_events[:5]],
            affected_equipment=affected_equipment
        )
    
    def _analyze_tariff_risks(self, events: List[NewsEvent], equipment_list: List[Equipment]) -> Dict[str, Any]:
        """分析關稅風險"""
        # 統計事件
        total_events = len(events)
        high_impact_events = [e for e in events if e.impact_level == 'high']
        recent_events = [e for e in events if (datetime.now() - e.published_date).days <= 30]
        
        # 分析受影響的貿易路線
        affected_trade_routes = set()
        trade_route_scores = {}
        
        for route_name, countries in self.trade_relationships.items():
            route_events = [e for e in events if e.country in countries]
            if route_events:
                affected_trade_routes.add(route_name)
                
                # 計算貿易路線風險分數
                route_score = 0
                for event in route_events:
                    if event.impact_level == 'high':
                        route_score += 30
                    elif event.impact_level == 'medium':
                        route_score += 18
                    else:
                        route_score += 8
                    
                    # 最近事件加權
                    if (datetime.now() - event.published_date).days <= 30:
                        route_score += 15
                
                trade_route_scores[route_name] = route_score
        
        # 分析關鍵字頻率
        keyword_frequency = {}
        for event in events:
            keywords = self.extract_keywords(event.title + " " + event.content)
            for keyword in keywords:
                if keyword in self.tariff_keywords:
                    keyword_frequency[keyword] = keyword_frequency.get(keyword, 0) + 1
        
        # 分析貿易戰風險
        trade_war_risks = self._analyze_trade_war_risks(events)
        
        # 計算供應鏈貿易暴露度
        trade_exposure = self._calculate_trade_exposure(equipment_list, affected_trade_routes)
        
        # 分析成本影響
        cost_impact = self._analyze_cost_impact(events, equipment_list)
        
        return {
            'total_events': total_events,
            'high_impact_events': len(high_impact_events),
            'recent_events': len(recent_events),
            'affected_trade_routes': list(affected_trade_routes),
            'trade_route_scores': trade_route_scores,
            'keyword_frequency': keyword_frequency,
            'trade_war_risks': trade_war_risks,
            'trade_exposure': trade_exposure,
            'cost_impact': cost_impact,
            'top_risk_routes': self._get_top_risk_trade_routes(trade_route_scores, 3)
        }
    
    def _analyze_trade_war_risks(self, events: List[NewsEvent]) -> Dict[str, Any]:
        """分析貿易戰風險"""
        trade_war_keywords = ['trade war', 'tariff war', '貿易戰', '關稅戰']
        trade_war_events = []
        
        for event in events:
            event_text = (event.title + " " + event.content).lower()
            if any(keyword in event_text for keyword in trade_war_keywords):
                trade_war_events.append(event)
        
        # 統計涉及的國家
        involved_countries = {}
        for event in trade_war_events:
            if event.country:
                involved_countries[event.country] = involved_countries.get(event.country, 0) + 1
        
        return {
            'total_trade_war_events': len(trade_war_events),
            'involved_countries': involved_countries,
            'escalation_risk': len(trade_war_events) > 3  # 如果超過3個事件則認為有升級風險
        }
    
    def _calculate_trade_exposure(self, equipment_list: List[Equipment], affected_routes: set) -> Dict[str, Any]:
        """計算貿易暴露度"""
        total_equipment = len(equipment_list)
        exposed_equipment = []
        
        for equipment in equipment_list:
            # 檢查設備是否在受影響的貿易路線上
            for route_name in affected_routes:
                if route_name in self.trade_relationships:
                    countries = self.trade_relationships[route_name]
                    if (equipment.manufacturing_country in countries and 
                        equipment.destination_country in countries):
                        exposed_equipment.append(equipment)
                        break
        
        exposure_rate = (len(exposed_equipment) / total_equipment) * 100 if total_equipment > 0 else 0
        
        return {
            'total_equipment': total_equipment,
            'exposed_equipment': len(exposed_equipment),
            'exposure_rate': round(exposure_rate, 2)
        }
    
    def _analyze_cost_impact(self, events: List[NewsEvent], equipment_list: List[Equipment]) -> Dict[str, Any]:
        """分析成本影響"""
        # 簡化的成本影響分析
        high_cost_events = [e for e in events if 'tariff increase' in e.content.lower() or '關稅上調' in e.content]
        
        # 估算受影響設備的成本增加
        affected_equipment_count = 0
        estimated_cost_increase = 0
        
        for equipment in equipment_list:
            # 檢查設備是否受到關稅影響
            for event in high_cost_events:
                if (event.country == equipment.manufacturing_country or 
                    event.country == equipment.destination_country):
                    affected_equipment_count += 1
                    # 假設關稅增加導致5-15%的成本增加
                    estimated_cost_increase += 10  # 平均10%
                    break
        
        avg_cost_increase = (estimated_cost_increase / affected_equipment_count) if affected_equipment_count > 0 else 0
        
        return {
            'high_cost_events': len(high_cost_events),
            'affected_equipment_count': affected_equipment_count,
            'estimated_avg_cost_increase_percent': round(avg_cost_increase, 2)
        }
    
    def _get_top_risk_trade_routes(self, route_scores: Dict[str, float], top_n: int) -> List[Dict[str, Any]]:
        """獲取風險最高的貿易路線"""
        sorted_routes = sorted(route_scores.items(), key=lambda x: x[1], reverse=True)
        
        top_routes = []
        for route, score in sorted_routes[:top_n]:
            risk_level = self.calculate_risk_level(min(100, score))
            top_routes.append({
                'trade_route': route,
                'risk_score': round(score, 2),
                'risk_level': risk_level,
                'countries': self.trade_relationships.get(route, [])
            })
        
        return top_routes
    
    def _calculate_tariff_risk_score(self, analysis_results: Dict[str, Any]) -> float:
        """計算關稅風險分數"""
        high_impact_events = analysis_results.get('high_impact_events', 0)
        recent_events = analysis_results.get('recent_events', 0)
        exposure_rate = analysis_results.get('trade_exposure', {}).get('exposure_rate', 0)
        trade_war_events = analysis_results.get('trade_war_risks', {}).get('total_trade_war_events', 0)
        cost_events = analysis_results.get('cost_impact', {}).get('high_cost_events', 0)
        
        # 基於高影響事件的風險分數 (0-30分)
        high_impact_score = min(30, high_impact_events * 6)
        
        # 基於最近事件的風險分數 (0-25分)
        recent_score = min(25, recent_events * 3)
        
        # 基於貿易暴露度的風險分數 (0-25分)
        exposure_score = min(25, exposure_rate * 0.4)
        
        # 基於貿易戰風險的風險分數 (0-15分)
        trade_war_score = min(15, trade_war_events * 4)
        
        # 基於成本影響的風險分數 (0-5分)
        cost_score = min(5, cost_events * 2)
        
        total_score = high_impact_score + recent_score + exposure_score + trade_war_score + cost_score
        
        return min(100, total_score)
    
    def _generate_summary(self, analysis_results: Dict[str, Any]) -> str:
        """生成分析摘要"""
        total_events = analysis_results['total_events']
        high_impact = analysis_results['high_impact_events']
        affected_routes = len(analysis_results['affected_trade_routes'])
        exposed_equipment = analysis_results['trade_exposure']['exposed_equipment']
        trade_war_events = analysis_results['trade_war_risks']['total_trade_war_events']
        
        summary = f"分析了 {total_events} 個關稅事件，其中 {high_impact} 個高影響事件，"
        summary += f"影響 {affected_routes} 條主要貿易路線，可能影響 {exposed_equipment} 個設備項目"
        
        if trade_war_events > 0:
            summary += f"，發現 {trade_war_events} 個貿易戰相關事件"
        
        summary += "。"
        
        return summary
    
    def _generate_recommendations(self, analysis_results: Dict[str, Any]) -> List[str]:
        """生成建議"""
        recommendations = []
        
        high_impact_events = analysis_results.get('high_impact_events', 0)
        exposure_rate = analysis_results.get('trade_exposure', {}).get('exposure_rate', 0)
        top_risk_routes = analysis_results.get('top_risk_routes', [])
        trade_war_risk = analysis_results.get('trade_war_risks', {}).get('escalation_risk', False)
        cost_increase = analysis_results.get('cost_impact', {}).get('estimated_avg_cost_increase_percent', 0)
        
        if high_impact_events > 2:
            recommendations.append('關稅高影響事件較多，建議重新評估貿易策略')
        
        if exposure_rate > 50:
            recommendations.append('貿易暴露度較高，建議考慮供應鏈多元化')
        
        if top_risk_routes:
            high_risk_route = top_risk_routes[0]['trade_route']
            recommendations.append(f'特別關注 {high_risk_route} 的關稅政策變化')
        
        if trade_war_risk:
            recommendations.append('貿易戰升級風險較高，建議準備應對措施')
        
        if cost_increase > 5:
            recommendations.append(f'預估成本增加 {cost_increase:.1f}%，建議調整定價策略')
        
        # 通用建議
        recommendations.extend([
            '密切監控貿易政策變化',
            '評估關稅對成本的影響',
            '考慮調整供應商結構',
            '準備貿易合規方案'
        ])
        
        return recommendations[:6]
    
    def _get_affected_equipment(self, equipment_list: List[Equipment], affected_routes: List[str]) -> List[Dict[str, Any]]:
        """獲取受影響的設備"""
        affected_equipment = []
        
        for equipment in equipment_list:
            for route_name in affected_routes:
                if route_name in self.trade_relationships:
                    countries = self.trade_relationships[route_name]
                    if (equipment.manufacturing_country in countries and 
                        equipment.destination_country in countries):
                        affected_equipment.append(equipment.to_dict())
                        break
        
        return affected_equipment[:5]  # 只返回前5個
    
    def analyze_trade_relationship(self, country1: str, country2: str) -> Dict[str, Any]:
        """
        分析特定貿易關係的關稅風險
        
        Args:
            country1: 國家1
            country2: 國家2
            
        Returns:
            貿易關係關稅風險分析結果
        """
        self.log_thinking(f"分析 {country1} 與 {country2} 的貿易關稅風險...")
        
        # 獲取相關的關稅事件
        related_events = NewsEvent.query.filter(
            NewsEvent.category == 'tariff',
            NewsEvent.country.in_([country1, country2])
        ).order_by(NewsEvent.published_date.desc()).limit(10).all()
        
        # 獲取該貿易關係的設備
        trade_equipment = Equipment.query.filter(
            ((Equipment.manufacturing_country == country1) & (Equipment.destination_country == country2)) |
            ((Equipment.manufacturing_country == country2) & (Equipment.destination_country == country1))
        ).all()
        
        # 分析貿易關係風險
        analysis_results = self._analyze_bilateral_trade(related_events, trade_equipment, country1, country2)
        risk_score = self._calculate_bilateral_risk_score(analysis_results)
        risk_level = self.calculate_risk_level(risk_score)
        
        summary = f"{country1} 與 {country2} 的貿易關稅風險分析：發現 {len(related_events)} 個相關事件，涉及 {len(trade_equipment)} 個設備項目"
        
        return self.format_response(
            analysis_type='bilateral_tariff',
            risk_level=risk_level,
            risk_score=risk_score,
            summary=summary,
            details=analysis_results,
            recommendations=self._generate_bilateral_recommendations(country1, country2, analysis_results),
            trade_relationship={
                'country1': country1,
                'country2': country2
            },
            recent_events=[event.to_dict() for event in related_events[:5]],
            trade_equipment=[eq.to_dict() for eq in trade_equipment[:5]]
        )
    
    def _analyze_bilateral_trade(self, events: List[NewsEvent], equipment: List[Equipment], country1: str, country2: str) -> Dict[str, Any]:
        """分析雙邊貿易風險"""
        high_impact_events = [e for e in events if e.impact_level == 'high']
        recent_events = [e for e in events if (datetime.now() - e.published_date).days <= 60]
        
        # 分析事件類型
        event_types = {}
        for event in events:
            keywords = self.extract_keywords(event.title + " " + event.content)
            for keyword in keywords:
                if keyword in self.tariff_keywords:
                    event_types[keyword] = event_types.get(keyword, 0) + 1
        
        # 檢查是否存在貿易戰
        trade_war_indicators = ['trade war', 'tariff war', '貿易戰', '關稅戰']
        has_trade_war = any(
            any(indicator in (event.title + " " + event.content).lower() for indicator in trade_war_indicators)
            for event in events
        )
        
        return {
            'total_events': len(events),
            'high_impact_events': len(high_impact_events),
            'recent_events': len(recent_events),
            'trade_equipment': len(equipment),
            'event_types': event_types,
            'has_trade_war': has_trade_war,
            'latest_event_date': events[0].published_date.isoformat() if events else None
        }
    
    def _calculate_bilateral_risk_score(self, analysis_results: Dict[str, Any]) -> float:
        """計算雙邊貿易風險分數"""
        high_impact = analysis_results.get('high_impact_events', 0)
        recent_events = analysis_results.get('recent_events', 0)
        total_events = analysis_results.get('total_events', 0)
        has_trade_war = analysis_results.get('has_trade_war', False)
        
        # 基於高影響事件
        high_impact_score = min(40, high_impact * 12)
        
        # 基於最近事件
        recent_score = min(30, recent_events * 6)
        
        # 基於總事件數
        total_score = min(15, total_events * 1.5)
        
        # 貿易戰加權
        trade_war_score = 15 if has_trade_war else 0
        
        return min(100, high_impact_score + recent_score + total_score + trade_war_score)
    
    def _generate_bilateral_recommendations(self, country1: str, country2: str, analysis_results: Dict[str, Any]) -> List[str]:
        """生成雙邊貿易建議"""
        recommendations = []
        
        high_impact = analysis_results.get('high_impact_events', 0)
        recent_events = analysis_results.get('recent_events', 0)
        has_trade_war = analysis_results.get('has_trade_war', False)
        
        if high_impact > 1:
            recommendations.append(f'{country1} 與 {country2} 存在高影響關稅事件，建議重新評估貿易成本')
        
        if recent_events > 2:
            recommendations.append(f'{country1}-{country2} 貿易關係最近變化較大，建議密切監控')
        
        if has_trade_war:
            recommendations.append(f'{country1} 與 {country2} 存在貿易戰風險，建議準備替代方案')
        
        recommendations.extend([
            f'關注 {country1} 與 {country2} 的貿易協定變化',
            f'評估 {country1}-{country2} 貿易路線的替代選項',
            f'準備 {country1} 與 {country2} 之間的合規文件'
        ])
        
        return recommendations[:5]

