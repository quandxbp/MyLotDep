from django.db import models
from product_tiki.models.product import *

from .accesstrade import AccessTrade

from product_tiki.models.ecommerce_channel import Tiki
from product_adayroi.models.ecommerce_channel import Adayroi

from multiprocessing import Queue, Process

import time

class EcommerceChannel(Tiki, Adayroi):
    name = models.CharField(max_length=255)
    platform = models.CharField(max_length=50,
                                choices=[('tiki', 'Tiki'),
                                         ('lazada', 'Lazada'),
                                         ('adayroi', 'Adayroi')],
                                default='tiki')
    access_trade_id = models.ForeignKey(AccessTrade,
                                        default=1,
                                        verbose_name="Access Trade",
                                        on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def sync_channel_product(self, top_product=False):
        print("Start syncing Product Data in %s" % self.platform)
        cust_method_name = '%s_get_data' % self.platform if not top_product else '%s_get_top_data' % self.platform
        if hasattr(self, cust_method_name):
            from .product import Product

            products_data = getattr(self, cust_method_name)()
            # Update channel id in each product
            sequence = 1 if top_product else 0
            [product.update({'channel_id': self,
                             'sequence': sequence}) for product in products_data]
            # Synchronize products data

            NUMBER_OF_WORKERS = 4
            queue = Queue()
            start, uid = 0, 0
            step = int(len(products_data) / NUMBER_OF_WORKERS)
            while start < len(products_data):
                print("UID %s" % uid)
                PO = Product()
                end = start + step
                pattern = products_data[start:end]
                start = end

                queue.put(PO.sync_product_channel(uid, pattern))
                uid += 1
            time.sleep(0.1)

    def update_data_channel(self):
        print("Updating product data in %s" % self.platform)
        cust_method_name = '%s_update_data' % self.platform
        if hasattr(self, cust_method_name):
            from .product import Product
            PO = Product()

            products_data = getattr(self, cust_method_name)()
            PO.update_data_product_channel(products_data, update_mongo=True)


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
