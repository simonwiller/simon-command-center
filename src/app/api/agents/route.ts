import { NextRequest, NextResponse } from 'next/server';
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
    ) as any[];
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
}
