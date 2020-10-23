from django.urls import path

from .views import *

urlpatterns = [
	path('drivers/<int:pk>/comments/', comments),
	path('drivers/<int:pk>', DriverDetailView.as_view()),
    path('drivers/', driver_list),
    path('teams/', team_list),
    ]