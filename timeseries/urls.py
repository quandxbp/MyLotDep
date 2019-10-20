from django.urls import path

from . import views
app_name = 'timeseries'

urlpatterns = [
    path('test', views.test, name='test'),
]