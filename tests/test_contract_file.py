import allure
from biblio_globus_models.models.models import Profile


@allure.story('Check contract file')
def test_contract_file():
    page = Profile()
    #page.open('')
    #page.login()
    doc = page.download_contract_template()
