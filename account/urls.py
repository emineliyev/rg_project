from django.urls import path
from .views import register, profile, logout_view, user_login

app_name = 'account'
urlpatterns = [
    path('registration/', register, name='registration'),
    path('login/', user_login, name='login'),
    path('profile/', profile, name='profile'),
    path('logout/', logout_view, name='logout'),
]
