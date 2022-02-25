from django.urls import path
from django.conf.urls import  url

from . import views

urlpatterns = [
    path(r'', views.SetGetData.as_view(), name='data'),
    url(r'^expire/$', views.set_expire, name='expire'),
    url(r'^zadd/$', views.add_zdata, name='zadd'),
    url(r'^zrank/$', views.get_zrank, name='zrank'),
    url(r'^zrange/$', views.get_zrange, name='zrange'),
    url(r'^clear/$', views.clear, name='clear'),
]