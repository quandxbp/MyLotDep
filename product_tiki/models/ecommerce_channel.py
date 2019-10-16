from django.db import models

from common.utils import *

import requests
import re
import logging
import ast

_logger = logging.getLogger(__name__)


class Tiki(models.Model):
    class Meta:
        abstract = True
        app_label = 'productdb'

    def tiki_get_data(self):

        products = []

        page, limit = 1, 250
        while True:
            endpoint = 'https://tiki.vn/api/v2/products?category=1789&page=%s&limit=%s' % (page, limit)
            print("Processing: %s" % endpoint)
            try:
                data = []
                response = requests.get(endpoint)
                if response.ok:
                    data = response.json().get('data')
                    if len(data) == 0:
                        break
                else:
                    break
                products.extend(data)
                page += 1

            except Exception as err:
                print("Error when getting Tiki products ")
                print(err)

        # Get detail data of a product
        for product in products:
            product_id = product.get('id')
            endpoint = "https://tiki.vn/api/v2/products/%s" % product_id
            print("Processing url %s " % endpoint)
            try:
                data = []
                response = requests.get(endpoint)
                if response.ok:
                    data = response.json()
                product.update(data)
            except Exception as err:
                print("Error when getting Tiki product %s detail " % product_id)
                print(err)

        return products
