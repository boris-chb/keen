from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class CustomUserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'country', 'date_of_birth']
    
class CustomUserChangeForm(UserCreationForm):
    model = CustomUser
    fields = UserCreationForm.Meta.fields + ('country',)

