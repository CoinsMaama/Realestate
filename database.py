import os
import psycopg2
from psycopg2 import sql

def init_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            telegram_id BIGINT UNIQUE NOT NULL,
            role VARCHAR(10) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()
    cur.close()
    conn.close()

def get_connection():
    return psycopg2.connect(os.getenv("DATABASE_URL"))

def save_user(telegram_id, role):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO users (telegram_id, role) VALUES (%s, %s) "
        "ON CONFLICT (telegram_id) DO UPDATE SET role = EXCLUDED.role",
        (telegram_id, role)
    )
    conn.commit()
    cur.close()
    conn.close()
