from django.contrib import admin
from . import models

# Register your models here.

admin.site.register([models.User, models.Member, models.MemberAddress, models.Itinerary, models.Transfer, models.Departure, models.Arrival,])
