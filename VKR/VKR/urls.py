"""
Definition of urls for VKR.
"""

from datetime import datetime
from django.urls import path
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView

from app import forms, views
from app.views import register


urlpatterns = [
    path('kiosk/', views.kiosk, name='kiosk'),
    path('kiosk/kioskbtn', views.kioskbtn, name='kioskbtn'),
    path('kiosk/kbutton', views.kbutton, name='kbutton'),
    path('tickets/', views.tickets, name='tickets'),
    path('', views.home, name='home'),
    path('login/',
         LoginView.as_view
         (
             template_name='app/login.html',
             authentication_form=forms.BootstrapAuthenticationForm,
             extra_context=
             {
                 'title': 'Log in',
                 'year' : datetime.now().year,
             }
         ),
         name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    # Пульт оператора
    path('service/', views.service, name='service'),
    path('service/windowbutton', views.windowbutton, name='windowbutton'),
    path('service/operator/', views.operator, name='operator'),
    path('service/operator/operatorbutton', views.operatorbutton, name='operatorbutton'),
    path('service/operator/nextbutton', views.nextbutton, name='nextbutton'),
    path('service/operator/cancelbutton', views.cancelbutton, name='cancelbutton'),
    path('service/operator/breakbutton', views.breakbutton, name='breakbutton'),
    path('service/operator/delaybutton', views.delaybutton, name='delaybutton'),
    path('service/operator/returnbutton', views.returnbutton, name='returnbutton'),
    path('service/operator/redirectbutton', views.redirectbutton, name='redirectbutton'),
    path('service/operator/redbutton', views.redbutton, name='redbutton'),
    #Статистика
    path('statistics/', views.statistics, name='statistics'),
    path('statistics/statisticstable', views.statisticstable, name='statisticstable'),
    path('statisticsw/', views.statisticsw, name='statisticsw'),
    path('statisticsw/statisticstablew', views.statisticstablew, name='statisticstablew'),
    path('statisticsall/', views.statisticsall, name='statisticsall'),
    path('statisticsall/statisticstableall', views.statisticstableall, name='statisticstableall'),
    # Настройки
    path('settings/', views.settings, name='settings'),
    path('settings/delbutton', views.delbutton, name='delbutton'),
    path('settings/edituser', views.edituser, name='edituser'),
    path('settings/settingstable', views.settingstable, name='settingstable'),
    path('register/', views.register, name='register'),
    path('settings/editer/', views.editer, name='editer'),
    path('settings/window/', views.settingsw, name='settingsw'),
    path('settings/window/settingswtable', views.settingswtable, name='settingswtable'),
    path('settings/window/addwindow', views.addwindow, name='addwindow'),
    path('settings/window/changestatusw', views.changestatusw, name='changestatusw'),
    path('settings/window/changeservicew', views.changeservicew, name='changeservicew'),
    path('settings/window/settingswchange', views.settingswchange, name='settingswchange'),
    path('settings/window/wchange', views.wchange, name='wchange'),
    path('settings/window/servicestable', views.servicestable, name='servicestable'),
    path('settings/ops/', views.settingso, name='settingso'),
    path('settings/ops/wchange', views.wchange, name='wchange'),
    path('settings/ops/servicestable', views.servicestable, name='servicestable'),
    path('settings/mainsettings', views.settingsm, name='settingsm'),

    path('admin/', admin.site.urls),
]


