from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views




urlpatterns = [
    path("register/", views.register, name="register"),
    path("login/", auth_views.LoginView.as_view(template_name="aura_restorant/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("", views.home, name='home'),
    path("profile/", views.ProfileView.as_view(), name='profile'),
    path("progile/edit/", views.ProfileUpdateView.as_view(), name='profile_edit'),
    path("menu/", views.MenuListView.as_view(), name='menu_list'),
    path("menu/<int:pk>/", views.MenuDetailView.as_view(), name='menu_detail'),
    path('cart/', views.cart_detail, name='cart'),
    path('cart/add/<int:pk>/', views.add_cart, name='cart_add'),
    path('cart/remove/<int:pk>/', views.cart_remove, name='cart_remove'),
    path('checkout/', views.checkout, name='checkout'),
    path('orders/<int:pk>/', views.order_detail, name='order_detail'),
]