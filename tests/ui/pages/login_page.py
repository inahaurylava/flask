from tests.ui.pages.base_page import BasePage


class LoginPage(BasePage):
    __INPUT_USER_NAME = "[data-testid=\"username-input\"]"
    __INPUT_PASSWORD = "[data-testid=\"password-input\"]"
    __CLICK_BUTTON = "[data-testid=\"login-button\"]"
    __host = ""


    def __init__(self, playwright, host):
        super().__init__(playwright)
        self.__host = host

    def get_login_page(self):
        self.playwright.goto(self.__host)

    def fill_user_name(self, user_name):
        self.playwright.locator(self.__INPUT_USER_NAME).fill(user_name)

    def fill_password(self, password):
        self.playwright.locator(self.__INPUT_PASSWORD).fill(password)

    def click_login_button(self):
        self.playwright.locator(self.__CLICK_BUTTON).click()

    def do_login(self, user_name, password):
        self.playwright.goto(self.__host)
        self.fill_user_name(user_name)
        self.fill_password(password)
        self.click_login_button()

        assert "tasks" in self.playwright.url, "❌ Юзер не был успешно залогинен"
        print("✅ Юзер успешно залогинен")



