import pytest
import os
from pytest_bdd import scenarios, given, then, when
from playwright.sync_api import sync_playwright, Page, expect
from utils.config_loader import load_config
from pages.siteBookPage import load_file
from pages.page import SiteBookBasicPage

scenarios('./siteBook.feature')

@pytest.fixture
def context():
    return {}

config = load_config(os.getenv('ENV', 'default'))
test_data = load_file("utils/testData.json")
locators_data = load_file("utils/locators.json")

@given('User navigate to the my site book URL')
def navigate_to_example(context):
    headless = os.getenv('HEADLESS', 'true').lower() == 'true'
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        page = browser.new_page()
        home_page = SiteBookBasicPage(page)
        home_page.navigate(config['url'])
        context['browser'] = browser
        context['home_page'] = home_page
        yield
        page.close()
        browser.close()

@then('User verify the title should be the configured title')
def check_title(context):
    home_page = context['home_page']
    assert home_page.get_title() == test_data['mainPageTitle']

@when('User click on login button')
def login(context):
    home_page = context['home_page']
    home_page.click_element(locators_data["loginButton"])

@then('User navigate to the login page')
def check_loginPage_navigation(context):
        home_page = context['home_page']
        login_tab = context['home_page'].page.wait_for_event('popup')
        context['login_tab'] = login_tab
        login_tab.wait_for_load_state()
        login_page = SiteBookBasicPage(login_tab)
        login_page.navigate(config['loginPageUrl'])
        expect(login_page.get_text(test_data['loginPageText'])).to_be_visible(timeout=20000)
        assert login_page.get_title() == test_data['loginPageText']
        context['login_page'] = login_page

@when('User enter mobile number')
def enter_mobileNumber(context):
    login_page = context['login_page']
    login_page.fill_input_text(locators_data['mobileNumberInputLocator'],test_data['mobileNumberInputData'])
    login_page.click_element(locators_data['loginSubmitButton'])

@when('User enter password')
def enter_mobileNumber(context):
    login_page = context['login_page']
    login_page.fill_input_text(locators_data['passwordInputLocator'],test_data['passwordForLogin'])
    login_page.click_element(locators_data['loginSubmitButton'])
    

@then('User navigate to the projects page')
def navigate_to_projects(context):
    login_page = context['login_page']
    expect(login_page.get_text(test_data['projectsPageText'])).to_be_visible(timeout=20000)
    assert login_page.get_url() == config['projectsPageUrl']