from django.contrib import admin
from models import *
# Register your models here.

from main_app.models import *
admin.site.register(Category)
admin.site.register(Content)
admin.site.register(AttachCategory)
admin.site.register(Suffix)
admin.site.register(Attachment)
admin.site.register(Account)
admin.site.register(Library)
admin.site.register(File)
admin.site.register(ContentAttribute)
admin.site.register(ContentAttributeKey)
