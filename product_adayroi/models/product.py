from django.db import models

import requests
import logging


class AdayroiProduct(models.Model):
    class Meta:
        abstract = True

    def _adayroi_get_provider(self, provider_data):
        if provider_data:
            provider_data['id'] = provider_data.get('merchantId')
            provider_data['name'] = provider_data.get('merchantName', 'Adayroi Seller')
            provider_data['is_best_store'] = False
            provider_data['url'] = ' ' if not provider_data.get('merchantUrl') else "https://adayroi.com%s" % provider_data.get('merchantUrl')
            provider_data['logo'] = provider_data.get('merchantLogo', ' ')
        return provider_data

    def _adayroi_get_related_product(self, product_data, related_products):
        if not related_products:
            return {}
        for product in related_products:
            product['product_id'] = product.get('merchantCode', ' ')
            product['base_product_id'] = product_data.get('baseProduct', ' ')
            product['platform'] = 'adayroi'
            product['url_path'] = product.get('url', ' ')
        return related_products

    def _adayroi_get_images(self, image_data):
        images = []
        if image_data:
            for img in image_data:
                if img.get('url'):
                    url = img.get('url').replace('80_80', '550_550')
                    images.extend({
                        'alter_text': img.get('altText'),
                        'url': url
                    })
        return images

    def _adayroi_get_specification(self, specification):
        attributes_list = []
        if specification:
            try:
                specification = specification[0]
                features = specification.get('features')
                for f in features:
                    feature_values = f.get('featureValues', {})
                    value = " ,".join(fv.get('value') for fv in feature_values)
                    if f.get('featureUnit'):
                        value = "%s %s" % (value, f.get('featureUnit', {}).get('name'))
                    attributes_list.extend({
                        'name': f.get('name'),
                        'value': value
                    })
            except ValueError:
                logging.error("Error when getting Adayroi Specification")
                logging.error(ValueError)
        return attributes_list

    def _adayroi_get_category(self, category_data):
        category = {}
        if category_data:
            category['id'] = category_data.get('id'),
            category['name'] = category_data.get('path')
        return category

    def adayroi_standardize_data(self, product_data):
        url = 'https://adayroi.com%s' % product_data.get('url')

        brand = {
            'name': product_data.get('brandName'),
            'slug': product_data.get('brandName').lower()
        }

        categories = self._adayroi_get_category(product_data.get('categoryImpression'))

        thumbnail_url = False
        if product_data.get('images'):
            thumbnail = product_data.get('images')[0]
            thumbnail_url = thumbnail.get('url')
            if '80_80' in thumbnail_url:
                thumbnail_url = thumbnail_url.replace('80_80', '550_550')

        attributes_list = self._adayroi_get_specification(product_data.get('classifications'))

        cur_offer = product_data.get('currentOffer', {})

        sale_price = product_data.get('price', {}).get('value', 0.0)
        list_price = product_data.get('productPrice', {}).get('value', 0.0)
        product_data.update({
            'product_id': product_data.get('baseProduct'),
            'spid': cur_offer.get('code', '1'),
            'url': url,
            'sku': product_data.get('productSKU') or product_data.get('sapSku') or ' ',
            'sale_price': sale_price,
            'list_price': list_price,
            'discount': int(list_price) - int(sale_price),
            'discount_rate': round((1 - int(sale_price)/int(list_price)) * 100, 0),
            'quantity': product_data.get('stock', {}).get('stockLevel', 0),
            'inventory_status': 'available' if product_data.get('purchasable') is True else False,
            'description': product_data.get('longDescription'),
            'thumbnail_url': thumbnail_url,

            'specification': attributes_list,
            'brand': brand,
            'category': categories,
            'provider': self._adayroi_get_provider(product_data.get('merchant')),
            'images': self._adayroi_get_images(product_data.get('images')),
            'related_products': self._adayroi_get_related_product(product_data=product_data,
                                                          related_products=product_data.get('offers'))
        })

        return product_data
