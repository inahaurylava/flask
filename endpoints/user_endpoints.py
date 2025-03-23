import requests
from endpoints.base_endpoints import BaseEndpoints

class UserEndpoints(BaseEndpoints):
    __CREATE_USER_ROUTE = "api/register"
    __LOGIN_USER_ROUTE = "api/login"

    def __init__(self, host):
        super().__init__(host)

    def create_user(self, username, password):
        resp = requests.post(f"{self.host}/{self.__CREATE_USER_ROUTE}",
                             json={
                                 "username": username,
                                 "password": password
                             })

        assert resp.status_code == 201, "❌Юзер не был создан успешно"
        print("✅Юзер успешно создан")


    def login_user(self, username, password):
        resp = requests.post(f"{self.host}/{self.__LOGIN_USER_ROUTE}",
                             json={
                                 "username": username,
                                 "password": password
                             })

        assert resp.status_code == 200, "❌ Юзер не был успешно залогинен"
        print("✅Юзер успешно залогинен")

        cookies = resp.cookies
        return cookies['session']