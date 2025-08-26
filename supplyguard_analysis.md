# SupplyGuard System Architecture and Functional Requirements Analysis

## Project Name
SupplyGuard: Procurement Risk Analysis System

## Overview
SupplyGuard is a proof-of-concept Agentic AI application designed to provide support for today's turbulent global environment, offering accelerators near real-time, explainable global supply chain market and risk intelligence. Rather than replacing human decision-makers, it serves as an intelligent assistant that continuously monitors geopolitical events, labor conditions, tariffs, and logistics disruptions to provide early warnings.

Accelerators can ask natural language questions and receive structured, visualized insights based on current data and verified sources. This is a multi-agent AI system that can transform how organizations manage equipment delivery risks in global supply chains.

By leveraging specialized AI agents, it provides comprehensive risk assessment through analyzing the following:
*   **Schedule Variations** - Identify delivery timeline risks
*   **Political Factors** - Real-time geopolitical risk insights through web search
*   **Tariff Changes** - Monitor trade policy impacts on procurement
*   **Logistics Disruptions** - Track transportation and traffic challenges

## Multi-Agent Process

This section outlines agent triggering and process coordination based on natural language queries in the equipment scheduling risk system.

### Agent Definitions
*   **ASSISTANT_AGENT**: Handles general queries, greetings, and fallback responses.
*   **SCHEDULER_AGENT**: Analyzes equipment scheduling data and calculates delivery risks.
*   **POLITICAL_RISK_AGENT**: Evaluates political risks based on manufacturing/project countries using web search.
*   **REPORTING_AGENT**: Synthesizes insights from other agents into a comprehensive report.

### Selection Strategy and Agent Flow
The system uses selection and termination strategies to determine which agent responds and when to end conversations.

#### 1. General Queries and Greetings
**Example**: `"Hello, can you help me?"`
**Flow**:
    User Query → ASSISTANT_AGENT → End Conversation

#### 2. Schedule Risk Queries
**Example**: `"What are the schedule risks?"`
**Flow**:
    User Query → SCHEDULER_AGENT → REPORTING_AGENT → End Conversation

#### 3. Political Risk Queries
**Example**: `"What are the political risks?"`
**Flow**:
    User Query → SCHEDULER_AGENT → POLITICAL_RISK_AGENT → REPORTING_AGENT → End Conversation

### Technical Implementation Details
*   **Thread Management**: System tracks conversation threads to maintain context
*   **Rate Limiting**: Rate-limited executor prevents external service overload
*   **Error Handling**: Includes retry logic and fallback mechanisms
*   **Thinking Process Logging**: Each agent uses logging to record reasoning steps
*   **Timeout Control**: Agents have individual and overall timeouts to prevent hanging

### Agent Message Processing
    User Message → AgentOrchestrator.process_message() → analyze_query_type() → process_specific_risk_query() or process_standard_query()

系統：
1.  使用關鍵字檢測分析查詢意圖
2.  根據查詢類型選擇適當的代理序列
3.  管理代理之間的對話流程
4.  處理錯誤條件和逾時
5.  將最終代理回應返回給用戶

這種代理架構實現了專業的風險分析，同時保持了連貫的對話流程，使每個代理都能專注於其專業領域。

## 後端技術 (不使用 Azure AI Agent Service, Azure OpenAI Service, Azure AI Foundry Playground)
*   **Python**: 用於 AI 邏輯和後端開發
*   **FastAPI**: 高效能 Python Web 框架，用於建構帶有自動文件說明的 API
*   **SQL Database**: 集中式、結構化資料庫，用於排程、設備元數據和風險分析結果 (例如 PostgreSQL, MySQL, SQLite)
*   **PyODBC**: Python 函式庫，用於連接 SQL Server 資料庫 (如果使用 SQL Server)
*   **Bing Search**: 用於即時網路搜尋，獲取地緣政治和物流風險洞察 (需要替代方案，因為Bing Search是Azure AI Agent Service的一部分)
*   **Web Interface**: Developer-oriented interface for real-time testing, monitoring, and debugging agent behavior

## Frontend Technologies
*   **React**: Frontend UI library for building interactive, component-based interfaces
*   **Vite**: Modern build tool for optimized frontend performance
*   **Tailwind CSS**: Utility-first CSS framework for rapid custom design without leaving HTML
*   **Chart Libraries**: JavaScript charting libraries for data visualization

## Development Tools
*   **Visual Studio Code**
*   **Postman**
*   **Git**

## Business Impact
SupplyGuard addresses critical business challenges through:
*   **Prevent Costly Delays** - Proactively identify equipment delivery risks before they impact projects
*   **Provide Early Warnings** - Timely alerts about emerging political, tariff, and logistics issues
*   **Streamline Collaboration** - Create shareable, structured documentation for procurement teams
*   **Support Data-Driven Decisions** - Make procurement choices through comprehensive risk analysis
*   **Reduce Supply Chain Disruptions** - Address potential issues before they affect project timelines

## Key Features
### Intelligent Multi-Agent Analysis
*   Specialized agent collaboration provides comprehensive risk assessment
*   Each agent focuses on specific risk domains (scheduling, political, tariff, logistics)
*   Comprehensive reports synthesize insights into actionable recommendations

### Interactive Risk Analysis
*   Conversational interface for natural risk queries and analysis
*   Real-time political risk intelligence through web search integration


## Alternative Solutions Consideration
Since users require not using Azure AI related technologies, here are alternative solutions to consider:

*   **AI Agent Service Alternatives**: Open-source agent frameworks such as LangChain or LlamaIndex can be used to implement multi-agent collaboration and process coordination.
*   **Large Language Model (LLM) Alternatives**: Open-source LLMs such as Hugging Face-based models, or calling other non-Azure LLM services through APIs.
*   **Search Service Alternatives**: Google Custom Search API or other web search APIs can be used to replace Bing Search.
*   **Database Alternatives**: Open-source relational databases such as PostgreSQL, MySQL, or SQLite can be used.
*   **Cloud Storage Alternatives**: Other cloud storage services such as AWS S3 or Google Cloud Storage, or directly using local file systems.

These alternatives will ensure that the system can still achieve SupplyGuard-like functionality without relying on Azure AI technologies.

