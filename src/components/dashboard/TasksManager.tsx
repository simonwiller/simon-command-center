"use client";
import React, { useState, useEffect } from 'react';

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
}
