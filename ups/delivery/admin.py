from django.contrib import admin
from .models import Truck, Shipment, Item

# Register your models here.
admin.site.register(Truck)
admin.site.register(Shipment)
admin.site.register(Item)