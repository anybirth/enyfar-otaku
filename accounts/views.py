import uuid
import datetime
from socket import gethostbyaddr, gethostbyname, gethostname
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django import http
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
from transaction.models import Request
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
        _uuid = str(uuid.uuid4())
        form.instance.password = make_password(self.request.POST.get('password'))
        user = form.save(commit=False)
        user.is_traveller = self.traveller
        user.email_verified=False
        user.uuid = _uuid
        user.uuid_deadline = timezone.now() + datetime.timedelta(days=1)
        user.save()
        send_mail(
            u'仮登録完了',
            u'仮登録が完了しました。\n以下のURLより本登録を完了させてください。\n\nhttps://' + gethostbyaddr(gethostname().strip('host-').replace('-', '.'))[0] + reverse_lazy('accounts:activate', args=[_uuid,]),
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
        user.social_confirm_deadline = timezone.now() + datetime.timedelta(hours=1)
        user.save()
        models.User.objects.filter(social_confirm_deadline__lte= timezone.now()).delete()
        return super().get(request)

    def form_valid(self, form):
        if not self.request.user:
            return render(request, 'accounts:signup')
        _uuid = str(uuid.uuid4())
        form.instance.password = make_password(self.request.POST.get('password'))
        user = form.save(commit=False)
        user.is_traveller = self.traveller
        user.email_verified=False
        user.social_confirm_deadline = None
        user.uuid = _uuid
        user.uuid_deadline = timezone.now() + datetime.timedelta(days=1)
        user.save()
        send_mail(
            u'仮登録完了',
            u'仮登録が完了しました。\n以下のURLより本登録を完了させてください。\n\nhttps://' + gethostbyaddr(gethostname().strip('host-').replace('-', '.'))[0] + str(reverse_lazy('accounts:activate', args=[_uuid,])),
            'info@anybirth.co.jp',
            [user.email],
            fail_silently=False,
        )
        return super().form_valid(form)

class CompleteView(generic.TemplateView):
    template_name = 'accounts/complete.html'

class ActivateView(generic.TemplateView):
    template_name = 'accounts/activate.html'

    def get(self, request, uuid):
        try:
            user = models.User.objects.get(uuid=uuid)
        except models.User.DoesNotExist:
            return redirect('accounts:activate_error')
        if timezone.now() > user.uuid_deadline:
            return redirect('accounts:activate_error')
        user.email_verified = True
        user.uuid = None
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
        _uuid = str(uuid.uuid4())
        user.uuid = _uuid
        user.uuid_deadline = timezone.now() + datetime.timedelta(days=1)
        user.save()
        send_mail(
            u'再認証メール',
            u'以下のURLより本登録を完了させてください。\n\nhttps://' + gethostbyaddr(gethostname().strip('host-').replace('-', '.'))[0] + reverse_lazy('accounts:activate', args=[_uuid,]),
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
    model = Request
    template_name = 'accounts/profile.html'
    context_object_name = 'requests'

@method_decorator(login_required, name='dispatch')
class ProfileTravellerView(generic.ListView):
    model = Request
    template_name = 'accounts/profile_traveller.html'
    context_object_name = 'requests'
