#Представления
from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Tickets, Windows, Services, Profile, LogWindows
from django.contrib.auth.models import User
from .forms import UserRegistrationForm, UserChangeForm, WindowsAuthenticationForm
from django.db.models import Avg, F
from datetime import timedelta
from distutils.util import strtobool
from django.contrib.sessions.models import Session
import json
import codecs
import re

# Страница киоска
def kiosk(request):
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

# Возвращет список услуг для генерации кнопок на странице киоска
def kioskbtn(request):
    if request.GET.get('click', False):
        serviceslist = Services.objects.latest('id_services').services
        return JsonResponse({'serviceslist':serviceslist}, status=200)

# Создает талон после нажатия кнопки услуги
def kbutton(request):
    if request.POST.get('click', False):
        Ticket = Tickets()
        if Tickets.objects.all().exists() == False:
            Ticket.id_ticket = 0
        else:
            Ticket.id_ticket = Tickets.objects.latest("id_ticket").id_ticket + 1
        t = datetime.now().date()
        name = request.POST.get('name')
        Ticket.service = name.split(' - ')[-1]
        name = name.split(' - ')[0]
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

# Возвращает список талонов для центрального табло
def tickets(request):
    t = datetime.now().date()
    listoftickets = []
    listofticketsw = []
    if Tickets.objects.filter(time_create__contains = t).filter(window_id = None).exists():
        tickets = Tickets.objects.filter(time_create__contains = t).filter(window_id = None).order_by('-time_create')
        for p in tickets:
            listoftickets.append(p.name_ticket)
    if Tickets.objects.filter(time_create__contains = t).exclude(window_id = None).filter(time_close = None).filter(status = "Вызван").exists():
        ticketsw = Tickets.objects.filter(time_create__contains = t).exclude(window_id = None).filter(time_close = None).filter(status = "Вызван").order_by('time_create')
        for p in ticketsw:
            listofticketsw.append(p.name_ticket + ' - ' + str(p.window_id))
    return JsonResponse({'listoftickets': listoftickets, 'listofticketsw': listofticketsw}, status=200)

# Возвращает талон для вызова
def ticketscall(request):
    t = datetime.now()
    if Tickets.objects.filter(time_create__contains = t.date()).exclude(window_id = None).filter(time_call__gt = t - timedelta(seconds=10)).exists():
       ticketsc = Tickets.objects.filter(time_create__contains = t.date()).exclude(window_id = None).filter(time_call__gt = t - timedelta(seconds=10))
       ticketc = ticketsc.earliest('time_call')
       jsonticket = json.dumps({ticketc.name_ticket: str(ticketc.window_id)})
       return JsonResponse({ticketc.name_ticket.replace(' ', ''): str(ticketc.window_id)}, status=200)
    else:
       return JsonResponse({}, status=200)


# Главное меню
@login_required
def home(request):
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


# Страница выбора окна
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

# Принимает выбранное окно и прописывает пользователя в нем и в логе окон
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

# Пульт оператора
@login_required
def operator(request):
    window_id = Windows.objects.get(operator = request.user).id_window
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

# Функция, что закрывает сессию пользователя на окне, если она есть.
@login_required
def operatorbutton(request):
    window_id = request.session.get('window_id')
    if request.GET.get('click', False):
        if Windows.objects.filter(operator = request.user).exists():
            window = Windows.objects.get(operator = request.user)
            window.operator_id = None
            window.save()
            logwindow = LogWindows.objects.filter(window_id = window.id_window).last()
            logwindow.time_logout = datetime.now()
            logwindow.save()
            if Tickets.objects.filter(window_id=window.id_window).filter(time_close = None).exists():
                Ticket = Tickets.objects.get(window_id=window.id_window, time_close = None)
                Ticket.time_close = datetime.now()
                Ticket.status = 'Закрыт'
                Ticket.save()
            request.session['window_id'] = None
        return JsonResponse({}, status=200)

