from django.urls import path
from main.views import show_main, create_news, show_news, show_xml, show_json, show_xml_by_id, show_json_by_id, register, login_user, logout_user, edit_news, delete_news, add_news_entry_ajax

app_name = 'main'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('create-news/', create_news, name='create_news'),
    path('news/<str:id>/', show_news, name='show_news'),
    path('xml/', show_xml, name='show_xml'),
    path('json/', show_json, name='show_json'),
    path('xml/<str:news_id>/', show_xml_by_id, name='show_xml_by_id'),
    path('json/<str:news_id>/', show_json_by_id, name='show_json_by_id'),
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('news/<uuid:id>/edit', edit_news, name='edit_news'),
    path('news/<uuid:id>/delete', delete_news, name='delete_news'),
    path('create-news-ajax', add_news_entry_ajax, name='add_news_entry_ajax'),
]
