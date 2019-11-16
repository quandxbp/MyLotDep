from django.db import models


class Provider(models.Model):
    id_on_channel = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    url = models.CharField(max_length=255, blank=True)
    logo = models.CharField(max_length=255, blank=True)
    is_best_store = models.BooleanField()

    def __str__(self):
        return self.name