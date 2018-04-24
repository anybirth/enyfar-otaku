import uuid
import datetime
from socket import gethostbyaddr, gethostbyname, gethostname
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django import http
from django.conf import settings
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.core.mail import send_mail
from django.contrib.auth import authenticate
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.hashers import make_password
from django.db.models.signals import post_save
from django.dispatch import receiver
from transaction.models import Order
from . import models
from . import forms

# Create your views here.

class SignupView(generic.TemplateView):
    template_name = 'accounts/signup.html'
    traveller = False

    def get_object(self, queryset=None):
        return queryset.get(traveller=self.traveller)

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('accounts:profile')
        return super().get(request)

class EmailSignupView(generic.CreateView):
    model = models.User
    form_class = forms.UserForm
    template_name = 'accounts/email_signup.html'
    success_url = reverse_lazy('accounts:complete')
    traveller = False

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('accounts:profile')
        return super().get(request)

    def form_valid(self, form):
        form.instance.password = make_password(self.request.POST.get('password'))
        user = form.save(commit=False)
        user.is_traveller = self.traveller
        user.email_verified=False
        user.uuid = str(uuid.uuid4())
        user.uuid_deadline = timezone.now() + datetime.timedelta(days=1)
        user.save()

        protocol = 'https://' if self.request.is_secure() else 'http://'
        host_name = settings.HOST_NAME
        send_mail(
            u'仮登録完了',
            u'仮登録が完了しました。\n' +
            '以下のURLより本登録を完了させてください。\n\n' +
            protocol + host_name + str(reverse_lazy('accounts:activate', args=[user.uuid,])),
            'info@anybirth.co.jp',
            [user.email],
            fail_silently=False,
        )
        return super().form_valid(form)

class SocialConfirmView(generic.UpdateView):
    model = models.User
    form_class = forms.UserForm
    template_name = 'accounts/social_confirm.html'
    success_url = reverse_lazy('accounts:complete')
    traveller = False

    def get_object(self, queryset=None):
        return self.request.user

    def get(self, request):
        user = request.user
        if not request.user.is_authenticated:
            return http.HttpResponseServerError()
        elif user.uuid:
            return redirect('accounts:already_registered')
        elif user.is_staff:
            return redirect('accounts:logout')
        user.social_confirm_deadline = timezone.now() + datetime.timedelta(minutes=10)
        user.save()
        return super().get(request)

    def form_valid(self, form):
        user = self.request.user
        if not user.is_authenticated:
            return http.HttpResponseServerError()
        elif user.uuid:
            return redirect('accounts:already_registered')
        elif user.is_staff:
            return redirect('accounts:logout')
        form.instance.password = make_password(self.request.POST.get('password'))
        user = form.save(commit=False)
        user.is_traveller = self.traveller
        user.email_verified=False
        user.social_confirm_deadline = None
        user.uuid = str(uuid.uuid4())
        user.uuid_deadline = timezone.now() + datetime.timedelta(days=1)
        user.save()

        protocol = 'https://' if self.request.is_secure() else 'http://'
        host_name = settings.HOST_NAME
        send_mail(
            u'仮登録完了',
            u'仮登録が完了しました。\n' +
            '以下のURLより本登録を完了させてください。\n\n' +
            protocol + host_name + str(reverse_lazy('accounts:activate', args=[user.uuid,])),
            'info@anybirth.co.jp',
            [user.email],
            fail_silently=False,
        )
        return super().form_valid(form)

class AlreadyRegisteredView(generic.TemplateView):
    template_name = 'accounts/already_registered.html'

class CompleteView(generic.TemplateView):
    template_name = 'accounts/complete.html'

class ActivateView(generic.TemplateView):
    template_name = 'accounts/activate.html'

    def get(self, request, uuid):
        try:
            user = models.User.objects.get(uuid=uuid)
        except models.User.DoesNotExist:
            return redirect('accounts:activate_error')
        if user.uuid_deadline < timezone.now() or not user.uuid_deadline:
            return redirect('accounts:activate_error')
        user.email_verified = True
        user.uuid_deadline = None
        user.save()

        send_mail(
            u'本登録完了',
            u'本登録が完了しました。本サービスをお楽しみください。',
            'info@anybirth.co.jp',
            [user.email],
            fail_silently=False,
        )
        return super().get(request, uuid)

class ActivateErrorView(generic.FormView):
    form_class = forms.ActivateForm
    model = models.User
    template_name = 'accounts/activate_error.html'
    success_url = reverse_lazy('accounts:activate_again')

    def form_valid(self, form):
        try:
            user = models.User.objects.get(email=form.cleaned_data['email'])
        except models.User.DoesNotExist:
            form.add_error(field='email', error='メールアドレスに一致するユーザーが見つかりません')
            return super().form_invalid(form)
        user.uuid = str(uuid.uuid4())
        user.uuid_deadline = timezone.now() + datetime.timedelta(days=1)
        user.save()

        protocol = 'https://' if self.request.is_secure() else 'http://'
        host_name = settings.HOST_NAME
        send_mail(
            u'再認証メール',
            u'以下のURLより本登録を完了させてください。\n\n' +
            protocol + host_name + str(reverse_lazy('accounts:activate', args=[user.uuid,])),
            'info@anybirth.co.jp',
            [user.email],
            fail_silently=False,
        )
        return super().form_valid(form)

class ActivateAgainView(generic.TemplateView):
    template_name = 'accounts/activate_again.html'

class LoginView(auth_views.LoginView):
    template_name = 'accounts/login.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('accounts:profile')
        return super().get(request)

class LogoutView(auth_views.LogoutView):
    next_page = reverse_lazy('accounts:login')

@method_decorator(login_required, name='dispatch')
class ProfileView(generic.ListView):
    model = Order
    template_name = 'accounts/profile.html'
    context_object_name = 'orders'

    def get(self, request):
        user = request.user
        if not user.is_staff and not user.uuid:
            return redirect('accounts:social_confirm')
        return super().get(request)

@method_decorator(login_required, name='dispatch')
class ProfileTravellerView(generic.ListView):
    model = Order
    template_name = 'accounts/profile_traveller.html'
    context_object_name = 'orders'

    def get(self, request):
        user = request.user
        if not user.is_staff and not user.uuid:
            return redirect('accounts:social_confirm')
        return super().get(request)

@method_decorator(login_required, name='dispatch')
class AssociateView(generic.TemplateView):
    template_name = 'accounts/associate.html'

    def get(self, request):
        if request.user.is_staff:
            return redirect('accounts:logout')
        return super().get(request)

@method_decorator(login_required, name='dispatch')
class AssociateCompleteView(generic.TemplateView):
    template_name = 'accounts/associate_complete.html'
