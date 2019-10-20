from django.db import models

import logging
_logger = logging.getLogger(__name__)

class Category(models.Model):

    name = models.CharField(max_length=255, unique=True)


    def __str__(self):
        return self.name