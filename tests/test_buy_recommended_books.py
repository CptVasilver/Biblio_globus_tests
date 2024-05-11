import allure
from biblio_globus_tests.models.profle_page import Profile


@allure.story('Buy a random book with different delivery ways')
def test_buy_with_different_delivery_ways(delivery_check):
    delivery_name, delivery_type = delivery_check

    page = Profile()
    page.open('')
    page.login()
    page.add_book()
    page.full_buy(delivery_type, delivery_name)


@allure.story('Buy a random book with a bag')
def test_buy_book_with_bag():
    page = Profile()
    page.open('')
    page.login()
    page.add_book()
    page.add_bag()
