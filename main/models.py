from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import Signal

from .utilities import send_activation_notification, get_timestamp_path

from django_countries.fields import CountryField



class AdvUser(AbstractUser):
	"""Пользователь"""
	is_activated = models.BooleanField(default=True, db_index=True, verbose_name='Прошел активацию?')
	send_messages = models.BooleanField(default=True, verbose_name = 'Оповещать о новых комментариях?')

	TEAMS = ( 	('Mercedes', 'Mercedes'),
				('Ferrari', 'Ferrari'),
				('Red Bull Racing', 'Red Bull Racing'),
				('Racing Point', 'Racing Point'),
				('Mclaren', 'Mclaren'),
				('Renault', 'Renault'),
				('Haas', 'Haas'),
				('Alfa Tauri', 'Alfa Tauri'),
				('Alfa Romeo', 'Alfa Romeo'),
				('Williams', 'Williams') )

	favorite_team = models.CharField(default=True, max_length=20, choices=TEAMS, 
									 verbose_name = 'Любимая команда' )

	class Meta(AbstractUser.Meta):
		pass

# Сигнал для отправки эл.писем
user_registrated = Signal(providing_args=['instance'])

def user_registrated_dispatcher(sender, **kwargs):
	"""Обработчик сигнала"""
	send_activation_notification(kwargs['instance'])

user_registrated.connect(user_registrated_dispatcher)


class Driver(models.Model):
	"""Пилот"""
	first_name = models.CharField(max_length=20, verbose_name='Имя')
	last_name = models.CharField(max_length=20, verbose_name='Фамилия')
	date_of_birth = models.DateField(verbose_name='Дата рождения')
	country = models.CharField(max_length=30, verbose_name='Страна')  
	image = models.ImageField(blank=True, upload_to=get_timestamp_path, verbose_name='Фото')
	is_active = models.BooleanField(default=True, db_index=True, verbose_name='Действующий пилот?')
	team = models.ForeignKey('Team', on_delete=models.PROTECT, verbose_name='Команда',
								null=True, blank=True)
	biography = models.TextField(default=True, verbose_name='Биография')
	starts = models.IntegerField(default=True, verbose_name='Кол-во стартов')
	wins = models.IntegerField(default=True, verbose_name='Кол-во побед')
	pole_position= models.IntegerField(default=True, verbose_name='Кол-во поулов')
	scores = models.IntegerField(default=True, verbose_name='Кол-во очков')
	podiums= models.IntegerField(default=True, verbose_name='Кол-во подиумов')
	best_laps= models.IntegerField(default=True, verbose_name='Кол-во лучших кругов')
	championship_win = models.IntegerField(default=True, verbose_name='Побед в чемпионате')


	def __str__(self):
		return self.first_name 

	class Meta:
		verbose_name = 'Пилот'
		verbose_name_plural = 'Пилоты'

class Team(models.Model):
	"""Команда"""
	name = models.CharField(max_length=20, verbose_name='Название')
	debut_in_f1 = models.DateField(verbose_name='Дебют в Ф1')
	country = models.CharField(max_length=30, verbose_name='Страна')  
	image = models.ImageField(blank=True, upload_to=get_timestamp_path, verbose_name='Фото')
	is_active = models.BooleanField(default=True, db_index=True, verbose_name='Действующая команда')
	team_history =models.TextField(default=True, verbose_name='История команды')
	starts = models.IntegerField(default=True, verbose_name='Кол-во стартов')
	wins = models.IntegerField(default=True, verbose_name='Кол-во побед')
	pole_position= models.IntegerField(default=True, verbose_name='Кол-во поулов')
	scores = models.IntegerField(default=True, verbose_name='Кол-во очков')
	podiums= models.IntegerField(default=True, verbose_name='Кол-во подиумов')
	best_laps= models.IntegerField(default=True, verbose_name='Кол-во лучших кругов')
	constructors_win = models.IntegerField(default=True, verbose_name='Побед в Кубке конструкторов')

	
	def __str__(self):
		return self.name

	class Meta:
		verbose_name = 'Команда'
		verbose_name_plural = 'Команды'

class Track(models.Model):
	"""Трасса"""
	name = models.CharField(max_length=30, verbose_name='Название')
	build = models.DateField(verbose_name='Построена')
	located = models.CharField(max_length=30, verbose_name='Расположение')
	image = models.ImageField(blank=True, upload_to=get_timestamp_path, verbose_name='Фото')
	is_active = models.BooleanField(default=True, db_index=True, verbose_name='Действующая трасса')
	length = models.IntegerField(verbose_name='Длина трассы')
	width = models.IntegerField(verbose_name='Ширина трассы')

	DRIVE = ( 	('По часовой стрелке', 'По часовой стрелке'),
				('Против часовой стрелки', 'Против часовой стрелки')
			)
	drive = models.CharField(default=True, max_length=30, choices=DRIVE, 
									 verbose_name = 'Движение' )
	number_of_turns = models.IntegerField(verbose_name='Количество поворотов')
	record = models.TimeField(verbose_name='Рекорд круга')
	flag = models.ImageField(blank=True, upload_to=get_timestamp_path, verbose_name='Флаг')

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = 'Трасса'
		verbose_name_plural = 'Трассы'
		

		


