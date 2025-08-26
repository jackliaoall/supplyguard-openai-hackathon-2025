from flask import Blueprint, jsonify, request
from src.models.user import db
from src.models.supply_chain import Equipment, Schedule, RiskAssessment, NewsEvent
from datetime import datetime
import json

supply_chain_bp = Blueprint('supply_chain', __name__)

# Equipment related routes
@supply_chain_bp.route('/equipment', methods=['GET'])
def get_equipment():
    """Get all equipment list"""
    equipment_list = Equipment.query.all()
    return jsonify([equipment.to_dict() for equipment in equipment_list])

@supply_chain_bp.route('/equipment', methods=['POST'])
def create_equipment():
    """建立新設備"""
    data = request.json
    equipment = Equipment(
        name=data['name'],
        category=data['category'],
        manufacturer=data['manufacturer'],
        manufacturing_country=data['manufacturing_country'],
        destination_country=data['destination_country']
    )
    db.session.add(equipment)
    db.session.commit()
    return jsonify(equipment.to_dict()), 201

@supply_chain_bp.route('/equipment/<int:equipment_id>', methods=['GET'])
def get_equipment_detail(equipment_id):
    """獲取特定設備詳細資訊"""
    equipment = Equipment.query.get_or_404(equipment_id)
    return jsonify(equipment.to_dict())

@supply_chain_bp.route('/equipment/<int:equipment_id>', methods=['PUT'])
def update_equipment(equipment_id):
    """更新設備資訊"""
    equipment = Equipment.query.get_or_404(equipment_id)
    data = request.json
    
    equipment.name = data.get('name', equipment.name)
    equipment.category = data.get('category', equipment.category)
    equipment.manufacturer = data.get('manufacturer', equipment.manufacturer)
    equipment.manufacturing_country = data.get('manufacturing_country', equipment.manufacturing_country)
    equipment.destination_country = data.get('destination_country', equipment.destination_country)
    
    db.session.commit()
    return jsonify(equipment.to_dict())

@supply_chain_bp.route('/equipment/<int:equipment_id>', methods=['DELETE'])
def delete_equipment(equipment_id):
    """刪除設備"""
    equipment = Equipment.query.get_or_404(equipment_id)
    db.session.delete(equipment)
    db.session.commit()
    return '', 204

# Schedule 相關路由
@supply_chain_bp.route('/schedules', methods=['GET'])
def get_schedules():
    """獲取所有排程"""
    schedules = Schedule.query.all()
    return jsonify([schedule.to_dict() for schedule in schedules])

@supply_chain_bp.route('/schedules', methods=['POST'])
def create_schedule():
    """建立新排程"""
    data = request.json
    schedule = Schedule(
        equipment_id=data['equipment_id'],
        planned_start_date=datetime.fromisoformat(data['planned_start_date']),
        planned_end_date=datetime.fromisoformat(data['planned_end_date']),
        status=data.get('status', 'planned'),
        risk_level=data.get('risk_level', 'low')
    )
    
    if 'actual_start_date' in data and data['actual_start_date']:
        schedule.actual_start_date = datetime.fromisoformat(data['actual_start_date'])
    if 'actual_end_date' in data and data['actual_end_date']:
        schedule.actual_end_date = datetime.fromisoformat(data['actual_end_date'])
    
    db.session.add(schedule)
    db.session.commit()
    return jsonify(schedule.to_dict()), 201

@supply_chain_bp.route('/schedules/<int:schedule_id>', methods=['GET'])
def get_schedule_detail(schedule_id):
    """獲取特定排程詳細資訊"""
    schedule = Schedule.query.get_or_404(schedule_id)
    return jsonify(schedule.to_dict())

