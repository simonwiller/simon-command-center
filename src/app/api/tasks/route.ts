import { NextRequest, NextResponse } from 'next/server';
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
}