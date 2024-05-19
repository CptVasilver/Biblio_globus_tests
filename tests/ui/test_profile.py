import allure
from biblio_globus_models.pages.profile_page import profile

test_user_data = {'Surname': 'Куаев', 'Name': 'Тестер', 'DoB': '01.01.2000', 'Sex': 'm',
                  'Phone number': '88005553535', 'Email': 'vasilver.work@yandex.ru'}
test_new_user_data = {'Surname': 'Куаева', 'Name': 'Тестериня', 'DoB': '01.01.2000', 'Sex': 'm',
                  'Phone number': '88005553535', 'Email': 'vasilver.work@yandex.ru'}

@allure.story('Confirm current user info')
def test_confirm_test_data(browser_managements):
    profile.open('')
    profile.login()
    profile.confirm_user_data(test_user_data)


@allure.story('Change current user info')
def test_change_user_data(browser_managements):
    profile.open('')
    profile.login()
    profile.change_user_data(test_new_user_data)
    profile.confirm_user_data(test_new_user_data)
    profile.change_user_data(test_user_data)
    profile.confirm_user_data(test_user_data)

