from django.urls import path

from . import views
app_name = 'product'
urlpatterns = [
    # Homepage
    path('', views.home, name='home'),
    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact'),
    path('404-not-found', views.page_not_found, name='page-not-found'),

    # Display products
    path('san-pham', views.products, name='products'),
    path('p', views.single_product),

    # Cron job
    path('cron', views.cron, name='cron'),
    path('cron_mongo', views.cron_mongo, name='cron mongo'),
    path('tiki_scheduler', views.tiki_scheduler, name='tiki_scheduler'),
    path('adayroi_scheduler', views.adayroi_scheduler, name='adayroi_scheduler'),
    path('tiki_scheduler_reverse', views.tiki_scheduler_reverse, name='tiki_scheduler_reverse'),
    path('adayroi_scheduler_reverse', views.adayroi_scheduler_reverse, name='adayroi_scheduler_reverse'),

    # Create Channels and Synchronize products on channels
    path('sync-product-view', views.sync_product_view, name='sync product view'),
    path('sync-product', views.sync_product, name='sync product'),
    path('update-product-view', views.update_product_view, name='update product view'),
    path('update-product', views.update_product, name='update product')
]
