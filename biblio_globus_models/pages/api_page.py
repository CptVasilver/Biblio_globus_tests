import allure
from allure import step
from biblio_globus_models.resources import schema_path
from biblio_globus_models.utils.api_helper import api_request
from tests.conftest import BASE_URL, get_cookie
from jsonschema import validate
import json


class ApiPage:
    def cities_and_regions_headers(self, cookie, user_name_cookie, basket_id):
        headers = {
            'Cookie': f'.ASPXAUTH ={cookie}; UserName={user_name_cookie}; BasketId={basket_id}'
        }
        return headers

    def book_headers(self, cookie, user_name_cookie):
        headers = {
            'Cookie': f'.ASPXAUTH ={cookie}; UserName={user_name_cookie}'
        }
        return headers

    def login(self, response_needed=False):
        response = get_cookie()
        cookie = response.cookies.get(".ASPXAUTH")
        user_name_cookie = response.cookies.get("UserName")
        if response_needed:
            return response
        else:
            return cookie, user_name_cookie

    def add_book_with_api(self, book_id, cookie, user_name_cookie):
        with allure.step('API request AddToBasket'):
            headers = self.book_headers(cookie, user_name_cookie)
            with step("Add book"):
                response = api_request(
                    base_api_url=BASE_URL,
                    endpoint="/Basket/AddToBasket/",
                    method="POST",
                    data={"productId": book_id},
                    params=headers
                )
            basket_id = response.cookies.get("BasketId")
        return basket_id, response

    def change_quantity(self, cookie, user_name_cookie, book_id, quantity):
        with allure.step('API request ChangeQuantity'):
            headers = self.book_headers(cookie, user_name_cookie)
            with step(f'Change quantity of books to {quantity}'):
                response = api_request(
                    base_api_url=BASE_URL,
                    endpoint="/Basket/ChangeQuantity/",
                    method="POST",
                    data={"BiblioNo": book_id, "Quantity": quantity},
                    params=headers
                )
        return response

    def get_regions(self, cookie, user_name_cookie, basket_id, country_id):
        with allure.step('API request GetRegions'):
            headers = self.cities_and_regions_headers(cookie, user_name_cookie, basket_id)
            with step(f'Receive regions of {country_id} country with GET request'):
                response = api_request(
                    base_api_url=BASE_URL,
                    endpoint="/Customer/GetRegions/",
                    method="GET",
                    data={"countryId": country_id},
                    params=headers
                )
        return response

    def get_cities(self, cookie, user_name_cookie, basket_id, country_id, region_id):
        with allure.step('API request GetCities'):
            headers = self.cities_and_regions_headers(cookie, user_name_cookie, basket_id)
            with step(f'Receive cities of {region_id} region of {country_id} country with GET request'):
                response = api_request(
                    base_api_url=BASE_URL,
                    endpoint="/Customer/GetCities/",
                    method="GET",
                    data={"countryId": country_id, "regionId": region_id},
                    params=headers
                )
        return response

    def check_regions(self, regions):
        with step('Reconcile received regions with list'):
            for region in range(152, 238):
                assert str(region) in regions

    def check_cities(self, cities, cities_list):
        with step('Reconcile received cities with list'):
            for city in cities_list:
                assert city in cities

    def check_status_code(self, status_code, login=False):
        if login:
            assert status_code == 302
        else:
            assert status_code == 200

    def check_schema(self, response, request_name):
        with open(schema_path(f'{request_name}.json')) as file:
            validate(response, schema=json.loads(file.read()))

    def check_resp(self, response, request):
        if request == 'change_quantity':
            assert response == 'true'
        elif request == 'add_to_basket':
            assert response == '{"NumberOfItems":1,"BasketTotal":"692,00","UserName":null}'
        elif request == 'login':
            assert request.find('Object moved')


api_profile = ApiPage()
