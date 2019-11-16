from django.urls import path

from . import views
app_name = 'timeseries'

urlpatterns = [
    path('test', views.test, name='test'),

    path('sync-price-view', views.sync_price_view, name='Sync Price View'),
    path('sync_price', views.import_price_data, name='sync_price')
]