@supply_chain_bp.route('/schedules/<int:schedule_id>', methods=['PUT'])
def update_schedule(schedule_id):
    """更新排程資訊"""
    schedule = Schedule.query.get_or_404(schedule_id)
    data = request.json
    
    if 'planned_start_date' in data:
        schedule.planned_start_date = datetime.fromisoformat(data['planned_start_date'])
    if 'planned_end_date' in data:
        schedule.planned_end_date = datetime.fromisoformat(data['planned_end_date'])
    if 'actual_start_date' in data and data['actual_start_date']:
        schedule.actual_start_date = datetime.fromisoformat(data['actual_start_date'])
    if 'actual_end_date' in data and data['actual_end_date']:
        schedule.actual_end_date = datetime.fromisoformat(data['actual_end_date'])
    
    schedule.status = data.get('status', schedule.status)
    schedule.delay_days = data.get('delay_days', schedule.delay_days)
    schedule.risk_level = data.get('risk_level', schedule.risk_level)
    
    db.session.commit()
    return jsonify(schedule.to_dict())

@supply_chain_bp.route('/schedules/<int:schedule_id>', methods=['DELETE'])
def delete_schedule(schedule_id):
    """刪除排程"""
    schedule = Schedule.query.get_or_404(schedule_id)
    db.session.delete(schedule)
    db.session.commit()
    return '', 204

# Risk Assessment 相關路由
@supply_chain_bp.route('/risk-assessments', methods=['GET'])
def get_risk_assessments():
    """獲取所有風險評估"""
    risk_assessments = RiskAssessment.query.all()
    return jsonify([assessment.to_dict() for assessment in risk_assessments])

@supply_chain_bp.route('/risk-assessments', methods=['POST'])
def create_risk_assessment():
    """建立新風險評估"""
    data = request.json
    assessment = RiskAssessment(
        equipment_id=data.get('equipment_id'),
        risk_type=data['risk_type'],
        risk_level=data['risk_level'],
        risk_score=data['risk_score'],
        description=data['description'],
        recommendations=data.get('recommendations'),
        sources=data.get('sources'),
        agent_name=data['agent_name']
    )
    db.session.add(assessment)
    db.session.commit()
    return jsonify(assessment.to_dict()), 201

@supply_chain_bp.route('/risk-assessments/<int:assessment_id>', methods=['GET'])
def get_risk_assessment_detail(assessment_id):
    """獲取特定風險評估詳細資訊"""
    assessment = RiskAssessment.query.get_or_404(assessment_id)
    return jsonify(assessment.to_dict())

@supply_chain_bp.route('/risk-assessments/<int:assessment_id>', methods=['PUT'])
def update_risk_assessment(assessment_id):
    """更新風險評估"""
    assessment = RiskAssessment.query.get_or_404(assessment_id)
    data = request.json
    
    assessment.risk_type = data.get('risk_type', assessment.risk_type)
    assessment.risk_level = data.get('risk_level', assessment.risk_level)
    assessment.risk_score = data.get('risk_score', assessment.risk_score)
    assessment.description = data.get('description', assessment.description)
    assessment.recommendations = data.get('recommendations', assessment.recommendations)
    assessment.sources = data.get('sources', assessment.sources)
    assessment.agent_name = data.get('agent_name', assessment.agent_name)
    
    db.session.commit()
    return jsonify(assessment.to_dict())

@supply_chain_bp.route('/risk-assessments/<int:assessment_id>', methods=['DELETE'])
def delete_risk_assessment(assessment_id):
    """刪除風險評估"""
    assessment = RiskAssessment.query.get_or_404(assessment_id)
    db.session.delete(assessment)
    db.session.commit()
    return '', 204

# News Event 相關路由
@supply_chain_bp.route('/news-events', methods=['GET'])
def get_news_events():
    """獲取所有新聞事件"""
    news_events = NewsEvent.query.order_by(NewsEvent.published_date.desc()).all()
    return jsonify([event.to_dict() for event in news_events])

