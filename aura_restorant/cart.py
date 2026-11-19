from decimal import Decimal
from .models import Menu
CART_SESSION_ID = 'cart'

class Cart:
    def __init__(self, request):
        self.session = request.session
        self.cart = self.session.setdefault(CART_SESSION_ID, {})
    def add(self, dish, quantity = 1, override = False):
        key = str(dish.pk)
        current = self.cart.get(key, 0)
        new_qty = quantity if override else current + quantity
        new_qty = min(new_qty, 20)
        if new_qty <= 0:
            self.remove(dish)
            return
        self.cart[key] = new_qty
        self.save()
    def remove(self, dish):
        self.cart.pop(str(dish.pk),None)
        self.save()
    def save(self):
        self.session.modified = True
    def clear(self):
        self.session[CART_SESSION_ID] = {}
        self.session.modified = True
    def __iter__(self):
        dishes = Menu.objects.in_bulk([int(k) for k in self.cart])
        for key,qty in self.cart.items():
            dish = dishes.get(int(key))
            if dish is None:
                continue
            yield {
                'dish': dish,
                'quantity': qty,
                'price': dish.price,
                'subtotal': dish.price * qty
            }
        def __len__(self):
            return sum(self.cart.values())
        def total_price(self):
            return sum((item['subtotal']for item in self),Decimal('0'))
