from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from .forms import *
from .models import *
from .utils import DataMixin
from django.contrib.auth.views import LoginView, FormView
from django.contrib.auth.forms import AuthenticationForm
from django.core.cache import cache
#from .models import Comment
#from .forms import CommentForm


class ContactFormView(DataMixin, FormView):
    form_class = ContactForm
    template_name = 'shop/contacts.html'
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Обратная связь')
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
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


class ShopHome(DataMixin, ListView):
    model = Shop
    template_name = 'shop/index.html'
    context_object_name = 'products'
    paginate_by = 3

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Товары всех категорий')
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

#    def comment(self, request, product_id):
#        comments = product_id.comments.filter(active=True)
#
#        if request.method == 'POST':
#            # A comment was posted
#            comment_form = CommentForm(data=request.POST)
#            if comment_form.is_valid():
#                # Create Comment object but don't save to database yet
#                new_comment = comment_form.save(commit=False)
#                # Assign the current post to the comment
#                new_comment.post = product_id
                # Save the comment to the database
#                new_comment.save()
#        else:
#            comment_form = CommentForm()

#        return render(request,
 #                 'blog/post/detail.html',
 #                 {'post': product_id,
 #                  'comments': comments,
 #                  'comment_form': comment_form})

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




# Страница с корзиной.
def basket_view(request):
    context = dict()
    context['categories'] = get_categories()
    basket = get_basket(get_sid(request))
    context['basket'] = ItemInBasket.objects.filter(basket=basket).select_related('product')
    return render(request, 'shop/basket.html', context=context)


# Добавляет отзыв к указанному товару
#def add_review(request, product_id):
#    form = AddReview(request.POST)
#    if form.is_valid():
#        Review.objects.create(name=form.cleaned_data['name'], text=form.cleaned_data['text'],
#                              star=form.cleaned_data['star'], product=Shop.objects.get(id=product_id))
#
#    return render(request, 'shop/product.html')


# Добавляет товар нужным ID в корзину
def to_basket(request, product_id):
    basket = get_basket(get_sid(request))
    product = Shop.objects.get(id=product_id)

    product_in_basket = ItemInBasket.objects.filter(basket=basket, product=product)

    if product_in_basket:
        my_obj = product_in_basket.first()
        my_obj.count += 1
        my_obj.save()
    else:
        ItemInBasket.objects.create(basket=basket, product=product, count=1)

    return redirect(basket_view)


# Оформление заказа:
# 1) Получаем корзину исходя из ID сессии / username
# 2) Получаем все товары из корзины. Если их не 0:
# 3) Создаём заказ
# *pib означаем product in basket
def create_order(request):
    basket = get_basket(get_sid(request))
    products = basket.product.all()

    if products:
        order = Order.objects.create(owner=get_sid(request))
        for product in products:
            pib = ItemInBasket.objects.get(product=product, basket=basket)
            ItemInOrder.objects.create(product=product, order=order, count=pib.count)
            pib.delete()
    return render(request, 'shop/create_order.html')


# Находим или создаём новую корзину
def get_basket(sid):
    basket, created = Basket.objects.get_or_create(sid=sid)
    return basket



# Получаем имя пользователя (если авторизован) или его ID сессии
def get_sid(request):
    if not request.user.is_authenticated:
        sid = request.session.session_key
        if not sid:
            sid = request.session.cycle_key()
    else:
        sid = request.user.username
    return sid


# Получаем из кэша категории для меню. Если кэша нет, записываем их туда
def get_categories():
    categories = cache.get_or_set('categories', Category.objects.filter(name=True), 3600)
    return categories



