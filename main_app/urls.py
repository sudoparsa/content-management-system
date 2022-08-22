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
    path('content', views.add_content, name='add-content'),
    path('content/<int:content_id>/', views.content_main_page, name='content_main_page'),
    path('content/<int:content_id>/download-link-content', views.create_download_link, name='download-content'),
    path('content/<int:content_id>/addLibrary/<int:library_id>/', views.add_to_library, name='add_library'),
    path('content/<int:content_id>/shareContent/<str:username>/', views.share_content, name='share_content'),
    path('', views.main, name='main'),
    path('my-page/<str:type>/<str:categoryTitle>/', views.my_page, name='my_page'),
    path('test', views.test, name='test'),

    path('show-library/', views.show_library, name='show-library'),
    path('add-library/', views.add_library, name='add-library'),
    path('add-attribute-key/', views.add_attribute_key, name='add-attribute-key'),

    path('delete-library', views.delete_library, name='delete-library')
]
