from django.urls import path

from . import views
from . import apis
from . import crons
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
    path('cron', crons.cron, name='cron'),
    path('cron_mongo', crons.cron_mongo, name='cron mongo'),
    path('tiki_scheduler', crons.tiki_scheduler, name='tiki_scheduler'),
    path('adayroi_scheduler', crons.adayroi_scheduler, name='adayroi_scheduler'),
    path('tiki_scheduler_reverse', crons.tiki_scheduler_reverse, name='tiki_scheduler_reverse'),
    path('adayroi_scheduler_reverse', crons.adayroi_scheduler_reverse, name='adayroi_scheduler_reverse'),

    # Create Channels and Synchronize products on channels
    path('sync-product-view', views.sync_product_view, name='sync product view'),
    path('sync-product', views.sync_product, name='sync product'),
    path('update-product-view', views.update_product_view, name='update product view'),
    path('update-product', views.update_product, name='update product'),

    # Api
    path('api/v1/search_product', apis.search_product, name='search product'),
    path('api/v1/get_product_comments', apis.get_product_comments, name='get product comments'),
    path('api/v1/get_product_articles', apis.get_product_articles, name='get product articles'),
    path('api/v1/get_current_product_price', apis.get_current_product_price, name='current product price')
]
