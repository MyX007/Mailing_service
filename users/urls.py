from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from users.apps import UsersConfig
from users.views import (RegisterView, ProfileView,
                         user_verification, reset_password,
                         ProfileListView, ProfileUpdateView)
from users.services import BlockUser

app_name = UsersConfig.name


urlpatterns = [
    path(
        '',
        LoginView.as_view(template_name='users/login.html'),
        name='login'
    ),
    path(
        'logout/',
        LogoutView.as_view(),
        name='logout'
    ),
    path(
        'register/',
        RegisterView.as_view(),
        name='register'
    ),
    path(
        'profile/<int:pk>/',
        ProfileView.as_view(),
        name='profile'
    ),
    path(
        'email-confirm/<str:token>/',
        user_verification,
        name='email-confirm'
    ),
    path(
        'password-reset/',
        reset_password,
        name='password-reset'
    ),
    path(
        'list',
        ProfileListView.as_view(),
        name='list'
    ),
    path(
        'profile/edit/<int:pk>/',
        ProfileUpdateView.as_view(),
        name='edit_profile'
    ),
    path(
        'user/<int:pk>/block/',
        BlockUser.block,
        name='block'
    ),
    path(
        'user/<int:pk>/unblock/',
        BlockUser.unblock,
        name='unblock'
    ),
]
