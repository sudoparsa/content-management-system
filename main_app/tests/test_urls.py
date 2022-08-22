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

    def test_content_main_page_url_is_resolved(self):
        url = reverse('content_main_page', args=['1'])
        self.assertEquals(resolve(url).func, content_main_page)

    def test_add_content_url_is_resolved(self):
        url = reverse('add-content')
        self.assertEquals(resolve(url).func, add_content)

    def test_download_content_url_is_resolved(self):
        url = reverse('download-content', args=[1])
        self.assertEquals(resolve(url).func, create_download_link)

    def test_share_content_url_is_resolved(self):
        url = reverse('share_content', args=[1, '<username>'])
        self.assertEquals(resolve(url).func, share_content)

    def test_show_library_url_is_resolved(self):
        url = reverse('show-library')
        self.assertEquals(resolve(url).func, show_library)

    def test_add_library_url_is_resolved(self):
        url = reverse('add-library')
        self.assertEquals(resolve(url).func, add_library)

    def test_add_attribute_key_url_is_resolved(self):
        url = reverse('add-attribute-key')
        self.assertEquals(resolve(url).func, add_attribute_key)

    def test_delete_library_url_is_resolved(self):
        url = reverse('delete-library')
        self.assertEquals(resolve(url).func, delete_library)

    def test_add_to_library_url_is_resolved(self):
        url = reverse('add_library', args=[1, 1])
        self.assertEquals(resolve(url).func, add_to_library)
