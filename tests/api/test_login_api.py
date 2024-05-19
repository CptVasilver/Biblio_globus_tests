import allure
from biblio_globus_models.pages.api_page import api_profile

@allure.story('Login with API')
def test_login_via_post():
    response = api_profile.login(response_needed=True)
    api_profile.check_status_code(response.status_code, login=True)

