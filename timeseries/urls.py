from django.urls import path

from . import views
from . import apis

app_name = 'timeseries'

urlpatterns = [
    path('test', views.test, name='test'),

    path('sync-price-view', views.sync_price_view, name='Sync Price View'),
    path('sync_price', views.import_price_data, name='sync_price'),

    # api
    path('api/v1/get_special_price_current_product', apis.get_special_price_current_product,
         name='get special price current product')
]
