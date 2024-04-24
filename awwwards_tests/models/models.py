import os
import requests
from selene import browser, have, command

from tests.conftest import get_cookie


class Profile:

    def open(self):
        browser.open('/')

    #  browser.all('.link-underlined').element_by(have.text('Reject all')).click()

    def scroll(self, tag):
        browser.element(f'.{tag}').perform(command.js.scroll_into_view)

    def go_to_catalogue(self):
        browser.element('[href="/catalog/categories"]').double_click()

    def check_country(self):
        browser.element('.header-main__user').click()
        browser.element('.text-sd').should(have.text('Afghanistan'))

    def assert_pint(self):
        browser.element('[data-test-id="profile-name"]').should(have.text('awwwards.'))
        browser.element('[data-test-id="main-user-description-text"]').should(have.text('The awards for design, '
                                                                                        'creativity and innovation on'
                                                                                        ' the Internet, '
                                                                                        'which recognize and promote '
                                                                                        'the best web designers in '
                                                                                        'the world'))

    def assert_courses(self):
        browser.all('.filter-box__list').all('span').should(
            have.texts('Illustration', 'Marketing & Business', 'Photography & video', 'Design', '3d & Animation',
                       'Web & App Design', 'Calligraphy & Typography'))

    def login(self):
        cookie = get_cookie()
        browser.driver.add_cookie({"name": ".ASPXAUTH", "value": cookie})
        browser.open('/')

    def check_pinterest(self):
        self.scroll('footer__nav')
        browser.element('[href="https://www.pinterest.es/awwwards/"]').click()
        self.assert_pint()

    def check_categories(self):
        self.choose_page('course')
        self.scroll('filter-box__list')
        self.assert_courses()

    def check_course(self):
        self.choose_page('course')
        self.scroll('filter-box__list')
        browser.element('.card-academy__title').should(have.text('Master Figma from 0 to 100'))
        browser.element('.card-academy__by').should(have.text('Mirko Santangelo'))
