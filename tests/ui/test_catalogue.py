import allure
from biblio_globus_models.pages.profile_page import profile


@allure.parent_suite('UI')
@allure.story('Checking categories in catalogue')
def test_catalogue(browser_managements):
    profile.open('')
    profile.login()
    profile.open('catalog/categories')
    profile.confirm_categories()
