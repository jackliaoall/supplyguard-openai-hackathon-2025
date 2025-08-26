import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { 
  AlertTriangle, 
  TrendingUp, 
  Package, 
  Calendar, 
  Globe, 
  BarChart3,
  RefreshCw,
  Search
} from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';

const Dashboard = () => {
  const [stats, setStats] = useState(null);
  const [equipment, setEquipment] = useState([]);
  const [riskAssessments, setRiskAssessments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const API_BASE = 'http://localhost:5001/api';

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      const [statsRes, equipmentRes, riskRes] = await Promise.all([
        fetch(`${API_BASE}/dashboard/stats`),
        fetch(`${API_BASE}/equipment`),
        fetch(`${API_BASE}/risk-assessments`)
      ]);

      if (!statsRes.ok || !equipmentRes.ok || !riskRes.ok) {
        throw new Error('Failed to fetch data');
      }

      const [statsData, equipmentData, riskData] = await Promise.all([
        statsRes.json(),
        equipmentRes.json(),
        riskRes.json()
      ]);

      setStats(statsData);
      setEquipment(equipmentData);
      setRiskAssessments(riskData);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const getRiskLevelColor = (level) => {
    switch (level) {
      case 'critical': return 'bg-red-500';
      case 'high': return 'bg-orange-500';
      case 'medium': return 'bg-yellow-500';
      case 'low': return 'bg-green-500';
      default: return 'bg-gray-500';
    }
  };

  const getRiskLevelBadgeVariant = (level) => {
    switch (level) {
      case 'critical': return 'destructive';
      case 'high': return 'destructive';
      case 'medium': return 'secondary';
      case 'low': return 'default';
      default: return 'outline';
    }
  };

  // 準備圖表數據
  const riskByType = riskAssessments.reduce((acc, risk) => {
    acc[risk.risk_type] = (acc[risk.risk_type] || 0) + 1;
    return acc;
  }, {});

  const chartData = Object.entries(riskByType).map(([type, count]) => ({
    name: type,
    count
  }));

  const riskLevelData = riskAssessments.reduce((acc, risk) => {
    acc[risk.risk_level] = (acc[risk.risk_level] || 0) + 1;
    return acc;
  }, {});

  const pieData = Object.entries(riskLevelData).map(([level, count]) => ({
    name: level,
    value: count,
    color: getRiskLevelColor(level).replace('bg-', '#')
  }));

  const COLORS = ['#ef4444', '#f97316', '#eab308', '#22c55e', '#6b7280'];

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <RefreshCw className="h-8 w-8 animate-spin" />
        <span className="ml-2">載入中...</span>
      </div>
    );
  }

  if (error) {
    return (
      <Alert variant="destructive">
        <AlertTriangle className="h-4 w-4" />
        <AlertDescription>
          載入數據時發生錯誤: {error}
        </AlertDescription>
      </Alert>
    );
  }

  return (
    <div className="space-y-6">
      {/* 標題區域 */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">供應鏈風險儀表板</h1>
          <p className="text-muted-foreground">
            監控全球供應鏈風險，提供即時洞察和預警
          </p>
        </div>
        <Button onClick={fetchDashboardData} variant="outline">
          <RefreshCw className="h-4 w-4 mr-2" />
          重新整理
        </Button>
      </div>

      {/* 統計卡片 */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-5">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">總設備數</CardTitle>
            <Package className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats?.total_equipment || 0}</div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">總排程數</CardTitle>
            <Calendar className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats?.total_schedules || 0}</div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">高風險項目</CardTitle>
            <AlertTriangle className="h-4 w-4 text-orange-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-orange-600">
              {stats?.high_risk_assessments || 0}
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">關鍵風險項目</CardTitle>
            <AlertTriangle className="h-4 w-4 text-red-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-red-600">
              {stats?.critical_risk_assessments || 0}
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">延遲排程</CardTitle>
            <TrendingUp className="h-4 w-4 text-red-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-red-600">
              {stats?.delayed_schedules || 0}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* 圖表區域 */}
      <div className="grid gap-4 md:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>風險類型分布</CardTitle>
            <CardDescription>
              按風險類型統計的風險評估數量
            </CardDescription>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="count" fill="#3b82f6" />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>風險等級分布</CardTitle>
            <CardDescription>
              按風險等級統計的風險評估數量
            </CardDescription>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={pieData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {pieData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </div>

      {/* 最新風險評估 */}
      <Card>
        <CardHeader>
          <CardTitle>最新風險評估</CardTitle>
          <CardDescription>
            最近的風險評估結果
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {riskAssessments.slice(0, 5).map((risk) => (
              <div key={risk.id} className="flex items-center justify-between p-4 border rounded-lg">
                <div className="flex items-center space-x-4">
                  <Badge variant={getRiskLevelBadgeVariant(risk.risk_level)}>
                    {risk.risk_level}
                  </Badge>
                  <div>
                    <p className="font-medium">{risk.risk_type} 風險</p>
                    <p className="text-sm text-muted-foreground">
                      {risk.description.substring(0, 100)}...
                    </p>
                  </div>
                </div>
                <div className="text-right">
                  <p className="font-bold">{risk.risk_score.toFixed(1)}</p>
                  <p className="text-sm text-muted-foreground">風險分數</p>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* 設備概覽 */}
      <Card>
        <CardHeader>
          <CardTitle>設備概覽</CardTitle>
          <CardDescription>
            供應鏈中的關鍵設備
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
            {equipment.slice(0, 6).map((item) => (
              <div key={item.id} className="p-4 border rounded-lg">
                <div className="flex items-center justify-between mb-2">
                  <h3 className="font-medium">{item.name}</h3>
                  <Globe className="h-4 w-4 text-muted-foreground" />
                </div>
                <p className="text-sm text-muted-foreground mb-1">
                  類別: {item.category}
                </p>
                <p className="text-sm text-muted-foreground mb-1">
                  製造商: {item.manufacturer}
                </p>
                <div className="flex justify-between text-xs text-muted-foreground">
                  <span>來源: {item.manufacturing_country}</span>
                  <span>目的地: {item.destination_country}</span>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default Dashboard;

