from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.

class Category(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, verbose_name=_('ユーザーID'))
    name = models.CharField(_('カテゴリー名'), max_length=50, unique=True)
    recommendation_ranking = models.PositiveSmallIntegerField(_('おすすめ順'), blank=True, null=True, unique=True)
    status = models.SmallIntegerField(_('状態'), default=0)
    created_at = models.DateTimeField(_('作成日時'), auto_now_add=True)
    updated_at = models.DateTimeField(_('更新日時'), auto_now=True)

    class Meta:
        verbose_name = _('カテゴリー')
        verbose_name_plural = _('カテゴリー')

    def __str__(self):
        return '%s' % self.name

class Tag(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, verbose_name=_('ユーザーID'))
    name = models.CharField(_('タグ名'), max_length=50, unique=True)
    recommendation_ranking = models.PositiveSmallIntegerField(_('おすすめ順'), blank=True, null=True, unique=True)
    status = models.SmallIntegerField(_('状態'), default=0)
    created_at = models.DateTimeField(_('作成日時'), auto_now_add=True)
    updated_at = models.DateTimeField(_('更新日時'), auto_now=True)

    class Meta:
        verbose_name = _('タグ')
        verbose_name_plural = _('タグ')

    def __str__(self):
        return '%s' % self.name

class Item(models.Model):
    category = models.ManyToManyField('Category', verbose_name=_('カテゴリーID'))
    tag = models.ManyToManyField('Tag', verbose_name=_('タグID'), blank=True)
    country = models.ForeignKey('meta.Country', on_delete=models.CASCADE, verbose_name=_('国・地域ID'))
    district = models.ForeignKey('meta.District', on_delete=models.CASCADE, verbose_name=_('行政区画ID'), blank=True, null=True)
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, verbose_name=_('ユーザーID'))
    name = models.CharField(_('商品名'), max_length=50)
    description = models.TextField(_('商品説明文'), blank=True)
    recommendation_ranking = models.PositiveSmallIntegerField(_('おすすめ順'), blank=True, null=True, unique=True)
    status = models.SmallIntegerField(_('状態'), default=0)
    created_at = models.DateTimeField(_('作成日時'), auto_now_add=True)
    updated_at = models.DateTimeField(_('更新日時'), auto_now=True)

    class Meta:
        verbose_name = _('商品')
        verbose_name_plural = _('商品')

    def __str__(self):
        return '%s' % self.name

class ItemImage(models.Model):
    item = models.ForeignKey('Item', on_delete=models.CASCADE, verbose_name=_('商品ID'))
    image_path = models.ImageField(verbose_name=_('画像パス'), upload_to='images/', unique=True)
    created_at = models.DateTimeField(_('作成日時'), auto_now_add=True)
    updated_at = models.DateTimeField(_('更新日時'), auto_now=True)

    class Meta:
        verbose_name = _('商品画像')
        verbose_name_plural = _('商品画像')

    def __str__(self):
        return '%s' % self.image_path.name

class ItemLike(models.Model):
    item = models.ForeignKey('Item', on_delete=models.CASCADE, verbose_name=_('商品ID'))
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, verbose_name=_('ユーザーID'))
    created_at = models.DateTimeField(_('作成日時'), auto_now_add=True)
    updated_at = models.DateTimeField(_('更新日時'), auto_now=True)

    class Meta:
        verbose_name = _('いいね')
        verbose_name_plural = _('いいね')

    def __str__(self):
        return '%s' % self.item.name + ': ' + self.user.username

class ItemRecommendation(models.Model):
    item = models.ForeignKey('Item', on_delete=models.CASCADE, verbose_name=_('商品ID'))
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, verbose_name=_('ユーザーID'))
    price = models.IntegerField(_('価格'))
    quantity = models.IntegerField(_('商品数'))
    description = models.TextField(_('説明文'), blank=True)
    recommendation_ranking = models.PositiveSmallIntegerField(_('おすすめ順'), blank=True, null=True, unique=True)
    expired_at = models.DateTimeField(_('掲載終了日'), blank=True)
    created_at = models.DateTimeField(_('作成日時'), auto_now_add=True)
    updated_at = models.DateTimeField(_('更新日時'), auto_now=True)

    class Meta:
        verbose_name = _('商品提案')
        verbose_name_plural = _('商品提案')

    def __str__(self):
        return '%s' % self.item.name
