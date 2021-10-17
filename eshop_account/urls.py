from django.urls import path
from .views import login_user, register, logout, user_account_main_page, edit_user_profile

urlpatterns = [
    path('login',login_user),
    path('register',register),
    path('logout',logout),
    path('user',user_account_main_page),
    path('user/edit',edit_user_profile)
]