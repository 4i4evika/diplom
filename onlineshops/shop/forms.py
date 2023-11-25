from django import forms
from .models import *
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from captcha.fields import CaptchaField
#from .models import Comment


class ContactForm(forms.Form):
    name = forms.CharField(label='Имя', max_length=200)
    email = forms.EmailField()
    content = forms.CharField(label='Сообщение',
                              widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}))
    captcha = CaptchaField(label='Введите текст с картинки')


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль',
                                widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Подтверждение пароля',
                                widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class AddReview(forms.Form):
    name = forms.CharField(label='Имя', required=True, max_length=150,
                           widget=forms.TextInput(attrs={'placeholder': 'Представьтесь', 'class': 'form-control'}))
    text = forms.CharField(widget=forms.Textarea({'placeholder': 'Содержание', 'class': 'form-control'}),
                           label='Содержание', required=True)
    star = forms.ChoiceField(choices=[(j, j) for j in range(1, 6)],
                             widget=forms.RadioSelect(attrs={'class': 'form-check-input'}), required=True)


#class CommentForm(forms.ModelForm):
#    name = forms.CharField(label='Имя', max_length=200)
#    content = forms.CharField(label='Сообщение',
#                              widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}))
    #class Meta:
    #    model = Comment
    #    fields = ('name', 'body')