from django.db import models
from django import forms

from .models.ecommerce_channel import EcommerceChannel


class SyncChannelForm(forms.Form):
    channel = forms.ModelChoiceField(queryset=EcommerceChannel.objects.all(), required=True)
    is_top_product = forms.BooleanField()
