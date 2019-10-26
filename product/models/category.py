from django.db import models

import logging
_logger = logging.getLogger(__name__)

class Category(models.Model):

    name = models.CharField(max_length=255, default='General')
    id_on_channel = models.CharField(max_length=255, default=0)

    def __str__(self):
        return self.name