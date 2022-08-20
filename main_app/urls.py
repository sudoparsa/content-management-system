from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('signup/', views.sign_up, name='signup'),
    path('suffix/', views.suffix, name='suffix'),
    path('create-suffix/', views.create_suffix, name='create_suffix'),
    # path('signup#/', views.sign_up, name='signup'),
    # path('content/<int:content_id>/', views.content_main_page, name='content_main_page'),
    path('attach-category/', views.attach_category, name='attach-category'),
    path('create-attach-category/', views.create_attach_category, name='create-attach-category'),
    path('category/', views.category, name='category'),
    path('create-category/', views.create_category, name='create-category'),
    path('my-page/', views.my_page, name= 'my_page'),
    path('', views.main, name = 'main'),
    path('test', views.test, name='test'),
    path('content', views.add_content, name='add-content'),
    path('content/<int:content_id>/', views.content_main_page, name='content_main_page'),
    path('my-page/<str:type>/<str:category>', views.my_page, name='my_page'),
    path('', views.main, name='main'),
    path('test', views.test, name='test')]
    path('my-page/<str:type>/<str:categoryTitle>/', views.my_page, name= 'my_page'),
    path('', views.main, name = 'main'),
    path('test', views.test, name = 'test'),
]
