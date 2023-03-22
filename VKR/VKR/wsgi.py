"""
WSGI config for VKR project.

This module contains the WSGI application used by Django's development server
and any production WSGI deployments. It should expose a module-level variable
named ``application``. Django's ``runserver`` and ``runfcgi`` commands discover
this application via the ``WSGI_APPLICATION`` setting.

Usually you will have the standard Django WSGI application here, but it also
might make sense to replace the whole Django WSGI application with a custom one
that later delegates to the Django one. For example, you could introduce WSGI
middleware here, or combine a Django application with an application of another
framework.

For more information, visit
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application
from app.models import Windows, Services, Tickets, LogWindows
from datetime import datetime
import json

os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    'VKR.settings')

with open('services.json', 'r', encoding='utf-8-sig') as f:
    my_json_obj = json.load(f)

    if Services.objects.all().exists() != False:
        lastserv = Services.objects.latest('id_services').services
    else:
        lastserv = ''
    if lastserv != my_json_obj:
        service = Services (services=my_json_obj)
        service.save()
        ls = service.services
        for s in ls:
            keys = list(s.keys())
            if s[keys[0]] == False:
                ls.remove(s)
        Window = Windows.objects.all()
        for i in Window:
            i.services = ls
            i.save()


t = datetime.now().date()
tt = datetime.now()

if Tickets.objects.exclude(time_create__contains = t).filter(time_close = None).exists() != False:
    ticketslist = Tickets.objects.exclude(time_create__contains = t).filter(time_close = None)
    for t in ticketslist:
        t.status = 'Истек'
        tm = datetime.now()
        tm = t.time_create
        tm = tm.replace(hour=23,minute=59,second=59,microsecond=0)
        t.time_close = tm
        t.save()

if LogWindows.objects.exclude(time_login__contains = t).filter(time_logout = None).exists() != False:
    logwindowslist = LogWindows.objects.exclude(time_login__contains = t).filter(time_logout = None)
    for l in logwindowslist:
        l.time_logout = l.time_login.replace(hour=23,minute=59,second=59,microsecond=0)
        l.save()
        newses = LogWindows.objects.create(id_log = LogWindows.objects.all().count(), operator_id = l.operator_id, window_id = l.window_id, time_login = tt)




# This application object is used by any WSGI server configured to use this
# file. This includes Django's development server, if the WSGI_APPLICATION
# setting points here.
application = get_wsgi_application()
