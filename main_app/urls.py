from django.urls import path

from . import views

urlpatterns = [
    path('suffix/', views.suffix, name='suffix'),
    path('create-suffix/', views.create_suffix, name='create_suffix'),
    path('attach-category/', views.attach_category, name='attach-category'),
    path('create-attach-category/', views.create_attach_category, name='create-attach-category'),
    path('category/', views.category, name='category'),
    path('create-category/', views.create_category, name='create-category')
]
