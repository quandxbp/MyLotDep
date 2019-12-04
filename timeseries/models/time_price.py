from .mongo_connection import MongoDB
from product.models.product import Product

import datetime
import csv


class TimePrice:
    _collection_name = 'time_price'
    conn = MongoDB(_collection_name)

    def _format_price(self, price_list):
        new_prices = []
        for price in price_list:
            price = format(int(price), ',d').replace(',', '.')
            new_prices.append(price)
        return new_prices

    def get_all_by_platform(self, platform):
        search_fields = {'platform': platform}
        records = self.conn.find_all_by(search_fields=search_fields)

        return records

    def update_price(self, product, price):
        today = datetime.date.today().strftime("%d-%m-%Y")
        cur_time = datetime.datetime.now().time().strftime("%H:%M:%S")
        search_field = {'product_id': product.get('product_id')}
        update_fields = {
            'platform': product.get('platform'),
            'url': product.get('url'),
            "updated_date": str(datetime.datetime.now()),
            'prices.{today}.{cur_time}'.format(today=str(today), cur_time=str(cur_time)): price
        }
        self.conn.update(search_field=search_field, update_fields=update_fields)

    def get_price_by_id(self, product_id):
        data = self.conn.find_one({'product_id': product_id}, ['prices'])

        labels, prices = [], []
        if data.get('prices'):
            old_price, count = 0, 0
            for date, time_n_price in data.get('prices').items():
                for time, price in time_n_price.items():
                    if price == old_price and count != 4:
                        count += 1
                        continue
                    format_date = datetime.datetime.strptime(date, '%d-%m-%Y').strftime('%m-%d-%Y')
                    label = "%s" % format_date
                    labels.append(label)
                    prices.append(price)
                    old_price = price
                    count = 0
        # Reverse two list because data returned in wrong side
        return labels, prices

    def get_price_list_by_id(self, product_id):
        data = self.conn.find_one({'product_id': product_id}, ['prices'])

        res = []
        if data.get('prices'):
            for date, time_n_price in data.get('prices').items():
                if '1970' in date:
                    continue
                for time, price in time_n_price.items():
                    dt_str = "%s %s" % (date, time)
                    format_dt = datetime.datetime.strptime(dt_str, "%d-%m-%Y %H:%M:%S")
                    reformat_dt = datetime.datetime.strftime(format_dt, "%m-%d-%Y %H:%M:%S")
                    res.append({"Date": str(reformat_dt),
                                "Price": price})
        res.reverse()
        return res

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
                        str(cur_time): float(product.price),
                    }
                ]
            }
        }

        self.conn.insert_one(data)

    def initialize_data_time_price(self, get_price_func):
        res = []
        products = Product.objects.all()
        existed_products = self.conn.find_all(filter_fields={'_id': 0, 'product_id': 1})
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
            self.conn.insert_one(data)

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
                time: decimal number,
            }
        ]
    ],

    "updated_date: Date Time,
    "created_date: Date time
"""