# Кнопка "Следующий"
@login_required
def nextbutton(request):
    t = datetime.now().date()
    window_id = request.session.get('window_id')
    if request.POST.get('click', False):
        service = Windows.objects.get(operator = request.user).services
        services = []
        for ser in service:
            if len(list(ser.keys())) > 1:
                if ser[list(ser.keys())[1]] == True:
                    services.append(list(ser.keys())[1])
                subservice = ser[list(ser.keys())[0]]
                for subser in subservice:
                    if subservice[subser] == True:
                        services.append(subser)
            else:
                if ser[list(ser.keys())[0]] == True:
                    services.append(list(ser.keys())[0])
        if request.session.get('time_pause') != None:
            logwindow = LogWindows.objects.filter(window_id = window_id).last()
            tt = datetime.now()
            tt = tt.replace(hour = request.session.get('time_pause').get('hour'), minute = request.session.get('time_pause').get('minute'), second = request.session.get('time_pause').get('second'), microsecond = 0)
            logwindow.time_pause = datetime.now()-tt + logwindow.time_pause
            logwindow.save()
            request.session['time_pause'] is None      
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
        elif (Tickets.objects.filter(time_create__contains = t).filter(time_close = None).filter(window = None).filter(service__in = services).exists() == False) and (Tickets.objects.filter(time_create__contains = t).exclude(status = 'Отложен').filter(time_close = None).filter(window = request.session.get('window_id')).filter(service__in = services).exists() == False):
            ticket = 'Текущий талон: Нет талонов в очереди'
            service = 'Услуга:'
            request.session['ticket'] = ticket
            return JsonResponse({"ticket": ticket, 'service': service}, status=200)
        elif request.session.get('Ticket_n') is None:
            window_id = request.session.get('window_id')
            Ticket = Tickets.objects.filter(time_create__contains = t).filter(time_close = None).filter(window = None).filter(service__in = services).earliest('id_ticket')
            Ticket.window = Windows.objects.get(operator = request.user)
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

# Кнопка "Клиент не подошел"
@login_required
def cancelbutton(request):
    t = datetime.now().date()
    if request.POST.get('click', False):
        service = Windows.objects.get(operator = request.user).services
        services = []
        for ser in service:
            if len(list(ser.keys())) > 1:
                if ser[list(ser.keys())[1]] == True:
                    services.append(list(ser.keys())[1])
                subservice = ser[list(ser.keys())[0]]
                for subser in subservice:
                    if subservice[subser] == True:
                        services.append(subser)
            else:
                if ser[list(ser.keys())[0]] == True:
                    services.append(list(ser.keys())[0])
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

# Кнопка "Перерыв"
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
        request.session['time_pause'] = {'hour': time.hour, 'minute': time.minute, 'second': time.second}
        hour = time.hour
        minute = time.minute
        second = time.second
        return JsonResponse({"ticket": ticket, 'service': service, "hour": hour, "minute": minute, "second": second}, status=200)

# Кнопка "Отложить"
@login_required
def delaybutton(request):
    t = datetime.now().date()
    if request.POST.get('click', False):
        service = Windows.objects.get(operator = request.user).services
        services = []
        for ser in service:
            if len(list(ser.keys())) > 1:
                if ser[list(ser.keys())[1]] == True:
                    services.append(list(ser.keys())[1])
                subservice = ser[list(ser.keys())[0]]
                for subser in subservice:
                    if subservice[subser] == True:
                        services.append(subser)
            else:
                if ser[list(ser.keys())[0]] == True:
                    services.append(list(ser.keys())[0])
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

# Кнопка "Вернуть"
@login_required
def returnbutton(request):
    t = datetime.now().date()
    if request.POST.get('click', False):
        window_id = request.session.get('window_id')
        if request.session.get('Ticket_n') != None:
            id=request.session.get('Ticket_n')
            Ticket = Tickets.objects.get(id_ticket=request.session.get('Ticket_n'))
            Ticket.time_close = datetime.now()
            Ticket.status = 'Закрыт'
            Ticket.operator = User.objects.get(id = request.user.id)
            Ticket.save()
        Ticket = Tickets.objects.filter(status = 'Отложен').filter(window = window_id).earliest('id_ticket')
        Ticket.time_pause += datetime.now() - Ticket.time_call.replace(tzinfo=None)
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

