from django.db import models
from django.contrib.staticfiles import finders

from .ecommerce_channel import EcommerceChannel
from .category import Category
from .brand import Brand
from .provider import Provider

# Import model in Each Channel
from product_tiki.models.product import TikiProduct
from product_adayroi.models.product import AdayroiProduct

from decimal import Decimal

import logging


class Product(TikiProduct, AdayroiProduct):
    active = models.BooleanField(default=True)
    name = models.CharField(max_length=255, blank=True)
    product_id = models.CharField(max_length=255, blank=True)
    seller_product_id = models.CharField(max_length=255, blank=True)
    sku = models.CharField(max_length=255, blank=True)
    seller_sku = models.CharField(max_length=255, blank=True)
    quantity = models.IntegerField(default=0)
    url = models.URLField(max_length=500, blank=True)
    url_path = models.URLField(max_length=500, blank=True)
    accesstrade_url = models.URLField(blank=True)
    thumbnail_url = models.CharField(max_length=500, blank=True)
    # Pricing
    sale_price = models.DecimalField(max_digits=20, decimal_places=0, default=Decimal('0'))
    list_price = models.DecimalField(max_digits=20, decimal_places=0, default=Decimal('0'))
    discount = models.DecimalField(max_digits=20, decimal_places=0, default=Decimal('0'))
    discount_rate = models.IntegerField(default=0)

    meta_description = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True)
    has_past_price = models.IntegerField(default=1)
    # sequence = 1 : main product
    # sequence = 2 : related product
    sequence = models.IntegerField(default=0)

    # Necessary Specifications
    screen_technology = models.CharField(max_length=255, blank=True)

    ram_memory = models.CharField(max_length=255, blank=True)
    rom_memory = models.CharField(max_length=255, blank=True)

    front_camera = models.CharField(max_length=255, blank=True)
    rear_camera = models.CharField(max_length=255, blank=True)
    recording = models.CharField(max_length=255, blank=True)

    weight = models.CharField(max_length=255, blank=True)
    dimension = models.CharField(max_length=255, blank=True)

    chip = models.CharField(max_length=255, blank=True)

    gpu = models.CharField(max_length=255, blank=True)

    pin_capacity = models.CharField(max_length=255, blank=True)

    # Other specification

    channel_id = models.ForeignKey(EcommerceChannel,
                                   default=1,
                                   verbose_name="ECommerce Channel",
                                   on_delete=models.CASCADE)
    brand_id = models.ForeignKey(Brand,
                                 default=1,
                                 verbose_name="Brand",
                                 on_delete=models.CASCADE)
    category_id = models.ForeignKey(Category,
                                    default=1,
                                    verbose_name="Category",
                                    on_delete=models.CASCADE)
    provider_id = models.ForeignKey(Provider,
                                    default=1,
                                    verbose_name="Provider",
                                    on_delete=models.CASCADE)

    def __str__(self):
        return "[%s] %s" % (self.sku, self.name) if self.sku else self.name

    def sync_product_channel(self, uid, products_data):
        print("Running in Worker %s" % uid)
        product_fields = [f.name for f in Product._meta.fields]

        def get_brand(brand_data):
            if not brand_data:
                brand_data = {
                    'name': 'General',
                    'slug': 'general'
                }
            try:
                brand_id = Brand.objects.get(name=brand_data.get('name'))
            except Brand.DoesNotExist:
                brand_id = Brand.objects.create(**{
                    'name': brand_data.get('name'),
                    'slug': brand_data.get('slug')
                })

            return brand_id

        def get_category(categ_data):
            if not categ_data:
                categ_data = {'name': 'General', 'id_on_channel': '0'}
            try:
                categ_id = Category.objects.get(name=categ_data.get('name'), id_on_channel=str(categ_data.get('id')))
            except Category.DoesNotExist:
                categ_id = Category.objects.create(**{
                    'name': categ_data.get('name'),
                    'id_on_channel': categ_data.get('id', "-1")
                })

            return categ_id

        def get_provider(provider_data):
            if not provider_data:
                provider_data = {'id_on_channel': '0',
                                 'name': 'General Provider',
                                 'url': ' ',
                                 'logo': ' ',
                                 'is_best_store': False}
            try:
                provider_id = Provider.objects.get(name=provider_data.get('name'), id_on_channel=str(provider_data.get('id')))
            except Provider.DoesNotExist:
                provider_id = Provider.objects.create(**{
                    'name': provider_data.get('name'),
                    'id_on_channel': provider_data.get('id', "-1"),
                    'url': provider_data.get('url'),
                    'logo': provider_data.get('logo'),
                    'is_best_store': provider_data.get('is_best_store')
                })

            return provider_id

        def get_specification(specification, new_product):
            from .specification import Specification
            for spec in specification:
                new_spec = Specification(name=spec.get('name'),
                                         value=spec.get('value'),
                                         product_id=new_product)
                new_spec.save()

        def get_related_products(related_products, new_product):
            from .related_product import RelatedProduct
            for rlp in related_products:
                new_related_product = RelatedProduct(product_id=rlp.get('product_id'),
                                                     main_product_id=rlp.get('main_product_id'),
                                                     url_path=rlp.get('url_path'),
                                                     platform=rlp.get('platform'),
                                                     related_product_id=new_product)
                new_related_product.save()

        for product in products_data:
            cust_method_name = '%s_standardize_data' % product.get('channel_id').platform
            if hasattr(self, cust_method_name):
                method = getattr(self, cust_method_name)
                standardize_product = method(product)

                if standardize_product.get('inventory_status') != 'available':
                    continue

                standardize_product['brand_id'] = get_brand(standardize_product.get('brand', False))
                standardize_product['category_id'] = get_category(standardize_product.get('category', False))
                standardize_product['provider_id'] = get_provider(standardize_product.get('provider', False))
                specification = standardize_product.get('specification')
                related_products = standardize_product.get('related_products')

                for k, v in standardize_product.copy().items():
                    if k not in product_fields or k == 'id':
                        del standardize_product[k]

                try:
                    try:
                        exsted_product = Product.objects.get(seller_product_id=standardize_product.get('seller_product_id'))
                    except Product.DoesNotExist:
                        logging.info("Create product %s" % standardize_product.get('name'))
                        new_product = Product(**standardize_product)
                        new_product.save()
                        get_specification(specification, new_product)
                        get_related_products(related_products, new_product)
                except Exception as err:
                    logging.error("ERROR: %s" % err)

    def update_data_product_channel(self, products_data, update_mongo=False):
        from timeseries.models.time_price import TimePrice
        TP = TimePrice()

        for product in products_data:
            cust_method_name = '%s_standardize_data' % product.get('channel_id').platform
            if hasattr(self, cust_method_name):
                method = getattr(self, cust_method_name)
                p = method(product)

                try:
                    Product.objects.filter(pk=p.get('id')).update(sale_price=p.get('sale_price'),
                                                                  list_price=p.get('list_price'),
                                                                  discount=p.get('discount'),
                                                                  discount_rate=p.get('discount_rate'))

                    if update_mongo:
                        try:
                            logging.info("Updating data in Mongo: %s" % p.get('product_id'))
                            TP.update_price(product=p, price=p.get('sale_price'))
                        except Exception as err:
                            logging.error('Error when updating product price in mongo')
                            logging.error(err)

                except Exception as err:
                    logging.error('Error when updating product price')
                    logging.error(err)

    def update_data_product_channel_mongo(self, products_data, update_sql=False):
        from timeseries.models.time_price import TimePrice
        TP = TimePrice()

        for product in products_data:
            cust_method_name = '%s_standardize_data' % product.get('platform')
            if hasattr(self, cust_method_name):
                method = getattr(self, cust_method_name)
                p = method(product)

                try:
                    logging.info("Updating data in Mongo: %s" % p.get('product_id'))
                    TP.update_price(product=p, price=p.get('sale_price'))

                    if update_sql:
                        try:
                            Product.objects.filter(pk=p.get('id')).update(sale_price=p.get('sale_price'),
                                                                          list_price=p.get('list_price'),
                                                                          discount=p.get('discount'),
                                                                          discount_rate=p.get('discount_rate'))
                        except Exception as err:
                            logging.error('Error when updating product price SQL')
                            logging.error(err)
                except Exception as err:
                    logging.error('Error when updating product price in mongo')
                    logging.error(err)