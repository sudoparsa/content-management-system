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
        self.account1 = Account.objects.create(user_id=self.user1.id)
        self.account2 = Account.objects.create(user_id=self.user2.id)
        self.category1 = Category.objects.create(title='movie')
        self.category1.allowed_suffixes.add(self.suffix2)
        self.category1.allowed_suffixes.add(self.suffix3)
        self.category1.allowed_attach_categories.add(self.attach_category1)
        self.file1 = File.objects.create(title='leftovers.mkv',
                                         bytes=b'salam',
                                         suffix_id=self.suffix2.id,
                                         creation_date=datetime.date(2022, 8, 18))
        self.library1 = Library.objects.create(title='my library',
                                               category_id=self.category1.id,
                                               account_id=self.account1.id)
        self.content1 = Content.objects.create(title='leftovers',
                                               is_private=True,
                                               category_id=self.category1.id,
                                               file_id=self.file1.id,
                                               library_id=self.library1.id,
                                               creator_account_id=self.account1.id)

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
        self.add_content_url = reverse('add-content')
        self.delete_library_url = reverse('delete-library')
        self.add_attribute_key_url = reverse('add-attribute-key')
        self.delete_content_url = reverse('delete-content')

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

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'Sign-in.html')

    def test_signup_GET(self):
        response = self.client.get(self.signup_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'Sign-up.html')

    def test_signup_POST(self):
        response = self.client.post(self.signup_url, {
            'name': 'new user',
            'username': 'new user name',
            'password': 'development',
            'email': 'new@gmail.com',
        })

        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/login/')

    def test_signup_username_exists_POST(self):
        response = self.client.post(self.signup_url, {
            'name': 'new user',
            'username': 'parsa',
            'password': 'development',
            'email': 'new@gmail.com',
        })

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'Sign-up.html')

    def test_signup_email_exists_POST(self):
        response = self.client.post(self.signup_url, {
            'name': 'new user',
            'username': 'new username',
            'password': 'development',
            'email': 'mostafa@gmail.com',
        })

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'Sign-up.html')

    def test_logout_GET(self):
        response = self.client.get(self.logout_url)

        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/')

    def test_main_GET(self):
        response = self.client.get(self.main_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'main.html')

    def test_my_page_auth_GET(self):
        my_page_url = reverse('my_page', args=['files', 'all'])
        response = self.client.get(my_page_url)

        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/')

    def test_my_page_files_all_GET(self):
        self.test_login_POST()
        my_page_url = reverse('my_page', args=['files', 'all'])
        response = self.client.get(my_page_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'my-page4.html')

    def test_my_page_files_category_GET(self):
        self.test_login_POST()
        my_page_url = reverse('my_page', args=['files', self.category1.title])
        response = self.client.get(my_page_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'my-page4.html')

    def test_my_page_libraries_category_GET(self):
        self.test_login_POST()
        my_page_url = reverse('my_page', args=['libraries', self.category1.title])
        response = self.client.get(my_page_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'my-page4.html')

    def test_my_page_shared_all_GET(self):
        self.test_login_POST()
        self.content1.shared_with_accounts.add(self.account2)
        my_page_url = reverse('my_page', args=['shared', 'all'])
        response = self.client.get(my_page_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'my-page4.html')

    def test_add_content_GET(self):
        response = self.client.get(self.add_content_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'add-content.html')

    def test_share_content_GET(self):
        share_content_url = reverse('share_content', args=[self.content1.id, self.user2.username])
        response = self.client.get(share_content_url)

        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, f'/content/{self.content1.id}/')

    def test_library_page_GET(self):
        library_page_url = reverse('library-page', args=[self.library1.id])
        response = self.client.get(library_page_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'my-page4.html')

    def test_content_main_page_GET(self):
        content_main_page_url = reverse('content_main_page', args=[self.content1.id])
        response = self.client.get(content_main_page_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'content.html')

    def test_add_to_library_GET(self):
        add_library_url = reverse('add_library', args=[self.content1.id,
                                                       self.library1.id])
        response = self.client.get(add_library_url)

        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, f'/content/{self.content1.id}/')

    def test_create_download_link_GET(self):
        url = reverse('download-content', args=[self.content1.id])

        response = self.client.get(url)

        self.assertEquals(response.status_code, 200)

    def test_delete_library_POST(self):
        self.test_login_POST()
        response = self.client.post(self.delete_library_url, {
            'category': self.category1.title,
            'title': self.library1.title,
        })

        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/my-page/libraries/all/')

    def test_add_attribute_key_POST(self):
        self.test_login_POST()
        response = self.client.post(self.add_attribute_key_url, {
            'category': self.category1.title,
            'attribute_name': 'test',
        })

        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/content-attribute-key/')

    def test_add_attribute_key_GET(self):
        response = self.client.get(self.add_attribute_key_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'add-attribute-key.html')

    def test_delete_content_POST(self):
        self.test_login_POST()
        response = self.client.post(self.delete_content_url, {
            'content_id': self.content1.id
        })

        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/my-page/files/all/')
