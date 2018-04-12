import uuid
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.conf import settings
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from . import models, forms
from main.models import Item

# Create your views here.

@method_decorator(login_required, name='dispatch')
class OrderView(generic.CreateView):
    _uuid = None
    model = models.Order
    form_class = forms.OrderForm
    template_name = 'transaction/order.html'

    def __init__(self):
        self._uuid = str(uuid.uuid4())

    def form_valid(self, form):
        user = self.request.user
        order = form.save(commit=False)
        order.user = user
        order.item = get_object_or_404(Item, pk=1)
        # order.item = get_object_or_404(Item, pk=self.request.GET.get('item'))
        order.uuid = self._uuid
        order.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('transaction:order_confirm', args=[self._uuid])

@method_decorator(login_required, name='dispatch')
class OrderConfirmView(generic.DetailView):
    model = models.Order
    slug_field = 'uuid'
    context_object_name = 'order'
    template_name = 'transaction/order_confirm.html'
