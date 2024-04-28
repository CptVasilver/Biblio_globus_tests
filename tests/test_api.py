import allure
from biblio_globus_models.models.models import Profile


def test_login_via_post():
    page = Profile()
    page.open('')
    page.login()

