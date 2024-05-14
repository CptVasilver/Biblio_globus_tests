import os
from os import path
from urllib.request import urlretrieve
import pypandoc
import allure
import requests
from allure import step
from allure_commons.types import AttachmentType
from selene import browser, have, command, be
from biblio_globus_models.resources import file_path
from tests.conftest import get_cookie, BASE_URL
from biblio_globus_models.utils import attach
from urllib.parse import quote


def find_delivery_text(delivery_name):
    if delivery_name == 'Self-borrow':
        return 'Подтверждение заказа'
    elif delivery_name == 'Boxberry':
        return 'Boxberry'
    elif delivery_name == 'Courier':
        return 'Курьерская доставка'
    elif delivery_name == 'Russia post':
        return 'Доставка «Почта России»'


class ProfilePage:

    def open(self, page):
        browser.open('/' + page)

    #  browser.all('.link-underlined').element_by(have.text('Reject all')).click()

    def scroll(self, tag):
        browser.element(f'.{tag}').perform(command.js.scroll_into_view)

    def add_book(self):
        with step('Add book to cart'):
            self.scroll('product')
            browser.element('.buttons').element('.btn').click()

    def add_bag(self):
        with step('Add bag to cart'):
            browser.element('[data-target="#recommendedProducts"]').click()
            browser.element('#add_9961627').click()

    def confirm_bag_in_cart(self):
        browser.element('.shopping-cart-title-counter').should(have.text('2'))

    def choose_delivery_type(self, delivery_type):
        browser.element('#usualCheckout').with_(click_by_js=True).click()
        with step(f'Choose a delivery type {delivery_type}'):
            browser.element(f'#{delivery_type}').click()
            browser.element('#usualCheckout').click()

    def confirm_delivery_type(self, delivery_type, delivery_name):
        delivery_text = find_delivery_text(delivery_name)
        browser.element('.box').should(have.text(delivery_text))

    def confirm_user_data(self, data):
        self.open('customer/profile')
        with step('Confirming test user data'):
            browser.element('#Customer_SecondName').should(have.value(data['Surname']))
            browser.element('#Customer_FirstName').should(have.value(data['Name']))
            browser.element('#BirthDate').should(have.value(data['DoB']))
            browser.element(f'#sex_{data["Sex"]}').should(have.value('1'))
            browser.element('#Customer_Phone_Basic').should(have.value(data['Phone number']))
            browser.element('#Customer_Email').should(have.value(data['Email']))
            allure.attach(body=str(data), name="Test data", attachment_type=AttachmentType.TEXT, extension="txt")

    def login(self):
        cookie, user_name_cookie = get_cookie()
        browser.driver.add_cookie({"name": ".ASPXAUTH", "value": cookie})
        browser.open('/')
        return cookie, user_name_cookie

    def confirm_login(self):
        with step('Confirm success login0'):
            browser.element('#icon_cab3').should(be.visible)

    def change_user_data(self, data):
        self.open('customer/profile')
        with step('Change user data'):
            browser.element('#Customer_SecondName').clear().type(data['Surname'])
            browser.element('#Customer_FirstName').clear().type(data['Name'])
            browser.element('.bootstrap-frm').element('[type="submit"]').click()
            browser.element('.bootstrap-frm>p').should(have.text('Изменения успешно сохранены'))

    def confirm_categories(self):
        browser.all('.card-header>h5').should(
            have.exact_texts('Художественная литература', 'Психология', 'Бизнес. Продвижение. Экономика',
                             'Информационные технологии', 'Философия. Эзотерика. Религия',
                             'Гуманитарные и общественные науки', 'Естественные науки. Математика',
                             'Прикладные науки. Техника. Сельское хозяйство', 'Книги для детей', 'Искусство',
                             'Английский язык', 'Немецкий язык', 'Французский язык', 'Другие языки',
                             'Медицина. Здоровье', 'Канцелярские товары', 'Хобби. Путешествия. Кулинария',
                             'Юриспруденция. Право', 'Спорт. Красота. Здоровье', 'Учебники',
                             'Антиквариат. Товары для Коллекционеров. Букинистика. Подарки',
                             'Постеры. Плакаты. Календари', 'Аудио/Видео', 'Подарочные карты'))

    def go_to_announcement(self):
        with step('Open announcement tab'):
            self.open('mediacenter/events')
            browser.element('[href="/mediacenter/event/645"]').click()
            browser.element('.d-block').with_(click_by_js=True).click()
        with step('Go to «Черный хлеб дорог» announcement'):
            browser.switch_to_next_tab()

    def assert_announcement(self):
        with step('Assert it is right announcement'):
            browser.element('#event-title').should(have.text('Презентация книги «Черный хлеб дорог»'))

    def download_contract_template(self):
        with step('Download contract'):
            self.open('information/corporate-customer-service')
            browser.element('#headingOne').click()
            url = quote('https://www.biblio-globus.ru/doc/Договор (Москва).docx', safe=':/')
            file_name = file_path('document.docx')
            urlretrieve(url, file_name)
            output = pypandoc.convert_file(file_name, 'plain', outputfile="biblio_globus_models/files/Doc.txt")
            a = path.isfile(file_path('Doc.txt'))

    def file_reconciliation(self):
        with open(file_path('Doc.txt'), 'r', encoding='utf-8') as f:
            with step('Checking file for correctness'):
                assert f.readline(9) == 'ДОГОВОР №'
                doc_attach = f.read()
                allure.attach(body=doc_attach, name="Document", attachment_type=AttachmentType.TEXT, extension="txt")
            f.close()
        open(file_path('Doc.txt'), 'w').close()
        open(file_path('document.docx'), 'w').close()

    def add_book_with_API(self, book_id, cookie, user_name_cookie):
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
        return basket_id

    def confirm_book_in_cart(self, book_name):
        with step(f'Searchig for {book_name} in cart'):
            browser.element('.product-name').should(have.text(book_name))

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

    def confirm_book_quantity(self, book_id, quantity):
        with step(f'Reconcile quantity of books with requested quantity'):
            browser.element(f'#basket_quantity1').should(have.text(str(quantity)))

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
        return response.text

    def check_regions(self, regions):
        with step('Reconcile received regions with list'):
            for region in range(152, 238):
                assert str(region) in regions

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
        return response.text

    def check_cities(self, cities, cities_list):
        with step('Reconcile received cities with list'):
            for city in cities_list:
                assert city in cities


profile = ProfilePage()
