from django.db import models

class RelatedProduct(models.Model):

    id_on_channel = models.CharField(max_length=255, default=1)

    class Meta:
        app_label = 'productdb'