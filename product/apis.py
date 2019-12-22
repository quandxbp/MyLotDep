from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound, JsonResponse

from .models.product import Product

import logging
import json


def search_product(request):
    products = []
    if request.method == 'GET':
        data = request.GET
        if data:
            search_data = data.get('search_data')
            if isinstance(search_data, list):
                search_data = search_data[0]
            search_data = "%" + str(search_data) + "%"
            try:
                sql = "SELECT pp.id, min(pp.product_id), pp.name, pp.thumbnail_url, pp.sale_price, pp.list_price, pp.discount_rate, pp.channel_id_id " \
                      "FROM product_product pp JOIN product_producttemplate pt ON pp.product_tmpl_id_id = pt.id " \
                      "WHERE pt.name LIKE %s GROUP BY pp.name LIMIT 5"
                query_set = Product.objects.raw(sql, [search_data])
                if query_set:
                    for p in query_set:
                        products.append({
                            'product_name': p.name,
                            'thumb_url': p.thumbnail_url,
                            'sale_price': float(p.sale_price),
                            'list_price': float(p.list_price),
                            'discount_rate': p.discount_rate,
                            'platform': p.channel_id.platform
                        })
            except Exception as err:
                logging.error("Error when querying product")
                logging.error(err)

    result = {
        'products': products
    }
    return JsonResponse(result)
