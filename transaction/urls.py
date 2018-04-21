from django.urls import path
from . import views

app_name = 'transaction'
urlpatterns = [
    path('order/', views.OrderView.as_view(), name='order'),
    path('order/confirm/<uuid:slug>/', views.OrderConfirmView.as_view(), name='order_confirm'),
    path('order/sent/<uuid:slug>/', views.OrderSentView.as_view(), name='order_sent'),
    path('order/accepted/<uuid:slug>/', views.OrderAcceptedView.as_view(), name='order_accepted'),
    path('delivery/method/<uuid:slug>/', views.DeliveryMethodView.as_view(), name='delivery_method'),
    path('delivery/select/<uuid:uuid>/', views.delivery_select, name='delivery_select'),
    path('delivery/post/<uuid:slug>/', views.DeliveryPostView.as_view(), name='delivery_post'),
]
