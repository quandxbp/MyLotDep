from django.urls import path

from . import views
app_name = 'product'
urlpatterns = [
    path('', views.index, name='index'),

    # Get track price


    # Create Channels and Synchronize products on channels
    path('create_channel', views.create_new_channel, name='create_channel'),
    path('sync_product_view', views.sync_product_view, name='sync_product_view'),
    path('sync_product', views.sync_product, name='sync_product')
]
