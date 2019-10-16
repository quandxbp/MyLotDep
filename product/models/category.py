from django.db import models

import logging
_logger = logging.getLogger(__name__)

class Category(models.Model):

    name = models.CharField(max_length=255, unique=True)

    class Meta:
        app_label = 'productdb'

    def __str__(self):
        return self.name