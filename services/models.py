import datetime

from django.db import models
from django.utils import timezone

class Service(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    slug = models.SlugField(unique=True)

class Price(models.Model):
    def __str__(self):
        return self.service_price 

