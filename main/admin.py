from django.contrib import admin
import datetime

from .models import AdvUser, Driver, Team, Track, Comment, Post
from .utilities import send_activation_notification

def send_activation_notifications(modeladmin, request, queryset):
	"""Отправка писем с оповещениями об активации"""
	for rec in queryset:
		if not rec.is_activated:
			send_activation_notification(rec)
	modeladmin.message_user(request, 'Письма с оповещениями отправлены')

send_activation_notifications.short_description = 'Отправка писем с оповещениями об активации'


class NonactivatedFilter(admin.SimpleListFilter):
	title = 'Прошли активацию?'
	parameter_name = 'acstate'

	def lookups(self, request, model_admin):
		return(
				('activated','Прошли'),
				('threedays', 'Не прошли более 3-х дней'),
				('week', 'Не прошли более недели'),
				)

	def queryset(self, request, queryset):
		val = self.value()
		if val == 'activated':
			return queryset.filter(is_active=True, is_activated=True)
		elif val == 'threedays':
			d = datetime.date.today() - datetime.timedelta(days=3)
			return queryset.filter(is_active=False, is_activated=False, date_joined__date__lt=d)
		elif val == 'week':
			d = datetime.date.today() - datetime.timedelta(weeks=7)
			return queryset.filter(is_active=False, is_activated=False, date_joined__date__lt=d)


class AdvUserAdmin(admin.ModelAdmin):
	list_display = ('__str__', 'is_activated', 'date_joined' )
	search_fields = ('username', 'email', 'first_name', 'last_name', 'favorite_team')						
	list_filter = (NonactivatedFilter,)

	fields = (
				('username', 'email'),
				('first_name', 'last_name'),
				('send_messages', 'is_active', 'is_activated'),
				'favorite_team',
				('is_staff', 'is_superuser'),
				'groups', 'user_permissions',
				('last_login', 'date_joined')
				)
	readonly_fields = ('last_login', 'date_joined')
	actions = (send_activation_notifications,)


class DriverAdmin(admin.ModelAdmin):
	list_display = ('first_name', 'last_name', 'date_of_birth', 'country','team', 'is_active' )

	search_fields = ('last_name', 'country', 'is_active')						

	
class TeamAdmin(admin.ModelAdmin):
	list_display = ('name', 'debut_in_f1', 'country', 'is_active' )

	search_fields = ('last_name', 'country', 'is_active')	

	
class TrackAdmin(admin.ModelAdmin):
	list_display = ('name', 'build', 'located', 'drive', 'length', 'width',
					'number_of_turns', 'record', 'is_active')

	search_fields = ('name', 'build', 'located', 'drive', 'is_active')


class CommentAdmin(admin.ModelAdmin):
	list_display = ('driver', 'author', 'created_at', 'content')


class PostAdmin(admin.ModelAdmin):
	list_display = ('title', 'author', 'content', 'created_at')
	search_fields = ('title', 'author', 'content', 'created_at')


admin.site.register(AdvUser, AdvUserAdmin)
admin.site.register(Driver, DriverAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Track, TrackAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Post, PostAdmin)

