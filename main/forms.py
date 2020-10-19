from django import forms
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from captcha.fields import CaptchaField

from .models import AdvUser, user_registrated, Comment

class ChangeUserInfoForm(forms.ModelForm):
	"""Форма для изменения личных данных"""
	email = forms.EmailField(required=True, label='Адрес электронной почты')

	class Meta:
		model = AdvUser
		fields = ('username', 'email', 'first_name', 'last_name', 'send_messages', 'favorite_team')

class RegisterUserForm(forms.ModelForm):
	"""Форма для регистрации нового пользователя"""		
	email = forms.EmailField(required=True, label='Адрес электронной почты')
	password1 = forms.CharField(label='Пароль', widget = forms.PasswordInput,
								help_text=password_validation.password_validators_help_text_html())
	password2 = forms.CharField(label='Пароль(Повторно)', widget = forms.PasswordInput,
								help_text='Введите пароль еще раз')

	def clean_password1(self):
		"""валидация пароля первого поля"""
		password1 = self.cleaned_data['password1']
		if password1:
			password_validation.validate_password(password1)
		return password1	

	def clean(self):
		"""Проверка на идентичность обоих паролей"""
		super().clean()
		password1 = self.cleaned_data['password1']
		password2 = self.cleaned_data['password2']
		if password1 and password2 and password1 != password2:
			errors = {'password2': ValidationError('Введенные пароли не совпадают', code='password_mismatch')}
			raise ValidationError(errors)

	def save(self, commit=True):
		"""Сохранение пользователя"""
		user = super().save(commit=False)
		user.set_password(self.cleaned_data['password1'])
		# Активный пользователь?
		user.is_active = False
		# Выполнил ли пользователь процедуру активации?
		user.is_activated = False

		if commit:
			user.save()

		# отправка сигнала для отправки письма об активации
		user_registrated.send(RegisterUserForm, instance=user)

		return user	

	class Meta:
		model = AdvUser
		fields = ('username', 'email', 'password1', 'password2', 'first_name', 
				  'last_name', 'send_messages', 'favorite_team')	


class UserCommentForm(forms.ModelForm):
	"""Форма для занесения комментариев
		зарег. пользователям"""
	class Meta:
		model = Comment
		exclude = ('is_active',)
		widgets = {'driver' : forms.HiddenInput}

class GuestCommentForm(forms.ModelForm):
	"""Форма для занесения комментариев
		гостями"""		
	captcha = CaptchaField(label='Введите текст с картинки', 
							error_messages={'invalid':'Неправилный текст'})
	class Meta:
		model = Comment
		exclude = ('is_active',)
		widgets = {'driver' : forms.HiddenInput}							
		