# Кнопка "Перенаправить"
@login_required
def redirectbutton(request):
    if request.POST.get('click', False):
        windows_l = []
        if Windows.objects.exclude(operator = None).exclude(id_window = request.session.get('window_id')).values_list('id_window').order_by('id_window').exists():
            for l in Windows.objects.exclude(operator_id = None).exclude(id_window = request.session.get('window_id')).values_list('id_window').order_by('id_window'):
                windows_l.append(l[0])
        return JsonResponse({"windows_l": windows_l}, status=200)

# Кнопка "Отправить" в модельном окне перенаправления
@login_required
def redbutton(request):
    t = datetime.now().date()
    if request.POST.get('click', False):
        red_window_id = request.POST.get("name")
        service = Windows.objects.get(operator = request.user).services
        services = []
        for ser in service:
            if len(list(ser.keys())) > 1:
                if ser[list(ser.keys())[1]] == True:
                    services.append(list(ser.keys())[1])
                subservice = ser[list(ser.keys())[0]]
                for subser in subservice:
                    if subservice[subser] == True:
                        services.append(subser)
            else:
                if ser[list(ser.keys())[0]] == True:
                    services.append(list(ser.keys())[0])
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

# Экран лога талонов
@login_required
def statistics(request):
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

# Возвращает данные для таблицы лога талонов
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
                tservice = ''
            else:
                tca = p.time_call.time().strftime("%H:%M:%S")
                tservice = datetime.now() - p.time_call
            if p.time_close == None:
                tcl = ''
            if p.time_close != None and p.time_call != None:
                tcl = p.time_close.time().strftime("%H:%M:%S")
                tservice = p.time_close - p.time_call
            elif p.time_close != None:
                tcl = p.time_close.time().strftime("%H:%M:%S")
            if p.window_id == None:
                iw = ''
            else:
                iw = p.window_id
            if p.operator == None:
                op = ''
            else:
                op = p.operator.last_name +' ('+ p.operator.username +')'
            if p.time_pause == timedelta(0):
                tpause = ''
            else:
                minute = p.time_pause.seconds//60
                hour = minute//60
                minute = minute%60
                second = p.time_pause.seconds%60
                tpause = datetime.now().time()
                tpause = tpause.replace(hour = hour, minute = minute, second = second, microsecond = 0).strftime("%H:%M:%S")
            if tservice != '':
                tservice = tservice.seconds
                s = tservice
                hours = s // 3600 
                s = s - (hours * 3600)
                minutes = s // 60
                seconds = s - (minutes * 60)
                tservicef = datetime.now().time()
                tservicef = tservicef.replace(hour = hours, minute = minutes, second = seconds, microsecond = 0).strftime("%H:%M:%S")
            else:
                tservicef=''
            listoftickets.append([p.name_ticket, p.service, p.status, tc, tca, tcl, iw, op, tpause, tservicef, tservice])
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
                tservice = ''
            else:
                tca = p.time_call.time().strftime("%H:%M:%S")
                tservice = datetime.now() - p.time_call
            if p.time_close == None:
                tcl = ''
            if p.time_close != None and p.time_call != None:
                tcl = p.time_close.time().strftime("%H:%M:%S")
                tservice = p.time_close - p.time_call
            elif p.time_close != None:
                tcl = p.time_close.time().strftime("%H:%M:%S")
            if p.window_id == None:
                iw = ''
            else:
                iw = p.window_id
            if p.operator == None:
                op = ''
            else:
                op = p.operator.last_name +' ('+ p.operator.username +')'
            if p.time_pause == timedelta(0):
                tpause = ''
            else:
                minute = p.time_pause.seconds//60
                hour = minute//60
                minute = minute%60
                second = p.time_pause.seconds%60
                tpause = datetime.now().time()
                tpause = tpause.replace(hour = hour, minute = minute, second = second, microsecond = 0).strftime("%H:%M:%S")
            if tservice != '':
                tservice = tservice.seconds
                s = tservice
                hours = s // 3600 
                s = s - (hours * 3600)
                minutes = s // 60
                seconds = s - (minutes * 60)
                tservicef = datetime.now().time()
                tservicef = tservicef.replace(hour = hours, minute = minutes, second = seconds, microsecond = 0).strftime("%H:%M:%S")
            else:
                tservicef=''
            listoftickets.append([p.name_ticket, p.service, p.status, tc, tca, tcl, iw, op, tpause, tservicef, tservice])
        return JsonResponse({'date': date, 'listoftickets': listoftickets}, status=200)

