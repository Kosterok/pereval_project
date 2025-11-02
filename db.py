import os
import json
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
load_dotenv()

class PerevalDatabase:
    """Класс для взаимодействия с базой данных ФСТР."""

    def __init__(self):
        """Инициализация подключения к БД через переменные окружения."""
        try:
            self.connection = psycopg2.connect(
                host=os.getenv("FSTR_DB_HOST", "localhost"),
                port=os.getenv("FSTR_DB_PORT", "5432"),
                user=os.getenv("FSTR_DB_LOGIN", "postgres"),
                password=os.getenv("FSTR_DB_PASS", ""),
                dbname=os.getenv("FSTR_DB_NAME", "pereval"),
                cursor_factory=RealDictCursor
            )
        except Exception as error:
            print(f"Ошибка подключения к БД: {error}")
            self.connection = None

    def add_pereval(self, pereval_data: dict):
        """Добавление новой записи о перевале"""
        if not self.connection:
            return None, "Нет подключения к базе данных"

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO pereval_added (date_added, raw_data, images, status)
                    VALUES (%s, %s::jsonb, %s::jsonb, 'new')
                    RETURNING id;
                    """,
                    (
                        pereval_data.get("add_time"),
                        json.dumps(pereval_data, ensure_ascii=False),
                        json.dumps(pereval_data.get("images", []), ensure_ascii=False)
                    ),
                )
                new_id = cursor.fetchone()["id"]
                self.connection.commit()
                return new_id, None
        except Exception as error:
            self.connection.rollback()
            return None, str(error)

    def close(self):
        """Закрытие соединения с базой данных."""
        if self.connection:
            self.connection.close()
