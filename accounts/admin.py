from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
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
    fieldsets = (
        (None, {'fields': ('username', 'email', 'phone_number', 'uuid', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'jender', 'birthday', 'profession', 'line_id', 'twitter_id', 'instagram_id', 'facebook_id', 'whatsapp_id', 'kik_id', 'wechat_id', 'level', 'notice', 'email_verified', 'is_traveller', 'is_banned', 'uuid_deadline', 'social_confirm_deadline')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )
    # The forms to add and change user instances
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm

admin.site.register(models.User, UserAdmin)
admin.site.register([models.UserAddress, models.Itinerary, models.Transfer,])
