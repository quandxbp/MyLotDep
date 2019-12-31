from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound, JsonResponse

from common.constants import DISPLAY_CATEGORY

from .models.product import Product
from .models.category import Category
from .models.ecommerce_channel import EcommerceChannel
from .models.specification import Specification
from .models.provider import Provider
from .models.related_product import RelatedProduct
from .models.accesstrade import AccessTrade
from timeseries.models.time_price import TimePrice
from .models.cron import run_scheduler

from .forms import SyncChannelForm
import logging


def adayroi_scheduler(request):
    try:
        adayroi = EcommerceChannel.objects.get(platform='adayroi')
        adayroi.update_data_channel_mongo()
        run_scheduler(period='hour', func=adayroi.update_data_channel, amount=3)
    except Exception as err:
        logging.error("Error when running scheduler")
        logging.error(err)
    return HttpResponse("Job is DONE")


def tiki_scheduler(request):
    try:
        tiki = EcommerceChannel.objects.get(platform='tiki')
        run_scheduler(period='hour', func=tiki.update_data_channel, amount=3)
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


def single_product(request, product_id):
    product = Product.objects.get(pk=product_id)
    specifications = Specification.objects.filter(product_id=product.id)

    # Get all related product data
    related_products = RelatedProduct.objects.filter(related_product_id=product.id)
    related_product_data = []
    if related_products:
        url_paths = [p.url_path for p in related_products]
        related_product_data = Product.objects.filter(url_path__in=url_paths)
        for rlp in related_product_data:
            diff_val = product.sale_price - rlp.sale_price
            if diff_val >= 0:
                rlp.is_gt = True
                rlp.diff_val = diff_val
            else:
                rlp.is_gt = False
                rlp.diff_val = -diff_val

    time_price = TimePrice()
    labels, prices = time_price.get_price_by_spid(product.spid)

    context = {
        'product': product,
        'specifications': specifications,
        'related_product_data': related_product_data,
        'labels': labels,
        'prices': prices
    }
    return render(request, "product/product-single.html", context=context)


def demo_product(request):
    product = Product.objects.get(spid=13481649)
    specifications = Specification.objects.filter(product_id=product.id)

    # Get all related product data
    related_products = RelatedProduct.objects.filter(related_product_id=product.id)
    related_product_data = []
    if related_products:
        url_paths = [p.url_path for p in related_products]
        related_product_data = Product.objects.filter(url_path__in=url_paths)
        for rlp in related_product_data:
            diff_val = product.sale_price - rlp.sale_price
            if diff_val >= 0:
                rlp.is_gt = True
                rlp.diff_val = diff_val
            else:
                rlp.is_gt = False
                rlp.diff_val = -diff_val

    time_price = TimePrice()
    labels, prices = time_price.get_price_by_spid(product.spid)

    context = {
        'product': product,
        'specifications': specifications,
        'related_product_data': related_product_data,
        'labels': labels,
        'prices': prices
    }
    return render(request, "product/product-single.html", context=context)


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

    return render(request, 'product/sync-product-view.html', {'form': form})


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


def update_product_view(request):
    if request.method == 'POST':
        form = SyncChannelForm(request.POST)
        if form.is_valid():
            print('Form is valid')
    else:
        form = SyncChannelForm()

    return render(request, 'product/update-product-view.html', {'form': form})


def update_product(request):
    if request.method == 'POST':
        data = request.POST
        if data:
            channel_id = data.get('channel', False)
            channel = EcommerceChannel.objects.get(pk=channel_id)
            channel.update_data_channel()
            return HttpResponse("Is syncing")
    else:
        return HttpResponseNotFound("Error: Request methods")
