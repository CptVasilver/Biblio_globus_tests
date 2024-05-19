import allure
from biblio_globus_models.pages.api_page import api_profile

book_id = 10988536
book_name = 'Рассказы из русской истории. Петр I. Империя. Т.2. Книга четвертая.'
quantity = int(10)


@allure.parent_suite('API')
@allure.story('Add book into cart with API')
def test_add_book_into_cart_api():
    cookie, user_name_cookie = api_profile.login()
    basket_id, response = api_profile.add_book_with_api(book_id, cookie, user_name_cookie)
    api_profile.check_status_code(response.status_code)
    api_profile.check_sсhema(response.json(), 'add_to_basket')
    api_profile.check_resp(response.text, 'add_to_basket')


@allure.parent_suite('API')
@allure.story('Change quantity of books in cart with API')
def test_change_quantity_of_books_in_cart():
    cookie, user_name_cookie = api_profile.login()
    api_profile.add_book_with_api(book_id, cookie, user_name_cookie)
    response = api_profile.change_quantity(cookie, user_name_cookie, book_id, quantity)
    api_profile.check_status_code(response.status_code)
    api_profile.check_sсhema(response.json(), 'change_quantity')
    api_profile.check_resp(response.text, 'change_quantity')
