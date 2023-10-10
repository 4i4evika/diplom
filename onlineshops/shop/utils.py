from .models import *
from django.db.models import Count


menu = [
    #{'title': 'Корзина', 'url_name': 'index'},
    {'title': 'Обратная связь', 'url_name': 'contacts'},
    #{'title': 'Войти', 'url_name': 'login'},
    #{'title': 'Регистрация', 'url_name': 'register'},
]


class DataMixin:
    paginate_by = 3

    def get_user_context(self, **kwargs):
        context = kwargs
        cats = Category.objects.annotate(Count('shop'))

        user_menu = menu.copy()
        if not self.request.user.is_authenticated:
            user_menu.pop(0)

        context['menu'] = user_menu
        context['cats'] = cats

        if 'cat_selected' not in context:
            context['cat_selected'] = 0
        return context
