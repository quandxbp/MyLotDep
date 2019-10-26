from django.db import models

import requests

import logging

_logger = logging.getLogger(__name__)

class AccessTrade(models.Model):

    # TODO: Hashing the accesstrade key
    accesstrade_access_key = models.CharField(max_length=255, blank=True,
                                              default='hIAO1n_PcfcRwUIKcpMqnJneuGQ-YrtC')
    accesstrade_secret_key = models.CharField(max_length=255, blank=True,
                                              default='obzlw+lj@f5)orhvn95-(f@t2pg_srm0')

    def __str__(self):
        return "AccessTrade-%s" % self.id

    def generate_accesstrade_headers(self):
        return {
            'Authorization': "Token %s" % self.accesstrade_access_key
        }

    def get_product_detail_by_id(self, merchant, product_id):
        headers = self.generate_accesstrade_headers()
        endpoint = "https://api.accesstrade.vn/v1/product_detail?merchant=%s&product_id=%s" % (merchant, product_id)
        response = requests.get(url=endpoint, headers=headers).json()

        return response

    def get_data_feeds_by_sku(self, domain, sku):
        headers = self.generate_accesstrade_headers()
        endpoint = "https://api.accesstrade.vn/v1/datafeeds?domain=%s&sku=%s" % (domain, sku)
        response = requests.get(url=endpoint, headers=headers).json()

        return response

    def get_top_products(self, merchant):
        headers = self.generate_accesstrade_headers()
        endpoint = "https://api.accesstrade.vn/v1/top_products?merchant=%s" % merchant
        response = requests.get(url=endpoint, headers=headers).json()

        return response