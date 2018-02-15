from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.

class Request(models.Model):
    item = models.ForeignKey('main.Item', on_delete=models.CASCADE, verbose_name=_('item'))
    buyer = models.ForeignKey('accounts.Member', on_delete=models.CASCADE, verbose_name=_('buyer'))
    buyer_address = models.ForeignKey('accounts.MemberAddress', on_delete=models.CASCADE, verbose_name=_('buyer\'s address'), blank=True, null=True)
    title = models.CharField(_('name'), max_length=50)
    description = models.TextField(_('description'), blank=True)
    delivery_method = models.SmallIntegerField(_('delivery request'))
    payment_method = models.SmallIntegerField(_('payment request'))
    price_request = models.IntegerField(_('price request'), blank=True)
    hand_place = models.CharField(_('hand place request'), max_length=255, blank=True)
    status = models.SmallIntegerField(_('status'), default=0)
    expired_at = models.DateTimeField(_('expired at'), blank=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        verbose_name = _('request')
        verbose_name_plural = _('requests')

    def __str__(self):
        return '%s' % self.title

class Agreement(models.Model):
    request = models.OneToOneField('Request', on_delete=models.CASCADE, verbose_name=_('request'))
    seller = models.ForeignKey('accounts.Member', on_delete=models.CASCADE, verbose_name=_('seller'))
    seller_address = models.ForeignKey('accounts.MemberAddress', on_delete=models.CASCADE, verbose_name=_('seller\'s address'), blank=True, null=True)
    price = models.IntegerField(_('price request'), blank=True)
    postage = models.IntegerField(_('postage'), default=0)
    arriving_at = models.DateTimeField(_('arriving at'))
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        verbose_name = _('agreement')
        verbose_name_plural = _('agreements')

    def __str__(self):
        return '%s' % self.request__title
