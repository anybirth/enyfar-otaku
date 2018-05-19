from django.urls import path
from . import views

app_name = 'main'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('category/<int:pk>', views.CategoryView.as_view(), name='category'),
]
