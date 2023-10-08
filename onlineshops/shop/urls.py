from django.urls import path
from .views import *
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', ShopHome.as_view(), name='index'),
    path('product/<slug:product_slug>/', ShowProduct.as_view(), name='product'),
    path('category/<slug:cat_slug>/', ShopCategory.as_view(), name='category'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', LogoutView.as_view(template_name='shop/logout.html'), name='logout'),
    path('contacts/', ContactFormView.as_view(), name='contacts'),
    path('basket/', Basket.as_view(), name='basket'),
]