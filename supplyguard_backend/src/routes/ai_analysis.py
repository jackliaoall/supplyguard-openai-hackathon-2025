from flask import Blueprint, jsonify, request
from src.models.user import db
from src.models.supply_chain import Equipment, Schedule, RiskAssessment, NewsEvent
import json
from datetime import datetime, timedelta
import random

ai_analysis_bp = Blueprint('ai_analysis', __name__)

@ai_analysis_bp.route('/analyze/query', methods=['POST'])
def analyze_query():
    """Process natural language queries and return analysis results"""
    data = request.json
    query = data.get('query', '')

    # This will integrate real AI agents in the future
    # Currently returning simulated analysis results

    # Simple keyword analysis to determine query type
    query_lower = query.lower()
    
    if any(keyword in query_lower for keyword in ['schedule', 'delay', 'timeline', '排程', '延遲', '時間']):
        return analyze_schedule_risks()
    elif any(keyword in query_lower for keyword in ['political', 'politics', 'geopolitical', '政治', '地緣政治']):
        return analyze_political_risks()
    elif any(keyword in query_lower for keyword in ['tariff', 'trade', 'customs', '關稅', '貿易', '海關']):
        return analyze_tariff_risks()
    elif any(keyword in query_lower for keyword in ['logistics', 'shipping', 'transport', '物流', '運輸', '航運']):
        return analyze_logistics_risks()
    else:
        return analyze_general_risks()

def analyze_schedule_risks():
    """分析排程風險"""
    schedules = Schedule.query.all()
    
    # 計算風險統計
    total_schedules = len(schedules)
    delayed_schedules = len([s for s in schedules if s.delay_days > 0])
    high_risk_schedules = len([s for s in schedules if s.risk_level in ['high', 'critical']])
    
    # 生成風險分析報告
    analysis_result = {
        'analysis_type': 'schedule',
        'agent_name': 'SCHEDULER_AGENT',
        'summary': f'分析了 {total_schedules} 個排程項目，發現 {delayed_schedules} 個延遲項目，{high_risk_schedules} 個高風險項目。',
        'risk_level': 'medium' if delayed_schedules > total_schedules * 0.3 else 'low',
        'risk_score': min(100, (delayed_schedules / max(total_schedules, 1)) * 100 + (high_risk_schedules / max(total_schedules, 1)) * 50),
        'details': {
            'total_schedules': total_schedules,
            'delayed_schedules': delayed_schedules,
            'high_risk_schedules': high_risk_schedules,
            'delay_rate': round((delayed_schedules / max(total_schedules, 1)) * 100, 2)
        },
        'recommendations': [
            '密切監控高風險排程項目',
            '與供應商確認交付時間表',
            '準備備用供應商方案',
            '提前安排物流資源'
        ],
        'affected_equipment': [schedule.equipment.to_dict() for schedule in schedules if schedule.risk_level in ['high', 'critical']][:5]
    }
    
    return jsonify(analysis_result)

def analyze_political_risks():
    """分析政治風險"""
    # 獲取最近的政治相關新聞事件
    political_events = NewsEvent.query.filter_by(category='political').order_by(NewsEvent.published_date.desc()).limit(10).all()
    
    # 獲取涉及的國家
    countries = set()
    for event in political_events:
        if event.country:
            countries.add(event.country)
    
    # 獲取這些國家相關的設備
    affected_equipment = Equipment.query.filter(
        (Equipment.manufacturing_country.in_(countries)) | 
        (Equipment.destination_country.in_(countries))
    ).all()
    
    # 計算風險等級
    high_impact_events = len([e for e in political_events if e.impact_level == 'high'])
    risk_level = 'high' if high_impact_events > 3 else 'medium' if high_impact_events > 1 else 'low'
    
    analysis_result = {
        'analysis_type': 'political',
        'agent_name': 'POLITICAL_RISK_AGENT',
        'summary': f'分析了 {len(political_events)} 個政治事件，涉及 {len(countries)} 個國家，可能影響 {len(affected_equipment)} 個設備項目。',
        'risk_level': risk_level,
        'risk_score': min(100, high_impact_events * 25 + len(political_events) * 5),
        'details': {
            'total_events': len(political_events),
            'high_impact_events': high_impact_events,
            'affected_countries': list(countries),
            'affected_equipment_count': len(affected_equipment)
        },
        'recommendations': [
            '持續監控政治局勢發展',
            '評估供應鏈多元化選項',
            '與當地合作夥伴保持密切聯繫',
            '準備應急採購計劃'
        ],
        'recent_events': [event.to_dict() for event in political_events[:5]],
        'affected_equipment': [eq.to_dict() for eq in affected_equipment[:5]]
    }
    
    return jsonify(analysis_result)

