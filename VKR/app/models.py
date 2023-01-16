"""
Definition of models.
"""

from django.db import models

from django.contrib.auth.models import User, Group
from datetime import timedelta

# Create your models here.

class Services (models.Model):
    id_services = models.AutoField(primary_key=True, verbose_name="ID набора сервисов")
    services = models.JSONField(null=True, verbose_name="Сервисы ОПС")

class Windows (models.Model):
    id_window = models.IntegerField(primary_key=True, verbose_name="ID окна")
    operator = models.OneToOneField(User, on_delete=models.PROTECT, null=True, verbose_name="Оператор")
    status = models.BooleanField(default=True, verbose_name="Статус окна")
    services = models.JSONField(null=True, verbose_name="Сервисы окна")

class LogWindows (models.Model):
    id_log = models.IntegerField(primary_key=True, verbose_name="ID Лога")
    window = models.ForeignKey(Windows, on_delete=models.PROTECT, verbose_name="Окно")
    operator = models.ForeignKey(User, on_delete=models.PROTECT, null=True, verbose_name="Оператор")
    time_login = models.DateTimeField(auto_now_add=True, verbose_name="Время входа")
    time_logout = models.DateTimeField(null=True, verbose_name="Время выхода")

class Tickets (models.Model):
    id_ticket = models.IntegerField(primary_key=True, verbose_name="ID талона")
    service = models.CharField(null=True, max_length=50, verbose_name="Услуга")
    status = models.CharField(null=True, max_length=50, verbose_name="Статус")
    window = models.ForeignKey(Windows, null=True, on_delete=models.PROTECT, verbose_name="Окно")
    operator = models.ForeignKey(User, on_delete=models.PROTECT, null=True, verbose_name="Оператор")
    name_ticket = models.CharField(max_length=50, verbose_name="Имя талона")
    time_create = models.DateTimeField(verbose_name="Время создания")
    time_call = models.DateTimeField(null=True, verbose_name="Время вызова")
    time_pause = models.DurationField(default=timedelta(seconds=0), verbose_name="Время пауз")
    time_close = models.DateTimeField(null=True, verbose_name="Время закрытия")

    def time_service(self):
        time_service = timedelta(0)
        if self.time_close is not None and self.time_call is not None:
            time_period = self.time_close - self.time_call
            time_service = time_period-self.time_pause
        if time_service == timedelta(seconds=0):
            time_service = None
        return time_service

class Profile(models.Model):
    operator = models.OneToOneField(User, on_delete=models.PROTECT, verbose_name="Оператор", primary_key = True)
    chief = models.BooleanField(default=False, verbose_name="Права начальника")
    status = models.BooleanField(default=False, verbose_name="Статус УЗ")