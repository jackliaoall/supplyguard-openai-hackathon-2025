"""
數據種子檔案 - 用於填充測試數據
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from datetime import datetime, timedelta
import random
from src.models.user import db
from src.models.supply_chain import Equipment, Schedule, RiskAssessment, NewsEvent
from flask import Flask

def create_app():
    """建立Flask應用程式實例"""
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    return app

def seed_equipment():
    """填充設備數據"""
    equipment_data = [
        {
            'name': '工業機器人 ARM-2000',
            'category': '自動化設備',
            'manufacturer': 'RoboTech Industries',
            'manufacturing_country': '德國',
            'destination_country': '台灣'
        },
        {
            'name': 'CNC 精密加工中心',
            'category': '機械設備',
            'manufacturer': 'Precision Machinery Co.',
            'manufacturing_country': '日本',
            'destination_country': '台灣'
        },
        {
            'name': '半導體測試設備 ST-500',
            'category': '電子設備',
            'manufacturer': 'SemiTest Corp',
            'manufacturing_country': '韓國',
            'destination_country': '台灣'
        },
        {
            'name': '太陽能電池板生產線',
            'category': '能源設備',
            'manufacturer': 'Solar Manufacturing Ltd',
            'manufacturing_country': '中國',
            'destination_country': '台灣'
        },
        {
            'name': '醫療影像設備 MRI-X1',
            'category': '醫療設備',
            'manufacturer': 'MedTech Solutions',
            'manufacturing_country': '美國',
            'destination_country': '台灣'
        },
        {
            'name': '化工反應器 CR-1000',
            'category': '化工設備',
            'manufacturer': 'ChemReactor Inc',
            'manufacturing_country': '荷蘭',
            'destination_country': '台灣'
        },
        {
            'name': '電動車電池組裝線',
            'category': '汽車設備',
            'manufacturer': 'EV Battery Systems',
            'manufacturing_country': '中國',
            'destination_country': '台灣'
        },
        {
            'name': '5G 基站設備 BS-5000',
            'category': '通訊設備',
            'manufacturer': 'TelecomTech Ltd',
            'manufacturing_country': '芬蘭',
            'destination_country': '台灣'
        }
    ]
    
    for data in equipment_data:
        equipment = Equipment(**data)
        db.session.add(equipment)
    
    db.session.commit()
    print(f"已添加 {len(equipment_data)} 個設備")

def seed_schedules():
    """填充排程數據"""
    equipment_list = Equipment.query.all()
    
    for equipment in equipment_list:
        # 為每個設備創建1-3個排程
        num_schedules = random.randint(1, 3)
        
        for i in range(num_schedules):
            # 隨機生成排程日期
            start_date = datetime.now() + timedelta(days=random.randint(-30, 60))
            end_date = start_date + timedelta(days=random.randint(30, 120))
            
            # 隨機決定是否有實際日期（模擬進行中或已完成的項目）
            actual_start = None
            actual_end = None
            status = 'planned'
            delay_days = 0
            
            if random.random() < 0.6:  # 60% 機率有實際開始日期
                actual_start = start_date + timedelta(days=random.randint(-5, 10))
                status = 'in_progress'
                
                if random.random() < 0.3:  # 30% 機率已完成
                    actual_end = actual_start + timedelta(days=random.randint(25, 150))
                    status = 'completed'
                    
                    # 計算延遲天數
                    if actual_end > end_date:
                        delay_days = (actual_end - end_date).days
                        status = 'delayed' if delay_days > 0 else 'completed'
            
            # 根據延遲情況設定風險等級
            if delay_days > 30:
                risk_level = 'critical'
            elif delay_days > 15:
                risk_level = 'high'
            elif delay_days > 5:
                risk_level = 'medium'
            else:
                risk_level = 'low'
            
            schedule = Schedule(
                equipment_id=equipment.id,
                planned_start_date=start_date,
                planned_end_date=end_date,
                actual_start_date=actual_start,
                actual_end_date=actual_end,
                status=status,
                delay_days=delay_days,
                risk_level=risk_level
            )
            db.session.add(schedule)
    
    db.session.commit()
    print(f"已添加排程數據")

def seed_news_events():
    """填充新聞事件數據"""
    news_data = [
        {
            'title': '德國工業4.0政策更新，影響製造業出口',
            'content': '德國政府宣布新的工業4.0政策框架，將對製造業出口產生重大影響...',
            'source': 'Industrial News',
            'url': 'https://example.com/news1',
            'country': '德國',
            'category': 'political',
            'impact_level': 'medium',
            'published_date': datetime.now() - timedelta(days=2)
        },
        {
            'title': '日本地震影響精密機械生產',
            'content': '日本東部發生6.2級地震，多家精密機械製造商暫停生產...',
            'source': 'Earthquake Monitor',
            'url': 'https://example.com/news2',
            'country': '日本',
            'category': 'natural_disaster',
            'impact_level': 'high',
            'published_date': datetime.now() - timedelta(days=1)
        },
        {
            'title': '韓國半導體出口關稅調整',
            'content': '韓國政府調整半導體相關設備的出口關稅政策...',
            'source': 'Trade Weekly',
            'url': 'https://example.com/news3',
            'country': '韓國',
            'category': 'economic',
            'impact_level': 'medium',
            'published_date': datetime.now() - timedelta(days=3)
        },
        {
            'title': '中國港口罷工影響貨物運輸',
            'content': '上海港工人罷工，導致大量貨物積壓，影響全球供應鏈...',
            'source': 'Shipping Times',
            'url': 'https://example.com/news4',
            'country': '中國',
            'category': 'logistics',
            'impact_level': 'high',
            'published_date': datetime.now() - timedelta(days=1)
        },
        {
            'title': '美國FDA加強醫療設備審查',
            'content': 'FDA宣布加強對進口醫療設備的審查程序，可能延長審批時間...',
            'source': 'Medical Device News',
            'url': 'https://example.com/news5',
            'country': '美國',
            'category': 'political',
            'impact_level': 'medium',
            'published_date': datetime.now() - timedelta(days=4)
        },
        {
            'title': '荷蘭化工廠爆炸事故',
            'content': '阿姆斯特丹附近化工廠發生爆炸，影響化工設備生產...',
            'source': 'Safety News',
            'url': 'https://example.com/news6',
            'country': '荷蘭',
            'category': 'natural_disaster',
            'impact_level': 'high',
            'published_date': datetime.now() - timedelta(days=2)
        },
        {
            'title': '芬蘭5G技術出口新規定',
            'content': '芬蘭政府發布5G設備出口的新安全規定...',
            'source': 'Tech Policy',
            'url': 'https://example.com/news7',
            'country': '芬蘭',
            'category': 'political',
            'impact_level': 'low',
            'published_date': datetime.now() - timedelta(days=5)
        }
    ]
    
    for data in news_data:
        event = NewsEvent(**data)
        db.session.add(event)
    
    db.session.commit()
    print(f"已添加 {len(news_data)} 個新聞事件")

def seed_risk_assessments():
    """填充風險評估數據"""
    equipment_list = Equipment.query.all()
    risk_types = ['schedule', 'political', 'tariff', 'logistics']
    risk_levels = ['low', 'medium', 'high', 'critical']
    agent_names = ['SCHEDULER_AGENT', 'POLITICAL_RISK_AGENT', 'TARIFF_AGENT', 'LOGISTICS_AGENT']
    
    for equipment in equipment_list:
        # 為每個設備創建2-4個風險評估
        num_assessments = random.randint(2, 4)
        
        for i in range(num_assessments):
            risk_type = random.choice(risk_types)
            risk_level = random.choice(risk_levels)
            
            # 根據風險等級設定分數範圍
            if risk_level == 'low':
                risk_score = random.uniform(0, 30)
            elif risk_level == 'medium':
                risk_score = random.uniform(30, 60)
            elif risk_level == 'high':
                risk_score = random.uniform(60, 85)
            else:  # critical
                risk_score = random.uniform(85, 100)
            
            # 生成描述和建議
            descriptions = {
                'schedule': f'{equipment.name} 的交付排程存在延遲風險，主要原因包括供應商產能限制和物流安排。',
                'political': f'由於 {equipment.manufacturing_country} 的政治局勢變化，可能影響 {equipment.name} 的正常生產和出口。',
                'tariff': f'{equipment.manufacturing_country} 與 {equipment.destination_country} 之間的貿易政策變化可能影響 {equipment.name} 的成本。',
                'logistics': f'{equipment.name} 的運輸路線存在潛在風險，包括港口擁堵和運輸延誤。'
            }
            
            recommendations = {
                'schedule': '建議與供應商重新協商交付時間，並準備備用供應商方案。',
                'political': '密切監控政治局勢發展，考慮供應鏈多元化策略。',
                'tariff': '評估關稅變化對成本的影響，考慮調整採購策略。',
                'logistics': '優化運輸路線，建立多元化的物流方案。'
            }
            
            assessment = RiskAssessment(
                equipment_id=equipment.id,
                risk_type=risk_type,
                risk_level=risk_level,
                risk_score=round(risk_score, 2),
                description=descriptions[risk_type],
                recommendations=recommendations[risk_type],
                sources='{"news_sources": ["example.com"], "data_sources": ["internal_analysis"]}',
                agent_name=agent_names[risk_types.index(risk_type)]
            )
            db.session.add(assessment)
    
    db.session.commit()
    print(f"已添加風險評估數據")

def main():
    """主函數 - 執行所有數據填充"""
    app = create_app()
    
    with app.app_context():
        # 清空現有數據（可選）
        print("清空現有數據...")
        db.drop_all()
        db.create_all()
        
        # 填充數據
        print("開始填充測試數據...")
        seed_equipment()
        seed_schedules()
        seed_news_events()
        seed_risk_assessments()
        
        print("數據填充完成！")

if __name__ == '__main__':
    main()

