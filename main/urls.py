from django.urls import path


from .views import *

app_name = 'main'

urlpatterns = [
	path('accounts/register/activate/<str:sign>/', user_activate, name='register_activate'),
	path('accounts/register/done', RegisterDoneView.as_view(), name='register_done'),
	path('accounts/register', RegisterUserView.as_view(), name='register'),
	path('accounts/password/reset/<uidb64>/<token>/', UserPasswordResetConfirmView.as_view(), 
									name='password_reset_confirm'),
	path('accounts/password/reset/complete/', UserPasswordResetCompleteView.as_view(), 
									name='password_reset_complete'),
	path('accounts/password/reset/done/', UserPasswordResetDoneView.as_view(),
									name='password_reset_done'),
	path('accounts/password/reset/', UserPasswordResetView.as_view(), 
									name='password_reset'),
	path('accounts/password/change', UserPasswordChangeView.as_view(), name='password_change'),
	path('accounts/profile/delete/', DeleteUserView.as_view(), name='profile_delete'),
	path('accounts/profile/change', ChangeUserInfoView.as_view(), name='profile_change'),
	path('accounts/profile/', profile, name='profile'),
	path('accounts/logout/', UserLogoutView.as_view(), name='logout'),
	path('accounts/login/', UserLoginView.as_view(), name='login'),
	path('drivers/<int:pk>/', driver_detail, name='driver_detail'),
	path('drivers/', by_drivers, name='by_drivers'),
	path('teams/<int:pk>/', team_detail, name='team_detail'),
	path('teams/', by_teams, name='by_teams'),
	path('tracks/', by_tracks, name='by_tracks'),
	path('gran-pri/', result_table, name='result_table'),
	path('<str:page>/', other_page, name='other'),
	path('', index, name='index'),
	]