import allure
from awwwards_tests.models.models import Profile


@allure.story('Log in')
def test_login():
    page = Profile()
    page.open()
    page.login()
    page.go_to_catalogue()
    pass


@allure.story('Checking user country')
def test_check_country():
    page = Profile()
    page.open()
    page.login()
    page.check_country()
