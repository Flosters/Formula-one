from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from django.template import TemplateDoesNotExist
from django.template.loader import get_template
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordResetDoneView
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import UpdateView, CreateView, DeleteView, FormView
from django.views.generic.base import TemplateView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.core.signing import BadSignature
from django.contrib.auth import logout
from django.contrib import messages

from .models import AdvUser, Driver, Team, Track
from .forms import ChangeUserInfoForm, RegisterUserForm
from .utilities import signer
 



def index(request):
	"""Главная страница"""
	drivers = Driver.objects.all()
	context = {'drivers': drivers}
	return render(request, 'main/index.html', context)

def other_page(request, page):
	try:
		template = get_template('main/' + page + '.html')
	except TemplateDoesNotExist:
		raise Http404	
	return HttpResponse(template.render(request=request))	

class UserLoginView(LoginView):
	"""Странциа входа"""
	template_name = 'main/login.html'

# Декоратор
# Допускает к странице только пользователей,
# выполнивших вход
@login_required
def profile(request):
	"""Профиля"""
	return render(request, 'main/profile.html')

class UserLogoutView(LoginRequiredMixin, LogoutView):
	"""Выход с сайта"""
	template_name = 'main/logout.html'

class ChangeUserInfoView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
	"""Правки личных данных"""
	model = AdvUser
	template_name = 'main/change_user_info.html'
	form_class = ChangeUserInfoForm
	success_url = reverse_lazy('main:profile')
	success_message = 'Личные данные пользователя изменены'

	def dispatch(self, request, *args, **kwargs):
		self.user_id = request.user.pk
		return super().dispatch(request, *args, **kwargs)

	def get_object(self, queryset=None):
		if not queryset:
			queryset = self.get_queryset()
		return get_object_or_404(queryset, pk=self.user_id)		

class UserPasswordChangeView(SuccessMessageMixin, LoginRequiredMixin, PasswordChangeView):
	"""Изменения пароля"""
	template_name = 'main/password_change.html'
	success_url = reverse_lazy('main:profile')
	success_message = 'Пароль изменен'

class RegisterUserView(CreateView):
	"""Регистрации"""
	model = AdvUser
	template_name = 'main/register_user.html'
	form_class = RegisterUserForm
	success_url = reverse_lazy('main:register_done')

class RegisterDoneView(TemplateView):
	"""Сообщение об успешной регистрации"""	
	template_name = 'main/register_done.html'


def user_activate(request, sign):
	"""активация нового пользователя"""
	try:
		username = signer.unsign(sign)
	except BadSignature:
		return render(request, 'main/bad_signature.html')
	user = get_object_or_404(AdvUser, username=username)
	
	if user.is_activated:
		template = 'main/user_is_activated.html'
	else:
		template = 'main/activation_done.html'
		user.is_active = True
		user.is_activated = True
		user.save()

	return render(request, template)			

class DeleteUserView(DeleteView):
	"""Удаление пользователя"""	
	model = AdvUser
	template_name = 'main/delete_user.html'
	success_url = reverse_lazy('main:index')

	def dispatch(self, request, *args, **kwargs):
		self.user_id = request.user.pk
		return super().dispatch(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		logout(request)
		messages.add_message(request, messages.SUCCESS, 'Пользователь удален')
		return super().post(request, *args, **kwargs)

	def get_object(self, queryset=None):
		if not queryset:
			queryset = self.get_queryset()
		return get_object_or_404(queryset, pk=self.user_id)		


class UserPasswordResetView(PasswordResetView):
	"""Отправка письма для сброса пароля"""
	template_name = 'main/password_reset.html'
	subject_template_name = 'email/reset_subject.txt'
	email_template_name = 'email/reset_email.html'
	success_url = reverse_lazy('main:password_reset_done')
	


class UserPasswordResetDoneView(PasswordResetDoneView):
	"""Уведомление об отправке письма"""
	template_name = 'main/email_sent.html'


class UserPasswordResetConfirmView(PasswordResetConfirmView):
	"""Сброс пароля"""
	template_name = 'main/password_reset_confirm.html'
	success_url = reverse_lazy('main:password_reset_complete')

class UserPasswordResetCompleteView(PasswordResetCompleteView):
	"""Уведомление об успешной смене пароля"""
	template_name = 'main/password_reset_complete.html'

def by_drivers(request):
	"""Вывод всех пилотов"""
	drivers = Driver.objects.all()
	context = {'drivers': drivers}
	return render(request, 'main/by_drivers.html', context)

def by_teams(request):
	"""Вывод всех команд"""
	teams = Team.objects.all()
	context = {'teams': teams}
	return render(request, 'main/by_teams.html', context)

def by_tracks(request):
	"""Вывод всех трасс"""
	tracks = Track.objects.all()
	context = {'tracks': tracks}
	return render(request, 'main/by_tracks.html', context)

def team_detail(request, pk):
	"""Подробно о команде"""
	team = get_object_or_404(Team, pk=pk)
	drivers = Driver.objects.filter(team=pk)
	context = {'team': team, 'drivers': drivers}
	return render(request, 'main/team_detail.html', context)	

def driver_detail(request, pk):
	"""Подробно о гонщике"""
	driver = get_object_or_404(Driver, pk=pk)
	context = {'driver': driver}
	return render(request, 'main/driver_detail.html', context)	

def track_detail(request, pk):
	track = get_object_or_404(Track, pk=pk)
	context = {'track': track}
	return render(request, 'main/track_detail.html', context)