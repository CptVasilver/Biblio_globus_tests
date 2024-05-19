import allure
import requests
import pytest
import os
from biblio_globus_models.utils import attach
from selene import browser
from allure import step
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv
from allure_commons.types import AttachmentType

DEFAULT_BROWSER_VERSION = "122.0"
BASE_URL = "https://www.biblio-globus.ru"


def pytest_addoption(parser):
    parser.addoption(
        '--browser_version',
        default='122.0'
    )


@pytest.fixture(scope='session', autouse=True)
def load_env():
    load_dotenv()


@pytest.fixture(scope='function',
                params=[('delivery_0', 'Self-borrow'), ('delivery_1', 'Boxberry'), ('delivery_2', 'Courier'),
                        ('delivery_3', 'Russia post')])
def delivery_check(request):
    delivery_type, delivery_name = request.param
    return delivery_name, delivery_type


@pytest.fixture(scope='function', autouse=False)
def browser_managements(request):
    browser_version = request.config.getoption('--browser_version')
    browser_version = browser_version if browser_version != "" else DEFAULT_BROWSER_VERSION
    options = Options()
    selenoid_capabilities = {
        "browserName": "chrome",
        "browserVersion": browser_version,
        "selenoid:options": {
            "enableVNC": True,
            "enableVideo": True
        }
    }
    options.capabilities.update(selenoid_capabilities)
    selenoid_login = os.getenv("SELENOID_LOGIN")
    selenoid_pass = os.getenv("SELENOID_PASS")
    driver = webdriver.Remote(
        command_executor=f"https://{selenoid_login}:{selenoid_pass}@selenoid.autotests.cloud/wd/hub",
        options=options
    )

    browser.config.driver = driver

    browser.config.base_url = BASE_URL
    browser.config.window_width = 1920
    browser.config.window_height = 1080
    browser.config.timeout = 15

    yield

    attach.add_video(browser)
    attach.add_logs(browser)
    attach.add_html(browser)
    attach.add_screenshot(browser)
    browser.quit()


def get_cookie():
    user_login = os.getenv("USER_LOGIN")
    user_pass = os.getenv("USER_PASSWORD")
    url = BASE_URL + "/auth/login"
    with step("Login via API"):
        response = requests.request(
            "POST",
            url=url,
            data={"UserName": user_login, "Password": user_pass, "RememberMe": False},
            allow_redirects=False
        )
        allure.attach(body=response.text, name="Response", attachment_type=AttachmentType.TEXT, extension="txt")
        allure.attach(body=response.cookies.get(".ASPXAUTH"), name="Cookie", attachment_type=AttachmentType.TEXT,
                      extension="txt")
    return response
