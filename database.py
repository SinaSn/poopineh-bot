import psycopg2

from config import DB_PARAMS


def connect_db():
    conn = psycopg2.connect(**DB_PARAMS)
    return conn


def init_db():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS poo_logs (
        id SERIAL PRIMARY KEY,
        user_id BIGINT NOT NULL,
        username TEXT,
        chat_id BIGINT NOT NULL,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
    )
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS groups (
            chat_id BIGINT PRIMARY KEY
        );"""
    )
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS messages (
            id SERIAL PRIMARY KEY,
            message TEXT NOT NULL
        );"""
    )
    conn.commit()
    cursor.close()
    conn.close()
