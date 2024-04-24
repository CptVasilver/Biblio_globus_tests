import allure
from awwwards_tests.models.models import Profile


@allure.story('Checking pinterest account')
def test_pinterest():
    page = Profile()
    page.open()
    page.check_pinterest()
