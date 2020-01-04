from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models.product import Product
from .models.ecommerce_channel import EcommerceChannel

import logging
import json

@csrf_exempt
def search_product(request):
    res = {}
    if request.method == 'GET':
        data = request.GET
        if data:
            search_data = data.get('q')
            if isinstance(search_data, list):
                search_data = search_data[0]
            ProductObj = Product()
            product_templates = ProductObj.get_product_template(search_data)
            products = ProductObj.get_product(search_data)
            platforms = ProductObj.get_count(search_data)

            res.update({
                'product_templates': product_templates,
                'products': products,
                'platforms': platforms
            })
    return JsonResponse(res)


# @csrf_exempt
# def search_product_by_template(request):
#     product_data = []
#     if request.method == 'GET':
#         data = request.GET
#         if data:
#             search_data = data.get('search_data')
#             if isinstance(search_data, list):
#                 search_data = search_data[0]
#             search_data = "%" + str(search_data) + "%"
#             try:
#                 ec_ids = EcommerceChannel.objects.all()
#                 for ec in ec_ids:
#                     products = []
#                     product_count = 0
#                     limit = 5
#
#                     sql = "SELECT pp.id, min(pp.product_id), pp.name, pp.thumbnail_url, pp.sale_price, pp.list_price, pp.discount_rate, pp.channel_id_id " \
#                           "FROM product_product pp JOIN product_producttemplate pt ON pp.product_tmpl_id_id = pt.id " \
#                           "WHERE pp.active = 1 AND pt.name LIKE %s " \
#                           "AND pp.channel_id_id = (SELECT pe.id FROM product_ecommercechannel pe WHERE pe.platform = %s)" \
#                           "GROUP BY pp.name LIMIT 5"
#                     query_set = Product.objects.raw(sql, [search_data, ec.platform])
#
#                     sql_count = "SELECT pp.id " \
#                                 "FROM product_product pp JOIN product_producttemplate pt ON pp.product_tmpl_id_id = pt.id " \
#                                 "WHERE pp.active = 1 AND pt.name LIKE %s " \
#                                 "AND pp.channel_id_id = (SELECT pe.id FROM product_ecommercechannel pe WHERE pe.platform = %s)"
#
#                     query_count = Product.objects.raw(sql_count, [search_data, ec.platform])
#                     if query_set:
#                         for p in query_set:
#                             products.append({
#                                 'product_name': p.name,
#                                 'thumb_url': p.thumbnail_url,
#                                 'sale_price': float(p.sale_price),
#                                 'list_price': float(p.list_price),
#                                 'discount_rate': p.discount_rate,
#                                 'platform': p.channel_id.platform
#                             })
#                     if query_count:
#                         product_count = sum(1 for q in query_count) - limit
#                     product_data.append((products, product_count))
#
#             except Exception as err:
#                 logging.error("Error when querying product")
#                 logging.error(err)
#
#     result = {
#         'product_data': product_data
#     }
#     return JsonResponse(result)


@csrf_exempt
def get_current_product_price(request):
    current_price_info = {}
    lowest_price_info = {}
    if request.method == 'GET':
        data = request.GET
        if data:
            spid = data.get('spid')
            lowest_price_spid = data.get('lowest_price_spid')
            product_id = data.get('product_id')
            platform = data.get('platform')

            ProductObj = Product()
            current_price_info = ProductObj.get_product_data_by_spid(product_id, spid, platform)
            lowest_price_info = ProductObj.get_product_data_by_spid(product_id, lowest_price_spid, platform)

    return JsonResponse({'current_price_info': current_price_info,
                        'lowest_price_info': lowest_price_info})
