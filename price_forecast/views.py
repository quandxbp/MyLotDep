from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import PriceForecast

import json

@csrf_exempt
def price_forecast(request):
    labels, prices = [], []

    if request.method == 'POST':
        PF = PriceForecast()
        data = request.POST
        if data:
            spid = data.get('spid')
            if isinstance(spid, list):
                spid = spid[0]
            labels, prices = PF.prophet_forecast(spid=spid)
    data = {
        'labels': labels,
        'prices': prices
    }
    return HttpResponse(json.dumps(data))
