import allure
from biblio_globus_models.pages.api_page import api_profile

book_id = 10988536
country_id = 643
region_id = 236
cities_list = ["Анадырь", "Билибино", "Певек"]


@allure.parent_suite('API')
@allure.story('Check delivery regions with API')
def test_check_delivery_regions_api():
    cookie, user_name_cookie = api_profile.login()
    basket_id = api_profile.add_book_with_api(book_id, cookie, user_name_cookie)
    regions = api_profile.get_regions(cookie, user_name_cookie, basket_id, country_id)
    api_profile.check_regions(regions.text)
    api_profile.check_status_code(regions.status_code)
    api_profile.check_schema(regions.json(), 'get_regions')


@allure.parent_suite('API')
@allure.story(f'Check delivery cities in {region_id} region with API')
def test_check_delivery_cities_api():
    cookie, user_name_cookie = api_profile.login()
    basket_id = api_profile.add_book_with_api(book_id, cookie, user_name_cookie)
    cities = api_profile.get_cities(cookie, user_name_cookie, basket_id, country_id, region_id)
    api_profile.check_cities(cities.text, cities_list)
    api_profile.check_status_code(cities.status_code)
    api_profile.check_schema(cities.json(), 'get_cities')
