from django.db import models
from product_tiki.models.product import *

from .accesstrade import AccessTrade

from product_tiki.models.ecommerce_channel import Tiki
from product_adayroi.models.ecommerce_channel import Adayroi

class EcommerceChannel(Tiki, Adayroi):
    name = models.CharField(max_length=255)
    platform = models.CharField(max_length=50,
                                choices=[('tiki', 'Tiki'),
                                         ('lazada', 'Lazada'),
                                         ('adayroi', 'Adayroi')])
    access_trade_id = models.ForeignKey(AccessTrade,
                                        default=1,
                                        verbose_name="Access Trade",
                                        on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def sync_channel_product(self):
        print("Start syncing Product Data in %s" % self.platform)
        cust_method_name = '%s_get_data' % self.platform
        if hasattr(self, cust_method_name):
            from .product import Product
            products_data = getattr(self, cust_method_name)()
            [product.update({'channel_id': self}) for product in products_data]
            # Synchronize products data
            Product.sync_product_channel(products_data)

    def _send_request(self, api_function, **kwargs):
        response = None
        try:
            response = api_function(**kwargs)
        except Exception as err:
            print("Error when requesting :%s" % api_function)
            print(err)
        return response

    def generate_accesstrade_headers(self):
        return {
            'Authorization': "Token %s" % self.access_trade_id.accesstrade_access_key
        }
