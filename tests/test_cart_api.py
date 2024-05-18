import allure
from biblio_globus_models.pages.profle_page import profile, api_profile

book_id = 10988536
book_name = 'Рассказы из русской истории. Петр I. Империя. Т.2. Книга четвертая.'
quantity = int(10)

@allure.story('Add book into cart with API')
def test_add_book_into_cart_api():
    profile.open('')
    cookie, user_name_cookie = profile.login()
    api_profile.add_book_with_api(book_id, cookie, user_name_cookie)
    api_profile.confirm_book_in_cart(book_name)


@allure.story('Change quantity of books in cart with API')
def test_change_quantity_of_books_in_cart():
    profile.open('')
    cookie, user_name_cookie = profile.login()
    basket_id, resp = api_profile.add_book_with_api(book_id, cookie, user_name_cookie)
    response = api_profile.change_quantity(cookie, user_name_cookie, basket_id, book_id, book_name, quantity)
    api_profile.confirm_book_quantity(book_id, quantity)
    api_profile.check_status_code(resp.status_code)
    api_profile.check_status_code(response.status_code)
    api_profile.check_shema(resp.json(), 'add_to_basket')
    api_profile.check_shema(response.json(), 'change_quantity')