from pages.base_page import BasePage

class TaskPage(BasePage):
    __INPUT_TASK_TITLE = "[data-testid=\"title-input\"]"
    __INPUT_TASK_DESCRIPTION = "[data-testid=\"description-input\"]"
    __INPUT_TASK_STATUS_CHECKBOX = "[data-testid=\"completed-checkbox\"]"
    __CREATE_TASK_BUTTON = "[data-testid=\"create-task-button\"]"
    __SUBMIT_TASK_BUTTON = "[data-testid=\"submit-button\"]"
    __TASKS_CONTAINER = "[data-testid=\"tasks-container\"]"
    __TASK_ITEM = '//div[@class="col-md-4 mb-4"]'
    __TASK_ITEM_HEADER = '//h5'
    __ERROR_MESSAGE = "[data-test=\"error-message-container\"]"
    __host = ""

    __fdfd = '//a[@class="btn btn-sm btn-warning"]'
    __EDIT_TASK_BUTTON = "[data-testid^=\"edit-task-button\"]"
    __TASK_ITEM_DESCRIPTION = "[data-testid^=\"task-description\"]"
    __TASK_ITEM_TOGGLE_BUTTON = "[data-testid^=\"toggle-button\"]"
    __TASK_DELETE_BUTTON = "[data-testid^=\"delete-task-button\"]"
    __TASK_CONFIRM_DELETE_BUTTON = "[data-testid^=\"delete-confirm-button\"]"
    __TASK_CONFIRM_DELETE_BUTTON2 = '//div[@class="btn btn-danger"]'
    __CONFIRM_DELETE_TASK_MODAL = "[data-testid^=\"delete-modal\"]"
    __CONFIRM_DELETE_TASK_MODAL2 = '//div[@class="modal-dialog"]//div[@class="modal-content"]//div[@class="modal-footer"]//form//button'

    __EXPECTED_COMPLETED_TASK_CHAR = '✓'
    __EXPECTED_INCOMPLETED_TASK_CHAR = '○'

    def __init__(self, playwright, host):
        super().__init__(playwright)
        self.__host = host

    def get_create_task_page(self):
        self.playwright.goto(f'{self.__host}/tasks')

    def click_create_task_button(self):
        self.playwright.locator(self.__CREATE_TASK_BUTTON).click()

    def click_submit_button(self):
        self.playwright.locator(self.__SUBMIT_TASK_BUTTON).click()

    def fill_task_title(self, task_title):
        self.playwright.locator(self.__INPUT_TASK_TITLE).fill(task_title)

    def fill_task_description(self, task_description):
        self.playwright.locator(self.__INPUT_TASK_DESCRIPTION).fill(task_description)

    def click_task_status_checkbox(self):
        self.playwright.locator(self.__INPUT_TASK_STATUS_CHECKBOX).click()

    def get_first_task_item(self):
        # self.get_create_task_page()
        tasks_container = self.playwright.locator(self.__TASKS_CONTAINER)
        tasks_list = tasks_container.locator(self.__TASK_ITEM)

        return tasks_list.first

    def create_task(self, task_title, task_description):
        self.get_create_task_page()
        self.click_create_task_button()

        self.fill_task_title(task_title)
        self.fill_task_description(task_description)
        self.click_submit_button()

        first_task = self.get_first_task_item()

        first_task_header = first_task.locator(self.__TASK_ITEM_HEADER)

        assert first_task_header.inner_text() == task_title, "❌ Созданый таск не появился в списке"
        print("✅ Таск успешно создан")

        return first_task


    def edit_task(self, new_title, new_description):
        first_task = self.get_first_task_item()
        first_task.locator(self.__EDIT_TASK_BUTTON).click()

        self.fill_task_title(new_title)
        self.fill_task_description(new_description)
        self.click_task_status_checkbox()

        self.click_submit_button()

        first_task = self.get_first_task_item()
        first_task_header = first_task.locator(self.__TASK_ITEM_HEADER)
        first_task_description = first_task.locator(self.__TASK_ITEM_DESCRIPTION)
        first_task_toggle_button = first_task.locator(self.__TASK_ITEM_TOGGLE_BUTTON)

        assert first_task_header.inner_text() == new_title, "❌ Название таски не обновилось"
        assert first_task_description.inner_text() == new_description, "❌ Описание таски не обновилось"
        assert first_task_toggle_button.inner_text() == self.__EXPECTED_COMPLETED_TASK_CHAR, "❌ Статус таски не обновилось"

        print("✅ Таск был обновлён успешно")

    def toggle_task_status(self):
        first_task = self.get_first_task_item()
        first_task_toggle_button = first_task.locator(self.__TASK_ITEM_TOGGLE_BUTTON)
        previous_status = first_task_toggle_button.inner_text()

        first_task_toggle_button.click()

        if previous_status == self.__EXPECTED_COMPLETED_TASK_CHAR:
            assert first_task_toggle_button.inner_text() == self.__EXPECTED_INCOMPLETED_TASK_CHAR, "❌ Статус таски не обновился до невыполненного"
        else:
            assert first_task_toggle_button.inner_text() == self.__EXPECTED_COMPLETED_TASK_CHAR, "❌ Статус таски не обновился до выполненного"

        print("✅ Статус таски был обновлён успешно")

    def delete_task(self, title):
        first_task = self.get_first_task_item()
        first_task_header = first_task.locator(self.__TASK_ITEM_HEADER)
        assert first_task_header.inner_text() == title, "❌ Таск не был найден перед его удалением"
        print("✅ Таск был успешно найден перед удалением")

        first_task.locator(self.__TASK_DELETE_BUTTON).click()

        confirm_delete_button = self.playwright.wait_for_selector(self.__CONFIRM_DELETE_TASK_MODAL2, timeout=5000)

        confirm_delete_button.click()

        first_task = self.get_first_task_item()
        first_task_header = first_task.locator(self.__TASK_ITEM_HEADER)
        assert first_task_header.inner_text() != title, "❌ Таск был найден после его удаления"
        print("✅ Таск был ожидаемо не найден после удаления")