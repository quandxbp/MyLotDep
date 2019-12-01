from django.urls import path

from . import views
app_name = 'forecast'

urlpatterns = [
    # Homepage
    path('prophet', views.price_forecast, name='prophet'),

]
