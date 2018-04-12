from django.urls import path
from . import views

urlpatterns = [
    path('order/', views.OrderView.as_view(), name='order'),
    path('order/confirm/<uuid:slug>/', views.OrderConfirmView.as_view(), name='order_confirm'),
]
