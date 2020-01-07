from django.db import models
from common.utils import get_soup

from product_tiki.models.product import *

from .accesstrade import AccessTrade

from product_tiki.models.ecommerce_channel import Tiki
from product_adayroi.models.ecommerce_channel import Adayroi

import time
import logging
import requests
import json


class EcommerceChannel(Tiki, Adayroi):
    name = models.CharField(max_length=255)
    platform = models.CharField(max_length=50,
                                choices=[('tiki', 'Tiki'),
                                         ('lazada', 'Lazada'),
                                         ('adayroi', 'Adayroi')],
                                default='tiki')
    access_trade_id = models.ForeignKey(AccessTrade,
                                        default=1,
                                        verbose_name="Access Trade",
                                        on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def sync_channel_product(self, top_product=False):
        logging.info("Start syncing Product Data in %s" % self.platform)
        cust_method_name = '%s_get_data' % self.platform if not top_product else '%s_get_top_data' % self.platform
        if hasattr(self, cust_method_name):
            from .product import Product

            products_data = getattr(self, cust_method_name)()
            # Update channel id in each product
            sequence = 1 if top_product else 0
            for product in products_data:
                if isinstance(product, list):
                    products_data.remove(product)
                    continue
                product.update({'channel_id': self,
                                'platform': self.platform,
                                'sequence': sequence})
            # Synchronize products data

            Product = Product()
            Product.sync_product_channel(1, products_data)

    def update_data_channel(self):
        logging.info("Updating product data in %s" % self.platform)
        cust_method_name = '%s_update_data' % self.platform
        if hasattr(self, cust_method_name):
            from .product import Product
            PO = Product()

            products_data = getattr(self, cust_method_name)()
            PO.update_data_product_channel(products_data, update_mongo=True)

    def update_data_channel_mongo(self, reverse=False):
        logging.info("Updating product data from Mongo in %s" % self.platform)
        cust_method_name = '%s_update_data_mongo' % self.platform
        if hasattr(self, cust_method_name):
            from .product import Product
            PO = Product()

            products_data = getattr(self, cust_method_name)()
            if reverse:
                products_data.reverse()
            PO.update_data_product_channel_mongo(products_data, update_sql=False)

    def get_product_comment_channel(self, platform, product_id):
        cust_method_name = '%s_get_comments' % platform
        if hasattr(self, cust_method_name):
            method = getattr(self, cust_method_name)(product_id)
            return method
        return []

    def get_product_comment_review_source(self, product_tmpl_name):
        # Hard code
        data = []
        vnreview_endpoint = 'https://vnreview.vn/VnReview/getComment.action'
        headers = {
            'Content-Type': 'application/json',
            'Referer': 'https://vnreview.vn/danh-gia-chi-tiet-di-dong/-/view_content/content/2823988/danh-gia-samsung-galaxy-a70-danh-cho-nhung-cu-dan-mang-thuc-thu'
        }
        params = {
            'articleId': "2823988",
            "skip": 0,
            "limit": 15,
            "sort": 1
        }

        try:
            vnreview_res = requests.post(url=vnreview_endpoint, data=json.dumps(params), headers=headers)
            if vnreview_res.ok:
                res = vnreview_res.json().get('returnValue')
                comments = json.loads(res)
                for comment in comments:
                    data.append({
                        'author': comment.get('userComment'),
                        'avatar': '/static/images/undefined-user.jpg',
                        'title': 'Không tiêu đề',
                        'content': comment.get('body'),
                        'created_at': comment.get('createDate'),
                    })
        except Exception as err:
            logging.error("Error when getting comments from VnReview")
            logging.error(err)
        return data

    def get_genk_article(self):
        url = "https://genk.vn/samsung-galaxy-a70-chiec-smartphone-toan-dien-nhat-trong-phan-khuc-trung-cap-20190523164118506.chn"
        try:
            soup = get_soup(url)
        except Exception as e:
            raise e

        articlesTag = soup.find("div", {"class": "w640"})

        content = str(articlesTag)
        return content

    def generate_accesstrade_headers(self):
        return {
            'Authorization': "Token %s" % self.access_trade_id.accesstrade_access_key
        }
