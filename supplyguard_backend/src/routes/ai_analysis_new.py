"""
AI分析相關的API路由 - 整合AI代理
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from flask import Blueprint, request, jsonify
import logging
from src.ai_agents.agent_orchestrator import AgentOrchestrator

ai_analysis_new_bp = Blueprint('ai_analysis_new', __name__)
logger = logging.getLogger(__name__)

# 初始化代理協調器
orchestrator = AgentOrchestrator()

@ai_analysis_new_bp.route('/analyze/query', methods=['POST'])
def analyze_query():
    """
    分析自然語言查詢
    """
    try:
        data = request.get_json()
        query = data.get('query', '')
        context = data.get('context', {})
        
        if not query:
            return jsonify({'error': 'Query is required'}), 400
        
        # 使用代理協調器處理查詢
        result = orchestrator.process_query(query, context)
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error in analyze_query: {str(e)}")
        return jsonify({
            'error': 'Internal server error',
            'details': str(e)
        }), 500

@ai_analysis_new_bp.route('/agents/capabilities', methods=['GET'])
def get_agent_capabilities():
    """
    獲取AI代理能力
    """
    try:
        capabilities = orchestrator.get_agent_capabilities()
        return jsonify(capabilities)
        
    except Exception as e:
        logger.error(f"Error in get_agent_capabilities: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@ai_analysis_new_bp.route('/health', methods=['GET'])
def health_check():
    """
    AI分析服務健康檢查
    """
    try:
        status = orchestrator.health_check()
        return jsonify(status)
        
    except Exception as e:
        logger.error(f"Error in health_check: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@ai_analysis_new_bp.route('/analyze/scheduler', methods=['POST'])
def analyze_scheduler():
    """
    專門的排程風險分析
    """
    try:
        data = request.get_json()
        equipment_id = data.get('equipment_id')
        
        scheduler_agent = orchestrator.agents['scheduler']
        
        if equipment_id:
            result = scheduler_agent.analyze_equipment_schedule(equipment_id)
        else:
            result = scheduler_agent.analyze({})
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error in analyze_scheduler: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@ai_analysis_new_bp.route('/analyze/political', methods=['POST'])
def analyze_political():
    """
    專門的政治風險分析
    """
    try:
        data = request.get_json()
        country = data.get('country')
        
        political_agent = orchestrator.agents['political']
        
        if country:
            result = political_agent.analyze_country_risk(country)
        else:
            result = political_agent.analyze({})
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error in analyze_political: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@ai_analysis_new_bp.route('/analyze/logistics', methods=['POST'])
def analyze_logistics():
    """
    專門的物流風險分析
    """
    try:
        data = request.get_json()
        origin = data.get('origin_country')
        destination = data.get('destination_country')
        
        logistics_agent = orchestrator.agents['logistics']
        
        if origin and destination:
            result = logistics_agent.analyze_route_risk(origin, destination)
        else:
            result = logistics_agent.analyze({})
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error in analyze_logistics: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@ai_analysis_new_bp.route('/analyze/tariff', methods=['POST'])
def analyze_tariff():
    """
    專門的關稅風險分析
    """
    try:
        data = request.get_json()
        country1 = data.get('country1')
        country2 = data.get('country2')
        
        tariff_agent = orchestrator.agents['tariff']
        
        if country1 and country2:
            result = tariff_agent.analyze_trade_relationship(country1, country2)
        else:
            result = tariff_agent.analyze({})
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error in analyze_tariff: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

