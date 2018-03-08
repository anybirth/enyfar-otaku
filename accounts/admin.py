from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm,  ReadOnlyPasswordHashField
from . import models

# Register your models here.

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = models.User
        fields = UserCreationForm.Meta.fields + ('email',)


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = models.User
        fields = '__all__'


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm

admin.site.register(models.User, UserAdmin)
admin.site.register([models.Member, models.MemberAddress, models.Itinerary, models.Transfer, models.Departure, models.Arrival,])
