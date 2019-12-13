from django.db import models


class ProductTemplate(models.Model):
    name = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name