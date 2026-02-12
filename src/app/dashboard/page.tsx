import React from 'react';
import AgentsManager from '@/components/dashboard/AgentsManager';
import TasksManager from '@/components/dashboard/TasksManager';

export default function Dashboard() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-8">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">
            🦞 Simon's Command Center
          </h1>
          <p className="text-lg text-gray-600">
            Advanced AI-powered task and agent management system
          </p>
        </div>

        {/* Quick Stats */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="bg-white rounded-lg shadow-md p-6">
            <h3 className="text-lg font-semibold text-gray-800 mb-2">Active Tasks</h3>
            <p className="text-3xl font-bold text-blue-600">-</p>
          </div>
          
          <div className="bg-white rounded-lg shadow-md p-6">
            <h3 className="text-lg font-semibold text-gray-800 mb-2">AI Agents</h3>
            <p className="text-3xl font-bold text-green-600">3</p>
            <p className="text-sm text-gray-500">Svend, Anders, Content</p>
          </div>
          
          <div className="bg-white rounded-lg shadow-md p-6">
            <h3 className="text-lg font-semibold text-gray-800 mb-2">Projects</h3>
            <p className="text-3xl font-bold text-purple-600">5</p>
            <p className="text-sm text-gray-500">Elkjøp, Affiliate, etc.</p>
          </div>
          
          <div className="bg-white rounded-lg shadow-md p-6">
            <h3 className="text-lg font-semibold text-gray-800 mb-2">Sites Monitored</h3>
            <p className="text-3xl font-bold text-orange-600">5</p>
            <p className="text-sm text-gray-500">All systems online</p>
          </div>
        </div>

        {/* Management Sections */}
        <div className="space-y-8">
          <div className="bg-white rounded-lg shadow-lg overflow-hidden">
            <AgentsManager />
          </div>
          
          <div className="bg-white rounded-lg shadow-lg overflow-hidden">
            <TasksManager />
          </div>
        </div>
      </div>
    </div>
  );
}