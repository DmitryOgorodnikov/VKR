"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render
from django.http import HttpRequest, HttpResponseRedirect, JsonResponse

from django.contrib.auth.decorators import login_required
from .models import Tickets, Windows, Services, Profile, LogWindows
from django.contrib.auth.models import User
from .forms import UserRegistrationForm, UserChangeForm, WindowsAuthenticationForm
from django.db.models import Avg, F
from datetime import timedelta
from django_tables2 import SingleTableView, MultiTableMixin
from django.views.generic.base import TemplateView
from django.db.models.functions import Round
from distutils.util import strtobool
from django import forms


import json
import codecs

# Страница киоска
def kiosk(request):
    assert isinstance(request, HttpRequest)
    with open('config.json', 'r', encoding='utf-8-sig') as f:
        my_json_obj = json.load(f)
        opsname = my_json_obj[0]['name']
    return render(
        request,
        'app/kiosk.html',
        {
            'title':'Киоск',
            'opsname': opsname,
        }
    )

def kioskbtn(request):
    if request.GET.get('click', False):
        serviceslist = Services.objects.latest('id_services').services
        return JsonResponse({'serviceslist':serviceslist}, status=200)

def kbutton(request):
    if request.POST.get('click', False):
        Ticket = Tickets()
        if Tickets.objects.all().exists() == False:
            Ticket.id_ticket = 0
        else:
            Ticket.id_ticket = Tickets.objects.latest("id_ticket").id_ticket + 1
        t = datetime.now().date()
        name = request.POST.get('name')
        Ticket.service = name
        name = name.split()
        if len(name) == 3:
            name = list(name[0])[0] + list(name[1])[0] + list(name[2])[0]
            if Tickets.objects.filter(time_create__contains = t).filter(name_ticket__iregex=r''+ name +'\s...').exists() == False:
                r = name + ' 001'
            else:
                r = Tickets.objects.filter(time_create__contains = t).filter(name_ticket__iregex=r''+ name +'\s...').latest("id_ticket").name_ticket
                x = int(r[-3:]) + 1
                r = r[0:3] + ' ' + str(f'{x:03}')

        elif len(name) == 2:
            name = list(name[0])[0] + list(name[1])[0]
            if Tickets.objects.filter(time_create__contains = t).filter(name_ticket__iregex=r''+ name +'\s...').exists() == False:
                r = name + ' 001'
            else:
                r = Tickets.objects.filter(time_create__contains = t).filter(name_ticket__iregex=r''+ name +'\s...').latest("id_ticket").name_ticket
                x = int(r[-3:]) + 1
                r = r[0:2] + ' ' + str(f'{x:03}')

        else:
            name = list(name[0])[0]
            if Tickets.objects.filter(time_create__contains = t).filter(name_ticket__iregex=r''+ name +'\s...').exists() == False:
                r = name + ' 001'
            else:
                r = Tickets.objects.filter(time_create__contains = t).filter(name_ticket__iregex=r''+ name +'\s...').latest("id_ticket").name_ticket
                x = int(r[-3:]) + 1
                r = r[0:1] + ' ' + str(f'{x:03}')
        Ticket.name_ticket = r
        Ticket.status = 'Выдан'
        Ticket.time_create = datetime.now()
        Ticket.save()

        with open('config.json', 'r', encoding='utf-8-sig') as f:
            my_json_obj = json.load(f)
            printcheck = my_json_obj[0]['print']

        return JsonResponse({'ticketname': r, 'printcheck': printcheck}, status=200)


def tickets(request):
    t = datetime.now().date()
    listoftickets = []
    listofticketsw = []

    if Tickets.objects.filter(time_create__contains = t).filter(window_id = None).exists():
        tickets = Tickets.objects.filter(time_create__contains = t).filter(window_id = None)
        for p in tickets:
            listoftickets.append(p.name_ticket)

    if Tickets.objects.filter(time_create__contains = t).exclude(window_id = None).filter(time_close = None).filter(status = "Вызван").exists():
        ticketsw = Tickets.objects.filter(time_create__contains = t).exclude(window_id = None).filter(time_close = None).filter(status = "Вызван")
        for p in ticketsw:
            listofticketsw.append(p.name_ticket + ' - ' + str(p.window_id))
    return JsonResponse({'listoftickets': listoftickets, 'listofticketsw': listofticketsw}, status=200)

