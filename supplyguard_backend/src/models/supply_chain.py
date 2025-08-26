from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from src.models.user import db

class Equipment(db.Model):
    """設備表 - 儲存供應鏈中的設備資訊"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    manufacturer = db.Column(db.String(200), nullable=False)
    manufacturing_country = db.Column(db.String(100), nullable=False)
    destination_country = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 關聯到排程
    schedules = db.relationship('Schedule', backref='equipment', lazy=True)
    
    def __repr__(self):
        return f'<Equipment {self.name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'manufacturer': self.manufacturer,
            'manufacturing_country': self.manufacturing_country,
            'destination_country': self.destination_country,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class Schedule(db.Model):
    """排程表 - 儲存設備的交付排程資訊"""
    id = db.Column(db.Integer, primary_key=True)
    equipment_id = db.Column(db.Integer, db.ForeignKey('equipment.id'), nullable=False)
    planned_start_date = db.Column(db.DateTime, nullable=False)
    planned_end_date = db.Column(db.DateTime, nullable=False)
    actual_start_date = db.Column(db.DateTime, nullable=True)
    actual_end_date = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(50), nullable=False, default='planned')  # planned, in_progress, delayed, completed
    delay_days = db.Column(db.Integer, default=0)
    risk_level = db.Column(db.String(20), default='low')  # low, medium, high, critical
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Schedule {self.id} for Equipment {self.equipment_id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'equipment_id': self.equipment_id,
            'planned_start_date': self.planned_start_date.isoformat() if self.planned_start_date else None,
            'planned_end_date': self.planned_end_date.isoformat() if self.planned_end_date else None,
            'actual_start_date': self.actual_start_date.isoformat() if self.actual_start_date else None,
            'actual_end_date': self.actual_end_date.isoformat() if self.actual_end_date else None,
            'status': self.status,
            'delay_days': self.delay_days,
            'risk_level': self.risk_level,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class RiskAssessment(db.Model):
    """風險評估表 - 儲存AI代理分析的風險評估結果"""
    id = db.Column(db.Integer, primary_key=True)
    equipment_id = db.Column(db.Integer, db.ForeignKey('equipment.id'), nullable=True)
    risk_type = db.Column(db.String(50), nullable=False)  # schedule, political, tariff, logistics
    risk_level = db.Column(db.String(20), nullable=False)  # low, medium, high, critical
    risk_score = db.Column(db.Float, nullable=False)  # 0-100
    description = db.Column(db.Text, nullable=False)
    recommendations = db.Column(db.Text, nullable=True)
    sources = db.Column(db.Text, nullable=True)  # JSON格式儲存來源連結
    agent_name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 關聯到設備
    equipment = db.relationship('Equipment', backref='risk_assessments')

    def __repr__(self):
        return f'<RiskAssessment {self.id} - {self.risk_type}>'

    def to_dict(self):
        return {
            'id': self.id,
            'equipment_id': self.equipment_id,
            'risk_type': self.risk_type,
            'risk_level': self.risk_level,
            'risk_score': self.risk_score,
            'description': self.description,
            'recommendations': self.recommendations,
            'sources': self.sources,
            'agent_name': self.agent_name,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class NewsEvent(db.Model):
    """新聞事件表 - 儲存影響供應鏈的新聞事件"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500), nullable=False)
    content = db.Column(db.Text, nullable=False)
    source = db.Column(db.String(200), nullable=False)
    url = db.Column(db.String(1000), nullable=True)
    country = db.Column(db.String(100), nullable=True)
    category = db.Column(db.String(100), nullable=False)  # political, economic, logistics, natural_disaster
    impact_level = db.Column(db.String(20), default='medium')  # low, medium, high
    published_date = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<NewsEvent {self.id} - {self.title[:50]}>'

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'source': self.source,
            'url': self.url,
            'country': self.country,
            'category': self.category,
            'impact_level': self.impact_level,
            'published_date': self.published_date.isoformat() if self.published_date else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

