import pytest
import os
import re
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
        projects_page = SiteBookBasicPage(login_tab)
        projects_page.navigate(config['loginPageUrl'])
        expect(projects_page.get_text(test_data['loginPageText'])).to_be_visible(timeout=20000)
        assert projects_page.get_title() == test_data['loginPageText']
        context['projects_page'] = projects_page

@when('User enter mobile number')
def enter_mobileNumber(context):
    projects_page = context['projects_page']
    projects_page.fill_input_text(locators_data['mobileNumberInputLocator'],test_data['mobileNumberInputData'])
    projects_page.click_element(locators_data['loginSubmitButton'])

@when('User enter password')
def enter_mobileNumber(context):
    projects_page = context['projects_page']
    projects_page.fill_input_text(locators_data['passwordInputLocator'],test_data['passwordForLogin'])
    projects_page.click_element(locators_data['loginSubmitButton'])


@then('User navigate to the projects page')
def navigate_to_projects(context):
    projects_page = context['projects_page']
    expect(projects_page.get_text(test_data['projectsPageText'])).to_be_visible(timeout=20000)
    assert projects_page.get_url() == config['projectsPageUrl']

@when('User verify sample project cards visible')
def check_sample_project_cards(context):
    projects_page = context['projects_page']
    card_locator = projects_page.locate_locator(locators_data['projectCardsListLocator'])
    any_project_text = card_locator.all_inner_texts()
    project_text = ""
    pattern = r'Sample \w+ Project [\w\+\d]+'
    regex = re.compile(pattern) 
    for text in any_project_text:
        match = regex.search(text)
        if match:
            print(match.group())
            project_text = match.group()
            break
    assert project_text == test_data['SelectProjectText']


@then('User selects the sample project card')
def navigate_quote_page(context):
    projects_page = context['projects_page']
    projects_page.click_element(locators_data['projectCardLocator'])
    expect(projects_page.get_text(test_data['quoteText'])).to_be_visible(timeout=20000)

@when('User selects Detailed Estimate from list')
def navigate_to_single_quote(context):
    projects_page = context['projects_page']
    projects_page.click_element(locators_data['detailedStatementLocator'])

@then('User verify details of the rows')
def verify_row_details(context):
    projects_page = context['projects_page']
    projects_page.verify_row_details(locators_data['groundFloorRowLocator'],test_data['groundFloorQuantity'],test_data['sqftUnit'],test_data['groundFloortotalcost'],locators_data['groundFloorQuantitySelector'],locators_data['groundFloorUnitSelector'],locators_data['groundFloorTotalCostSelector'])
    projects_page.verify_row_details(locators_data['fronYardRowLocator'],test_data['frontYardArea'],test_data['sqftUnit'],test_data['frontYardCost'],locators_data['fronYardQuantitySelector'],locators_data['fronYardUnitSelector'],locators_data['fronYardTotalCostSelector'])
    projects_page.verify_row_details(locators_data['parkingAreaRowLocator'],test_data['parkingAreaQuantity'],test_data['sqftUnit'],test_data['parkingAreaCost'],locators_data['parkingAreaQuantitySelector'],locators_data['parkingAreaUnitSelector'],locators_data['parkingAreaTotalCostSelector'])
    projects_page.verify_row_details(locators_data['passageRowLocator'],test_data['passageArea'],test_data['sqftUnit'],test_data['passageCost'],locators_data['passageQuantitySelector'],locators_data['passageUnitSelector'],locators_data['passageTotalCostSelector'])
    projects_page.verify_row_details(locators_data['lobbyRowLocator'],test_data['lobbyArea'],test_data['sqftUnit'],test_data['lobbyCost'],locators_data['lobbyQuantitySelector'],locators_data['lobbyUnitSelector'],locators_data['lobbyTotalCostSelector'])
    projects_page.verify_row_details(locators_data['toiletParkingAreaRowLocator'],test_data['toiletParkingArea'],test_data['sqftUnit'],test_data['toiletParkingCost'],locators_data['toiletParkingAreaQuantitySelector'],locators_data['toiletParkingAreaUnitSelector'],locators_data['toiletParkingAreaTotalCostSelector'])
    projects_page.verify_row_details(locators_data['dining&DrawingroomRowLocator'],test_data['dining&DrawingroomArea'],test_data['sqftUnit'],test_data['dining&DrawingroomCost'],locators_data['dining&DrawingroomQuantitySelector'],locators_data['dining&DrawingroomUnitSelector'],locators_data['dining&DrawingroomTotalCostSelector'])
    projects_page.verify_row_details(locators_data['pantryAreaRowLocator'],test_data['pantryArea'],test_data['sqftUnit'],test_data['pantryAreaCost'],locators_data['pantryAreaQuantitySelector'],locators_data['pantryAreaUnitSelector'],locators_data['pantryAreaTotalCostSelector'])
    projects_page.verify_row_details(locators_data['backyardRowLocator'],test_data['backyardArea'],test_data['sqftUnit'],test_data['backyardCost'],locators_data['backyardQuantitySelector'],locators_data['backyardUnitSelector'],locators_data['backyardTotalCostSelector'])
    projects_page.verify_row_details(locators_data['firstFloorRowLocator'],test_data['firstFloorArea'],test_data['sqftUnit'],test_data['firstFloorCost'],locators_data['firstFloorQuantitySelector'],locators_data['firstFloorUnitSelector'],locators_data['firstFloorTotalCostSelector'])
    projects_page.verify_row_details(locators_data['diningAreaRowLocator'],test_data['diningArea'],test_data['sqftUnit'],test_data['diningAreaCost'],locators_data['diningAreaQuantitySelector'],locators_data['diningAreaUnitSelector'],locators_data['diningAreaTotalCostSelector'])
    projects_page.verify_row_details(locators_data['balconyRowLocator'],test_data['balconyArea'],test_data['sqftUnit'],test_data['balconyCost'],locators_data['balconyQuantitySelector'],locators_data['balconyUnitSelector'],locators_data['balconyTotalCostSelector'])
    projects_page.verify_row_details(locators_data['livingAreaRowLocator'],test_data['livingArea'],test_data['sqftUnit'],test_data['livingCost'],locators_data['livingAreaQuantitySelector'],locators_data['livingAreaUnitSelector'],locators_data['livingAreaTotalCostSelector'])

