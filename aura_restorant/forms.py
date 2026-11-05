from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth import get_user_model
User = get_user_model()
from .models import Accounts
from django.db import transaction

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()
    name = forms.CharField(max_length=15, label="ім'я")
    secondname = forms.CharField(max_length=15, label="прізвище") 
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email")
    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Користувач з таким email вже існує")
        return email
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
            Accounts.objects.create(
                user = user,
                name = self.cleaned_data["name"],
                secondname = self.cleaned_data["secondname"],
                description = "",
            )
        return user

class AccountUpdateForm(forms.ModelForm):
    email = forms.EmailField(label='email')

    class Meta:
        model = Accounts
        fields = ['name', 'secondname', 'photo', 'description']
    field_order = ["name", "secondname", "email", "description", "photo"]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].initial = self.instance.user.email
    def clean_email(self):
        email = self.cleaned_data["email"]
        taken = (
            User.objects.filter(email__iexact=email)
            .exclude(pk=self.instance.user.pk)
            .exists()
        )
        if taken:
            raise forms.ValidationError("цей email вже використовується")
        return email
    def save(self, commit = True):
        account = super().save(commit = False)
        account.user.email = self.cleaned_data["email"]
        if commit:
            with transaction.atomic():
                account.user.save(update_fields=["email"])
                account.save
        return account
