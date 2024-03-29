from django import template
from shop.models import *


register = template.Library()


@register.inclusion_tag('shop/list_categories.html')
def show_categories(sort=None, cat_selected=0):
    if not sort:
        cats = Category.objects.all()
    else:
        cats = Category.objects.order_by(sort)
    context = {'cats': cats, 'cat_selected': cat_selected}
    return context