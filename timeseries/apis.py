from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models.time_price import TimePrice

import logging
import json


@csrf_exempt
def get_special_price_current_product(request):
    special_price_info = {}
    if request.method == 'GET':
        data = request.GET
        if data:
            spid = data.get('spid')
            TP = TimePrice()
            special_price_info = TP.get_special_price_statistics(spid)

    return JsonResponse(special_price_info)
