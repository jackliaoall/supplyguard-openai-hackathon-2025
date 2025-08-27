"""
Schedule Analysis Agent
Responsible for analyzing equipment delivery schedule risks
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from datetime import datetime, timedelta
from typing import Dict, List, Any
from src.ai_agents.base_agent import BaseAgent
from src.models.supply_chain import Schedule, Equipment

class SchedulerAgent(BaseAgent):
    """Schedule Analysis Agent"""

    def __init__(self):
        super().__init__(
            name="SCHEDULER_AGENT",
            description="Analyze equipment delivery schedule risks, identify potential delays and timeline issues"
        )
    
    def analyze(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze schedule risks

        Args:
            data: Data containing schedule information

        Returns:
            Schedule risk analysis results
        """
        self.log_thinking("Starting schedule risk analysis...")

        # Get all schedule data
        schedules = Schedule.query.all()

        if not schedules:
            return self.format_response(
                analysis_type='schedule',
                risk_level='low',
                risk_score=0,
                summary='No schedule data found',
                details={'total_schedules': 0},
                recommendations=['Add schedule data for analysis']
            )

        # Prepare context for AI analysis
        context = self._prepare_schedule_context(schedules)

        # Create analysis query
        query = f"Analyze the delivery schedule risks for {len(schedules)} equipment schedules. Identify delays, bottlenecks, and potential timeline issues."

        # Use AI service for analysis
        ai_result = self.analyze_with_ai(query, context)

        # Combine AI results with traditional analysis
        traditional_analysis = self._analyze_schedules(schedules)

        # Merge AI insights with traditional analysis
        return self._merge_analysis_results(ai_result, traditional_analysis, schedules)

    def _prepare_schedule_context(self, schedules: List[Schedule]) -> Dict[str, Any]:
        """Prepare context information for AI analysis"""
        now = datetime.now()

        # Categorize schedules
        delayed_schedules = []
        upcoming_schedules = []
        critical_schedules = []

        for schedule in schedules:
            if schedule.delivery_date < now and schedule.status != 'completed':
                delayed_schedules.append({
                    'id': schedule.id,
                    'equipment_name': schedule.equipment.name if schedule.equipment else 'Unknown',
                    'delivery_date': schedule.delivery_date.strftime('%Y-%m-%d'),
                    'status': schedule.status,
                    'days_overdue': (now - schedule.delivery_date).days
                })
            elif schedule.delivery_date <= now + timedelta(days=7):
                upcoming_schedules.append({
                    'id': schedule.id,
                    'equipment_name': schedule.equipment.name if schedule.equipment else 'Unknown',
                    'delivery_date': schedule.delivery_date.strftime('%Y-%m-%d'),
                    'status': schedule.status,
                    'days_until_delivery': (schedule.delivery_date - now).days
                })

            if schedule.priority == 'high' or schedule.status == 'at_risk':
                critical_schedules.append({
                    'id': schedule.id,
                    'equipment_name': schedule.equipment.name if schedule.equipment else 'Unknown',
                    'priority': schedule.priority,
                    'status': schedule.status
                })

        return {
            'total_schedules': len(schedules),
            'delayed_schedules': delayed_schedules,
            'upcoming_schedules': upcoming_schedules,
            'critical_schedules': critical_schedules,
            'schedule_data': f"Total: {len(schedules)}, Delayed: {len(delayed_schedules)}, Upcoming: {len(upcoming_schedules)}, Critical: {len(critical_schedules)}"
        }

    def _merge_analysis_results(self, ai_result: Dict[str, Any], traditional_analysis: Dict[str, Any], schedules: List[Schedule]) -> Dict[str, Any]:
        """Merge AI analysis with traditional analysis"""

        # Use AI risk assessment if available, otherwise fall back to traditional
        risk_level = ai_result.get('risk_level', traditional_analysis.get('risk_level', 'medium'))
        risk_score = ai_result.get('risk_score', traditional_analysis.get('risk_score', 50))

        # Combine summaries
        ai_summary = ai_result.get('summary', '')
        traditional_summary = traditional_analysis.get('summary', '')
        combined_summary = f"{ai_summary} {traditional_summary}".strip()

        # Combine recommendations
        ai_recommendations = ai_result.get('recommendations', [])
        traditional_recommendations = traditional_analysis.get('recommendations', [])
        all_recommendations = ai_recommendations + traditional_recommendations

        # Remove duplicates and limit to top 5
        unique_recommendations = list(dict.fromkeys(all_recommendations))[:5]

        return self.format_response(
            analysis_type='schedule',
            risk_level=risk_level,
            risk_score=risk_score,
            summary=combined_summary or f"Analyzed {len(schedules)} equipment schedules",
            details={
                **traditional_analysis.get('details', {}),
                'ai_insights': ai_result.get('key_findings', []),
                'ai_confidence': ai_result.get('confidence', 75)
            },
            recommendations=unique_recommendations,
            affected_equipment=traditional_analysis.get('affected_equipment', [])
        )
        
        # 計算整體風險分數
        risk_score = self._calculate_overall_risk_score(analysis_results)
        risk_level = self.calculate_risk_level(risk_score)
        
        # 生成摘要
        summary = self._generate_summary(analysis_results)
        
        # 生成建議
        recommendations = self._generate_recommendations(analysis_results)
        
        # 獲取受影響的設備
        affected_equipment = self._get_affected_equipment(schedules)
        
        return self.format_response(
            analysis_type='schedule',
            risk_level=risk_level,
            risk_score=risk_score,
            summary=summary,
            details=analysis_results,
            recommendations=recommendations,
            affected_equipment=affected_equipment
        )
    
    def _analyze_schedules(self, schedules: List[Schedule]) -> Dict[str, Any]:
        """分析排程數據"""
        total_schedules = len(schedules)
        delayed_schedules = []
        high_risk_schedules = []
        upcoming_deadlines = []
        
        current_time = datetime.now()
        
        for schedule in schedules:
            # 檢查延遲
            if schedule.delay_days > 0:
                delayed_schedules.append(schedule)
            
            # 檢查高風險排程
            if schedule.risk_level in ['high', 'critical']:
                high_risk_schedules.append(schedule)
            
            # 檢查即將到期的排程
            if schedule.planned_end_date:
                days_to_deadline = (schedule.planned_end_date - current_time).days
                if 0 <= days_to_deadline <= 30:  # 30天內到期
                    upcoming_deadlines.append({
                        'schedule_id': schedule.id,
                        'equipment_name': schedule.equipment.name if schedule.equipment else 'Unknown',
                        'days_to_deadline': days_to_deadline,
                        'planned_end_date': schedule.planned_end_date.isoformat()
                    })
        
        # 計算統計數據
        delay_rate = (len(delayed_schedules) / total_schedules) * 100 if total_schedules > 0 else 0
        high_risk_rate = (len(high_risk_schedules) / total_schedules) * 100 if total_schedules > 0 else 0
        
        # 計算平均延遲天數
        total_delay_days = sum([s.delay_days for s in schedules])
        avg_delay_days = total_delay_days / total_schedules if total_schedules > 0 else 0
        
        return {
            'total_schedules': total_schedules,
            'delayed_schedules': len(delayed_schedules),
            'high_risk_schedules': len(high_risk_schedules),
            'upcoming_deadlines': len(upcoming_deadlines),
            'delay_rate': round(delay_rate, 2),
            'high_risk_rate': round(high_risk_rate, 2),
            'avg_delay_days': round(avg_delay_days, 2),
            'upcoming_deadlines_detail': upcoming_deadlines[:5]  # 只返回前5個
        }
    
    def _calculate_overall_risk_score(self, analysis_results: Dict[str, Any]) -> float:
        """計算整體風險分數"""
        delay_rate = analysis_results.get('delay_rate', 0)
        high_risk_rate = analysis_results.get('high_risk_rate', 0)
        upcoming_deadlines = analysis_results.get('upcoming_deadlines', 0)
        total_schedules = analysis_results.get('total_schedules', 1)
        
        # 基於延遲率的風險分數 (0-40分)
        delay_score = min(40, delay_rate * 1.5)
        
        # 基於高風險排程比例的風險分數 (0-30分)
        high_risk_score = min(30, high_risk_rate * 1.2)
        
        # 基於即將到期排程的風險分數 (0-30分)
        deadline_score = min(30, (upcoming_deadlines / total_schedules) * 100)
        
        total_score = delay_score + high_risk_score + deadline_score
        
        return min(100, total_score)
    
    def _generate_summary(self, analysis_results: Dict[str, Any]) -> str:
        """生成分析摘要"""
        total = analysis_results['total_schedules']
        delayed = analysis_results['delayed_schedules']
        high_risk = analysis_results['high_risk_schedules']
        upcoming = analysis_results['upcoming_deadlines']
        
        summary = f"分析了 {total} 個排程項目，發現 {delayed} 個延遲項目，{high_risk} 個高風險項目"
        
        if upcoming > 0:
            summary += f"，{upcoming} 個項目即將到期"
        
        summary += "。"
        
        return summary
    
    def _generate_recommendations(self, analysis_results: Dict[str, Any]) -> List[str]:
        """生成建議"""
        recommendations = []
        
        delay_rate = analysis_results.get('delay_rate', 0)
        high_risk_rate = analysis_results.get('high_risk_rate', 0)
        upcoming_deadlines = analysis_results.get('upcoming_deadlines', 0)
        
        if delay_rate > 20:
            recommendations.append('延遲率較高，建議重新評估項目時間表和資源配置')
        
        if high_risk_rate > 30:
            recommendations.append('高風險項目比例偏高，需要加強風險管控措施')
        
        if upcoming_deadlines > 5:
            recommendations.append('多個項目即將到期，建議優先處理緊急項目')
        
        # 通用建議
        recommendations.extend([
            '密切監控高風險排程項目',
            '與供應商確認交付時間表',
            '準備備用供應商方案',
            '提前安排物流資源'
        ])
        
        return recommendations[:6]  # 限制建議數量
    
    def _get_affected_equipment(self, schedules: List[Schedule]) -> List[Dict[str, Any]]:
        """獲取受影響的設備"""
        high_risk_schedules = [s for s in schedules if s.risk_level in ['high', 'critical']]
        
        affected_equipment = []
        for schedule in high_risk_schedules[:5]:  # 只返回前5個
            if schedule.equipment:
                affected_equipment.append(schedule.equipment.to_dict())
        
        return affected_equipment
    
    def analyze_equipment_schedule(self, equipment_id: int) -> Dict[str, Any]:
        """
        分析特定設備的排程風險
        
        Args:
            equipment_id: 設備ID
            
        Returns:
            設備排程風險分析結果
        """
        self.log_thinking(f"分析設備 {equipment_id} 的排程風險...")
        
        # 獲取設備的排程
        schedules = Schedule.query.filter_by(equipment_id=equipment_id).all()
        equipment = Equipment.query.get(equipment_id)
        
        if not schedules:
            return self.format_response(
                analysis_type='equipment_schedule',
                risk_level='low',
                risk_score=0,
                summary=f'設備 {equipment.name if equipment else equipment_id} 沒有排程數據',
                details={'total_schedules': 0},
                recommendations=['為該設備添加排程數據']
            )
        
        # 分析設備排程
        analysis_results = self._analyze_schedules(schedules)
        risk_score = self._calculate_overall_risk_score(analysis_results)
        risk_level = self.calculate_risk_level(risk_score)
        
        summary = f"設備 {equipment.name if equipment else equipment_id} 的排程分析：{self._generate_summary(analysis_results)}"
        
        return self.format_response(
            analysis_type='equipment_schedule',
            risk_level=risk_level,
            risk_score=risk_score,
            summary=summary,
            details=analysis_results,
            recommendations=self._generate_recommendations(analysis_results),
            equipment=equipment.to_dict() if equipment else None
        )

