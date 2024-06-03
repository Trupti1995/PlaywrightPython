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

    def locate_locator(self, selector:str):
        return self.page.locator(selector)

    def verify_row_details(self, row_selector: str, expected_quantity: float, expected_unit: str, expected_total_cost: float, quantity_selector: str, unit_selector: str, total_selector:str):
        # Locate the row
        row = self.page.locator(row_selector)

        # Get the text content of the elements
        quantity = row.locator(quantity_selector).text_content()
        unit = row.locator(unit_selector).text_content()
        total_cost = row.locator(total_selector).text_content()

        # Convert the text content to the appropriate types
        quantity = float(quantity)
        total_cost = float(total_cost.replace('₹', '').replace(',', '').strip())
        unit = unit.strip()

        # Perform the assertions
        assert quantity == expected_quantity
        assert total_cost == expected_total_cost
        assert unit == expected_unit