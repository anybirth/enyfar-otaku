from django.shortcuts import render
from django.views import generic
from . import models
from transaction.models import Order

# Create your views here.

class IndexView(generic.ListView):
    model = models.Item
    context_object_name = 'items'
    template_name = 'main/index.html'

    def get_queryset(self):
        return models.Item.objects.order_by('created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = models.Category.objects.all()
        context['recommended_categories'] = models.Category.objects.order_by('recommendation_ranking')[:3]
        context['orders'] = Order.objects.filter(status=0).order_by('-created_at')

        context['recommended_items_array'] = []
        context['new_items_array'] = []

        all_recommended_items = models.Item.objects.order_by('recommendation_ranking').values()
        all_new_items = models.Item.objects.order_by('-created_at').values()
        for recommended_item, new_item in zip(all_recommended_items, all_new_items):
            recommended_item['category_id'] = 0
            new_item['category_id'] = 0
        context['recommended_items_array'].append(all_recommended_items)
        context['new_items_array'].append(all_new_items)

        for category in context['categories']:
            recommended_items = models.Item.objects.filter(category=category).order_by('recommendation_ranking').values()
            new_items = models.Item.objects.filter(category=category).order_by('-created_at').values()
            for recommended_item, new_item in zip(recommended_items, new_items):
                recommended_item['category_id'] = category.id
                new_item['category_id'] = category.id
            context['recommended_items_array'].append(recommended_items)
            context['new_items_array'].append(new_items)
        return context

class CategoryView(generic.DetailView):
    model = models.Category
    context_object_name = 'category'
    template_name = 'main/item_list.html'
