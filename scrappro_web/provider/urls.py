from django.urls import path, include
from .views import get_provider_list

urlpatterns = [
    path('list/<int:client>', get_provider_list),
]