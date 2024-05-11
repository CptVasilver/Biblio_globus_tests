import allure
from biblio_globus_models.models.profle_page import profile


@allure.story('Check media-center announcement')
def test_media_center_announcement():
    profile.open('')
    profile.login()
    profile.go_to_announcement()
    profile.assert_announcement()
