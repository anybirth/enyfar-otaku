from django.contrib import admin
from . import models

# Register your models here.

admin.site.register([models.Category, models.Tag, models.Item, models.ItemImage, models.ItemLike,])
