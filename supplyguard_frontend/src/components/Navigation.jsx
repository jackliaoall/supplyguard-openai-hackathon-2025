import React from 'react';
import { Button } from '@/components/ui/button';
import { 
  BarChart3, 
  MessageSquare, 
  Package, 
  Calendar, 
  Globe, 
  Settings,
  Menu,
  X
} from 'lucide-react';
import { useState } from 'react';

const Navigation = ({ activeTab, setActiveTab }) => {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  const navigationItems = [
    {
      id: 'dashboard',
      label: 'Dashboard',
      icon: BarChart3,
      description: 'Overview and Statistics'
    },
    {
      id: 'query',
      label: 'AI Analysis',
      icon: MessageSquare,
      description: 'Intelligent Risk Query'
    },
    {
      id: 'equipment',
      label: 'Equipment Management',
      icon: Package,
      description: 'Equipment Information Management'
    },
    {
      id: 'schedules',
      label: 'Schedule Management',
      icon: Calendar,
      description: 'Delivery Schedule Monitoring'
    },
    {
      id: 'risks',
      label: 'Risk Monitoring',
      icon: Globe,
      description: 'Global Risk Tracking'
    }
  ];

  const toggleMobileMenu = () => {
    setIsMobileMenuOpen(!isMobileMenuOpen);
  };

  return (
    <>
      {/* Desktop Navigation */}
      <nav className="hidden md:flex bg-white border-b border-gray-200 px-6 py-4">
        <div className="flex items-center space-x-8">
          {/* Logo */}
          <div className="flex items-center space-x-2">
            <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
              <BarChart3 className="h-5 w-5 text-white" />
            </div>
            <span className="text-xl font-bold text-gray-900">SupplyGuard</span>
          </div>

          {/* Navigation Items */}
          <div className="flex space-x-1">
            {navigationItems.map((item) => {
              const Icon = item.icon;
              const isActive = activeTab === item.id;
              
              return (
                <Button
                  key={item.id}
                  variant={isActive ? "default" : "ghost"}
                  onClick={() => setActiveTab(item.id)}
                  className={`flex items-center space-x-2 px-4 py-2 ${
                    isActive 
                      ? 'bg-blue-600 text-white hover:bg-blue-700' 
                      : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
                  }`}
                >
                  <Icon className="h-4 w-4" />
                  <span>{item.label}</span>
                </Button>
              );
            })}
          </div>
        </div>

        {/* 右側操作 */}
        <div className="ml-auto flex items-center space-x-4">
          <Button variant="ghost" size="sm">
            <Settings className="h-4 w-4" />
          </Button>
        </div>
      </nav>

      {/* Mobile Navigation */}
      <nav className="md:hidden bg-white border-b border-gray-200">
        <div className="px-4 py-3">
          <div className="flex items-center justify-between">
            {/* Logo */}
            <div className="flex items-center space-x-2">
              <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
                <BarChart3 className="h-5 w-5 text-white" />
              </div>
              <span className="text-xl font-bold text-gray-900">SupplyGuard</span>
            </div>

            {/* Hamburger Menu Button */}
            <Button
              variant="ghost"
              size="sm"
              onClick={toggleMobileMenu}
              className="p-2"
            >
              {isMobileMenuOpen ? (
                <X className="h-6 w-6" />
              ) : (
                <Menu className="h-6 w-6" />
              )}
            </Button>
          </div>

          {/* Mobile Menu */}
          {isMobileMenuOpen && (
            <div className="mt-4 space-y-2">
              {navigationItems.map((item) => {
                const Icon = item.icon;
                const isActive = activeTab === item.id;
                
                return (
                  <Button
                    key={item.id}
                    variant={isActive ? "default" : "ghost"}
                    onClick={() => {
                      setActiveTab(item.id);
                      setIsMobileMenuOpen(false);
                    }}
                    className={`w-full justify-start space-x-3 px-4 py-3 ${
                      isActive 
                        ? 'bg-blue-600 text-white hover:bg-blue-700' 
                        : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
                    }`}
                  >
                    <Icon className="h-5 w-5" />
                    <div className="text-left">
                      <div className="font-medium">{item.label}</div>
                      <div className="text-xs opacity-75">{item.description}</div>
                    </div>
                  </Button>
                );
              })}
            </div>
          )}
        </div>
      </nav>

      {/* 當前頁面標題 (移動版) */}
      <div className="md:hidden bg-gray-50 px-4 py-2 border-b border-gray-200">
        <div className="flex items-center space-x-2">
          {(() => {
            const currentItem = navigationItems.find(item => item.id === activeTab);
            if (currentItem) {
              const Icon = currentItem.icon;
              return (
                <>
                  <Icon className="h-5 w-5 text-blue-600" />
                  <div>
                    <div className="font-medium text-gray-900">{currentItem.label}</div>
                    <div className="text-sm text-gray-500">{currentItem.description}</div>
                  </div>
                </>
              );
            }
            return null;
          })()}
        </div>
      </div>
    </>
  );
};

export default Navigation;

