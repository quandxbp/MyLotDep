from django.db import models
from .product import Product


class Specification(models.Model):
    name = models.CharField(max_length=255, blank=True)
    value = models.CharField(max_length=255, blank=True)

    product_id = models.ForeignKey(Product,
                                   default=1,
                                   verbose_name="Product",
                                   on_delete=models.CASCADE)


