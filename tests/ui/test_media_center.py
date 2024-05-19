import allure
from biblio_globus_models.pages.profile_page import profile


@allure.story('Check media-center announcement')
def test_media_center_announcement(browser_management):
    profile.open('')
    profile.login()
    profile.go_to_announcement()
    profile.assert_announcement()
