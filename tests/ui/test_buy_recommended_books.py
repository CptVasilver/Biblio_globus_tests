import allure
from biblio_globus_models.pages.profile_page import profile


@allure.story('Buy a random book with different delivery ways')
def test_buy_with_different_delivery_ways(browser_management, delivery_check):
    delivery_name, delivery_type = delivery_check

    profile.open('')
    profile.login()
    profile.add_book()
    profile.choose_delivery_type(delivery_type)
    profile.confirm_delivery_type(delivery_name)


@allure.story('Buy a random book with a bag')
def test_buy_book_with_bag(browser_management):
    profile.open('')
    profile.login()
    profile.add_book()
    profile.add_bag()
    profile.confirm_bag_in_cart()
