from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound, JsonResponse

from .app.ner import NERTAG

ner_model = NERTAG()


# Create your views here.
def test(request):
    name = "Điện Thoại Samsung Galaxy M30s (64GB/4GB) - Hàng Chính Hãng"
    results = ner_model.predict_product(name)
    return HttpResponse("<p>%s</p><p>%s</p>" % (name, results))
