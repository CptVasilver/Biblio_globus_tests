import allure
from biblio_globus_models.models.profle_page import profile


@allure.story('Increase quantity of product in the cart')
def test_add_book_into_cart_api():

    profile.open('')
    cookie, user_name_cookie = profile.login()
    profile.add_book_with_API(10988536, cookie, user_name_cookie)
    pass