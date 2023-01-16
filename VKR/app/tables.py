# tables.py
import django_tables2 as tables
from .models import Tickets
from datetime import timedelta
from django.db.models import F, DurationField, ExpressionWrapper
from django.db.models.functions import Coalesce
from django.contrib.auth.models import User

class TicketsTable(tables.Table):
    service = tables.Column(verbose_name= "Время обслуживания")
    class Meta:
        model = Tickets
        template_name = "django_tables2/bootstrap.html"
        fields = ("id_ticket","id_window_id","name_ticket","time_create","time_call","time_pause","time_close","service")
    
    def order_service(self, queryset, is_descending):
        service = timedelta(0)
        queryset = queryset.annotate(service = ExpressionWrapper(timedelta(0)+F("time_close")-F("time_call")-F("time_pause"), output_field=DurationField())).order_by('-service').exclude(service = None)
        return (queryset, True)

class TicketsTableCentral(tables.Table):
    class Meta:
        model = Tickets
        template_name = "django_tables2/bootstrap.html"
        fields = ("name_ticket","id_window_id")