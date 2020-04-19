from django.conf.urls import url, include
from . import views

urlpatterns = [
    # url(r'^training/$', views.training , name="training"),
    url(r'^testing/$', views.testing , name="testing"),
    # url(r'^coba/$', views.coba , name="coba"),
    url(r'^export/$', views.export , name="export"),
    url(r'^export_iris/(?P<tipe>[\w-]+)/$', views.export_iris , name="export_iris"),
    url(r'^convert_time/$', views.convert_time , name="convert_time"),
    url(r'^training/(?P<tipe>[\w-]+)/$', views.database , name="database"),
    url(r'^get_duration/$', views.get_duration , name="get_duration"),
    url(r'^training/$', views.index , name="index"),
]
