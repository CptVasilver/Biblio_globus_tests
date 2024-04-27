import allure
from biblio_globus_models.models.models import Profile


@allure.story('Check media-center announcement')
def test_mediacenter_announcement():
    page = Profile()
    page.open('')
    page.login()
    page.go_to_announcement()
