import time

from conftest_ui import playwright_page
from conftest_ui import app_fixture
import allure
import random
import pytest

from pages.login_page import LoginPage

params = [
    ("ina", "inaina5")
]

@allure.feature("UI Тест")
@allure.story("Полный цикл создания задачи")
@pytest.mark.parametrize("username, password", params)
def test_positive_login(playwright_page, app_fixture, username, password):
    allure.dynamic.title(f"Полный цикл создания таски через UI, юзернейм {username}.")

    # 1 login
    with allure.step("Логин юзера"):
        login_page = LoginPage(playwright_page, app_fixture["host"])
        login_page.do_login('ina', 'inaina5')
        playwright_page.screenshot(path=f"output/screenshots/test_positive_login/screenshot.png")

    # 2-3 Создание новой задачи
    with allure.step("Создание новой задачи и проверка, что она появилась в списке"):
        from pages.task_page import TaskPage
        task_page = TaskPage(playwright_page, app_fixture["host"])

        title = f"test_task_{random.randint(1, 1000)}"
        description = "test_task_description"
        task_page.create_task(title, description)
        playwright_page.screenshot(path=f"output/screenshots/test_positive_create_task/screenshot.png")

    # 4-5 Редактирование задачи (изменение названия, описания, статуса). Проверка, что изменения сохранились
    with allure.step("Редактирование задачи (изменение названия, описания, статуса). Проверка, что изменения сохранились"):
        new_title = f"new_{title}"
        task_page.edit_task(new_title, f"new_{description}")
        playwright_page.screenshot(path=f"output/screenshots/test_positive_edit_task/screenshot.png")

    # 6-7 Отметка задачи как выполненной/невыполненной. Проверка, что статус изменился
    with allure.step("Отметка задачи как выполненной/невыполненной. Проверка, что статус изменился"):
        task_page.toggle_task_status()
        playwright_page.screenshot(path=f"output/screenshots/test_positive_change_status_task/screenshot.png")

    # 8-9 Удаление задачи. Проверка, что задача исчезла из списка.
    with allure.step("Удаление задачи. Проверка, что задача исчезла из списка."):
        task_page.delete_task(new_title)
        playwright_page.screenshot(path=f"output/screenshots/test_positive_delete_task/screenshot.png")

        time.sleep(3)


