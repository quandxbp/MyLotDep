from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound, JsonResponse

from .models.time_price import TimePrice

def test(request):
    time_price = TimePrice()
    time_price.initialize_data_time_price()
    return HttpResponse("AHIHI")
