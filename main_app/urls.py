from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('signup/', views.sign_up, name='signup'),
    path('signup#/', views.sign_up, name='signup'),
    path('content/<int:content_id>/', views.content_main_page, name='content_main_page'),
    path('attach-category/', views.attach_category, name='attach-category'),
    path('create-attach-category/', views.create_attach_category, name='create-attach-category'),
    path('category/', views.category, name='category'),
    path('create-category/', views.create_category, name='create-category')
]