# Основная страница
@login_required
def home(request):
    assert isinstance(request, HttpRequest)
    operator = request.user
    if operator.profile.chief == True:
        return render(
            request,
            'app/index.html',
            {
                'title':'Главное меню',
            }
        )
    else:
        return HttpResponseRedirect('./service/')


# Пульт оператора
@login_required
def service(request):
    if (Windows.objects.filter(operator = request.user).exists() != False):
        return HttpResponseRedirect('./operator/')
    else:
        form = WindowsAuthenticationForm()
        return render(
            request,
            'app/service.html',
            {
                'title':'Авторизация в пульт оператора',
                'year':datetime.now().year,
                'form': form,
            }
        )

def windowbutton(request):
    if request.GET.get('click', False):
        windows_l = []
        for l in Windows.objects.filter(operator = None).filter(status = True).values_list('id_window').order_by('id_window'):
            windows_l.append(l[0])

        return JsonResponse({"windows_l": windows_l}, status=200)

    if request.POST.get('click', False):
        window_id = request.POST.get("name")
        request.session['window_id'] = window_id
        window = Windows.objects.get(id_window = window_id)
        user = User.objects.get(username=request.user)
        window.operator = user
        window.save()
        number = LogWindows.objects.all().count()
        logwindow = LogWindows(id_log = number, window = window, operator = user)
        logwindow.time_login = datetime.now()
        logwindow.save()
        return JsonResponse({}, status=200)

@login_required
def operator(request):
    assert isinstance(request, HttpRequest)
    window_id = request.session.get('window_id')
    form = WindowsAuthenticationForm()
    return render(
        request,
        'app/operator.html',
        {
            'title':'Пульт оператора',
            'year':datetime.now().year,
            'window_id': window_id,
            'form':form,
        }
    )

@login_required
def operatorbutton(request):
    window_id = request.session.get('window_id')
    if request.GET.get('click', False):
        window = Windows.objects.get(id_window = window_id)
        window.operator_id = None
        window.save()
        logwindow = LogWindows.objects.filter(window_id = window_id).last()
        logwindow.time_logout = datetime.now()
        logwindow.save()
        request.session['window_id'] = None
        return JsonResponse({}, status=200)

