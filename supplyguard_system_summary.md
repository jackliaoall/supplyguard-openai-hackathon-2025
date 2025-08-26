# SupplyGuard Supply Chain Risk Analysis System

## System Overview

SupplyGuard is a supply chain risk analysis system similar to Microsoft's supply chain solutions, using Python backend and React frontend, independent of Azure AI technologies, capable of analyzing global supply chain data and identifying potential risks.

## System Architecture

### Backend Architecture (Python Flask)
- **Framework**: Flask + SQLAlchemy
- **Database**: SQLite
- **API Design**: RESTful API
- **Port**: 5001

### Frontend Architecture (React)
- **Framework**: React + Vite
- **UI Library**: Custom Components
- **State Management**: React Hooks
- **Port**: 5173

### AI Agent System
- **Agent Orchestrator**: AgentOrchestrator
- **Four Specialized Agents**:
  1. **Scheduler Agent** (SchedulerAgent) - Analyze equipment delivery schedule risks
  2. **Political Risk Agent** (PoliticalRiskAgent) - Assess geopolitical risks
  3. **Logistics Agent** (LogisticsAgent) - Monitor transportation and logistics disruption risks
  4. **Tariff Agent** (TariffAgent) - Analyze trade policy and tariff changes

## Core Features

### 1. Dashboard
- Supply chain risk overview
- Real-time statistics
- Risk type and level distribution
- Latest risk assessments
- Equipment overview

### 2. AI Risk Analysis
- **Natural Language Queries**: Support for English and Chinese queries
- **Intelligent Routing**: Automatically identify query intent and route to appropriate agents
- **Multi-dimensional Analysis**: Four dimensions - scheduling, political, logistics, tariff
- **Real-time Analysis**: Risk assessment based on latest data

### 3. Equipment Management
- Equipment list management
- Equipment detail viewing
- Risk status monitoring

### 4. Schedule Management
- Delivery timeline management
- Delay risk monitoring
- Deadline reminders

### 5. Risk Monitoring
- Multi-level risk assessment
- Real-time risk alerts
- Historical risk trends

## Data Model

### Core Entities
1. **Equipment** - Equipment information
2. **Schedule** - Schedule information
3. **RiskAssessment** - Risk assessment
4. **NewsEvent** - News events

### Relationship Design
- Equipment and Schedule: One-to-many
- Equipment and Risk Assessment: One-to-many
- Country and News Events: One-to-many

## AI Agent Detailed Functions

### Scheduler Agent (SchedulerAgent)
- **Function**: Analyze equipment delivery schedule risks
- **Keywords**: schedule, delivery, timeline, delay
- **Analysis Content**:
  - Delayed project statistics
  - High-risk schedule identification
  - Upcoming deadline reminders
  - Risk score calculation

### Political Risk Agent (PoliticalRiskAgent)
- **Function**: Assess geopolitical risk impact on supply chain
- **Keywords**: political, government, policy
- **Analysis Content**:
  - Political event impact assessment
  - Country risk score calculation
  - Supply chain exposure analysis
  - Affected equipment identification

### Logistics Agent (LogisticsAgent)
- **Function**: Monitor transportation and logistics disruption risks
- **Keywords**: logistics, transport, shipping
- **Analysis Content**:
  - Logistics route risk assessment
  - Port risk monitoring
  - Transportation disruption analysis
  - Alternative route recommendations

### Tariff Agent (TariffAgent)
- **Function**: Analyze trade policy and tariff changes
- **Keywords**: tariff, trade, customs
- **Analysis Content**:
  - Trade war risk assessment
  - Tariff change impact analysis
  - Cost impact calculation
  - Trade route risks

## API Endpoints

### Basic API (v1)
- `GET /api/equipment` - Get equipment list
- `GET /api/schedules` - Get schedule list
- `GET /api/risk-assessments` - Get risk assessments
- `GET /api/dashboard/stats` - Get dashboard statistics

### AI Analysis API (v2)
- `POST /api/v2/analyze/query` - Natural language query analysis
- `GET /api/v2/agents/capabilities` - Get agent capabilities
- `GET /api/v2/health` - 健康檢查
- `POST /api/v2/analyze/scheduler` - 專門排程分析
- `POST /api/v2/analyze/political` - 專門政治風險分析
- `POST /api/v2/analyze/logistics` - 專門物流分析
- `POST /api/v2/analyze/tariff` - 專門關稅分析

## 技術特色

### 1. Intelligent Query Routing
- Intent recognition based on keywords and pattern matching
- Automatic routing to the most suitable AI agent
- Support for entity extraction (country, equipment type, time)

### 2. Multi-Agent Collaboration
- Unified management by agent orchestrator
- Each agent specializes in specific domains
- Support for comprehensive analysis and single agent analysis

### 3. Risk Score Calculation
- Multi-factor risk assessment model
- Dynamic weight adjustment
- Four-level risk grades (low, medium, high, critical)

### 4. Real-time Data Processing
- Analysis based on latest news events
- Dynamic risk score updates
- Real-time recommendation generation

## Deployment Information

### Development Environment
- Backend: http://localhost:5001
- Frontend: http://localhost:5173
- Database: SQLite (local file)

### System Requirements
- Python 3.11+
- Node.js 20+
- Flask, SQLAlchemy, Flask-CORS
- React, Vite

## Test Results

### Functional Testing
✅ Dashboard data display normal
✅ AI analysis query function normal
✅ Natural language processing correct routing
✅ Four AI agents running normally
✅ API health check passed
✅ Frontend-backend integration successful

### Performance Testing
✅ API response time < 2 seconds
✅ Frontend page loading smooth
✅ Database query efficiency good
✅ AI agent analysis speed moderate

## 示例查詢

### 支援的查詢類型
1. **排程風險**: "What are the schedule risks?", "分析設備交付排程的風險"
2. **政治風險**: "分析德國的政治風險", "評估地緣政治影響"
3. **物流風險**: "分析中國到台灣的物流風險", "檢查港口擁堵情況"
4. **關稅風險**: "分析貿易關稅風險", "評估貿易戰影響"

### 查詢結果示例
```json
{
  "agent_name": "LOGISTICS_AGENT",
  "analysis_type": "logistics",
  "risk_level": "medium",
  "risk_score": 55.0,
  "summary": "分析了 1 個物流事件，許估運輸和配送風險。",
  "recommendations": [
    "監控主要港口狀況",
    "準備替代運輸路線",
    "與物流供應商保持溝通"
  ]
}
```

## 未來擴展

### 短期改進
- 增加更多數據源
- 優化 AI 分析算法
- 添加用戶認證系統
- 實現數據可視化圖表

### 長期規劃
- 機器學習模型訓練
- 預測性風險分析
- 多語言支援
- 移動端應用
- 雲端部署

## Summary

SupplyGuard system successfully implements core functionality similar to Microsoft's supply chain solutions, providing:

1. **Complete Supply Chain Risk Analysis Platform**
2. **Intelligent AI Agent System**
3. **Intuitive User Interface**
4. **Flexible API Architecture**
5. **Scalable Technical Architecture**

The system can effectively identify and analyze various risks in the supply chain, providing valuable insights and recommendations for business decision-making.

