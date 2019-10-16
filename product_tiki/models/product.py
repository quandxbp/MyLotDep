from django.db import models

import logging

_logger = logging.getLogger(__name__)


class TikiProduct(models.Model):
    class Meta:
        abstract = True
        app_label = 'productdb'

    def tiki_standardize_data(self, product_data):
        url = 'https://tiki.vn/%s' % product_data.get('url_path')
        cur_seller = product_data.get('current_seller', {})
        product_data.update({
            'product_id': product_data.get('id'),
            'seller_product_id': cur_seller.get('product_id', ' '),
            'seller_sku': cur_seller.get('sku', ' '),
            'url': url,
            'thumbnail_url': product_data.get('thumbnail_url'),
            'brand': product_data.get('brand'),
            'category': product_data.get('categories')
        })

        return product_data