@login_required
def nextbutton(request):
    t = datetime.now().date()
    #request.session['Ticket_n'] = None
    if request.POST.get('click', False):
        service = Windows.objects.get(id_window = request.session.get('window_id')).services
        services = []
        for ser in service:
            if ser['status'] == True:
                services.append(ser['rusname'])

        if (Tickets.objects.filter(time_close = None).filter(window = request.session.get('window_id')).filter(status = 'Перенаправлен')):

            if (Tickets.objects.filter(time_create__contains = t).filter(time_close = None).filter(window = request.session.get('window_id')).exists() == True) and (request.session.get('Ticket_n') != None):
                id=request.session.get('Ticket_n')
                Ticket = Tickets.objects.get(id_ticket=request.session.get('Ticket_n'))
                Ticket.time_close = datetime.now()
                Ticket.status = 'Закрыт'
                Ticket.operator = User.objects.get(id = request.user.id)
                Ticket.save()

            window_id = request.session.get('window_id')
            Ticket = Tickets.objects.filter(time_close = None).filter(window = request.session.get('window_id')).earliest('id_ticket')
            Ticket.window = Windows.objects.get(id_window=window_id)
            Ticket.time_call = datetime.now()
            Ticket.status = 'Вызван'
            Ticket.operator = User.objects.get(id = request.user.id)
            Ticket.save()
            ticket = 'Текущий талон: ' + Ticket.name_ticket
            service = 'Услуга: ' + Ticket.service
            request.session['ticket'] = ticket
            request.session['Ticket_n'] = Ticket.id_ticket

            time = Ticket.time_call
            hour = time.hour
            minute = time.minute
            second = time.second

            return JsonResponse({"ticket": ticket, 'service': service, "hour": hour, "minute": minute, "second": second}, status=200)

        elif (Tickets.objects.filter(time_create__contains = t).filter(time_close = None).filter(window = None).filter(service__in = services).exists() == False) and (Tickets.objects.filter(time_create__contains = t).filter(time_close = None).filter(window = request.session.get('window_id')).filter(service__in = services).exists() == False):
            ticket = 'Текущий талон: Нет талонов в очереди'
            service = 'Услуга:'
            request.session['ticket'] = ticket
            return JsonResponse({"ticket": ticket, 'service': service}, status=200)

        elif request.session.get('Ticket_n') is None:
            window_id = request.session.get('window_id')
            Ticket = Tickets.objects.filter(time_create__contains = t).filter(time_close = None).filter(window = None).filter(service__in = services).earliest('id_ticket')
            Ticket.window = Windows.objects.get(id_window=window_id)
            Ticket.time_call = datetime.now()
            Ticket.status = 'Вызван'
            Ticket.operator = User.objects.get(id = request.user.id)
            Ticket.save()
            ticket = 'Текущий талон: ' + Ticket.name_ticket
            service = 'Услуга: ' + Ticket.service
            request.session['ticket'] = ticket
            request.session['Ticket_n'] = Ticket.id_ticket

            time = Ticket.time_call
            hour = time.hour
            minute = time.minute
            second = time.second

            return JsonResponse({"ticket": ticket, 'service': service, "hour": hour, "minute": minute, "second": second}, status=200)


        else:
            id=request.session.get('Ticket_n')
            Ticket = Tickets.objects.get(id_ticket=request.session.get('Ticket_n'))
            Ticket.time_close = datetime.now()
            Ticket.status = 'Закрыт'
            Ticket.operator = User.objects.get(id = request.user.id)
            Ticket.save()

            if Tickets.objects.filter(time_create__contains = t).filter(time_close = None).filter(window = None).filter(service__in = services).exists() == False:
                ticket = 'Текущий талон: Нет талонов в очереди'
                service = 'Услуга:'
                request.session['ticket'] = ticket
                request.session['Ticket_n'] = None
                return JsonResponse({"ticket": ticket, 'service': service}, status=200)

            window_id = request.session.get('window_id')
            Ticket = Tickets.objects.filter(time_create__contains = t).filter(time_close = None).filter(service__in = services).filter(window = None).filter(service__in = services).earliest('id_ticket')
            Ticket.window = Windows.objects.get(id_window=window_id)
            Ticket.time_call = datetime.now()
            Ticket.status = 'Вызван'
            Ticket.operator = User.objects.get(id = request.user.id)
            Ticket.save()
            ticket = 'Текущий талон: ' + Ticket.name_ticket
            service = 'Услуга: ' + Ticket.service
            request.session['ticket'] = ticket
            request.session['Ticket_n'] = Ticket.id_ticket

            time = Ticket.time_call
            hour = time.hour
            minute = time.minute
            second = time.second

            return JsonResponse({"ticket": ticket, 'service': service, "hour": hour, "minute": minute, "second": second}, status=200)

@login_required
def cancelbutton(request):
    t = datetime.now().date()
    if request.POST.get('click', False):
        service = Windows.objects.get(id_window = request.session.get('window_id')).services
        services = []
        for ser in service:
            if ser['status'] == True:
                services.append(ser['rusname'])

        Ticket = (Tickets.objects.filter(id_ticket=request.session.get('Ticket_n')))[0]
        Ticket.time_close = datetime.now()
        Ticket.status = 'Отменен'
        Ticket.operator = User.objects.get(id = request.user.id)
        Ticket.save()

        if Tickets.objects.filter(time_create__contains = t).filter(time_close = None).filter(window = None).filter(service__in = services).exists() == False:
            ticket = 'Текущий талон: Нет талонов в очереди'
            service = 'Услуга: '
            request.session['ticket'] = ticket
            request.session['Ticket_n'] = None
            return JsonResponse({"ticket": ticket, 'service': service}, status=200)

        window_id = request.session.get('window_id')
        Ticket = Tickets.objects.filter(time_create__contains = t).filter(time_close = None).filter(window = None).filter(service__in = services).earliest('id_ticket')
        Ticket.window = Windows.objects.get(id_window=window_id)
        Ticket.time_call = datetime.now()
        Ticket.status = 'Вызван'
        Ticket.operator = User.objects.get(id = request.user.id)
        Ticket.save()
        ticket = 'Текущий талон: ' + Ticket.name_ticket
        service = 'Услуга: ' + Ticket.service
        request.session['ticket'] = ticket
        request.session['Ticket_n'] = Ticket.id_ticket

        time = Ticket.time_call
        hour = time.hour
        minute = time.minute
        second = time.second

        return JsonResponse({"ticket": ticket, 'service': service, "hour": hour, "minute": minute, "second": second}, status=200)

