from django.db import models
from product_tiki.models.product import *

from .accesstrade import AccessTrade

from product_tiki.models.ecommerce_channel import Tiki
from product_adayroi.models.ecommerce_channel import Adayroi

from multiprocessing import Queue, Process

import time
import logging


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
        logging.info("Start syncing Product Data in %s" % self.platform)
        cust_method_name = '%s_get_data' % self.platform if not top_product else '%s_get_top_data' % self.platform
        if hasattr(self, cust_method_name):
            from .product import Product

            products_data = getattr(self, cust_method_name)()
            # Update channel id in each product
            sequence = 1 if top_product else 0
            for product in products_data:
                if isinstance(product, list):
                    products_data.remove(product)
                    continue
                product.update({'channel_id': self,
                                'platform': self.platform,
                                'sequence': sequence})
            # Synchronize products data

            NUMBER_OF_WORKERS = 4
            queue = Queue()
            start, uid = 0, 0
            step = int(len(products_data) / NUMBER_OF_WORKERS)
            Product = Product()
            while start < len(products_data):
                print("UID %s" % uid)
                end = start + step
                pattern = products_data[start:end]
                start = end

                queue.put(Product.sync_product_channel(uid, pattern))
                uid += 1
            time.sleep(0.1)

    def update_data_channel(self):
        logging.info("Updating product data in %s" % self.platform)
        cust_method_name = '%s_update_data' % self.platform
        if hasattr(self, cust_method_name):
            from .product import Product
            PO = Product()

            products_data = getattr(self, cust_method_name)()
            PO.update_data_product_channel(products_data, update_mongo=True)

    def update_data_channel_mongo(self):
        logging.info("Updating product data from Mongo in %s" % self.platform)
        cust_method_name = '%s_update_data_mongo' % self.platform
        if hasattr(self, cust_method_name):
            from .product import Product
            PO = Product()

            products_data = getattr(self, cust_method_name)()
            PO.update_data_product_channel_mongo(products_data, update_sql=False)

    def generate_accesstrade_headers(self):
        return {
            'Authorization': "Token %s" % self.access_trade_id.accesstrade_access_key
        }
