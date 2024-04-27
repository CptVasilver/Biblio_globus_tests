import allure
from biblio_globus_models.models.models import Profile

test_user_data = {'Surname': 'Куаев', 'Name': 'Тестер', 'DoB': '01.01.2000', 'Sex': 'm',
                  'Phone number': '88005553535', 'Email': 'vasilver.work@yandex.ru'}


@allure.story('Confirm current user info')
def test_confirm_test_data():
    page = Profile()
    page.open('')
    page.login()
    page.confirm_user_data(test_user_data)


@allure.story('Change current user info')
def test_change_user_data():
    page = Profile()
    page.open('')
    page.login()
    page.change_user_data(test_user_data)
