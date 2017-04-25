from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Package(models.Model):
    p_id = models.AutoField(primary_key=True) #customed primary key
    p_name = models.CharField(max_length=100)
    status = models.CharField(max_length=20)
    x_loc = models.IntegerField()
    y_loc = models.IntegerField()
    user = models.OneToOneField(User)

    def __str__(self):
        return self.p_name

