import requests
from tests.api.endpoints.base_endpoints import BaseEndpoints

class TaskEndpoints(BaseEndpoints):
    __TASK_ROUTE = "api/tasks"
    __auth_cookie = ""

    def __init__(self, host, auth_cookie):
        super().__init__(host)
        self.__auth_cookie = auth_cookie


    def create_task(self, title, description, completed):
        resp = requests.post(f"{self.host}/{self.__TASK_ROUTE}",
                             json={
                                 "title": title,
                                 "description": description,
                                 "completed": completed
                             }, headers={"Cookie": f'session={self.__auth_cookie}'})

        assert resp.status_code == 201, "❌ Таск не был успешно создан"
        print("✅ Таск успешно создан")

        return resp.json()

    def get_task(self, task_id, expect_fine):
        resp = requests.get(f"{self.host}/{self.__TASK_ROUTE}/{task_id}", headers={"Cookie": f'session={self.__auth_cookie}'})

        if expect_fine:
            assert resp.status_code == 200, "❌ Таск не найден"

            task_resp = resp.json()

            assert task_resp["id"] == task_id, "❌ Таск id не совпадает с переданным"
            print("✅ Таск id совпадает с переданным")

            return task_resp

        assert resp.status_code == 404, "❌ Таск найден"
        print("✅ Таск ожидаемо не был найден")

        return ''

    def update_task(self, task_id, title, description, completed):
        resp = requests.put(f"{self.host}/{self.__TASK_ROUTE}/{task_id}",
                            json={
                                "title": title,
                                "description": description,
                                "completed": completed
                            },
                            headers={"Cookie": f'session={self.__auth_cookie}'})

        assert resp.status_code == 200, "❌ Таск не был обновлён успешно"

        task_resp = resp.json()

        assert task_resp["title"] == title, "❌ title не обновился"
        assert task_resp["description"] == description, "❌ description не обновился"
        assert task_resp["completed"] == completed, "❌ completed status не обновился"
        print("✅ Таск был обновлён успешно")

    def delete_task(self, task_id):
        resp = requests.delete(f"{self.host}/{self.__TASK_ROUTE}/{task_id}",
                            headers={"Cookie": f'session={self.__auth_cookie}'})

        assert resp.status_code == 204, "❌ Таск не был удалён успешно"
        print("✅ Таск был удалён успешно")