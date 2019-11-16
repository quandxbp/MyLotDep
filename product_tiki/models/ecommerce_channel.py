from django.db import models

from common.constants import *

import requests
import logging

_logger = logging.getLogger(__name__)


class Tiki(models.Model):
    class Meta:
        abstract = True

    def get_detail_data(self, product_id, spid=False):
        endpoint = "https://tiki.vn/api/v2/products/%s" % product_id
        if spid:
            endpoint = "https://tiki.vn/api/v2/products/%s?spid=%s" % (product_id, spid)
        print("Processing url %s " % endpoint)

        data = []
        try:
            response = requests.get(endpoint)
            if response.ok:
                data = response.json()
        except Exception as err:
            print("Error when getting Tiki product %s detail " % product_id)
            print(err)
        return data

    def tiki_get_data(self, max_records=20, limit=20, get_related_flag=True):
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
                        break
                    cur_product.extend(data)
                    page += 1

                except Exception as err:
                    print("Error when getting Tiki products ")
                    print(err)
            products.extend(cur_product)

        product_ids = [product.get('id') for product in products]
        existed_product_ids = Product.objects.filter(product_id__in=product_ids)
        new_products = list(filter(lambda p: p.get('id') not in existed_product_ids, products))
        # Get detail data of a product
        for product in new_products:
            data = self.get_detail_data(product.get('id'))
            product.update(data)

        if get_related_flag:
            related_products = []
            for product in new_products:
                if product.get('other_sellers'):
                    for rlp in product.get('other_sellers'):
                        spid = rlp.get('product_id')
                        data = self.get_detail_data(product.get('id'), spid)
                        related_products.append(data)
            new_products += related_products

        return new_products

    def tiki_get_top_data(self, max_records=250, limit=250):
        from product.models.product import Product
        top_products = []

        try:
            top_products = self.access_trade_id.get_top_products(MERCHANT['tiki']).get('data')
        except Exception as err:
            print("Error when requesting to Accesstrade")
            print(err)

        if top_products:
            for product in top_products:
                product_id = product.get('aff_link', '').split('-p')[-1].replace('.html', '').strip()
                product.update({'id': product_id})

            product_ids = [product.get('id') for product in top_products]
            existed_product_ids = Product.objects.filter(product_id__in=product_ids)
            new_products = list(filter(lambda p: p.get('id') not in existed_product_ids, top_products))

            # Update sequence of top_products
            if existed_product_ids:
                existed_product_ids.update(sequence=1)

            for product in new_products:
                data = self.get_detail_data(product.get('id'))
                product.update(data)

            return new_products

        return top_products

    def tiki_update_data(self):
        from product.models.product import Product

        products = Product.objects.filter(channel_id=self.id)

        update_products = [{'id': p.product_id,
                            'channel_id': p.channel_id} for p in products]

        for product in update_products[:10]:
            data = self.get_detail_data(product.get('id'))
            product.update(data)

        return update_products
