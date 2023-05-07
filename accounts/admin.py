from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from accounts.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.models import Group
from .models import User, OTPcode

class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ['email', 'full_name', 'is_admin']
    list_filter = ['is_admin']

    fieldsets =[
        (None, {'fields':('phone_number', 'email', 'full_name', 'password')}),
        ('permisions', {'fields':('is_admin', 'is_active')}),
    ]

    add_fieldsets = [
        (None, {'fields':('phone_number', 'email', 'full_name', 'password1', 'password2')})
    ]

    search_fields = ["email", 'full_name']
    ordering = ["full_name"]
    filter_horizontal = []

class OTPcodeAdmin(admin.ModelAdmin):
    list_display = ['phone_number', 'code', 'created']

admin.site.unregister(Group)
admin.site.register(User, UserAdmin)
admin.site.register(OTPcode)