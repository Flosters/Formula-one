# Generated by Django 3.0.6 on 2020-09-21 12:38

from django.db import migrations, models
import main.utilities


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_auto_20200920_1601'),
    ]

    operations = [
        migrations.CreateModel(
            name='Track',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='Название')),
                ('build', models.DateField(max_length=8, verbose_name='Построена')),
                ('located', models.CharField(max_length=30, verbose_name='Расположение')),
                ('image', models.ImageField(blank=True, upload_to=main.utilities.get_timestamp_path, verbose_name='Фото')),
                ('is_active', models.BooleanField(db_index=True, default=True, verbose_name='Действующая трасса')),
                ('length', models.IntegerField(verbose_name='Длина трассы')),
                ('width', models.IntegerField(verbose_name='Ширина трассы')),
                ('drive', models.CharField(choices=[('По часовой стрелке', 'По часовой стрелке'), ('Против часовой стрелки', 'Против часовой стрелки')], default=True, max_length=30, verbose_name='Движение')),
                ('number_of_turns', models.IntegerField(verbose_name='Количество поворотов')),
                ('record', models.TimeField(verbose_name='Рекорд круга')),
            ],
        ),
    ]