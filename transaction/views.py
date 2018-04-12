import uuid
from django.shortcuts import render
from django.views import generic
from django.conf import settings
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from . import models, forms

# Create your views here.

@method_decorator(login_required, name='dispatch')
class OrderView(generic.CreateView):
    _uuid = str(uuid.uuid4())
    model = models.Order
    form_class = forms.OrderForm
    template_name = 'transaction/order.html'
    success_url = reverse_lazy('transaction:order_confirm', args=[_uuid])

    def form_valid(self, form):
        user = self.request.user
        order = form.save(commit=False)
        order.user = user
        order.item = self.request.GET.get('item')
        order.uuid = _uuid
        order.save()

        protocol = 'https://' if self.request.is_secure() else 'http://'
        host_name = settings.HOST_NAME
        send_mail(
            u'依頼完了',
            u'依頼が完了しました。\n' +
            u'マイページはこちら↓\n\n' +
            protocol + host_name + str(reverse_lazy('accounts:profile')),
            'info@anybirth.co.jp',
            [user.email],
            fail_silently=False,
        )
        return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
class OrderConfirmView(generic.DetailView):
    model = models.Order
    slug_field = 'uuid'
    context_object_name = 'order'
    template_name = 'transaction/order_confirm.html'
