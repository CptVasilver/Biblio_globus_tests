import allure
from biblio_globus_models.pages.profile_page import profile


@allure.parent_suite('UI')
@allure.story('Check media-center announcement')
def test_media_center_announcement(browser_managements):
    profile.open('')
    profile.login()
    profile.go_to_announcement()
    profile.assert_announcement()
