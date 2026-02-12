-- Command Center Database Schema
-- MySQL Database for Simon's Command Center

CREATE DATABASE IF NOT EXISTS command_center;
USE command_center;

-- Users table
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    role ENUM('admin', 'agent', 'viewer') DEFAULT 'viewer',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Projects table
CREATE TABLE projects (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    domain ENUM('elkjop', 'affiliate', 'ecommerce', 'personal') NOT NULL,
    status ENUM('active', 'paused', 'completed', 'cancelled') DEFAULT 'active',
    priority INT DEFAULT 3, -- 1=high, 2=medium, 3=low
    start_date DATE,
    deadline DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Agents table
CREATE TABLE agents (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    type ENUM('coding', 'content', 'coordinator', 'monitor') NOT NULL,
    description TEXT,
    api_endpoint VARCHAR(500),
    status ENUM('active', 'inactive', 'maintenance') DEFAULT 'active',
    capabilities JSON, -- ["web_scraping", "content_generation", etc.]
    config JSON, -- Agent-specific configuration
    last_seen TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Tasks table
CREATE TABLE tasks (
    id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    project_id INT,
    assigned_agent_id INT,
    assigned_user_id INT,
    status ENUM('pending', 'in_progress', 'review', 'completed', 'cancelled') DEFAULT 'pending',
    priority INT DEFAULT 3, -- 1=high, 2=medium, 3=low
    estimated_hours DECIMAL(4,1),
    actual_hours DECIMAL(4,1),
    due_date DATETIME,
    completed_at TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE SET NULL,
    FOREIGN KEY (assigned_agent_id) REFERENCES agents(id) ON DELETE SET NULL,
    FOREIGN KEY (assigned_user_id) REFERENCES users(id) ON DELETE SET NULL
);

-- Agent logs table
CREATE TABLE agent_logs (
    id INT PRIMARY KEY AUTO_INCREMENT,
    agent_id INT NOT NULL,
    task_id INT,
    action VARCHAR(255) NOT NULL,
    message TEXT,
    level ENUM('info', 'warning', 'error', 'success') DEFAULT 'info',
    metadata JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (agent_id) REFERENCES agents(id) ON DELETE CASCADE,
    FOREIGN KEY (task_id) REFERENCES tasks(id) ON DELETE SET NULL
);

-- Deployments table
CREATE TABLE deployments (
    id INT PRIMARY KEY AUTO_INCREMENT,
    project_id INT,
    agent_id INT,
    version VARCHAR(50),
    status ENUM('pending', 'building', 'deploying', 'success', 'failed') DEFAULT 'pending',
    commit_hash VARCHAR(40),
    branch VARCHAR(100) DEFAULT 'main',
    deploy_url VARCHAR(500),
    error_message TEXT,
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP NULL,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE SET NULL,
    FOREIGN KEY (agent_id) REFERENCES agents(id) ON DELETE SET NULL
);

-- Site monitoring table
CREATE TABLE site_monitoring (
    id INT PRIMARY KEY AUTO_INCREMENT,
    site_name VARCHAR(255) NOT NULL,
    url VARCHAR(500) NOT NULL,
    status_code INT,
    response_time_ms INT,
    is_up BOOLEAN DEFAULT TRUE,
    last_check TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Initial data
INSERT INTO users (email, name, role) VALUES 
('simon@simonwiller.dk', 'Simon Willer', 'admin');

INSERT INTO agents (name, type, description, capabilities) VALUES 
('Svend', 'coordinator', 'Central AI Coordinator - OpenClaw integration', '["task_management", "coordination", "monitoring"]'),
('Anders', 'coding', 'Development Agent - Code generation and deployment', '["code_generation", "github_integration", "deployment"]');

INSERT INTO projects (name, description, domain, priority) VALUES 
('Command Center', 'Advanced AI Command Center for task and agent management', 'personal', 1),
('Personalized Campaigns', 'Elkjøp CRO project - campaign effectiveness optimization', 'elkjop', 1),
('Affiliate Site Optimization', 'SEO and content pipeline for affiliate sites', 'affiliate', 2);

INSERT INTO site_monitoring (site_name, url) VALUES 
('Akasser.dk', 'https://akasser.dk'),
('Pejs.dk', 'https://pejs.dk'),
('Barnevogne.dk', 'https://barnevogne.dk'),
('Postkasse.dk', 'https://postkasse.dk'),
('Dolk.dk', 'https://dolk.dk');