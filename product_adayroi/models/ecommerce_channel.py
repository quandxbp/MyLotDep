from django.db import models

import requests


class Adayroi(models.Model):
    class Meta:
        abstract = True

    def adayroi_get_data(self):
        products = []
        page, total_page, limit = 0, 1, 100
        pagi_flag = True

        while page < total_page:
            endpoint = "https://rest.adayroi.com/cxapi/v2/adayroi/search?fields=FULL&q&categoryCode=322&pageSize=%s&currentPage=%s" % (
                limit, page)
            print("Processing: %s" % endpoint)
            try:
                data = []
                response = requests.get(endpoint)
                if response.ok:
                    json_data = response.json()
                    data = json_data.get('products')
                    if pagi_flag:
                        total_page = json_data.get('pagination').get('totalPages')
                        pagi_flag = False

                products.extend(data)

            except Exception as err:
                print("Error when getting Adayroi products ")
                print(err)
            page += 1

        # Get detail data of a product
        filter_products = [p for p in products if p.get('baseProductCode').isdigit()]
        for product in filter_products:
            product_id = product.get('baseProductCode')
            endpoint = "https://rest.adayroi.com/cxapi/v2/adayroi/product/detail?fields=FULL&productCode=%s" % product_id
            print("Processing url %s " % endpoint)
            try:
                data = []
                response = requests.get(endpoint)
                if response.ok:
                    data = response.json()
                product.update(data)
            except Exception as err:
                print("Error when getting Adayroi product %s detail " % product_id)
                print(err)

        return filter_products
