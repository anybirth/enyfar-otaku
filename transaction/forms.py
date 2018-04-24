import datetime
from django import forms
from django.conf import settings
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from . import models
from accounts.models import UserAddress

class OrderForm(forms.ModelForm):
    class Meta:
        model = models.Order
        fields = ['number', 'delivered_at_order']
        widgets = {
            'number': forms.Select(
                choices = (
                    ('1', _('1')),
                    ('2', _('2')),
                    ('3', _('3')),
                    ('4', _('5')),
                    ('5', _('5')),
                    ('6', _('6')),
                    ('7', _('7')),
                    ('8', _('8')),
                    ('9', _('9')),
                    ('10', _('10+')),
                )
            ),
            'delivered_at_order': forms.SelectDateWidget(
                years = range(timezone.now().year, timezone.now().year + 2),
                months = {
                    timezone.now().month: _(str(timezone.now().month)),
                    timezone.now().month + 1: _(str(timezone.now().month + 1)),
                },
                empty_label=("年", "月", "日"),
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for fieldname in ['number', 'delivered_at_order']:
            self.fields[fieldname].help_text = None
            self.fields[fieldname].required = True

    def clean_delivered_at_order(self):
        delivered_at_order = self.cleaned_data['delivered_at_order']
        if delivered_at_order <= timezone.now().date() + datetime.timedelta(days=1):
            raise forms.ValidationError('明後日以降の日付を選択してください')
        return delivered_at_order

class DeliveryMethodForm(forms.ModelForm):
    class Meta:
        model = models.Order
        fields = ['delivery_method']
        widgets = {
            'delivery_method': forms.RadioSelect(
                choices = settings.DELIVERY_METHOD,
            )
        }

class DeliveryPostForm(forms.ModelForm):
    class Meta:
        model = UserAddress
        fields = ['district', 'postal_code', 'address1', 'address2', 'last_name', 'first_name']

    def clean_postal_code(self):
        postal_code = self.cleaned_data['postal_code']
        if not postal_code.isdigit():
            raise forms.ValidationError('郵便番号はハイフンなしの半角数字で入力してください')
        return postal_code