# Страница лога окон
@login_required
def statisticsw(request):
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

# Возвращает данные для таблицы лога окон
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
                tcount = Tickets.objects.filter(time_call__gte = p.time_login).filter(window_id = p.window_id).count()
                taverage = Tickets.objects.filter(time_call__gte = p.time_login).filter(window_id = p.window_id)
            else:
                tlogout = p.time_logout.time().strftime("%H:%M:%S")
                tservice = (datetime.min + (p.time_logout - p.time_login)).time().strftime("%H:%M:%S")
                tcount = Tickets.objects.filter(time_call__gte = p.time_login).filter(time_call__lte = p.time_logout).filter(window_id = p.window_id).count()
                taverage = Tickets.objects.filter(time_call__gte = p.time_login).filter(time_call__lte = p.time_logout).filter(window_id = p.window_id)
            if p.time_pause == timedelta(0):
                tpause = ''
            else:
                minute = p.time_pause.seconds//60
                hour = minute//60
                minute = minute%60
                second = p.time_pause.seconds%60
                tpause = datetime.now().time()
                tpause = tpause.replace(hour = hour, minute = minute, second = second, microsecond = 0).strftime("%H:%M:%S")
            taverage = taverage.aggregate(average_difference=Avg(F('time_close') - F('time_call')))
            if taverage.get('average_difference') is None:
                taverage = ""
                s = 0
            else:
                s = taverage.get('average_difference').seconds
                hours = s // 3600 
                s = s - (hours * 3600)
                minutes = s // 60
                seconds = s - (minutes * 60)
                taverage = datetime.now().time()
                taverage = taverage.replace(hour = hours, minute = minutes, second = seconds, microsecond = 0).strftime("%H:%M:%S")
            listoflogwindows.append([p.window_id,p.operator.last_name + ' (' + p.operator.username + ')', tlogin, tlogout, tservice, tpause, tcount, taverage, s])
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
                tcount = Tickets.objects.filter(time_call__gte = p.time_login).filter(window_id = p.window_id).count()
                taverage = Tickets.objects.filter(time_call__gte = p.time_login).filter(window_id = p.window_id)
            else:
                tlogout = p.time_logout.time().strftime("%H:%M:%S")
                tservice = (datetime.min + (p.time_logout - p.time_login)).time().strftime("%H:%M:%S")
                tcount = Tickets.objects.filter(time_call__gte = p.time_login).filter(time_call__lte = p.time_logout).filter(window_id = p.window_id).count()
                taverage = Tickets.objects.filter(time_call__gte = p.time_login).filter(time_call__lte = p.time_logout).filter(window_id = p.window_id)
            if p.time_pause == timedelta(0):
                tpause = ''
            else:
                minute = p.time_pause.seconds//60
                hour = minute//60
                minute = minute%60
                second = p.time_pause.seconds%60
                tpause = datetime.now().time()
                tpause = tpause.replace(hour = hour, minute = minute, second = second, microsecond = 0).strftime("%H:%M:%S")
            taverage = taverage.aggregate(average_difference=Avg(F('time_close') - F('time_call')))
            if taverage.get('average_difference') is None:
                taverage = ""
                s = 0
            else:
                s = taverage.get('average_difference').seconds
                hours = s // 3600 
                s = s - (hours * 3600)
                minutes = s // 60
                seconds = s - (minutes * 60)
                taverage = datetime.now().time()
                taverage = taverage.replace(hour = hours, minute = minutes, second = seconds, microsecond = 0).strftime("%H:%M:%S")
            listoflogwindows.append([p.window_id,p.operator.last_name + ' (' + p.operator.username + ')', tlogin, tlogout, tservice, tpause, tcount, taverage, s])
        return JsonResponse({'date': date, 'listoflogwindows': listoflogwindows}, status=200)

