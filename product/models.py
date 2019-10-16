from django.db import models

from .models import *
# Create your models here.
from decimal import Decimal


class Product(models.Model):
    class Meta:
        app_label = 'timeseriesdb'

    product_id = models.CharField(max_length=255, blank=True)
    price = models.DecimalField(max_digits=20, decimal_places=4, default=Decimal('0.0000'))

