from django.conf.urls import url
from . import views
app_name = "delivery"


urlpatterns = [
    url(r'^searchShipment/', views.searchShipment, name='searchShipment'),
    url(r'^overviewShipment/', views.overviewShipment, name='overviewShipment'),
    url(r'^detailShipment/(?P<pk>[0-9]+)$', views.detailShipment, name='detailShipment'),
]
