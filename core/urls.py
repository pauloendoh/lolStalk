from django.urls import path
from django.contrib.auth import views as auth_views

from core import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', auth_views.login, {'template_name': 'login.html'}, name='login'),
    path('logout/', auth_views.logout, {'next_page': '/'}, name='logout'),
]