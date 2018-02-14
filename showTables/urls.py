from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^(?P<period>[0-9]{2}[OE]{1})$', views.index, name='index'),
]