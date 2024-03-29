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
    path('my-page/<str:type>/<str:categoryTitle>/', views.my_page, name= 'my_page'),
    path('library/<int:libraryId>/', views.library_page, name= 'library-page'),
    path('personal-info', views.personal_info, name = 'personal-info'),
    path('show-library/', views.show_library, name='show-library'),
    path('add-library/', views.add_library, name='add-library'),
    path('add-attribute-key/', views.add_attribute_key, name='add-attribute-key'),
    path('delete-library', views.delete_library, name='delete-library'),
    path('delete-attribute-key/<str:item_id>', views.delete_attribute_key, name='delete-attribute-key'),
    path('content-attribute-key/', views.show_attribute_key, name='content-attribute-key'),
    path('content-attribute-key/category/<str:cat_id>', views.get_category, name='get_cat_id'),
    path('delete-content', views.delete_content, name='delete-content')

]
