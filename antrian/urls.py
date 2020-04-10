from django.conf.urls import url, include
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^create/$', views.create, name="create"),
    url(r'^jenis_pengobatan/$', views.jenis_pengobatan, name="jenis_pengobatan"),
    url(r'^update/(?P<pasien_id>[0-9]+)/$', views.update, name="update"),
    url(r'^selesai/(?P<pasien_id>[0-9]+)/$', views.selesai, name="selesai"),
    url(r'^delete/(?P<pasien_id>[0-9]+)/$', views.delete, name="delete"),
]