@login_required
def breakbutton(request):
    if request.POST.get('click', False):

        Ticket = (Tickets.objects.filter(id_ticket=request.session.get('Ticket_n')))[0]
        Ticket.time_close = datetime.now()
        Ticket.status = 'Закрыт'
        Ticket.operator = User.objects.get(id = request.user.id)
        Ticket.save()
        ticket = 'Текущий талон: Перерыв'
        service = 'Услуга: '

        time = Ticket.time_close
        hour = time.hour
        minute = time.minute
        second = time.second

        return JsonResponse({"ticket": ticket, 'service': service, "hour": hour, "minute": minute, "second": second}, status=200)

@login_required
def delaybutton(request):
    t = datetime.now().date()
    if request.POST.get('click', False):
        service = Windows.objects.get(id_window = request.session.get('window_id')).services
        services = []
        for ser in service:
            if ser['status'] == True:
                services.append(ser['rusname'])

        Ticket = (Tickets.objects.filter(id_ticket=request.session.get('Ticket_n')))[0]
        Ticket.status = 'Отложен'
        ticket_r = Ticket.name_ticket
        Ticket.save()

        if Tickets.objects.filter(time_create__contains = t).filter(time_close = None).filter(window = None).filter(service__in = services).exists() == False:
            ticket = 'Текущий талон: Нет талонов в очереди'
            service = 'Услуга: '
            request.session['ticket'] = ticket
            request.session['Ticket_n'] = None
            return JsonResponse({"ticket": ticket, 'service': service, "ticket_r": ticket_r}, status=200)

        window_id = request.session.get('window_id')
        Ticket = Tickets.objects.filter(time_create__contains = t).filter(time_close = None).filter(window = None).filter(service__in = services).earliest('id_ticket')
        Ticket.window = Windows.objects.get(id_window=window_id)
        Ticket.time_call = datetime.now()
        Ticket.status = 'Вызван'
        Ticket.operator = User.objects.get(id = request.user.id)
        Ticket.save()
        ticket = 'Текущий талон: ' + Ticket.name_ticket
        service = 'Услуга: ' + Ticket.service
        request.session['ticket'] = ticket
        request.session['Ticket_n'] = Ticket.id_ticket

        time = Ticket.time_call
        hour = time.hour
        minute = time.minute
        second = time.second

        return JsonResponse({"ticket": ticket, 'service': service, "hour": hour, "minute": minute, "second": second, "ticket_r": ticket_r}, status=200)

@login_required
def returnbutton(request):
    t = datetime.now().date()
    if request.POST.get('click', False):
        service = Windows.objects.get(id_window = request.session.get('window_id')).services
        services = []
        for ser in service:
            if ser['status'] == True:
                services.append(ser['rusname'])

        window_id = request.session.get('window_id')
        Ticket = Tickets.objects.filter(status = 'Отложен').filter(window = window_id).earliest('id_ticket')
        Ticket.time_pause += datetime.now() - Ticket.time_call.replace(tzinfo=None)
        Ticket.time_call = datetime.now()
        Ticket.status = 'Вызван'
        Ticket.save()
        ticket = 'Текущий талон: ' + Ticket.name_ticket
        service = 'Услуга: ' + Ticket.service
        request.session['ticket'] = ticket
        request.session['Ticket_n'] = Ticket.id_ticket

        time = Ticket.time_call
        hour = time.hour
        minute = time.minute
        second = time.second

        return JsonResponse({"ticket": ticket, 'service': service, "hour": hour, "minute": minute, "second": second}, status=200)

@login_required
def redirectbutton(request):
    if request.POST.get('click', False):
        windows_l = []
        for l in Windows.objects.exclude(id_window = None).exclude(id_window = request.session.get('window_id')).values_list('id_window').order_by('id_window'):
            windows_l.append(l[0])

        return JsonResponse({"windows_l": windows_l}, status=200)

