from django.conf.urls import url, include
from . import views

urlpatterns=[
    # url(r'^$', views.index, name="index"),
    url(r'^add/$', views.TambahAntrian.as_view(), name='tambah-antrian'),
    url(r'^list/$', views.list_pasien, name='list'),
]