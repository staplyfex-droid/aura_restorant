from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserRegistrationForm, AccountUpdateForm, CartAddForm, OrderForm
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, UpdateView, ListView, DetailView
from .models import Accounts, Category, Menu, Order, OrderItem
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.views.decorators.http import require_POST
from .cart import Cart




def register(request):
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            return redirect("home")
    else:
        form = UserRegistrationForm()
    return render(request,"aura_restorant/register.html",{"form": form})


def home(request):
    return render(request, "aura_restorant/home.html")

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'aura_restorant/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
  
        account, created = Accounts.objects.get_or_create(
            user=self.request.user,
            defaults={'name': self.request.user.username, 'secondname': ''}
        )
        context['account'] = account
            
        return context

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Accounts
    form_class = AccountUpdateForm
    template_name = 'aura_restorant/profile_edit.html'
    success_url = reverse_lazy('home')
    def get_object(self, queryset = None):
        return get_object_or_404(Accounts, user = self.request.user)


class MenuListView(ListView):
    model = Menu
    template_name = 'aura_restorant/menu_list.html'
    context_object_name = 'dishes'
    def get_queryset(self):
        qs = Menu.objects.select_related('category')
        category_id = self.request.GET.get('category')
        if category_id and category_id.isdigit():
            qs = qs.filter(category_id=category_id)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['selected_category'] = self.request.GET.get('category', '')
        return context

class MenuDetailView(DetailView):
    model = Menu
    template_name = 'aura_restorant/menu_detail.html'
    context_object_name = 'dish'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reviews'] = self.object.reviews.filter(is_approwed=True).select_related('user')
        return context

def cart_detail(request):
    return render(request, 'aura_restorant/cart.html', {'cart': Cart(request)})

@require_POST
def add_cart(request, pk):
    cart = Cart(request)
    dish = get_object_or_404(Menu, pk=pk)
    form = CartAddForm(request.POST)
    if not dish.is_available:
        messages.error(request, "ця страва недоступна для замовлення")
    elif form.is_valid():
        cd = form.cleaned_data
        cart.add(dish, quantity = cd['quantity'], override = cd['override'])
        messages.success(request, "Страву додано до кошика")
    return redirect(request.POST.get('next') or 'cart')

@require_POST
def cart_remove(request, pk):
    cart = Cart(request)
    cart.remove(get_object_or_404(Menu, pk=pk))
    return redirect('cart')

@login_required
def checkout(request):
    cart = Cart(request)
    if len(cart) == 0:
        return redirect('cart')
    account, _ = Accounts.objects.get_or_create(user=request.user, defaults = {'name': request.user.username, 'secondname': ''},)
    unavailable = [i['dish'].name for i in cart if not i['dish'].is_available]
    if unavailable:
        messages.error(request, 'Недоступні страви: ' + ', '.join(unavailable) + '. Видаліть їх з кошика.')
        return redirect('cart')
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                order = form.save(commit=False)
                order.user = account
                order.save()
                OrderItem.objects.bulk_create([
                    OrderItem(order = order, item = i['dish'], quantity = i['quantity'], price = i['price'])
                    for i in cart
                ])
            cart.clear()
            return redirect('order_detail', pk = order.pk)
    else:
        form = OrderForm()
    return render(request, 'aura_restorant/checkout.html', {'form': form, 'cart': cart})

@login_required
def order_detail(request, pk):
    order = get_object_or_404(
        Order.objects.prefetch_related('items__item'),
        pk = pk,
        user__user = request.user,
    )
    return render(request, 'aura_restorant/order_detail.html', {'order': order})
   
