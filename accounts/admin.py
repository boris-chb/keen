from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .forms import CustomUserRegisterForm, CustomUserChangeForm

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserRegisterForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['username', 'email', 'is_staff', 'country', 'date_joined']

admin.site.register(CustomUser, CustomUserAdmin)
