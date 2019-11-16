from django.db import models

import logging

_logger = logging.getLogger(__name__)


class TikiProduct(models.Model):
    class Meta:
        abstract = True

    def _get_specification(self, specification):
        spec_dict = {}
        attributes_list = []
        for spec in specification:
            attributes_list.extend(spec.get('attributes', []))

        for attr in attributes_list:
            if attr.get('name') == "Camera trước":
                spec_dict['front_camera'] = attr.get('value')
            elif attr.get('name') == "Camera sau":
                spec_dict['rear_camera'] = attr.get('value')
            elif attr.get('name') == "Quay phim":
                spec_dict['recording'] = attr.get('value')
            elif attr.get('name') == "Loại / Công nghệ màn hình":
                spec_dict['screen_technology'] = attr.get('value')
            elif attr.get('name') == "Bộ nhớ RAM":
                spec_dict['ram_memory'] = attr.get('value')
            elif attr.get('name') == "Bộ nhớ trong (ROM)":
                spec_dict['rom_memory'] = attr.get('value')
            elif attr.get('name') == "Trọng lượng":
                spec_dict['weight'] = attr.get('value')
            elif attr.get('name') == "Kích thước":
                spec_dict['dimension'] = attr.get('value')
            elif attr.get('name') == "Tên chip":
                spec_dict['chip'] = attr.get('value')
            elif attr.get('name') == "Chip đồ họa (GPU)":
                spec_dict['gpu'] = attr.get('value')
            elif attr.get('name') == "Dung lượng pin (mAh)":
                spec_dict['pin_capacity'] = attr.get('value')

        return spec_dict, attributes_list

    def _get_provider(self, provider_data):
        if not provider_data:
            return []
        provider_data['is_best_store'] = False if provider_data.get('is_best_store', False) in ['false',
                                                                                                False] else True
        provider_data['url'] = ' ' if not provider_data.get('link') else provider_data.get('link').replace('api.', '')
        return provider_data

    def _get_related_product(self, product_data, related_products):
        for product in related_products:
            product['name'] = product_data.get('name')
            product['url_key'] = "%s.html?spid=%s" % (product_data.get('url_key'), product.get('product_id'))
            product['main_product_id'] = product_data.get('id')
            product['platform'] = 'tiki'
            product['product_id'] = product.get('product_id')
        return related_products

    def tiki_standardize_data(self, product_data):
        url = 'https://tiki.vn/%s' % product_data.get('url_path')
        cur_seller = product_data.get('current_seller', {})
        if not cur_seller:
            cur_seller = {}

        spec_dict, attributes_list = self._get_specification(product_data.get('specifications'))

        product_data.update({
            'product_id': product_data.get('id'),
            'sale_price': product_data.get('price', 0),
            'seller_product_id': cur_seller.get('product_id', ' '),
            'seller_sku': cur_seller.get('sku', ' '),
            'url': url,
            'thumbnail_url': product_data.get('thumbnail_url', ' '),
            # Specifications
            'screen_technology': spec_dict.get('screen_technology', ' '),
            'ram_memory': spec_dict.get('ram_memory', ' '),
            'rom_memory': spec_dict.get('rom_memory', ' '),
            'front_camera': spec_dict.get('front_camera', ' '),
            'rear_camera': spec_dict.get('rear_camera', ' '),
            'recording': spec_dict.get('recording', ' '),
            'weight': spec_dict.get('weight', ' '),
            'dimension': spec_dict.get('dimension', ' '),
            'chip': spec_dict.get('chip', ' '),
            'gpu': spec_dict.get('gpu', ' '),
            'pin_capacity': spec_dict.get('pin_capacity', ' '),

            'specification': attributes_list,

            'brand': product_data.get('brand'),
            'category': product_data.get('categories'),
            'provider': self._get_provider(product_data.get('current_seller')),
            'related_products': self._get_related_product(product_data=product_data,
                                                          related_products=product_data.get('other_sellers'))
        })

        return product_data
