from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.

class Table(models.Model):
    #n = models.IntegerField(null=False)
    #m = models.IntegerField(null=False)
    #points = ArrayField(models.CharField())
    result = ArrayField(models.IntegerField())
    time_in_sec = models.DecimalField(max_digits=30, decimal_places=20)
    max_memory_in_MB = models.DecimalField(max_digits=30, decimal_places=20)
