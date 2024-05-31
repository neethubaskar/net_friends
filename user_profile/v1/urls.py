from django.urls import path, include
from user_profile.v1.views.user_registration import (
    UserRegistrationView, LoginView, LogoutView, UserSearchView)

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-registration'),
    path('login/', LoginView.as_view(), name='user-login'),
    path('logout/', LogoutView.as_view(), name='user-logout'),
    path('search/', UserSearchView.as_view(), name='user-search'),
]