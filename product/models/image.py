from django.db import models
from .product import Product


class Image(models.Model):

    name = models.CharField(max_length=255, blank=True)
    url = models.URLField()
    image = models.ImageField(upload_to="images/%Y/%m/%D/")
    description = models.TextField(blank=True)

    product_id = models.ForeignKey(Product,
                                   null=True,
                                   verbose_name="Products",
                                   on_delete=models.CASCADE)
