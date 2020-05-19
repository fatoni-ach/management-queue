from django.conf.urls import url, include
from . import views

urlpatterns=[
    # url(r'^$', views.index, name="index"),
    url(r'^add/$', views.TambahAntrian.as_view(), name='tambah-antrian'),
    url(r'^list/$', views.list_pasien, name='list'),
    url(r'^datapasien/$', views.datapasien, name='datapasien'),
    url(r'^adddatapasien/$', views.adddatapasien, name='adddatapasien'),
    url(r'^addnoantrian/$', views.addnoantrian, name='addnoantrian'),
    url(r'^getStatus/$', views.getStatus, name='getStatus'),
]