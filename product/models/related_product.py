from django.db import models
from .product import Product

from decimal import Decimal

class RelatedProduct(models.Model):
    product_id = models.CharField(max_length=255, blank=True)
    main_product_id = models.CharField(max_length=255, blank=True)
    platform = models.CharField(max_length=255, blank=True)
    url_path = models.CharField(max_length=255, blank=True)
    ld_url = models.CharField(max_length=255, blank=True)
    related_product_id = models.ForeignKey(Product,
                                           default=1,
                                           verbose_name="Product",
                                           on_delete=models.CASCADE)
