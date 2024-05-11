import allure
from biblio_globus_tests.models.profle_page import Profile


@allure.story('Check media-center announcement')
def test_media_center_announcement():
    page = Profile()
    page.open('')
    page.login()
    page.go_to_announcement()
