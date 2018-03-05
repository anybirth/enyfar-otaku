from django.shortcuts import render
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from .forms import UserForm

class CustomModelBackend(ModelBackend):

    def authenticate(self, request, username=None, password=None):
        UserModel = get_user_model()
        if '@' in username:
            kwargs = {'email': username}
        else:
            kwargs = {'username': username}
        try:
            user = UserModel.objects.get(**kwargs)
            if user.check_password(password):
                return user
        except UserModel.DoesNotExist:
            UserModel.set_password(self, raw_password=password)
