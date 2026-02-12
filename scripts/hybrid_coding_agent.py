#!/usr/bin/env python3
"""
Hybrid Coding Agent - Anders
Combines OpenAI API calls with local development tools
"""

import os
import sys
import json
import subprocess
from datetime import datetime
from pathlib import Path

class HybridAndersAgent:
    def __init__(self):
        self.name = "Anders"
        self.version = "2.0-Hybrid"
        self.project_root = Path("/home/ubuntu/simon-command-center")
        self.openai_key = os.getenv('OPENAI_API_KEY')
        
    def status_report(self):
        """Generate comprehensive status report"""
        status = {
            "agent": self.name,
            "version": self.version,
            "timestamp": datetime.now().isoformat(),
            "project_root": str(self.project_root),
            "capabilities": {
                "local_development": True,
                "openai_api": bool(self.openai_key),
                "codex_cli_local": "Available on Simon's machine",
                "git_integration": True,
                "database_operations": True,
                "deployment_automation": True
            },
            "current_setup": self.analyze_project_state()
        }
        return status
    
    def analyze_project_state(self):
        """Analyze current project state"""
        state = {
            "next_js": self.check_file_exists("package.json"),
            "database_schema": self.check_file_exists("database/schema.sql"),
            "api_routes": self.check_directory_exists("src/app/api"),
            "github_actions": self.check_file_exists(".github/workflows/deploy.yml"),
            "environment_config": self.check_file_exists(".env.example"),
            "git_initialized": self.check_directory_exists(".git")
        }
        return state
    
    def check_file_exists(self, relative_path):
        """Check if file exists relative to project root"""
        return (self.project_root / relative_path).exists()
    
    def check_directory_exists(self, relative_path):
        """Check if directory exists relative to project root"""
        return (self.project_root / relative_path).is_dir()
    
    def create_api_routes(self):
        """Create API routes using template generation"""
        api_dir = self.project_root / "src/app/api"
        
        # Create agents API
        agents_dir = api_dir / "agents"
        agents_dir.mkdir(parents=True, exist_ok=True)
        
        agents_route = '''import { NextRequest, NextResponse } from 'next/server';
import mysql from 'mysql2/promise';

// Database connection
const getConnection = async () => {
  return mysql.createConnection({
    host: process.env.DATABASE_HOST,
    user: process.env.DATABASE_USER,
    password: process.env.DATABASE_PASSWORD,
    database: process.env.DATABASE_NAME,
  });
};

export async function GET() {
  try {
    const connection = await getConnection();
    const [rows] = await connection.execute(
      `SELECT id, name, type, description, status, capabilities, last_seen, created_at 
       FROM agents ORDER BY created_at DESC`
    );
    await connection.end();
    
    return NextResponse.json({ 
      success: true, 
      agents: rows 
    });
  } catch (error) {
    console.error('Error fetching agents:', error);
    return NextResponse.json({ 
      success: false, 
      error: 'Failed to fetch agents' 
    }, { status: 500 });
  }
}

export async function POST(request: NextRequest) {
  try {
    const { name, type, description, capabilities } = await request.json();
    
    const connection = await getConnection();
    const [result] = await connection.execute(
      `INSERT INTO agents (name, type, description, capabilities, status) 
       VALUES (?, ?, ?, ?, 'active')`,
      [name, type, description, JSON.stringify(capabilities)]
    );
    await connection.end();
    
    return NextResponse.json({ 
      success: true,
      message: 'Agent created successfully',
      id: result.insertId 
    });
  } catch (error) {
    console.error('Error creating agent:', error);
    return NextResponse.json({ 
      success: false, 
      error: 'Failed to create agent' 
    }, { status: 500 });
  }
}'''

        with open(agents_dir / "route.ts", "w") as f:
            f.write(agents_route)
        
        # Create tasks API
        tasks_dir = api_dir / "tasks"
        tasks_dir.mkdir(parents=True, exist_ok=True)
        
        tasks_route = '''import { NextRequest, NextResponse } from 'next/server';
import mysql from 'mysql2/promise';

const getConnection = async () => {
  return mysql.createConnection({
    host: process.env.DATABASE_HOST,
    user: process.env.DATABASE_USER,
    password: process.env.DATABASE_PASSWORD,
    database: process.env.DATABASE_NAME,
  });
};

export async function GET() {
  try {
    const connection = await getConnection();
    const [rows] = await connection.execute(`
      SELECT t.*, p.name as project_name, a.name as agent_name 
      FROM tasks t 
      LEFT JOIN projects p ON t.project_id = p.id 
      LEFT JOIN agents a ON t.assigned_agent_id = a.id 
      ORDER BY t.created_at DESC
    `);
    await connection.end();
    
    return NextResponse.json({ success: true, tasks: rows });
  } catch (error) {
    console.error('Error fetching tasks:', error);
    return NextResponse.json({ 
      success: false, 
      error: 'Failed to fetch tasks' 
    }, { status: 500 });
  }
}

export async function POST(request: NextRequest) {
  try {
    const { title, description, project_id, assigned_agent_id, priority, due_date } = await request.json();
    
    const connection = await getConnection();
    const [result] = await connection.execute(`
      INSERT INTO tasks (title, description, project_id, assigned_agent_id, priority, due_date, status) 
      VALUES (?, ?, ?, ?, ?, ?, 'pending')
    `, [title, description, project_id, assigned_agent_id, priority, due_date]);
    await connection.end();
    
    return NextResponse.json({ 
      success: true,
      message: 'Task created successfully',
      id: result.insertId 
    });
  } catch (error) {
    console.error('Error creating task:', error);
    return NextResponse.json({ 
      success: false, 
      error: 'Failed to create task' 
    }, { status: 500 });
  }
}'''

        with open(tasks_dir / "route.ts", "w") as f:
            f.write(tasks_route)
        
        return {
            "success": True,
            "message": "API routes created successfully",
            "routes": ["agents", "tasks"]
        }
    
    def setup_database_connection(self):
        """Create database connection utility"""
        lib_dir = self.project_root / "src/lib"
        lib_dir.mkdir(parents=True, exist_ok=True)
        
        db_config = '''import mysql from 'mysql2/promise';

export interface DatabaseConfig {
  host: string;
  user: string;
  password: string;
  database: string;
}

export class DatabaseManager {
  private config: DatabaseConfig;

  constructor() {
    this.config = {
      host: process.env.DATABASE_HOST || 'localhost',
      user: process.env.DATABASE_USER || 'root',
      password: process.env.DATABASE_PASSWORD || '',
      database: process.env.DATABASE_NAME || 'command_center',
    };
  }

  async getConnection() {
    try {
      return await mysql.createConnection(this.config);
    } catch (error) {
      console.error('Database connection failed:', error);
      throw new Error('Failed to connect to database');
    }
  }

  async executeQuery<T = any>(query: string, params: any[] = []): Promise<T[]> {
    const connection = await this.getConnection();
    try {
      const [rows] = await connection.execute(query, params);
      return rows as T[];
    } finally {
      await connection.end();
    }
  }

  async insertRecord(table: string, data: Record<string, any>): Promise<number> {
    const columns = Object.keys(data).join(', ');
    const placeholders = Object.keys(data).map(() => '?').join(', ');
    const values = Object.values(data);
    
    const query = `INSERT INTO ${table} (${columns}) VALUES (${placeholders})`;
    const connection = await this.getConnection();
    
    try {
      const [result] = await connection.execute(query, values);
      return (result as any).insertId;
    } finally {
      await connection.end();
    }
  }
}

export const db = new DatabaseManager();'''

        with open(lib_dir / "database.ts", "w") as f:
            f.write(db_config)
        
        return {"success": True, "message": "Database connection utility created"}

    def initialize_git_repo(self):
        """Initialize Git repository with proper setup"""
        try:
            os.chdir(self.project_root)
            
            # Create .gitignore
            gitignore_content = '''# Dependencies
node_modules/
*.log
npm-debug.log*

# Next.js
.next/
out/
dist/

# Environment variables
.env.local
.env.development.local
.env.test.local
.env.production.local

# Database
*.db
*.sqlite

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Build outputs
build/
coverage/'''

            with open(self.project_root / ".gitignore", "w") as f:
                f.write(gitignore_content)
            
            # Initialize git if not already done
            if not (self.project_root / ".git").exists():
                subprocess.run(["git", "init"], check=True)
                subprocess.run(["git", "add", "."], check=True)
                subprocess.run(["git", "commit", "-m", "🚀 Initial Command Center setup with Anders"], check=True)
            
            return {"success": True, "message": "Git repository initialized"}
            
        except Exception as e:
            return {"success": False, "error": str(e)}

if __name__ == "__main__":
    anders = HybridAndersAgent()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "status":
            status = anders.status_report()
            print("🤖 Anders Status Report:")
            print(json.dumps(status, indent=2))
            
        elif command == "create_api":
            result = anders.create_api_routes()
            print("⚡ API Routes:")
            print(json.dumps(result, indent=2))
            
        elif command == "setup_db":
            result = anders.setup_database_connection()
            print("🗄️ Database Setup:")
            print(json.dumps(result, indent=2))
            
        elif command == "init_git":
            result = anders.initialize_git_repo()
            print("📁 Git Setup:")
            print(json.dumps(result, indent=2))
            
        else:
            print(f"❌ Unknown command: {command}")
            print("Available: status, create_api, setup_db, init_git")
    else:
        print("🤖 Anders Hybrid Coding Agent v2.0")
        print("Usage: python3 hybrid_coding_agent.py [command]")
        print("Commands: status, create_api, setup_db, init_git")