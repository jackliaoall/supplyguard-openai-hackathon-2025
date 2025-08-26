"""
物流風險分析代理
負責監控運輸和物流中斷風險
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from datetime import datetime, timedelta
from typing import Dict, List, Any
from src.ai_agents.base_agent import BaseAgent
from src.models.supply_chain import Equipment, NewsEvent

class LogisticsAgent(BaseAgent):
    """物流風險分析代理"""
    
    def __init__(self):
        super().__init__(
            name="LOGISTICS_AGENT",
            description="監控運輸和物流中斷風險，分析港口、航運、陸運等物流環節的風險"
        )
        
        # 物流風險關鍵字
        self.logistics_keywords = [
            'port', 'shipping', 'transport', 'logistics', 'cargo', 'freight',
            'delay', 'congestion', 'strike', 'blockage', 'route', 'customs',
            '港口', '航運', '運輸', '物流', '貨物', '貨運', '延遲', '擁堵', 
            '罷工', '阻塞', '路線', '海關'
        ]
        
        # 主要物流路線
        self.major_routes = {
            '亞洲-歐洲': ['中國', '日本', '韓國', '德國', '荷蘭', '英國'],
            '亞洲-北美': ['中國', '日本', '韓國', '美國', '加拿大'],
            '歐洲-北美': ['德國', '荷蘭', '英國', '美國', '加拿大'],
            '亞洲內部': ['中國', '日本', '韓國', '台灣', '新加坡']
        }
    
    def analyze(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        分析物流風險
        
        Args:
            data: 包含物流相關資訊的數據
            
        Returns:
            物流風險分析結果
        """
        self.log_thinking("開始分析物流風險...")
        
        # 獲取物流相關新聞事件
        logistics_events = NewsEvent.query.filter_by(category='logistics').order_by(
            NewsEvent.published_date.desc()
        ).limit(20).all()
        
        # 獲取所有設備以分析物流路線
        equipment_list = Equipment.query.all()
        
        # 分析物流風險
        analysis_results = self._analyze_logistics_risks(logistics_events, equipment_list)
        
        # 計算整體風險分數
        risk_score = self._calculate_logistics_risk_score(analysis_results)
        risk_level = self.calculate_risk_level(risk_score)
        
        # 生成摘要
        summary = self._generate_summary(analysis_results)
        
        # 生成建議
        recommendations = self._generate_recommendations(analysis_results)
        
        # 獲取受影響的設備
        affected_equipment = self._get_affected_equipment(equipment_list, analysis_results['affected_routes'])
        
        return self.format_response(
            analysis_type='logistics',
            risk_level=risk_level,
            risk_score=risk_score,
            summary=summary,
            details=analysis_results,
            recommendations=recommendations,
            recent_events=[event.to_dict() for event in logistics_events[:5]],
            affected_equipment=affected_equipment
        )
    
    def _analyze_logistics_risks(self, events: List[NewsEvent], equipment_list: List[Equipment]) -> Dict[str, Any]:
        """分析物流風險"""
        # 統計事件
        total_events = len(events)
        high_impact_events = [e for e in events if e.impact_level == 'high']
        recent_events = [e for e in events if (datetime.now() - e.published_date).days <= 7]
        
        # 分析受影響的路線
        affected_routes = set()
        route_risk_scores = {}
        
        # 分析物流路線風險
        for route_name, countries in self.major_routes.items():
            route_events = [e for e in events if e.country in countries]
            if route_events:
                affected_routes.add(route_name)
                
                # 計算路線風險分數
                route_score = 0
                for event in route_events:
                    if event.impact_level == 'high':
                        route_score += 25
                    elif event.impact_level == 'medium':
                        route_score += 15
                    else:
                        route_score += 5
                    
                    # 最近事件加權
                    if (datetime.now() - event.published_date).days <= 7:
                        route_score += 10
                
                route_risk_scores[route_name] = route_score
        
        # 分析關鍵字頻率
        keyword_frequency = {}
        for event in events:
            keywords = self.extract_keywords(event.title + " " + event.content)
            for keyword in keywords:
                if keyword in self.logistics_keywords:
                    keyword_frequency[keyword] = keyword_frequency.get(keyword, 0) + 1
        
        # 分析港口風險
        port_risks = self._analyze_port_risks(events)
        
        # 計算供應鏈物流暴露度
        logistics_exposure = self._calculate_logistics_exposure(equipment_list, affected_routes)
        
        return {
            'total_events': total_events,
            'high_impact_events': len(high_impact_events),
            'recent_events': len(recent_events),
            'affected_routes': list(affected_routes),
            'route_risk_scores': route_risk_scores,
            'keyword_frequency': keyword_frequency,
            'port_risks': port_risks,
            'logistics_exposure': logistics_exposure,
            'top_risk_routes': self._get_top_risk_routes(route_risk_scores, 3)
        }
    
    def _analyze_port_risks(self, events: List[NewsEvent]) -> Dict[str, Any]:
        """分析港口風險"""
        port_keywords = ['port', 'harbor', 'dock', '港口', '碼頭']
        port_events = []
        
        for event in events:
            event_text = (event.title + " " + event.content).lower()
            if any(keyword in event_text for keyword in port_keywords):
                port_events.append(event)
        
        # 統計港口相關事件
        port_countries = {}
        for event in port_events:
            if event.country:
                port_countries[event.country] = port_countries.get(event.country, 0) + 1
        
        return {
            'total_port_events': len(port_events),
            'affected_port_countries': port_countries,
            'high_risk_ports': [country for country, count in port_countries.items() if count >= 2]
        }
    
    def _calculate_logistics_exposure(self, equipment_list: List[Equipment], affected_routes: set) -> Dict[str, Any]:
        """計算物流暴露度"""
        total_equipment = len(equipment_list)
        exposed_equipment = []
        
        for equipment in equipment_list:
            # 檢查設備是否在受影響的路線上
            for route_name, countries in self.major_routes.items():
                if route_name in affected_routes:
                    if (equipment.manufacturing_country in countries or 
                        equipment.destination_country in countries):
                        exposed_equipment.append(equipment)
                        break
        
        exposure_rate = (len(exposed_equipment) / total_equipment) * 100 if total_equipment > 0 else 0
        
        return {
            'total_equipment': total_equipment,
            'exposed_equipment': len(exposed_equipment),
            'exposure_rate': round(exposure_rate, 2)
        }
    
    def _get_top_risk_routes(self, route_risk_scores: Dict[str, float], top_n: int) -> List[Dict[str, Any]]:
        """獲取風險最高的路線"""
        sorted_routes = sorted(route_risk_scores.items(), key=lambda x: x[1], reverse=True)
        
        top_routes = []
        for route, score in sorted_routes[:top_n]:
            risk_level = self.calculate_risk_level(min(100, score))
            top_routes.append({
                'route': route,
                'risk_score': round(score, 2),
                'risk_level': risk_level,
                'countries': self.major_routes.get(route, [])
            })
        
        return top_routes
    
    def _calculate_logistics_risk_score(self, analysis_results: Dict[str, Any]) -> float:
        """計算物流風險分數"""
        high_impact_events = analysis_results.get('high_impact_events', 0)
        recent_events = analysis_results.get('recent_events', 0)
        exposure_rate = analysis_results.get('logistics_exposure', {}).get('exposure_rate', 0)
        port_events = analysis_results.get('port_risks', {}).get('total_port_events', 0)
        
        # 基於高影響事件的風險分數 (0-35分)
        high_impact_score = min(35, high_impact_events * 7)
        
        # 基於最近事件的風險分數 (0-25分)
        recent_score = min(25, recent_events * 4)
        
        # 基於物流暴露度的風險分數 (0-25分)
        exposure_score = min(25, exposure_rate * 0.4)
        
        # 基於港口風險的風險分數 (0-15分)
        port_score = min(15, port_events * 3)
        
        total_score = high_impact_score + recent_score + exposure_score + port_score
        
        return min(100, total_score)
    
    def _generate_summary(self, analysis_results: Dict[str, Any]) -> str:
        """生成分析摘要"""
        total_events = analysis_results['total_events']
        high_impact = analysis_results['high_impact_events']
        affected_routes = len(analysis_results['affected_routes'])
        exposed_equipment = analysis_results['logistics_exposure']['exposed_equipment']
        port_events = analysis_results['port_risks']['total_port_events']
        
        summary = f"分析了 {total_events} 個物流事件，其中 {high_impact} 個高影響事件，"
        summary += f"影響 {affected_routes} 條主要物流路線，可能影響 {exposed_equipment} 個設備項目"
        
        if port_events > 0:
            summary += f"，發現 {port_events} 個港口相關風險事件"
        
        summary += "。"
        
        return summary
    
    def _generate_recommendations(self, analysis_results: Dict[str, Any]) -> List[str]:
        """生成建議"""
        recommendations = []
        
        high_impact_events = analysis_results.get('high_impact_events', 0)
        exposure_rate = analysis_results.get('logistics_exposure', {}).get('exposure_rate', 0)
        top_risk_routes = analysis_results.get('top_risk_routes', [])
        port_events = analysis_results.get('port_risks', {}).get('total_port_events', 0)
        
        if high_impact_events > 2:
            recommendations.append('物流高影響事件較多，建議加強運輸風險管控')
        
        if exposure_rate > 60:
            recommendations.append('物流暴露度較高，建議考慮多元化運輸路線')
        
        if top_risk_routes:
            high_risk_route = top_risk_routes[0]['route']
            recommendations.append(f'特別關注 {high_risk_route} 路線的物流狀況')
        
        if port_events > 3:
            recommendations.append('港口風險事件頻發，建議評估替代港口選項')
        
        # 通用建議
        recommendations.extend([
            '密切監控主要物流路線狀況',
            '與物流服務商保持密切溝通',
            '準備備用運輸方案',
            '考慮增加庫存緩衝'
        ])
        
        return recommendations[:6]
    
    def _get_affected_equipment(self, equipment_list: List[Equipment], affected_routes: List[str]) -> List[Dict[str, Any]]:
        """獲取受影響的設備"""
        affected_equipment = []
        
        for equipment in equipment_list:
            for route_name in affected_routes:
                if route_name in self.major_routes:
                    countries = self.major_routes[route_name]
                    if (equipment.manufacturing_country in countries or 
                        equipment.destination_country in countries):
                        affected_equipment.append(equipment.to_dict())
                        break
        
        return affected_equipment[:5]  # 只返回前5個
    
    def analyze_route_risk(self, origin_country: str, destination_country: str) -> Dict[str, Any]:
        """
        分析特定路線的物流風險
        
        Args:
            origin_country: 起始國家
            destination_country: 目的地國家
            
        Returns:
            路線物流風險分析結果
        """
        self.log_thinking(f"分析 {origin_country} 到 {destination_country} 的物流風險...")
        
        # 確定路線類型
        route_type = self._determine_route_type(origin_country, destination_country)
        
        # 獲取相關的物流事件
        related_events = NewsEvent.query.filter(
            NewsEvent.category == 'logistics',
            NewsEvent.country.in_([origin_country, destination_country])
        ).order_by(NewsEvent.published_date.desc()).limit(10).all()
        
        # 獲取該路線的設備
        route_equipment = Equipment.query.filter(
            Equipment.manufacturing_country == origin_country,
            Equipment.destination_country == destination_country
        ).all()
        
        # 分析路線風險
        analysis_results = self._analyze_route_logistics(related_events, route_equipment, route_type)
        risk_score = self._calculate_route_risk_score(analysis_results)
        risk_level = self.calculate_risk_level(risk_score)
        
        summary = f"{origin_country} 到 {destination_country} 的物流風險分析：發現 {len(related_events)} 個相關事件，涉及 {len(route_equipment)} 個設備項目"
        
        return self.format_response(
            analysis_type='route_logistics',
            risk_level=risk_level,
            risk_score=risk_score,
            summary=summary,
            details=analysis_results,
            recommendations=self._generate_route_recommendations(origin_country, destination_country, analysis_results),
            route_info={
                'origin': origin_country,
                'destination': destination_country,
                'route_type': route_type
            },
            recent_events=[event.to_dict() for event in related_events[:5]],
            route_equipment=[eq.to_dict() for eq in route_equipment[:5]]
        )
    
    def _determine_route_type(self, origin: str, destination: str) -> str:
        """確定路線類型"""
        for route_name, countries in self.major_routes.items():
            if origin in countries and destination in countries:
                return route_name
        return '其他路線'
    
    def _analyze_route_logistics(self, events: List[NewsEvent], equipment: List[Equipment], route_type: str) -> Dict[str, Any]:
        """分析路線物流風險"""
        high_impact_events = [e for e in events if e.impact_level == 'high']
        recent_events = [e for e in events if (datetime.now() - e.published_date).days <= 30]
        
        # 分析事件類型
        event_types = {}
        for event in events:
            keywords = self.extract_keywords(event.title + " " + event.content)
            for keyword in keywords:
                if keyword in self.logistics_keywords:
                    event_types[keyword] = event_types.get(keyword, 0) + 1
        
        return {
            'total_events': len(events),
            'high_impact_events': len(high_impact_events),
            'recent_events': len(recent_events),
            'route_equipment': len(equipment),
            'route_type': route_type,
            'event_types': event_types,
            'latest_event_date': events[0].published_date.isoformat() if events else None
        }
    
    def _calculate_route_risk_score(self, analysis_results: Dict[str, Any]) -> float:
        """計算路線風險分數"""
        high_impact = analysis_results.get('high_impact_events', 0)
        recent_events = analysis_results.get('recent_events', 0)
        total_events = analysis_results.get('total_events', 0)
        
        # 基於高影響事件
        high_impact_score = min(45, high_impact * 15)
        
        # 基於最近事件
        recent_score = min(35, recent_events * 8)
        
        # 基於總事件數
        total_score = min(20, total_events * 2)
        
        return min(100, high_impact_score + recent_score + total_score)
    
    def _generate_route_recommendations(self, origin: str, destination: str, analysis_results: Dict[str, Any]) -> List[str]:
        """生成路線特定建議"""
        recommendations = []
        
        high_impact = analysis_results.get('high_impact_events', 0)
        recent_events = analysis_results.get('recent_events', 0)
        route_type = analysis_results.get('route_type', '')
        
        if high_impact > 1:
            recommendations.append(f'{origin} 到 {destination} 路線存在高影響物流事件，建議評估替代路線')
        
        if recent_events > 2:
            recommendations.append(f'{route_type} 最近物流活動異常，建議密切監控')
        
        recommendations.extend([
            f'與 {origin} 和 {destination} 的物流合作夥伴保持聯繫',
            f'評估 {route_type} 的替代運輸方案',
            f'關注 {origin}-{destination} 路線的海關政策變化'
        ])
        
        return recommendations[:5]

