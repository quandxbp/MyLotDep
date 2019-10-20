from .mongo_connection import MongoDB
from product.models.product import Product

from common.utils import get_soup
from common.constants import DOMAIN

from multiprocessing import Pool

import datetime
import re
import json


class TimePrice:
    _collection_name = 'time_price'
    _conn = MongoDB()

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

        self._conn.insert_one(self._collection_name, data)

    def _process_raw_url(self, raw_url):
        if 'http' in raw_url:
            raw_url = raw_url.split('/', 3)[-1]
        if '.html' in raw_url:
            raw_url = raw_url.split('.html')[0]

        return raw_url

    def initialize_data_time_price(self):
        res = []
        products = Product.objects.all()
        for p in products:
            print("Inserting %s" % p.url)
            raw_url = self._process_raw_url(p.url)
            prices = self.get_data_jajum(p.channel_id.platform, raw_url)
            if not prices:
                continue
            res.append({
                'product_id': p.product_id,
                'url': raw_url,
                'platform': p.channel_id.platform,
                'prices': prices,
                'updated_date': datetime.datetime.now(),
                'created_date': datetime.datetime.now()
            })

        self._conn.insert_many(self._collection_name, res)
        return True

    def get_data_jajum(self, platform, raw_url):
        processed_url = self._process_raw_url(raw_url)
        jajum_url = "https://jajum.com/products/{domain}/{product_url}". \
            format(domain=DOMAIN[platform], product_url=processed_url)

        soup = get_soup(jajum_url)
        res = {}

        if soup:
            pattern = re.compile('datasets.*borderColor')
            script = soup.find("script", text=pattern).text
            datasets = re.search(r'\[{(.*?)}\]', script, re.MULTILINE | re.DOTALL)

            if datasets:
                datasets = datasets.group(0).strip()
                datasets = datasets.split('\"data\":')[1]
                data_list = json.loads(datasets)

                for record in data_list:
                    timestamp = record.get('x')
                    price = record.get('y')
                    date_time = datetime.datetime.fromtimestamp(float(timestamp) / 1e3)
                    only_date = date_time.strftime("%d-%m-%Y")
                    only_time = date_time.time()

                    if res.get(only_date):
                        res[only_date].update({only_time: price})
                    else:
                        res[only_date] = {only_time: price}

        return res


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
