from django.urls import path

from . import views
app_name = 'product'
urlpatterns = [
    # Homepage
    path('', views.home, name='home'),
    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact'),
    path('404-not-found', views.page_not_found, name='page_not_found'),

    # Display products
    path('san-pham', views.products, name='products'),
    path('p', views.single_product),

    # Create Channels and Synchronize products on channels
    path('create_channel', views.create_new_channel, name='create_channel'),
    path('sync_product_view', views.sync_product_view, name='sync_product_view'),
    path('sync_product', views.sync_product, name='sync_product')
]
