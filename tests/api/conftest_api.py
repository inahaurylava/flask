import pytest
import os
import psycopg2

DB_PARAMS = {
    'dbname': os.environ.get('POSTGRES_DB', 'taskmanager'),
    'user': os.environ.get('POSTGRES_USER', 'postgres'),
    'password': os.environ.get('POSTGRES_PASSWORD', 'postgres'),
    #local
    'host': os.environ.get('POSTGRES_HOST', 'localhost'),
    #Docker
    #'host': os.environ.get('POSTGRES_HOST', 'db'),
    'port': os.environ.get('POSTGRES_PORT', '5432')
}

@pytest.fixture
def api_fixture():
    host = "http://localhost:5000"
    #host = "http://web:5000"

    return { "host" : host }

@pytest.fixture(scope="function")
def db_connection():
    """Фикстура для подключения к БД"""
    print("🔌 Подключение к БД...")
    conn = psycopg2.connect(**DB_PARAMS)  # Устанавливаем соединение с БД
    yield conn  # Передаем соединение в тест

    cur=conn.cursor()
    sql_delete = 'DELETE FROM task'
    cur.execute(sql_delete)

    # чистим всех пользователей кроме тех, которые используются в ui тестах и не должны быть удалены
    sql_delete_users = 'DELETE FROM "user" WHERE username != %s'
    param = 'ina_ui'
    cur.execute(sql_delete_users, (param,))
    # Фиксируем изменения
    conn.commit()
    # Узнаем, сколько строк было удалено
    rows_deleted = cur.rowcount
    print(f"Удалено строк: {rows_deleted}")
    cur.close()
    conn.close()  # Закрываем соединение после теста
    print("🔌 Соединение с БД закрыто.")