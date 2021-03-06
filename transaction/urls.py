from django.urls import path
from . import views

app_name = 'transaction'
urlpatterns = [
    path('order/', views.OrderView.as_view(), name='order'),
    path('order/confirm/<uuid:slug>/', views.OrderConfirmView.as_view(), name='order_confirm'),
    path('order/sent/<uuid:slug>/', views.OrderSentView.as_view(), name='order_sent'),
    path('order/accepted/<uuid:slug>/', views.OrderAcceptedView.as_view(), name='order_accepted'),
    path('order/cancel/<uuid:slug>/', views.OrderCancelView.as_view(), name='order_cancel'),
    path('delivery/method/<uuid:slug>/', views.DeliveryMethodView.as_view(), name='delivery_method'),
    path('delivery/select/<uuid:uuid>/', views.delivery_select, name='delivery_select'),
    path('delivery/post/<uuid:slug>/', views.DeliveryPostView.as_view(), name='delivery_post'),
    path('delivery/register/<uuid:uuid>/<int:id>/', views.delivery_register, name='delivery_register'),
    path('payment/<uuid:slug>/', views.PaymentView.as_view(), name='payment'),
]
