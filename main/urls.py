from django.urls import path
from main.views import show_main, create_news, show_news, show_xml, show_json, register, login_user, logout_user, edit_news, delete_news

app_name = 'main'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('create-news/', create_news, name='create_news'),
    path('news/<str:id>/', show_news, name='show_news'),
    path('xml/', show_xml, name='show_xml'),
    path('json/', show_json, name='show_json'),
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('news/<uuid:id>/edit', edit_news, name='edit_news'),
    path('news/<uuid:id>/delete', delete_news, name='delete_news'),
]
