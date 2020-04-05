from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import UserAccounts

class RegForm(UserCreationForm):
    class Meta:
        model = UserAccounts
        fields = ["email","phone","first_name","last_name"]
        # widgets = {"email": forms.EmailInput( attrs={"class":""})}

class UpdationForm(UserChangeForm):
    class Meta:
        model = UserAccounts
        fields = ["phone","first_name","last_name","password"]