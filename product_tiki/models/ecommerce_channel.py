from django.db import models

from common.constants import *

import requests
import logging

class Tiki(models.Model):
    class Meta:
        abstract = True

    def tiki_get_detail_data(self, product_id, spid=False):
        if spid:
            endpoint = "https://tiki.vn/api/v2/products/%s?spid=%s" % (product_id, spid)
        else:
            endpoint = "https://tiki.vn/api/v2/products/%s" % product_id
        logging.info("Processing url in get detail data %s " % endpoint)

        data = []
        try:
            response = requests.get(endpoint)
            if response.ok:
                data = response.json()
        except Exception as err:
            logging.error("Error when getting Tiki product %s detail " % product_id)
            logging.error(err)
        return data

    def tiki_get_data(self, max_records=1000, limit=250, get_related_flag=True):
        from product.models.product import Product

        products = []
        for categ in CATEGORY['tiki']:
            cur_product = []
            page = 1
            while True and len(cur_product) < max_records:
                endpoint = 'https://tiki.vn/api/v2/products?category={categ}&page={page}&limit={limit}'. \
                    format(categ=categ, page=page, limit=limit)
                print("Processing: %s" % endpoint)
                try:
                    data = []
                    response = requests.get(endpoint)
                    if response.ok:
                        data = response.json().get('data')
                        if len(data) == 0:
                            break
                    else:
                        continue
                    cur_product.extend(data)
                    page += 1

                except Exception as err:
                    print("Error when getting Tiki products ")
                    print(err)
            products.extend(cur_product)

        product_ids = [product.get('current_seller', {}).get('product_id') for product in products]
        existed_product_ids = Product.objects.filter(spid__in=product_ids)
        new_products = list(filter(lambda p: p.get('current_seller', {}).get('product_id') not in existed_product_ids,
                                   products))

        # Get detail data of a product
        # new_products = [{'id': 32028822, 'spid': 32028824}]
        for product in new_products:
            # data = self.tiki_get_detail_data(product.get('id'), product.get('spid'))
            data = self.tiki_get_detail_data(product.get('id'))
            product.update(data)

        if get_related_flag:
            related_products = []
            for product in new_products:
                if product.get('other_sellers'):
                    for rlp in product.get('other_sellers'):
                        data = self.tiki_get_detail_data(product.get('id'), rlp.get('product_id'))
                        related_products.append(data)
            new_products += related_products

        return new_products

    def tiki_get_top_data(self, max_records=250, limit=250, get_related_flag=True):
        from product.models.product import Product
        top_products = []

        try:
            top_products = self.access_trade_id.get_top_products(MERCHANT['tiki']).get('data')
        except Exception as err:
            logging.error("Error when requesting to Accesstrade")
            logging.error(err)

        if top_products:
            elec_products = []
            for product in top_products:
                if product.get('product_category') == '1789':
                    product_id = product.get('aff_link', '').split('-p')[-1].replace('.html', '').strip()
                    product.update({'id': product_id})
                    elec_products.append(product)

            product_ids = [product.get('id') for product in elec_products]
            existed_product_ids = Product.objects.filter(product_id__in=product_ids)
            new_products = list(filter(lambda p: p.get('id') not in existed_product_ids, elec_products))

            # Update sequence of top_products
            if existed_product_ids:
                existed_product_ids.update(sequence=1)

            for product in new_products:
                data = self.tiki_get_detail_data(product.get('id'))
                product.update(data)

            if get_related_flag:
                related_products = []
                for product in new_products:
                    if product.get('other_sellers'):
                        for rlp in product.get('other_sellers'):
                            data = self.tiki_get_detail_data(product.get('id'), rlp.get('product_id'))
                            related_products.append(data)
                new_products += related_products

            return new_products

        return []

    def tiki_update_data(self, limit=False):
        from product.models.product import Product

        products = Product.objects.filter(channel_id=self.id)

        if limit:
            products = products[:limit]
        update_products = [{'id': p.product_id,
                            'spid': p.spid,
                            'platform': self.platform} for p in products]

        for product in update_products:
            data = self.tiki_get_detail_data(product.get('id'), product.get('spid'))
            product.update(data)

        return update_products

    def tiki_update_data_mongo(self, limit=False):
        from timeseries.models.time_price import TimePrice
        TP = TimePrice()

        products = TP.get_all_by_platform(self.platform)
        update_products = [{'id': p.get('product_id'),
                            'spid': p.get('spid'),
                            'platform': self.platform} for p in products]
        for product in update_products:
            data = self.tiki_get_detail_data(product.get('id'), product.get('spid'))
            product.update(data)

        return update_products

