from django.urls import path, include
from .views import get_client_list


urlpatterns = [
    path('list', get_client_list),
]