from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound, JsonResponse

from .models.ecommerce_channel import EcommerceChannel
from .models.cron import run_scheduler

import logging


def adayroi_scheduler_reverse(request):
    try:
        adayroi = EcommerceChannel.objects.get(platform='adayroi')
        adayroi.update_data_channel_mongo(reverse=True)
        params = {'reverse': True}
        run_scheduler(period='hour', func=adayroi.update_data_channel_mongo, params=params, amount=3)
    except Exception as err:
        logging.error("Error when running scheduler")
        logging.error(err)
    return HttpResponse("Job is DONE")


def tiki_scheduler_reverse(request):
    try:
        tiki = EcommerceChannel.objects.get(platform='tiki')
        tiki.update_data_channel_mongo(reverse=True)
        params = {'reverse': True}
        run_scheduler(period='hour', func=tiki.update_data_channel_mongo, params=params, amount=3)
    except Exception as err:
        logging.error("Error when running scheduler")
        logging.error(err)
    return HttpResponse("Job is DONE")


def adayroi_scheduler(request):
    try:
        adayroi = EcommerceChannel.objects.get(platform='adayroi')
        adayroi.update_data_channel_mongo()
        run_scheduler(period='hour', func=adayroi.update_data_channel_mongo, amount=3)
    except Exception as err:
        logging.error("Error when running scheduler")
        logging.error(err)
    return HttpResponse("Job is DONE")


def tiki_scheduler(request):
    try:
        tiki = EcommerceChannel.objects.get(platform='tiki')
        tiki.update_data_channel_mongo()
        run_scheduler(period='hour', func=tiki.update_data_channel_mongo, amount=3)
    except Exception as err:
        logging.error("Error when running scheduler")
        logging.error(err)
    return HttpResponse("Job is DONE")


def cron(request):
    all_ecommerce_channels = EcommerceChannel.objects.all()
    for ec in all_ecommerce_channels:
        try:
            run_scheduler(period='hour', func=ec.update_data_channel, amount=3)
        except Exception as err:
            logging.error("Error when running scheduler")
            logging.error(err)

    return HttpResponse("Job is DONE")


def cron_mongo(request):
    all_ecommerce_channels = EcommerceChannel.objects.all()
    for ec in all_ecommerce_channels:
        try:
            run_scheduler(period='hour', func=ec.update_data_channel_mongo, amount=3)
        except Exception as err:
            logging.error("Error when running scheduler")
            logging.error(err)

    return HttpResponse("Job is DONE")
