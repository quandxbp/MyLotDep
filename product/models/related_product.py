from django.db import models
from .product import Product

from decimal import Decimal

class RelatedProduct(models.Model):
    product_id = models.CharField(max_length=255, blank=True)
    main_product_id = models.CharField(max_length=255, blank=True)
    name = models.CharField(max_length=255, blank=True)
    url_key = models.CharField(max_length=255, blank=True)
    platform = models.CharField(max_length=255, blank=True)
    ld_url = models.CharField(max_length=255, blank=True)
    price = models.DecimalField(max_digits=20, decimal_places=0, default=Decimal('0'))
    related_product_id = models.ForeignKey(Product,
                                           default=1,
                                           verbose_name="Product",
                                           on_delete=models.CASCADE)
