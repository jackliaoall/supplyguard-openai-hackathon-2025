import React, { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Textarea } from '@/components/ui/textarea';
import { 
  Send, 
  Bot, 
  User, 
  AlertTriangle, 
  TrendingUp, 
  Globe, 
  Truck,
  DollarSign,
  RefreshCw,
  Lightbulb
} from 'lucide-react';

const QueryInterface = () => {
  const [query, setQuery] = useState('');
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const API_BASE = 'http://localhost:5001/api';

  const predefinedQueries = [
    {
      text: "Schedule Risk Analysis",
      query: "What are the schedule risks?",
      icon: TrendingUp,
      description: "Analyze equipment delivery schedule risks"
    },
    {
      text: "Political Risk Assessment",
      query: "What are the political risks?",
      icon: Globe,
      description: "Assess geopolitical impact on supply chain"
    },
    {
      text: "Logistics Risk Monitoring",
      query: "What are the logistics risks?",
      icon: Truck,
      description: "Monitor transportation and logistics disruption risks"
    },
    {
      text: "Tariff Risk Analysis",
      query: "What are the tariff risks?",
      icon: DollarSign,
      description: "Analyze trade policy and tariff changes"
    }
  ];

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!query.trim()) return;

    const userMessage = {
      id: Date.now(),
      type: 'user',
      content: query,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setLoading(true);
    setError(null);

    try {
      const response = await fetch(`${API_BASE}/analyze/query`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query }),
      });

      if (!response.ok) {
        throw new Error('Failed to analyze query');
      }

      const result = await response.json();

      const botMessage = {
        id: Date.now() + 1,
        type: 'bot',
        content: result,
        timestamp: new Date()
      };

      setMessages(prev => [...prev, botMessage]);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
      setQuery('');
    }
  };

  const handlePredefinedQuery = (predefinedQuery) => {
    setQuery(predefinedQuery);
  };

  const getRiskLevelColor = (level) => {
    switch (level) {
      case 'critical': return 'text-red-600 bg-red-50 border-red-200';
      case 'high': return 'text-orange-600 bg-orange-50 border-orange-200';
      case 'medium': return 'text-yellow-600 bg-yellow-50 border-yellow-200';
      case 'low': return 'text-green-600 bg-green-50 border-green-200';
      default: return 'text-gray-600 bg-gray-50 border-gray-200';
    }
  };

  const getAgentIcon = (agentName) => {
    switch (agentName) {
      case 'SCHEDULER_AGENT': return TrendingUp;
      case 'POLITICAL_RISK_AGENT': return Globe;
      case 'LOGISTICS_AGENT': return Truck;
      case 'TARIFF_AGENT': return DollarSign;
      default: return Bot;
    }
  };

  const renderAnalysisResult = (result) => {
    const AgentIcon = getAgentIcon(result.agent_name);
    
    return (
      <div className="space-y-4">
        {/* 代理資訊 */}
        <div className="flex items-center space-x-2">
          <AgentIcon className="h-5 w-5 text-blue-600" />
          <span className="font-medium text-blue-600">{result.agent_name}</span>
          <Badge variant="outline">{result.analysis_type}</Badge>
        </div>

        {/* 風險等級和分數 */}
        <div className={`p-4 rounded-lg border ${getRiskLevelColor(result.risk_level)}`}>
          <div className="flex items-center justify-between mb-2">
            <span className="font-medium">風險等級: {result.risk_level.toUpperCase()}</span>
            <span className="font-bold">分數: {result.risk_score.toFixed(1)}</span>
          </div>
          <p className="text-sm">{result.summary}</p>
        </div>

        {/* 詳細資訊 */}
        {result.details && (
          <Card>
            <CardHeader>
              <CardTitle className="text-lg">詳細分析</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid gap-2">
                {Object.entries(result.details).map(([key, value]) => (
                  <div key={key} className="flex justify-between">
                    <span className="text-muted-foreground">{key}:</span>
                    <span className="font-medium">
                      {Array.isArray(value) ? value.join(', ') : value}
                    </span>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        )}

        {/* 建議 */}
        {result.recommendations && result.recommendations.length > 0 && (
          <Card>
            <CardHeader>
              <CardTitle className="text-lg flex items-center">
                <Lightbulb className="h-5 w-5 mr-2 text-yellow-500" />
                建議措施
              </CardTitle>
            </CardHeader>
            <CardContent>
              <ul className="space-y-2">
                {result.recommendations.map((rec, index) => (
                  <li key={index} className="flex items-start">
                    <span className="text-blue-500 mr-2">•</span>
                    <span>{rec}</span>
                  </li>
                ))}
              </ul>
            </CardContent>
          </Card>
        )}

        {/* 受影響的設備 */}
        {result.affected_equipment && result.affected_equipment.length > 0 && (
          <Card>
            <CardHeader>
              <CardTitle className="text-lg">受影響的設備</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-2">
                {result.affected_equipment.map((equipment) => (
                  <div key={equipment.id} className="p-3 border rounded-lg">
                    <div className="font-medium">{equipment.name}</div>
                    <div className="text-sm text-muted-foreground">
                      {equipment.manufacturing_country} → {equipment.destination_country}
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        )}

        {/* 最近事件 */}
        {result.recent_events && result.recent_events.length > 0 && (
          <Card>
            <CardHeader>
              <CardTitle className="text-lg">相關事件</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {result.recent_events.map((event) => (
                  <div key={event.id} className="p-3 border rounded-lg">
                    <div className="font-medium mb-1">{event.title}</div>
                    <div className="text-sm text-muted-foreground mb-2">
                      {event.country} • {event.category} • {event.impact_level}
                    </div>
                    <div className="text-sm">{event.content.substring(0, 200)}...</div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        )}
      </div>
    );
  };

  return (
    <div className="space-y-6">
      {/* 標題 */}
      <div>
        <h1 className="text-3xl font-bold tracking-tight">AI 風險分析</h1>
        <p className="text-muted-foreground">
          使用自然語言查詢供應鏈風險，獲得智能分析和建議
        </p>
      </div>

      {/* 預定義查詢 */}
      <Card>
        <CardHeader>
          <CardTitle>快速查詢</CardTitle>
          <CardDescription>
            點擊下方按鈕快速開始風險分析
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid gap-3 md:grid-cols-2 lg:grid-cols-4">
            {predefinedQueries.map((item, index) => {
              const Icon = item.icon;
              return (
                <Button
                  key={index}
                  variant="outline"
                  className="h-auto p-4 flex flex-col items-start space-y-2"
                  onClick={() => handlePredefinedQuery(item.query)}
                >
                  <div className="flex items-center space-x-2">
                    <Icon className="h-4 w-4" />
                    <span className="font-medium">{item.text}</span>
                  </div>
                  <span className="text-xs text-muted-foreground text-left">
                    {item.description}
                  </span>
                </Button>
              );
            })}
          </div>
        </CardContent>
      </Card>

      {/* Query Input */}
      <Card>
        <CardHeader>
          <CardTitle>Natural Language Query</CardTitle>
          <CardDescription>
            Enter your question, AI agents will analyze supply chain risks for you
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="flex space-x-2">
              <Input
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="For example: Analyze political risks in Germany..."
                className="flex-1"
                disabled={loading}
              />
              <Button type="submit" disabled={loading || !query.trim()}>
                {loading ? (
                  <RefreshCw className="h-4 w-4 animate-spin" />
                ) : (
                  <Send className="h-4 w-4" />
                )}
              </Button>
            </div>
          </form>
        </CardContent>
      </Card>

      {/* Error Alert */}
      {error && (
        <Alert variant="destructive">
          <AlertTriangle className="h-4 w-4" />
          <AlertDescription>
            Error occurred during query analysis: {error}
          </AlertDescription>
        </Alert>
      )}

      {/* 對話歷史 */}
      {messages.length > 0 && (
        <div className="space-y-4">
          <h2 className="text-xl font-semibold">分析結果</h2>
          {messages.map((message) => (
            <Card key={message.id}>
              <CardHeader>
                <div className="flex items-center space-x-2">
                  {message.type === 'user' ? (
                    <User className="h-5 w-5 text-blue-600" />
                  ) : (
                    <Bot className="h-5 w-5 text-green-600" />
                  )}
                  <span className="font-medium">
                    {message.type === 'user' ? '您的查詢' : 'AI 分析結果'}
                  </span>
                  <span className="text-sm text-muted-foreground">
                    {message.timestamp.toLocaleTimeString()}
                  </span>
                </div>
              </CardHeader>
              <CardContent>
                {message.type === 'user' ? (
                  <p className="text-lg">{message.content}</p>
                ) : (
                  renderAnalysisResult(message.content)
                )}
              </CardContent>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
};

export default QueryInterface;

