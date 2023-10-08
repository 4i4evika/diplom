from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from .forms import *
from .models import *
from .utils import DataMixin
#from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, FormView
from django.contrib.auth.forms import AuthenticationForm


class ContactFormView(DataMixin, FormView):
    form_class = ContactForm
    template_name = 'shop/contacts.html'
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Обратная связь')
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        print(form.cleaned_data)
        return redirect('index')


class LoginUser(DataMixin, LoginView):
    form_class = AuthenticationForm
    template_name = 'shop/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Авторизация')
        return dict(list(context.items()) + list(c_def.items()))



class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'shop/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Регистрация')
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('index')


#menu = [
#    {'title': 'Корзина', 'url_name': 'index'},
#    {'title': 'Войти', 'url_name': 'index'},
#]
class ShopHome(DataMixin, ListView):
    model = Shop
    template_name = 'shop/index.html'
    context_object_name = 'products'
    paginate_by = 3

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Главная страница')
        return dict(list(context.items()) + list(c_def.items()))

def get_queryset(self):
        return Shop.objects.filter(is_published=True).select_related('cat')


class ShowProduct(DataMixin, DetailView):
    model = Shop
    template_name = 'shop/product.html'
    slug_url_kwarg = 'product_slug'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['product'])
        return dict(list(context.items()) + list(c_def.items()))


class ShopCategory(DataMixin, ListView):
    model = Shop
    template_name = 'shop/index.html'
    context_object_name = 'products'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c = Category.objects.get(slug=self.kwargs['cat_slug'])
        c_def = self.get_user_context(title=str(c.name), cat_selected=c.pk)
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Shop.objects.filter(cat__slug=self.kwargs['cat_slug'],
                                   is_published=True).select_related('cat')





class Basket(ListView):
    model = Shop
    template_name = 'shop/basket.html'
    context_object_name = 'product'


    def get_basket(sid):
        basket, created = Basket.objects.get_or_create(sid=sid)
        return basket


