import allure
from biblio_globus_models.pages.profile_page import profile


@allure.parent_suite('UI')
@allure.story('Check contract file')
def test_contract_file(browser_managements):
    profile.open('')
    profile.login()
    profile.download_contract_template()
    profile.file_reconciliation()
