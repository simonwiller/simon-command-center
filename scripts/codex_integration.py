#!/usr/bin/env python3
"""
Codex CLI Integration for Anders
Handles OpenAI Codex CLI commands and device auth
"""

import subprocess
import os
import json
from datetime import datetime

class CodexIntegration:
    def __init__(self):
        self.project_root = "/home/ubuntu/simon-command-center"
        
    def check_codex_auth(self):
        """Check if Codex CLI is authenticated"""
        try:
            result = subprocess.run(
                ["codex", "--version"], 
                capture_output=True, 
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                return {"status": "authenticated", "version": result.stdout.strip()}
            else:
                return {"status": "needs_auth", "error": result.stderr}
        except FileNotFoundError:
            return {"status": "not_installed", "error": "Codex CLI not found"}
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    def run_codex_command(self, prompt, auto_approve=False):
        """Run Codex command in project directory"""
        try:
            os.chdir(self.project_root)
            
            # Build codex command
            cmd = ["codex", "exec"]
            if auto_approve:
                cmd.append("--full-auto")
            cmd.append(prompt)
            
            print(f"🤖 Running: {' '.join(cmd)}")
            
            # Execute codex command
            result = subprocess.run(
                cmd,
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            
            return {
                "status": "success" if result.returncode == 0 else "error",
                "returncode": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "timestamp": datetime.now().isoformat()
            }
            
        except subprocess.TimeoutExpired:
            return {"status": "timeout", "error": "Command timed out after 5 minutes"}
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    def generate_api_routes(self):
        """Use Codex to generate API routes for Command Center"""
        prompt = """Create Next.js API routes for the Command Center project:

1. /api/agents - GET (list agents) and POST (create agent)
2. /api/tasks - GET (list tasks) and POST (create task)  
3. /api/projects - GET (list projects) and POST (create project)

Use TypeScript, MySQL2, and proper error handling.
Database connection config from environment variables.
Follow Next.js 15 App Router conventions."""

        return self.run_codex_command(prompt, auto_approve=True)
    
    def implement_database_connection(self):
        """Use Codex to implement database connection utilities"""
        prompt = """Create a database connection utility for the Command Center:

1. Create src/lib/database.ts with MySQL connection
2. Add connection pooling and error handling
3. Create helper functions for common queries
4. Add TypeScript types for database models

Use environment variables for database config."""

        return self.run_codex_command(prompt, auto_approve=True)
    
    def setup_github_integration(self):
        """Use Codex to setup GitHub integration"""
        prompt = """Setup GitHub integration for Command Center project:

1. Initialize git repository if needed
2. Create .gitignore for Next.js project
3. Add all files and make initial commit
4. Configure GitHub Actions for deployment
5. Add README with setup instructions

Make commits with good commit messages."""

        return self.run_codex_command(prompt, auto_approve=True)

if __name__ == "__main__":
    integration = CodexIntegration()
    
    # Check Codex authentication status
    auth_status = integration.check_codex_auth()
    print("🔐 Codex Auth Status:")
    print(json.dumps(auth_status, indent=2))
    
    if auth_status["status"] == "authenticated":
        print("\n✅ Codex is ready! Anders can now generate code.")
        print("\nAvailable commands:")
        print("- generate_api_routes()")
        print("- implement_database_connection()")  
        print("- setup_github_integration()")
    else:
        print(f"\n⏳ Codex status: {auth_status['status']}")
        print("Complete device authentication first.")