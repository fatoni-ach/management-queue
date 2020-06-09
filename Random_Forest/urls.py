"""Random_Forest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^pttp/', include('pttp.urls', namespace="pttp")),
    url(r'^login/$', views.login_view , name="login"),
    url(r'^logout/$', views.logout_view , name="logout"),
    url(r'^reset/$', views.reset , name="reset"),
    url(r'^data-antrian/$', views.data_antrian , name="data_antrian"),
    url(r'^poli/(?P<jenis_pengobatan>[\w-]+)/$', views.poli , name="poli"),
    url(r'^antrian/', include('antrian.urls', namespace="antrian")),
    url(r'^api/request/', include('api.urls', namespace="api")),
    url(r'^$', views.index, name="index"),
]
