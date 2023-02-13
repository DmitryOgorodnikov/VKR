#Формы
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

#Форма для входа в систему
class BootstrapAuthenticationForm(AuthenticationForm):
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'Логин'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Пароль'}))

#Форма для регистрации пользователя
class UserRegistrationForm(forms.ModelForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': ''}))
    last_name = forms.CharField(label='ФИО', widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': ''}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder': ''}))
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder': ''}))

    chief = forms.BooleanField(label='Права начальника', required=False)

    class Meta:
        model = User
        fields = ('username', 'last_name')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают!')
        return cd['password2']

    def clean_username(self):
        username = self.cleaned_data.get("username")
        try:
            User._default_manager.get(username=username)
            raise forms.ValidationError('Пользователь уже существует!')
        except User.DoesNotExist:
            return username

#Форма для редактирования пользователя
class UserChangeForm(forms.ModelForm):

    username = forms.CharField(label='Логин', widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': ''}))
    last_name = forms.CharField(label='ФИО', widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': ''}))
    password = forms.CharField(label='Пароль', required=False, widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder': ''}))
    password2 = forms.CharField(label='Повторите пароль', required=False, widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder': ''}))

    chief = forms.BooleanField(label='Права начальника', required=False)


    class Meta:
        model = User
        fields = ('id','username', 'last_name')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise ValidationError('Пароли не совпадают')
        return cd['password2']

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if self.instance.username != username:
            try:
                User._default_manager.get(username=username)
                raise forms.ValidationError('Пользователь уже существует!')
            except User.DoesNotExist:
                return username
        return username

#Форма для авторизации на окно
class WindowsAuthenticationForm(forms.Form):
    id_window = forms.ChoiceField(choices = [('','')], label='Окно')
