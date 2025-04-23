class DbOperations():
    def __init__(self, connection):
        self.connection = connection

    def get_task_and_compare(self, task_from_api, task_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT id, title, description, completed FROM task WHERE id = %s", (task_id,))
        task_from_db = cursor.fetchone()
        cursor.close()
        assert task_from_db is not None, f"❌ Задача с ID {task_id} не найдена в БД!"
        print(f"✅ Таск найден в БД: {task_from_db}")

        # 6 сравниваем апи и бд
        assert task_from_api["id"] == task_from_db[0], "❌ Таск id не совпадает с БД"
        assert task_from_api["title"] == task_from_db[1], "❌ Таск title не совпадает с БД"
        assert task_from_api["description"] == task_from_db[2], "❌ Таск description не совпадает с БД"
        assert task_from_api["completed"] == task_from_db[3], "❌ Таск completed не совпадает с БД"

        print(f"✅ Поля таска из БД сопадают с таском из АПИ: {task_from_db}")

        return task_from_db