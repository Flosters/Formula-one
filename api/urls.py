from django.urls import path

from .views import *

urlpatterns = [
    path('drivers/', driver_list),
    path('teams/', team_list),
]