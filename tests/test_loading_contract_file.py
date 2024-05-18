import allure
from biblio_globus_models.pages.profle_page import profile


@allure.story('Check contract file')
def test_contract_file():
    profile.open('')
    profile.login()
    profile.download_contract_template()
    profile.file_reconciliation()
