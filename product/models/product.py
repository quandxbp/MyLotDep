from django.db import models

from .ecommerce_channel import EcommerceChannel
from .category import Category
from .brand import Brand
from .related_product import RelatedProduct

# Import model in Each Channel
from product_tiki.models.product import TikiProduct
from product_adayroi.models.product import AdayroiProduct

from decimal import Decimal
from urllib.request import urlopen
from urllib.parse import urlparse
from django.core.files import File
from io import BytesIO


class Product(TikiProduct, AdayroiProduct):
    active = models.BooleanField(default=True)
    name = models.CharField(max_length=255, blank=True)
    product_id = models.CharField(max_length=255, blank=True)
    seller_product_id = models.CharField(max_length=255, blank=True)
    sku = models.CharField(max_length=255, blank=True)
    seller_sku = models.CharField(max_length=255, blank=True)
    quantity = models.IntegerField(default=0)
    url = models.URLField(max_length=500, blank=True)
    accesstrade_url = models.URLField(blank=True)
    thumbnail = models.ImageField(upload_to="images/%Y/%m/%D/", default='images/%Y/%m/%D/no-img.jpg')
    # Pricing
    price = models.DecimalField(max_digits=20, decimal_places=4, default=Decimal('0.0000'))
    list_price = models.DecimalField(max_digits=20, decimal_places=4, default=Decimal('0.0000'))
    discount = models.DecimalField(max_digits=20, decimal_places=4, default=Decimal('0.0000'))

    meta_description = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True)

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
    related_product_id = models.ManyToManyField(RelatedProduct)

    def __str__(self):
        return "[%s] %s" % (self.sku, self.name) if self.sku else self.name

    @classmethod
    def sync_product_channel(cls, products_data):
        print("Syncing data on channel")
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
                categ_data = {'name': 'General'}
            try:
                categ_id = Category.objects.get(name=categ_data.get('name'))
            except Category.DoesNotExist:
                categ_id = Category.objects.create(**{
                    'name': categ_data.get('name'),
                })

            return categ_id

        def get_thumbnail(thumbnail_url, product):
            try:
                thumb_name = urlparse(thumbnail_url).path.split('/')[-1]
                thumb_content = BytesIO(urlopen(thumbnail_url).read())
            except Exception as err:
                thumbnail_url = 'http://cdh.vnu.edu.vn/templates/not-found.png'
                thumb_name = urlparse(thumbnail_url).path.split('/')[-1]
                thumb_content = BytesIO(urlopen(thumbnail_url).read())
            return thumb_name, File(thumb_content)

        for product in products_data:
            cust_method_name = '%s_standardize_data' % product.get('channel_id').platform
            if hasattr(cls, cust_method_name):
                method = getattr(cls, cust_method_name)
                standardize_product = method(cls, product)

                standardize_product['brand_id'] = get_brand(standardize_product.get('brand', False))
                standardize_product['category_id'] = get_category(standardize_product.get('category', False))
                thumb_name, thumb_content = get_thumbnail(standardize_product['thumbnail_url'], standardize_product)

                for k, v in standardize_product.copy().items():
                    if k not in product_fields or k == 'id':
                        del standardize_product[k]

                try:
                    existed_product = Product.objects.get(product_id=standardize_product.get('product_id'))
                except Product.DoesNotExist:
                    print("Create product %s" % standardize_product.get('name'))
                    new_product = Product(**standardize_product)
                    # Create thumbnail
                    new_product.thumbnail.save(thumb_name, thumb_content)
                    new_product.save()


