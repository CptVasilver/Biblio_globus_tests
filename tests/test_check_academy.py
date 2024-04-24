import allure
from awwwards_tests.models.models import Profile


@allure.story('Checking categories of courses in academy')
def test_categories():
    page = Profile()
    page.open()
    page.check_categories()


@allure.story('Looking for specific course')
def test_check_course():
    page = Profile()
    page.open()
    page.check_course()
