import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { 
  Package, 
  Plus, 
  Search, 
  Filter, 
  MapPin, 
  Building, 
  Calendar,
  AlertTriangle,
  RefreshCw,
  Eye,
  Edit,
  Trash2
} from 'lucide-react';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '@/components/ui/dialog';
import { Label } from '@/components/ui/label';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';

const EquipmentManagement = () => {
  const [equipment, setEquipment] = useState([]);
  const [filteredEquipment, setFilteredEquipment] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterCategory, setFilterCategory] = useState('all');
  const [selectedEquipment, setSelectedEquipment] = useState(null);
  const [equipmentRisks, setEquipmentRisks] = useState(null);
  const [showAddDialog, setShowAddDialog] = useState(false);
  const [showDetailDialog, setShowDetailDialog] = useState(false);

  const API_BASE = 'http://localhost:5001/api';

  useEffect(() => {
    fetchEquipment();
  }, []);

  useEffect(() => {
    filterEquipment();
  }, [equipment, searchTerm, filterCategory]);

  const fetchEquipment = async () => {
    try {
      setLoading(true);
      const response = await fetch(`${API_BASE}/equipment`);
      if (!response.ok) {
        throw new Error('Failed to fetch equipment');
      }
      const data = await response.json();
      setEquipment(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const filterEquipment = () => {
    let filtered = equipment;

    if (searchTerm) {
      filtered = filtered.filter(item =>
        item.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        item.manufacturer.toLowerCase().includes(searchTerm.toLowerCase()) ||
        item.manufacturing_country.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }

    if (filterCategory !== 'all') {
      filtered = filtered.filter(item => item.category === filterCategory);
    }

    setFilteredEquipment(filtered);
  };

  const fetchEquipmentRisks = async (equipmentId) => {
    try {
      const response = await fetch(`${API_BASE}/equipment/${equipmentId}/risks`);
      if (!response.ok) {
        throw new Error('Failed to fetch equipment risks');
      }
      const data = await response.json();
      setEquipmentRisks(data);
    } catch (err) {
      console.error('Error fetching equipment risks:', err);
    }
  };

  const handleViewDetails = async (item) => {
    setSelectedEquipment(item);
    await fetchEquipmentRisks(item.id);
    setShowDetailDialog(true);
  };

  const getUniqueCategories = () => {
    const categories = [...new Set(equipment.map(item => item.category))];
    return categories;
  };

  const getRiskLevelColor = (level) => {
    switch (level) {
      case 'critical': return 'bg-red-500 text-white';
      case 'high': return 'bg-orange-500 text-white';
      case 'medium': return 'bg-yellow-500 text-black';
      case 'low': return 'bg-green-500 text-white';
      default: return 'bg-gray-500 text-white';
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
          載入設備數據時發生錯誤: {error}
        </AlertDescription>
      </Alert>
    );
  }

  return (
    <div className="space-y-6">
      {/* 標題和操作 */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">設備管理</h1>
          <p className="text-muted-foreground">
            管理供應鏈中的設備資訊和風險狀態
          </p>
        </div>
        <div className="flex space-x-2">
          <Button onClick={fetchEquipment} variant="outline">
            <RefreshCw className="h-4 w-4 mr-2" />
            重新整理
          </Button>
          <Button onClick={() => setShowAddDialog(true)}>
            <Plus className="h-4 w-4 mr-2" />
            新增設備
          </Button>
        </div>
      </div>

      {/* 搜尋和篩選 */}
      <Card>
        <CardHeader>
          <CardTitle>搜尋和篩選</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex space-x-4">
            <div className="flex-1">
              <div className="relative">
                <Search className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                <Input
                  placeholder="搜尋設備名稱、製造商或國家..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="pl-10"
                />
              </div>
            </div>
            <Select value={filterCategory} onValueChange={setFilterCategory}>
              <SelectTrigger className="w-48">
                <SelectValue placeholder="選擇類別" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">所有類別</SelectItem>
                {getUniqueCategories().map((category) => (
                  <SelectItem key={category} value={category}>
                    {category}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
        </CardContent>
      </Card>

      {/* 設備列表 */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {filteredEquipment.map((item) => (
          <Card key={item.id} className="hover:shadow-lg transition-shadow">
            <CardHeader>
              <div className="flex items-center justify-between">
                <Package className="h-6 w-6 text-blue-600" />
                <Badge variant="outline">{item.category}</Badge>
              </div>
              <CardTitle className="text-lg">{item.name}</CardTitle>
              <CardDescription>{item.manufacturer}</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                <div className="flex items-center space-x-2 text-sm">
                  <Building className="h-4 w-4 text-muted-foreground" />
                  <span>製造地: {item.manufacturing_country}</span>
                </div>
                <div className="flex items-center space-x-2 text-sm">
                  <MapPin className="h-4 w-4 text-muted-foreground" />
                  <span>目的地: {item.destination_country}</span>
                </div>
                <div className="flex items-center space-x-2 text-sm">
                  <Calendar className="h-4 w-4 text-muted-foreground" />
                  <span>建立時間: {new Date(item.created_at).toLocaleDateString()}</span>
                </div>
                
                <div className="flex space-x-2 pt-2">
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => handleViewDetails(item)}
                    className="flex-1"
                  >
                    <Eye className="h-4 w-4 mr-1" />
                    詳情
                  </Button>
                  <Button variant="outline" size="sm">
                    <Edit className="h-4 w-4" />
                  </Button>
                  <Button variant="outline" size="sm">
                    <Trash2 className="h-4 w-4" />
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {filteredEquipment.length === 0 && (
        <Card>
          <CardContent className="text-center py-8">
            <Package className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
            <p className="text-muted-foreground">沒有找到符合條件的設備</p>
          </CardContent>
        </Card>
      )}

      {/* 設備詳情對話框 */}
      <Dialog open={showDetailDialog} onOpenChange={setShowDetailDialog}>
        <DialogContent className="max-w-4xl max-h-[80vh] overflow-y-auto">
          <DialogHeader>
            <DialogTitle>設備詳情</DialogTitle>
            <DialogDescription>
              查看設備的詳細資訊和風險評估
            </DialogDescription>
          </DialogHeader>
          
          {selectedEquipment && (
            <div className="space-y-6">
              {/* 基本資訊 */}
              <Card>
                <CardHeader>
                  <CardTitle>基本資訊</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="grid gap-4 md:grid-cols-2">
                    <div>
                      <Label>設備名稱</Label>
                      <p className="font-medium">{selectedEquipment.name}</p>
                    </div>
                    <div>
                      <Label>類別</Label>
                      <p className="font-medium">{selectedEquipment.category}</p>
                    </div>
                    <div>
                      <Label>製造商</Label>
                      <p className="font-medium">{selectedEquipment.manufacturer}</p>
                    </div>
                    <div>
                      <Label>製造國家</Label>
                      <p className="font-medium">{selectedEquipment.manufacturing_country}</p>
                    </div>
                    <div>
                      <Label>目的地國家</Label>
                      <p className="font-medium">{selectedEquipment.destination_country}</p>
                    </div>
                    <div>
                      <Label>建立時間</Label>
                      <p className="font-medium">
                        {new Date(selectedEquipment.created_at).toLocaleString()}
                      </p>
                    </div>
                  </div>
                </CardContent>
              </Card>

              {/* 風險評估 */}
              {equipmentRisks && (
                <Card>
                  <CardHeader>
                    <CardTitle>風險評估</CardTitle>
                    <CardDescription>
                      該設備的風險分析結果
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    {equipmentRisks.risk_assessments.length > 0 ? (
                      <div className="space-y-4">
                        {equipmentRisks.risk_assessments.map((risk) => (
                          <div key={risk.id} className="p-4 border rounded-lg">
                            <div className="flex items-center justify-between mb-2">
                              <div className="flex items-center space-x-2">
                                <Badge variant={getRiskLevelBadgeVariant(risk.risk_level)}>
                                  {risk.risk_level}
                                </Badge>
                                <span className="font-medium">{risk.risk_type} 風險</span>
                              </div>
                              <span className="font-bold">{risk.risk_score.toFixed(1)}</span>
                            </div>
                            <p className="text-sm text-muted-foreground mb-2">
                              {risk.description}
                            </p>
                            {risk.recommendations && (
                              <div>
                                <Label className="text-xs">建議:</Label>
                                <p className="text-sm">{risk.recommendations}</p>
                              </div>
                            )}
                            <div className="text-xs text-muted-foreground mt-2">
                              分析代理: {risk.agent_name} • 
                              更新時間: {new Date(risk.updated_at).toLocaleString()}
                            </div>
                          </div>
                        ))}
                      </div>
                    ) : (
                      <p className="text-muted-foreground">暫無風險評估數據</p>
                    )}
                  </CardContent>
                </Card>
              )}
            </div>
          )}
        </DialogContent>
      </Dialog>

      {/* 新增設備對話框 */}
      <Dialog open={showAddDialog} onOpenChange={setShowAddDialog}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>新增設備</DialogTitle>
            <DialogDescription>
              添加新的設備到供應鏈管理系統
            </DialogDescription>
          </DialogHeader>
          <div className="space-y-4">
            <div>
              <Label htmlFor="name">設備名稱</Label>
              <Input id="name" placeholder="輸入設備名稱" />
            </div>
            <div>
              <Label htmlFor="category">類別</Label>
              <Input id="category" placeholder="輸入設備類別" />
            </div>
            <div>
              <Label htmlFor="manufacturer">製造商</Label>
              <Input id="manufacturer" placeholder="輸入製造商名稱" />
            </div>
            <div>
              <Label htmlFor="manufacturing_country">製造國家</Label>
              <Input id="manufacturing_country" placeholder="輸入製造國家" />
            </div>
            <div>
              <Label htmlFor="destination_country">目的地國家</Label>
              <Input id="destination_country" placeholder="輸入目的地國家" />
            </div>
            <div className="flex space-x-2 pt-4">
              <Button className="flex-1">新增設備</Button>
              <Button variant="outline" onClick={() => setShowAddDialog(false)}>
                取消
              </Button>
            </div>
          </div>
        </DialogContent>
      </Dialog>
    </div>
  );
};

export default EquipmentManagement;