@login_required
def redbutton(request):
    t = datetime.now().date()
    red_window_id = request.POST.get("name")
    if request.POST.get('click', False):
        service = Windows.objects.get(id_window = request.session.get('window_id')).services
        services = []
        for ser in service:
            if ser['status'] == True:
                services.append(ser['rusname'])

        id=request.session.get('Ticket_n')
        Ticket = Tickets.objects.get(id_ticket=request.session.get('Ticket_n'))
        Ticket.window = Windows.objects.get(id_window=red_window_id)
        Ticket.status = 'Перенаправлен'
        Ticket.save()

        if Tickets.objects.filter(time_create__contains = t).filter(time_close = None).filter(window = None).filter(service__in = services).exists() == False:
            ticket = 'Текущий талон: Нет талонов в очереди'
            service = 'Услуга:'
            request.session['ticket'] = ticket
            request.session['Ticket_n'] = None
            return JsonResponse({"ticket": ticket, 'service': service}, status=200)

        window_id = request.session.get('window_id')
        Ticket = Tickets.objects.filter(time_create__contains = t).filter(time_close = None).filter(service__in = services).filter(window = None).filter(service__in = services).earliest('id_ticket')
        Ticket.window = Windows.objects.get(id_window=window_id)
        Ticket.time_call = datetime.now()
        Ticket.status = 'Вызван'
        Ticket.operator = User.objects.get(id = request.user.id)
        Ticket.save()
        ticket = 'Текущий талон: ' + Ticket.name_ticket
        service = 'Услуга: ' + Ticket.service
        request.session['ticket'] = ticket
        request.session['Ticket_n'] = Ticket.id_ticket

        time = Ticket.time_call
        hour = time.hour
        minute = time.minute
        second = time.second

        return JsonResponse({"ticket": ticket, 'service': service, "hour": hour, "minute": minute, "second": second}, status=200)


# Статистика
@login_required
def statistics(request):
    assert isinstance(request, HttpRequest)
    with open('config.json', 'r', encoding='utf-8-sig') as f:
        my_json_obj = json.load(f)
        opsname = my_json_obj[0]['name']
    return render(
        request,
        'app/statistics.html',
        {
            'title':'Лог Талонов',
            'opsname': opsname,
            'year':datetime.now().year,
        }
    )

@login_required
def statisticstable(request):
    if request.GET.get('click', False):
        t = datetime.now().date()
        listoftickets = []
        tickets = Tickets.objects.filter(time_create__contains = t).order_by('id_ticket')
        for p in tickets:
            tc = p.time_create.time().strftime("%H:%M:%S")

            if p.time_call == None:
                tca = ''
            else:
                tca = p.time_call.time().strftime("%H:%M:%S")

            if p.time_close == None:
                tcl = ''
            else:
                tcl = p.time_close.time().strftime("%H:%M:%S")

            if p.window_id == None:
                iw = ''
            else:
                iw = p.window_id

            if p.operator == None:
                op = ''
            else:
                op = p.operator.last_name +' ('+ p.operator.username +')'

            listoftickets.append([p.name_ticket, p.service, p.status, tc, tca, tcl, iw, op])
        return JsonResponse({'listoftickets': listoftickets}, status=200)

    if request.GET.get('click2', False):
        date = request.GET.get('date').split(', ')
        date[1] = str(int(date[1]) + 1)
        date = ("-".join(date))
        date = (datetime.strptime(date, "%Y-%m-%d")).date()
        listoftickets = []
        tickets = Tickets.objects.filter(time_create__contains = date).order_by('id_ticket')
        for p in tickets:
            tc = p.time_create.time().strftime("%H:%M:%S")

            if p.time_call == None:
                tca = ''
            else:
                tca = p.time_call.time().strftime("%H:%M:%S")

            if p.time_close == None:
                tcl = ''
            else:
                tcl = p.time_close.time().strftime("%H:%M:%S")

            if p.window_id == None:
                iw = ''
            else:
                iw = p.window_id

            if p.operator == None:
                op = ''
            else:
                op = p.operator.last_name +' ('+ p.operator.username +')'

            listoftickets.append([p.name_ticket, p.service, p.status, tc, tca, tcl, iw, op])
        return JsonResponse({'date': date, 'listoftickets': listoftickets}, status=200)

@login_required
def statisticsw(request):
    assert isinstance(request, HttpRequest)
    with open('config.json', 'r', encoding='utf-8-sig') as f:
        my_json_obj = json.load(f)
        opsname = my_json_obj[0]['name']
    return render(
        request,
        'app/statisticsw.html',
        {
            'title':'Статистика по окнам',
            'opsname': opsname,
            'year':datetime.now().year,
        }
    )

