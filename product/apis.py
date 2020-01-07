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


@csrf_exempt
def get_product_comments(request):
    res = {}
    if request.method == 'GET':
        data = request.GET
        if data:
            platform = data.get('platform')
            product_id = data.get('product_id')
            product_tmpl_name = data.get('product_tmpl_name')
            EC = EcommerceChannel()
            channel_comments = EC.get_product_comment_channel(platform, product_id)
            review_sources = EC.get_product_comment_review_source(product_tmpl_name)

            res.update({
                'channel_comments': channel_comments,
                'review_sources': review_sources
            })

    return JsonResponse(res)


@csrf_exempt
def get_product_articles(request):
    res = {}
    if request.method == 'GET':
        EC = EcommerceChannel()
        # channel_comments = EC.get_product_comment_channel(platform, product_id)
        genk_article_source = EC.get_genk_article()

        res.update({
            'genk_article_source': genk_article_source,
        })

    return JsonResponse(res)


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
