# Generated by Django 4.1.5 on 2023-01-09 10:02

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('operator', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL, verbose_name='Оператор')),
                ('chief', models.BooleanField(default=False, verbose_name='Права начальника')),
            ],
        ),
        migrations.CreateModel(
            name='Services',
            fields=[
                ('id_services', models.IntegerField(primary_key=True, serialize=False, verbose_name='ID набора сервисов')),
                ('services', models.JSONField(null=True, verbose_name='Сервисы ОПС')),
            ],
        ),
        migrations.CreateModel(
            name='Windows',
            fields=[
                ('id_window', models.IntegerField(primary_key=True, serialize=False, verbose_name='ID окна')),
                ('status', models.BooleanField(default=True, verbose_name='Статус окна')),
                ('services', models.JSONField(null=True, verbose_name='Сервисы окна')),
                ('id_operator', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='ID оператора')),
            ],
        ),
        migrations.CreateModel(
            name='Tickets',
            fields=[
                ('id_ticket', models.IntegerField(primary_key=True, serialize=False, verbose_name='ID талона')),
                ('status', models.CharField(max_length=50, null=True, verbose_name='Статус')),
                ('operator', models.CharField(max_length=200, null=True, verbose_name='Оператор')),
                ('name_ticket', models.CharField(max_length=50, verbose_name='Имя талона')),
                ('time_create', models.DateTimeField(verbose_name='Время создания')),
                ('time_call', models.DateTimeField(null=True, verbose_name='Время вызова')),
                ('time_pause', models.DurationField(default=datetime.timedelta(0), verbose_name='Время пауз')),
                ('time_close', models.DateTimeField(null=True, verbose_name='Время закрытия')),
                ('id_window', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='app.windows', verbose_name='Окно')),
            ],
        ),
        migrations.CreateModel(
            name='LogWindows',
            fields=[
                ('id_log', models.IntegerField(primary_key=True, serialize=False, verbose_name='ID Лога')),
                ('operator', models.CharField(max_length=50, null=True, verbose_name='Оператор')),
                ('time_login', models.DateTimeField(auto_now_add=True, verbose_name='Время входа')),
                ('time_logout', models.DateTimeField(null=True, verbose_name='Время выхода')),
                ('window', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='app.windows', verbose_name='Окно')),
            ],
        ),
    ]
