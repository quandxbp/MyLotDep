from django.db import models

import requests


class AdayroiProduct(models.Model):
    class Meta:
        abstract = True

    def adayroi_standardize_data(self, product_data):
        url = 'https://adayroi.com/%s' % product_data.get('url')

        brand = {
            'name': product_data.get('brandName'),
            'slug': product_data.get('brandName').lower()
        }

        categories = {
            'name': product_data.get('categoryPath')
        }

        thumbnail_url = False
        if product_data.get('images'):
            thumbnail = product_data.get('images')[0]
            thumbnail_url = thumbnail.get('url')

        product_data.update({
            'id_on_channel': product_data.get('baseProductCode'),
            'url': url,
            'sku': product_data.get('productSKU'),
            'quantity': product_data.get('stock', {}).get('stockLevel', 0),
            'price': product_data.get('price', {}).get('value', 0.0),
            'list_price': product_data.get('productPrice', {}).get('value', 0.0),
            'thumbnail_url': thumbnail_url,
            'brand': brand,
            'category': categories
        })

        return product_data
