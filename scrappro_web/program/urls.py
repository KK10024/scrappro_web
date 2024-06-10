from django.urls import path, include
from .views import program_login, program_version, UserDetail_view

urlpatterns = [
    path('login', program_login),
    path('user_info', UserDetail_view),
    path('version', program_version),
]
