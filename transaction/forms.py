from django import forms
from django.conf import settings
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from . import models

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

class DeliveryMethodForm(forms.ModelForm):
    class Meta:
        model = models.Order
        fields = ['delivery_method']
        widgets = {
            'delivery_method': forms.RadioSelect(
                choices = settings.DELIVERY_METHOD,
            )
        }