@login_required
def statisticstablew(request):
    if request.GET.get('click', False):
        t = datetime.now().date()
        listoflogwindows = []
        logwindow = LogWindows.objects.filter(time_login__contains = t).order_by('id_log')
        for p in logwindow:
            tlogin = p.time_login.time().strftime("%H:%M:%S")

            if p.time_logout == None:
                tlogout = ''
                tservice = ''
            else:
                tlogout = p.time_logout.time().strftime("%H:%M:%S")
                tservice = (datetime.min + (p.time_logout - p.time_login)).time().strftime("%H:%M:%S")
            listoflogwindows.append([p.window_id,p.operator.last_name + ' (' + p.operator.username + ')', tlogin, tlogout, tservice])
        return JsonResponse({'listoflogwindows': listoflogwindows}, status=200)

    if request.GET.get('click2', False):
        date = request.GET.get('date').split(', ')
        date[1] = str(int(date[1]) + 1)
        date = ("-".join(date))
        date = (datetime.strptime(date, "%Y-%m-%d")).date()
        listoflogwindows = []
        logwindow = LogWindows.objects.filter(time_login__contains = date).order_by('id_log')
        for p in logwindow:
            tlogin = p.time_login.time().strftime("%H:%M:%S")

            if p.time_logout == None:
                tlogout = ''
                tservice = ''
            else:
                tlogout = p.time_logout.time().strftime("%H:%M:%S")
                tservice = (datetime.min + (p.time_logout - p.time_login)).time().strftime("%H:%M:%S")
            listoflogwindows.append([p.window_id,p.operator.last_name + ' (' + p.operator.username + ')', tlogin, tlogout, tservice])
        return JsonResponse({'date': date, 'listoflogwindows': listoflogwindows}, status=200)

@login_required
def statisticsall(request):
    assert isinstance(request, HttpRequest)
    with open('config.json', 'r', encoding='utf-8-sig') as f:
        my_json_obj = json.load(f)
        opsname = my_json_obj[0]['name']
    return render(
        request,
        'app/statisticsall.html',
        {
            'title':'Статистика за год',
            'opsname': opsname,
            'year':datetime.now().year,
        }
    )

@login_required
def statisticstableall(request):
    if request.GET.get('click', False):

        service = Services.objects.latest('id_services').services
        services = []
        for ser in service:
            if ser['status'] == True:
                services.append(ser['rusname'])
        t = datetime.now().date()
        select_time = '2023'
        nt = []
        nt.append (Tickets.objects.filter(time_create__year = select_time).filter(time_create__month = '01').count())
        nt.append (Tickets.objects.filter(time_create__year = select_time).filter(time_create__month = '02').count())
        nt.append (Tickets.objects.filter(time_create__year = select_time).filter(time_create__month = '03').count())
        nt.append (Tickets.objects.filter(time_create__year = select_time).filter(time_create__month = '04').count())
        nt.append (Tickets.objects.filter(time_create__year = select_time).filter(time_create__month = '05').count())
        nt.append (Tickets.objects.filter(time_create__year = select_time).filter(time_create__month = '06').count())
        nt.append (Tickets.objects.filter(time_create__year = select_time).filter(time_create__month = '07').count())
        nt.append (Tickets.objects.filter(time_create__year = select_time).filter(time_create__month = '08').count())
        nt.append (Tickets.objects.filter(time_create__year = select_time).filter(time_create__month = '09').count())
        nt.append (Tickets.objects.filter(time_create__year = select_time).filter(time_create__month = '10').count())
        nt.append (Tickets.objects.filter(time_create__year = select_time).filter(time_create__month = '11').count())
        nt.append (Tickets.objects.filter(time_create__year = select_time).filter(time_create__month = '12').count())
        
        stc = []
        stat = []
        for s in services:
           stc.append (Tickets.objects.filter(time_create__contains = select_time).filter(service=s).count())
           temp = Tickets.objects.filter(time_create__contains = select_time).filter(service=s).aggregate(average_difference=Avg(F('time_close') - F('time_call')))
           if temp.get('average_difference') == None:
               stat.append (0)
           else:
               stat.append (temp.get('average_difference').seconds)
               if temp.get('average_difference').microseconds > 500000:
                   stat[0] += 1

        return JsonResponse({'nt': nt, 'stc': stc, 'services': services, 'stat': stat}, status=200)


