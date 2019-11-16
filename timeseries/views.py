from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound, JsonResponse

from .models.time_price import TimePrice
from .models.price_source import PriceSource

from .forms import SyncPriceForm


def test(request):
    TP = TimePrice()
    # time_price.initialize_data_time_price(time_price.get_data_jajum)
    TP.get_data_beetracker('tiki',
                           "https://tiki.vn/tai-nghe-bluetooth-apple-airpods-2-true-wireless-mv7n2-hop-sac-thuong-hang-nhap-khau-p12706787.html?src=recently-viewed&spid=23239506")
    return HttpResponse("AHIHI")


def sync_price_view(request):
    if request.method == 'POST':
        form = SyncPriceForm(request.POST)
        if form.is_valid():
            print('Form is valid')

    else:
        form = SyncPriceForm()

    return render(request, 'timeseries/sync_price_view.html', {'form': form})


def import_price_data(request):
    if request.method == 'POST':
        data = request.POST
        if data:
            time_price = TimePrice()
            price_source = PriceSource()
            source = data.get('source')

            if not source:
                return HttpResponseNotFound("Error: Price Source")

            time_price.initialize_data_time_price(price_source.get_source(source))
            return HttpResponse("<h1>Done</h1>")
    else:
        return HttpResponseNotFound("Error: Request methods")
