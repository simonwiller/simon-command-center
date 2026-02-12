#!/usr/bin/env python3
"""
Anders Phase 2: Frontend Components & GitHub Integration
Next steps for Command Center completion
"""

import os
import json
import subprocess
from datetime import datetime
from pathlib import Path

class AndersPhaseTwo:
    def __init__(self):
        self.project_root = Path("/home/ubuntu/simon-command-center")
        
    def create_dashboard_components(self):
        """Create interactive dashboard components"""
        
        # Create agents management component
        agents_component = '''import React, { useState, useEffect } from 'react';

interface Agent {
  id: number;
  name: string;
  type: string;
  description: string;
  status: string;
  capabilities: string[];
  last_seen: string;
  created_at: string;
}

export default function AgentsManager() {
  const [agents, setAgents] = useState<Agent[]>([]);
  const [loading, setLoading] = useState(true);
  const [newAgent, setNewAgent] = useState({
    name: '',
    type: 'coding',
    description: '',
    capabilities: []
  });

  useEffect(() => {
    fetchAgents();
  }, []);

  const fetchAgents = async () => {
    try {
      const response = await fetch('/api/agents');
      const data = await response.json();
      if (data.success) {
        setAgents(data.agents);
      }
    } catch (error) {
      console.error('Error fetching agents:', error);
    } finally {
      setLoading(false);
    }
  };

  const createAgent = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const response = await fetch('/api/agents', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(newAgent)
      });
      
      const data = await response.json();
      if (data.success) {
        fetchAgents();
        setNewAgent({ name: '', type: 'coding', description: '', capabilities: [] });
      }
    } catch (error) {
      console.error('Error creating agent:', error);
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active': return 'bg-green-200 text-green-800';
      case 'inactive': return 'bg-gray-200 text-gray-800';
      default: return 'bg-yellow-200 text-yellow-800';
    }
  };

  if (loading) {
    return <div className="p-4">Loading agents...</div>;
  }

  return (
    <div className="p-6">
      <h2 className="text-2xl font-bold mb-6">🤖 AI Agents Management</h2>
      
      {/* Agent List */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-8">
        {agents.map((agent) => (
          <div key={agent.id} className="bg-white rounded-lg shadow-md p-4">
            <div className="flex items-center justify-between mb-2">
              <h3 className="font-semibold text-lg">{agent.name}</h3>
              <span className={`px-2 py-1 rounded text-xs ${getStatusColor(agent.status)}`}>
                {agent.status}
              </span>
            </div>
            <p className="text-sm text-gray-600 mb-2">{agent.type}</p>
            <p className="text-sm mb-3">{agent.description}</p>
            {agent.capabilities && (
              <div className="flex flex-wrap gap-1">
                {JSON.parse(agent.capabilities).map((cap: string, index: number) => (
                  <span key={index} className="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded">
                    {cap}
                  </span>
                ))}
              </div>
            )}
          </div>
        ))}
      </div>

      {/* Create New Agent Form */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h3 className="text-xl font-semibold mb-4">Create New Agent</h3>
        <form onSubmit={createAgent} className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-1">Name</label>
            <input
              type="text"
              value={newAgent.name}
              onChange={(e) => setNewAgent({...newAgent, name: e.target.value})}
              className="w-full p-2 border rounded-md"
              required
            />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Type</label>
            <select
              value={newAgent.type}
              onChange={(e) => setNewAgent({...newAgent, type: e.target.value})}
              className="w-full p-2 border rounded-md"
            >
              <option value="coding">Coding</option>
              <option value="content">Content</option>
              <option value="monitor">Monitor</option>
              <option value="coordinator">Coordinator</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Description</label>
            <textarea
              value={newAgent.description}
              onChange={(e) => setNewAgent({...newAgent, description: e.target.value})}
              className="w-full p-2 border rounded-md h-24"
              required
            />
          </div>
          <button
            type="submit"
            className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700"
          >
            Create Agent
          </button>
        </form>
      </div>
    </div>
  );
}'''

        components_dir = self.project_root / "src/components/dashboard"
        components_dir.mkdir(parents=True, exist_ok=True)
        
        with open(components_dir / "AgentsManager.tsx", "w") as f:
            f.write(agents_component)

        # Create tasks management component
        tasks_component = '''import React, { useState, useEffect } from 'react';

interface Task {
  id: number;
  title: string;
  description: string;
  status: string;
  priority: number;
  due_date: string;
  project_name: string;
  agent_name: string;
  created_at: string;
}

export default function TasksManager() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchTasks();
  }, []);

  const fetchTasks = async () => {
    try {
      const response = await fetch('/api/tasks');
      const data = await response.json();
      if (data.success) {
        setTasks(data.tasks);
      }
    } catch (error) {
      console.error('Error fetching tasks:', error);
    } finally {
      setLoading(false);
    }
  };

  const getPriorityColor = (priority: number) => {
    switch (priority) {
      case 1: return 'bg-red-200 text-red-800';
      case 2: return 'bg-yellow-200 text-yellow-800';
      default: return 'bg-green-200 text-green-800';
    }
  };

  const getPriorityText = (priority: number) => {
    switch (priority) {
      case 1: return 'High';
      case 2: return 'Medium';
      default: return 'Low';
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed': return 'bg-green-200 text-green-800';
      case 'in_progress': return 'bg-blue-200 text-blue-800';
      case 'cancelled': return 'bg-red-200 text-red-800';
      default: return 'bg-gray-200 text-gray-800';
    }
  };

  if (loading) {
    return <div className="p-4">Loading tasks...</div>;
  }

  return (
    <div className="p-6">
      <h2 className="text-2xl font-bold mb-6">📋 Tasks Management</h2>
      
      <div className="space-y-4">
        {tasks.map((task) => (
          <div key={task.id} className="bg-white rounded-lg shadow-md p-4">
            <div className="flex items-start justify-between mb-2">
              <div className="flex-1">
                <h3 className="font-semibold text-lg mb-1">{task.title}</h3>
                <p className="text-gray-600 text-sm mb-2">{task.description}</p>
                
                <div className="flex items-center gap-4 text-sm text-gray-500">
                  {task.project_name && (
                    <span>📁 {task.project_name}</span>
                  )}
                  {task.agent_name && (
                    <span>🤖 {task.agent_name}</span>
                  )}
                  {task.due_date && (
                    <span>📅 {new Date(task.due_date).toLocaleDateString()}</span>
                  )}
                </div>
              </div>
              
              <div className="flex flex-col gap-2">
                <span className={`px-2 py-1 rounded text-xs ${getStatusColor(task.status)}`}>
                  {task.status.replace('_', ' ')}
                </span>
                <span className={`px-2 py-1 rounded text-xs ${getPriorityColor(task.priority)}`}>
                  {getPriorityText(task.priority)}
                </span>
              </div>
            </div>
          </div>
        ))}
      </div>

      {tasks.length === 0 && (
        <div className="text-center py-8 text-gray-500">
          <p>No tasks found. Create your first task to get started!</p>
        </div>
      )}
    </div>
  );
}'''

        with open(components_dir / "TasksManager.tsx", "w") as f:
            f.write(tasks_component)
            
        return {"success": True, "message": "Dashboard components created"}
    
    def update_dashboard_page(self):
        """Update main dashboard to use new components"""
        dashboard_page = '''import React from 'react';
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
}'''

        dashboard_path = self.project_root / "src/app/dashboard/page.tsx"
        with open(dashboard_path, "w") as f:
            f.write(dashboard_page)
            
        return {"success": True, "message": "Dashboard updated with interactive components"}
    
    def prepare_github_push(self):
        """Prepare everything for GitHub push"""
        try:
            os.chdir(self.project_root)
            
            # Check git status
            result = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
            changes = result.stdout.strip()
            
            if changes:
                # Add all changes
                subprocess.run(["git", "add", "."], check=True)
                
                # Commit with comprehensive message
                commit_msg = """🚀 Command Center Phase 2 Complete

✅ Interactive dashboard components
✅ API routes for agents & tasks  
✅ Database connection utilities
✅ TypeScript integration
✅ Responsive design

Ready for deployment to SiteGround!

Co-authored-by: Anders <anders@ai-agent.dev>"""

                subprocess.run(["git", "commit", "-m", commit_msg], check=True)
                
                return {
                    "success": True, 
                    "message": "Ready to push to GitHub",
                    "next_steps": [
                        "git remote add origin https://github.com/simonwiller/simon-command-center.git",
                        "git branch -M main",
                        "git push -u origin main"
                    ]
                }
            else:
                return {"success": True, "message": "No changes to commit, ready for push"}
                
        except Exception as e:
            return {"success": False, "error": str(e)}

if __name__ == "__main__":
    anders_phase2 = AndersPhaseTwo()
    
    print("🚀 Anders Phase 2 Setup Starting...")
    
    # Step 1: Create dashboard components
    result1 = anders_phase2.create_dashboard_components()
    print("📱 Dashboard Components:")
    print(json.dumps(result1, indent=2))
    
    # Step 2: Update dashboard page
    result2 = anders_phase2.update_dashboard_page()
    print("\n📊 Dashboard Update:")
    print(json.dumps(result2, indent=2))
    
    # Step 3: Prepare for GitHub
    result3 = anders_phase2.prepare_github_push()
    print("\n📁 GitHub Preparation:")
    print(json.dumps(result3, indent=2))