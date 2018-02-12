from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.

class Country(models.Model):
    name = models.CharField(_('name'), max_length=50)
    is_supported = models.BooleanField(_('supported'), default=False)

    class Meta:
        verbose_name = _('country')
        verbose_name_plural = _('countries')

    def __str__(self):
        return '%s' % self.name

class District(models.Model):
    country = models.ForeignKey('Country', on_delete=models.CASCADE, verbose_name=_('country'))
    name = models.CharField(_('name'), max_length=50)
    suffix = models.CharField(_('suffix'), max_length=50, blank=True)
    is_supported = models.BooleanField(_('supported'), default=False)

    class Meta:
        verbose_name = _('district')
        verbose_name_plural = _('districts')

    def __str__(self):
        return '%s' % self.name
