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
