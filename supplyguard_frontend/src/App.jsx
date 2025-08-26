import React, { useState } from 'react';
import Navigation from './components/Navigation';
import Dashboard from './components/Dashboard';
import QueryInterface from './components/QueryInterface';
import EquipmentManagement from './components/EquipmentManagement';
import './App.css';

function App() {
  const [activeTab, setActiveTab] = useState('dashboard');

  const renderContent = () => {
    switch (activeTab) {
      case 'dashboard':
        return <Dashboard />;
      case 'query':
        return <QueryInterface />;
      case 'equipment':
        return <EquipmentManagement />;
      case 'schedules':
        return (
          <div className="p-8 text-center">
            <h2 className="text-2xl font-bold mb-4">Schedule Management</h2>
            <p className="text-muted-foreground">This feature is under development...</p>
          </div>
        );
      case 'risks':
        return (
          <div className="p-8 text-center">
            <h2 className="text-2xl font-bold mb-4">Risk Monitoring</h2>
            <p className="text-muted-foreground">This feature is under development...</p>
          </div>
        );
      default:
        return <Dashboard />;
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Navigation activeTab={activeTab} setActiveTab={setActiveTab} />
      <main className="container mx-auto px-4 py-6 max-w-7xl">
        {renderContent()}
      </main>
    </div>
  );
}

export default App;
