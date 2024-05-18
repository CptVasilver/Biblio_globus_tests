import allure
import requests
from allure import step
from allure_commons.types import AttachmentType
from selene import browser, have
from biblio_globus_models.resources import schema_path
from tests.conftest import BASE_URL
from jsonschema import validate
import json

class ApiPage:
    def add_book_with_api(self, book_id, cookie, user_name_cookie):
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
        with step("Add cookies"):
            for cookie_name, cookie_value in response.cookies.items():
                allure.attach(body=cookie_value, name=f"Cookie {cookie_name}", attachment_type=AttachmentType.TEXT,
                              extension="txt")
                browser.driver.add_cookie({"name": cookie_name, "value": cookie_value})
        browser.open('/basket/detail')
        basket_id = response.cookies.get("BasketId")
        return basket_id, response



    def change_quantity(self, cookie, user_name_cookie, basket_id, book_id, book_name, quantity):
        url = BASE_URL + "/Basket/ChangeQuantity/"

        headers = {
            'Cookie': f'.ASPXAUTH ={cookie}; UserName={user_name_cookie}; BasketId={basket_id}'
        }
        with step(f'Change quantity of {book_name} to {quantity}'):
            response = requests.request(
                "POST",
                url=url,
                data={"BiblioNo": book_id, "Quantity": quantity},
                headers=headers
            )
        browser.open('/basket/detail')
        return response



    def get_regions(self, cookie, user_name_cookie, basket_id, country_id):
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
            allure.attach(body=response.text, name="Regions", attachment_type=AttachmentType.TEXT,
                          extension="txt")
        return response



    def get_cities(self, cookie, user_name_cookie, basket_id, country_id, region_id):
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
            allure.attach(body=response.text, name="Cities", attachment_type=AttachmentType.TEXT,
                          extension="txt")
        return response

    def confirm_book_in_cart(self, book_name):
        with step(f'Searchig for {book_name} in cart'):
            browser.element('.product-name').should(have.text(book_name))

    def confirm_book_quantity(self, book_id, quantity):
        with step(f'Reconcile quantity of books with requested quantity'):
            browser.element(f'#quantity_{book_id}').should(have.attribute("value", str(quantity)))

    def check_regions(self, regions):
        with step('Reconcile received regions with list'):
            for region in range(152, 238):
                assert str(region) in regions

    def check_cities(self, cities, cities_list):
        with step('Reconcile received cities with list'):
            for city in cities_list:
                assert city in cities

    def check_status_code(self, status_code):
        assert status_code == 200

    def check_shema(self, response, request_name):
        with open(schema_path(f'{request_name}.json')) as file:
            validate(response.json(), schema=json.loads(file.read()))


api_profile = ApiPage()

