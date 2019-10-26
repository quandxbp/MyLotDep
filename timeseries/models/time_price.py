from .mongo_connection import MongoDB
from product.models.product import Product

from common.utils import get_soup
from common.constants import DOMAIN

from multiprocessing import Pool

import datetime
import re
import json
import ast
import requests


class TimePrice:
    _collection_name = 'time_price'
    _conn = MongoDB(_collection_name)

    def create_price(self):
        product = Product.objects.filter(pk=1)
        product = product[0]
        today = datetime.date.today().strftime("%d-%m-%Y")
        cur_time = datetime.datetime.now().time()
        data = {
            'product_id': product.product_id,
            'url': product.url,
            'platform': product.channel_id.platform,
            'prices': {
                today: [
                    {
                        'price': float(product.price),
                        'at_time': str(cur_time),
                    }
                ]
            }
        }

        self._conn.insert_one(data)

    def initialize_data_time_price(self, get_price_func):
        res = []
        products = Product.objects.all()
        existed_products = self._conn.find_all(filter_fields={'_id': 0, 'product_id': 1})
        existed_products_ids = [p.get('product_id') for p in existed_products]
        new_products = filter(lambda p: p.product_id not in existed_products_ids, products)

        for p in new_products:
            print("Inserting %s" % p.url)
            prices = get_price_func(p.channel_id.platform, p.url)
            if not prices:
                continue
            data = {
                'product_id': p.product_id,
                'url': p.url,
                'platform': p.channel_id.platform,
                'prices': prices,
                'updated_date': str(datetime.datetime.now()),
                'created_date': str(datetime.datetime.now()),
            }
            res.append(data)
            self._conn.insert_one(data)

        # self._conn.insert_many(res)
        return True


"""
    "_id" : ObjectId,
    "product_id": string (unique),
    "url": string (unique),
    "platform": tiki, lazada, adayroi
    "prices": [
        Date:
        [
            {
                "price": decimal number,
                "at_time": time,
            }
        ]
    ],

    "updated_date: Date Time,
    "created_date: Date time
"""