@supply_chain_bp.route('/news-events', methods=['POST'])
def create_news_event():
    """建立新新聞事件"""
    data = request.json
    event = NewsEvent(
        title=data['title'],
        content=data['content'],
        source=data['source'],
        url=data.get('url'),
        country=data.get('country'),
        category=data['category'],
        impact_level=data.get('impact_level', 'medium'),
        published_date=datetime.fromisoformat(data['published_date'])
    )
    db.session.add(event)
    db.session.commit()
    return jsonify(event.to_dict()), 201

@supply_chain_bp.route('/news-events/<int:event_id>', methods=['GET'])
def get_news_event_detail(event_id):
    """獲取特定新聞事件詳細資訊"""
    event = NewsEvent.query.get_or_404(event_id)
    return jsonify(event.to_dict())

@supply_chain_bp.route('/news-events/<int:event_id>', methods=['PUT'])
def update_news_event(event_id):
    """更新新聞事件"""
    event = NewsEvent.query.get_or_404(event_id)
    data = request.json
    
    event.title = data.get('title', event.title)
    event.content = data.get('content', event.content)
    event.source = data.get('source', event.source)
    event.url = data.get('url', event.url)
    event.country = data.get('country', event.country)
    event.category = data.get('category', event.category)
    event.impact_level = data.get('impact_level', event.impact_level)
    
    if 'published_date' in data:
        event.published_date = datetime.fromisoformat(data['published_date'])
    
    db.session.commit()
    return jsonify(event.to_dict())

@supply_chain_bp.route('/news-events/<int:event_id>', methods=['DELETE'])
def delete_news_event(event_id):
    """刪除新聞事件"""
    event = NewsEvent.query.get_or_404(event_id)
    db.session.delete(event)
    db.session.commit()
    return '', 204

# 統計和分析相關路由
@supply_chain_bp.route('/dashboard/stats', methods=['GET'])
def get_dashboard_stats():
    """獲取儀表板統計資料"""
    total_equipment = Equipment.query.count()
    total_schedules = Schedule.query.count()
    high_risk_assessments = RiskAssessment.query.filter_by(risk_level='high').count()
    critical_risk_assessments = RiskAssessment.query.filter_by(risk_level='critical').count()
    delayed_schedules = Schedule.query.filter(Schedule.delay_days > 0).count()
    
    return jsonify({
        'total_equipment': total_equipment,
        'total_schedules': total_schedules,
        'high_risk_assessments': high_risk_assessments,
        'critical_risk_assessments': critical_risk_assessments,
        'delayed_schedules': delayed_schedules
    })

@supply_chain_bp.route('/equipment/<int:equipment_id>/risks', methods=['GET'])
def get_equipment_risks(equipment_id):
    """獲取特定設備的所有風險評估"""
    equipment = Equipment.query.get_or_404(equipment_id)
    risk_assessments = RiskAssessment.query.filter_by(equipment_id=equipment_id).all()
    return jsonify({
        'equipment': equipment.to_dict(),
        'risk_assessments': [assessment.to_dict() for assessment in risk_assessments]
    })

@supply_chain_bp.route('/countries/<country_name>/risks', methods=['GET'])
def get_country_risks(country_name):
    """獲取特定國家的風險資訊"""
    # 獲取該國家的設備
    equipment_list = Equipment.query.filter(
        (Equipment.manufacturing_country == country_name) | 
        (Equipment.destination_country == country_name)
    ).all()
    
    # 獲取該國家的新聞事件
    news_events = NewsEvent.query.filter_by(country=country_name).order_by(NewsEvent.published_date.desc()).limit(10).all()
    
    # 獲取相關的風險評估
    equipment_ids = [eq.id for eq in equipment_list]
    risk_assessments = RiskAssessment.query.filter(RiskAssessment.equipment_id.in_(equipment_ids)).all()
    
    return jsonify({
        'country': country_name,
        'equipment': [eq.to_dict() for eq in equipment_list],
        'news_events': [event.to_dict() for event in news_events],
        'risk_assessments': [assessment.to_dict() for assessment in risk_assessments]
    })

