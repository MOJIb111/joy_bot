import time
import psycopg2
from config import config

class Repository:
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname= config.DB_CONFIG["dbname"],
            user= config.DB_CONFIG["user"],
            password= config.DB_CONFIG["password"],
            host= config.DB_CONFIG["host"],
            port= config.DB_CONFIG["port"]
        )

    #доделать методы репозитория, описанные в переписке
    def create_table(self):
        time.sleep(5)
        conn = self.conn

        cursor = conn.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS pictures(
            id SERIAL PRIMARY KEY,
            img_url TEXT NOT NULL UNIQUE,
            rating INTEGER NOT NULL,
            date TEXT NOT NULL, 
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
            """)
        conn.commit()
        cursor.close()
        conn.close()
        print("✅ Таблица создана")