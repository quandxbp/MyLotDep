from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound, JsonResponse

from django.views.decorators.csrf import csrf_exempt
from common.constants import DISPLAY_CATEGORY

from .models.product import Product
from .models.category import Category
from .models.ecommerce_channel import EcommerceChannel
from .models.specification import Specification
from .models.accesstrade import AccessTrade
from timeseries.models.time_price import TimePrice
from .models.cron import run_job

from .forms import SyncChannelForm

def test():
    print('ahihi')

def cron(request):
    EC = EcommerceChannel()
    run_job(period='second', func=EC.update_data_channel, amount=1)

    return HttpResponse("Run job")


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
    product_id = "32033730"
    product = Product.objects.filter(product_id=product_id)[0]
    specifications = Specification.objects.filter(product_id=product.id)
    # time_price = TimePrice()
    # labels, prices = time_price.get_price_by_id(product_id)

    context = {
        'product': product,
        'specifications': specifications,
        # 'labels': labels,
        # 'prices': prices
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
