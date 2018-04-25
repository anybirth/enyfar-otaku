from django.shortcuts import render
from django.views import generic
from . import models

# Create your views here.

class IndexView(generic.ListView):
    model = models.Item
    context_object_name = 'items'
    template_name = 'main/index.html'
