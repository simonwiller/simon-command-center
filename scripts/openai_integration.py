#!/usr/bin/env python3
"""
OpenAI Integration for Anders
Handles OpenAI API calls including device authentication
"""

import os
import json
import requests
import time
from datetime import datetime

class OpenAIIntegration:
    def __init__(self):
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.base_url = "https://api.openai.com/v1"
        self.device_auth_url = "https://auth.openai.com/codex/device"
        
    def device_auth_flow(self):
        """
        Implement OpenAI device authentication flow
        Similar to https://auth.openai.com/codex/device
        """
        print("🔐 Starting OpenAI Device Authentication...")
        print(f"📱 Visit: {self.device_auth_url}")
        print("⏳ Follow the authentication steps in your browser")
        
        # Placeholder for actual device auth implementation
        # This would normally involve:
        # 1. POST to device auth endpoint to get device code
        # 2. Show user code and verification URL  
        # 3. Poll token endpoint until user completes auth
        # 4. Store access token for API calls
        
        return {
            "status": "pending_browser_auth",
            "url": self.device_auth_url,
            "message": "Complete authentication in browser"
        }
    
    def code_generation(self, prompt, context=""):
        """Generate code using OpenAI API"""
        if not self.api_key:
            return "❌ OpenAI API key not configured. Set OPENAI_API_KEY environment variable."
        
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            system_msg = f"""You are Anders, Simon's coding agent for the Command Center project.
            
Project Context:
- Next.js 15 + TypeScript + Tailwind CSS
- MySQL database with agents, tasks, projects tables
- Goal: AI-powered task and agent management system

Current context: {context}

Generate practical, working code that follows TypeScript/Next.js best practices."""

            data = {
                "model": "gpt-4",
                "messages": [
                    {"role": "system", "content": system_msg},
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": 2000,
                "temperature": 0.3
            }
            
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=data
            )
            
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content']
            else:
                return f"❌ API Error: {response.status_code} - {response.text}"
                
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    def analyze_project(self, project_path):
        """Analyze current project status"""
        analysis = {
            "timestamp": datetime.now().isoformat(),
            "project_path": project_path,
            "files_found": [],
            "next_steps": []
        }
        
        # Check key project files
        key_files = [
            "package.json",
            "next.config.js", 
            "tailwind.config.js",
            "src/app/page.tsx",
            "src/app/dashboard/page.tsx",
            "database/schema.sql",
            ".github/workflows/deploy.yml"
        ]
        
        for file in key_files:
            file_path = os.path.join(project_path, file)
            if os.path.exists(file_path):
                analysis["files_found"].append(file)
        
        # Determine next steps based on what's missing
        if "package.json" not in analysis["files_found"]:
            analysis["next_steps"].append("Initialize Next.js project")
        elif not any("api" in f for f in analysis["files_found"]):
            analysis["next_steps"].append("Implement API routes")
        else:
            analysis["next_steps"].append("Ready for deployment")
            
        return analysis

if __name__ == "__main__":
    integration = OpenAIIntegration()
    
    # Test device auth flow
    auth_result = integration.device_auth_flow()
    print(json.dumps(auth_result, indent=2))
    
    # Analyze project
    project_analysis = integration.analyze_project("/home/ubuntu/simon-command-center")
    print("\n📊 Project Analysis:")
    print(json.dumps(project_analysis, indent=2))