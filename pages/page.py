from playwright.sync_api import Page

class SiteBookBasicPage:
    def __init__(self, page: Page):
        self.page = page

    def navigate(self, url:str):
        self.page.goto(url)

    def get_title(self):
        return self.page.title()

    def click_element(self, selector: str):
        self.page.locator(selector).click()

    def wait_for_event(self):
        self.page.wait_for_event('popup')

    def wait_for_load_state(self):
        self.page.wait_for_load_state("load")

    def get_url(self) -> str:
        return self.page.url

    def get_text(self,text):
        return self.page.get_by_text(text)

    def fill_input_text(self,selector: str, input_text):
        self.page.locator(selector).fill(input_text)