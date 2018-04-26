from django.shortcuts import render
from django.views import generic
from . import models
from transaction.models import Order

# Create your views here.

class IndexView(generic.TemplateView):
    template_name = 'main/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recommended_categories'] = models.Category.objects.order_by('recommendation_ranking')[:3]
        return context
