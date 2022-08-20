from django.test import SimpleTestCase
from django.urls import resolve, reverse
from main_app.views import *


class TestUrls(SimpleTestCase):

    def test_login_url_is_resolved(self):
        url = reverse('login')
        self.assertEquals(resolve(url).func, login)

    def test_logout_url_is_resolved(self):
        url = reverse('logout')
        self.assertEquals(resolve(url).func, logout)

    def test_signup_url_is_resolved(self):
        url = reverse('signup')
        self.assertEquals(resolve(url).func, sign_up)

    def test_suffix_url_is_resolved(self):
        url = reverse('suffix')
        self.assertEquals(resolve(url).func, suffix)

    def test_create_suffix_url_is_resolved(self):
        url = reverse('create_suffix')
        self.assertEquals(resolve(url).func, create_suffix)

    def test_attach_category_url_is_resolved(self):
        url = reverse('attach-category')
        self.assertEquals(resolve(url).func, attach_category)

    def test_create_attach_category_url_is_resolved(self):
        url = reverse('create-attach-category')
        self.assertEquals(resolve(url).func, create_attach_category)

    def test_category_url_is_resolved(self):
        url = reverse('category')
        self.assertEquals(resolve(url).func, category)

    def test_create_category_url_is_resolved(self):
        url = reverse('create-category')
        self.assertEquals(resolve(url).func, create_category)

    def test_my_page_url_is_resolved(self):
        url = reverse('my_page', args=['mkv', 'movie'])
        self.assertEquals(resolve(url).func, my_page)

    def test_main_url_is_resolved(self):
        url = reverse('main')
        self.assertEquals(resolve(url).func, main)

    def test_test_url_is_resolved(self):
        url = reverse('test')
        self.assertEquals(resolve(url).func, test)
