import mysql from 'mysql2/promise';

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

export const db = new DatabaseManager();