import allure
from biblio_globus_models.models.profle_page import profile

book_id = 10988536
country_id = 643
region_id = 236
cities_list = ["Анадырь", "Билибино", "Певек"]


@allure.story('Check delivery regions with API')
def test_check_delivery_regions_api():
    profile.open('')
    cookie, user_name_cookie = profile.login()
    basket_id = profile.add_book_with_API(book_id, cookie, user_name_cookie)
    regions = profile.get_regions(cookie, user_name_cookie, basket_id, country_id)
    profile.check_regions(regions)


@allure.story(f'Check delivery cities in {region_id} region with API')
def test_check_delivery_cities_api():
    profile.open('')
    cookie, user_name_cookie = profile.login()
    basket_id = profile.add_book_with_API(book_id, cookie, user_name_cookie)
    cities = profile.get_cities(cookie, user_name_cookie, basket_id, country_id, region_id)
    profile.check_cities(cities, cities_list)
