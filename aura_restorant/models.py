from django.db import models
from django.contrib.auth.models import User

class Accounts(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Користувач", related_name="user_accounts")
    name = models.CharField(max_length=20)
    secondname = models.CharField(max_length=20)
    description = models.TextField()
    photo = models.ImageField(upload_to='media/', blank=True, null=True)
    def __str__(self):
        return f"{self.name}{self.description}"

class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name='назва категорії')
    
class Menu(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='dishes', null=True, verbose_name='категорія')
    name = models.CharField(max_length=30)
    description = models.TextField()
    photo = models.ImageField(upload_to='media/', blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    weight = models.PositiveIntegerField(verbose_name='вага в грамах', help_text='вкажіть вагу в грамах')
    is_available = models.BooleanField(default=True, verbose_name='в наявності')

class Order(models.Model):
    user = models.ForeignKey(Accounts, on_delete=models.CASCADE, verbose_name='клієнт', related_name='user_history')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='час замовлення')
    address = models.CharField(max_length=255, verbose_name='адресса доставки')
    phone = models.CharField(max_length=20, verbose_name='номер телефону')
    PAYMENT_CHOICES = [
        ('online', 'Онлайн'),
        ('cash', 'Готівка при отриманні'),
    ]
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES, verbose_name='спосіб оплати')

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    item = models.ForeignKey(Menu, on_delete=models.PROTECT,verbose_name='страва')    
    quantity = models.PositiveIntegerField(default=1, verbose_name='кількість')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='ціна на момент покупки')

class Review(models.Model):
    user = models.ForeignKey(Accounts, on_delete=models.CASCADE, verbose_name='користувач')
    item = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='reviews', verbose_name='страва')
    text = models.TextField(verbose_name='відгук')
    rate = models.PositiveSmallIntegerField(verbose_name='оцінка 1-5')
    is_approwed = models.BooleanField(default=False, verbose_name='схвалено модератором')
    