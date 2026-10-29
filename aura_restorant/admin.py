from django.contrib import admin
from .models import Accounts, Menu, Order, OrderItem, Review, Category

admin.site.register(Accounts)
admin.site.register(Menu)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Review)
admin.site.register(Category)