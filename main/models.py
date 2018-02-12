from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.

class Category(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, verbose_name=_('user'))
    name = models.CharField(_('name'), max_length=50, unique=True)
    status = models.SmallIntegerField(_('status'), default=0)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')

    def __str__(self):
        return '%s' % self.name

class Tag(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, verbose_name=_('user'))
    name = models.CharField(_('name'), max_length=50, unique=True)
    status = models.SmallIntegerField(_('status'), default=0)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        verbose_name = _('tag')
        verbose_name_plural = _('tags')

    def __str__(self):
        return '%s' % self.name

class Item(models.Model):
    category = models.ManyToManyField('Category', verbose_name=_('category'))
    tag = models.ManyToManyField('Tag', verbose_name=_('tag'), blank=True)
    country = models.ForeignKey('meta.Country', on_delete=models.CASCADE, verbose_name=_('counntry'))
    district = models.ForeignKey('meta.District', on_delete=models.CASCADE, verbose_name=_('district'), blank=True, null=True)
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, verbose_name=_('user'))
    name = models.CharField(_('name'), max_length=50)
    description = models.TextField(_('description'), blank=True)
    status = models.SmallIntegerField(_('status'), default=0)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        verbose_name = _('item')
        verbose_name_plural = _('items')

    def __str__(self):
        return '%s' % self.name

class ItemImage(models.Model):
    item = models.ForeignKey('Item', on_delete=models.CASCADE, verbose_name=_('item'))
    image = models.ImageField(verbose_name=_('image'), upload_to='images/', unique=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        verbose_name = _('item image')
        verbose_name_plural = _('item images')

    def __str__(self):
        return '%s' % self.image.name

class ItemLike(models.Model):
    item = models.ForeignKey('Item', on_delete=models.CASCADE, verbose_name=_('item'))
    member = models.ForeignKey('accounts.Member', on_delete=models.CASCADE, verbose_name=_('member'))
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        verbose_name = _('item like')
        verbose_name_plural = _('item likes')

    def __str__(self):
        return '%s' % self.item__name + ': ' + self.member__user__username
