from django.db import models
import datetime

from .ecommerce_channel import EcommerceChannel

class ProductExtraFunc(models.Model):
    class Meta:
        abstract = True

    def get_product_data_by_spid(self, product_id, spid, platform):
        EC = EcommerceChannel()
        cust_method_name = '%s_get_detail_data' % platform
        if hasattr(EC, cust_method_name):

            product = getattr(EC, cust_method_name)(product_id, spid)

            return {
                'sale_price': product.get('price', 0),
                'cur_datetime': str(f"{datetime.datetime.now():%d-%m-%Y %H:%M}")
            }
        return {}
