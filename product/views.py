from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound, JsonResponse

from .models.ecommerce_channel import EcommerceChannel
from .models.accesstrade import AccessTrade
from django.views.decorators.csrf import csrf_exempt

from .models.product import Product
from .models.ecommerce_channel import EcommerceChannel
from .models.image import Image

from .forms import SyncChannelForm
import json


def index(request):
    return HttpResponse("<h1> Index Page </h1>")


def sync_product_view(request):
    if request.method == 'POST':
        form = SyncChannelForm(request.POST)
        if form.is_valid():
            print('aihhi')
    else:
        form = SyncChannelForm()

    return render(request, 'product/sync_product_channel_view.html', {'form': form})


@csrf_exempt
def create_new_channel(request):
    payload = json.loads(request.body)
    if payload:
        channel_name = payload.get('name', False)
        channel_platform = payload.get('platform', False)
        if False not in [channel_name, channel_platform]:
            access_trade = AccessTrade()
            access_trade.save()
            new_channel = EcommerceChannel(name=channel_name,
                                           platform=channel_platform,
                                           access_trade_id=access_trade)
            new_channel.save()
        else:
            return HttpResponseNotFound("Error: Request parameters")
        return JsonResponse(
            {'channel_id': new_channel.id}
        )
    else:
        return HttpResponseNotFound("Error: Request method")


def sync_product(request):
    if request.method == 'POST':
        data = request.POST
        if data:
            channel_id = data.get('channel', False)
            channel = EcommerceChannel.objects.get(pk=channel_id)
            channel.sync_channel_product()
            return HttpResponse("Is syncing")
    else:
        return HttpResponseNotFound("Error: Request methods")
