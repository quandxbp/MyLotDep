from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound, JsonResponse

from .models.time_price import TimePrice
from .models.price_source import PriceSource
from common.utils import write_to_csv

from .forms import SyncPriceForm


def test(request):
    TP = TimePrice()
    price_list = TP.get_price_list_by_id(product_id="12206668")
    print(price_list)
    write_to_csv(price_list)

    return HttpResponse("Done")


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
