# Generated by Django 2.2.5 on 2019-11-22 17:14

from decimal import Decimal
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AccessTrade',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('accesstrade_access_key', models.CharField(blank=True, default='hIAO1n_PcfcRwUIKcpMqnJneuGQ-YrtC', max_length=255)),
                ('accesstrade_secret_key', models.CharField(blank=True, default='obzlw+lj@f5)orhvn95-(f@t2pg_srm0', max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('slug', models.CharField(blank=True, max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='General', max_length=255)),
                ('id_on_channel', models.CharField(default=0, max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='EcommerceChannel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('platform', models.CharField(choices=[('tiki', 'Tiki'), ('lazada', 'Lazada'), ('adayroi', 'Adayroi')], default='tiki', max_length=50)),
                ('access_trade_id', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='product.AccessTrade', verbose_name='Access Trade')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True)),
                ('name', models.CharField(blank=True, max_length=255)),
                ('product_id', models.CharField(blank=True, max_length=255)),
                ('seller_product_id', models.CharField(blank=True, max_length=255)),
                ('sku', models.CharField(blank=True, max_length=255)),
                ('seller_sku', models.CharField(blank=True, max_length=255)),
                ('quantity', models.IntegerField(default=0)),
                ('url', models.URLField(blank=True, max_length=500)),
                ('url_path', models.URLField(blank=True, max_length=500)),
                ('accesstrade_url', models.URLField(blank=True)),
                ('thumbnail_url', models.CharField(blank=True, max_length=500)),
                ('sale_price', models.DecimalField(decimal_places=0, default=Decimal('0'), max_digits=20)),
                ('list_price', models.DecimalField(decimal_places=0, default=Decimal('0'), max_digits=20)),
                ('discount', models.DecimalField(decimal_places=0, default=Decimal('0'), max_digits=20)),
                ('discount_rate', models.IntegerField(default=0)),
                ('meta_description', models.TextField(blank=True, null=True)),
                ('description', models.TextField(blank=True)),
                ('has_past_price', models.IntegerField(default=1)),
                ('sequence', models.IntegerField(default=0)),
                ('screen_technology', models.CharField(blank=True, max_length=255)),
                ('ram_memory', models.CharField(blank=True, max_length=255)),
                ('rom_memory', models.CharField(blank=True, max_length=255)),
                ('front_camera', models.CharField(blank=True, max_length=255)),
                ('rear_camera', models.CharField(blank=True, max_length=255)),
                ('recording', models.CharField(blank=True, max_length=255)),
                ('weight', models.CharField(blank=True, max_length=255)),
                ('dimension', models.CharField(blank=True, max_length=255)),
                ('chip', models.CharField(blank=True, max_length=255)),
                ('gpu', models.CharField(blank=True, max_length=255)),
                ('pin_capacity', models.CharField(blank=True, max_length=255)),
                ('brand_id', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='product.Brand', verbose_name='Brand')),
                ('category_id', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='product.Category', verbose_name='Category')),
                ('channel_id', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='product.EcommerceChannel', verbose_name='ECommerce Channel')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Provider',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_on_channel', models.CharField(max_length=255, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('url', models.CharField(blank=True, max_length=255)),
                ('logo', models.CharField(blank=True, max_length=255)),
                ('is_best_store', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Specification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255)),
                ('value', models.CharField(blank=True, max_length=255)),
                ('product_id', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='product.Product', verbose_name='Product')),
            ],
        ),
        migrations.CreateModel(
            name='RelatedProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_id', models.CharField(blank=True, max_length=255)),
                ('main_product_id', models.CharField(blank=True, max_length=255)),
                ('platform', models.CharField(blank=True, max_length=255)),
                ('url_path', models.CharField(blank=True, max_length=255)),
                ('ld_url', models.CharField(blank=True, max_length=255)),
                ('related_product_id', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='product.Product', verbose_name='Product')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='provider_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='product.Provider', verbose_name='Provider'),
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255)),
                ('url', models.URLField()),
                ('image', models.ImageField(upload_to='images/%Y/%m/%D/')),
                ('description', models.TextField(blank=True)),
                ('product_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='product.Product', verbose_name='Products')),
            ],
        ),
    ]
