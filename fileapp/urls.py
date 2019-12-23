from django.conf.urls import url
from . import views

app_name = 'fileapp'

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^uploads/simple/$', views.simple_upload, name='simple_upload'),
    url(r'^search/$', views.search, name='search'),
]