# Страница общей статистики
@login_required
def statisticsall(request):
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

# Возвращает данные для страницы общей статистики
@login_required
def statisticstableall(request):
    if request.GET.get('click', False):
        service = Services.objects.latest('id_services').services
        services = []
        for ser in service:
            if len(list(ser.keys())) > 1:
                subservice = ser[list(ser.keys())[0]]
                for subser in subservice:
                    services.append(subser)
            else:
                subservice = list(ser.keys())[0]
                services.append(subservice)
        if request.GET.get('date') is None:
            t = datetime.now().strftime("%Y")
        else:
            t = request.GET.get('date')
        nt = []
        nt.append (Tickets.objects.filter(time_create__year = t).filter(time_create__month = '01').count())
        nt.append (Tickets.objects.filter(time_create__year = t).filter(time_create__month = '02').count())
        nt.append (Tickets.objects.filter(time_create__year = t).filter(time_create__month = '03').count())
        nt.append (Tickets.objects.filter(time_create__year = t).filter(time_create__month = '04').count())
        nt.append (Tickets.objects.filter(time_create__year = t).filter(time_create__month = '05').count())
        nt.append (Tickets.objects.filter(time_create__year = t).filter(time_create__month = '06').count())
        nt.append (Tickets.objects.filter(time_create__year = t).filter(time_create__month = '07').count())
        nt.append (Tickets.objects.filter(time_create__year = t).filter(time_create__month = '08').count())
        nt.append (Tickets.objects.filter(time_create__year = t).filter(time_create__month = '09').count())
        nt.append (Tickets.objects.filter(time_create__year = t).filter(time_create__month = '10').count())
        nt.append (Tickets.objects.filter(time_create__year = t).filter(time_create__month = '11').count())
        nt.append (Tickets.objects.filter(time_create__year = t).filter(time_create__month = '12').count())
        stc = []
        stat = []
        for s in services:
           stc.append (Tickets.objects.filter(time_create__contains = t).filter(service=s).count())
           temp = Tickets.objects.filter(time_create__contains = t).filter(service=s).aggregate(average_difference=Avg(F('time_close') - F('time_call')))
           if temp.get('average_difference') == None:
               stat.append (0)
           else:
               stat.append (temp.get('average_difference').seconds)
               if temp.get('average_difference').microseconds > 500000:
                   stat[0] += 1
        return JsonResponse({'nt': nt, 'stc': stc, 'services': services, 'stat': stat, 'date': t}, status=200)


# Страница настроек учетных записей
@login_required
def settings(request):
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

# Кнопка удаления учетной записи
def delbutton(request):
    if request.POST.get('click', False):
        Userdel = (User.objects.filter(id=request.POST.get('idbutton')))[0]
        Userdel.is_active = False
        Userdel.save()

        return JsonResponse({}, status=200)

# Кнопка редактирования пользователя
@login_required
def edituser(request):
    if request.POST.get('click', False):
        Useredit = (User.objects.filter(id=request.POST.get('idbutton')))[0]

        request.session['useredit'] = Useredit.id
        return JsonResponse({}, status=200)

# Страница регистрации
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

# Страница редактирования пользователя
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

# Предоставляет список пользователей
@login_required
def settingstable(request):
    if request.POST.get('click', False):
        user = []
        users = User.objects.exclude(username = 'admin').exclude(is_active = False)
        for p in users:
            user.append([p.id, p.username, p.last_name])

        return JsonResponse({"user": user}, status=200)

# Страница окон
@login_required
def settingsw(request):
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

# Предоставляет список окон
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

# Кнопка добавления нового окна
@login_required
def addwindow(request):
    if request.POST.get('click', False):
        number = Windows.objects.all().count()
        window = Windows(id_window = number+1, services = Services.objects.latest('id_services').services)
        window.save()
        return JsonResponse({}, status=200)

