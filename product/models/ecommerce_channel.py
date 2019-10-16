from django.db import models
from product_tiki.models.product import *

from .accesstrade import AccessTrade

from bs4 import BeautifulSoup

from product_tiki.models.ecommerce_channel import Tiki
from product_adayroi.models.ecommerce_channel import Adayroi

import logging
from urllib.request import urlopen, Request

import requests


_logger = logging.getLogger(__name__)


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
        _logger.info("Start syncing Product Data in %s" % self.platform)
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
            _logger.error("Error when requesting :%s" % api_function)
            _logger.error(err)
        return response

    def generate_accesstrade_headers(self):
        return {
            'Authorization': "Token %s" % self.access_trade_id.accesstrade_access_key
        }

    def _get_soup(self, url):
        print("Processing url %s" % url)
        headers = {'User-Agent': 'User-Agent:Mozilla/5.0'}

        response = Request(url, headers=headers)
        data = urlopen(response).read()
        soup = BeautifulSoup(data, "lxml")

        return soup
