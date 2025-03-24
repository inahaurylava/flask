class BasePage():
    def __init__(self, playwright):
        self.playwright = playwright

    def open_url(self, url):
        self.playwright.goto(url)

    def find_element(self):
        return self.playwright

    def click_element(self):
        self.playwright.locator().click()

    def enter_text(self, locator, text, timeout=5):
        element = self.playwright.locator(locator, timeout)
        element.clear()
        element.fill(text)

    def find_elements(self, locator):
        return self.playwright.locator(*locator)