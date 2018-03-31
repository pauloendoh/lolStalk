from django.urls import path
from django.contrib.auth import views as auth_views

from core import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', auth_views.login, {'template_name': 'login.html'}, name='login'),
    path('logout/', auth_views.logout, {'next_page': '/'}, name='logout'),
    path('search', views.search, name='search' ),
    path('summoner/<str:region>/<str:nickname>', views.summoner, name='summoner' ),
    path('champions', views.champions, name='champions'),
    path('follow/<int:summoner_id>', views.follow, name="follow"),
    path('following', views.following, name='following'),
    path('expired_api_key', views.expired_api_key, name="expired_api_key"),
    path('update_matches', views.update_matches, name='update_matches'),

]