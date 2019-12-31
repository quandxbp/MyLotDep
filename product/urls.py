from django.urls import path

from . import views
from . import apis
app_name = 'product'
urlpatterns = [
    # Homepage
    path('', views.home, name='home'),
    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact'),
    path('404-not-found', views.page_not_found, name='page-not-found'),

    # Display products
    path('san-pham', views.products, name='products'),
    path('<int:product_id>', views.single_product, name='single product'),
    path('demo-product', views.demo_product, name='demo product'),

    # Cron job
    path('cron', views.cron, name='cron'),
    path('cron_mongo', views.cron_mongo, name='cron mongo'),
    path('tiki_scheduler', views.tiki_scheduler, name='tiki_scheduler'),
    path('adayroi_scheduler', views.adayroi_scheduler, name='adayroi_scheduler'),

    # Create Channels and Synchronize products on channels
    path('sync-product-view', views.sync_product_view, name='sync product view'),
    path('sync-product', views.sync_product, name='sync product'),
    path('update-product-view', views.update_product_view, name='update product view'),
    path('update-product', views.update_product, name='update product'),

    # Api
    path('api/v1/search_product', apis.search_product, name='search product'),
    path('api/v1/current_product_statistics', apis.current_product_statistics, name='current product statistics')
]