def analyze_tariff_risks():
    """分析關稅風險"""
    # 獲取經濟相關新聞事件
    economic_events = NewsEvent.query.filter_by(category='economic').order_by(NewsEvent.published_date.desc()).limit(10).all()
    
    # 模擬關稅風險分析
    analysis_result = {
        'analysis_type': 'tariff',
        'agent_name': 'TARIFF_AGENT',
        'summary': f'分析了 {len(economic_events)} 個經濟事件，識別出潛在的關稅和貿易政策風險。',
        'risk_level': 'medium',
        'risk_score': 45,
        'details': {
            'total_events': len(economic_events),
            'trade_policy_changes': 3,
            'tariff_increases': 2,
            'affected_categories': ['電子設備', '機械設備', '原材料']
        },
        'recommendations': [
            '監控貿易政策變化',
            '評估成本影響',
            '考慮供應鏈重新配置',
            '與貿易專家諮詢'
        ],
        'recent_events': [event.to_dict() for event in economic_events[:5]]
    }
    
    return jsonify(analysis_result)

def analyze_logistics_risks():
    """分析物流風險"""
    # 獲取物流相關新聞事件
    logistics_events = NewsEvent.query.filter_by(category='logistics').order_by(NewsEvent.published_date.desc()).limit(10).all()
    
    analysis_result = {
        'analysis_type': 'logistics',
        'agent_name': 'LOGISTICS_AGENT',
        'summary': f'分析了 {len(logistics_events)} 個物流事件，評估運輸和配送風險。',
        'risk_level': 'medium',
        'risk_score': 55,
        'details': {
            'total_events': len(logistics_events),
            'port_delays': 2,
            'shipping_disruptions': 3,
            'weather_impacts': 1
        },
        'recommendations': [
            '監控主要港口狀況',
            '準備替代運輸路線',
            '與物流供應商保持溝通',
            '考慮提前發貨'
        ],
        'recent_events': [event.to_dict() for event in logistics_events[:5]]
    }
    
    return jsonify(analysis_result)

def analyze_general_risks():
    """綜合風險分析"""
    # 獲取各類風險評估
    risk_assessments = RiskAssessment.query.order_by(RiskAssessment.created_at.desc()).limit(20).all()
    
    # 按風險類型分組
    risk_by_type = {}
    for assessment in risk_assessments:
        if assessment.risk_type not in risk_by_type:
            risk_by_type[assessment.risk_type] = []
        risk_by_type[assessment.risk_type].append(assessment)
    
    # 計算整體風險等級
    high_risk_count = len([a for a in risk_assessments if a.risk_level in ['high', 'critical']])
    overall_risk_level = 'high' if high_risk_count > 5 else 'medium' if high_risk_count > 2 else 'low'
    
    analysis_result = {
        'analysis_type': 'general',
        'agent_name': 'REPORTING_AGENT',
        'summary': f'綜合分析了 {len(risk_assessments)} 個風險評估，發現 {high_risk_count} 個高風險項目。',
        'risk_level': overall_risk_level,
        'risk_score': min(100, sum([a.risk_score for a in risk_assessments]) / max(len(risk_assessments), 1)),
        'details': {
            'total_assessments': len(risk_assessments),
            'high_risk_count': high_risk_count,
            'risk_by_type': {risk_type: len(assessments) for risk_type, assessments in risk_by_type.items()}
        },
        'recommendations': [
            '優先處理高風險項目',
            '建立風險監控機制',
            '定期更新風險評估',
            '制定應急響應計劃'
        ],
        'recent_assessments': [assessment.to_dict() for assessment in risk_assessments[:10]]
    }
    
    return jsonify(analysis_result)

