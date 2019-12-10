from django.db import models
from .product import Product


class Image(models.Model):

    url = models.CharField(max_length=256)
    alter_text = models.CharField(max_length=256, blank=True)
    product_id = models.ForeignKey(Product,
                                   null=True,
                                   verbose_name="Products",
                                   on_delete=models.CASCADE)
