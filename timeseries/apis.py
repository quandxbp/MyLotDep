from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models.time_price import TimePrice

import logging
import json


@csrf_exempt
def get_special_price_current_product(request):
    cur_special_price_info = {}
    lowest_special_price_info = {}
    if request.method == 'GET':
        data = request.GET
        if data:
            spid = data.get('spid')
            lowest_price_spid = data.get('lowest_price_spid')

            TP = TimePrice()
            cur_special_price_info = TP.get_special_price_statistics(spid)
            lowest_special_price_info = TP.get_special_price_statistics(lowest_price_spid)

    return JsonResponse({'cur_special_price_info': cur_special_price_info,
                         'lowest_special_price_info': lowest_special_price_info})
