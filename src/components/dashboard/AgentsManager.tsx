"use client";
import React, { useState, useEffect } from 'react';

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
}
