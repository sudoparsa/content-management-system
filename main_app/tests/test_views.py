from django.test import TestCase, Client
from django.urls import reverse
from main_app.models import *
import datetime


class TestViews(TestCase):
    def create_objects(self):
        self.suffix1 = Suffix.objects.create(title='srt')
        self.suffix2 = Suffix.objects.create(title='mkv')
        self.suffix3 = Suffix.objects.create(title='mp4')
        self.attach_category1 = AttachCategory.objects.create(title='subtitle')
        self.user1 = User.objects.create_user(username='parsa',
                                              password='development',
                                              email='parsa@gmail.com')
        self.user2 = User.objects.create_user(username='mostafa',
                                              password='1234',
                                              email='mostafa@gmail.com')
        self.category1 = Category.objects.create(title='movie')
        self.category1.allowed_suffixes.add(self.suffix2)
        self.category1.allowed_suffixes.add(self.suffix3)
        self.category1.allowed_attach_categories.add(self.attach_category1)
        self.file1 = File.objects.create(title='leftovers.mkv',
                                         bytes=b'salam',
                                         creation_date=datetime.date(2022, 8, 18))
        self.content1 = Content.objects.create(title='leftovers',
                                               is_private=True,
                                               category_id=self.category1.id,
                                               file_id=self.file1.id,)

    def setUp(self):
        self.create_objects()
        self.client = Client()
        self.suffix_url = reverse('suffix')
        self.create_suffix_url = reverse('create_suffix')
        self.attach_category_url = reverse('attach-category')
        self.create_attach_category_url = reverse('create-attach-category')
        self.category_url = reverse('category')
        self.create_category_url = reverse('create-category')
        self.login_url = reverse('login')
        self.signup_url = reverse('signup')
        self.logout_url = reverse('logout')
        self.main_url = reverse('main')
        self.test_url = reverse('test')

    def test_suffix_GET(self):
        response = self.client.get(self.suffix_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'example.html')

    def test_create_suffix_POST(self):
        response = self.client.post(self.create_suffix_url, {
            'suffix': 'mkv'
        })
        self.assertEquals(response.status_code, 200)

    def test_attach_category_GET(self):
        response = self.client.get(self.attach_category_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'example2.html')

    def test_create_attach_category_POST(self):
        response = self.client.post(self.create_attach_category_url, {
            'suffix-id': self.suffix1.id,
            'title': 'subtitle'
        })

        self.assertEquals(response.status_code, 200)

    def test_category_GET(self):
        response = self.client.get(self.category_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'example3.html')

    def test_create_category_POST(self):
        response = self.client.post(self.create_category_url, {
            'suffix-id': self.suffix1.id,
            'category-id': self.attach_category1.id,
            'title': 'movie',
        })

        self.assertEquals(response.status_code, 200)

    def test_login_GET(self):
        response = self.client.get(self.login_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'Sign-in.html')

    def test_login_POST(self):
        response = self.client.post(self.login_url, {
            'username': 'parsa',
            'password': 'development',
        })

        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/')

    def test_login_failed_POST(self):
        response = self.client.post(self.login_url, {
            'username': 'mostafa',
            'password': '123',
        })

        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/login/')

    def test_signup_GET(self):
        response = self.client.get(self.signup_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'Sign-up.html')

    def test_signup_POST(self):
        response = self.client.post(self.signup_url, {
            'name':     'new user',
            'username': 'new user name',
            'password': 'development',
            'email':    'new@gmail.com',
        })

        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/login/')

    def test_signup_POST_username_exists(self):
        response = self.client.post(self.signup_url, {
            'name':     'new user',
            'username': 'parsa',
            'password': 'development',
            'email':    'new@gmail.com',
        })

        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/signup/')

    def test_signup_POST_email_exists(self):
        response = self.client.post(self.signup_url, {
            'name':     'new user',
            'username': 'new username',
            'password': 'development',
            'email':    'mostafa@gmail.com',
        })

        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/signup/')

    def test_logout_GET(self):
        response = self.client.get(self.logout_url)

        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/')

    def test_main_GET(self):
        response = self.client.get(self.main_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'main.html')

    def test_test_GET(self):
        response = self.client.get(self.test_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'category.html')

    def test_my_page_GET_files_all(self):
        my_page_url = reverse('my_page', args=['files', 'all'])
        response = self.client.get(my_page_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'my-page4.html')

    def test_my_page_GET_files_category(self):
        my_page_url = reverse('my_page', args=['files', self.category1.id])
        response = self.client.get(my_page_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'my-page4.html')
