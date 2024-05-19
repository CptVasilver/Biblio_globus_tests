import logging

import allure
import requests
from allure import step
from allure_commons.types import AttachmentType
from biblio_globus_models.resources import schema_path
from tests.conftest import BASE_URL, get_cookie
from jsonschema import validate
import json


class ApiPage:
    def login(self, response_needed=False):
        response = get_cookie()
        cookie = response.cookies.get(".ASPXAUTH")
        user_name_cookie = response.cookies.get("UserName")
        if response_needed:
            return response
        else:
            return cookie, user_name_cookie

    def add_book_with_api(self, book_id, cookie, user_name_cookie):
        with allure.step('API request'):
            url = BASE_URL + "/Basket/AddToBasket/"

            headers = {
                'Cookie': f'.ASPXAUTH ={cookie}; UserName={user_name_cookie}'
            }
            with step("Add book"):
                response = requests.request(
                    "POST",
                    url=url,
                    data={"productId": book_id},
                    headers=headers
                )
            response_logging(response)
            basket_id = response.cookies.get("BasketId")
        return basket_id, response

    def change_quantity(self, cookie, user_name_cookie, book_id, quantity):
        with allure.step('API request'):
            url = BASE_URL + "/Basket/ChangeQuantity/"

            headers = {
                'Cookie': f'.ASPXAUTH ={cookie}; UserName={user_name_cookie}'
            }
            with step(f'Change quantity of books to {quantity}'):
                response = requests.request(
                    "POST",
                    url=url,
                    data={"BiblioNo": book_id, "Quantity": quantity},
                    headers=headers
                )
            response_logging(response)
        return response

    def get_regions(self, cookie, user_name_cookie, basket_id, country_id):
        with allure.step('API request'):
            url = BASE_URL + "/Customer/GetRegions/"

            headers = {
                'Cookie': f'.ASPXAUTH ={cookie}; UserName={user_name_cookie}; BasketId={basket_id}'
            }
            with step(f'Receive regions of {country_id} country with GET request'):
                response = requests.request(
                    "GET",
                    url=url,
                    data={"countryId": country_id},
                    headers=headers
                )
                response_logging(response)
        return response

    def get_cities(self, cookie, user_name_cookie, basket_id, country_id, region_id):
        with allure.step('API request'):
            url = BASE_URL + "/Customer/GetCities/"

            headers = {
                'Cookie': f'.ASPXAUTH ={cookie}; UserName={user_name_cookie}; BasketId={basket_id}'
            }
            with step(f'Receive cities of {region_id} region of {country_id} country with GET request'):
                response = requests.request(
                    "GET",
                    url=url,
                    data={"countryId": country_id, "regionId": region_id},
                    headers=headers
                )
            response_logging(response)
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

    def check_sсhema(self, response, request_name):
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


def response_logging(response):
    logging.info("Request: " + response.request.url)
    if response.request.body:
        logging.info("INFO Request body: " + response.request.body)
    logging.info("Request headers: " + str(response.request.headers))
    logging.info("Response code " + str(response.status_code))
    logging.info("Response: " + response.text)
    allure.attach(body=json.dumps(response.json(), indent=4, ensure_ascii=True), name="Response",
                  attachment_type=AttachmentType.JSON, extension="json")
    allure.attach(body=response.request, name="Request",
                  attachment_type=AttachmentType.TEXT, extension="txt")
