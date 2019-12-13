from django.urls import path

from . import views
app_name = 'ner'

urlpatterns = [
    # Homepage
    path('ner', views.test, name='test'),

]