# Настройки
@login_required
def settings(request):
    assert isinstance(request, HttpRequest)
    with open('config.json', 'r', encoding='utf-8-sig') as f:
        my_json_obj = json.load(f)
        opsname = my_json_obj[0]['name']
    return render(
        request,
        'app/settings.html',
        {
            'title':'Операторы',
            'year':datetime.now().year,
            'opsname': opsname,
        }
    )

def delbutton(request):
    if request.POST.get('click', False):
        Userdel = (User.objects.filter(id=request.POST.get('idbutton')))[0]
        Userdel.is_active = False
        Userdel.save()

        return JsonResponse({}, status=200)

@login_required
def edituser(request):
    if request.POST.get('click', False):
        Useredit = (User.objects.filter(id=request.POST.get('idbutton')))[0]

        request.session['useredit'] = Useredit.id
        return JsonResponse({}, status=200)

@login_required
def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            new_profile = Profile.objects.create(operator=new_user)
            new_profile.chief = user_form.cleaned_data['chief']
            new_profile.save()
            return HttpResponseRedirect('../settings')
    else:
        user_form = UserRegistrationForm()
    head = 'Создание нового аккаунта'
    subhead = 'Пожалуйста, зарегистрируйте нового пользователя, используя нижеуказанную форму'
    namebutton = 'Создать'
    return render(
        request,
        'app/register.html',
        {
            'title':'Регистрация пользователя',
            'user_form': user_form,
            'head': head, 'subhead': subhead, 
            'namebutton': namebutton, 
            'year':datetime.now().year,
        }
    )

@login_required
def editer(request):
    Useredit = User.objects.filter(id = request.session.get('useredit'))[0]
    if request.method == 'POST':
        user_form = UserChangeForm(request.POST, instance=Useredit)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            if user_form.cleaned_data['password'] != '':
                new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            if Profile.objects.get(operator=new_user) != None:
                new_profile = Profile.objects.get(operator=new_user)
            else:
                new_profile = Profile.objects.create(operator=new_user)
            new_profile.chief = user_form.cleaned_data['chief']
            new_profile.save()
            del request.session['useredit']
            return HttpResponseRedirect('/settings')
    else:
        user_form = UserChangeForm(instance=Useredit)
    user_form.initial.update({'chief':Useredit.profile.chief})
    head = 'Редактирование аккаунта'
    subhead = 'Пожалуйста, измените данные пользователя, используя нижеуказанную форму'
    namebutton = 'Изменить'
    return render(
        request,
        'app/register.html',
        {
            'title':'Изменение пользователя',
            'user_form': user_form,
            'head': head, 'subhead': subhead, 
            'namebutton': namebutton, 
            'year':datetime.now().year,
        }
    )

@login_required
def settingstable(request):
    if request.POST.get('click', False):
        user = []
        users = User.objects.exclude(username = 'admin').exclude(is_active = False)
        for p in users:
            user.append([p.id, p.username, p.last_name])

        return JsonResponse({"user": user}, status=200)

@login_required
def settingsw(request):
    assert isinstance(request, HttpRequest)
    with open('config.json', 'r', encoding='utf-8-sig') as f:
        my_json_obj = json.load(f)
        opsname = my_json_obj[0]['name']
    return render(
        request,
        'app/settingsw.html',
        {
            'title':'Окна',
            'year':datetime.now().year,
            'opsname':opsname,
        }
    )

@login_required
def settingswtable(request):
    if request.GET.get('click', False):
        window = []
        windows = Windows.objects.all().order_by("id_window")
        for p in windows:
            if p.operator == None:
                operator = ''
            else:
                operator = p.operator.username
            window.append([p.id_window, p.status, operator])

        return JsonResponse({"window": window}, status=200)

@login_required
def addwindow(request):
    if request.POST.get('click', False):
        number = Windows.objects.all().count()
        window = Windows(id_window = number+1, services = Services.objects.latest('id_services').services)
        window.save()
        return JsonResponse({}, status=200)

@login_required
def windowreset(request):
    if request.POST.get('click', False):
        window = Windows.objects.get(id_window = request.POST.get('idwindow'))
        logwindow = LogWindows.objects.filter(operator = window.operator).last()
        logwindow.time_logout = datetime.now()
        logwindow.save()
        window.operator = None
        window.save()
        return JsonResponse({}, status=200)

