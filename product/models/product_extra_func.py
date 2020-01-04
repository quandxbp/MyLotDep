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
                'cur_datetime': str(f"{datetime.datetime.now():%d-%m-%Y %H:%M:%S}")
            }
        return {}

    def get_count(self, search_data, channel_ids=None):
        from .product import Product

        res = []
        search_data = "%" + str(search_data) + "%"
        if not channel_ids:
            channel_ids = EcommerceChannel.objects.all()

        for channel in channel_ids:
            product_count = 0
            sql_count = "SELECT pp.id " \
                        "FROM product_product pp JOIN product_producttemplate pt ON pp.product_tmpl_id_id = pt.id " \
                        "WHERE pp.active = 1 AND pt.name LIKE %s " \
                        "AND pp.channel_id_id = (SELECT pe.id FROM product_ecommercechannel pe WHERE pe.platform = %s)"

            query_count = Product.objects.raw(sql_count, [search_data, channel.platform])
            if query_count:
                product_count = sum(1 for q in query_count)
            res.append((
                channel.platform.upper(), product_count
            ))
        return res

    def get_product_template(self, search_data, limit=5):
        from .product import Product
        search_data = "%" + str(search_data) + "%"

        sql = "SELECT pt.id, pt.name " \
              "FROM product_producttemplate pt " \
              "WHERE pt.name LIKE %s GROUP BY pt.id LIMIT %s "

        product_templates = Product.objects.raw(sql, [search_data, limit])

        return [p.name for p in product_templates]

    def get_product(self, search_data, channel_ids=None, limit=5):
        from .product import Product
        res = []
        search_data = "%" + str(search_data) + "%"
        if not channel_ids:
            channel_ids = EcommerceChannel.objects.all()

        for channel in channel_ids:
            sql = "SELECT pp.id, pp.product_id, pp.name, pp.thumbnail_url, pp.sale_price, pp.list_price, pp.discount_rate, pp.channel_id_id " \
                  "FROM product_product pp JOIN product_producttemplate pt ON pp.product_tmpl_id_id = pt.id " \
                  "WHERE pp.active = 1 AND pt.name LIKE %s " \
                  "AND pp.channel_id_id = (SELECT pe.id FROM product_ecommercechannel pe WHERE pe.platform = %s)" \
                  "GROUP BY pp.name " \
                  "ORDER BY pp.sale_price ASC LIMIT %s"
            products = Product.objects.raw(sql, [search_data, channel.platform, limit])
            if products:
                for p in products:
                    res.append({
                        'product_name': p.name,
                        'thumb_url': p.thumbnail_url,
                        'sale_price': float(p.sale_price),
                        'list_price': float(p.list_price),
                        'discount_rate': p.discount_rate,
                        'platform': p.channel_id.platform
                    })
        return res
