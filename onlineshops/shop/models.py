from django.db import models
from django.urls import reverse

class Shop(models.Model):
    title = models.CharField(max_length=200, verbose_name='Наименование')
    slug = models.SlugField(max_length=255, unique=True, verbose_name='Ссылка')
    description = models.TextField(null=True, blank=True, verbose_name='Описание')
    image = models.ImageField(upload_to="images/%Y/%m/%d", blank=True, verbose_name='Изображение')
    price = models.TextField(null=False, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=True, verbose_name='В наличии')
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name='Категория')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product', kwargs={'product_slug': self.slug})

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='Ссылка')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Review(models.Model):
    name = models.CharField(max_length=150)
    text = models.TextField()
    star = models.IntegerField()
    product = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='reviews')


class Basket(models.Model):
    sid = models.CharField(max_length=150, blank=True, null=True)
    username = models.CharField(max_length=150, blank=True, null=True)
    product = models.ManyToManyField(Shop, through='ItemInBasket', related_name='basket')


class ItemInBasket(models.Model):
    product = models.ForeignKey(Shop, on_delete=models.CASCADE)
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE)
    count = models.IntegerField()


class Order(models.Model):
    product = models.ManyToManyField(Shop, through='ItemInOrder')
    owner = models.CharField(max_length=150, default='no owner')

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ['id']


class ItemInOrder(models.Model):
    product = models.ForeignKey(Shop, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    count = models.IntegerField()