# Кнопка сброса пользователя с окна
@login_required
def windowreset(request):
    if request.POST.get('click', False):
        window = Windows.objects.get(id_window = request.POST.get('idwindow'))
        logwindow = LogWindows.objects.filter(operator = window.operator).last()
        logwindow.time_logout = datetime.now()
        logwindow.save()
        sessions = list(Session.objects.all())
        for s in sessions:
            if s.get_decoded().get('_auth_user_id') == str(window.operator.id):
                ses = Session.objects.get(pk = s.pk)
                ses.delete()
        window.operator = None
        window.save()
        return JsonResponse({}, status=200)

# Кнопка изменения статуса окна
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

# Кнопка для перехода на страницу услуг окна
@login_required
def changeservicew(request):
    if request.POST.get('click', False):
        idwindow = request.POST.get('idwindow')
        request.session['idwindow'] = idwindow
        return JsonResponse({}, status=200)

# Страница услуг окна
@login_required
def settingswchange(request):
    if request.POST.get('click', False):
        idwindow = request.session.get('idwindow')
    else:
        idwindow = request.session.get('idwindow')
        return render(
            request,
            'app/settingswchange.html',
            {
                'title':'Услуги окна',
                'year':datetime.now().year,
                'idwindow':idwindow,
            }
        )

# Возвращает список услуг для окна или ОПС
@login_required
def servicestable(request):
    if request.GET.get('click', False):
        idwindow = request.session.get('idwindow')
        serviceslist = Windows.objects.get(id_window = idwindow).services
        return JsonResponse({'serviceslist':serviceslist}, status=200)
    if request.GET.get('click2', False):
        serviceslist = Services.objects.latest('id_services').services
        return JsonResponse({'serviceslist':serviceslist}, status=200)

# Кнопка применения изменений при изменении услуг
@login_required
def wchange(request):
    if request.GET.get('click', False):
        listofcheck = request.GET.get('listofcheck')
        listofcheck = json.loads(listofcheck)
        service = Services.objects.latest('id_services')
        services = str(service.services)
        window = Windows.objects.get(id_window = request.session.get('idwindow'))
        services = str(window.services)
        for p in listofcheck:
            k = "'" + str(list(p.keys())[0]) + "'"
            v = str(list(p.values())[0]).lower()
            services = services.replace(k + ': ' + 'False', k + ': ' + v)
            services = services.replace(k + ': ' + 'True', k + ': ' + v)
        services = services.replace("'",'"')
        window.services = json.loads(services)
        window.save()
        return JsonResponse({}, status=200)

    if request.POST.get('click2', False):
        listofcheck = request.POST.get('listofcheck')
        listofcheck = json.loads(listofcheck)
        service = Services.objects.latest('id_services')
        services = str(service.services)

        for p in listofcheck:
            k = "'" + str(list(p.keys())[0]) + "'"
            v = str(list(p.values())[0]).lower()
            services = services.replace(k + ': ' + 'False', k + ': ' + v)
            services = services.replace(k + ': ' + 'True', k + ': ' + v)
        listofservices = json.dumps(services, ensure_ascii=False)
        listofservices = listofservices[1:-1]
        listofservices.replace('True', 'true')
        listofservices.replace('False', 'false')
        listofservices = listofservices.replace("'",'"')
        with codecs.open("services.json", "w", "utf-8-sig") as temp:
            temp.write(listofservices)
            temp.close()
        re.sub(r'\'*\': False', '', services, count=0)
        service.services = json.loads(listofservices)
        service.save() 
        ls = service.services
        lsc = []
        for s in ls:
            if s[list(s.keys())[-1]] == True:
                lsc.append(s)
            else:
                continue
            if len(lsc[-1]) > 1:
                sc = lsc[-1][list(lsc[-1].keys())[0]]
                myDict = {key:val for key, val in sc.items() if val != False}
                lsc[-1][list(lsc[-1].keys())[0]] = myDict
        Window = Windows.objects.all()
        for i in Window:
            if len(i.services) != len(lsc):
                i.services = lsc
                i.save()
        return JsonResponse({}, status=200)

# Страница услуг ОПС
@login_required
def settingso(request):
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

# Страница настроек
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



