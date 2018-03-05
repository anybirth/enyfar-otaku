import uuid
import datetime
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

# @receiver(post_save, sender=models.User)
# def create_traveller_member(sender, instance, created, **kwargs):
#     if created:
#         if not isinstance(instance, AnonymousUser):
#             if instance.is_staff == False:
#                 models.Member.objects.get_or_create(user=instance, is_traveller=True, is_verified=False)

class SignupView(generic.TemplateView):
    template_name = 'accounts/signup.html'

class EmailSignupView(generic.CreateView):
    model = models.User
    form_class = forms.UserForm
    template_name = 'accounts/email_signup.html'
    success_url = reverse_lazy('accounts:complete')

    def form_valid(self, form):
        _uuid = str(uuid.uuid4())
        form.instance.password = make_password(self.request.POST.get('password'))
        user = form.save(commit=False)
        user.is_active = False
        user.uuid = _uuid
        user.uuid_deadline = timezone.now() + datetime.timedelta(days=1)
        user.save()
        if not isinstance(form.instance, AnonymousUser):
            if instance.is_staff == False:
                models.Member.objects.get_or_create(user=form.instance, is_traveller=False, is_verified=False)
        # create_traveller_member(sender=models.User, instance=form.instance, created=True)
        send_mail(
            u'仮登録完了',
            # u'仮登録が完了しました。\n以下のURLより本登録を完了させてください。\n\nhttp://172.20.10.6:8000/accounts/activate/' + _uuid,
            u'仮登録が完了しました。\n以下のURLより本登録を完了させてください。\n\nhttp://192.168.33.10:8000/accounts/activate/' + _uuid,
            'info@anybirth.co.jp',
            [user.email],
            fail_silently=False,
        )
        return super().form_valid(form)

class SignupTravellerView(generic.TemplateView):
    template_name = 'accounts/signup.html'

class EmailSignupTravellerView(generic.CreateView):
    model = models.User
    form_class = forms.UserForm
    template_name = 'accounts/email_signup.html'
    success_url = reverse_lazy('accounts:complete')

    def form_valid(self, form):
        _uuid = str(uuid.uuid4())
        form.instance.password = make_password(self.request.POST.get('password'))
        user = form.save(commit=False)
        user.is_active = False
        user.uuid = _uuid
        user.uuid_deadline = timezone.now() + datetime.timedelta(days=1)
        user.save()
        if not isinstance(instance, AnonymousUser):
            if instance.is_staff == False:
                models.Member.objects.get_or_create(user=instance, is_traveller=True, is_verified=False)
        send_mail(
            u'仮登録完了',
            # u'仮登録が完了しました。\n以下のURLより本登録を完了させてください。\n\nhttp://172.20.10.6:8000/accounts/activate/' + _uuid,
            u'仮登録が完了しました。\n以下のURLより本登録を完了させてください。\n\nhttp://192.168.33.10:8000/accounts/activate/' + _uuid,
            'info@anybirth.co.jp',
            [user.email],
            fail_silently=False,
        )
        return super().form_valid(form)

class CompleteView(generic.TemplateView):
    template_name = 'accounts/complete.html'

class ActivateView(generic.View):
    template_name = 'accounts/activate.html'

    def get(self, request, uuid):
        try:
            user = models.User.objects.get(uuid=uuid)
        except models.User.DoesNotExist:
            return redirect('accounts:activate_error')
        delta = timezone.now() - user.uuid_deadline
        if delta > datetime.timedelta(days=1):
            return redirect('accounts:activate_error')
        user.is_active = True
        user.uuid = None
        user.uuid_deadline = None
        user.save()
        user.member.is_verified = True
        user.member.save()
        send_mail(
            u'本登録完了',
            u'本登録が完了しました。本サービスをお楽しみください。',
            'info@anybirth.co.jp',
            [user.email],
            fail_silently=False,
        )
        return render(request, 'accounts/activate.html', {'uuid': user.uuid})

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
            return super(ActivateErrorView, self).form_invalid(form)
        _uuid = uuid.uuid4()
        user.uuid = _uuid
        user.uuid_deadline = timezone.now() + datetime.timedelta(days=1)
        user.save()
        send_mail(
            u'再認証メール',
            # u'以下のURLより本登録を完了させてください。\n\nhttp://172.20.10.6:8000/accounts/activate/' + str(_uuid),
            u'以下のURLより本登録を完了させてください。\n\nhttp://192.168.33.10:8000/accounts/activate/' + str(_uuid),
            'info@anybirth.co.jp',
            [user.email],
            fail_silently=False,
        )
        return super().form_valid(form)

class ActivateAgainView(generic.TemplateView):
    template_name = 'accounts/activate_again.html'

class LoginView(auth_views.LoginView):
    template_name='accounts/login.html'

@method_decorator(login_required, name='dispatch')
class ProfileTravellerView(generic.ListView):
    model = Request
    template_name = 'accounts/profile_traveller.html'
    context_object_name = 'requests'

    def get_queryset(self, **kwargs):
        if not self.request.user:
            return Request.objects.filter(item__buyer=self.request.user)
        else:
            return Request.objects.all()

    def get_context_data(self, **kwargs):
        context = super(ProfileTravellerView, self).get_context_data(**kwargs)
