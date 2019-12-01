from django.db import models
from .product import Product


class Image(models.Model):

    url = models.URLField()
    product_id = models.ForeignKey(Product,
                                   null=True,
                                   verbose_name="Products",
                                   on_delete=models.CASCADE)
