import allure
from biblio_globus_tests.models.profle_page import Profile


def test_login_via_post():
    page = Profile()
    page.open('')
    page.login()

