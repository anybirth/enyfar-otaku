from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.

class Country(models.Model):
    name = models.CharField(_('国・地域名'), max_length=50)
    is_supported = models.BooleanField(_('対応'), default=False)

    class Meta:
        verbose_name = _('国・地域')
        verbose_name_plural = _('国・地域')

    def __str__(self):
        return '%s' % self.name

class District(models.Model):
    country = models.ForeignKey('Country', on_delete=models.CASCADE, verbose_name=_('国・地域ID'))
    name = models.CharField(_('行政区画名'), max_length=50)
    suffix = models.CharField(_('接尾語'), max_length=50, blank=True)
    is_supported = models.BooleanField(_('対応'), default=False)

    class Meta:
        verbose_name = _('行政区画')
        verbose_name_plural = _('行政区画')

    def __str__(self):
        return '%s' % self.name