@ai_analysis_bp.route('/analyze/equipment/<int:equipment_id>', methods=['POST'])
def analyze_equipment_risks(equipment_id):
    """分析特定設備的風險"""
    equipment = Equipment.query.get_or_404(equipment_id)
    
    # 獲取設備相關的風險評估
    risk_assessments = RiskAssessment.query.filter_by(equipment_id=equipment_id).all()
    
    # 獲取設備的排程
    schedules = Schedule.query.filter_by(equipment_id=equipment_id).all()
    
    # 獲取相關國家的新聞事件
    country_events = NewsEvent.query.filter(
        (NewsEvent.country == equipment.manufacturing_country) |
        (NewsEvent.country == equipment.destination_country)
    ).order_by(NewsEvent.published_date.desc()).limit(5).all()
    
    # 計算綜合風險分數
    if risk_assessments:
        avg_risk_score = sum([a.risk_score for a in risk_assessments]) / len(risk_assessments)
    else:
        avg_risk_score = 30  # 預設風險分數
    
    # 檢查是否有延遲
    has_delays = any(s.delay_days > 0 for s in schedules)
    if has_delays:
        avg_risk_score += 20
    
    # 檢查是否有高影響新聞事件
    high_impact_events = [e for e in country_events if e.impact_level == 'high']
    if high_impact_events:
        avg_risk_score += 15
    
    risk_level = 'critical' if avg_risk_score > 80 else 'high' if avg_risk_score > 60 else 'medium' if avg_risk_score > 40 else 'low'
    
    analysis_result = {
        'equipment': equipment.to_dict(),
        'overall_risk_level': risk_level,
        'overall_risk_score': min(100, avg_risk_score),
        'risk_assessments': [assessment.to_dict() for assessment in risk_assessments],
        'schedules': [schedule.to_dict() for schedule in schedules],
        'related_events': [event.to_dict() for event in country_events],
        'recommendations': generate_equipment_recommendations(equipment, risk_assessments, schedules, country_events)
    }
    
    return jsonify(analysis_result)

def generate_equipment_recommendations(equipment, risk_assessments, schedules, events):
    """為特定設備生成建議"""
    recommendations = []
    
    # 基於風險評估的建議
    high_risk_assessments = [a for a in risk_assessments if a.risk_level in ['high', 'critical']]
    if high_risk_assessments:
        recommendations.append(f'該設備存在 {len(high_risk_assessments)} 個高風險項目，需要立即關注')
    
    # 基於排程的建議
    delayed_schedules = [s for s in schedules if s.delay_days > 0]
    if delayed_schedules:
        recommendations.append(f'發現 {len(delayed_schedules)} 個延遲排程，建議重新評估交付時間')
    
    # 基於地緣政治事件的建議
    high_impact_events = [e for e in events if e.impact_level == 'high']
    if high_impact_events:
        recommendations.append(f'{equipment.manufacturing_country} 或 {equipment.destination_country} 存在高影響事件，建議密切監控')
    
    # 通用建議
    recommendations.extend([
        '定期更新供應商資訊',
        '建立備用供應鏈方案',
        '與相關團隊保持溝通'
    ])
    
    return recommendations

@ai_analysis_bp.route('/analyze/country/<country_name>', methods=['POST'])
def analyze_country_risks(country_name):
    """分析特定國家的風險"""
    # 獲取該國家相關的設備
    equipment_list = Equipment.query.filter(
        (Equipment.manufacturing_country == country_name) | 
        (Equipment.destination_country == country_name)
    ).all()
    
    # 獲取該國家的新聞事件
    news_events = NewsEvent.query.filter_by(country=country_name).order_by(NewsEvent.published_date.desc()).limit(20).all()
    
    # 計算風險分數
    high_impact_events = len([e for e in news_events if e.impact_level == 'high'])
    political_events = len([e for e in news_events if e.category == 'political'])
    economic_events = len([e for e in news_events if e.category == 'economic'])
    
    risk_score = min(100, high_impact_events * 20 + political_events * 10 + economic_events * 8)
    risk_level = 'critical' if risk_score > 80 else 'high' if risk_score > 60 else 'medium' if risk_score > 40 else 'low'
    
    analysis_result = {
        'country': country_name,
        'risk_level': risk_level,
        'risk_score': risk_score,
        'affected_equipment_count': len(equipment_list),
        'total_events': len(news_events),
        'high_impact_events': high_impact_events,
        'political_events': political_events,
        'economic_events': economic_events,
        'equipment': [eq.to_dict() for eq in equipment_list],
        'recent_events': [event.to_dict() for event in news_events[:10]],
        'recommendations': [
            f'密切監控 {country_name} 的政治經濟局勢',
            '評估該國家供應鏈的替代方案',
            '與當地合作夥伴保持聯繫',
            '準備應急採購計劃'
        ]
    }
    
    return jsonify(analysis_result)

