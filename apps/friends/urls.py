from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^friends$', views.friends),
    url(r'^users/(?P<id>\d+)$', views.profile),
    url(r'^users/add/(?P<id>\d+)$', views.add),
    url(r'^users/remove/(?P<id>\d+)$', views.remove)
]
