from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    path('login', views.user_login, name='login'),
    path('logout', views.user_logout, name='logout'),
    path('register', views.user_register, name='register'),
    path('account/toggle_follow/<user_name>', views.toggle_follow, name='toggle_follow'),
    path('edit_info', views.user_edit_info, name='edit_info'),
    path('edit_profile', views.user_edit_profile, name='edit_profile'),
    path('change_password', views.user_change_password, name='change_password'),
    path('reset_password', views.user_reset_password, name='reset_password'),
    path('profile/<user_name>', views.user_profile, name='profile'),
]