@ai_analysis_bp.route('/generate-report', methods=['POST'])
def generate_comprehensive_report():
    """生成綜合風險報告"""
    data = request.json
    report_type = data.get('report_type', 'general')
    
    # 獲取基礎數據
    equipment_count = Equipment.query.count()
    schedule_count = Schedule.query.count()
    risk_assessment_count = RiskAssessment.query.count()
    news_event_count = NewsEvent.query.count()
    
    # 獲取高風險項目
    high_risk_assessments = RiskAssessment.query.filter(RiskAssessment.risk_level.in_(['high', 'critical'])).all()
    delayed_schedules = Schedule.query.filter(Schedule.delay_days > 0).all()
    
    # 生成報告
    report = {
        'report_id': f'RPT_{datetime.now().strftime("%Y%m%d_%H%M%S")}',
        'generated_at': datetime.now().isoformat(),
        'report_type': report_type,
        'summary': {
            'total_equipment': equipment_count,
            'total_schedules': schedule_count,
            'total_risk_assessments': risk_assessment_count,
            'total_news_events': news_event_count,
            'high_risk_items': len(high_risk_assessments),
            'delayed_schedules': len(delayed_schedules)
        },
        'risk_overview': {
            'overall_risk_level': calculate_overall_risk_level(high_risk_assessments, delayed_schedules),
            'critical_areas': identify_critical_areas(high_risk_assessments),
            'trending_risks': identify_trending_risks()
        },
        'detailed_analysis': {
            'high_risk_assessments': [assessment.to_dict() for assessment in high_risk_assessments[:10]],
            'delayed_schedules': [schedule.to_dict() for schedule in delayed_schedules[:10]]
        },
        'recommendations': generate_comprehensive_recommendations(high_risk_assessments, delayed_schedules),
        'next_review_date': (datetime.now() + timedelta(days=7)).isoformat()
    }
    
    return jsonify(report)

def calculate_overall_risk_level(high_risk_assessments, delayed_schedules):
    """計算整體風險等級"""
    critical_count = len([a for a in high_risk_assessments if a.risk_level == 'critical'])
    high_count = len([a for a in high_risk_assessments if a.risk_level == 'high'])
    delay_count = len(delayed_schedules)
    
    if critical_count > 5 or delay_count > 10:
        return 'critical'
    elif critical_count > 2 or high_count > 5 or delay_count > 5:
        return 'high'
    elif high_count > 2 or delay_count > 2:
        return 'medium'
    else:
        return 'low'

def identify_critical_areas(high_risk_assessments):
    """識別關鍵風險領域"""
    risk_types = {}
    for assessment in high_risk_assessments:
        if assessment.risk_type not in risk_types:
            risk_types[assessment.risk_type] = 0
        risk_types[assessment.risk_type] += 1
    
    # 排序並返回前3個風險類型
    sorted_risks = sorted(risk_types.items(), key=lambda x: x[1], reverse=True)
    return [{'risk_type': risk_type, 'count': count} for risk_type, count in sorted_risks[:3]]

def identify_trending_risks():
    """識別趨勢風險"""
    # 獲取最近7天的風險評估
    recent_date = datetime.now() - timedelta(days=7)
    recent_assessments = RiskAssessment.query.filter(RiskAssessment.created_at >= recent_date).all()
    
    # 按風險類型分組
    trending = {}
    for assessment in recent_assessments:
        if assessment.risk_type not in trending:
            trending[assessment.risk_type] = []
        trending[assessment.risk_type].append(assessment)
    
    # 計算趨勢
    trends = []
    for risk_type, assessments in trending.items():
        avg_score = sum([a.risk_score for a in assessments]) / len(assessments)
        trends.append({
            'risk_type': risk_type,
            'recent_count': len(assessments),
            'average_score': round(avg_score, 2),
            'trend': 'increasing' if avg_score > 60 else 'stable'
        })
    
    return sorted(trends, key=lambda x: x['average_score'], reverse=True)[:5]

def generate_comprehensive_recommendations(high_risk_assessments, delayed_schedules):
    """生成綜合建議"""
    recommendations = []
    
    if len(high_risk_assessments) > 5:
        recommendations.append('立即召開風險評估會議，制定應對策略')
    
    if len(delayed_schedules) > 3:
        recommendations.append('重新評估所有項目時間表，調整資源配置')
    
    # 基於風險類型的建議
    risk_types = set([a.risk_type for a in high_risk_assessments])
    if 'political' in risk_types:
        recommendations.append('加強地緣政治風險監控，準備供應鏈多元化方案')
    if 'logistics' in risk_types:
        recommendations.append('優化物流路線，建立備用運輸方案')
    if 'schedule' in risk_types:
        recommendations.append('改善項目管理流程，提高交付準確性')
    
    # 通用建議
    recommendations.extend([
        '建立定期風險評估機制',
        '加強與供應商的溝通協調',
        '投資於風險管理技術和工具',
        '培訓團隊風險識別和應對能力'
    ])
    
    return recommendations[:8]  # 限制建議數量

