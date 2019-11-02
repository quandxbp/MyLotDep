from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound, JsonResponse

from django.views.decorators.csrf import csrf_exempt
from common.constants import DISPLAY_CATEGORY

from .models.product import Product
from .models.category import Category
from .models.ecommerce_channel import EcommerceChannel
from .models.accesstrade import AccessTrade

from .forms import SyncChannelForm
import json


def home(request):
    categ_ids = Category.objects.filter(id_on_channel__in=DISPLAY_CATEGORY['tiki'])
    top_products = Product.objects.filter(sequence=1, category_id__in=categ_ids)
    context = {"top_products": top_products}
    return render(request, "home.html", context=context)


def products(request):
    categ_ids = Category.objects.filter(id_on_channel__in=DISPLAY_CATEGORY['tiki'])
    products = Product.objects.filter(category_id__in=categ_ids).order_by('-id')[:50]
    context = {'products': products}
    return render(request, 'product/products.html', context=context)


def single_product(request):
    return render(request, "product/product-single.html")


def contact(request):
    return render(request, "contact.html")


def about(request):
    return render(request, "about.html")


def page_not_found(request):
    return render(request, "page-not-found.html")


def sync_product_view(request):
    if request.method == 'POST':
        form = SyncChannelForm(request.POST)
        if form.is_valid():
            print('Form is valid')
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
            is_top_product = data.get('is_top_product', False)
            channel = EcommerceChannel.objects.get(pk=channel_id)
            channel.sync_channel_product(is_top_product)
            return HttpResponse("Is syncing")
    else:
        return HttpResponseNotFound("Error: Request methods")
