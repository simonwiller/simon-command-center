# Simon's Command Center 🦞

Advanced AI-powered Command Center for managing agents, tasks, and projects across multiple domains.

## Features

- 🤖 **Agent Management** - Coordinate AI agents (Anders, Svend, content agents)
- 📋 **Task System** - Cross-domain task management with priorities  
- 🚀 **Auto Deployment** - GitHub Actions → SiteGround deployment
- 📊 **Analytics Dashboard** - Real-time monitoring and insights
- 🔗 **API Integration** - OpenAI, Claude, WordPress REST APIs

## Domains

- **Elkjøp** - Work projects and campaigns
- **Affiliate** - akasser.dk, pejs.dk, barnevogne.dk, postkasse.dk  
- **Ecommerce** - dolk.dk management
- **Personal** - Life admin and coordination

## Architecture

- **Frontend**: Next.js 15 + TypeScript + Tailwind CSS
- **Backend**: Next.js API Routes + MySQL
- **AI Agents**: OpenAI GPT-4 (Anders) + Claude Sonnet (Content)
- **Coordinator**: Svend via OpenClaw integration
- **Hosting**: SiteGround shared hosting

## Quick Start

1. Clone and install:
   ```bash
   git clone https://github.com/simonwiller/simon-command-center.git
   cd simon-command-center
   npm install
   ```

2. Setup environment:
   ```bash
   cp .env.example .env.local
   # Edit .env.local with your credentials
   ```

3. Setup database:
   ```bash
   mysql -u root -p < database/schema.sql
   ```

4. Run development server:
   ```bash
   npm run dev
   ```

## Deployment

Automatic deployment to SiteGround via GitHub Actions on push to main branch.

---
Test deployment 2026-02-12

Built with ❤️ by Simon Willer & AI Agents
