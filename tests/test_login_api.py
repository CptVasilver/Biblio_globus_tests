import allure
from biblio_globus_models.pages.profle_page import profile


@allure.story('Login with API')
def test_login_via_post():
    profile.open('')
    profile.login()
    profile.confirm_login()

