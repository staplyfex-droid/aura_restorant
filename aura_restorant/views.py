from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserRegistrationForm, AccountUpdateForm
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, UpdateView
from .models import Accounts
from django.urls import reverse_lazy




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