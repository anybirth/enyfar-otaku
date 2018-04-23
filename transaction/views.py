import datetime
import uuid
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.conf import settings
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from . import models, forms
from main.models import Item
from accounts.models import UserAddress

# Create your views here.

@method_decorator(login_required, name='dispatch')
class OrderView(generic.CreateView):
    _uuid = None
    model = models.Order
    form_class = forms.OrderForm
    template_name = 'transaction/order.html'

    def __init__(self):
        self._uuid = str(uuid.uuid4())

    def get_success_url(self):
        return reverse_lazy('transaction:order_confirm', args=[self._uuid])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['item'] = Item.objects.get(pk=1)
        # context['item'] = Item.objects.get(pk=self.request.GET.get('item'))
        return context

    def form_valid(self, form):
        user = self.request.user
        order = form.save(commit=False)
        order.requester = user
        order.item = Item.objects.get(pk=1)
        # order.item = Item.objects.get(pk=self.request.GET.get('item'))
        order.uuid = self._uuid
        order.status_deadline = timezone.now() + datetime.timedelta(hours=1)
        order.save()
        return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
class OrderConfirmView(generic.DetailView):
    model = models.Order
    slug_field = 'uuid'
    context_object_name = 'order'
    template_name = 'transaction/order_confirm.html'

    def get_object(self, queryset=None):
        obj = get_object_or_404(models.Order, uuid=self.kwargs['slug'], status=1)
        return obj

    def post(self, request, slug):
        order = get_object_or_404(models.Order, uuid=slug, status=1)
        order.status = 2
        order.status_deadline = None
        order.save()
        models.Order.objects.filter(status_deadline__lte=timezone.now()).delete()

        protocol = 'https://' if self.request.is_secure() else 'http://'
        host_name = settings.HOST_NAME
        send_mail(
            '依頼送信完了',
            '依頼を受け付けました\n' +
            '承認されると以下のURLにアクセスできます（テスト）\n\n' +
            protocol + host_name + str(reverse_lazy('transaction:order_accepted', args=[slug])),
            'info@anybirth.co.jp',
            [request.user.email],
            fail_silently=False,
        )

        return redirect(reverse_lazy('transaction:order_sent', args=[order.uuid]), permanent=True)

@method_decorator(login_required, name='dispatch')
class OrderSentView(generic.DetailView):
    model = models.Order
    slug_field = 'uuid'
    context_object_name = 'order'
    template_name = 'transaction/order_sent.html'

    def get_object(self, queryset=None):
        obj = get_object_or_404(models.Order, uuid=self.kwargs['slug'], status=2)
        return obj

class OrderAcceptedView(generic.DetailView):
    model = models.Order
    slug_field = 'uuid'
    context_object_name = 'order'
    template_name = 'transaction/order_accepted.html'

    def get_object(self, queryset=None):
        obj = get_object_or_404(models.Order, uuid=self.kwargs['slug'], status=3)
        return obj

class OrderCancelView(generic.DeleteView):
    model = models.Order
    slug_field = 'uuid'
    template_name = 'transaction/order_cancel.html'
    success_url = reverse_lazy('transaction:order')

    def get_object(self, queryset=None):
        obj = get_object_or_404(models.Order, uuid=self.kwargs['slug'], status=3)
        return obj

@method_decorator(login_required, name='dispatch')
class DeliveryMethodView(generic.UpdateView):
    model = models.Order
    form_class = forms.DeliveryMethodForm
    slug_field = 'uuid'
    template_name = 'transaction/delivery_method.html'

    def get_object(self, queryset=None):
        obj = get_object_or_404(models.Order, uuid=self.kwargs['slug'], status=3)
        return obj

    def get_success_url(self):
        return reverse_lazy('transaction:delivery_select', args=[self.kwargs['slug']])

@login_required
def delivery_select(request, uuid):
    order = get_object_or_404(models.Order, uuid=uuid, status=3)
    if order.delivery_method == 1:
        return redirect(reverse_lazy('transaction:delivery_post', args=[order.uuid]), permanent=True)
    elif order.delivery_method == 2:
        return redirect(reverse_lazy('transaction:delivery_hand', args=[order.uuid]), permanent=True)

@method_decorator(login_required, name='dispatch')
class DeliveryPostView(generic.CreateView):
    model = UserAddress
    form_class = forms.DeliveryPostForm
    template_name = 'transaction/delivery_post.html'

    def get_object(self, queryset=None):
        obj = get_object_or_404(models.Order, uuid=self.kwargs['slug'], status=3)
        return obj

    def get_success_url(self):
        return reverse_lazy('transaction:payment', args=[self.kwargs['slug']])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_addresses'] = UserAddress.objects.filter(user=self.request.user)
        context['uuid'] = self.kwargs['slug']
        return context

    def form_valid(self, form):
        user = self.request.user
        user_address = form.save(commit=False)
        user_address.user = user
        user_address.save()
        order = models.Order.objects.get(uuid=self.kwargs['slug'], status=3)
        order.requester_address = UserAddress.objects.get(id=user_address.id)
        order.save()
        return super().form_valid(form)

@login_required
def delivery_register(request, uuid, id):
    order = get_object_or_404(models.Order, uuid=uuid, status=3)
    order.requester_address = UserAddress.objects.get(id=id)
    order.save()
    return redirect(reverse_lazy('transaction:payment', args=[order.uuid]), permanent=True)

@method_decorator(login_required, name='dispatch')
class PaymentView(generic.DetailView):
    model = models.Order
    slug_field = 'uuid'
    context_object_name = 'order'
    template_name = 'transaction/payment.html'

    def get_object(self, queryset=None):
        obj = get_object_or_404(models.Order, uuid=self.kwargs['slug'], status=3)
        return obj
