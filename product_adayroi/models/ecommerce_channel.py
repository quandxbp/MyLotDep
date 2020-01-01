from django.db import models

import requests
import logging


class Adayroi(models.Model):
    class Meta:
        abstract = True

    def adayroi_get_detail_data(self, base_product_code, offer_code):
        endpoint = "https://rest.adayroi.com/cxapi/v2/adayroi/product/detail?fields=FULL&productCode=%s&offerCode=%s" \
                   % (base_product_code, offer_code)
        logging.info("Processing url in getting detail data %s " % endpoint)

        data = []
        try:
            response = requests.get(endpoint)
            if response.ok:
                data = response.json()
        except Exception as err:
            logging.error("Error when getting Adayroi product %s detail " % base_product_code)
            logging.error(err)
        return data

    def adayroi_get_data(self, max_records=4, limit=250, get_related_flag=True, pagination_flag=True):
        from product.models.product import Product
        products = []

        total_page, page = 1, 0
        while page < max_records:
            endpoint = "https://rest.adayroi.com/cxapi/v2/adayroi/search?fields=FULL&q&categoryCode=322&pageSize=%s&currentPage=%s" % (
                limit, page)
            logging.info("Processing: %s" % endpoint)
            try:
                data = []
                response = requests.get(endpoint)
                if response.ok:
                    json_data = response.json()
                    data = json_data.get('products')
                    if pagination_flag:
                        total_page = json_data.get('pagination').get('totalPages')
                        pagination_flag = False
                        if max_records < total_page:
                            max_records = total_page
                products.extend(data)

            except Exception as err:
                logging.error("Error when getting Adayroi products ")
                logging.error(err)
            page += 1

        # Get detail data of a product
        filter_products = [p for p in products if p.get('baseProductCode').isdigit()]
        product_codes = [product.get('code') for product in filter_products]
        existed_product_ids = Product.objects.filter(spid__in=product_codes)
        new_products = list(filter(lambda p: p.get('code') not in existed_product_ids, filter_products))
        # Get detail data of a product
        for product in new_products:
            base_product_code = product.get('baseProductCode')
            offer_code = product.get('code')
            data = self.adayroi_get_detail_data(base_product_code, offer_code)
            product.update(data)

        if get_related_flag:
            related_products = []
            for product in new_products:
                if product.get('offers'):
                    for rlp in product.get('offers'):
                        data = self.adayroi_get_detail_data(base_product_code=product.get('baseProduct'),
                                                            offer_code=rlp.get('code'))
                        related_products.append(data)
            new_products += related_products
        return new_products

    def adayroi_update_data(self, limit=False):
        from product.models.product import Product

        products = Product.objects.filter(channel_id=self.id)

        if limit:
            products = products[:limit]
        update_products = [{'id': p.product_id,
                            'spid': p.spid,
                            'platform': self.platform} for p in products]

        for product in update_products:
            data = self.adayroi_get_detail_data(product.get('id'), product.get('spid'))
            product.update(data)

        return update_products

    def adayroi_update_data_mongo(self, limit=False):
        from timeseries.models.time_price import TimePrice
        TP = TimePrice()

        products = TP.get_all_by_platform(self.platform)
        update_products = [{'id': p.get('product_id'),
                            'spid': p.get('spid'),
                            'platform': self.platform} for p in products if p.get('spid') not in [1, '1']]
        for product in update_products:
            data = self.adayroi_get_detail_data(product.get('id'), product.get('spid'))
            product.update(data)

        return update_products
