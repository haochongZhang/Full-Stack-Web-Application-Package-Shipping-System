from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Truck(models.Model):
    truck_id = models.AutoField(primary_key=True) #customed primary key
    status = models.CharField(max_length=20)
    x_loc = models.IntegerField()
    y_loc = models.IntegerField()

    def __str__(self):
        return self.truck_id    #???

class Shipment(models.Model):
    shipment_id = models.AutoField(primary_key=True) #customed primary key
    shipment_id = models.CharField(max_length=100)
    status = models.CharField(max_length=20) 
    dest_addr_x = models.IntegerField()
    dest_addr_y = models.IntegerField()
    truck = models.ForeignKey(Truck, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.s_name

class Item(models.Model):
    item_id = models.AutoField(primary_key=True) #customed primary key  
    item_name = models.CharField(max_length=100)
    count = models.IntegerField()
    shipment = models.ForeignKey(Shipment, on_delete=models.CASCADE)

    def __str__(self):
        return self.item_name

