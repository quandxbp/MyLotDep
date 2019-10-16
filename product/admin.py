from django.contrib import admin

from .models.product import Product
from .models.image import Image
from .models.ecommerce_channel import EcommerceChannel
from .models.related_product import RelatedProduct
from .models.accesstrade import AccessTrade
# Register your models here.

admin.site.register(Product)

admin.site.register(Image)

admin.site.register(EcommerceChannel)

admin.site.register(RelatedProduct)

admin.site.register(AccessTrade)
