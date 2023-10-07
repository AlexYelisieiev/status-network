from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from .models import CustomUser
from .forms import CustomUserChangeForm, CustomUserCreationForm


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    list_display = ['username', 'age', 'email']
    readonly_fields = ['age']

    fieldsets = (
        (None, {'fields': ('username', 'email', 'password', 'age')}),
    )
    add_fieldsets = (
        (None, {'fields': ('username', 'email', 'password1', 'password2', 'age')}),
    )

# Register your models here.
admin.site.register(CustomUser, CustomUserAdmin)
