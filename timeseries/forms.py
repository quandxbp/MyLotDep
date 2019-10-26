from django.db import models
from django import forms


source_choices = (
    ('beetracker', 'BeeTracker'),
    ('jajum', 'JaJum')
)

class SyncPriceForm(forms.Form):
    source = forms.ChoiceField(choices=source_choices, required=True)
