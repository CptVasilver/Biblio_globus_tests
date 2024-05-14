import allure
from biblio_globus_models.models.profle_page import profile

book_id = 10988536
book_name = 'Рассказы из русской истории. Петр I. Империя. Т.2. Книга четвертая.'
quantity = int(10)

@allure.story('Add book into cart with API')
def test_add_book_into_cart_api():
    profile.open('')
    cookie, user_name_cookie = profile.login()
    profile.add_book_with_API(book_id, cookie, user_name_cookie)
    profile.confirm_book_in_cart(book_name)


@allure.story('Change quantity of books in cart with API')
def test_change_quantity_of_books_in_cart():
    profile.open('')
    cookie, user_name_cookie = profile.login()
    basket_id = profile.add_book_with_API(book_id, cookie, user_name_cookie)
    profile.change_quantity(cookie, user_name_cookie, basket_id, book_id, book_name, quantity)
    profile.confirm_book_quantity(book_id, quantity)
    pass