import allure
from biblio_globus_models.pages.profile_page import profile


@allure.story('Checking categories in catalogue')
def test_catalogue():
    profile.open('')
    profile.login()
    profile.open('catalog/categories')
    profile.confirm_categories()
