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
        search_field = {'spid': product.get('spid')}
        update_fields = {
            'platform': product.get('platform'),
            'product_id': product.get('product_id'),
            'url': product.get('url'),
            "updated_date": str(datetime.datetime.now()),
            'prices.{today}.{cur_time}'.format(today=str(today), cur_time=str(cur_time)): price
        }
        self.conn.update(search_field=search_field, update_fields=update_fields)

    def get_price_by_spid(self, spid):
        data = self.conn.find_one({'spid': spid}, ['prices'])

        labels, prices = [], []
        if data:
            if data.get('prices', False):
                price_len, count = len(data.get('prices')), 0
                old_date, old_price, = False, 0
                for date, time_n_price in data.get('prices').items():
                    count += 1
                    if '1970' in date or date == old_date:
                        continue
                    for time, price in time_n_price.items():
                        if price == old_price and price_len != count:
                            continue
                        if price_len == count:  # Only get one record in the last date
                            count += 1
                        format_date = datetime.datetime.strptime(date, '%d-%m-%Y').strftime('%m-%d-%Y')
                        label = "%s" % format_date

                        labels.append(label)
                        prices.append(price)
                        old_price = price
                    old_date = date

        # Reverse two list because data returned in opposite side
        return labels, prices

    def get_price_list_by_spid(self, spid):
        data = self.conn.find_one({'spid': spid}, ['prices'])

        res = []
        if data:
            if data.get('prices', False):
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

    def get_special_price_statistics(self, spid):
        data = self.conn.find_one({'spid': spid}, ['prices'])
        res = {
            'highest': ('Chưa có dữ liệu', 0),
            'lowest': ('Chưa có dữ liệu', 0),
            'average': 0,
            'period': 0,
        }

        if data:
            if data.get('prices', False):
                prices = data.get('prices')
                limit, highest, lowest = 50, 0, float('inf')
                average, average_count = 0, 0
                old_price = 0

                price_lst = [(date, time_n_price) for date, time_n_price in prices.items()]
                price_lst.reverse()

                today = datetime.datetime.today()
                last_date = False
                for price_element in price_lst[:50]:
                    date = price_element[0]
                    time_n_price = price_element[1]

                    # Calculate period
                    last_date = datetime.datetime.strptime(str(date), "%d-%m-%Y")
                    if '1970' in date:
                        continue
                    for time, price in time_n_price.items():
                        dt_str = "%s %s" % (date, time)
                        # Get highest price
                        if price > highest:
                            highest = price
                            res['highest'] = (dt_str, price)
                        # Get lowest price
                        if price < lowest:
                            lowest = price
                            res['lowest'] = (dt_str, price)

                        # Calculate average price of the product
                        if old_price != price:
                            average += price
                            average_count += 1
                            old_price = price
                res['average'] = int(average / average_count)
                res['period'] = (today - last_date).days

        return res

    def create_price(self, product):
        today = datetime.date.today().strftime("%d-%m-%Y")
        cur_time = datetime.datetime.now().time()
        data = {
            'product_id': product.product_id,
            'spid': product.spid,
            'url': product.url,
            'platform': product.channel_id.platform,
            'prices': {
                today: [{
                    str(cur_time): float(product.price),
                }]
            },
            'updated_date': str(datetime.datetime.now()),
            'created_date': str(datetime.datetime.now()),
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
                'spid': p.spid,
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