@then('User verify details of the rows with wrong data')
def verify_failed_case(context):
    projects_page = context['projects_page']
    projects_page.verify_row_details(locators_data['groundFloorRowLocator'],test_data['wrongQuantity'],test_data['wrongUnit'],test_data['wrongCost'],locators_data['groundFloorQuantitySelector'],locators_data['groundFloorUnitSelector'],locators_data['groundFloorTotalCostSelector'])
    projects_page.verify_row_details(locators_data['fronYardRowLocator'],test_data['wrongQuantity'],test_data['wrongUnit'],test_data['wrongCost'],locators_data['fronYardQuantitySelector'],locators_data['fronYardUnitSelector'],locators_data['fronYardTotalCostSelector'])
    projects_page.verify_row_details(locators_data['parkingAreaRowLocator'],test_data['wrongQuantity'],test_data['wrongUnit'],test_data['wrongCost'],locators_data['parkingAreaQuantitySelector'],locators_data['parkingAreaUnitSelector'],locators_data['parkingAreaTotalCostSelector'])
    projects_page.verify_row_details(locators_data['passageRowLocator'],test_data['wrongQuantity'],test_data['wrongUnit'],test_data['wrongCost'],locators_data['passageQuantitySelector'],locators_data['passageUnitSelector'],locators_data['passageTotalCostSelector'])
    projects_page.verify_row_details(locators_data['lobbyRowLocator'],test_data['wrongQuantity'],test_data['wrongUnit'],test_data['wrongCost'],locators_data['lobbyQuantitySelector'],locators_data['lobbyUnitSelector'],locators_data['lobbyTotalCostSelector'])
    projects_page.verify_row_details(locators_data['toiletParkingAreaRowLocator'],test_data['wrongQuantity'],test_data['wrongUnit'],test_data['wrongCost'],locators_data['toiletParkingAreaQuantitySelector'],locators_data['toiletParkingAreaUnitSelector'],locators_data['toiletParkingAreaTotalCostSelector'])
    projects_page.verify_row_details(locators_data['dining&DrawingroomRowLocator'],test_data['wrongQuantity'],test_data['wrongUnit'],test_data['wrongCost'],locators_data['dining&DrawingroomQuantitySelector'],locators_data['dining&DrawingroomUnitSelector'],locators_data['dining&DrawingroomTotalCostSelector'])
    projects_page.verify_row_details(locators_data['pantryAreaRowLocator'],test_data['wrongQuantity'],test_data['wrongUnit'],test_data['wrongCost'],locators_data['pantryAreaQuantitySelector'],locators_data['pantryAreaUnitSelector'],locators_data['pantryAreaTotalCostSelector'])
    projects_page.verify_row_details(locators_data['backyardRowLocator'],test_data['wrongQuantity'],test_data['wrongUnit'],test_data['wrongCost'],locators_data['backyardQuantitySelector'],locators_data['backyardUnitSelector'],locators_data['backyardTotalCostSelector'])
    projects_page.verify_row_details(locators_data['firstFloorRowLocator'],test_data['wrongQuantity'],test_data['wrongUnit'],test_data['wrongCost'],locators_data['firstFloorQuantitySelector'],locators_data['firstFloorUnitSelector'],locators_data['firstFloorTotalCostSelector'])
    projects_page.verify_row_details(locators_data['diningAreaRowLocator'],test_data['wrongQuantity'],test_data['wrongUnit'],test_data['wrongCost'],locators_data['diningAreaQuantitySelector'],locators_data['diningAreaUnitSelector'],locators_data['diningAreaTotalCostSelector'])
    projects_page.verify_row_details(locators_data['balconyRowLocator'],test_data['wrongQuantity'],test_data['wrongUnit'],test_data['wrongCost'],locators_data['balconyQuantitySelector'],locators_data['balconyUnitSelector'],locators_data['balconyTotalCostSelector'])
    projects_page.verify_row_details(locators_data['livingAreaRowLocator'],test_data['wrongQuantity'],test_data['wrongUnit'],test_data['wrongCost'],locators_data['livingAreaQuantitySelector'],locators_data['livingAreaUnitSelector'],locators_data['livingAreaTotalCostSelector'])