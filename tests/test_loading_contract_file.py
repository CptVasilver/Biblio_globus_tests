import allure
from biblio_globus_tests.models.profle_page import Profile


@allure.story('Check contract file')
def test_contract_file():
    page = Profile()
    page.open('')
    page.login()
    page.download_contract_template()