@login_required
def changestatusw(request):
    if request.POST.get('click', False):
        window = Windows.objects.get(id_window = request.POST.get('idwindow'))
        if window.status is True:
            window.status = False
        else:
            window.status = True
        window.save()
        return JsonResponse({}, status=200)

@login_required
def changeservicew(request):
    if request.POST.get('click', False):
        assert isinstance(request, HttpRequest)
        idwindow = request.POST.get('idwindow')
        request.session['idwindow'] = idwindow
        return JsonResponse({}, status=200)

@login_required
def settingswchange(request):
    if request.POST.get('click', False):
        idwindow = request.session.get('idwindow')
    else:
        idwindow = request.session.get('idwindow')
        assert isinstance(request, HttpRequest)
        return render(
            request,
            'app/settingswchange.html',
            {
                'title':'Услуги окна',
                'year':datetime.now().year,
                'idwindow':idwindow,
            }
        )

@login_required
def servicestable(request):
    if request.GET.get('click', False):
        idwindow = request.session.get('idwindow')
        serviceslist = Windows.objects.get(id_window = idwindow).services
        return JsonResponse({'serviceslist':serviceslist}, status=200)
    if request.GET.get('click2', False):
        serviceslist = Services.objects.latest('id_services').services
        return JsonResponse({'serviceslist':serviceslist}, status=200)

@login_required
def wchange(request):
    if request.GET.get('click', False):
        listofcheck = request.GET.get('listofcheck')
        listofcheck = listofcheck.split()
        window = Windows.objects.get(id_window = request.session.get('idwindow'))
        i = 0
        for p in listofcheck:
            window.services[i]['status'] = (p == 'true')
            i += 1
        window.save()
        return JsonResponse({}, status=200)

    if request.POST.get('click2', False):
        listofcheck = request.POST.get('listofcheck')
        listofcheck = listofcheck.split()
        service = Services.objects.latest('id_services')
        i = 0
        for p in listofcheck:
            service.services[i]['status'] = (p == 'true')
            i += 1
        listofservices = json.dumps(service.services, ensure_ascii=False)
        with codecs.open("services.json", "w", "utf-8-sig") as temp:
            temp.write(listofservices)
            temp.close()
        service.save()
        ls = service.services
        for s in ls:
            if s['status'] == False:
                ls.remove(s)
        Window = Windows.objects.all()
        for i in Window:
            if len(i.services) != len(ls):
                i.services = ls
                i.save()
        return JsonResponse({}, status=200)

@login_required
def settingso(request):
    assert isinstance(request, HttpRequest)
    with open('config.json', 'r', encoding='utf-8-sig') as f:
        my_json_obj = json.load(f)
        opsname = my_json_obj[0]['name']
    return render(
        request,
        'app/settingso.html',
        {
            'title':'Услуги ОПС',
            'year':datetime.now().year,
            'opsname':opsname,
        }
    )

@login_required
def settingsm(request):
    if request.GET.get('click1', False):
        with open('config.json', 'r', encoding='utf-8-sig') as f:
            my_json_obj = json.load(f)
            opsname = my_json_obj[0]['name']
            printcheck = my_json_obj[0]['print']
        return JsonResponse({'opsname':opsname, 'printcheck':printcheck }, status=200)
    
    if request.POST.get('click2', False):
        listofsettings = request.POST.get('listofsettings')
        listofsettings = listofsettings.split()
        with open('config.json', 'r', encoding='utf-8-sig') as f:
            my_json_obj = json.load(f)
            if my_json_obj[0]['name'] != listofsettings[0]:
                my_json_obj[0]['name'] = listofsettings[0]
            if my_json_obj[0]['print'] != strtobool(listofsettings[1]):
                my_json_obj[0]['print'] = strtobool(listofsettings[1])
        my_json_obj = json.dumps(my_json_obj, ensure_ascii=False)
        with codecs.open("config.json", "w", "utf-8-sig") as temp:
            temp.write(my_json_obj)
            temp.close()
        return JsonResponse({}, status=200)

    else:
        assert isinstance(request, HttpRequest)
        with open('config.json', 'r', encoding='utf-8-sig') as f:
            my_json_obj = json.load(f)
            opsname = my_json_obj[0]['name']
        return render(
            request,
            'app/settingsm.html',
            {
                'title':'Окна',
                'year':datetime.now().year,
                'opsname':opsname,
            }
    )



