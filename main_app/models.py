from django.db import models
from django.contrib.auth.models import User


class Suffix(models.Model):
    title = models.CharField(max_length=6)


class AttachCategory(models.Model):
    title = models.CharField(max_length=30)
    allowed_suffixes = models.ManyToManyField(Suffix, related_name='allowed_attach_categories')


class Category(models.Model):
    title = models.CharField(max_length=30)
    allowed_attach_categories = models.ManyToManyField(AttachCategory, related_name='allowed_categories')
    allowed_suffixes = models.ManyToManyField(Suffix, related_name='allowed_categories')
    image = models.ImageField(upload_to='dynamic/category_images/', null=True)


class File(models.Model):
    title = models.CharField(max_length=30)
    creation_date = models.DateField(auto_now_add=True)
    modification_date = models.DateField(null=True)
    bytes = models.BinaryField(max_length=10 ** 7)
    suffix = models.ForeignKey(Suffix, on_delete=models.SET_NULL, null=True, related_name='files')


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='account')
    storage = models.BigIntegerField(default=10 ** 6)
    image = models.ImageField(upload_to ='dynamic/user_images/', null= True)


class Library(models.Model):
    title = models.CharField(max_length=30)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, related_name='libraries')


class Content(models.Model):
    title = models.CharField(max_length=30)
    is_private = models.BooleanField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='contents')
    file = models.ForeignKey(File, on_delete=models.CASCADE)
    library = models.ForeignKey(Library, on_delete=models.SET_NULL, null=True, blank=True, related_name='contents')
    creator_account = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, related_name='created_contents')
    shared_with_accounts = models.ManyToManyField(Account, related_name='shared_with_contents')

class ContentAttributeKey(models.Model):
    key = models.CharField(max_length=30)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)

class ContentAttribute(models.Model):
    key = models.ForeignKey(ContentAttributeKey, on_delete=models.CASCADE, related_name='content_attributes')
    value = models.CharField(max_length=50)
    content = models.ForeignKey(Content, on_delete=models.CASCADE)

class Attachment(models.Model):
    title = models.CharField(max_length=30)
    attach_category = models.ForeignKey(AttachCategory, on_delete=models.SET_NULL, null=True,
                                        related_name='attachments')
    content = models.ForeignKey(Content, on_delete=models.CASCADE, related_name='attachments')
    file = models.ForeignKey(File, on_delete=models.CASCADE)



