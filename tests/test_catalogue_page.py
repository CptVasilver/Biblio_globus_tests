import allure
from biblio_globus_tests.models.profle_page import Profile


@allure.story('Checking categories in catalogue')
def test_catalogue():
    page = Profile()
    page.open('')
    page.login()
    page.open('catalog/categories')
    page.confirm_categories()
