from conftest_api import api_fixture
from conftest_api import db_connection
from db.db_operations import DbOperations
from endpoints.task_endpoints import TaskEndpoints
from endpoints.user_endpoints import UserEndpoints
import allure
import pytest

params = [
    ("ina_5", "password123")
]

@allure.feature("API Тест")
@allure.story("Полный цикл создания задачи через API запросы")
@pytest.mark.parametrize("username, password", params)
def test_api(api_fixture, db_connection, username, password):
    allure.dynamic.title(f"Полный цикл создания таски через API, юзернейм {username}.")

    # 1 Создание юзера
    with allure.step("Создание юзера"):
        user_endpoints = UserEndpoints(api_fixture["host"])
        user_endpoints.create_user(username, password)

    # 2 авторизовали юзера
    with allure.step("Авторизация юзера"):
        auth_cookie = user_endpoints.login_user(username, password)

    # 3 создали таск
    with allure.step("Создание таски"):
        task_endpoints = TaskEndpoints(api_fixture["host"], auth_cookie)
        task = task_endpoints.create_task("title", "password", True)

    # получили таск по айди
    with allure.step("Получение таски по айди"):
        task_from_api = task_endpoints.get_task(task["id"], True)
        task_id = task_from_api["id"]

    # подняли таск из базы по айди и сравнили с таском из апи
    with allure.step("Получение таски из бд и сравнение с таской из апи"):
        db_operations = DbOperations(db_connection)
        task_from_db = db_operations.get_task_and_compare(task_from_api, task_id)

    # 7, 8 изменение title, description, completed задачи
    with allure.step("Изменение таски"):
        new_status = not task_from_db[3]
        task_endpoints.update_task(task_from_api["id"], "title", "password", new_status)

    # 9 удаление задачи
    with allure.step("Удаление"):
        task_endpoints.delete_task(task_from_api["id"])

    # 10 проверяем, что удалили
    with allure.step("Проверка удалённой таски"):
        task_endpoints.get_task(task_from_api["id"], False)