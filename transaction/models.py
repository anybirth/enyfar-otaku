from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.

class Proposal(models.Model):
    item = models.ForeignKey('main.Item', on_delete=models.CASCADE, verbose_name=_('商品ID'))
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, verbose_name=_('ユーザーID'))
    itinerary = models.ForeignKey('accounts.Itinerary', on_delete=models.CASCADE, verbose_name=_('旅程ID'))
    title = models.CharField(_('提案タイトル'), max_length=50)
    description = models.TextField(_('提案説明文'), blank=True)
    delivery_method = models.SmallIntegerField(_('配送方法'))
    payment_method = models.SmallIntegerField(_('支払方法'))
    price_proposal = models.IntegerField(_('価格提案'), blank=True)
    hand_place = models.CharField(_('商品手渡し場所'), max_length=255, blank=True)
    delivered_at = models.DateTimeField(_('予定お届け日時'), blank=True, null=True)
    status = models.SmallIntegerField(_('状態'), default=0)
    expired_at = models.DateTimeField(_('掲載終了日'), blank=True)
    created_at = models.DateTimeField(_('作成日時'), auto_now_add=True)
    updated_at = models.DateTimeField(_('更新日時'), auto_now=True)

    class Meta:
        verbose_name = _('提案')
        verbose_name_plural = _('提案')

    def __str__(self):
        return '%s' % self.user.username

class Order(models.Model):
    item = models.ForeignKey('main.Item', on_delete=models.CASCADE, verbose_name=_('商品ID'))
    requester = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='requester_set', verbose_name=_('リクエスターID'))
    traveller = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='traveller_set', verbose_name=_('トラベラーID'), blank=True, null=True)
    requester_address = models.ForeignKey('accounts.UserAddress', on_delete=models.CASCADE, verbose_name=_('リクエスター住所ID'), blank=True, null=True)
    uuid = models.UUIDField('ユニークID', primary_key=False)
    title = models.CharField(_('リクエストタイトル'), max_length=50, blank=True)
    description = models.TextField(_('リクエスト説明文'), blank=True)
    number = models.IntegerField(_('個数'))
    delivery_method = models.SmallIntegerField(_('配送方法'), blank=True, null=True)
    delivered_at_order = models.DateTimeField(_('希望お届け日時'), blank=True, null=True)
    hand_place = models.CharField(_('商品手渡し場所'), max_length=255, blank=True)
    payment_method = models.SmallIntegerField(_('支払方法'), blank=True, null=True)
    price_order = models.IntegerField(_('希望価格'), blank=True, null=True)
    price = models.IntegerField(_('価格'), blank=True, null=True)
    postage = models.IntegerField(_('送料'), default=0)
    status = models.SmallIntegerField(_('状態'), default=1)
    status_deadline = models.DateTimeField(_('状態有効期限'), blank=True, null=True)
    expired_at = models.DateTimeField(_('掲載終了日'), blank=True, null=True)
    created_at = models.DateTimeField(_('作成日時'), auto_now_add=True)
    updated_at = models.DateTimeField(_('更新日時'), auto_now=True)

    class Meta:
        verbose_name = _('依頼')
        verbose_name_plural = _('依頼')

    def __str__(self):
        return '%s' % self.user.username
